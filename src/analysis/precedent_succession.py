"""Is a precedent forgotten after a few years because one of the pronunce that cited it takes its place?
Exploratory check asked by Umberto on 21/11/2026; rules fixed in docs/decisions.md before running.
  precedents P     deposited 1970-2010 (at least 15 years of follow-up), cited at least 5 times in the first
                   3 years after deposit (age < 4 years)
  successors       pronunce deposited within 3 years after P that cite P
  controls         for every successor, one pronuncia drawn at random (seed) with the same year of deposit, the
                   same type and the same main topic, that does not cite P
  later window     citations made when P is 4 to 15 years old, counted only from pronunce that do NOT cite P
                   (a citation of the successor in place of P, not next to it)
Reading rule: replacement is supported if (a) successors receive more later citations than their controls
(ratio, 95% bootstrap interval over precedents, lower bound above 1) and (b) in the later window the
successors together receive more citations from pronunce that do not cite P than P itself receives.
Output: reports/precedent_succession.json.  Usage: .venv/bin/python src/analysis/precedent_succession.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED, REPS = 20261125, 1000
nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_deposito"])
edges = pd.read_csv(P / "edges_citations.csv")
z = np.load(P / "topics_theta.npz")
topic = dict(zip(z["pid"], z["theta"].argmax(1)))
dep = dict(zip(nodes.pid, nodes.data_deposito))
tipo = dict(zip(nodes.pid, nodes.tipo))
year = dict(zip(nodes.pid, nodes.anno))
citers = edges.groupby("cited_id").citing_id.apply(list).to_dict()
YEAR = np.timedelta64(int(365.25 * 24 * 3600), "s")


def age(p, c):  # years between the deposit of p and of c
    return (dep[c] - dep[p]) / pd.Timedelta(days=365.25)


pool = nodes[nodes.pid.isin(topic)].groupby(["anno", "tipo"]).pid.apply(list).to_dict()
rng = np.random.default_rng(SEED)
rows = []
for p in nodes.pid[(nodes.anno >= 1970) & (nodes.anno <= 2010)]:
    cs = citers.get(p, [])
    early = [c for c in cs if age(p, c) < 4]
    if len(early) < 5 or p not in topic:
        continue
    cite_p = set(cs)
    succ, ctrl = [], []
    for s in early:
        if s not in topic:
            continue
        cand = [x for x in pool.get((year[s], tipo[s]), []) if topic[x] == topic[s] and x not in cite_p and x != p]
        if cand:
            succ.append(s)
            ctrl.append(cand[rng.integers(len(cand))])

    def later(x, exclude_p=True):
        return sum(1 for c in citers.get(x, []) if 4 <= age(p, c) <= 15 and (not exclude_p or c not in cite_p))
    p_later = sum(1 for c in cs if 4 <= age(p, c) <= 15)
    bands = {f"{a}-{b}": sum(1 for c in cs if a <= age(p, c) < b + 1) for a, b in [(0, 3), (4, 7), (8, 11), (12, 15)]}
    rows.append({"pid": int(p), "early": len(early), "successors": len(succ), "p_later": p_later,
                 "succ_later": sum(later(s) for s in succ), "ctrl_later": sum(later(x) for x in ctrl), **{"p_" + k: v for k, v in bands.items()}})
d = pd.DataFrame(rows)
d = d[d.successors > 0]
ratio = d.succ_later.sum() / d.ctrl_later.sum()
boot = []
for _ in range(REPS):
    i = rng.integers(len(d), size=len(d))
    boot.append(d.succ_later.values[i].sum() / d.ctrl_later.values[i].sum())
lo, hi = np.percentile(boot, [2.5, 97.5])
out = {"precedents": int(len(d)), "successors": int(d.successors.sum()),
       "p_citations_by_age": {k: float(d["p_" + k].mean()) for k in ["0-3", "4-7", "8-11", "12-15"]},
       "later_window": {"p_itself_mean": float(d.p_later.mean()), "successors_mean": float(d.succ_later.mean()),
                        "controls_mean": float(d.ctrl_later.mean()), "ratio_successors_controls": float(ratio),
                        "ratio_lo": float(lo), "ratio_hi": float(hi)},
       "share_precedents_successors_exceed_p": float((d.succ_later > d.p_later).mean())}
a = lo > 1
b = d.succ_later.sum() > d.p_later.sum()
out["reading"] = {"a_successors_above_controls": bool(a), "b_successors_above_p": bool(b),
                  "verdict": "sostenuta" if (a and b) else ("parziale" if (a or b) else "non sostenuta")}
json.dump(out, open(REPO / "reports/precedent_succession.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
