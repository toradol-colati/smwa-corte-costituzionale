"""Exploratory measures from the course textbooks (Easley and Kleinberg 2010; Barabasi 2016), each
with its null or reference model. Added on 18/11/2026 to cover the course topics: not part of the
analyses fixed before the results.

1. Rich get richer (preferential attachment): exponent a of E[new citations in year t+1] ~
   (1 + citations up to t)^a, comparing each pronuncia only with the pronunce deposited in the same
   year, at the same year t (cell means as offset and as reference; topic of Barabasi, ch. 5). a = 0: no attachment; a = 1: linear attachment. Reference: the same estimate on 5 networks
   of the D1 null (every citation keeps its citing pronuncia and the year of its target, which is
   redrawn at random), where a should be about 0.
2. Triadic closure: transitivity of the undirected citation network, against the time-respecting
   swap null (Uzzi et al. 2013, as in D1), which keeps citations made, citations received and the
   age of every citation. The directed version is not used (.claude/rules/network-analysis.md).
3. Degree correlations: correlation between the citations received by the citing and by the cited
   pronuncia, and between the citations made by the citing and received by the cited one; same null.
4. Small world: average distance and transitivity of the undirected giant component, against an
   Erdos-Renyi graph with the same number of nodes and edges.
5. Bridges: betweenness (undirected); share of the neighbours in other communities for the top 1%,
   against the top 1% by citations received and against all connected pronunce.
6. Robustness: giant component after removing the most cited pronunce, against random removal.
Output: reports/course_measures.json
Usage: .venv/bin/python src/analysis/course_measures.py
"""
import json
import random
import sys
from pathlib import Path

import igraph as ig
import numpy as np
import pandas as pd
import statsmodels.api as sm

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/analysis"))
from d1_pronunce import network, swap_null  # noqa: E402

P = REPO / "data/processed"
SEED = 20261116
REPS = 100
rng = np.random.default_rng(SEED)
random.seed(SEED)
nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_deposito"])
edges = pd.read_csv(P / "edges_citations.csv")
sub, ci, cj = network(nodes, edges, np.ones(len(nodes), bool))
n = len(sub)
year = sub.anno.values
dep = sub.data_deposito.values.astype("datetime64[D]").astype(int)
yi, yj = year[ci], year[cj]
out = {"reps": REPS}


# 1. preferential attachment
def attachment(cj_):
    rows = []
    for t in range(1966, int(year.max())):
        alive = np.flatnonzero(year <= t)
        k = np.bincount(cj_[yi <= t], minlength=n)[alive]
        new = np.bincount(cj_[yi == t + 1], minlength=n)[alive]
        rows.append(pd.DataFrame({"pid": alive, "cohort": year[alive], "t": t, "k": k, "y": new}))
    d = pd.concat(rows, ignore_index=True)
    cell = d.groupby(["cohort", "t"])
    d["y_cell"], d["k_cell"] = cell.y.transform("mean"), cell.k.transform("mean")
    d = d[d.y_cell > 0]
    x = np.log((1 + d.k.values) / (1 + d.k_cell.values))
    alpha = max(1e-3, float(((d.y - d.y_cell) ** 2).mean() - d.y.mean()) / float((d.y_cell ** 2).mean()))
    m = sm.GLM(d.y.values, sm.add_constant(x), offset=np.log(d.y_cell.values), family=sm.families.NegativeBinomial(alpha=alpha)
               ).fit(cov_type="cluster", cov_kwds={"groups": d.pid.values})
    b, se = float(m.params[1]), float(m.bse[1])
    return {"a": b, "lo": b - 1.96 * se, "hi": b + 1.96 * se, "rows": int(len(d))}


def year_null(cj_):
    """D1 null: the target is redrawn among pronunce of the same year deposited no later than the citing one."""
    new = cj_.copy()
    for y in np.unique(yj):
        sel = np.flatnonzero(yj == y)
        pool = np.flatnonzero(year == y)
        draw = pool[rng.integers(0, len(pool), len(sel))]
        late = dep[draw] > dep[ci[sel]]
        for _ in range(20):
            if not late.any():
                break
            draw[late] = pool[rng.integers(0, len(pool), late.sum())]
            late = dep[draw] > dep[ci[sel]]
        draw[late] = cj_[sel][late]
        new[sel] = draw
    return new


pa = attachment(cj)
pa_null = [attachment(year_null(cj))["a"] for _ in range(5)]
out["preferential_attachment"] = {**pa, "null_values": pa_null, "null_mean": float(np.mean(pa_null))}
print("attachment", out["preferential_attachment"], flush=True)

# 2-3. triadic closure and degree correlations against the swap null
indeg, outdeg = np.bincount(cj, minlength=n), np.bincount(ci, minlength=n)


def structure(cj_):
    g = ig.Graph(n=n, edges=list(zip(ci, cj_)), directed=False).simplify()
    return {"transitivity": g.transitivity_undirected(), "avg_local_clustering": g.transitivity_avglocal_undirected(mode="zero"),
            "corr_in_in": float(np.corrcoef(indeg[ci], indeg[cj_])[0, 1]), "corr_out_in": float(np.corrcoef(outdeg[ci], indeg[cj_])[0, 1])}


obs = structure(cj)
null = [structure(swap_null(ci, cj, yi, yj, dep, rng)) for _ in range(REPS)]
out["structure"] = {k: {"observed": obs[k], "null_mean": float(np.mean([x[k] for x in null])),
                        "null_lo": float(np.quantile([x[k] for x in null], .025)), "null_hi": float(np.quantile([x[k] for x in null], .975)),
                        "p_two_sided": float(min(1, 2 * min((1 + sum(x[k] >= obs[k] for x in null)) / (REPS + 1),
                                                             (1 + sum(x[k] <= obs[k] for x in null)) / (REPS + 1))))}
                    for k in obs}
print("structure", out["structure"], flush=True)

# 4. small world: giant component against an Erdos-Renyi graph with the same nodes and edges
g = ig.Graph(n=n, edges=list(zip(ci, cj)), directed=False).simplify()
giant = g.connected_components().giant()
er = ig.Graph.Erdos_Renyi(n=g.vcount(), m=g.ecount()).connected_components().giant()
out["small_world"] = {"giant_nodes": giant.vcount(), "giant_share": giant.vcount() / n, "mean_degree": 2 * g.ecount() / n,
                      "avg_distance": giant.average_path_length(directed=False), "transitivity": giant.transitivity_undirected(),
                      "er_avg_distance": er.average_path_length(directed=False), "er_transitivity": er.transitivity_undirected(),
                      "er_giant_nodes": er.vcount()}
print("small world", out["small_world"], flush=True)

# 5. bridges: betweenness on the undirected network
bet = np.array(g.betweenness(directed=False))
com = pd.read_csv(P / "communities.csv").set_index("pid").community.reindex(sub.pid).values
k1 = n // 100


def outside(v):
    """Share of the neighbours of v that belong to another community."""
    nb = g.neighbors(v)
    return float(np.mean([com[u] != com[v] for u in nb])) if nb else np.nan


top_b, top_i = np.argsort(-bet)[:k1], np.argsort(-indeg)[:k1]
connected = np.flatnonzero(np.array(g.degree()) > 0)
out["bridges"] = {"top1_betweenness_share_neighbours_outside": float(np.nanmean([outside(v) for v in top_b])),
                  "top1_citations_share_neighbours_outside": float(np.nanmean([outside(v) for v in top_i])),
                  "all_connected_share_neighbours_outside": float(np.nanmean([outside(v) for v in connected])),
                  "overlap_top1_betweenness_citations": len(set(top_b) & set(top_i)) / k1,
                  "spearman_betweenness_citations": float(pd.Series(bet).corr(pd.Series(indeg), method="spearman")),
                  "top10": [{"pid": int(sub.pid.values[v]), "betweenness": float(bet[v]), "citazioni": int(indeg[v]),
                             "quota_vicini_in_altre_comunita": outside(v)} for v in top_b[:10]]}
print("bridges", {k: v for k, v in out["bridges"].items() if k != "top10"}, flush=True)

# 6. robustness: giant component (share of all pronunce) after removing the most cited, or at random
rob = {}
for frac in [0.01, 0.02, 0.05, 0.10, 0.20]:
    kk = int(frac * n)
    targ = g.copy(); targ.delete_vertices(np.argsort(-indeg)[:kk].tolist())
    rand = []
    for _ in range(10):
        h = g.copy(); h.delete_vertices(rng.choice(n, kk, replace=False).tolist())
        rand.append(h.connected_components().giant().vcount() / n)
    rob[str(frac)] = {"targeted": targ.connected_components().giant().vcount() / n, "random_mean": float(np.mean(rand)),
                      "random_lo": float(np.min(rand)), "random_hi": float(np.max(rand))}
out["robustness"] = {"giant_share_before": giant.vcount() / n, "after_removal": rob}
print("robustness", out["robustness"], flush=True)
json.dump(out, open(REPO / "reports/course_measures.json", "w"), indent=1, default=float)
