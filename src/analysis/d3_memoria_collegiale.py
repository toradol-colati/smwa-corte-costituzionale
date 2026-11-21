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
  model        conditional logit with the exact conditional likelihood (all subsets
               of d cases among the n rows of a stratum, computed by recursion),
               standard errors clustered by drafter. The Breslow approximation, used
               until 17/11/2026, is kept only as starting point and for comparison:
               with several cases per stratum it biases strong effects towards 1.

Secondary "full" model: risk set = all earlier precedents, reference category =
precedent decided before R joined the Court.

Exploratory variant (18/11/2026): the same model plus two pair variables, same challenged act and
same challenged article (norme oggetto from the massime, legge 87/1953 art. 23), to see whether the
self-drafted effect comes from repeated questions assigned to the same relatore.

Outputs: reports/d3_results.json, reports/d3_results.md
Usage: .venv/bin/python src/analysis/d3_memoria_collegiale.py
       add --md-only to rewrite reports/d3_results.md from reports/d3_results.json
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


def clogit_breslow(X: np.ndarray, y: np.ndarray, strata: np.ndarray, cluster: np.ndarray):
    """Conditional logit, Breslow approximation (starting values and comparison only). Rows must be sorted by stratum.
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

    ll, score_s, H = parts(beta)
    for _ in range(50):
        step = np.linalg.solve(H, score_s.sum(0))
        for _half in range(30):  # step-halving: the plain Newton step can overshoot
            ll2, score2, H2 = parts(beta + step)
            if np.isfinite(ll2) and ll2 >= ll - 1e-10:
                break
            step = step / 2
        beta, ll, score_s, H = beta + step, ll2, score2, H2
        if np.abs(step).max() < 1e-9:
            break
    Hinv = np.linalg.inv(H)
    cl = cluster[starts]
    S = pd.DataFrame(score_s).groupby(cl).sum().values
    G = len(S)
    V = Hinv @ (S.T @ S) @ Hinv * G / (G - 1)
    return beta, V, ll, G, len(starts)


D_BINS = [1, 2, 3, 4, 6, 9, 13, 21, 36, 10**6]  # strata grouped by number of cases, to vectorise the recursion


class ExactCLogit:
    """Exact conditional logit. For a stratum with weights w_i = exp(x_i b) and d cases the
    likelihood is exp(sum_cases x_i b) / e_d(w), where e_d is the elementary symmetric
    polynomial of degree d (sum over all subsets of d rows). e_d, its gradient and its
    Hessian are computed with the recursion e_k <- e_k + w_j e_(k-1), row by row, for all
    strata of a group at once; rows are rescaled at every step to avoid overflow.
    Rows must be sorted by stratum."""

    def __init__(self, X, y, strata, cluster):
        self.X, self.y = X, y.astype(float)
        starts = np.flatnonzero(np.r_[True, strata[1:] != strata[:-1]])
        lens = np.diff(np.r_[starts, len(strata)])
        self.starts, self.sid = starts, np.repeat(np.arange(len(starts)), lens)
        self.d = np.add.reduceat(self.y, starts).astype(int)
        self.sx_case = np.add.reduceat(X * self.y[:, None], starts)
        self.cluster = cluster[starts]
        self.groups = []
        for lo, hi in zip(D_BINS[:-1], D_BINS[1:]):
            ss = np.flatnonzero((self.d >= lo) & (self.d < hi))
            if len(ss) == 0:
                continue
            nmax = int(lens[ss].max())
            pos = np.arange(nmax)
            idx = starts[ss][:, None] + pos[None, :]
            valid = pos[None, :] < lens[ss][:, None]
            self.groups.append((ss, np.where(valid, idx, 0), valid, int(self.d[ss].max())))

    def evaluate(self, b, hessian=True):
        """Returns log-likelihood, per-stratum scores (S x k) and the Hessian (k x k)."""
        X, k = self.X, self.X.shape[1]
        eta = X @ b
        # each stratum is centred on its d-th largest linear predictor (d = cases), not on the largest: the likelihood
        # does not change, and e_d stays representable (at least d weights are >= 1), where centring on the largest
        # let it underflow in strata with many cases and widely spread weights
        order = np.lexsort((-eta, self.sid))
        m = eta[order][self.starts + self.d - 1]
        w_all = np.exp(eta - m[self.sid])
        S = len(self.starts)
        logden = np.zeros(S)
        dlog = np.zeros((S, k))
        H = np.zeros((k, k))
        for ss, idx, valid, D in self.groups:
            W = np.where(valid, w_all[idx], 0.0)
            Xg = X[idx] * valid[:, :, None]
            G = len(ss)
            E = np.zeros((G, D + 1)); E[:, 0] = 1.0
            dE = np.zeros((G, D + 1, k))
            ddE = np.zeros((G, D + 1, k, k)) if hessian else None
            logc = np.zeros(G)
            for j in range(idx.shape[1]):
                w, x = W[:, j], Xg[:, j, :]
                Es, dEs = E[:, :-1], dE[:, :-1, :]
                if hessian:
                    ddEs = ddE[:, :-1]
                    t = (x[:, None, :, None] * x[:, None, None, :]) * Es[:, :, None, None] \
                        + x[:, None, :, None] * dEs[:, :, None, :] + dEs[:, :, :, None] * x[:, None, None, :] + ddEs
                    ddE[:, 1:] += w[:, None, None, None] * t
                dE[:, 1:] += w[:, None, None] * (x[:, None, :] * Es[:, :, None] + dEs)
                E[:, 1:] += w[:, None] * Es
                c = E.max(1)
                E /= c[:, None]; dE /= c[:, None, None]
                if hessian:
                    ddE /= c[:, None, None, None]
                logc += np.log(c)
            dg = self.d[ss]
            Ed = E[np.arange(G), dg]
            if (Ed <= 0).any():
                raise FloatingPointError("e_d underflow in a stratum")
            dEd = dE[np.arange(G), dg]
            logden[ss] = np.log(Ed) + logc
            dlog[ss] = dEd / Ed[:, None]
            if hessian:
                ddEd = ddE[np.arange(G), dg]
                r = dEd / Ed[:, None]
                H -= (ddEd / Ed[:, None, None]).sum(0) - (r[:, :, None] * r[:, None, :]).sum(0)
        ll = float((self.y * (eta - m[self.sid])).sum() - logden.sum())
        return ll, self.sx_case - dlog, H

    def fit(self, b0, tol=1e-9, max_iter=50):
        b = np.asarray(b0, float).copy()
        ll, sc, H = self.evaluate(b)
        for _ in range(max_iter):
            step = np.linalg.solve(-H, sc.sum(0))
            ok = None
            for _half in range(30):
                try:
                    trial = self.evaluate(b + step)
                except FloatingPointError:  # trial point so far off that e_d underflows: worse by definition, halve
                    step /= 2
                    continue
                ok = trial
                if trial[0] >= ll - 1e-10:
                    break
                step /= 2
            if ok is None:
                raise FloatingPointError("e_d underflow at every trial step")
            ll2, sc2, H2 = ok
            b, ll, sc, H = b + step, ll2, sc2, H2
            self.n_iter = _ + 1
            if np.abs(step).max() < tol:
                break
        Hinv = np.linalg.inv(-H)
        # convergence = the full (not halved) Newton step at the final point is negligible; recorded, not used by the main analysis
        self.max_newton_step = float(np.abs(Hinv @ sc.sum(0)).max())
        self.converged = self.max_newton_step < 1e-6
        Sc = pd.DataFrame(sc).groupby(self.cluster).sum().values
        G = len(Sc)
        V = Hinv @ (Sc.T @ Sc) @ Hinv * G / (G - 1)
        return b, V, ll, G, len(self.starts)


def clogit(X: np.ndarray, y: np.ndarray, strata: np.ndarray, cluster: np.ndarray):
    """Exact conditional logit, started from the Breslow estimate. Returns beta, cluster-robust
    covariance, log-likelihood, number of clusters, number of strata, Breslow beta."""
    b0 = clogit_breslow(X, y, strata, cluster)[0]
    model = ExactCLogit(X, y, strata, cluster)
    b, V, ll, G, S = model.fit(b0)
    clogit.last = {"converged": model.converged, "max_newton_step": model.max_newton_step, "newton_iterations": model.n_iter}
    return b, V, ll, G, S, b0


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


def load_norme():
    """Challenged provisions (norme oggetto, legge 87/1953 art. 23) of every pronuncia, from the
    massime: set of acts (code or description, number, date) and of articles (act + article).
    Returns the two dicts and the coverage by decade."""
    import glob
    from lxml import etree
    acts, arts, rows = {}, {}, []
    for path in sorted(glob.glob(str(REPO / "data/raw/massime/*/*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            h = p.find("pronuncia_testata")
            pid = int(h.findtext("anno_pronuncia")) * 10000 + int(h.findtext("numero_pronuncia"))
            for m in p.findall("massime/massima"):
                ns = m.findall("norme/norma")
                rows.append((pid, len(ns) > 0))
                for x in ns:
                    f = {c: (x.findtext(c) or "").strip().lower() for c in ["codice", "descrizione", "numero", "data", "articolo"]}
                    act = (f["codice"] or f["descrizione"], f["numero"], f["data"])
                    acts.setdefault(pid, set()).add(act)
                    if f["articolo"]:
                        arts.setdefault(pid, set()).add(act + (f["articolo"],))
    d = pd.DataFrame(rows, columns=["pid", "has"])
    cov = {"massime_with_norme": float(d.has.mean()), "pronunce_with_norme": float(d.groupby("pid").has.max().mean()),
           "by_decade_massime": {int(k): float(v) for k, v in d.groupby(d.pid // 100000 * 10).has.mean().items()}}
    return acts, arts, cov


def load_parametri():
    """Constitutional articles of every pronuncia (src/analysis/parametri.py), their idf weights and
    the norm of each pronuncia's weighted vector, for the cosine similarity of a pair."""
    import math
    t = pd.read_csv(P / "parametri_pronunce.csv")
    sets = {r.pid: set(str(r.articles).split("|")) for r in t.itertuples()}
    N = len(sets)
    n_a = {}
    for st in sets.values():
        for a in st:
            n_a[a] = n_a.get(a, 0) + 1
    w = {a: math.log(N / c) for a, c in n_a.items()}
    norm = {p: math.sqrt(sum(w[a] ** 2 for a in st)) for p, st in sets.items()}
    return sets, w, norm


def build(nodes, coll, app, edges, theta, mode="mandate", edges_file=None, rng=None, norme=None, param=None):
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
        acts_c, arts_c = (norme[0].get(r.pid, set()), norme[1].get(r.pid, set())) if norme else (set(), set())
        par_c = param[0].get(r.pid, set()) if param else set()
        for s in sel:
            j = cand[s]
            p = pid[j]
            sj = R in sat.get(p, ())
            dj = R in red[p]
            if norme:
                acts_p, arts_p = norme[0].get(p, set()), norme[1].get(p, set())
                nm = (int(bool(acts_c & acts_p)), int(bool(arts_c & arts_p)), int(not acts_c or not acts_p))
            else:
                nm = (0, 0, 1)
            if param:
                par_p = param[0].get(p, set())
                if par_c and par_p:
                    nm = nm + (sum(param[1][a] ** 2 for a in par_c & par_p) / (param[2][r.pid] * param[2][p]), 0)
                else:
                    nm = nm + (0.0, 1)
            else:
                nm = nm + (0.0, 1)
            rows.append((r.pid, p, int(is_case[s]), R, int(dj), int(sj and not dj), int(sj),
                         int(in_mand[s]) if mode == "full" else 1,
                         (dep[i] - dep[j]).astype(int) / 365.25, float(tc @ theta[p]),
                         r.anno, r.tipo, nodes.tipo.values[j], r.giudizio, nodes.in_deg.values[j]) + nm)
    cols = ["citing", "cited", "y", "R", "self_drafted", "sat_not_drafted", "sat", "in_mandate", "age", "sim",
            "anno", "tipo", "tipo_cited", "giudizio", "in_deg_cited", "same_act", "same_article", "norme_missing",
            "param_sim", "param_missing"]
    return pd.DataFrame(rows, columns=cols)


def design(t: pd.DataFrame, mode: str, extra=False, norme=False, param=False, bins=None):
    bins = AGE_BINS if bins is None else bins  # other classes only in the check of the full model (d3_full_check.py)
    age = pd.cut(t.age, bins, right=False, labels=False)
    used = sorted(age.dropna().unique())[1:]
    cols = {"self_drafted": t.self_drafted.values, "sat_not_drafted": t.sat_not_drafted.values}
    if mode == "full":
        cols["in_mandate_absent"] = (t.in_mandate.values == 1) & (t.sat.values == 0)
    cols["topic_similarity"] = t.sim.values
    for a in used:
        cols[f"age_{bins[int(a)]}_{bins[int(a) + 1]}"] = (age == a).values
    if extra:
        cols["cited_is_sentenza"] = (t.tipo_cited == "S").values
        cols["log1p_citations_cited"] = np.log1p(t.in_deg_cited.values)
    if norme:  # exploratory: same challenged act / article (legge 87/1953 art. 23), missing-data indicator
        cols["same_challenged_act"] = t.same_act.values
        cols["same_challenged_article"] = t.same_article.values
        cols["challenged_norms_missing"] = t.norme_missing.values
    if param:  # exploratory (19/11/2026): finer subject, weighted similarity of the constitutional articles invoked
        cols["param_similarity"] = t.param_sim.values
        cols["param_missing"] = t.param_missing.values
    X = np.column_stack([np.asarray(v, float) for v in cols.values()])
    keep = X.std(0) > 0
    return X[:, keep], [c for c, k in zip(cols, keep) if k]


def estimate(t: pd.DataFrame, mode="mandate", extra=False, label="", norme=False, param=False):
    t = t.sort_values(["citing", "y"], ascending=[True, False]).reset_index(drop=True)
    X, names = design(t, mode, extra, norme, param)
    beta, V, ll, G, S, b_breslow = clogit(X, t.y.values.astype(float), t.citing.values, t.R.values)
    se = np.sqrt(np.diag(V))
    res = {"label": label, "strata": int(S), "clusters": int(G), "rows": int(len(t)), "cases": int(t.y.sum()),
           "cases_sat_not_drafted": int((t.y * t.sat_not_drafted).sum()), "cases_self_drafted": int((t.y * t.self_drafted).sum()),
           "cases_absent": int((t.y * (1 - t.sat) * t.in_mandate).sum()),
           "controls_absent": int(((1 - t.y) * (1 - t.sat) * t.in_mandate).sum()), "loglik": ll, **clogit.last, "coef": {}}
    for n, b, s, bb in zip(names, beta, se, b_breslow):
        res["coef"][n] = {"or": float(np.exp(b)), "lo": float(np.exp(b - 1.96 * s)), "hi": float(np.exp(b + 1.96 * s)),
                          "beta": float(b), "se": float(s), "p": float(2 * stats.norm.sf(abs(b / s))),
                          "or_breslow": float(np.exp(bb))}
    return res


VARIANT_LABELS = {  # keys of reports/d3_results.json -> plain labels for the report
    "controlli aggiuntivi (tipo del precedente, citazioni ricevute)": "con due controlli in più: tipo del precedente e citazioni già ricevute",
    "senza autocitazioni del redattore": "senza i precedenti scritti dallo stesso giudice",
    "solo pronunce dalla 287/1986 (redattore osservato)": "solo pronunce dalla 287/1986 (il nome di chi scrive è nei dati)",
    "solo pronunce fino alla 286/1986 (relatore come approssimazione)": "solo pronunce che citano fino alla 286/1986 (al posto di chi scrive, il relatore)",
    "senza gli anni dell'arretrato (citanti 1987-1989 escluse)": "senza gli anni dell'arretrato (tolte le pronunce che citano del 1987–1989)",
    "senza le ordinanze di correzione": "senza le ordinanze che correggono errori materiali",
    "solo sentenze che citano": "solo sentenze che citano",
    "solo ordinanze che citano": "solo ordinanze che citano",
    "citanti fino al 2000": "solo pronunce che citano fino al 2000",
    "citanti dal 2001": "solo pronunce che citano dal 2001",
    "solo giudizi in via incidentale": "solo giudizi in via incidentale",
    "testo intero (anche Ritenuto in fatto)": "citazioni da tutto il testo (anche dal «Ritenuto in fatto»)",
    "con le citazioni delle massime (note editoriali)": "con anche le citazioni delle note editoriali alle massime",
    "controllo per norma impugnata in comune (esplorativo)": "con un controllo per la stessa legge impugnata (prova esplorativa)",
    "materia fine: parametri costituzionali (esplorativo)": "materia più fine, dagli articoli della Costituzione invocati (prova esplorativa)",
}
COEF_LABELS = {
    "self_drafted": "il precedente l'ha scritto lo stesso giudice (`self_drafted`)",
    "sat_not_drafted": "il giudice sedeva nel collegio del precedente, senza scriverlo (`sat_not_drafted`)",
    "in_mandate_absent": "il precedente è stato deciso mentre il giudice era in carica, ma assente (`in_mandate_absent`)",
    "topic_similarity": "somiglianza di materia tra le due pronunce, da 0 a 1 (`topic_similarity`)",
}


def _num(x, d):  # Italian format: comma for decimals
    return f"{x:.{d}f}".replace(".", ",")


def _int(x):  # Italian format: dot for thousands
    return f"{x:,}".replace(",", ".")


def _p(p):
    return "< 0,001" if p < 0.001 else _num(p, 3)


def _coef_label(n):
    if n.startswith("age_"):
        lo, hi = n[4:].split("_")
        return f"il precedente ha {lo} anni o più" if hi == "200" else f"il precedente ha tra {lo} e {hi} anni"
    return COEF_LABELS.get(n, n)


def render_md(out):
    """Write reports/d3_results.md from the numbers in reports/d3_results.json (no estimation here)."""
    def row(name, r):
        c = r["coef"]["sat_not_drafted"]
        return (f"| {name} | {_int(r['strata'])} | {_int(r['cases'])} | {_int(r['cases_absent'])} | {_num(c['or'], 2)} | "
                f"{_num(c['lo'], 2)}–{_num(c['hi'], 2)} | {_p(c['p'])} |")

    def coef_table(res):
        lines = ["| Caratteristica del precedente | Odds ratio | Intervallo al 95% | Valore p |", "| --- | --- | --- | --- |"]
        return lines + [f"| {_coef_label(n)} | {_num(c['or'], 3)} | {_num(c['lo'], 3)}–{_num(c['hi'], 3)} | {_p(c['p'])} |"
                        for n, c in res["coef"].items()]

    p = out["primary"]
    md = ["# D3: un giudice cita di più le pronunce decise in collegi in cui sedeva?\n",
          "Prodotto da `src/analysis/d3_memoria_collegiale.py`, con i numeri salvati in `reports/d3_results.json`.\n",
          "## Che cosa misura la tabella principale\n",
          "Per ogni pronuncia che cita, il programma mette a confronto i precedenti che cita con un campione di precedenti che avrebbe "
          "potuto citare e non ha citato. Guarda solo i precedenti decisi mentre il giudice che scrive la pronuncia era già alla Corte. "
          "Tra questi distingue due gruppi:\n",
          "- i precedenti decisi da un collegio in cui il giudice sedeva, senza averli scritti lui;",
          "- i precedenti decisi mentre il giudice era in carica, ma assente da quel collegio.\n",
          "La colonna \"Odds ratio\" dice quanto è più probabile, in termini di odds, che il giudice citi un precedente del primo gruppo "
          "invece che del secondo, a parità di età del precedente, di materia e del fatto di averlo scritto lui. 1 vuol dire nessuna "
          "differenza; sopra 1 cita di più i precedenti decisi con lui presente; sotto 1, di meno. L'intervallo al 95% raccoglie i valori "
          "compatibili con i dati. Il valore p dice quanto sarebbe raro un risultato così lontano da 1 se la differenza non ci fosse. "
          "L'incertezza tiene conto che le pronunce scritte dallo stesso giudice si somigliano (errori standard raggruppati per chi scrive).\n",
          "La prima riga è il risultato principale, deciso prima di vedere i dati. Le altre ripetono il calcolo cambiando una cosa alla "
          "volta, per vedere se il risultato regge.\n",
          "| Prova | Pronunce che citano | Citazioni | Di cui a precedenti decisi con il giudice assente | Odds ratio | "
          "Intervallo al 95% | Valore p |",
          "| --- | --- | --- | --- | --- | --- | --- |", row("**Risultato principale**", p)]
    md += [row(VARIANT_LABELS.get(k, k), v) for k, v in out["variants"].items()]
    md += ["\n## Tutti i numeri del modello principale\n",
           "Ogni riga confronta i precedenti con quella caratteristica con quelli senza. Per le classi di età il confronto è con i "
           "precedenti di meno di un anno. Per la somiglianza di materia il confronto è tra i due estremi, 0 (nessun tema in comune) e 1 "
           "(gli stessi temi nelle stesse proporzioni): per questo il numero è così grande.\n"] + coef_table(p)
    seeds = "; ".join(_num(x, 3) for x in out["seed_sensitivity_or"])
    md += [f"\nLo stesso calcolo, ripetuto con altri 5 campioni casuali di precedenti non citati, dà questi odds ratio per "
           f"`sat_not_drafted`: {seeds}.",
           f"\nGiudici che scrivono (i gruppi usati per l'incertezza): {_int(p['clusters'])}. Righe del confronto: {_int(p['rows'])}.",
           "\n## Il modello completo (secondario)\n",
           "Qui entrano tutti i precedenti, anche quelli decisi prima che il giudice arrivasse alla Corte, e il confronto è con questi "
           "ultimi. Il risultato non dice solo se il giudice sedeva nel collegio, ma anche quanto il precedente è vicino nel tempo: per "
           "questo è secondario. Il controllo su questo modello è in `reports/d3_full_check.json` e nella relazione, sezione 3.4.\n"]
    md += coef_table(out["full"])
    return "\n".join(md) + "\n"


def main():
    nodes, coll, app, edges, theta = load()
    acts, arts, cov = load_norme()
    par = load_parametri()
    out = {"norme_coverage": cov}
    t = build(nodes, coll, app, edges, theta, "mandate", norme=(acts, arts), param=par)
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
    # exploratory (18/11/2026): are self-citations repeated questions? Same challenged act / article
    V["controllo per norma impugnata in comune (esplorativo)"] = estimate(t, norme=True)
    # exploratory (19/11/2026): finer subject from the constitutional articles invoked (docs/decisions.md)
    V["materia fine: parametri costituzionali (esplorativo)"] = estimate(t, param=True)
    known = t[t.norme_missing == 0]
    out["norme_descrittive"] = {lab: {"cases_same_article": float(known[m & (known.y == 1)].same_article.mean()),
                                      "controls_same_article": float(known[m & (known.y == 0)].same_article.mean()),
                                      "cases": int((m & (known.y == 1)).sum())}
                                for lab, m in [("self_drafted", known.self_drafted == 1), ("sat_not_drafted", known.sat_not_drafted == 1),
                                               ("absent", known.sat == 0)]}
    # sensitivity to the control sample: 5 other seeds
    ors = []
    for s in range(1, 6):
        ts = build(nodes, coll, app, edges, theta, "mandate", rng=np.random.default_rng(SEED + s))
        ors.append(estimate(ts)["coef"]["sat_not_drafted"]["or"])
    out["seed_sensitivity_or"] = ors
    out["variants"] = V
    full = build(nodes, coll, app, edges, theta, "full")
    out["full"] = estimate(full, mode="full", label="Modello completo: tutti i precedenti, riferimento = precedente al mandato")
    # absences from the collegio are described in src/analysis/d3_absences.py (reports/d3_absences.json)
    json.dump(out, open(REPO / "reports/d3_results.json", "w"), indent=1, ensure_ascii=False)

    (REPO / "reports/d3_results.md").write_text(render_md(out), encoding="utf-8")


if __name__ == "__main__":
    import sys
    if "--md-only" in sys.argv:  # rewrite the report from the saved numbers, without estimating again
        (REPO / "reports/d3_results.md").write_text(render_md(json.load(open(REPO / "reports/d3_results.json"))), encoding="utf-8")
    else:
        main()
