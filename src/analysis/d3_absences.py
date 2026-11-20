"""Absences from the collegio, the source of identification of the D3 primary result.
Required by .claude/rules/network-analysis.md ("descrivere le assenze per tipo di giudizio e materia").
1. Absence rate at the level judge x pronuncia: for every judge and every pronuncia decided between the
   judge's first and last collegio appearance, absent = the judge is not in that collegio. Rates by type of
   proceeding, decade, main constitutional article and topic, with chi-square tests and Cramer's V (with
   hundreds of thousands of pairs any difference is "significant": the effect size is what matters).
2. Balance in the D3 table (data/interim/d3_mandate.pkl, risk set of the primary model): among the non-cited
   precedents (random sample of the risk set), those decided with the drafter present but not drafting versus
   those decided in the drafter's absence; standardized mean differences of the covariates.
3. Are the absences real? Share of present and absent rows whose precedent has an incomplete collegio
   (fewer than 11 recognised judges, the legal quorum), which would turn an extraction failure into an absence;
   and how the absent rows and cases are spread across drafters (a result resting on a few long absences
   would show here).
Output: reports/d3_absences.json
Usage: .venv/bin/python src/analysis/d3_absences.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_decisione", "data_deposito"])
nodes["dec"] = nodes.data_decisione.fillna(nodes.data_deposito)
coll = pd.read_csv(P / "collegio.csv").merge(nodes[["pid", "dec"]], on="pid")
app = coll.groupby("judge_id").dec.agg(first="min", last="max")
sat = set(zip(coll.pid, coll.judge_id))
main = pd.read_csv(P / "parametri_pronunce.csv").set_index("pid").main_article.astype(str)
topic = pd.read_csv(P / "topics_pronunce.csv").set_index("pid").topic
nodes["main"] = nodes.pid.map(main).fillna("nessuno")
top_art = nodes.main.value_counts().index[:10]
nodes["main10"] = np.where(nodes.main.isin(top_art), nodes.main, "altri")
nodes["topic"] = nodes.pid.map(topic).fillna(-1).astype(int)
nodes["decade"] = nodes.anno // 10 * 10
rows = []
dec = nodes.dec.values
for j, r in app.iterrows():
    m = (dec >= r["first"]) & (dec <= r["last"])
    sub = nodes.loc[m, ["pid", "giudizio", "decade", "main10", "topic"]].copy()
    sub["judge"] = j
    rows.append(sub)
pairs = pd.concat(rows, ignore_index=True)
pairs["absent"] = [(p, j) not in sat for p, j in zip(pairs.pid, pairs.judge)]
out = {"pairs": int(len(pairs)), "absence_rate": float(pairs.absent.mean()), "by": {}}
for col in ["giudizio", "decade", "main10", "topic"]:
    tab = pd.crosstab(pairs[col], pairs.absent)
    chi2, p, dof, _ = chi2_contingency(tab)
    v = float(np.sqrt(chi2 / (len(pairs) * (min(tab.shape) - 1))))
    rates = pairs.groupby(col).absent.agg(["mean", "size"])
    out["by"][col] = {"cramers_v": v, "p": float(p), "rates": {str(k): {"rate": float(x["mean"]), "n": int(x["size"])} for k, x in rates.iterrows()},
                      "min_rate": float(rates["mean"].min()), "max_rate": float(rates["mean"].max())}
# balance in the D3 risk set
t = pd.read_pickle(REPO / "data/interim/d3_mandate.pkl")
nd = nodes.set_index("pid")
t["cited_incidentale"] = t.cited.map(nd.giudizio).eq("incidentale").astype(float)
t["cited_sentenza"] = t.tipo_cited.eq("S").astype(float)
t["cited_year"] = t.cited.map(nd.anno).astype(float)
ctrl = t[(t.y == 0) & (t.self_drafted == 0)]
pres, absn = ctrl[ctrl.sat == 1], ctrl[ctrl.sat == 0]
bal = {}
for col, lab in [("age", "età del precedente (anni)"), ("sim", "somiglianza di materia (topic)"), ("param_sim", "somiglianza degli articoli della Costituzione"),
                 ("cited_sentenza", "il precedente è una sentenza"), ("cited_incidentale", "il precedente viene da un giudizio incidentale"),
                 ("cited_year", "anno del precedente")]:
    a, b = pres[col].astype(float), absn[col].astype(float)
    smd = (a.mean() - b.mean()) / np.sqrt((a.var() + b.var()) / 2)
    bal[col] = {"label": lab, "mean_present": float(a.mean()), "mean_absent": float(b.mean()), "smd": float(smd)}
out["balance"] = {"controls_present": int(len(pres)), "controls_absent": int(len(absn)), "covariates": bal,
                  "max_abs_smd": float(max(abs(x["smd"]) for x in bal.values()))}
# 3. real absences: incomplete collegi and spread across drafters
size = coll.groupby("pid").judge_id.nunique()
t["collegio_size"] = t.cited.map(size).fillna(0).astype(int)
groups = {"present": t[t.sat_not_drafted == 1], "absent": t[t.sat == 0]}
out["collegio_quality"] = {"pronunce_collegio_under_11": int(nodes.pid.map(size).fillna(0).lt(11).sum()),
                           **{k: {"rows": int(len(g)), "cases": int(g.y.sum()), "share_collegio_under_11": float(g.collegio_size.lt(11).mean())}
                              for k, g in groups.items()}}
ab = groups["absent"].groupby("R").agg(rows=("y", "size"), cases=("y", "sum"))
out["spread_by_drafter"] = {"drafters": int(t.R.nunique()), "drafters_with_absent_rows": int(len(ab)),
                            "drafters_with_absent_cases": int((ab.cases > 0).sum()),
                            "top5_share_absent_rows": float(ab.rows.nlargest(5).sum() / ab.rows.sum()),
                            "top5_share_absent_cases": float(ab.cases.nlargest(5).sum() / ab.cases.sum())}
json.dump(out, open(REPO / "reports/d3_absences.json", "w"), indent=1)
print(json.dumps({k: (v if k != "by" else {c: {x: v[c][x] for x in ["cramers_v", "min_rate", "max_rate"]} for c in v}) for k, v in out.items() if k != "balance"}, indent=1))
print(out["collegio_quality"], out["spread_by_drafter"])
print(json.dumps({c: (round(x["mean_present"], 3), round(x["mean_absent"], 3), round(x["smd"], 3)) for c, x in bal.items()}, indent=1), out["balance"]["controls_present"], out["balance"]["controls_absent"])
