"""D3 - collegial memory. Does a drafter cite more often the precedents decided by
a collegio he or she sat on?  PRIMARY RESULT of the project (docs/spec.md).

Design (all fixed in docs/decisions.md before any estimate):
  stratum      one citing pronuncia with a single matched drafter R
  risk set     precedents decided between R's first and last appearance in a
               collegio and deposited before the citing pronuncia
  cases        precedents of the risk set cited in the base text
  controls     50 non-cited precedents drawn at random from the risk set
  variables    self_drafted, sat_not_drafted (reference: R in office but absent
               from the collegio), age classes, topic similarity (cosine)
  model        conditional logit (Breslow form for several cases per stratum),
               standard errors clustered by drafter

Secondary "full" model: risk set = all earlier precedents, reference category =
precedent decided before R joined the Court.

Outputs: reports/d3_results.json, reports/d3_results.md
Usage: .venv/bin/python src/analysis/d3_memoria_collegiale.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
P = REPO / "data/processed"
SEED = 20261116
N_CONTROLS = 50
AGE_BINS = [0, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 200]
SWITCH = 19860287


def clogit(X: np.ndarray, y: np.ndarray, strata: np.ndarray, cluster: np.ndarray):
    """Conditional logit, Breslow likelihood. Rows must be sorted by stratum.
    Returns beta, cluster-robust covariance, log-likelihood."""
    starts = np.flatnonzero(np.r_[True, strata[1:] != strata[:-1]])
    sid = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(strata)]))
    d = np.add.reduceat(y, starts).astype(float)
    k = X.shape[1]
    beta = np.zeros(k)
    sx_case = np.add.reduceat(X * y[:, None], starts)

    def parts(b):
        eta = X @ b
        eta = eta - np.maximum.reduceat(eta, starts)[sid]
        w = np.exp(eta)
        den = np.add.reduceat(w, starts)
        p = w / den[sid]
        xbar = np.add.reduceat(X * p[:, None], starts)
        ll = float((y * eta).sum() - (d * np.log(den)).sum())
        score_s = sx_case - d[:, None] * xbar
        Xc = X - xbar[sid]
        H = (Xc * (p * d[sid])[:, None]).T @ Xc
        return ll, score_s, H

    for _ in range(50):
        ll, score_s, H = parts(beta)
        step = np.linalg.solve(H, score_s.sum(0))
        beta = beta + step
        if np.abs(step).max() < 1e-9:
            break
    ll, score_s, H = parts(beta)
    Hinv = np.linalg.inv(H)
    cl = cluster[starts]
    S = pd.DataFrame(score_s).groupby(cl).sum().values
    G = len(S)
    V = Hinv @ (S.T @ S) @ Hinv * G / (G - 1)
    return beta, V, ll, G, len(starts)


def load():
    nodes = pd.read_csv(P / "nodes.csv", parse_dates=["data_decisione", "data_deposito"])
    nodes["dec"] = nodes.data_decisione.fillna(nodes.data_deposito)
    coll = pd.read_csv(P / "collegio.csv").merge(nodes[["pid", "dec"]], on="pid")
    app = coll.groupby("judge_id").dec.agg(first="min", last="max")
    edges = pd.read_csv(P / "edges_citations.csv")
    z = np.load(P / "topics_theta.npz")
    th = z["theta"] / np.linalg.norm(z["theta"], axis=1, keepdims=True)
    theta = dict(zip(z["pid"], th))
    return nodes, coll, app, edges, theta


def build(nodes, coll, app, edges, theta, mode="mandate", edges_file=None, rng=None):
    """Case-control table. mode = 'mandate' (primary risk set) or 'full'."""
    rng = rng or np.random.default_rng(SEED)
    if edges_file:
        edges = pd.read_csv(P / edges_file)
    nodes = nodes.sort_values(["data_deposito", "pid"]).reset_index(drop=True)
    pid = nodes.pid.values
    dep = nodes.data_deposito.values.astype("datetime64[D]")
    dec = nodes.dec.values.astype("datetime64[D]")
    idx = {p: i for i, p in enumerate(pid)}
    sat = coll.groupby("pid").judge_id.apply(set).to_dict()
    red = {r.pid: {int(x) for x in str(r.redattore_ids).split("|") if x not in ("", "nan", "0")} for r in nodes.itertuples()}
    cited = edges.groupby("citing_id").cited_id.apply(set).to_dict()
    has_theta = np.array([p in theta for p in pid])
    first = {j: np.datetime64(d, "D") for j, d in app["first"].items()}
    last = {j: np.datetime64(d, "D") for j, d in app["last"].items()}
    rows = []
    for i, r in enumerate(nodes.itertuples()):
        R = red[r.pid]
        if len(R) != 1 or r.redattore_source == "none" or r.pid not in theta:
            continue
        R = next(iter(R))
        if R not in first:
            continue
        n_before = np.searchsorted(dep, dep[i], side="left")  # deposited strictly before
        cand = np.arange(n_before)
        in_mand = (dec[cand] >= first[R]) & (dec[cand] <= last[R])
        if mode == "mandate":
            cand = cand[in_mand & has_theta[cand]]
        else:
            keep = has_theta[cand]
            cand, in_mand = cand[keep], in_mand[keep]
        if len(cand) == 0:
            continue
        cset = cited.get(r.pid, set())
        is_case = np.fromiter((pid[j] in cset for j in cand), bool, len(cand))
        if not is_case.any():
            continue
        ctrl = np.flatnonzero(~is_case)
        if len(ctrl) > N_CONTROLS:
            ctrl = rng.choice(ctrl, N_CONTROLS, replace=False)
        sel = np.r_[np.flatnonzero(is_case), ctrl]
        tc = theta[r.pid]
        for s in sel:
            j = cand[s]
            p = pid[j]
            sj = R in sat.get(p, ())
            dj = R in red[p]
            rows.append((r.pid, p, int(is_case[s]), R, int(dj), int(sj and not dj), int(sj),
                         int(in_mand[s]) if mode == "full" else 1,
                         (dep[i] - dep[j]).astype(int) / 365.25, float(tc @ theta[p]),
                         r.anno, r.tipo, nodes.tipo.values[j], r.giudizio, nodes.in_deg.values[j]))
    cols = ["citing", "cited", "y", "R", "self_drafted", "sat_not_drafted", "sat", "in_mandate", "age", "sim",
            "anno", "tipo", "tipo_cited", "giudizio", "in_deg_cited"]
    return pd.DataFrame(rows, columns=cols)


def design(t: pd.DataFrame, mode: str, extra=False):
    age = pd.cut(t.age, AGE_BINS, right=False, labels=False)
    used = sorted(age.dropna().unique())[1:]
    cols = {"self_drafted": t.self_drafted.values, "sat_not_drafted": t.sat_not_drafted.values}
    if mode == "full":
        cols["in_mandate_absent"] = (t.in_mandate.values == 1) & (t.sat.values == 0)
    cols["topic_similarity"] = t.sim.values
    for a in used:
        cols[f"age_{AGE_BINS[int(a)]}_{AGE_BINS[int(a) + 1]}"] = (age == a).values
    if extra:
        cols["cited_is_sentenza"] = (t.tipo_cited == "S").values
        cols["log1p_citations_cited"] = np.log1p(t.in_deg_cited.values)
    X = np.column_stack([np.asarray(v, float) for v in cols.values()])
    keep = X.std(0) > 0
    return X[:, keep], [c for c, k in zip(cols, keep) if k]


def estimate(t: pd.DataFrame, mode="mandate", extra=False, label=""):
    t = t.sort_values(["citing", "y"], ascending=[True, False]).reset_index(drop=True)
    X, names = design(t, mode, extra)
    beta, V, ll, G, S = clogit(X, t.y.values.astype(float), t.citing.values, t.R.values)
    se = np.sqrt(np.diag(V))
    res = {"label": label, "strata": int(S), "clusters": int(G), "rows": int(len(t)), "cases": int(t.y.sum()),
           "cases_sat_not_drafted": int((t.y * t.sat_not_drafted).sum()), "cases_self_drafted": int((t.y * t.self_drafted).sum()),
           "cases_absent": int((t.y * (1 - t.sat) * t.in_mandate).sum()),
           "controls_absent": int(((1 - t.y) * (1 - t.sat) * t.in_mandate).sum()), "loglik": ll, "coef": {}}
    for n, b, s in zip(names, beta, se):
        res["coef"][n] = {"or": float(np.exp(b)), "lo": float(np.exp(b - 1.96 * s)), "hi": float(np.exp(b + 1.96 * s)),
                          "beta": float(b), "se": float(s), "p": float(2 * stats.norm.sf(abs(b / s)))}
    return res


def main():
    nodes, coll, app, edges, theta = load()
    out = {}
    t = build(nodes, coll, app, edges, theta, "mandate")
    t.to_pickle(REPO / "data/interim/d3_mandate.pkl")
    # descriptive: raw citation rates by category (per 1,000 pairs of the full risk set are not
    # available after sampling; cases vs sampled controls are reported instead)
    out["raw"] = {k: {"cases": int(v.y.sum()), "controls": int((1 - v.y).sum())}
                  for k, v in {"self_drafted": t[t.self_drafted == 1], "sat_not_drafted": t[t.sat_not_drafted == 1],
                               "absent": t[t.sat == 0]}.items()}
    out["primary"] = estimate(t, label="Risultato principale: precedenti decisi durante il mandato del redattore")
    V = {}
    V["controlli aggiuntivi (tipo del precedente, citazioni ricevute)"] = estimate(t, extra=True)
    V["senza autocitazioni del redattore"] = estimate(t[t.self_drafted == 0])
    V["solo pronunce dalla 287/1986 (redattore osservato)"] = estimate(t[(t.citing >= SWITCH) & (t.cited >= SWITCH)])
    V["solo pronunce fino alla 286/1986 (relatore come approssimazione)"] = estimate(t[t.citing < SWITCH])
    V["senza gli anni dell'arretrato (citanti 1987-1989 escluse)"] = estimate(t[~t.anno.between(1987, 1989)])
    V["senza le ordinanze di correzione"] = estimate(t[t.giudizio != "correzione"])
    V["solo sentenze che citano"] = estimate(t[t.tipo == "S"])
    V["solo ordinanze che citano"] = estimate(t[t.tipo == "O"])
    V["citanti fino al 2000"] = estimate(t[t.anno <= 2000])
    V["citanti dal 2001"] = estimate(t[t.anno >= 2001])
    V["solo giudizi in via incidentale"] = estimate(t[t.giudizio == "incidentale"])
    tf = build(nodes, coll, app, edges, theta, "mandate", edges_file="edges_citations_fulltext.csv")
    V["testo intero (anche Ritenuto in fatto)"] = estimate(tf)
    tn = build(nodes, coll, app, edges, theta, "mandate", edges_file="edges_citations_with_notes.csv")
    V["con le citazioni delle massime (note editoriali)"] = estimate(tn)
    # sensitivity to the control sample: 5 other seeds
    ors = []
    for s in range(1, 6):
        ts = build(nodes, coll, app, edges, theta, "mandate", rng=np.random.default_rng(SEED + s))
        ors.append(estimate(ts)["coef"]["sat_not_drafted"]["or"])
    out["seed_sensitivity_or"] = ors
    out["variants"] = V
    full = build(nodes, coll, app, edges, theta, "full")
    out["full"] = estimate(full, mode="full", label="Modello completo: tutti i precedenti, riferimento = precedente al mandato")
    # absences by time since first appearance (mechanical-absence check)
    c2 = coll.merge(app, left_on="judge_id", right_index=True)
    out["absence_check"] = "risk set starts at the first collegio appearance of the drafter"
    json.dump(out, open(REPO / "reports/d3_results.json", "w"), indent=1, ensure_ascii=False)

    def row(name, r):
        c = r["coef"]["sat_not_drafted"]
        return (f"| {name} | {r['strata']:,} | {r['cases']:,} | {r['cases_absent']:,} | {c['or']:.2f} | {c['lo']:.2f}–{c['hi']:.2f} | {c['p']:.2g} |")
    md = ["# D3 - memoria collegiale\n", "Generato da `src/analysis/d3_memoria_collegiale.py`.\n",
          "Odds ratio di `sat_not_drafted`: quanto più spesso il redattore cita un precedente deciso da un collegio in cui sedeva "
          "(senza averlo redatto) rispetto a un precedente deciso mentre era in carica ma assente. Errori standard raggruppati per redattore.\n",
          "| Analisi | Pronunce che citano | Citazioni | Citazioni a precedenti con redattore assente | OR | IC 95% | p |",
          "| --- | --- | --- | --- | --- | --- | --- |", row("**Principale**", out["primary"])]
    md += [row(k, v) for k, v in V.items()]
    md.append("\n**Tutti i coefficienti del modello principale**\n\n| Variabile | OR | IC 95% | p |\n| --- | --- | --- | --- |")
    md += [f"| {n} | {c['or']:.3f} | {c['lo']:.3f}–{c['hi']:.3f} | {c['p']:.2g} |" for n, c in out["primary"]["coef"].items()]
    md.append(f"\nSensibilità al campione dei controlli (altri 5 seed), OR: {', '.join(f'{x:.3f}' for x in ors)}.")
    md.append(f"\nGruppi (redattori): {out['primary']['clusters']}. Righe: {out['primary']['rows']:,}.")
    md.append("\n**Modello completo** (tutti i precedenti; riferimento: precedente deciso prima dell'ingresso del redattore)\n\n| Variabile | OR | IC 95% | p |\n| --- | --- | --- | --- |")
    md += [f"| {n} | {c['or']:.3f} | {c['lo']:.3f}–{c['hi']:.3f} | {c['p']:.2g} |" for n, c in out["full"]["coef"].items()]
    (REPO / "reports/d3_results.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
