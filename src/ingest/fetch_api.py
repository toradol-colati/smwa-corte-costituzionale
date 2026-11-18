"""Data obtained through APIs (course content: working with APIs).
1. Court SPARQL endpoint: outcome (tipoDispositivo) of each pronuncia, from 2005,
   and the members of the sittings (sedute) linked to each pronuncia, from 2004.
2. MediaWiki API (it.wikipedia.org): pages linking to a pronuncia on the Court's
   site or on Consulta Online.
Outputs: data/processed/esiti.csv, data/interim/sedute_membri.csv,
data/processed/wikipedia_links.csv, and rows appended to data/raw/MANIFEST.csv? No:
API snapshots are not raw files; the query date is stored in reports/api_fetch.json.
Usage: .venv/bin/python src/ingest/fetch_api.py
"""
import json, re, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sparql_check import query, ONTO, YEAR
UA = "smwa-corte-costituzionale/0.1 (academic research)"
NUM = "http://dbpedia.org/ontology/number"
LABEL = "http://www.w3.org/2000/01/rdf-schema#label"

def esiti():
    rows = query(f"SELECT ?y ?n ?l WHERE {{ ?s <{ONTO}tipoDispositivo> ?t ; <{YEAR}> ?y ; <{NUM}> ?n . ?t <{LABEL}> ?l }}")
    e = pd.DataFrame(rows, columns=["anno", "num", "esito"]).astype({"anno": int, "num": int})
    e["pid"] = e.anno * 10000 + e.num
    e = e.drop_duplicates(["pid", "esito"])
    e["illegittimita"] = e.esito.str.contains("illegittimità|ill\\. cost", case=False)
    e[["pid", "esito", "illegittimita"]].to_csv(REPO / "data/processed/esiti.csv", index=False)
    return e

def sedute():
    out = []
    for y in range(2004, 2027):
        rows = query(f"SELECT ?n ?sur WHERE {{ ?s <{ONTO}seduta> ?sed ; <{YEAR}> ?y ; <{NUM}> ?n . ?sed <{ONTO}haMembro> ?g . "
                     f"?g <http://xmlns.com/foaf/0.1/surname> ?sur FILTER(STR(?y) = \"{y}\") }}")
        out += [(y * 10000 + int(n), s) for n, s in rows]
    d = pd.DataFrame(out, columns=["pid", "surname"]).drop_duplicates()
    d.to_csv(REPO / "data/interim/sedute_membri.csv", index=False)
    return d

def wikipedia():
    def get(params):
        url = "https://it.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
        return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60))
    rows = []
    for dom in ["*.cortecostituzionale.it", "*.giurcost.org"]:
        cont = {}
        while True:
            d = get({"action": "query", "list": "exturlusage", "euquery": dom, "eulimit": "500", "euprop": "title|url",
                     "eunamespace": "0", "format": "json", **cont})
            for l in d["query"]["exturlusage"]:
                u = l["url"]
                m = (re.search(r"(?:anno|param_anno)=(\d{4}).*?(?:numero|param_numero)=(\d+)", u) or re.search(r"pronuncia/(\d{4})/(\d+)", u)
                     or re.search(r"COST:(\d{4}):(\d+)", u) or re.search(r"decisioni/(\d{4})/0*(\d+)[so]", u))
                if m and int(m.group(2)) > 0:
                    rows.append((int(m.group(1)) * 10000 + int(m.group(2)), l["title"]))
            if "continue" not in d:
                break
            cont = d["continue"]
    w = pd.DataFrame(rows, columns=["pid", "page"]).drop_duplicates()
    w.to_csv(REPO / "data/processed/wikipedia_links.csv", index=False)
    return w

if __name__ == "__main__":
    e = esiti(); w = wikipedia(); s = sedute()
    info = {"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "esiti_rows": len(e), "esiti_pronunce": int(e.pid.nunique()),
            "pronunce_illegittimita": int(e[e.illegittimita].pid.nunique()), "wikipedia_pairs": len(w), "wikipedia_pronunce": int(w.pid.nunique()),
            "wikipedia_pages": int(w.page.nunique()), "sedute_rows": len(s), "sedute_pronunce": int(s.pid.nunique())}
    json.dump(info, open(REPO / "reports/api_fetch.json", "w"), indent=1)
    print(info)
