"""Sizing of the references to other courts in the texts of the Constitutional Court (19/11/2026),
before any extractor: how many pronunce name each court, in the base text (Considerato in diritto and
dispositivo) and in the facts, how many with a decision identifier nearby, by decade. Also fixes the
development/test split of the citing pronunce for the court extractors (seed 20261123), before reading.
A mention of a court is not a citation of a decision: many are generic ("la giurisprudenza della Cassazione").
Outputs: reports/courts_sizing.json, data/interim/courts_split.csv
Usage: .venv/bin/python src/courts/sizing.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
COURTS = {
    "Cassazione": r"Corte (?:suprema )?di cassazione|\bCassazione\b|\bCass\.",
    "Corte EDU": r"Corte europea dei diritti dell['’]uomo|Corte EDU|Corte di Strasburgo|Corte europea dei diritti umani",
    "Corte di giustizia UE": r"Corte di giustizia|CGUE|Corte di Lussemburgo",
    "Consiglio di Stato": r"Consiglio di Stato|Cons\. ?Stato",
}
IDENT = {"Cassazione": r"n\.\s*\d{2,6}", "Corte EDU": r"\bc\.\s|\bcontro\b|ricors[oi] n\.",
         "Corte di giustizia UE": r"\bC-\d+/\d+|caus[ae]\s+C", "Consiglio di Stato": r"n\.\s*\d{2,6}"}
df = pd.read_pickle(REPO / "data/interim/pronunce.pkl")
base = df.diritto.fillna("") + " " + df.dispositivo.fillna("")
facts = df.fatto.fillna("") + " " + df.intro.fillna("")
decade = df.anno // 10 * 10
out = {"pronunce": int(len(df)), "pronunce_by_decade": {int(k): int(v) for k, v in decade.value_counts().sort_index().items()}, "courts": {}}
for k, rx in COURTS.items():
    in_base = base.str.contains(rx, regex=True)
    with_id = base.str.contains(rf"(?:{rx})[^.;]{{0,160}}?(?:{IDENT[k]})", regex=True)
    out["courts"][k] = {"pronunce_base": int(in_base.sum()), "pronunce_base_with_identifier": int(with_id.sum()),
                        "pronunce_facts": int(facts.str.contains(rx, regex=True).sum()), "mentions_base": int(base.str.count(rx).sum()),
                        "pronunce_base_by_decade": {int(d): int(v) for d, v in in_base.groupby(decade).sum().items()}}
pids = np.sort(df.pid.unique())
dev = set(np.random.default_rng(20261123).permutation(pids)[: len(pids) // 2])
pd.DataFrame({"pid": pids, "half": ["dev" if p in dev else "test" for p in pids]}).to_csv(REPO / "data/interim/courts_split.csv", index=False)
json.dump(out, open(REPO / "reports/courts_sizing.json", "w"), indent=1)
print(json.dumps({k: {x: v[x] for x in ["pronunce_base", "pronunce_base_with_identifier", "mentions_base"]} for k, v in out["courts"].items()}, indent=1))
