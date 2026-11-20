"""D3, secondary full model: why are the precedents decided during the drafter's mandate cited less
than precedents of the same age class decided before the drafter joined the Court (odds ratio 0.88,
whether the drafter sat or was absent)?  Exploratory check, added on 20/11/2026 after an external
review; variants, reading rule and stop rule fixed in docs/decisions.md before any estimate.
Only existing columns are used (no new construct), and no age x seniority term: inside a citing
pronuncia "in mandate" is an age cut-off at the drafter's seniority, so such terms would remove the
identification of the coefficient.
  0  baseline: must reproduce the full model of reports/d3_results.json exactly; identification
     table (rows inside/outside the mandate by age class, strata whose cut-off falls in each class)
     and raw curve (cases per sampled control by quarter of age, first three years)
  1  quarter-year age classes in the first two years
  2  separate samples by period of the citing pronuncia (to 2000, from 2001)
  3  separate samples by type of the citing pronuncia (sentenze, ordinanze)
  4  same challenged provision and similarity of the constitutional articles, together
  5  two other samples of controls (seeds +1, +2)
Every model also reports the ratio present/absent (sat_not_drafted / in_mandate_absent) with the
interval from the full cluster-robust covariance.
Output: reports/d3_full_check.json.  Usage: .venv/bin/python src/analysis/d3_full_check.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/analysis"))
import d3_memoria_collegiale as d3  # noqa: E402

FINE_BINS = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 3, 4, 5, 7, 10, 15, 20, 30, 200]
HALF = float(np.exp(np.log(0.875) / 2))  # reading rule: half of the baseline distance from 1, log scale
T0 = time.time()


def log(msg):
    print(f"[{time.time() - T0:7.0f}s] {msg}", flush=True)


def fit(t, label, start=None, **kw):
    """Exact conditional logit. Starts from the Breslow estimate, as in d3_memoria_collegiale.py, unless `start`
    (name -> beta) is given: then from those values, and zero for the other columns."""
    t = t.sort_values(["citing", "y"], ascending=[True, False]).reset_index(drop=True)
    X, names = d3.design(t, "full", **kw)
    for need in ["sat_not_drafted", "in_mandate_absent"] + (["same_challenged_act", "param_similarity"] if kw.get("norme") else []):
        assert need in names, f"{need} missing from the design of {label}"
    y, strata, cluster = t.y.values.astype(float), t.citing.values, t.R.values
    b0 = d3.clogit_breslow(X, y, strata, cluster)[0] if start is None else np.array([start.get(n, 0.0) for n in names])
    model = d3.ExactCLogit(X, y, strata, cluster)
    b, V, ll, G, S = model.fit(b0)
    i, j = names.index("sat_not_drafted"), names.index("in_mandate_absent")
    se = np.sqrt(np.diag(V))
    coef = {n: {"or": float(np.exp(b[k])), "lo": float(np.exp(b[k] - 1.96 * se[k])), "hi": float(np.exp(b[k] + 1.96 * se[k]))}
            for k, n in enumerate(names)}
    dr, sr = b[i] - b[j], np.sqrt(V[i, i] + V[j, j] - 2 * V[i, j])
    res = {"label": label, "strata": int(S), "clusters": int(G), "rows": int(len(t)), "cases": int(t.y.sum()),
           "sat_not_drafted": coef["sat_not_drafted"], "in_mandate_absent": coef["in_mandate_absent"],
           "ratio_present_absent": {"or": float(np.exp(dr)), "lo": float(np.exp(dr - 1.96 * sr)), "hi": float(np.exp(dr + 1.96 * sr))},
           "reaches_half": bool(coef["sat_not_drafted"]["or"] >= HALF), "converged": model.converged, "max_newton_step": model.max_newton_step, "newton_iterations": model.n_iter,
           "start": "breslow" if start is None else "baseline exact estimates", "beta": dict(zip(names, map(float, b))), "coef": coef}
    log(f"{label} [{'converged' if model.converged else 'NOT CONVERGED'}, {model.n_iter} it.]: sat {res['sat_not_drafted']['or']:.3f} ({res['sat_not_drafted']['lo']:.3f}-{res['sat_not_drafted']['hi']:.3f}), "
        f"absent {res['in_mandate_absent']['or']:.3f}, ratio {res['ratio_present_absent']['or']:.3f} "
        f"({res['ratio_present_absent']['lo']:.3f}-{res['ratio_present_absent']['hi']:.3f})")
    return res


def main():
    nodes, coll, app, edges, theta = d3.load()
    cache = REPO / "data/interim/d3_full.pkl"
    if cache.exists():
        t = pd.read_pickle(cache)
    else:
        acts, arts, _ = d3.load_norme()
        par = d3.load_parametri()
        t = d3.build(nodes, coll, app, edges, theta, "full", norme=(acts, arts), param=par)
        t.to_pickle(cache)
    log(f"table: {len(t):,} rows, {t.citing.nunique():,} strata")
    out = {"half_threshold": HALF}
    # 0. baseline, reproduction of reports/d3_results.json
    ref = json.load(open(REPO / "reports/d3_results.json"))["full"]["coef"]
    base = fit(t, "0 modello completo, come in d3_results.json")
    for k in ["sat_not_drafted", "in_mandate_absent"]:
        assert abs(base[k]["or"] - ref[k]["or"]) < 1e-6, f"baseline does not reproduce {k}: {base[k]['or']} vs {ref[k]['or']}"
    out["baseline"] = base
    # identification: where the cut-off falls, and how many rows sit on each side of it
    nd = nodes.set_index("pid")
    first = app["first"]
    seniority = (nd.data_deposito.reindex(t.citing).values - first.reindex(t.R).values) / np.timedelta64(1, "D") / 365.25
    t["seniority"] = seniority
    t["status"] = np.select([t.self_drafted == 1, t.sat_not_drafted == 1, t.in_mandate == 1], ["redatto", "presente", "assente"], "prima del mandato")
    t["age_class"] = pd.cut(t.age, d3.AGE_BINS, right=False).astype(str)
    st = t.groupby("citing").agg(sen=("seniority", "first"))
    st["cls"] = pd.cut(st.sen, d3.AGE_BINS, right=False).astype(str)
    ident = {}
    for cls, g in t.groupby("age_class", observed=True):
        ident[cls] = {s: {"cases": int(g[g.status == s].y.sum()), "controls": int((g.status == s).sum() - g[g.status == s].y.sum())}
                      for s in ["presente", "assente", "prima del mandato"]}
        ident[cls]["strata_with_cutoff_in_class"] = int((st.cls == cls).sum())
    out["identification"] = {"by_age_class": ident, "seniority_quantiles": {str(q): float(st.sen.quantile(q)) for q in [0.1, 0.25, 0.5, 0.75, 0.9]}}
    young = t[(t.age < 3) & (t.status != "redatto")].copy()
    young["q"] = (young.age // 0.25 * 0.25).round(2)
    curve = young.groupby(["q", young.in_mandate.map({1: "nel mandato", 0: "prima del mandato"})]).y.agg(["sum", "size"])
    out["raw_curve_first_3_years"] = [{"age_from": float(q), "side": s, "cases": int(r["sum"]), "controls": int(r["size"] - r["sum"]),
                                       "cases_per_control": float(r["sum"] / max(r["size"] - r["sum"], 1))} for (q, s), r in curve.iterrows()]
    t = t.drop(columns=["seniority", "status", "age_class"])
    # 1. quarter-year classes in the first two years
    out["v1_fine_young_ages"] = fit(t, "1 classi di età trimestrali nei primi due anni", bins=FINE_BINS)
    # 2. by period, 3. by type of the citing pronuncia
    out["v2_period"] = {"fino al 2000": fit(t[t.anno <= 2000], "2 citanti fino al 2000"), "dal 2001": fit(t[t.anno >= 2001], "2 citanti dal 2001")}
    out["v3_type"] = {"sentenze": fit(t[t.tipo == "S"], "3 solo sentenze che citano"), "ordinanze": fit(t[t.tipo == "O"], "3 solo ordinanze che citano")}
    # 4. challenged provision and constitutional articles
    # from the Breslow start this model does not converge: "same challenged article" almost separates cases from controls
    # (docs/decisions.md, 20/11/2026); it starts from the exact baseline estimates, zero for the new columns
    out["v4_norme_param"] = fit(t, "4 disposizione impugnata e articoli della Costituzione", start=base["beta"], norme=True, param=True)
    # 5. other control samples
    out["v5_seeds"] = {}
    for s in (1, 2):
        ts = d3.build(nodes, coll, app, edges, theta, "full", rng=np.random.default_rng(d3.SEED + s))
        out["v5_seeds"][f"seed+{s}"] = fit(ts, f"5 controlli con seed +{s}")
    json.dump(out, open(REPO / "reports/d3_full_check.json", "w"), indent=1, ensure_ascii=False)
    log("done")


if __name__ == "__main__":
    main()
