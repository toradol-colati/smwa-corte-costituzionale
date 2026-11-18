"""Inspect the raw Constitutional Court archives and write reports/data_inspection.md.

Descriptive checks only (structure, coverage, consistency), no network analysis.
Every number quoted in docs/context.md and docs/data_schema.md comes from here.

Usage (from the repository root, after src/ingest/download.py):
    python3 src/ingest/inspect_raw.py
"""

from __future__ import annotations

import csv
import glob
import re
import unicodedata
from pathlib import Path

import pandas as pd
from lxml import etree

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "data" / "raw"
REPORT = REPO_ROOT / "reports" / "data_inspection.md"

HEADER_FIELDS = [
    "anno_pronuncia", "numero_pronuncia", "ecli", "tipologia_pronuncia", "presidente",
    "relatore_pronuncia", "redattore_pronuncia", "data_decisione", "data_deposito",
]


# ---------------------------------------------------------------- loading

def element_text(element) -> str:
    return "".join(element.itertext()) if element is not None else ""


def load_pronunce() -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(str(RAW / "pronunce" / "*" / "*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            head, body = p.find("pronuncia_testata"), p.find("pronuncia_testo")
            row = {k: (head.findtext(k) or "").strip() for k in HEADER_FIELDS}
            for k in ["collegio", "epigrafe", "dispositivo"]:
                row[k] = element_text(body.find(k))
            testo = body.find("testo")
            row["section_tags"] = "|".join(c.tag for c in testo)
            row["testo"] = element_text(testo)
            rows.append(row)
    df = pd.DataFrame(rows)
    df["anno"] = df.anno_pronuncia.astype(int)
    df["num"] = df.numero_pronuncia.astype(int)
    df["decade"] = df.anno // 10 * 10
    for col in ["data_decisione", "data_deposito"]:
        df[col + "_d"] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")
    return df


def load_massime() -> tuple[pd.DataFrame, pd.DataFrame]:
    pron, mass = [], []
    for path in sorted(glob.glob(str(RAW / "massime" / "*" / "*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            head = p.find("pronuncia_testata")
            anno, num = int(head.findtext("anno_pronuncia")), int(head.findtext("numero_pronuncia"))
            items = p.findall("massime/massima")
            pron.append({"anno": anno, "num": num,
                         "tipologia_pronuncia_m": (head.findtext("tipologia_pronuncia") or "").strip(),
                         "tipologia_giudizio": (head.findtext("tipologia_giudizio") or "").strip(),
                         "n_massime": len(items)})
            for m in items:
                mass.append({"anno": anno, "num": num, "id": m.findtext("numero"),
                             "titolo": (m.findtext("titolo") or "").strip(),
                             "n_parametri": len(m.findall("parametri/parametro")),
                             "n_norme": len(m.findall("norme/norma"))})
    return pd.DataFrame(pron), pd.DataFrame(mass)


def load_giudici() -> pd.DataFrame:
    path = RAW / "giudici" / "Cc_Opendata_AnagraficaGiudici" / "Cc_Opendata_AnagraficaGiudici.xml"
    rows = [{c.tag: (c.text or "").strip() for c in g} for g in etree.parse(str(path)).getroot()]
    g = pd.DataFrame(rows)
    for col in ["data_nomina", "data_giuramento", "data_cessazione"]:
        g[col + "_d"] = pd.to_datetime(g[col], format="%d/%m/%Y", errors="coerce")
    g["composite"] = g.Nome_Cognome.str.contains(" - ")
    return g


# ---------------------------------------------------------------- helpers

def md_table(frame: pd.DataFrame, index: bool = True) -> str:
    frame = frame.reset_index() if index else frame
    cols = [str(c) for c in frame.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(fmt(v) for v in row.values) + " |")
    return "\n".join(lines)


def fmt(value) -> str:
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".") if value == value else ""
    return str(value)


def ascii_upper(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().upper()


def collegio_size(raw: str) -> int:
    """Approximate number of judges listed in the collegio element.
    Heuristic for inspection only: the real extraction belongs to src/judges/."""
    text = re.sub(r"\s+", " ", raw or "").strip()
    text = re.sub(r"^LA CORTE COSTITUZIONALE\s*", "", text, flags=re.I)
    text = re.sub(r"^composta da(i signori|i giudici)?\s*:?\s*", "", text, flags=re.I)
    text = re.sub(r",?\s*Giudici\s*,?\s*$", "", text)
    text = re.sub(r"Presidente\s*:\s*", "", text)
    text = re.sub(r";?\s*Giudici\s*:\s*", ", ", text)
    text = re.sub(r",\s*Presidente", "", text)
    parts = [p for p in re.split(r"\s+-\s+|,\s*|;\s*", text) if re.search(r"[A-ZÀ-Ý]{3,}", p)]
    return len(parts)


SIGNATURE_TAIL = 900


# ---------------------------------------------------------------- report

def main() -> None:
    df = load_pronunce()
    pm, mm = load_massime()
    gj = load_giudici()
    out: list[str] = []
    w = out.append

    w("# Ispezione dei dati grezzi\n")
    w("Generato da `src/ingest/inspect_raw.py` sui file elencati in `data/raw/MANIFEST.csv`. "
      "Solo controlli descrittivi: struttura, copertura, coerenza. Non modificare a mano.\n")
    with (RAW / "MANIFEST.csv").open(encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    w("## Versione dei dati\n")
    w(md_table(pd.DataFrame(manifest)[["file", "downloaded_at", "sha256"]], index=False) + "\n")

    # --- pronunce: identifiers and numbering
    w("## Pronunce: identificativi e numerazione\n")
    by_year = df.groupby("anno").num.agg(["count", "min", "max", "nunique"])
    w(f"- Pronunce: **{len(df):,}** ({df.anno.min()}–{df.anno.max()}); "
      f"sentenze (S) {int((df.tipologia_pronuncia == 'S').sum()):,}, "
      f"ordinanze (O) {int((df.tipologia_pronuncia == 'O').sum()):,}; altri tipi: "
      f"{int((~df.tipologia_pronuncia.isin(['S', 'O'])).sum())}.")
    w(f"- Coppie anno + numero duplicate: {int(df.duplicated(['anno', 'num']).sum())}. "
      f"Anni con buchi nella numerazione: {int(((by_year['max'] != by_year['count']) | (by_year['min'] != 1)).sum())}. "
      "La numerazione è annuale e unica per sentenze e ordinanze.")
    ecli_ok = df.ecli == "ECLI:IT:COST:" + df.anno_pronuncia + ":" + df.numero_pronuncia
    w(f"- ECLI diverso da `ECLI:IT:COST:anno:numero`: {int((~ecli_ok).sum())}.")
    y_dep, y_dec = df.data_deposito_d.dt.year, df.data_decisione_d.dt.year
    w(f"- L'anno della pronuncia coincide con l'anno del deposito in tutti i casi tranne {int((df.anno != y_dep).sum())} "
      f"(errori di data: {', '.join(f'{r.num}/{r.anno} depositata il {r.data_deposito}' for r in df[df.anno != y_dep].itertuples())}); "
      f"con l'anno della decisione nel {(df.anno == y_dec).mean():.2%} dei casi. "
      f"Pronunce decise in un anno e depositate (e numerate) nell'anno dopo: {int(((df.anno == y_dep) & (df.anno != y_dec)).sum())}.")
    inversions = {}
    for col in ["data_deposito_d", "data_decisione_d"]:
        inversions[col] = int(sum((g.sort_values("num")[col].diff().dt.days < 0).sum() for _, g in df.groupby("anno")))
    w(f"- Coppie consecutive in cui il numero cresce ma la data scende: rispetto al deposito {inversions['data_deposito_d']}, "
      f"rispetto alla decisione {inversions['data_decisione_d']}. Il numero segue l'ordine del deposito.")
    per_year = df.groupby("anno").size()
    start = int(per_year.cumsum().ge(1000).idxmax())
    after_start = per_year.loc[start:]
    w(f"- La rete raggiunge 1.000 pronunce nel {start} (cumulate a fine anno: {int(per_year.cumsum()[start]):,}). "
      f"Dal {start} il numero minimo di pronunce depositate in un anno è {int(after_start.min())} ({int(after_start.idxmin())}); "
      f"l'anno in corso ({int(per_year.index.max())}, incompleto) ne conta {int(per_year.iloc[-1])}.")
    lag = (df.data_deposito_d - df.data_decisione_d).dt.days
    w(f"- Giorni tra decisione e deposito: mediana {lag.median():.0f}, 99° percentile {lag.quantile(.99):.0f}; "
      f"date di decisione mancanti {int(df.data_decisione_d.isna().sum())}; deposito prima della decisione "
      f"(errori di data) {int((lag < 0).sum())}.\n")

    # --- people in the header
    w("## Pronunce: presidente, relatore, redattore\n")
    empty = lambda s: s.fillna("").str.strip() == ""
    fill = pd.DataFrame({
        "presidente vuoto": empty(df.presidente), "relatore vuoto": empty(df.relatore_pronuncia),
        "redattore vuoto": empty(df.redattore_pronuncia)}).groupby(df.decade).mean()
    w("Quota di campi vuoti per decennio:\n")
    w(md_table(fill.round(3)) + "\n")
    red_by_year = empty(df.redattore_pronuncia).groupby(df.anno).mean()
    w("Campo `redattore_pronuncia` vuoto, anni di passaggio: " +
      ", ".join(f"{y}: {v:.0%}" for y, v in red_by_year.loc[1999:2004].items()) + ".\n")
    tail = df.dispositivo.fillna("").str[-SIGNATURE_TAIL:]
    df["sig_redattore"] = tail.str.contains(r"redattor|redattric", case=False)
    first_switch = df[df.sig_redattore].sort_values(["anno", "num"]).iloc[0]
    before = df[(df.anno < first_switch.anno) | ((df.anno == first_switch.anno) & (df.num < first_switch.num))]
    after = df.drop(before.index)
    w("Firme in fondo al dispositivo:\n")
    w(f"- Fino a {first_switch.num - 1}/{first_switch.anno} la pronuncia è firmata da tutti i giudici del collegio; "
      f"il redattore non è indicato in nessun punto. Pronunce di quel periodo che nominano un redattore nelle firme: "
      f"{int(before.sig_redattore.sum())}.")
    w(f"- Da {first_switch.num}/{first_switch.anno} (decisa il {first_switch.data_decisione}, depositata il "
      f"{first_switch.data_deposito}) firmano il Presidente e il redattore (\"Il redattore: …\", poi \"…, Redattore\" "
      f"o \"Redattrice\"). Pronunce successive senza redattore nelle firme: {int((~after.sig_redattore).sum())}, "
      "per lo più ordinanze lette in udienza e firmate dal solo Presidente.")
    both = df[~empty(df.relatore_pronuncia) & ~empty(df.redattore_pronuncia)]
    norm = lambda s: s.str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    differ = both[norm(both.relatore_pronuncia) != norm(both.redattore_pronuncia)]
    multi = df[df.redattore_pronuncia.str.contains(" - ", regex=False)]
    w(f"- Con entrambi i campi compilati ({len(both):,} pronunce), relatore diverso dal redattore: {len(differ)} "
      f"(per decennio: {differ.groupby('decade').size().to_dict()}).")
    w(f"- Pronunce con più redattori (nomi separati da \" - \"): {len(multi)}, dal {multi.anno.min()} al {multi.anno.max()}.")
    w(f"- Stringhe distinte: relatore {df.relatore_pronuncia.nunique()}, redattore {df.redattore_pronuncia.nunique()}, "
      f"presidente {df.presidente.nunique()} (il presidente è indicato col solo cognome).\n")

    # --- collegio
    df["n_collegio"] = df.collegio.map(collegio_size)
    w("## Pronunce: collegio\n")
    w("Numero di giudici nell'elemento `collegio`, stima con un'euristica (da rifare in `src/judges/`):\n")
    bins = pd.cut(df.n_collegio, [-1, 10, 12, 15, 99], labels=["≤10 (da controllare)", "11–12", "13–15", ">15 (da controllare)"])
    w(md_table(pd.crosstab(df.decade, bins)) + "\n")
    w(f"- Collegi con 11 o 12 giudici: {int(df.n_collegio.isin([11, 12]).sum()):,} "
      f"({df.n_collegio.isin([11, 12]).mean():.1%}). Sono validi: il numero legale è 11 (art. 16, legge 87/1953). "
      "Una soglia 13–15 li scarterebbe.")
    digits = df.collegio.str.contains(r"[A-Z]+[01][A-Z]*\b")
    w(f"- Nomi con cifre al posto di lettere (errori di trascrizione, es. \"PERASS1\", \"MAR10\"): {int(digits.sum())} collegi, "
      f"per decennio {df[digits].groupby('decade').size().to_dict()}.\n")

    # --- text structure
    w("## Pronunce: struttura del testo\n")
    tagged = df.section_tags.str.contains("fatto") & df.section_tags.str.contains("diritto")
    w("- Nelle sentenze, `<testo>` contiene il testo con due marcatori di intestazione, `<fatto>` e `<diritto>`, "
      "che racchiudono solo il titolo (\"Ritenuto in fatto\", \"Considerato in diritto\"): il testo della sezione "
      "segue il marcatore, fuori dal tag.")
    w(f"- Sentenze con entrambi i marcatori: {int((tagged & (df.tipologia_pronuncia == 'S')).sum()):,} su "
      f"{int((df.tipologia_pronuncia == 'S').sum()):,}; ordinanze con i marcatori: "
      f"{int((tagged & (df.tipologia_pronuncia == 'O')).sum())}.")
    lens = df.assign(epigrafe=df.epigrafe.str.len(), testo=df.testo.str.len(), dispositivo=df.dispositivo.str.len())
    w("Lunghezza mediana (caratteri) degli elementi, per tipo e decennio:\n")
    w(md_table(lens.groupby(["tipologia_pronuncia", "decade"])[["epigrafe", "testo", "dispositivo"]].median().astype(int)) + "\n")
    o = df[df.tipologia_pronuncia == "O"]
    w(f"- Nelle ordinanze `<testo>` è vuoto nel {(o.testo.str.strip() == '').mean():.1%} dei casi: la motivazione "
      f"(\"Ritenuto che…\", \"Considerato che…\") sta dentro `<epigrafe>`. \"Considerato che\" compare nell'epigrafe del "
      f"{o.epigrafe.str.contains('onsiderato che').mean():.0%} delle ordinanze "
      f"(per decennio {o.epigrafe.str.contains('onsiderato che').groupby(o.decade).mean().round(2).to_dict()}): "
      "le altre usano formule diverse, da censire.")
    w(f"- Il dispositivo comincia con \"per questi motivi\" nel {df.dispositivo.str.contains('per questi motivi', case=False).mean():.1%} "
      "delle pronunce e finisce con le firme e la data di deposito.\n")

    # --- massime
    w("## Massime\n")
    merged = df[["anno", "num", "tipologia_pronuncia", "decade"]].merge(pm, on=["anno", "num"], how="left")
    merged["con_massime"] = merged.n_massime.fillna(0) > 0
    w(f"- Pronunce nell'archivio delle massime: {len(pm):,}, le stesse dell'archivio delle pronunce "
      f"(mancanti: {int(merged.n_massime.isna().sum())}; tipo diverso: "
      f"{int((merged.tipologia_pronuncia != merged.tipologia_pronuncia_m).sum())}). Massime: {len(mm):,}; "
      f"per pronuncia mediana {merged[merged.con_massime].n_massime.median():.0f}, massimo {int(merged.n_massime.max())}.")
    w("Quota di pronunce con almeno una massima:\n")
    w(md_table(merged.groupby(["decade", "tipologia_pronuncia"]).con_massime.mean().unstack().round(3)) + "\n")
    recent = merged[merged.anno >= 2023].groupby("anno").con_massime.mean()
    w("Anni recenti: " + ", ".join(f"{y}: {v:.0%}" for y, v in recent.items()) + ". Le massime arrivano dopo la pronuncia.\n")
    w("Tipo di giudizio (`tipologia_giudizio`, presente solo nelle massime ma per tutte le pronunce):\n")
    w(md_table(pm.tipologia_giudizio.replace("", "(vuoto)").value_counts().rename("pronunce").to_frame()) + "\n")
    mm["first_segment"] = (mm.titolo.str.replace(r"^SENT\.\s*\d+/\d+\s*[A-Z]?\.?\s*|^ORD\.\s*\d+/\d+\s*[A-Z]?\.?\s*", "", regex=True)
                           .str.split(" - ").str[0].str.strip())
    upper = mm.titolo.str.match(r"^(SENT|ORD)\.")
    w(f"- Titolo della massima: voci separate da \" - \"; la prima è di solito la materia. Titoli nel formato vecchio, "
      f"tutto maiuscolo e con prefisso \"SENT. n/aa\": {upper.mean():.0%} (ultimo anno: {int(mm[upper].anno.max())}). "
      f"Prime voci distinte: {mm.first_segment.nunique():,}: la materia va normalizzata prima dell'uso.")
    w(f"- Massime con parametri costituzionali: {(mm.n_parametri > 0).mean():.1%}; con norme impugnate: "
      f"{(mm.n_norme > 0).mean():.1%}. Parametri e norme hanno un campo `codice` non descritto nel DTD.")
    per_pron = mm.groupby(["anno", "num"]).first_segment.nunique()
    w(f"- Pronunce con massime su più prime voci diverse: {(per_pron > 1).mean():.1%}.\n")

    # --- judges
    w("## Anagrafica dei giudici\n")
    real = gj[~gj.composite].copy()
    w(f"- Righe: {len(gj)}; giudici: {len(real)}; righe composte da più nomi (\"Lattanzi - Cartabia\"), che corrispondono "
      f"alle pronunce con più redattori: {int(gj.composite.sum())}.")
    w("- Organo di elezione o nomina (`Eletto_da`): " +
      ", ".join(f"{k}: {v}" for k, v in real.Eletto_da.value_counts().items()) + ". La grafia di \"Corte dei conti\" va uniformata.")
    real["anni"] = (real.data_cessazione_d - real.data_giuramento_d).dt.days / 365.25
    w(f"- `data_cessazione` vuota: {int(real.data_cessazione_d.isna().sum())} giudici, molti dei quali hanno chiaramente "
      "cessato dalla carica (vedi tabella sotto). Va completata in `data/manual/` con la fonte.")
    long = real[real.anni > 12.1]
    w(f"- Mandati più lunghi di 12 anni (errori di data): " +
      ", ".join(f"{r.Nome_Cognome} ({r.data_giuramento}–{r.data_cessazione})" for r in long.itertuples()) + ".")
    pre67 = real[real.data_giuramento_d < "1967-12-10"]
    w(f"- Giudici che hanno giurato prima della legge cost. 2/1967: {len(pre67)}; durata mediana del mandato "
      f"{pre67.anni.median():.1f} anni (dopo: {real[real.data_giuramento_d >= '1967-12-10'].anni.median():.1f}).")
    surnames = real.Cognome.str.replace(r"\s+[A-Z]\.(\s*[A-Z]\.)*$", "", regex=True).map(ascii_upper)
    homonyms = real[surnames.duplicated(keep=False)].Nome_Cognome.tolist()
    w(f"- Cognomi condivisi da più giudici: {', '.join(homonyms)}. L'abbinamento non può usare il solo cognome.")
    w(f"- Note biografiche vuote: {int((real.Nota_biografica == '').sum())}; lunghezza mediana {real.Nota_biografica.str.len().median():.0f} caratteri. "
      "Contengono la professione al momento dell'elezione (utile per D4).\n")

    coll = df.assign(coll_ascii=df.collegio.map(ascii_upper)).sort_values("data_deposito_d")
    missing = []
    for r in real[real.data_cessazione_d.isna()].itertuples():
        sur = ascii_upper(re.sub(r"\s+[A-Z]\.(\s*[A-Z]\.)*$", "", r.Cognome))
        hits = coll[coll.coll_ascii.str.contains(r"\b" + re.escape(sur) + r"\b", regex=True)]
        missing.append({"giudice": r.Nome_Cognome, "giuramento": r.data_giuramento,
                        "ultimo collegio (stima)": hits.data_decisione.iloc[-1] if len(hits) else ""})
    w("Giudici senza data di cessazione, con l'ultima decisione in cui il cognome compare nel collegio "
      "(stima: i cognomi condivisi possono confondere):\n")
    w(md_table(pd.DataFrame(missing), index=False) + "\n")

    # --- rough citation probe
    w("## Sonda grezza sulle citazioni (non validata)\n")
    w("Solo per orientarsi, non per l'analisi: riconosce il primo numero di ogni citazione del tipo \"sentenza n. X del "
      "AAAA\", nel testo delle sentenze (anche il «Ritenuto in fatto») e nell'epigrafe delle ordinanze.\n")
    pattern = re.compile(r"\b(sentenz[ae]|ordinanz[ae]|sentt?\.|ordd?\.)\s+(?:nn?\.?)\s*(\d{1,4})\s*(?:del\s+|/)(\d{4})\b", re.I)
    deposit = df.set_index(["anno", "num"]).data_deposito_d.to_dict()
    hits = []
    for r in df.itertuples():
        text = r.testo if r.tipologia_pronuncia == "S" else r.epigrafe
        for m in pattern.finditer(text or ""):
            target = (int(m.group(3)), int(m.group(2)))
            hits.append((r.data_deposito_d, deposit.get(target)))
    probe = pd.DataFrame(hits, columns=["citing", "cited"])
    found = probe.dropna()
    delta = (found.cited - found.citing).dt.days
    w(f"- Menzioni riconosciute: {len(probe):,}; verso pronunce inesistenti: {probe.cited.isna().mean():.1%}.")
    w(f"- Verso pronunce depositate prima: {int((delta < 0).sum()):,}; lo stesso giorno: {int((delta == 0).sum())}; "
      f"dopo: {int((delta > 0).sum())}.")
    phrase = (df.testo + df.epigrafe).str.contains("in pari data")
    w(f"- Pronunce che contengono \"in pari data\": {int(phrase.sum())}. Le citazioni tra pronunce depositate lo stesso "
      "giorno esistono davvero: non sono errori di estrazione.\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Written {REPORT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
