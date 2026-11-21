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
    if isinstance(value, float):  # Italian format: comma for decimals
        return f"{value:.3f}".rstrip("0").rstrip(".").replace(".", ",") if value == value else ""
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


def it(x, d=1) -> str:  # Italian format: comma for decimals
    return f"{x:.{d}f}".replace(".", ",")


def num(x) -> str:  # Italian format: dot for thousands
    return f"{int(x):,}".replace(",", ".")


def pct(x, d=1) -> str:
    return it(100 * x, d) + "%"


def by_decade(d: dict, value=str) -> str:
    return "; ".join(f"anni {k}: {value(v)}" for k, v in d.items())


# ---------------------------------------------------------------- report

def main() -> None:
    df = load_pronunce()
    pm, mm = load_massime()
    gj = load_giudici()
    out: list[str] = []
    w = out.append

    w("# Primo controllo dei file scaricati\n")
    w("Prodotto da `src/ingest/inspect_raw.py` sui file elencati in `data/raw/MANIFEST.csv`, prima di qualsiasi analisi. Descrive "
      "com'è fatto ogni file, quanto è completo anno per anno e se i dati sono coerenti tra loro; non corregge nulla. Che cosa contiene "
      "ogni campo dei file (le etichette XML, scritte `così`) è spiegato in `docs/data_schema.md`; il suo significato giuridico in "
      "`docs/context.md`.\n")
    with (RAW / "MANIFEST.csv").open(encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    w("## Quale versione dei dati\n")
    w("Per ogni file scaricato: quando è stato scaricato e la sua impronta, un codice che cambia se cambia anche un solo carattere "
      "del file.\n")
    w(md_table(pd.DataFrame(manifest)[["file", "downloaded_at", "sha256"]]
               .set_axis(["File", "Scaricato il (ora UTC)", "Impronta (SHA-256)"], axis=1), index=False) + "\n")

    # --- pronunce: identifiers and numbering
    w("## Le pronunce: numeri e date\n")
    by_year = df.groupby("anno").num.agg(["count", "min", "max", "nunique"])
    n_s, n_o = int((df.tipologia_pronuncia == "S").sum()), int((df.tipologia_pronuncia == "O").sum())
    w(f"- Pronunce: **{num(len(df))}**, dal {df.anno.min()} al {df.anno.max()}: {num(n_s)} sentenze e {num(n_o)} ordinanze "
      f"(altri tipi: {int((~df.tipologia_pronuncia.isin(['S', 'O'])).sum())}).")
    w(f"- Pronunce con lo stesso anno e lo stesso numero: {int(df.duplicated(['anno', 'num']).sum())}. Anni con numeri mancanti: "
      f"{int(((by_year['max'] != by_year['count']) | (by_year['min'] != 1)).sum())}. Quindi ogni anno la numerazione riparte da 1 "
      "ed è unica per sentenze e ordinanze: anno e numero bastano a identificare una pronuncia.")
    ecli_ok = df.ecli == "ECLI:IT:COST:" + df.anno_pronuncia + ":" + df.numero_pronuncia
    w(f"- Pronunce con un codice europeo (ECLI) diverso da `ECLI:IT:COST:anno:numero`: {int((~ecli_ok).sum())}.")
    y_dep, y_dec = df.data_deposito_d.dt.year, df.data_decisione_d.dt.year
    wrong = df[df.anno != y_dep]
    w(f"- L'anno della pronuncia è quello del deposito, tranne in {len(wrong)} "
      f"{'caso (un errore di data' if len(wrong) == 1 else 'casi (errori di data'}: "
      f"{', '.join(f'la {r.num}/{r.anno}, depositata il {r.data_deposito} secondo i dati' for r in wrong.itertuples())}). "
      f"Coincide con l'anno della decisione nel {pct((df.anno == y_dec).mean(), 2)} dei casi: "
      f"{int(((df.anno == y_dep) & (df.anno != y_dec)).sum())} pronunce sono state decise in un anno e depositate, e quindi "
      "numerate, nell'anno dopo.")
    inversions = {}
    for col in ["data_deposito_d", "data_decisione_d"]:
        inversions[col] = int(sum((g.sort_values("num")[col].diff().dt.days < 0).sum() for _, g in df.groupby("anno")))
    w(f"- Pronunce con un numero più alto della precedente ma una data più vecchia: {num(inversions['data_deposito_d'])} guardando "
      f"la data di deposito, {num(inversions['data_decisione_d'])} guardando quella della decisione. Quindi il numero segue l'ordine "
      "del deposito, non quello della decisione.")
    per_year = df.groupby("anno").size()
    start = int(per_year.cumsum().ge(1000).idxmax())
    after_start = per_year.loc[start:]
    w(f"- La rete arriva a 1.000 pronunce nel {start} (a fine anno sono {num(per_year.cumsum()[start])}). Dal {start} l'anno con "
      f"meno pronunce depositate è il {int(after_start.idxmin())}, con {int(after_start.min())}; l'anno in corso "
      f"({int(per_year.index.max())}, non ancora finito) ne ha {int(per_year.iloc[-1])}.")
    lag = (df.data_deposito_d - df.data_decisione_d).dt.days
    w(f"- Giorni tra la decisione e il deposito: {lag.median():.0f} a metà della distribuzione (mediana); il 99% delle pronunce "
      f"entro {lag.quantile(.99):.0f}. Date di decisione mancanti: {int(df.data_decisione_d.isna().sum())}. Pronunce depositate "
      f"prima della data di decisione, quindi con una data sbagliata: {int((lag < 0).sum())}.\n")

    # --- people in the header
    w("## Le pronunce: presidente, relatore e chi ha scritto\n")
    empty = lambda s: s.fillna("").str.strip() == ""
    fill = pd.DataFrame({
        "Presidente vuoto": empty(df.presidente), "Relatore vuoto": empty(df.relatore_pronuncia),
        "Redattore vuoto": empty(df.redattore_pronuncia)}).groupby(df.decade).mean()
    w("Quota di pronunce, per decennio, in cui il campo è vuoto (1 = sempre vuoto, 0 = mai). Il relatore è il giudice che segue la "
      "causa; il redattore è chi scrive la pronuncia (campo `redattore_pronuncia`).\n")
    w(md_table(fill.round(3).rename_axis("Decennio")) + "\n")
    red_by_year = empty(df.redattore_pronuncia).groupby(df.anno).mean()
    w("Il campo del redattore negli anni in cui comincia a essere compilato (quota di pronunce con il campo vuoto): " +
      "; ".join(f"{y}: {v:.0%}" for y, v in red_by_year.loc[1999:2004].items()) + ".\n")
    tail = df.dispositivo.fillna("").str[-SIGNATURE_TAIL:]
    df["sig_redattore"] = tail.str.contains(r"redattor|redattric", case=False)
    first_switch = df[df.sig_redattore].sort_values(["anno", "num"]).iloc[0]
    before = df[(df.anno < first_switch.anno) | ((df.anno == first_switch.anno) & (df.num < first_switch.num))]
    after = df.drop(before.index)
    w("**Le firme in fondo alla pronuncia**\n")
    w(f"- Fino alla {first_switch.num - 1}/{first_switch.anno} firmano tutti i giudici del collegio, e chi ha scritto la pronuncia "
      f"non è indicato da nessuna parte. Pronunce di quel periodo che nominano un redattore nelle firme: "
      f"{int(before.sig_redattore.sum())}.")
    w(f"- Dalla {first_switch.num}/{first_switch.anno} (decisa il {first_switch.data_decisione}, depositata il "
      f"{first_switch.data_deposito}) firmano il Presidente e chi ha scritto la pronuncia (\"Il redattore: …\", poi \"…, Redattore\" "
      f"o \"Redattrice\"). Pronunce successive senza il redattore nelle firme: {int((~after.sig_redattore).sum())}, per lo più "
      "ordinanze lette in udienza e firmate dal solo Presidente.")
    both = df[~empty(df.relatore_pronuncia) & ~empty(df.redattore_pronuncia)]
    norm = lambda s: s.str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    differ = both[norm(both.relatore_pronuncia) != norm(both.redattore_pronuncia)]
    multi = df[df.redattore_pronuncia.str.contains(" - ", regex=False)]
    w(f"- Pronunce con entrambi i campi compilati: {num(len(both))}. In {len(differ)} il relatore è diverso da chi ha scritto "
      f"(per decennio: {by_decade(differ.groupby('decade').size().to_dict())}).")
    w(f"- Pronunce scritte da più giudici (nomi separati da \" - \"): {len(multi)}, dal {multi.anno.min()} al {multi.anno.max()}.")
    w(f"- Valori diversi di ogni campo: relatore {df.relatore_pronuncia.nunique()}, redattore {df.redattore_pronuncia.nunique()}, "
      f"presidente {df.presidente.nunique()} (il presidente è scritto con il solo cognome).\n")

    # --- collegio
    df["n_collegio"] = df.collegio.map(collegio_size)
    w("## Le pronunce: il collegio\n")
    w("Numero di giudici scritti nel campo `collegio`, contati in modo approssimato (il conteggio vero è fatto dopo, in "
      "`src/judges/`). I collegi con 10 giudici o meno, o con più di 15, sono da controllare.\n")
    bins = pd.cut(df.n_collegio, [-1, 10, 12, 15, 99],
                  labels=["10 o meno (da controllare)", "11–12", "13–15", "più di 15 (da controllare)"])
    w(md_table(pd.crosstab(df.decade, bins).rename_axis("Decennio")) + "\n")
    w(f"- Collegi con 11 o 12 giudici: {num(df.n_collegio.isin([11, 12]).sum())} ({pct(df.n_collegio.isin([11, 12]).mean())}). "
      "Sono validi, perché il numero legale è 11 (legge 87/1953, art. 16): una soglia di 13–15 giudici li scarterebbe.")
    digits = df.collegio.str.contains(r"[A-Z]+[01][A-Z]*\b")
    w(f"- Collegi con nomi in cui ci sono cifre al posto delle lettere (errori di trascrizione, per esempio \"PERASS1\", \"MAR10\"): "
      f"{int(digits.sum())}; per decennio: {by_decade(df[digits].groupby('decade').size().to_dict())}.\n")

    # --- text structure
    w("## Le pronunce: come è diviso il testo\n")
    tagged = df.section_tags.str.contains("fatto") & df.section_tags.str.contains("diritto")
    w("- Nelle sentenze il campo `<testo>` contiene due etichette, `<fatto>` e `<diritto>`, che racchiudono solo il titolo della "
      "parte (\"Ritenuto in fatto\", \"Considerato in diritto\"): il testo della parte viene dopo l'etichetta, non dentro.")
    w(f"- Sentenze con entrambe le etichette: {num((tagged & (df.tipologia_pronuncia == 'S')).sum())} su {num(n_s)}; ordinanze con "
      f"le etichette: {int((tagged & (df.tipologia_pronuncia == 'O')).sum())}.")
    lens = df.assign(epigrafe=df.epigrafe.str.len(), testo=df.testo.str.len(), dispositivo=df.dispositivo.str.len())
    w("Lunghezza di ogni parte a metà della distribuzione (mediana, in caratteri), per tipo di pronuncia (O = ordinanza, "
      "S = sentenza) e decennio:\n")
    w(md_table(lens.groupby(["tipologia_pronuncia", "decade"])[["epigrafe", "testo", "dispositivo"]].median().astype(int)
               .rename_axis(["Tipo", "Decennio"])) + "\n")
    o = df[df.tipologia_pronuncia == "O"]
    considerato = o.epigrafe.str.contains("onsiderato che")
    w(f"- Nelle ordinanze `<testo>` è vuoto nel {pct((o.testo.str.strip() == '').mean())} dei casi: il ragionamento "
      f"(\"Ritenuto che…\", \"Considerato che…\") sta dentro `<epigrafe>`. La formula \"Considerato che\" compare nell'epigrafe "
      f"del {considerato.mean():.0%} delle ordinanze (per decennio: "
      f"{by_decade(considerato.groupby(o.decade).mean().round(2).to_dict(), lambda v: f'{round(v * 100):.0f}%')}): le altre usano "
      "formule diverse, da elencare prima di scrivere il programma che legge i testi.")
    w(f"- Il dispositivo comincia con \"per questi motivi\" nel "
      f"{pct(df.dispositivo.str.contains('per questi motivi', case=False).mean())} delle pronunce e finisce con le firme e la "
      "data di deposito.\n")

    # --- massime
    w("## Le massime\n")
    merged = df[["anno", "num", "tipologia_pronuncia", "decade"]].merge(pm, on=["anno", "num"], how="left")
    merged["con_massime"] = merged.n_massime.fillna(0) > 0
    w(f"- Pronunce nell'archivio delle massime: {num(len(pm))}, le stesse dell'archivio delle pronunce (mancanti: "
      f"{int(merged.n_massime.isna().sum())}; con un tipo diverso: "
      f"{int((merged.tipologia_pronuncia != merged.tipologia_pronuncia_m).sum())}). Massime: {num(len(mm))}; di solito una per "
      f"pronuncia (mediana {merged[merged.con_massime].n_massime.median():.0f}), al massimo {int(merged.n_massime.max())}.")
    w("Quota di pronunce con almeno una massima (1 = tutte), per decennio e tipo:\n")
    w(md_table(merged.groupby(["decade", "tipologia_pronuncia"]).con_massime.mean().unstack().round(3)
               .rename(columns={"O": "Ordinanze", "S": "Sentenze"}).rename_axis("Decennio")) + "\n")
    recent = merged[merged.anno >= 2023].groupby("anno").con_massime.mean()
    w("Gli ultimi anni: " + "; ".join(f"{y}: {v:.0%}" for y, v in recent.items()) +
      ". Le massime vengono scritte qualche mese dopo la pronuncia.\n")
    w("Il tipo di giudizio (campo `tipologia_giudizio`) sta solo nell'archivio delle massime, ma c'è per tutte le pronunce:\n")
    w(md_table(pm.tipologia_giudizio.replace("", "(vuoto)").value_counts().rename("Pronunce").to_frame()
               .rename_axis("Tipo di giudizio")) + "\n")
    mm["first_segment"] = (mm.titolo.str.replace(r"^SENT\.\s*\d+/\d+\s*[A-Z]?\.?\s*|^ORD\.\s*\d+/\d+\s*[A-Z]?\.?\s*", "", regex=True)
                           .str.split(" - ").str[0].str.strip())
    upper = mm.titolo.str.match(r"^(SENT|ORD)\.")
    w(f"- Il titolo di ogni massima è fatto di voci separate da \" - \"; la prima di solito è la materia. Titoli nel formato vecchio, "
      f"tutto in maiuscolo e con davanti un'abbreviazione come \"SENT. n/aa\": {upper.mean():.0%} (l'ultimo anno in cui compaiono: "
      f"{int(mm[upper].anno.max())}). Prime voci diverse: {num(mm.first_segment.nunique())}: prima di usarle come materia "
      "vanno ricondotte a un elenco più corto.")
    w(f"- Massime con i parametri, cioè le norme della Costituzione (o di leggi costituzionali) che si dicono violate: "
      f"{pct((mm.n_parametri > 0).mean())}; con le leggi impugnate: {pct((mm.n_norme > 0).mean())}. Parametri e leggi hanno un "
      "campo `codice` che i documenti ufficiali sulla struttura dei file non descrivono.")
    per_pron = mm.groupby(["anno", "num"]).first_segment.nunique()
    w(f"- Pronunce con massime che hanno prime voci diverse tra loro: {pct((per_pron > 1).mean())}.\n")

    # --- judges
    w("## L'elenco dei giudici\n")
    real = gj[~gj.composite].copy()
    w(f"- Righe: {len(gj)}; giudici: {len(real)}. Le altre {int(gj.composite.sum())} righe hanno più nomi insieme "
      "(\"Lattanzi - Cartabia\"): corrispondono alle pronunce scritte da più giudici, non a persone.")
    w("- Chi ha eletto o nominato il giudice (campo `Eletto_da`): " +
      "; ".join(f"{k}: {v}" for k, v in real.Eletto_da.value_counts().items()) +
      ". \"Corte dei Conti\" e \"Corte dei conti\" sono la stessa cosa scritta in due modi.")
    real["anni"] = (real.data_cessazione_d - real.data_giuramento_d).dt.days / 365.25
    w(f"- Fine del mandato (`data_cessazione`) mancante: {int(real.data_cessazione_d.isna().sum())} giudici, molti dei quali hanno "
      "chiaramente finito il mandato (tabella qui sotto). Va completata a mano in `data/manual/`, con la fonte.")
    long = real[real.anni > 12.1]
    w(f"- Mandati di più di 12 anni, quindi date sbagliate: " +
      ", ".join(f"{r.Nome_Cognome} ({r.data_giuramento}–{r.data_cessazione})" for r in long.itertuples()) + ".")
    pre67 = real[real.data_giuramento_d < "1967-12-10"]
    w(f"- Giudici che hanno giurato prima della legge costituzionale 2/1967, che riguarda la durata del mandato: {len(pre67)}; "
      f"durata mediana del loro mandato {it(pre67.anni.median())} anni (per quelli venuti dopo: "
      f"{it(real[real.data_giuramento_d >= '1967-12-10'].anni.median())}).")
    surnames = real.Cognome.str.replace(r"\s+[A-Z]\.(\s*[A-Z]\.)*$", "", regex=True).map(ascii_upper)
    homonyms = real[surnames.duplicated(keep=False)].Nome_Cognome.tolist()
    w(f"- Giudici con lo stesso cognome di un altro: {', '.join(homonyms)}. Per collegare i nomi all'elenco non basta il cognome.")
    w(f"- Note biografiche vuote: {int((real.Nota_biografica == '').sum())}; lunghezza mediana "
      f"{real.Nota_biografica.str.len().median():.0f} caratteri. Dicono la professione del giudice al momento dell'elezione "
      "(serve per D4).\n")

    coll = df.assign(coll_ascii=df.collegio.map(ascii_upper)).sort_values("data_deposito_d")
    missing = []
    for r in real[real.data_cessazione_d.isna()].itertuples():
        sur = ascii_upper(re.sub(r"\s+[A-Z]\.(\s*[A-Z]\.)*$", "", r.Cognome))
        hits = coll[coll.coll_ascii.str.contains(r"\b" + re.escape(sur) + r"\b", regex=True)]
        missing.append({"Giudice": r.Nome_Cognome, "Giuramento": r.data_giuramento,
                        "Ultimo collegio (stima)": hits.data_decisione.iloc[-1] if len(hits) else ""})
    w("Giudici senza la data di fine del mandato, con l'ultima decisione in cui il loro cognome compare nel collegio (è una stima: "
      "i cognomi condivisi possono confondere):\n")
    w(md_table(pd.DataFrame(missing), index=False) + "\n")

    # --- rough citation probe
    w("## Una prima ricerca grezza delle citazioni (non controllata)\n")
    w("Serve solo per orientarsi, non per le analisi. Cerca le citazioni scritte come \"sentenza n. X del AAAA\" e ne prende il "
      "primo numero, nel testo delle sentenze (compreso il «Ritenuto in fatto») e nell'epigrafe delle ordinanze.\n")
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
    w(f"- Citazioni trovate: {num(len(probe))}; verso pronunce che non esistono: {pct(probe.cited.isna().mean())}.")
    w(f"- Verso pronunce depositate prima: {num((delta < 0).sum())}; lo stesso giorno: {int((delta == 0).sum())}; "
      f"dopo: {int((delta > 0).sum())}.")
    phrase = (df.testo + df.epigrafe).str.contains("in pari data")
    w(f"- Pronunce che contengono le parole \"in pari data\": {int(phrase.sum())}. Quindi le citazioni tra pronunce depositate lo "
      "stesso giorno esistono davvero: non sono errori del programma.\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Written {REPORT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
