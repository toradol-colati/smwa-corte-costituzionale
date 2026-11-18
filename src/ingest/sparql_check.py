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


def main() -> None:
    df = load_pronunce()
    pm, mm = load_massime()
    gj = load_giudici()
    out: list[str] = []
    w = out.append
    w("# Endpoint SPARQL e file scaricati: verifica e riconciliazione\n")
    w(f"Generato da `src/ingest/sparql_check.py` il {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC, "
      f"interrogando `{ENDPOINT}` e confrontando con i file di `data/raw/MANIFEST.csv`. "
      "L'endpoint è aggiornato in continuo; i file sono quelli del download registrato nel manifest.\n")

    w("## Metadati esposti\n")
    for cls in ["Pronuncia", "Massima", "Giudice", "Seduta"]:
        w(f"**{cls}**\n")
        w(md_table(properties(cls), index=False) + "\n")

    w("## Pronunce\n")
    n_ep = int(query(f"SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> }}")[0][0])
    ep_year = per_year(f"SELECT ?y (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> ; <{YEAR}> ?y }} GROUP BY ?y")
    file_year = df.groupby("anno").size()
    diff = pd.DataFrame({"file": file_year, "endpoint": ep_year}).fillna(0).astype(int)
    diff = diff[diff.file != diff.endpoint]
    w(f"- Pronunce distinte: endpoint {n_ep:,}, file {len(df):,}.")
    w("- Anni con conteggi diversi:\n")
    w(md_table(diff) + "\n" if len(diff) else "nessuno.\n")

    n_type = int(query(f"SELECT (COUNT(?s) AS ?n) WHERE {{ ?s a <{ONTO}Pronuncia> }}")[0][0])
    n_rel = int(query(f"SELECT (COUNT(?r) AS ?n) WHERE {{ ?s <{ONTO}relatorePronuncia> ?r }}")[0][0])
    w(f"- Triple di tipo `Pronuncia`: {n_type:,}, contro {n_ep:,} pronunce distinte. Triple `relatorePronuncia`: {n_rel:,}. "
      "Nell'endpoint una pronuncia con più relatori riceve una tripla di tipo per ciascun relatore (verificato su 194/2019, "
      "102/2016, 119/2024): il conteggio delle triple di tipo non è il numero delle pronunce.\n")

    w("## Relatore: endpoint e file a confronto\n")
    rows = query(f"SELECT ?n ?y ?sur WHERE {{ ?s a <{ONTO}Pronuncia> ; <http://dbpedia.org/ontology/number> ?n ; "
                 f"<{YEAR}> ?y ; <{ONTO}relatorePronuncia> ?g . ?g <http://xmlns.com/foaf/0.1/surname> ?sur }}")
    ep_rel: dict[tuple[int, int], list[str]] = {}
    for n, y, sur in rows:
        ep_rel.setdefault((int(y), int(n)), []).append(sur)
    norm = lambda s: re.sub(r"[^A-Z ]", "", unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper())
    checked = agree = 0
    mismatches = []
    for r in df.itertuples():
        surnames = ep_rel.get((r.anno, r.num))
        if not surnames:
            continue
        checked += 1
        file_rel = norm(r.relatore_pronuncia)
        # the endpoint disambiguates homonyms with initials ("SANDULLI A."): drop them before matching
        parts = [re.sub(r"( [A-Z])+$", "", norm(p).strip()) for s in surnames for p in s.split(" - ")]
        if parts and all(p and p in file_rel for p in parts):
            agree += 1
        else:
            mismatches.append({"pronuncia": f"{r.num}/{r.anno}", "file": r.relatore_pronuncia, "endpoint": " / ".join(surnames)})
    w(f"- Pronunce confrontate: {checked:,}. Concordanza (ogni cognome dell'endpoint compare nel relatore dei file): "
      f"**{agree / checked:.2%}** ({checked - agree} discordanze).")
    if mismatches:
        grouped = (pd.DataFrame(mismatches).groupby(["file", "endpoint"]).size()
                   .rename("pronunce").sort_values(ascending=False).reset_index())
        w(f"- Discordanze raggruppate per coppia di nomi ({len(grouped)} coppie distinte; le prime 30):\n")
        w(md_table(grouped.head(30), index=False) + "\n")

    w("## Massime\n")
    n_mass = int(query(f"SELECT (COUNT(DISTINCT ?m) AS ?n) WHERE {{ ?m a <{ONTO}Massima> }}")[0][0])
    ep_m = per_year(f"SELECT ?y (COUNT(?m) AS ?n) WHERE {{ ?p <{ONTO}massima> ?m ; <{YEAR}> ?y }} GROUP BY ?y")
    file_m = mm.groupby("anno").size()
    dm = pd.DataFrame({"file": file_m, "endpoint": ep_m}).fillna(0).astype(int)
    dm = dm[dm.file != dm.endpoint]
    w(f"- Massime distinte: endpoint {n_mass:,}, file {len(mm):,}.")
    w("- Anni con conteggi diversi:\n")
    w(md_table(dm) + "\n" if len(dm) else "nessuno.\n")

    w("## Giudici\n")
    n_g = int(query(f"SELECT (COUNT(DISTINCT ?g) AS ?n) WHERE {{ ?g a <{ONTO}Giudice> }}")[0][0])
    w(f"- Giudici: endpoint {n_g}, righe dell'anagrafica nei file {len(gj)} "
      f"(di cui {int(gj.composite.sum())} righe composte da più nomi).\n")

    w("## Esito (`tipoDispositivo`)\n")
    esito = per_year(f"SELECT ?y (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s <{ONTO}tipoDispositivo> ?t ; <{YEAR}> ?y }} GROUP BY ?y")
    cov = pd.DataFrame({"pronunce nei file": file_year, "con esito nell'endpoint": esito}).fillna(0).astype(int)
    cov = cov[cov["con esito nell'endpoint"] > 0]
    cov["quota"] = (cov["con esito nell'endpoint"] / cov["pronunce nei file"]).round(3)
    w(md_table(cov) + "\n")
    types = query(f"SELECT ?t ?l (COUNT(?s) AS ?n) WHERE {{ ?s <{ONTO}tipoDispositivo> ?t . "
                  "OPTIONAL { ?t <http://www.w3.org/2000/01/rdf-schema#label> ?l } } GROUP BY ?t ?l ORDER BY DESC(?n)")
    w(f"- Tipi di esito distinti: {len(types)}.\n")
    w(md_table(pd.DataFrame([[r[0].split('/')[-1], r[1] if len(r) > 2 else '', r[-1]] for r in types],
                            columns=["codice", "etichetta", "triple"]), index=False) + "\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Written {REPORT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
