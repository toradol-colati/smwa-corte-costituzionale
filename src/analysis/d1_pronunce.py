"""D1 - pronunce. (a) Is authority concentrated in a few precedents, beyond what a
time-respecting null gives? (b) Do HITS authorities coincide with the most cited
pronunce? (c) Does authority add information for predicting future citations?
(d) D1b: how long does a precedent last?

Rules fixed in docs/decisions.md (2026-11-11 and 2026-11-16). Outputs:
reports/d1_results.json, data/interim/d1_yearly.pkl
Usage: .venv/bin/python src/analysis/d1_pronunce.py
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import powerlaw
import scipy.sparse as sp
import statsmodels.api as sm
from lifelines import KaplanMeierFitter
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED = 20261116
REPS = int(__import__("os").environ.get("REPS", 1000))
START_YEAR = 1966  # the network reaches 1,000 pronunce (reports/data_inspection.md)


def gini(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


def hits(A, iters=200, tol=1e-10):
    """A[i, j] = 1 if i cites j. Returns (authority, hub)."""
    n = A.shape[0]
    a = np.ones(n) / np.sqrt(n)
    At = A.T.tocsr()
    for _ in range(iters):
        h = A @ a
        a2 = At @ h
        nrm = np.linalg.norm(a2)
        if nrm == 0:
            return a2, h
        a2 /= nrm
        if np.abs(a2 - a).max() < tol:
            a = a2
            break
        a = a2
    h = A @ a
    return a, h / (np.linalg.norm(h) or 1)


def pagerank(A, d=0.85, iters=100):
    n = A.shape[0]
    out = np.asarray(A.sum(1)).ravel()
    M = sp.diags(1 / np.where(out == 0, 1, out)) @ A
    r = np.ones(n) / n
    for _ in range(iters):
        r2 = (1 - d) / n + d * (M.T @ r + r[out == 0].sum() / n)
        if np.abs(r2 - r).sum() < 1e-10:
            break
        r = r2
    return r


def cohort_pct(values, cohort):
    """Percentile rank (0-100) within the cohort of pronunce deposited in the same year."""
    s = pd.Series(values)
    return (s.groupby(cohort).rank(pct=True, method="average") * 100).values


def compare(auth, indeg, cohort):
    """Agreement between authority and citation counts."""
    rho = float(spearmanr(auth, indeg)[0])
    k = max(1, len(auth) // 100)
    ta, ti = set(np.argsort(-auth, kind="stable")[:k]), set(np.argsort(-indeg, kind="stable")[:k])
    pa, pi = cohort_pct(auth, cohort), cohort_pct(indeg, cohort)
    r2 = float(np.corrcoef(pa, pi)[0, 1] ** 2)
    return {"spearman": rho, "top1_overlap": len(ta & ti) / k, "r2_cohort_pct": r2,
            "share_auth_zero": float((auth <= 1e-12).mean())}


def swap_null(ci, cj, yi, yj, dep, rng):
    """Uzzi-style swap: permute cited ids among citations with the same citing year and
    cited year; a swap is kept only if the cited pronuncia is still deposited no later
    than the citing one and no duplicate edge is created. Preserves in-degree, out-degree
    and the age of citations."""
    order = np.lexsort((rng.random(len(ci)), yj, yi))
    key = yi[order] * 10000 + yj[order]
    new = cj.copy()
    grp_start = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    grp_len = np.diff(np.r_[grp_start, len(key)])
    shift = np.repeat(grp_start, grp_len) + (np.arange(len(key)) - np.repeat(grp_start, grp_len) + 1) % np.repeat(grp_len, grp_len)
    new[order] = cj[order[shift]]  # rotate within the randomly ordered class = random derangement-like permutation
    bad = dep[new] > dep[ci]
    bad |= new == ci
    code = ci.astype(np.int64) * 100000 + new
    _, first_idx = np.unique(code, return_index=True)
    dup = np.ones(len(code), bool)
    dup[first_idx] = False
    bad |= dup
    new[bad] = cj[bad]
    return new


def network(nodes, edges, mask):
    sub = nodes[mask].sort_values(["data_deposito", "pid"]).reset_index(drop=True)
    idx = pd.Series(sub.index.values, index=sub.pid.values)
    e = edges[edges.citing_id.isin(idx.index) & edges.cited_id.isin(idx.index)]
    return sub, idx.loc[e.citing_id].values, idx.loc[e.cited_id].values


def main():
    rng = np.random.default_rng(SEED)
    nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_deposito"])
    edges = pd.read_csv(P / "edges_citations.csv")
    out = {}

    # ---------- (a) concentration of citations received, against an age-preserving null
    sub, ci, cj = network(nodes, edges, np.ones(len(nodes), bool))
    n = len(sub)
    year = sub.anno.values
    dep = sub.data_deposito.values.astype("datetime64[D]").astype(int)
    indeg = np.bincount(cj, minlength=n)
    k1 = n // 100
    obs = {"gini": gini(indeg), "top1_share": float(np.sort(indeg)[-k1:].sum() / len(cj)), "max": int(indeg.max()),
           "never_cited": float((indeg == 0).mean())}
    # null: every citation keeps its citing pronuncia and the year of its target; the target is
    # redrawn at random among the pronunce of that year deposited no later than the citing one.
    by_year = {y: np.flatnonzero(year == y) for y in np.unique(year)}
    cited_year = year[cj]
    null = {k: [] for k in obs}
    order = np.argsort(cited_year, kind="stable")
    bounds = np.searchsorted(cited_year[order], np.unique(cited_year))
    for _ in range(REPS):
        new = np.empty_like(cj)
        for y, a, b in zip(np.unique(cited_year), bounds, np.r_[bounds[1:], len(cj)]):
            pool = by_year[y]
            sel = order[a:b]
            draw = pool[rng.integers(0, len(pool), b - a)]
            late = dep[draw] > dep[ci[sel]]
            for _try in range(20):
                if not late.any():
                    break
                draw[late] = pool[rng.integers(0, len(pool), late.sum())]
                late = dep[draw] > dep[ci[sel]]
            draw[late] = cj[sel][late]
            new[sel] = draw
        d = np.bincount(new, minlength=n)
        null["gini"].append(gini(d)); null["top1_share"].append(float(np.sort(d)[-k1:].sum() / len(cj)))
        null["max"].append(int(d.max())); null["never_cited"].append(float((d == 0).mean()))
    out["concentration"] = {k: {"observed": obs[k], "null_mean": float(np.mean(v)), "null_lo": float(np.quantile(v, .025)),
                                "null_hi": float(np.quantile(v, .975)), "p": float((np.sum(np.array(v) >= obs[k]) + 1) / (REPS + 1))}
                            for k, v in null.items()}
    # variant (check of 17/11/2026): ordinanze are cited far less than sentenze, so the target is
    # also redrawn within the same type; own random stream, so that the other results do not move
    rng_t = np.random.default_rng(SEED + 1)
    tipo = (sub.tipo == "S").values.astype(int)
    key_c, key_n = cited_year * 2 + tipo[cj], year * 2 + tipo
    pools = {k: np.flatnonzero(key_n == k) for k in np.unique(key_c)}
    order_t = np.argsort(key_c, kind="stable")
    uk, st = np.unique(key_c[order_t], return_index=True)
    en = np.r_[st[1:], len(cj)]
    null_t = {k: [] for k in obs}
    for _ in range(REPS):
        new = np.empty_like(cj)
        for kk, a, b in zip(uk, st, en):
            pool, sel = pools[kk], order_t[a:b]
            draw = pool[rng_t.integers(0, len(pool), b - a)]
            late = dep[draw] > dep[ci[sel]]
            for _try in range(20):
                if not late.any():
                    break
                draw[late] = pool[rng_t.integers(0, len(pool), late.sum())]
                late = dep[draw] > dep[ci[sel]]
            draw[late] = cj[sel][late]
            new[sel] = draw
        d = np.bincount(new, minlength=n)
        null_t["gini"].append(gini(d)); null_t["top1_share"].append(float(np.sort(d)[-k1:].sum() / len(cj)))
        null_t["max"].append(int(d.max())); null_t["never_cited"].append(float((d == 0).mean()))
    out["concentration_by_type"] = {k: {"observed": obs[k], "null_mean": float(np.mean(v)), "null_lo": float(np.quantile(v, .025)),
                                        "null_hi": float(np.quantile(v, .975)), "p": float((np.sum(np.array(v) >= obs[k]) + 1) / (REPS + 1))}
                                    for k, v in null_t.items()}
    S_ = tipo == 1
    out["concentration_by_type"]["observed_by_type"] = {"gini_sentenze": gini(indeg[S_]), "never_cited_sentenze": float((indeg[S_] == 0).mean()),
                                                        "gini_ordinanze": gini(indeg[~S_]), "never_cited_ordinanze": float((indeg[~S_] == 0).mean())}
    fit = powerlaw.Fit(indeg[indeg > 0], discrete=True, verbose=False)
    R, p = fit.distribution_compare("power_law", "lognormal", normalized_ratio=True)
    R2, p2 = fit.distribution_compare("power_law", "truncated_power_law", normalized_ratio=True)
    out["tail"] = {"alpha": float(fit.power_law.alpha), "xmin": int(fit.power_law.xmin),
                   "n_tail": int((indeg >= fit.power_law.xmin).sum()), "vs_lognormal_R": float(R), "vs_lognormal_p": float(p),
                   "vs_truncated_R": float(R2), "vs_truncated_p": float(p2)}
    print("concentration", json.dumps(out["concentration"], indent=0)[:600], out["tail"], flush=True)

    # ---------- (b) authority vs citations on three networks, with the swap null at the end year
    nets = {"replica_agnoloni_pagallo": (nodes.tipo == "S") & (nodes.giudizio == "incidentale") & (nodes.anno <= 2014),
            "rete_completa": np.ones(len(nodes), bool), "sole_sentenze": nodes.tipo == "S"}
    yearly = []
    for name, mask in nets.items():
        sub, ci, cj = network(nodes, edges, mask.values if hasattr(mask, "values") else mask)
        n = len(sub)
        year = sub.anno.values
        dep = sub.data_deposito.values.astype("datetime64[D]").astype(int)
        A = sp.csr_matrix((np.ones(len(ci)), (ci, cj)), shape=(n, n))
        a, h = hits(A)
        indeg = np.asarray(A.sum(0)).ravel()
        res = compare(a, indeg, year)
        res["pagerank"] = compare(pagerank(A), indeg, year)
        res["nodes"], res["edges"] = int(n), int(len(ci))
        top30 = np.argsort(-indeg, kind="stable")[:30]
        res["top30_spearman_auth_indeg"] = float(spearmanr(a[top30], indeg[top30])[0])
        res["top30_same_order"] = bool((np.argsort(-a[top30], kind="stable") == np.arange(30)).all())
        res["top30_auth_in_top30_cited"] = int(len(set(np.argsort(-a)[:30]) & set(top30)))
        nul = {"spearman": [], "top1_overlap": [], "r2_cohort_pct": []}
        yi, yj = year[ci], year[cj]
        for _ in range(REPS):
            new = swap_null(ci, cj, yi, yj, dep, rng)
            An = sp.csr_matrix((np.ones(len(ci)), (ci, new)), shape=(n, n))
            an, _ = hits(An, iters=60, tol=1e-7)
            c = compare(an, indeg, year)  # in-degree is preserved by the swap
            for k in nul:
                nul[k].append(c[k])
        for k, v in nul.items():
            res[k + "_null"] = {"mean": float(np.mean(v)), "lo": float(np.quantile(v, .025)), "hi": float(np.quantile(v, .975)),
                                "p_lower": float((np.sum(np.array(v) <= res[k]) + 1) / (REPS + 1))}
        out[name] = res
        print(name, {k: v for k, v in res.items() if k != "pagerank"}, flush=True)
        # yearly series (full network and sentenze only)
        if name != "replica_agnoloni_pagallo":
            for y in range(START_YEAR, int(year.max()) + 1):
                m = year <= y
                nn = int(m.sum())
                keep = m[ci]
                Ay = sp.csr_matrix((np.ones(keep.sum()), (ci[keep], cj[keep])), shape=(nn, nn))
                ay, hy = hits(Ay, iters=100, tol=1e-8)
                iy = np.asarray(Ay.sum(0)).ravel()
                c = compare(ay, iy, year[:nn])
                c.update(year=y, net=name)
                yearly.append(c)
                if name == "rete_completa":
                    recent = np.bincount(cj[keep & (year[ci] == y)], minlength=nn)
                    pd.DataFrame({"pid": sub.pid.values[:nn], "year": y, "auth_pct": cohort_pct(ay, year[:nn]),
                                  "hub_pct": cohort_pct(hy, year[:nn]), "cum_cit": iy, "cit_year": recent,
                                  "age": y - year[:nn]}).to_pickle(REPO / f"data/interim/d1_panel_{y}.pkl")
    yr = pd.DataFrame(yearly)
    yr.to_pickle(REPO / "data/interim/d1_yearly.pkl")
    out["yearly_summary"] = {net: {k: [float(x[k].min()), float(x[k].median()), float(x[k].max())]
                                   for k in ["spearman", "top1_overlap", "r2_cohort_pct", "share_auth_zero"]}
                             for net, x in yr.groupby("net")}

    # ---------- (c) one pre-registered prediction test
    panel = pd.concat([pd.read_pickle(REPO / f"data/interim/d1_panel_{y}.pkl") for y in range(START_YEAR, 2025)])
    nxt = pd.concat([pd.read_pickle(REPO / f"data/interim/d1_panel_{y}.pkl")[["pid", "year", "cit_year"]]
                     for y in range(START_YEAR + 1, 2026)])
    nxt["year"] -= 1
    panel = panel.merge(nxt.rename(columns={"cit_year": "y_next"}), on=["pid", "year"])
    panel["l_cum"], panel["l_rec"], panel["age2"] = np.log1p(panel.cum_cit), np.log1p(panel.cit_year), panel.age ** 2
    train, test = panel[panel.year <= 2009], panel[panel.year >= 2010]
    base = ["l_cum", "l_rec", "age", "age2"]
    alpha = max(1e-3, float(((train.y_next.var() - train.y_next.mean()) / train.y_next.mean() ** 2)))
    fam = sm.families.NegativeBinomial(alpha=alpha)
    dev = {}
    coefs = {}
    for label, cols in [("citations", base), ("citations_authority", base + ["auth_pct"])]:
        m = sm.GLM(train.y_next, sm.add_constant(train[cols]), family=fam).fit()
        mu = m.predict(sm.add_constant(test[cols]))
        dev[label] = fam.resid_dev(test.y_next.values, mu.values) ** 2
        coefs[label] = {k: [float(m.params[k]), float(m.bse[k])] for k in m.params.index}
    test = test.assign(d0=dev["citations"], d1=dev["citations_authority"])
    bypid = test.groupby("pid")[["d0", "d1"]].sum().values
    red = 1 - bypid[:, 1].sum() / bypid[:, 0].sum()
    boot = []
    for _ in range(REPS):
        s = bypid[rng.integers(0, len(bypid), len(bypid))]
        boot.append(1 - s[:, 1].sum() / s[:, 0].sum())
    out["prediction"] = {"train_rows": int(len(train)), "test_rows": int(len(test)), "test_pronunce": int(len(bypid)), "alpha": alpha,
                         "deviance_citations": float(bypid[:, 0].sum()), "deviance_with_authority": float(bypid[:, 1].sum()),
                         "reduction": float(red), "reduction_lo": float(np.quantile(boot, .025)), "reduction_hi": float(np.quantile(boot, .975)),
                         "criterion_met": bool(red >= 0.02 and np.quantile(boot, .025) > 0), "coefs": coefs}
    print("prediction", {k: v for k, v in out["prediction"].items() if k != "coefs"}, flush=True)

    # ---------- (d) D1b: ageing of precedents
    sub, ci, cj = network(nodes, edges, np.ones(len(nodes), bool))
    year = sub.anno.values
    age = year[ci] - year[cj]
    n_year = pd.Series(year).value_counts()
    citing_per_year = pd.Series(year[ci]).value_counts()  # citations made per year
    # rate at age a = citations of age a / sum over citing years of (citations made that year x precedents of year - a available)
    num = np.bincount(age, minlength=71).astype(float)
    den = np.zeros(71)
    for y, c in citing_per_year.items():
        for a in range(0, 71):
            if (y - a) in n_year.index:
                den[a] += c * n_year[y - a] / n_year[n_year.index <= y].sum()
    rate = num / np.where(den == 0, np.nan, den)  # relative to uniform choice among available precedents (=1)
    peak = int(np.nanargmax(rate[:30]))
    half = next((a for a in range(peak, 60) if rate[a] <= rate[peak] / 2), None)
    out["ageing"] = {"relative_rate_by_age": [None if np.isnan(x) else float(x) for x in rate[:61]], "peak_age": peak,
                     "half_life_after_peak": None if half is None else int(half - peak),
                     "age_when_rate_below_1": next((a for a in range(peak, 60) if rate[a] < 1), None)}
    # survival: years from deposit to the last citation received; the precedent is "dead" if
    # 10 full years pass after its last citation (or after deposit) before the end of the data
    END = 2026
    last = pd.Series(year[ci]).groupby(cj).max().reindex(range(len(sub)))
    life = (last.fillna(pd.Series(year)) - year).values.astype(float)
    last_y = last.fillna(pd.Series(year)).values
    dead = (END - last_y) >= 10
    dur = np.where(dead, life, END - year)
    kmf = KaplanMeierFitter().fit(dur, dead)
    surv = kmf.survival_function_at_times([0, 1, 5, 10, 20, 30, 40, 50]).to_dict()
    out["survival"] = {"km": {int(k): float(v) for k, v in surv.items()}, "median": float(kmf.median_survival_time_),
                       "share_cited_after_30y": float(((last_y - year) >= 30)[year <= END - 30].mean()),
                       "n_old": int((year <= END - 30).sum())}
    S = sub.tipo.values == "S"
    for lab, msk in [("sentenze", S), ("ordinanze", ~S)]:
        k = KaplanMeierFitter().fit(dur[msk], dead[msk])
        out["survival"][lab] = {"median": float(k.median_survival_time_), "km10": float(k.survival_function_at_times([10]).iloc[0])}
    json.dump(out, open(REPO / "reports/d1_results.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ["ageing", "survival", "yearly_summary"]}, indent=0)[:1500])


if __name__ == "__main__":
    main()
