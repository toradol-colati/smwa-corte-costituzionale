"""D2 - do the pronunce drafted by a judge receive more citations than expected
given the judge's opportunities? Does it last after the mandate?
D4 - do judges cite more the pronunce drafted by judges with the same
appointing body or the same professional background? (only if power >= 0.80)

Expected value for D2 (docs/decisions.md, .claude/rules/network-analysis.md): every citation keeps
its citing pronuncia and the deposit year of its target; the target is drawn among the pronunce of
that year (variant: of that year and of the same type), i.e. in proportion to the observed age curve.

Inference for D2 (changed after the check of 17/11/2026, declared in docs/decisions.md): drafter
sets are permuted among pronunce of the same stratum (year; variants: year and type; year, type and
topic; only pronunce from 287/1986), and every pronuncia keeps the citations it actually received.
The pre-registered null (targets redrawn at random) gives the same expected value but ignores how
differently pronunce are cited, so it overstates how many judges differ from 1: it is still
computed and stored under "nullo_preregistrato", but not interpreted.
Self-citations (citing and cited pronuncia sharing a drafter) are excluded from observed and
expected values; under permutation every pronuncia keeps only the citations it received from pronunce
of other drafters (observed drafters), whoever is assigned to it.

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
WINDOW_YEARS = 10  # citations received within 10 years of the deposit (docs/decisions.md, 16/11/2026)
PERM = int(os.environ.get("PERM", 10000))
SWITCH = 19860287  # first pronuncia with the redattore recorded


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
    ci_all, cj_all = idx.loc[edges.citing_id].values, idx.loc[edges.cited_id].values
    # main ratio: citations received within WINDOW_YEARS of the deposit of the cited pronuncia
    # (docs/decisions.md, 16/11/2026); None = all citations
    in_main = np.ones(len(ci_all), bool) if WINDOW_YEARS is None else (dep[ci_all] - dep[cj_all]) <= WINDOW_YEARS * 365.25
    self_all = (D[ci_all] & D[cj_all]).any(1)
    n_drafted = D.sum(0)
    last_y = np.full(J, 9999.0)
    for r in judges.itertuples():
        if pd.notna(r.last):
            last_y[r.judge_id] = r.last.year + r.last.dayofyear / 366
    t_all = 1970 + dep[ci_all] / 365.25
    tested = np.array([r.judge_id for r in judges.itertuples() if n_drafted[r.judge_id] >= MIN_PRONUNCE])
    out = {"min_pronunce": MIN_PRONUNCE, "window_years": WINDOW_YEARS, "permutations": PERM, "reps_preregistered": REPS,
           "self_citations_excluded": int((self_all & in_main).sum()), "citations_used": int((~self_all & in_main).sum()),
           "self_citation_rule": "a citation is excluded when the citing pronuncia shares a drafter with the cited one (observed "
                                 "drafters); under permutation every pronuncia keeps only the citations it received from pronunce "
                                 "of other drafters, whoever is assigned to it"}

    # ---- label-permutation null (interpreted). Drafter sets are shuffled among pronunce of the
    # same stratum; every pronuncia keeps the citations it actually received. The expected value
    # is the same as in the pre-registered rule (age curve), the variability is the right one.
    maxd = max(1, max(len(l) for l in red_lists))
    L = np.full((n, maxd), -1, int)
    for i, l in enumerate(red_lists):
        L[i, :len(l)] = l

    def counts(perm, ci_, cj_, main_, t_, own_):
        """Citations received by every judge under the drafter assignment perm (pronuncia i takes
        the drafters of pronuncia perm[i]): main ratio, during and after the mandate. own_ marks the
        self-citations under the observed drafters: they are excluded whoever gets the pronuncia, so
        every pronuncia carries only the citations it received from pronunce of other drafters."""
        Lc = L[perm[cj_]]
        shared = own_
        c_main, c_dur, c_post = np.zeros(J), np.zeros(J), np.zeros(J)
        for k in range(maxd):
            jj = Lc[:, k]
            m = (jj >= 0) & ~shared
            jm, tm, lm = jj[m], t_[m], last_y[jj[m]]
            c_main += np.bincount(jm[main_[m]], minlength=J)
            c_dur += np.bincount(jm[tm <= lm], minlength=J)
            c_post += np.bincount(jm[(tm > lm) & (tm <= lm + POST_WINDOW)], minlength=J)
        return c_main, c_dur, c_post

    def perm_null(strata, ci_, cj_, main_, t_, own_, js, seed):
        prng = np.random.default_rng(seed)
        base = np.argsort(strata, kind="stable")
        sims = np.zeros((3, PERM, len(js)), np.float32)
        for r_ in range(PERM):
            perm = np.empty(n, int)
            perm[base] = np.lexsort((prng.random(n), strata))
            for a, c in enumerate(counts(perm, ci_, cj_, main_, t_, own_)):
                sims[a, r_] = c[js]
        return sims

    from scipy.stats import norm, spearmanr, wilcoxon
    topic = pd.read_csv(P / "topics_pronunce.csv").set_index("pid").topic.reindex(nodes.pid).fillna(-1).astype(int).values
    in87 = nodes.pid.values >= SWITCH
    m87 = in87[ci_all] & in87[cj_all]
    variants = {
        "permutazione_anno": (year, np.ones(len(ci_all), bool), tested),
        "permutazione_anno_tipo": (year * 2 + tipo, np.ones(len(ci_all), bool), tested),
        "permutazione_anno_tipo_materia": ((year * 2 + tipo) * 100 + topic + 1, np.ones(len(ci_all), bool), tested),
        "permutazione_anno_dal_1987": (np.where(in87, year, -1), m87,
                                       np.array([j for j in tested if D[in87, j].sum() >= MIN_PRONUNCE])),
    }
    jinfo = judges.set_index("judge_id")
    for vi, (vname, (strata, cmask, js)) in enumerate(variants.items()):
        ci_, cj_, main_, t_, own_ = ci_all[cmask], cj_all[cmask], in_main[cmask], t_all[cmask], self_all[cmask]
        o_main, o_dur, o_post = (c[js] for c in counts(np.arange(n), ci_, cj_, main_, t_, own_))
        if vname == "permutazione_anno":  # the identity assignment reproduces the observed counts
            ref = D[cj_all[in_main & ~self_all]].sum(0)[js]
            assert np.array_equal(o_main, ref), "observed counts do not match"
        sims = perm_null(strata, ci_, cj_, main_, t_, own_, js, SEED + 100 + vi)
        exp, exp_dur, exp_post = sims[0].mean(0), sims[1].mean(0), sims[2].mean(0)
        lr_obs = np.log(np.maximum(o_main, .5) / exp)
        lr_sim = np.log(np.maximum(sims[0], .5) / exp)
        p = (1 + (np.abs(lr_sim) >= np.abs(lr_obs) - 1e-12).sum(0)) / (PERM + 1)
        z = (o_main - exp) / sims[0].std(0, ddof=1)
        # 95% interval of the ratio: bootstrap of the judge's own pronunce (their citations as received)
        valid = ~self_all[cmask] & main_
        cnt = np.bincount(cj_[valid], minlength=n).astype(float)
        brng = np.random.default_rng(SEED + 200 + vi)
        dmask = in87 if vname.endswith("1987") else np.ones(n, bool)
        rows = []
        for a, j in enumerate(js):
            pj = cnt[np.flatnonzero(D[:, j] & dmask)]
            bs = pj[brng.integers(0, len(pj), (2000, len(pj)))].sum(1) / exp[a]
            r = jinfo.loc[j]
            row = dict(judge_id=int(j), nome=r.Nome_Cognome, pronunce=int(len(pj)), osservate=int(o_main[a]), attese=float(exp[a]),
                       rapporto=float(o_main[a] / exp[a]), lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)),
                       z=float(z[a]), p=float(p[a]), giuramento=str(r.data_giuramento.date()), organo=r.organo, provenienza=r.provenienza)
            if pd.notna(r["last"]) and r["last"].year <= 2015 and exp_dur[a] > 0 and exp_post[a] > 0:
                row.update(rapporto_durante=float(o_dur[a] / exp_dur[a]), rapporto_post=float(o_post[a] / exp_post[a]),
                           osservate_post=int(o_post[a]))
            rows.append(row)
        t = pd.DataFrame(rows)
        t["p_holm"] = holm(t.p.values)
        var_null = np.var(lr_sim, axis=1)
        res = {"judges_tested": int(len(t)), "sig_holm_above": int(((t.p_holm < .05) & (t.rapporto > 1)).sum()),
               "sig_holm_below": int(((t.p_holm < .05) & (t.rapporto < 1)).sum()),
               "outside_null_band_unadjusted": int(((o_main > np.quantile(sims[0], .975, 0)) | (o_main < np.quantile(sims[0], .025, 0))).sum()),
               "ratio_quantiles": {q: float(t.rapporto.quantile(q)) for q in [.05, .25, .5, .75, .95]},
               "var_log_ratio": float(np.var(lr_obs)), "var_log_ratio_null_mean": float(var_null.mean()),
               "var_log_ratio_null_hi": float(np.quantile(var_null, .975)), "var_ratio_to_null": float(np.var(lr_obs) / var_null.mean()),
               "p_heterogeneity": float((1 + (var_null >= np.var(lr_obs)).sum()) / (PERM + 1))}
        if "rapporto_post" in t:
            pmk = t.rapporto_post.notna().values
            rho = float(spearmanr(t.rapporto_durante[pmk], t.rapporto_post[pmk])[0])
            rn = np.array([spearmanr(sims[1][r_, pmk] / exp_dur[pmk], sims[2][r_, pmk] / exp_post[pmk])[0] for r_ in range(PERM)])
            pm = t[pmk]
            res["post_mandate"] = {"judges": int(pmk.sum()), "spearman_during_post": rho,
                                   "spearman_null_mean": float(rn.mean()), "spearman_null_lo": float(np.quantile(rn, .025)),
                                   "spearman_null_hi": float(np.quantile(rn, .975)), "p_above_null": float((1 + (rn >= rho).sum()) / (PERM + 1)),
                                   "median_ratio_during": float(pm.rapporto_durante.median()), "median_ratio_post": float(pm.rapporto_post.median()),
                                   "wilcoxon_p": float(wilcoxon(np.log(pm.rapporto_post.clip(lower=.01)), np.log(pm.rapporto_durante.clip(lower=.01))).pvalue)}
        res["table"] = t.sort_values("rapporto", ascending=False).to_dict("records")
        out[vname] = res
        print(vname, {k: v for k, v in res.items() if k != "table"}, flush=True)
        print(t.sort_values("rapporto", ascending=False)[["nome", "pronunce", "osservate", "attese", "rapporto", "lo", "hi", "p_holm"]].head(6).to_string(), flush=True)

    # ---- pre-registered null, kept for transparency: every citation keeps its citing pronuncia and
    # the year (and type) of its target, the target is redrawn at random. Its variance ignores how
    # differently pronunce are cited, so it overstates the number of judges far from 1 (check 17/11/2026).
    keep = in_main & ~self_all
    ci, cj = ci_all[keep], cj_all[keep]
    obs = D[cj].sum(0).astype(float)
    pre = {"note": "underdispersed: variability of a multinomial draw, not of pronunce; not interpreted"}
    for label, by_type in [("age_only", False), ("age_and_type", True)]:
        key = year[cj] * 2 + (tipo[cj] if by_type else 0)
        node_key = year * 2 + (tipo if by_type else 0)
        pools = {k: np.flatnonzero(node_key == k) for k in np.unique(key)}
        order = np.argsort(key, kind="stable")
        uniq, starts = np.unique(key[order], return_index=True)
        ends = np.r_[starts[1:], len(key)]
        sims = np.zeros((REPS, J))
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
            sims[rep] = D[new].sum(0)
        exp = sims.mean(0)
        zz = (obs[tested] - exp[tested]) / sims[:, tested].std(0, ddof=1)
        ph = holm(2 * norm.sf(np.abs(zz)))
        ratio = obs[tested] / exp[tested]
        null_var = np.var(np.log(np.maximum(sims[:, tested], .5) / exp[tested]), axis=1)
        pre[label] = {"judges_tested": int(len(tested)), "sig_holm_above": int(((ph < .05) & (ratio > 1)).sum()),
                      "sig_holm_below": int(((ph < .05) & (ratio < 1)).sum()), "var_log_ratio": float(np.var(np.log(ratio))),
                      "var_log_ratio_null_mean": float(null_var.mean()), "var_ratio_to_null": float(np.var(np.log(ratio)) / null_var.mean())}
        print("pre-registered", label, pre[label], flush=True)
    out["nullo_preregistrato"] = pre
    json.dump(out, open(REPO / "reports/d2_results.json", "w"), indent=1, ensure_ascii=False, default=float)

    # ---------------- D4 (own random stream: changes to D2 must not alter D4)
    rng = np.random.default_rng(SEED + 4)
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
