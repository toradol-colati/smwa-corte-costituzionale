"""Topic model (LDA) on the texts of the massime, to obtain the subject matter of
each pronuncia. Rules fixed in docs/spec.md (Modelli nulli, point 8):
  - K in 10..60 step 10; choose the smallest K whose coherence is within 2% of the best
    (NPMI on document co-occurrence of the top-10 words; see docs/decisions.md);
  - stability over 5 seeds;
  - pronuncia = simple mean of its massime; subject = topic with the highest mean weight.

Outputs: data/processed/topics_theta.npz (pid, theta), data/processed/topics_pronunce.csv,
reports/topics.md, reports/topics.json
Usage: .venv/bin/python src/analysis/topics.py
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from lxml import etree
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import normalized_mutual_info_score

REPO = Path(__file__).resolve().parents[2]
SEED = 20261116
STOP = set("""a ad al allo ai agli all alla alle con col coi da dal dallo dai dagli dall dalla dalle di del dello dei degli dell della
delle in nel nello nei negli nell nella nelle su sul sullo sui sugli sull sulla sulle per tra fra il lo la i gli le un uno una e ed o od ma
se che chi cui non come dove quando anche più meno già ancora solo sia siano essere è sono stato stata stati state era erano ha hanno
aveva avere abbia abbiano questo questa questi queste quello quella quelli quelle tale tali ciò così quale quali quanto ogni altro altra
altri altre stesso stessa stessi stesse proprio propria propri proprie suo sua suoi sue loro ne ci si vi li mi ti lui lei essi esse
infatti inoltre pertanto quindi perché poiché mentre però tuttavia ovvero oppure cioè nonché né può possono deve devono va vanno viene
vengono fatto fatta parte modo caso casi senso sensi tra secondo comma art artt legge leggi cost costituzione costituzionale
costituzionali corte sentenza sentenze ordinanza ordinanze questione questioni legittimità illegittimità riferimento norma norme
disposizione disposizioni dichiarata dichiarato fondata infondata manifestamente inammissibile inammissibilità ammissibilità sollevata
proposta relazione specie nonche del n nn cfr lett ex primo secondo terzo quarto quinto sesto prima dopo sensi quale essa esso tal
dichiara ritenuto considerato denunciata impugnata impugnato censurata rimettente giudice quo cit citata""".split())


def load_massime() -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(str(REPO / "data/raw/massime/*/*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            h = p.find("pronuncia_testata")
            pid = int(h.findtext("anno_pronuncia")) * 10000 + int(h.findtext("numero_pronuncia"))
            for m in p.findall("massime/massima"):
                arts = [(x.findtext("articolo") or "").strip() for x in m.findall("parametri/parametro")
                        if "ostituzione" in (x.findtext("descrizione") or "")]
                rows.append(dict(pid=pid, titolo=(m.findtext("titolo") or "").strip(),
                                 testo=(m.findtext("testo") or "").strip(), cost_arts="|".join(a for a in arts if a)))
    return pd.DataFrame(rows)


def npmi(top_idx: np.ndarray, B) -> float:
    """Mean NPMI over pairs of top words, B = binary doc-term matrix (csc)."""
    n = B.shape[0]
    sub = B[:, top_idx]
    co = (sub.T @ sub).toarray().astype(float)
    df = np.diag(co)
    vals = []
    for i in range(len(top_idx)):
        for j in range(i + 1, len(top_idx)):
            if co[i, j] == 0:
                vals.append(-1.0)
                continue
            pij, pi, pj = co[i, j] / n, df[i] / n, df[j] / n
            vals.append(np.log(pij / (pi * pj)) / -np.log(pij))
    return float(np.mean(vals))


def fit(X, k, seed):
    return LatentDirichletAllocation(n_components=k, learning_method="online", batch_size=2048, max_iter=5,
                                     learning_offset=10.0, random_state=seed, n_jobs=4).fit(X)


def main() -> None:
    m = load_massime()
    m = m[m.testo.str.len() > 50].reset_index(drop=True)
    vec = CountVectorizer(lowercase=True, token_pattern=r"[a-zà-ù]{3,}", stop_words=list(STOP), max_df=0.5, min_df=30,
                          max_features=8000)
    X = vec.fit_transform(m.testo)
    vocab = np.array(vec.get_feature_names_out())
    B = (X > 0).astype(np.int32).tocsc()
    res = {}
    models = {}
    for k in [10, 20, 30, 40, 50, 60]:
        lda = fit(X, k, SEED)
        tops = np.argsort(-lda.components_, axis=1)[:, :10]
        res[k] = float(np.mean([npmi(t, B) for t in tops]))
        models[k] = lda
        print(k, round(res[k], 4), flush=True)
    best = max(res.values())
    # NPMI can be negative: "within 2% of the best" is taken on the range of observed values
    span = best - min(res.values())
    k_star = min(k for k, v in res.items() if v >= best - 0.02 * max(span, 1e-9) or v >= best * 0.98 > 0)
    lda = models[k_star]
    # stability: best-match Jaccard of top-20 words across 5 seeds
    ref = [set(t) for t in np.argsort(-lda.components_, axis=1)[:, :20]]
    stab = []
    for s in range(1, 5):
        other = [set(t) for t in np.argsort(-fit(X, k_star, SEED + s).components_, axis=1)[:, :20]]
        stab.append(float(np.mean([max(len(a & b) / len(a | b) for b in other) for a in ref])))
    theta_m = lda.transform(X)
    m["topic"] = theta_m.argmax(1)
    th = pd.DataFrame(theta_m).assign(pid=m.pid.values).groupby("pid").mean()
    np.savez_compressed(REPO / "data/processed/topics_theta.npz", pid=th.index.values, theta=th.values)
    pr = pd.DataFrame({"pid": th.index, "topic": th.values.argmax(1), "topic_weight": th.values.max(1),
                       "n_topics_02": (th.values >= 0.2).sum(1)})
    pr.to_csv(REPO / "data/processed/topics_pronunce.csv", index=False)
    # verification (descriptive)
    m["anno"] = m.pid // 10000
    seg = m.titolo.str.split(" - ").str[0].str.strip().str.lower()
    new = m[(m.anno >= 2015) & ~m.titolo.str.match(r"^(SENT|ORD)\.")]
    common = seg[new.index].value_counts()
    keep = new[seg[new.index].isin(common[common >= 30].index)]
    nmi_title = normalized_mutual_info_score(seg[keep.index], keep.topic)
    first_art = m.cost_arts.str.split("|").str[0]
    ka = m[first_art != ""]
    nmi_art = normalized_mutual_info_score(first_art[ka.index], ka.topic)
    rng = np.random.default_rng(SEED)
    nmi_title_null = float(np.mean([normalized_mutual_info_score(seg[keep.index], rng.permutation(keep.topic.values)) for _ in range(20)]))
    nmi_art_null = float(np.mean([normalized_mutual_info_score(first_art[ka.index], rng.permutation(ka.topic.values)) for _ in range(20)]))
    tops = np.argsort(-lda.components_, axis=1)[:, :12]
    labels = {}
    out = ["# Topic sulle massime\n", "Generato da `src/analysis/topics.py`.\n",
           f"- Massime usate: {len(m):,} (testo oltre 50 caratteri); vocabolario: {len(vocab):,} parole.",
           "- Coerenza NPMI per numero di topic: " + ", ".join(f"K={k}: {v:.4f}" for k, v in res.items()) + ".",
           f"- K scelto con la regola fissata (il più piccolo entro il 2% del migliore): **{k_star}**.",
           f"- Stabilità su 5 seed (Jaccard medio delle prime 20 parole, miglior abbinamento): {np.mean(stab):.3f} (min {min(stab):.3f}).",
           f"- Pronunce con materia: {len(pr):,}; peso medio del topic dominante {pr.topic_weight.mean():.2f}; "
           f"pronunce con più di un topic sopra 0,2: {(pr.n_topics_02 > 1).mean():.1%}.",
           f"- Verifica con i titoli delle massime (dal 2015, prime voci con almeno 30 massime, {len(keep):,} massime): "
           f"informazione mutua normalizzata {nmi_title:.3f}, contro {nmi_title_null:.3f} con topic rimescolati.",
           f"- Verifica con il primo parametro costituzionale ({len(ka):,} massime): NMI {nmi_art:.3f}, contro {nmi_art_null:.3f} rimescolando.\n",
           "| Topic | Massime | Parole più pesanti | Prima voce dei titoli più frequente (dal 2015) |", "| --- | --- | --- | --- |"]
    for k in range(k_star):
        words = ", ".join(vocab[tops[k]])
        s = seg[new.index][new.topic == k].value_counts()
        lab = s.index[0] if len(s) else ""
        labels[k] = lab
        out.append(f"| {k} | {(m.topic == k).sum():,} | {words} | {lab} |")
    (REPO / "reports/topics.md").write_text("\n".join(out), encoding="utf-8")
    json.dump({"coherence": res, "k": k_star, "stability": stab, "nmi_title": nmi_title, "nmi_art": nmi_art,
               "labels": labels, "top_words": {int(k): list(vocab[tops[k]]) for k in range(k_star)}},
              open(REPO / "reports/topics.json", "w"), ensure_ascii=False, indent=1)
    print("\n".join(out[:12]))


if __name__ == "__main__":
    main()
