"""D2 - do the pronunce drafted by a judge receive more citations than expected
given the judge's opportunities? Does it last after the mandate?
D4 - do judges cite more the pronunce drafted by judges with the same
appointing body or the same professional background? (only if power >= 0.80)

Null for D2 (docs/decisions.md): every citation keeps its citing pronuncia and
the deposit year of its target; the target is redrawn among the pronunce of that
year (variant: of that year and of the same type). Self-citations (citing and
cited drafted by the same judge) are excluded from observed and expected.

Outputs: reports/d2_results.json, reports/d4_results.json, data/processed/judges_attributes.csv
Usage: .venv/bin/python src/analysis/d2_d4_giudici.py
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED = 20261116
REPS = int(os.environ.get("REPS", 1000))
MIN_PRONUNCE = 30
POST_WINDOW = 10


def holm(p):
    p = np.asarray(p)
    order = np.argsort(p)
    adj = np.empty(len(p))
    run = 0
    for rank, i in enumerate(order):
        run = max(run, (len(p) - rank) * p[i])
        adj[i] = min(1, run)
    return adj


def provenance(bio: str, eletto: str) -> str:
    """Automatic coding of the professional background from the biographical note."""
    head = (bio or "")[:400].lower()
    if re.search(r"professor|docente|ordinario di|libero docente|rettore", head):
        return "professore"
    if re.search(r"president[e] di sezione|consigliere|procuratore|avvocato generale|magistrat|primo presidente|presidente (?:della|del) (?:corte|consiglio)|pretore|giudice", head):
        return "magistrato"
    if re.search(r"avvocato|avv\.", head):
        return "avvocato"
    if "Corte" in eletto or "Consiglio" in eletto:
        return "magistrato"
    return "non codificato"


def main():
    rng = np.random.default_rng(SEED)
    nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_decisione", "data_deposito"]).sort_values(["data_deposito", "pid"]).reset_index(drop=True)
    judges = pd.read_csv(P / "judges.csv", parse_dates=["data_giuramento"])
    edges = pd.read_csv(P / "edges_citations.csv")
    coll = pd.read_csv(P / "collegio.csv").merge(nodes[["pid", "data_decisione"]], on="pid")
    app = coll.groupby("judge_id").data_decisione.agg(first="min", last="max")
    judges = judges.merge(app, left_on="judge_id", right_index=True, how="left")
    judges["organo"] = judges.eletto_da.map(lambda s: "magistrature" if ("Corte" in s or "Consiglio" in s) else s)
    judges["provenienza"] = [provenance(b, e) for b, e in zip(judges.Nota_biografica.fillna(""), judges.eletto_da)]
    judges[["judge_id", "Nome_Cognome", "eletto_da", "organo", "provenienza", "data_giuramento", "first", "last"]].to_csv(P / "judges_attributes.csv", index=False)

    idx = pd.Series(nodes.index.values, index=nodes.pid.values)
    n = len(nodes)
    year = nodes.anno.values
    tipo = (nodes.tipo == "S").values.astype(int)
    dep = nodes.data_deposito.values.astype("datetime64[D]").astype(int)
    # single drafter per pronuncia for attribution; pronunce with several drafters count for each (weight 1)
    red_lists = [[int(x) for x in str(s).split("|") if x not in ("", "nan", "0")] for s in nodes.redattore_ids]
    J = int(judges.judge_id.max()) + 1
    D = np.zeros((n, J), bool)
    for i, l in enumerate(red_lists):
        D[i, l] = True
    ci, cj = idx.loc[edges.citing_id].values, idx.loc[edges.cited_id].values
    self_cit = (D[ci] & D[cj]).any(1)
    ci, cj = ci[~self_cit], cj[~self_cit]
    n_drafted = D.sum(0)
    obs = D[cj].sum(0).astype(float)
    last_y = np.full(J, 9999.0)
    for r in judges.itertuples():
        if pd.notna(r.last):
            last_y[r.judge_id] = r.last.year + r.last.dayofyear / 366
    cit_time = 1970 + dep[ci] / 365.25
    post = D[cj] & ((cit_time[:, None] > last_y[None, :]) & (cit_time[:, None] <= last_y[None, :] + POST_WINDOW))
    during = D[cj] & (cit_time[:, None] <= last_y[None, :])
    obs_post, obs_during = post.sum(0).astype(float), during.sum(0).astype(float)

    def simulate(by_type: bool):
        key = year[cj] * 2 + (tipo[cj] if by_type else 0)
        node_key = year * 2 + (tipo if by_type else 0)
        pools = {k: np.flatnonzero(node_key == k) for k in np.unique(key)}
        order = np.argsort(key, kind="stable")
        uniq, starts = np.unique(key[order], return_index=True)
        ends = np.r_[starts[1:], len(key)]
        sims = np.zeros((REPS, J)); sims_post = np.zeros((REPS, J)); sims_during = np.zeros((REPS, J))
        for rep in range(REPS):
            new = np.empty_like(cj)
            for k, a, b in zip(uniq, starts, ends):
                pool, sel = pools[k], order[a:b]
                draw = pool[rng.integers(0, len(pool), b - a)]
                bad = (dep[draw] > dep[ci[sel]]) | (D[ci[sel]] & D[draw]).any(1)
                for _ in range(10):
                    if not bad.any():
                        break
                    draw[bad] = pool[rng.integers(0, len(pool), bad.sum())]
                    bad = (dep[draw] > dep[ci[sel]]) | (D[ci[sel]] & D[draw]).any(1)
                draw[bad] = cj[sel][bad]
                new[sel] = draw
            Dn = D[new]
            sims[rep] = Dn.sum(0)
            sims_post[rep] = (Dn & ((cit_time[:, None] > last_y[None, :]) & (cit_time[:, None] <= last_y[None, :] + POST_WINDOW))).sum(0)
            sims_during[rep] = (Dn & (cit_time[:, None] <= last_y[None, :])).sum(0)
        return sims, sims_post, sims_during

    out = {"reps": REPS, "self_citations_excluded": int(self_cit.sum()), "citations_used": int(len(ci))}
    for label, by_type in [("age_only", False), ("age_and_type", True)]:
        sims, sims_post, sims_during = simulate(by_type)
        exp = sims.mean(0)
        rows = []
        for r in judges.itertuples():
            j = r.judge_id
            if n_drafted[j] < MIN_PRONUNCE or exp[j] == 0:
                continue
            ratio_sims = sims[:, j] / exp[j]
            # p-value from the z-score against the null mean and standard deviation: with 1,000
            # repetitions the empirical p-value cannot go below 0.002, and Holm's correction over
            # more than 100 judges would then never reject by construction.
            from scipy.stats import norm
            z = (obs[j] - exp[j]) / sims[:, j].std(ddof=1)
            p = 2 * norm.sf(abs(z))
            # interval of the observed/expected ratio: the null spread, recentred on the observed ratio
            lo, hi = obs[j] / np.quantile(sims[:, j], .975), obs[j] / max(np.quantile(sims[:, j], .025), 1e-9)
            row = dict(judge_id=j, nome=r.Nome_Cognome, pronunce=int(n_drafted[j]), osservate=int(obs[j]), attese=float(exp[j]),
                       rapporto=float(obs[j] / exp[j]), lo=float(lo), hi=float(hi), z=float(z), p=float(min(1, p)),
                       giuramento=str(r.data_giuramento.date()), organo=r.organo, provenienza=r.provenienza)
            if pd.notna(r.last) and r.last.year <= 2015 and sims_post[:, j].mean() > 0 and sims_during[:, j].mean() > 0:
                row.update(rapporto_post=float(obs_post[j] / sims_post[:, j].mean()), osservate_post=int(obs_post[j]),
                           rapporto_durante=float(obs_during[j] / sims_during[:, j].mean()))
            rows.append(row)
        t = pd.DataFrame(rows)
        t["p_holm"] = holm(t.p.values)
        # heterogeneity: variance of log ratios vs the null variance of simulated ratios
        tested = t.judge_id.values
        obs_var = float(np.var(np.log(t.rapporto)))
        null_var = [float(np.var(np.log(np.maximum(sims[s, tested], 0.5) / exp[tested]))) for s in range(REPS)]
        res = {"judges_tested": int(len(t)), "sig_holm_above": int(((t.p_holm < .05) & (t.rapporto > 1)).sum()),
               "sig_holm_below": int(((t.p_holm < .05) & (t.rapporto < 1)).sum()),
               "ratio_quantiles": {q: float(t.rapporto.quantile(q)) for q in [.05, .25, .5, .75, .95]},
               "var_log_ratio": obs_var, "var_log_ratio_null_mean": float(np.mean(null_var)), "var_log_ratio_null_hi": float(np.quantile(null_var, .975)),
               "table": t.sort_values("rapporto", ascending=False).to_dict("records")}
        pm = t.dropna(subset=["rapporto_post"]) if "rapporto_post" in t else t.iloc[:0]
        if len(pm):
            from scipy.stats import spearmanr, wilcoxon
            brng = np.random.default_rng(SEED + 1)  # separate stream: does not alter the null simulations
            bs = [spearmanr(*pm.iloc[brng.integers(0, len(pm), len(pm))][["rapporto_durante", "rapporto_post"]].values.T)[0] for _ in range(2000)]
            res["post_mandate"] = {"judges": int(len(pm)), "spearman_during_post": float(spearmanr(pm.rapporto_durante, pm.rapporto_post)[0]),
                                   "spearman_lo": float(np.quantile(bs, .025)), "spearman_hi": float(np.quantile(bs, .975)),
                                   "median_ratio_during": float(pm.rapporto_durante.median()), "median_ratio_post": float(pm.rapporto_post.median()),
                                   "wilcoxon_p": float(wilcoxon(np.log(pm.rapporto_post.clip(lower=.01)), np.log(pm.rapporto_durante.clip(lower=.01))).pvalue)}
        out[label] = res
        print(label, {k: v for k, v in res.items() if k != "table"}, flush=True)
        print(t.sort_values("rapporto", ascending=False)[["nome", "pronunce", "osservate", "attese", "rapporto", "p_holm"]].head(8).to_string(), flush=True)
    json.dump(out, open(REPO / "reports/d2_results.json", "w"), indent=1, ensure_ascii=False)

    # ---------------- D4
    jj = pd.read_csv(P / "edges_judges.csv")
    jj = jj[jj.a != jj.b]
    att = judges.set_index("judge_id")
    d4 = {}
    for attr in ["organo", "provenienza"]:
        lab = att[attr].to_dict()
        ok = jj[jj.a.map(lab).ne("non codificato") & jj.b.map(lab).ne("non codificato")]
        a, b, w = ok.a.values, ok.b.values, ok.weight.values.astype(float)
        ids = np.unique(np.r_[a, b])
        # permutation blocks: judges sworn in within the same decade
        block = {j: att.data_giuramento[j].year // 10 for j in ids}

        def stat(labels, weights=w):
            same = np.fromiter((labels[x] == labels[y] for x, y in zip(a, b)), bool, len(a))
            return float(weights[same].sum() / weights.sum())

        def permuted():
            new = {}
            for blk in set(block.values()):
                members = [j for j in ids if block[j] == blk]
                vals = [lab[j] for j in members]
                for j, v in zip(members, rng.permutation(vals)):
                    new[j] = v
            return new

        observed = stat(lab)
        null = np.array([stat(permuted()) for _ in range(REPS)])
        p = float((np.sum(null >= observed) + 1) / (REPS + 1))
        # power: inject a 20% excess of same-group citations on permuted labels and test again
        hits = 0
        n_pow, n_inner = 200, 200
        for _ in range(n_pow):
            l0 = permuted()
            same = np.fromiter((l0[x] == l0[y] for x, y in zip(a, b)), bool, len(a))
            w1 = rng.poisson(w * np.where(same, 1.2, 1.0)).astype(float)
            s1 = float(w1[same].sum() / w1.sum())
            inner = []
            for _ in range(n_inner):
                l1 = {}
                for blk in set(block.values()):
                    members = [j for j in ids if block[j] == blk]
                    for j, v in zip(members, rng.permutation([l0[j] for j in members])):
                        l1[j] = v
                sm_ = np.fromiter((l1[x] == l1[y] for x, y in zip(a, b)), bool, len(a))
                inner.append(w1[sm_].sum() / w1.sum())
            hits += (np.sum(np.array(inner) >= s1) + 1) / (n_inner + 1) < 0.05
        d4[attr] = {"groups": pd.Series({j: lab[j] for j in ids}).value_counts().to_dict(), "judges": int(len(ids)),
                    "citations": int(w.sum()), "same_group_share": observed, "null_mean": float(null.mean()),
                    "null_lo": float(np.quantile(null, .025)), "null_hi": float(np.quantile(null, .975)), "p": p,
                    "ratio_to_null": observed / float(null.mean()), "power_for_20pct": hits / n_pow, "run": bool(hits / n_pow >= 0.8)}
        print(attr, d4[attr], flush=True)
    for attr, ph in zip(d4, holm([d4[k]["p"] for k in d4])):
        d4[attr]["p_holm"] = float(ph)
        d4[attr]["excess_over_null"] = d4[attr]["ratio_to_null"] - 1
        d4[attr]["reaches_minimum_effect_20pct"] = bool(d4[attr]["ratio_to_null"] >= 1.2)
    json.dump(d4, open(REPO / "reports/d4_results.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
