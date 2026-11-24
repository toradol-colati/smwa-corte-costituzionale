"""Co-sitting network: judge A -- judge B, weight = number of pronunce that A and B decided together,
that is, pronunce in whose collegio both sat (data/processed/collegio.csv, built by build_judges.py).
Asked by Umberto on 24/11/2026. Descriptive: no test is run on it, because judges in office in the same
years sit together almost always (.claude/rules/network-analysis.md).

Every pronuncia of the archive is a published decision, so every pronuncia counts. The date of a pronuncia
is the date of decision (the date of deposit when the decision date is missing), as in build_judges.py.
A judge is "active" from the first to the last pronuncia in whose collegio he or she sat: the end dates of
the official list of judges are not reliable (reports/judges_quality.md), and are only checked here.

Outputs
  data/processed/edges_cositting.csv      one row per pair of judges who decided at least one pronuncia together:
                                          judge_a, judge_b (judge_a < judge_b), weight, first and last pronuncia
                                          decided together, n_both_active (pronunce of the archive decided while
                                          both were active), share = weight / n_both_active
  data/processed/judges_cositting.csv     one row per judge with at least one presence: name, first and last
                                          presence, pronunce sat, number of colleagues, strength (sum of weights)
  data/processed/cositting_network.graphml  the same network, for Gephi or networkx
  reports/cositting_network.json          description and checks
Usage: .venv/bin/python src/networks/cositting.py
"""
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"


def main():
    nodes = pd.read_csv(P / "nodes.csv", usecols=["pid", "data_decisione", "data_deposito"],
                        parse_dates=["data_decisione", "data_deposito"])
    nodes["date"] = nodes.data_decisione.fillna(nodes.data_deposito)
    coll = pd.read_csv(P / "collegio.csv").merge(nodes[["pid", "date"]], on="pid")
    judges = pd.read_csv(P / "judges.csv", parse_dates=["data_giuramento", "data_cessazione"]).set_index("judge_id")

    # pairs: every pair of judges sitting in the same collegio, counted once per pronuncia
    weight, first, last = Counter(), {}, {}
    for (pid, date), g in coll.groupby(["pid", "date"]):
        for a, b in itertools.combinations(sorted(set(g.judge_id)), 2):
            weight[(a, b)] += 1
            first[(a, b)] = min(first.get((a, b), date), date)
            last[(a, b)] = max(last.get((a, b), date), date)

    # judges: first and last presence, pronunce sat
    act = coll.groupby("judge_id").agg(first_presence=("date", "min"), last_presence=("date", "max"),
                                       n_pronunce=("pid", "nunique"))
    dates = np.sort(nodes.date.values)

    def n_between(d0, d1):  # pronunce of the archive decided from d0 to d1, both included
        return int(np.searchsorted(dates, np.datetime64(d1), side="right") - np.searchsorted(dates, np.datetime64(d0), side="left"))

    rows = []
    for (a, b), w in weight.items():
        d0 = max(act.first_presence[a], act.first_presence[b])
        d1 = min(act.last_presence[a], act.last_presence[b])
        nb = n_between(d0, d1)
        rows.append(dict(judge_a=a, judge_b=b, name_a=judges.Nome_Cognome[a], name_b=judges.Nome_Cognome[b], weight=w,
                         first_together=first[(a, b)].date(), last_together=last[(a, b)].date(),
                         n_both_active=nb, share=w / nb))
    e = pd.DataFrame(rows).sort_values(["judge_a", "judge_b"]).reset_index(drop=True)
    e.to_csv(P / "edges_cositting.csv", index=False)

    strength = pd.concat([e[["judge_a", "weight"]].rename(columns={"judge_a": "j"}),
                          e[["judge_b", "weight"]].rename(columns={"judge_b": "j"})]).groupby("j").weight
    jn = act.join(judges[["Nome_Cognome", "eletto_da"]]).assign(n_colleagues=strength.size(), strength=strength.sum())
    jn = jn.reset_index()[["judge_id", "Nome_Cognome", "eletto_da", "first_presence", "last_presence", "n_pronunce",
                           "n_colleagues", "strength"]]
    jn["first_presence"] = jn.first_presence.dt.date
    jn["last_presence"] = jn.last_presence.dt.date
    jn.to_csv(P / "judges_cositting.csv", index=False)

    G = nx.Graph()
    for r in jn.itertuples():
        G.add_node(int(r.judge_id), name=r.Nome_Cognome, eletto_da=str(r.eletto_da), first_presence=str(r.first_presence),
                   last_presence=str(r.last_presence), n_pronunce=int(r.n_pronunce))
    for r in e.itertuples():
        G.add_edge(int(r.judge_a), int(r.judge_b), weight=int(r.weight), n_both_active=int(r.n_both_active), share=float(r.share))
    nx.write_graphml(G, P / "cositting_network.graphml")

    # pairs active in the same years (their periods of presence overlap), with or without a pronuncia together
    ids = list(act.index)
    overlap = [(a, b) for a, b in itertools.combinations(sorted(ids), 2)
               if max(act.first_presence[a], act.first_presence[b]) <= min(act.last_presence[a], act.last_presence[b])]
    never = [(a, b) for a, b in overlap if (a, b) not in weight]
    # check of the official list: presences after the end of the mandate written in the list
    chk = act.join(judges[["Nome_Cognome", "data_giuramento", "data_cessazione", "end_source"]])
    chk["days_after_end"] = (chk.last_presence - chk.data_cessazione).dt.days
    after = chk[chk.days_after_end > 0].sort_values("days_after_end", ascending=False)
    # total weight must equal the number of pairs inside each collegio, summed over the pronunce
    size = coll.groupby("pid").judge_id.nunique()
    q = lambda s, x: float(s.quantile(x))
    sig = e[e.n_both_active >= 100]
    out = dict(
        judges=int(len(jn)), edges=int(len(e)), possible_pairs=int(len(ids) * (len(ids) - 1) // 2),
        density=float(len(e) / (len(ids) * (len(ids) - 1) / 2)),
        pronunce_with_collegio=int(size.size), total_weight=int(e.weight.sum()),
        total_weight_check=int((size * (size - 1) // 2).sum()),
        pairs_active_same_years=len(overlap), pairs_active_same_years_together=len(overlap) - len(never),
        pairs_active_same_years_never_together=[dict(a=judges.Nome_Cognome[a], b=judges.Nome_Cognome[b],
                                                     n_both_active=n_between(max(act.first_presence[a], act.first_presence[b]),
                                                                             min(act.last_presence[a], act.last_presence[b])))
                                                for a, b in never],
        weight=dict(min=int(e.weight.min()), q25=q(e.weight, .25), median=q(e.weight, .5), q75=q(e.weight, .75), max=int(e.weight.max())),
        share=dict(min=float(e.share.min()), q25=q(e.share, .25), median=q(e.share, .5), q75=q(e.share, .75), max=float(e.share.max())),
        share_pairs_100=dict(pairs=int(len(sig)), median=q(sig.share, .5), min=float(sig.share.min())),
        colleagues=dict(min=int(jn.n_colleagues.min()), median=float(jn.n_colleagues.median()), max=int(jn.n_colleagues.max())),
        top10_weight=[dict(a=r.name_a, b=r.name_b, weight=int(r.weight), n_both_active=int(r.n_both_active), share=float(r.share))
                      for r in e.nlargest(10, "weight").itertuples()],
        bottom10_share_pairs_100=[dict(a=r.name_a, b=r.name_b, weight=int(r.weight), n_both_active=int(r.n_both_active), share=float(r.share))
                                  for r in sig.nsmallest(10, "share").itertuples()],
        registry_presence_after_end=[dict(judge=r.Nome_Cognome, giuramento=str(r.data_giuramento.date()),
                                          end_in_list=str(r.data_cessazione.date()), end_source=r.end_source,
                                          last_presence=str(r.last_presence.date()), days_after_end=int(r.days_after_end))
                                     for r in after.itertuples()],
        note_incomplete_collegio="the 257 pronunce of data/interim/collegio_errors.csv have a collegio not fully recognised: "
                                 "their missing judges are missing from the weights",
    )
    json.dump(out, open(REPO / "reports/cositting_network.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if not isinstance(v, list)}, indent=1, ensure_ascii=False))
    print("never together:", out["pairs_active_same_years_never_together"])
    print("after end:", [(r["judge"], r["days_after_end"]) for r in out["registry_presence_after_end"]])


if __name__ == "__main__":
    main()
