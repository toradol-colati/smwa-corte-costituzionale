"""Build the node table and the three layers, and write the basic description of
the citation network. Outputs:
  data/processed/nodes.csv         one row per pronuncia with all attributes
  data/processed/edges_redazione.csv, (collegio.csv already built)
  data/processed/edges_judges.csv  judge A -> judge B, weight = citations from
                                   pronunce drafted by A to pronunce drafted by B
  reports/network_basic.json / .md
Usage: .venv/bin/python src/networks/build.py
"""
import glob, json
from pathlib import Path
import networkx as nx
import numpy as np
import pandas as pd
from lxml import etree
REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"

def giudizio():
    rows = []
    for path in glob.glob(str(REPO / "data/raw/massime/*/*.xml")):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            h = p.find("pronuncia_testata")
            rows.append((int(h.findtext("anno_pronuncia")) * 10000 + int(h.findtext("numero_pronuncia")),
                         (h.findtext("tipologia_giudizio") or "").strip()))
    g = pd.DataFrame(rows, columns=["pid", "giudizio_raw"])
    def short(s):
        s = s.upper()
        if "+" in s: return "misto"
        if "INCIDENTALE" in s: return "incidentale"
        if "PRINCIPALE" in s: return "principale"
        if "ENTI" in s: return "conflitto enti"
        if "POTERI" in s: return "conflitto poteri"
        if "REFERENDUM" in s: return "referendum"
        if "CORREZIONE" in s: return "correzione"
        return "altro"
    g["giudizio"] = g.giudizio_raw.map(short)
    return g

def main():
    meta = pd.read_csv(P / "pronunce.csv", parse_dates=["data_decisione", "data_deposito"])
    pj = pd.read_csv(P / "pronunce_judges.csv")
    e = pd.read_csv(P / "edges_citations.csv")
    nodes = meta.merge(pj, on="pid").merge(giudizio()[["pid", "giudizio"]], on="pid", how="left")
    nodes["in_deg"] = nodes.pid.map(e.groupby("cited_id").size()).fillna(0).astype(int)
    nodes["out_deg"] = nodes.pid.map(e.groupby("citing_id").size()).fillna(0).astype(int)
    nodes.to_csv(P / "nodes.csv", index=False)
    red = nodes[["pid", "redattore_ids", "redattore_source"]].assign(judge_id=nodes.redattore_ids.fillna("").str.split("|")).explode("judge_id")
    red = red[red.judge_id.fillna("").ne("") & red.judge_id.ne("0")].astype({"judge_id": int})[["judge_id", "pid", "redattore_source"]]
    red.to_csv(P / "edges_redazione.csv", index=False)
    r1 = red.rename(columns={"judge_id": "a", "pid": "citing_id"})[["a", "citing_id"]]
    r2 = red.rename(columns={"judge_id": "b", "pid": "cited_id"})[["b", "cited_id"]]
    jj = e.merge(r1, on="citing_id").merge(r2, on="cited_id").groupby(["a", "b"]).size().rename("weight").reset_index()
    jj.to_csv(P / "edges_judges.csv", index=False)

    G = nx.DiGraph(); G.add_nodes_from(nodes.pid); G.add_edges_from(zip(e.citing_id, e.cited_id))
    n, m = G.number_of_nodes(), G.number_of_edges()
    dep = nodes.sort_values(["data_deposito", "pid"]).data_deposito.values
    # possible backward pairs: for each node, number of nodes deposited strictly before
    earlier = np.searchsorted(dep, dep, side="left")
    wcc = sorted((len(c) for c in nx.weakly_connected_components(G)), reverse=True)
    iso = int(((nodes.in_deg == 0) & (nodes.out_deg == 0)).sum())
    age = (e.merge(nodes[["pid", "data_deposito"]].rename(columns={"pid": "citing_id", "data_deposito": "d1"}), on="citing_id")
            .merge(nodes[["pid", "data_deposito"]].rename(columns={"pid": "cited_id", "data_deposito": "d0"}), on="cited_id"))
    age_y = (age.d1 - age.d0).dt.days / 365.25
    lcc = G.subgraph(max(nx.weakly_connected_components(G), key=len))
    stats = dict(nodes=n, edges=m, is_dag=nx.is_directed_acyclic_graph(G), isolates=iso,
                 density_backward=m / int(earlier.sum()), wcc_count=len(wcc), wcc_largest=wcc[0], wcc_largest_share=wcc[0] / n,
                 in_deg_mean=float(nodes.in_deg.mean()), in_deg_median=float(nodes.in_deg.median()), in_deg_max=int(nodes.in_deg.max()),
                 out_deg_mean=float(nodes.out_deg.mean()), out_deg_median=float(nodes.out_deg.median()), out_deg_max=int(nodes.out_deg.max()),
                 share_never_cited=float((nodes.in_deg == 0).mean()), share_citing_nothing=float((nodes.out_deg == 0).mean()),
                 top1pct_share_of_citations=float(nodes.in_deg.sort_values(ascending=False).head(n // 100).sum() / m),
                 gini_in=float((lambda x: (2 * np.arange(1, len(x) + 1) - len(x) - 1).dot(x) / (len(x) * x.sum()))(np.sort(nodes.in_deg.values.astype(float)))),
                 citation_age_median=float(age_y.median()), citation_age_q25=float(age_y.quantile(.25)), citation_age_q75=float(age_y.quantile(.75)),
                 share_age_under5=float((age_y < 5).mean()), share_age_over20=float((age_y > 20).mean()),
                 dag_longest_path=int(nx.dag_longest_path_length(G)),
                 degree_assortativity_in_in=float(nx.degree_pearson_correlation_coefficient(G, x="in", y="in")),
                 judge_edges=len(jj), judge_self_weight=int(jj[jj.a == jj.b].weight.sum()), judge_total_weight=int(jj.weight.sum()),
                 by_type={t: dict(n=int(len(x)), in_mean=float(x.in_deg.mean()), out_mean=float(x.out_deg.mean())) for t, x in nodes.groupby("tipo")},
                 by_decade_out={int(d): float(x.out_deg.mean()) for d, x in nodes.groupby(nodes.anno // 10 * 10)},
                 by_giudizio={k: int(v) for k, v in nodes.giudizio.value_counts().items()},
                 top20_cited=[dict(pid=int(r.pid), tipo=r.tipo, in_deg=int(r.in_deg)) for r in nodes.nlargest(20, "in_deg").itertuples()])
    json.dump(stats, open(REPO / "reports/network_basic.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in stats.items() if not isinstance(v, (dict, list))}, indent=1))
    print(stats["top20_cited"][:10]); print(stats["by_decade_out"])

if __name__ == "__main__":
    main()
