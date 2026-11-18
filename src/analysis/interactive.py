"""Interactive view of the core of the citation network: the N most cited pronunce and the
citations among them. Self-contained HTML (no external library, data embedded).
Layout: Fruchterman-Reingold (igraph), fixed seed.
Output: reports/rete_interattiva.html
Usage: .venv/bin/python src/analysis/interactive.py
"""
import json
import random
from pathlib import Path

import igraph as ig
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED, N = 20261116, 400
nodes = pd.read_csv(P / "nodes.csv")
edges = pd.read_csv(P / "edges_citations.csv")
judges = pd.read_csv(P / "judges.csv").set_index("judge_id").Nome_Cognome.to_dict()
comm = pd.read_csv(P / "communities.csv").set_index("pid").community.to_dict()
topic = pd.read_csv(P / "topics_pronunce.csv").set_index("pid").topic.to_dict()
tj = json.load(open(REPO / "reports/topics.json"))
top = nodes.nlargest(N, "in_deg").reset_index(drop=True)
idx = {p: i for i, p in enumerate(top.pid)}
e = edges[edges.citing_id.isin(idx) & edges.cited_id.isin(idx)]
g = ig.Graph(n=len(top), edges=[(idx[a], idx[b]) for a, b in zip(e.citing_id, e.cited_id)])
random.seed(SEED)
lay = g.layout_fruchterman_reingold(niter=2000)
xs, ys = zip(*lay.coords)
sx = lambda v, vs: round((v - min(vs)) / (max(vs) - min(vs)) * 1000, 1)
big = top.pid.map(comm).value_counts().index[:9].tolist()


def drafter(s):
    ids = [int(x) for x in str(s).split("|") if x not in ("", "nan", "0")]
    return ", ".join(judges.get(i, "?") for i in ids) or "non indicato"


cs = pd.Series(comm)
ts = pd.Series(topic)
leg = []
for c in big:  # label of a community: words of its most frequent topic and median year (titles exist only from 2015)
    members = cs.index[cs == c]
    t = ts.reindex(members).dropna().astype(int).value_counts().index[0]
    leg.append(f"{', '.join(tj['top_words'][str(t)][:3])}… (anno mediano {int(nodes[nodes.pid.isin(members)].anno.median())})")
leg.append("altri filoni")
data = {"nodes": [{"id": int(r.pid), "l": f"{'sent.' if r.tipo == 'S' else 'ord.'} {r.num}/{r.anno}", "y": int(r.anno), "c": int(r.in_deg),
                   "o": int(r.out_deg), "r": drafter(r.redattore_ids), "proxy": r.redattore_source == "relatore_proxy",
                   "g": big.index(comm[r.pid]) if comm[r.pid] in big else 9,
                   "t": ", ".join(tj["top_words"][str(int(topic[r.pid]))][:5]) if r.pid in topic else "senza massime",
                   "x": sx(xs[i], xs), "yy": sx(ys[i], ys)} for i, r in top.iterrows()],
        "edges": [[idx[a], idx[b]] for a, b in zip(e.citing_id, e.cited_id)], "leg": leg}
html = (Path(__file__).with_name("interactive_template.html")).read_text(encoding="utf-8")
html = html.replace("/*DATA*/", json.dumps(data, ensure_ascii=False)).replace("__N__", str(N)).replace("__E__", f"{len(e):,}".replace(",", "."))
(REPO / "reports/rete_interattiva.html").write_text(html, encoding="utf-8")
print(len(top), "nodes", len(e), "edges; min citations", int(top.in_deg.min()))
