"""Secondary and descriptive analyses.
1. Communities (Leiden, undirected citation network) validated with the topics.
2. Outcome (from the SPARQL endpoint, 2005-): are pronunce declaring a law
   unconstitutional cited more, in a fixed 10-year window?
3. Wikipedia (descriptive validation of D1): share of pronunce linked from
   it.wikipedia among the top 1% by authority and by citations, cohort percentiles.
4. Self-citation and collegial-memory raw rates for the report.
Output: reports/extras.json
Usage: .venv/bin/python src/analysis/extras.py
"""
import json
import random
from pathlib import Path
import igraph as ig
import leidenalg
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.metrics import normalized_mutual_info_score

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED = 20261116
rng = np.random.default_rng(SEED)
nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_deposito"])
edges = pd.read_csv(P / "edges_citations.csv")
out = {}

# 1. communities
idx = pd.Series(range(len(nodes)), index=nodes.pid.values)
g = ig.Graph(n=len(nodes), edges=list(zip(idx.loc[edges.citing_id], idx.loc[edges.cited_id])), directed=False).simplify()
part = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition, seed=SEED)
memb = np.array(part.membership)
sizes = np.bincount(memb)
tp = pd.read_csv(P / "topics_pronunce.csv").set_index("pid").topic
big = np.isin(memb, np.flatnonzero(sizes >= 50))
has = nodes.pid.isin(tp.index).values & big
t = tp.loc[nodes.pid[has]].values
nmi = normalized_mutual_info_score(memb[has], t)
null = [normalized_mutual_info_score(memb[has], rng.permutation(t)) for _ in range(200)]
# null that keeps the degree sequence: modularity of a degree-preserving rewiring
rew = g.copy(); rew.rewire(n=10 * g.ecount())
part0 = leidenalg.find_partition(rew, leidenalg.ModularityVertexPartition, seed=SEED)
top = []
tj = json.load(open(REPO / "reports/topics.json"))
for c in np.argsort(-sizes)[:12]:
    m = (memb == c) & nodes.pid.isin(tp.index).values
    vc = pd.Series(tp.loc[nodes.pid[m]].values).value_counts(normalize=True)
    top.append({"community": int(c), "size": int(sizes[c]), "median_year": int(nodes.anno[memb == c].median()),
                "top_topic": int(vc.index[0]), "top_topic_share": float(vc.iloc[0]),
                "top_topic_words": tj["top_words"][str(int(vc.index[0]))][:6]})
out["communities"] = {"n_communities": int(len(sizes)), "communities_50plus": int((sizes >= 50).sum()),
                      "share_nodes_in_50plus": float(big.mean()), "modularity": float(part.modularity),
                      "modularity_rewired": float(part0.modularity), "nmi_topic": float(nmi), "nmi_null_mean": float(np.mean(null)),
                      "nmi_null_hi": float(np.quantile(null, .975)), "largest": top}
pd.DataFrame({"pid": nodes.pid, "community": memb}).to_csv(P / "communities.csv", index=False)
# second method, as planned: Infomap (igraph implementation), compared with Leiden
random.seed(SEED)
im = np.array(g.community_infomap(trials=5).membership)
im_sizes = np.bincount(im)
big_i = np.isin(im, np.flatnonzero(im_sizes >= 50))
has_i = nodes.pid.isin(tp.index).values & big_i
out["communities"]["infomap"] = {"n_communities": int(len(im_sizes)), "communities_50plus": int((im_sizes >= 50).sum()),
                                 "share_nodes_in_50plus": float(big_i.mean()), "modularity": float(g.modularity(im.tolist())),
                                 "nmi_with_leiden": float(normalized_mutual_info_score(memb, im)),
                                 "nmi_with_leiden_connected_only": float(normalized_mutual_info_score(memb[np.array(g.degree()) > 0], im[np.array(g.degree()) > 0])),
                                 "nmi_topic": float(normalized_mutual_info_score(im[has_i], tp.loc[nodes.pid[has_i]].values))}

# 2. outcome and citations in a fixed 10-year window (cohorts 2005-2015)
es = pd.read_csv(P / "esiti.csv").groupby("pid").illegittimita.max()
dep = nodes.set_index("pid").data_deposito
e2 = edges.assign(d1=edges.citing_id.map(dep), d0=edges.cited_id.map(dep))
win = e2[(e2.d1 - e2.d0).dt.days <= 3652].groupby("cited_id").size()
coh = nodes[nodes.anno.between(2006, 2015) & nodes.pid.isin(es.index)].copy()
coh["ill"] = coh.pid.map(es).values
coh["cit10"] = coh.pid.map(win).fillna(0)
res = {}
for lab, x in [("tutte", coh), ("sentenze", coh[coh.tipo == "S"])]:
    a, b = x[x.ill].cit10, x[~x.ill].cit10
    boot = [x.sample(len(x), replace=True, random_state=int(s)).pipe(lambda d: d[d.ill].cit10.mean() / d[~d.ill].cit10.mean())
            for s in rng.integers(0, 1e9, 500)]
    res[lab] = {"n_ill": int(len(a)), "n_altre": int(len(b)), "media_ill": float(a.mean()), "media_altre": float(b.mean()),
                "mediana_ill": float(a.median()), "mediana_altre": float(b.median()), "rapporto_medie": float(a.mean() / b.mean()),
                "rapporto_lo": float(np.quantile(boot, .025)), "rapporto_hi": float(np.quantile(boot, .975)),
                "mannwhitney_p": float(mannwhitneyu(a, b).pvalue)}
out["esito"] = res
allp = pd.read_csv(P / "esiti.csv")
out["esito"]["distribuzione"] = allp.esito.value_counts().head(8).to_dict()

# 3. Wikipedia
w = pd.read_csv(P / "wikipedia_links.csv")
wp = set(w.pid)
last = pd.read_pickle(REPO / "data/interim/d1_panel_2026.pkl") if (REPO / "data/interim/d1_panel_2026.pkl").exists() else pd.read_pickle(REPO / "data/interim/d1_panel_2025.pkl")
last["wiki"] = last.pid.isin(wp)
last["cit_pct"] = last.groupby(last.pid // 10000).cum_cit.rank(pct=True) * 100
k = len(last) // 100
out["wikipedia"] = {"linked_pronunce": int(last.wiki.sum()), "base_rate": float(last.wiki.mean()),
                    "share_in_top1_authority_pct": float(last.nlargest(k, "auth_pct").wiki.mean()),
                    "share_in_top1_citations_pct": float(last.nlargest(k, "cit_pct").wiki.mean()),
                    "share_in_top1_raw_citations": float(last.nlargest(k, "cum_cit").wiki.mean()),
                    "median_auth_pct_linked": float(last[last.wiki].auth_pct.median()),
                    "median_cit_pct_linked": float(last[last.wiki].cit_pct.median()),
                    "most_linked": w.pid.value_counts().head(8).to_dict()}

# 4. raw numbers for the report
jj = pd.read_csv(P / "edges_judges.csv")
out["judge_network"] = {"judges": int(len(set(jj.a) | set(jj.b))), "pairs": int(len(jj)), "weight": int(jj.weight.sum()),
                        "self_share": float(jj[jj.a == jj.b].weight.sum() / jj.weight.sum())}
json.dump(out, open(REPO / "reports/extras.json", "w"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(out, indent=1, ensure_ascii=False, default=str)[:3500])
