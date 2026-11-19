"""How well the D2 permutation strata separate judge and subject (check of 19/11/2026): share of the
pronunce of the tested judges that sit in strata with at least two different drafters. A pronuncia alone
with its drafter in its stratum cannot be exchanged, and pushes that judge's ratio towards 1.
Output: reports/d2_strata_check.json
Usage: .venv/bin/python src/analysis/d2_strata_check.py
"""
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
nodes = pd.read_csv(REPO / "data/processed/nodes.csv")
d2 = json.load(open(REPO / "reports/d2_results.json"))
tested = {r["judge_id"] for r in d2["permutazione_anno"]["table"]}
main = pd.read_csv(REPO / "data/processed/parametri_pronunce.csv").set_index("pid").main_article.astype(str)
topic = pd.read_csv(REPO / "data/processed/topics_pronunce.csv").set_index("pid").topic
nodes["main"] = nodes.pid.map(main).fillna("nessuno")
nodes["topic"] = nodes.pid.map(topic).fillna(-1)
nodes["red"] = nodes.redattore_ids.astype(str)
own = nodes.red.apply(lambda s: any(int(x) in tested for x in s.split("|") if x not in ("", "nan", "0")))
out = {}
for lab, keys in [("anno", ["anno"]), ("anno_tipo", ["anno", "tipo"]), ("anno_tipo_materia", ["anno", "tipo", "topic"]),
                  ("anno_tipo_parametro", ["anno", "tipo", "main"])]:
    mixed = nodes.groupby(keys).red.transform("nunique") >= 2
    out[lab] = {"share_tested_pronunce_in_mixed_strata": float(mixed[own].mean()), "strata": int(nodes.groupby(keys).ngroups)}
json.dump(out, open(REPO / "reports/d2_strata_check.json", "w"), indent=1)
print(json.dumps(out, indent=1))
