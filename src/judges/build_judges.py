"""Judges: registry, drafter (redattore) of each pronuncia, and collegio.

Outputs
  data/processed/judges.csv            one row per judge, with mandate dates
  data/processed/pronunce_judges.csv   relatore, redattore(s), source of the redattore, collegio size
  data/processed/collegio.csv          one row per (pronuncia, sitting judge)
  reports/judges_quality.md            matching rates against the fixed thresholds

Redattore source (docs/context.md, section 5):
  field           the XML field (from 2002)
  signature       "Il redattore: X" / "X, Redattore" at the end of the text (287/1986 - 2001)
  relatore_proxy  the relatore, for pronunce up to 286/1986 (declared approximation)

Usage: .venv/bin/python src/judges/build_judges.py
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd
from lxml import etree

REPO = Path(__file__).resolve().parents[2]
SWITCH = 19860287  # first pronuncia signed by President and redattore only
NAME_FIX = {"CAIANELLO": "CAIANIELLO", "CAPOLOZZA": "CAPALOZZA"}  # spelling errors in the files (sparql_reconciliation.md)


def key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\b(PROF|DOTT|AVV|SSA|ON)\b\.?", " ", s)
    s = re.sub(r"[^A-Z ]", " ", s.replace("'", ""))
    s = re.sub(r"\s+", " ", s).strip()
    for a, b in NAME_FIX.items():
        s = s.replace(a, b)
    return s


def load_registry() -> pd.DataFrame:
    path = REPO / "data/raw/giudici/Cc_Opendata_AnagraficaGiudici/Cc_Opendata_AnagraficaGiudici.xml"
    g = pd.DataFrame([{c.tag: (c.text or "").strip() for c in x} for x in etree.parse(str(path)).getroot()])
    g = g[~g.Nome_Cognome.str.contains(" - ")].reset_index(drop=True)
    g["judge_id"] = range(1, len(g) + 1)
    for c in ["data_nomina", "data_giuramento", "data_cessazione"]:
        g[c] = pd.to_datetime(g[c], format="%d/%m/%Y", errors="coerce")
    g["surname"] = g.Cognome.str.replace(r"\s+[A-Z]\.(\s*[A-Z]\.)*$", "", regex=True).map(key)
    g.loc[g.surname == "GABRIELI PANTALEO", "surname"] = "PANTALEO GABRIELI"  # as written in the texts
    g["first"] = g.Nome.map(key)
    g["full"] = g.Nome_Cognome.map(key)
    # the registry writes "Francesco Gabrieli Pantaleo": the texts say "Francesco Pantaleo Gabrieli"
    g["eletto_da"] = g.Eletto_da.str.replace("Corte dei Conti", "Corte dei conti")
    g["end_source"] = "registry"
    # declared fixes (docs/decisions.md, 2026-11-16)
    g.loc[g.surname == "SPAGNOLI", ["data_cessazione", "end_source"]] = [pd.Timestamp("1995-02-25"), "corrected (official list)"]
    missing = g.data_cessazione.isna()
    g.loc[missing, "data_cessazione"] = g.loc[missing, "data_giuramento"] + pd.DateOffset(years=9)
    g.loc[missing, "end_source"] = "giuramento + 9 years (art. 135 Cost.)"
    return g


def main() -> None:
    df = pd.read_pickle(REPO / "data/interim/pronunce.pkl")
    g = load_registry()
    df["dec"] = df.data_decisione.fillna(df.data_deposito)

    # The registry end dates are unreliable (missing for 33 judges, wrong for others, e.g.
    # Granata, Chiarelli, Mezzanotte). For matching names a judge is a candidate from the oath
    # to 13 years later (the longest mandates lasted 12 years); the surname must still appear.
    def in_office(date):
        return g[(g.data_giuramento - pd.Timedelta(days=5) <= date) & (date <= g.data_giuramento + pd.DateOffset(years=13))]

    def match_person(name: str, date) -> list[int]:
        """Judge ids for a name string (possibly several names joined by ' - ')."""
        ids = []
        for part in re.split(r"\s+-\s+", name or ""):
            k = key(part)
            if not k:
                continue
            cand = in_office(date)
            hit = cand[cand.surname.map(lambda s: re.search(r"\b" + re.escape(s) + r"$", k) is not None or k == s)]
            if len(hit) > 1:
                hit2 = hit[hit["first"].map(lambda f: f != "" and f.split()[0] in k)]
                hit = hit2 if len(hit2) else hit
            if len(hit) != 1:  # fall back to all judges, any time
                allhit = g[g.full == k]
                hit = allhit if len(allhit) == 1 else hit
            ids.append(int(hit.judge_id.iloc[0]) if len(hit) == 1 else 0)
        return ids

    sig1 = re.compile(r"(?:Presidente e\s+)?(?:redattore|relatore)\s*:\s*([A-Za-zÀ-ÿ' ]+?)\s*(?=Il\s|Cancelliere|Depositata|Presidente|$)", re.I)
    sig2 = re.compile(r"([A-ZÀ-Ýa-zà-ÿ' ]+?),\s*Redatt(?:ore|rice)", re.U)
    rows, coll_rows = [], []
    surname_re = {r.judge_id: re.compile(r"\b" + re.escape(r.surname) + r"\b") for r in g.itertuples()}
    for r in df.itertuples():
        rel = match_person(r.relatore_pronuncia, r.dec)
        red, source = [], ""
        if r.redattore_pronuncia:
            red, source = match_person(r.redattore_pronuncia, r.dec), "field"
        elif r.pid >= SWITCH:
            names = sig1.findall(r.firme) or [m for m in sig2.findall(r.firme)]
            if names:
                names = [re.sub(r"^.*\b(?:Presidente|F\.to:?)\s*", "", n).strip() for n in names]
                red, source = [i for n in names for i in match_person(n, r.dec)], "signature"
        if not red or 0 in red:
            if r.pid < SWITCH:
                red, source = rel, "relatore_proxy"
            elif not red:
                red, source = [], "none"
        # collegio: judges in office whose surname appears in the collegio text
        ck = key(r.collegio)
        cand = in_office(r.dec)
        sitting = []
        for j in cand.itertuples():
            if surname_re[j.judge_id].search(ck):
                same = cand[cand.surname == j.surname]
                if len(same) > 1 and j.first.split()[0] not in ck:
                    continue
                sitting.append(j.judge_id)
        coll_rows += [(r.pid, j) for j in sitting]
        n_listed = len([p for p in re.split(r"\s+-\s+|,\s*|;\s*", re.sub(
            r"^.*?composta da(?:i signori|i giudici)?\s*:?\s*|Presidente\s*:\s*|,\s*Presidente|;?\s*Giudici\s*:?\s*,?", " ",
            r.collegio, flags=re.I)) if re.search(r"[A-ZÀ-Ý]{3,}", p)])
        rows.append(dict(pid=r.pid, relatore_id=rel[0] if len(rel) == 1 else 0,
                         relatore_ids="|".join(map(str, rel)), redattore_ids="|".join(map(str, red)),
                         n_redattori=len(red), redattore_source=source, n_collegio=len(sitting), n_listed=n_listed))
    pj = pd.DataFrame(rows)
    coll = pd.DataFrame(coll_rows, columns=["pid", "judge_id"])
    proc = REPO / "data/processed"
    g[["judge_id", "Nome_Cognome", "surname", "eletto_da", "data_nomina", "data_giuramento", "data_cessazione",
       "end_source", "Nota_biografica"]].to_csv(proc / "judges.csv", index=False)
    pj.to_csv(proc / "pronunce_judges.csv", index=False)
    coll.to_csv(proc / "collegio.csv", index=False)

    # ---------------- quality report
    pj = pj.merge(df[["pid", "anno", "tipo"]], on="pid")
    pj["decade"] = pj.anno // 10 * 10
    red_ok = pj.redattore_ids.map(lambda s: s != "" and "0" not in s.split("|"))
    coll_ok = pj.n_collegio.between(11, 15) & (pj.n_collegio >= pj.n_listed)
    pct = lambda x: f"{100 * x:.2f}%".replace(".", ",")  # Italian format
    pct1 = lambda x: f"{100 * x:.1f}%".replace(".", ",")
    num = lambda x: f"{x:,}".replace(",", ".")
    src = pj.redattore_source.value_counts().to_dict()
    out = ["# Giudici: quanto bene sono stati riconosciuti\n",
           "Prodotto da `src/judges/build_judges.py`. Per ogni pronuncia il programma cerca chi l'ha scritta (il redattore), chi l'ha "
           "seguita come relatore e chi sedeva nel collegio, e collega ogni nome all'elenco ufficiale dei giudici pubblicato dalla Corte.\n",
           "## Le misure principali\n",
           f"- Pronunce in cui il nome di chi ha scritto è stato collegato all'elenco dei giudici: **{pct(red_ok.mean())}** "
           "(soglia decisa prima: 98%).",
           f"- Da dove viene il nome di chi ha scritto: dal campo dei dati in {num(src.get('field', 0))} pronunce; dalla firma in fondo al "
           f"testo in {num(src.get('signature', 0))}; dal relatore, usato al suo posto fino alla 286/1986, in {num(src.get('relatore_proxy', 0))}; "
           f"in {num(src.get('none', 0))} non c'è.",
           f"- Pronunce con il collegio riconosciuto per intero, cioè con un numero di giudici tra 11 e 15, tutti collegati all'elenco e "
           f"non meno dei nomi scritti nel testo: **{pct(coll_ok.mean())}** (soglia decisa prima: 98%). Senza il confronto con i nomi "
           f"scritti nel testo: {pct(pj.n_collegio.between(11, 15).mean())}.",
           f"- Pronunce scritte da più giudici insieme: {(pj.n_redattori > 1).sum()}.",
           f"- Pronunce in cui il nome del relatore è stato collegato all'elenco: "
           f"{pct((pj.relatore_ids.map(lambda s: s != '' and '0' not in s.split('|'))).mean())}.\n",
           "## Per decennio\n",
           "| Decennio | Chi ha scritto: nome collegato | Collegio riconosciuto per intero | Giudici per collegio, in media |",
           "| --- | --- | --- | --- |"]
    for d, x in pj.groupby("decade"):
        mean = f"{x.n_collegio.mean():.2f}".replace(".", ",")
        out.append(f"| anni {d} | {pct1(red_ok[x.index].mean())} | {pct1(coll_ok[x.index].mean())} | {mean} |")
    out += ["\n## Quanti giudici sono stati riconosciuti in ogni collegio\n",
            "Il collegio decide con almeno 11 giudici (il numero legale): un numero più basso vuol dire che il programma non ha "
            "riconosciuto tutti i nomi.\n",
            "| Giudici riconosciuti nel collegio | Pronunce |", "| --- | --- |"]
    out += [f"| {k} | {num(v)} |" for k, v in pj.n_collegio.value_counts().sort_index().items()]
    last = coll.merge(df[["pid", "dec"]], on="pid").groupby("judge_id").dec.agg(["min", "max", "size"])
    chk = g.set_index("judge_id").join(last)
    chk["gap_end_days"] = (chk.data_cessazione - chk["max"]).dt.days
    odd = chk[(chk.gap_end_days > 400) | (chk["size"].isna())]
    end_label = {"registry": "dall'elenco ufficiale", "giuramento + 9 years (art. 135 Cost.)": "calcolata: giuramento più 9 anni",
                 "corrected (official list)": "corretta sull'elenco del sito della Corte"}
    out += ["\n## Giudici da controllare\n",
            "Giudici che non compaiono in nessun collegio, o la cui ultima presenza in un collegio è più di 400 giorni prima della fine "
            "del mandato. Per i giudici ancora in carica è normale: il mandato non è finito. Quando l'elenco ufficiale non dà la fine del "
            "mandato, la data è calcolata come giuramento più 9 anni, la durata fissata dalla Costituzione (art. 135).\n"]
    out += [f"- {r.Nome_Cognome}: giuramento {r.data_giuramento:%d/%m/%Y}; fine del mandato {r.data_cessazione:%d/%m/%Y} "
            f"({end_label.get(r.end_source, r.end_source)}); ultima presenza in un collegio {r['max']:%d/%m/%Y}."
            if pd.notna(r['max']) else f"- {r.Nome_Cognome}: non compare in nessun collegio."
            for _, r in odd.iterrows()]
    (REPO / "reports/judges_quality.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
