"""Verification queries against the Court's SPARQL endpoint, reconciled with the
downloaded XML files. Writes reports/sparql_reconciliation.md.

Only checks: which metadata the endpoint exposes, and whether its counts match
the files (pronunce, massime, giudici, outcome coverage). No analysis.

Usage (from the repository root, after src/ingest/download.py):
    python3 src/ingest/sparql_check.py
"""

from __future__ import annotations

import re
import unicodedata
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_raw import load_giudici, load_massime, load_pronunce, md_table  # noqa: E402

ENDPOINT = "https://dati.cortecostituzionale.it/sparql/endpoint"
ONTO = "https://dati.cortecostituzionale.it/ontology/"
YEAR = "http://www.w3.org/2006/time#year"
USER_AGENT = "smwa-corte-costituzionale/0.1 (academic research)"
REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT = REPO_ROOT / "reports" / "sparql_reconciliation.md"


def query(sparql: str) -> list[list[str]]:
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "application/sparql-results+xml"})
    text = urllib.request.urlopen(request, timeout=300).read().decode("utf-8")
    rows = []
    for result in re.findall(r"<result>(.*?)</result>", text, re.S):
        rows.append([v.replace(ONTO, "onto:") for v in re.findall(r"<(?:uri|literal|bnode)[^>]*>([^<]*)<", result)])
    return rows


def properties(cls: str) -> pd.DataFrame:
    rows = query(f"SELECT ?p (COUNT(*) AS ?n) WHERE {{ ?s a <{ONTO}{cls}> ; ?p ?o }} GROUP BY ?p ORDER BY DESC(?n)")
    return pd.DataFrame(rows, columns=["proprietà", "triple"])


def per_year(sparql: str) -> pd.Series:
    return pd.Series({int(y): int(n) for y, n in query(sparql)}).sort_index()


PROP_LABELS = {  # plain names of the properties found in the endpoint
    "onto:massima": "massime della pronuncia",
    "onto:relatorePronuncia": "relatore",
    "http://dbpedia.org/ontology/number": "numero",
    "http://purl.org/dc/elements/1.1/identifier": "codice identificativo",
    "http://purl.org/dc/elements/1.1/type": "tipo",
    "http://rdfs.org/sioc/ns#content": "testo",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "tipo di oggetto (pronuncia, massima…)",
    "http://www.w3.org/2000/01/rdf-schema#label": "nome leggibile",
    "http://www.w3.org/2006/time#year": "anno",
    "onto:tipoProcedimento": "tipo di procedimento",
    "onto:presidentePronuncia": "presidente",
    "onto:seduta": "seduta",
    "onto:tipoDispositivo": "esito",
    "onto:testoMassima": "testo della massima",
    "onto:riferimentoCostMassima": "riferimenti alla Costituzione",
    "onto:riferimentoNormMassima": "riferimenti ad altre norme",
    "http://www.w3.org/2002/07/owl#sameAs": "lo stesso oggetto in un'altra banca dati",
    "http://xmlns.com/foaf/0.1/name": "nome",
    "http://xmlns.com/foaf/0.1/surname": "cognome",
    "http://xmlns.com/foaf/0.1/title": "titolo (prof., dott.…)",
    "http://www.w3.org/2000/01/rdf-schema#comment": "nota",
    "http://xmlns.com/foaf/0.1/depiction": "immagine",
    "onto:haMembro": "membri (giudici)",
    "onto:verbale": "verbale",
    "http://purl.org/dc/elements/1.1/date": "data",
}
CLASSES = [("Pronuncia", "Pronunce"), ("Massima", "Massime"), ("Giudice", "Giudici"), ("Seduta", "Sedute")]


def num(x) -> str:  # Italian format: dot for thousands
    return f"{int(x):,}".replace(",", ".")


def year_table(frame: pd.DataFrame, names: dict) -> str:
    if not len(frame):
        return "nessuno.\n"
    return md_table(frame.rename(columns=names).rename_axis("Anno")) + "\n"


def render_md(r: dict) -> str:
    """r: the results collected in main(). Returns the text of the report."""
    out: list[str] = []
    w = out.append
    w("# Il confronto con la banca dati SPARQL della Corte\n")
    w(f"Prodotto da `src/ingest/sparql_check.py` il {r['when']} (ora UTC). Oltre ai file da scaricare, la Corte ha una banca dati "
      f"che un programma può interrogare con il linguaggio SPARQL, all'indirizzo `{ENDPOINT}`. È una seconda fonte ufficiale: "
      "confrontandola con i file scaricati, elencati in `data/raw/MANIFEST.csv`, si possono scoprire errori nei file. La banca dati "
      "si aggiorna di continuo, mentre i file sono quelli di un giorno preciso: negli anni più recenti qualche differenza è normale.\n")
    w("## Che cosa contiene la banca dati\n")
    w("La banca dati descrive quattro tipi di oggetti: pronunce, massime, giudici e sedute della Corte. Ogni informazione è registrata "
      "come una \"tripla\": oggetto, proprietà, valore (per esempio: una pronuncia, \"relatore\", un giudice). Per ogni proprietà le "
      "tabelle dicono quante triple ci sono: è un modo per vedere quanto è completa ogni informazione. \"onto:\" abbrevia "
      f"`{ONTO}`, cioè le proprietà definite dalla Corte; le altre vengono da vocabolari usati da molte banche dati.\n")
    for cls, label in CLASSES:
        t = r["props"][cls]
        w(f"**{label}**\n")
        w(md_table(pd.DataFrame({"Proprietà (nome tecnico)": t["proprietà"].values,
                                 "Che cosa è": [PROP_LABELS.get(p, "") for p in t["proprietà"]],
                                 "Triple": t["triple"].values}), index=False) + "\n")
    w("## Le pronunce\n")
    w(f"- Pronunce diverse: nella banca dati {num(r['n_ep'])}, nei file {num(r['n_files'])}.")
    w("- Anni in cui i due conteggi non coincidono:\n")
    w(year_table(r["diff"], {"file": "Nei file", "endpoint": "Nella banca dati"}))
    w(f"- Triple che dicono \"questo oggetto è una pronuncia\": {num(r['n_type'])}, più delle {num(r['n_ep'])} pronunce. Il motivo: "
      "nella banca dati una pronuncia con più relatori è registrata una volta per ogni relatore (controllato sulle pronunce 194/2019, "
      "102/2016 e 119/2024). Quindi contare queste triple non dà il numero delle pronunce. Triple con il relatore: "
      f"{num(r['n_rel'])}.\n")
    w("## Il relatore: banca dati e file a confronto\n")
    checked, agree = r["checked"], r["agree"]
    share = f"{100 * agree / checked:.2f}%".replace(".", ",")
    w(f"- Pronunce confrontate: {num(checked)}. Il relatore coincide, cioè ogni cognome della banca dati compare nel relatore dei "
      f"file, nel **{share}** dei casi; le differenze sono {num(checked - agree)}.")
    g = r["grouped"]
    if g is not None and len(g):
        w(f"- Le differenze, raggruppate per coppia di nomi ({len(g)} coppie{'; qui le prime 30' if len(g) > 30 else ''}). Un nome "
          "scritto in due modi simili è di solito un errore di grafia; una casella vuota vuol dire che nei file il relatore manca.\n")
        w(md_table(g.head(30).set_axis(["Nei file", "Nella banca dati", "Pronunce"], axis=1), index=False) + "\n")
    w("## Le massime\n")
    w(f"- Massime diverse: nella banca dati {num(r['n_mass'])}, nei file {num(r['n_mass_files'])}.")
    w("- Anni in cui i due conteggi non coincidono:\n")
    w(year_table(r["dm"], {"file": "Nei file", "endpoint": "Nella banca dati"}))
    w("## I giudici\n")
    w(f"- Giudici: nella banca dati {r['n_g']}; righe dell'elenco dei giudici nei file {r['n_gj']}, di cui {r['n_comp']} con più "
      "nomi insieme (corrispondono alle pronunce scritte da più giudici, non a persone).\n")
    w("## L'esito delle pronunce (`tipoDispositivo`)\n")
    w("La banca dati dice anche l'esito di ogni pronuncia, per esempio \"non fondatezza\" o \"illegittimità costituzionale\". La "
      "tabella dà, per ogni anno in cui c'è almeno un esito, quante pronunce lo hanno e la quota sul totale delle pronunce nei file "
      "(1 = tutte; sopra 1 se la banca dati ha più pronunce dei file).\n")
    w(year_table(r["cov"], {"pronunce nei file": "Pronunce nei file", "con esito nell'endpoint": "Con l'esito nella banca dati",
                            "quota": "Quota"}))
    w(f"- Tipi di esito diversi: {len(r['types'])}.\n")
    w(md_table(r["types"].set_axis(["Codice", "Esito", "Triple"], axis=1), index=False) + "\n")
    return "\n".join(out)


def main() -> None:
    df = load_pronunce()
    pm, mm = load_massime()
    gj = load_giudici()
    r: dict = {"when": f"{datetime.now(timezone.utc):%d/%m/%Y alle %H:%M}",
               "props": {cls: properties(cls) for cls, _ in CLASSES}}

    n_ep = int(query(f"SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> }}")[0][0])
    ep_year = per_year(f"SELECT ?y (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> ; <{YEAR}> ?y }} GROUP BY ?y")
    file_year = df.groupby("anno").size()
    diff = pd.DataFrame({"file": file_year, "endpoint": ep_year}).fillna(0).astype(int)
    r.update(n_ep=n_ep, n_files=len(df), diff=diff[diff.file != diff.endpoint])
    r["n_type"] = int(query(f"SELECT (COUNT(?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> }}")[0][0])
    r["n_rel"] = int(query(f"SELECT (COUNT(?r) AS ?n) WHERE {{ ?s <{ONTO}relatorePronuncia> ?r }}")[0][0])

    rows = query(f"SELECT ?n ?y ?sur WHERE {{ ?s a <{ONTO}Pronuncia> ; <http://dbpedia.org/ontology/number> ?n ; "
                 f"<{YEAR}> ?y ; <{ONTO}relatorePronuncia> ?g . ?g <http://xmlns.com/foaf/0.1/surname> ?sur }}")
    ep_rel: dict[tuple[int, int], list[str]] = {}
    for n, y, sur in rows:
        ep_rel.setdefault((int(y), int(n)), []).append(sur)
    norm = lambda s: re.sub(r"[^A-Z ]", "", unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper())
    checked = agree = 0
    mismatches = []
    for row in df.itertuples():
        surnames = ep_rel.get((row.anno, row.num))
        if not surnames:
            continue
        checked += 1
        file_rel = norm(row.relatore_pronuncia)
        # the endpoint disambiguates homonyms with initials ("SANDULLI A."): drop them before matching
        parts = [re.sub(r"( [A-Z])+$", "", norm(p).strip()) for s in surnames for p in s.split(" - ")]
        if parts and all(p and p in file_rel for p in parts):
            agree += 1
        else:
            mismatches.append({"pronuncia": f"{row.num}/{row.anno}", "file": row.relatore_pronuncia, "endpoint": " / ".join(surnames)})
    r.update(checked=checked, agree=agree, grouped=(
        pd.DataFrame(mismatches).groupby(["file", "endpoint"]).size().rename("pronunce").sort_values(ascending=False).reset_index()
        if mismatches else None))

    r["n_mass"] = int(query(f"SELECT (COUNT(DISTINCT ?m) AS ?n) WHERE {{ ?m a <{ONTO}Massima> }}")[0][0])
    ep_m = per_year(f"SELECT ?y (COUNT(?m) AS ?n) WHERE {{ ?p <{ONTO}massima> ?m ; <{YEAR}> ?y }} GROUP BY ?y")
    dm = pd.DataFrame({"file": mm.groupby("anno").size(), "endpoint": ep_m}).fillna(0).astype(int)
    r.update(n_mass_files=len(mm), dm=dm[dm.file != dm.endpoint])

    r["n_g"] = int(query(f"SELECT (COUNT(DISTINCT ?g) AS ?n) WHERE {{ ?g a <{ONTO}Giudice> }}")[0][0])
    r.update(n_gj=len(gj), n_comp=int(gj.composite.sum()))

    esito = per_year(f"SELECT ?y (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s <{ONTO}tipoDispositivo> ?t ; <{YEAR}> ?y }} GROUP BY ?y")
    cov = pd.DataFrame({"pronunce nei file": file_year, "con esito nell'endpoint": esito}).fillna(0).astype(int)
    cov = cov[cov["con esito nell'endpoint"] > 0]
    cov["quota"] = (cov["con esito nell'endpoint"] / cov["pronunce nei file"]).round(3)
    r["cov"] = cov
    types = query(f"SELECT ?t ?l (COUNT(?s) AS ?n) WHERE {{ ?s <{ONTO}tipoDispositivo> ?t . "
                  "OPTIONAL { ?t <http://www.w3.org/2000/01/rdf-schema#label> ?l } } GROUP BY ?t ?l ORDER BY DESC(?n)")
    r["types"] = pd.DataFrame([[t[0].split('/')[-1], t[1] if len(t) > 2 else '', t[-1]] for t in types],
                              columns=["codice", "etichetta", "triple"])
    out = [render_md(r)]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Written {REPORT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
