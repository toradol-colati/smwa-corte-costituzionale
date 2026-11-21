"""Topic model (LDA) on the texts of the massime, to obtain the subject matter of
each pronuncia. Rules fixed in docs/spec.md (Modelli nulli, point 8):
  - K in 10..60 step 10; choose the smallest K whose coherence is within 2% of the best
    (NPMI on document co-occurrence of the top-10 words; see docs/decisions.md);
  - stability over 5 seeds;
  - pronuncia = simple mean of its massime; subject = topic with the highest mean weight.

Outputs: data/processed/topics_theta.npz (pid, theta), data/processed/topics_pronunce.csv,
reports/topics.md, reports/topics.json
Usage: .venv/bin/python src/analysis/topics.py               (fit, slow)
       .venv/bin/python src/analysis/topics.py --labels-only (labels from the saved fit)
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


def specific_labels(pr_topic: pd.Series, m: pd.DataFrame, min_count: int = 15, min_share: float = 0.10) -> dict:
    """Label of each topic from the first heading of the massime titles (format used from 2015).
    Each massima takes the dominant topic of its pronuncia. The label is the heading most
    over-represented in the topic (lift = share in the topic / share overall) among headings with at
    least min_count massime and at least min_share of the topic's massime; otherwise no label. The most frequent heading is not used: the commonest
    headings overall ("bilancio e contabilita' pubblica", "thema decidendum") would win everywhere."""
    x = m[(m.pid // 10000 >= 2015) & ~m.titolo.str.match(r"^(SENT|ORD)\.")].copy()
    x["head"] = x.titolo.str.split(" - ").str[0].str.strip().str.lower()
    x["topic"] = x.pid.map(pr_topic)
    x = x.dropna(subset=["topic"])
    overall = x["head"].value_counts(normalize=True)
    labels = {}
    for k, g in x.groupby("topic"):
        c = g["head"].value_counts()
        c = c[(c >= min_count) & (c / len(g) >= min_share)]
        if c.empty:
            labels[int(k)] = {"label": "", "share_in_topic": 0.0, "lift": 0.0, "massime": int(len(g))}
            continue
        lift = (c / len(g)) / overall[c.index]
        h = lift.idxmax()
        labels[int(k)] = {"label": h, "share_in_topic": float(c[h] / len(g)), "lift": float(lift[h]), "massime": int(len(g))}
    return labels


TABLE_HEAD = "| Tema | Massime | Parole che pesano di più | Voce dei titoli più tipica del tema (dal 2015): quota nel tema, volte la media |"
NO_LABEL = "nessuna voce arriva al 10% delle massime del tema"


def it(x, d):  # Italian format: comma for decimals
    return f"{x:.{d}f}".replace(".", ",")


def thousands(x):  # Italian format: dot for thousands
    return f"{x:,}".replace(",", ".")


def label_text(v):
    if not v["label"]:
        return NO_LABEL
    return f"{v['label']}: {v['share_in_topic']:.0%}, {it(v['lift'], 1)} volte la media"


def render_md(st, rows):
    """st: numbers computed in main(); rows: (topic, n massime, top words, label text). Returns the report text."""
    coh = "; ".join(f"{k} temi: {it(v, 4)}" for k, v in st["coherence"].items())
    out = ["# La materia delle pronunce, ricavata dalle massime\n",
           "Prodotto da `src/analysis/topics.py`. Per sapere di che cosa parla ogni pronuncia, un programma (un modello LDA) legge i "
           "testi delle massime e raggruppa in temi le parole che compaiono spesso insieme. Ogni massima riceve un peso per ogni tema; la "
           "materia di una pronuncia è la media dei pesi delle sue massime.\n",
           "## I numeri principali\n",
           f"- **Che cosa è stato letto.** {thousands(st['n_massime'])} massime, quelle con un testo di più di 50 caratteri. Parole "
           f"considerate: {thousands(st['n_vocab'])}, tolte quelle troppo comuni o troppo rare.",
           f"- **Quanti temi.** Il programma è stato provato con {', '.join(map(str, st['coherence']))} temi. Per ogni prova si misura "
           "quanto le parole principali di ogni tema compaiono davvero insieme nelle massime (la \"coerenza\", misurata con l'NPMI: più "
           f"è alta, meglio è): {coh}. La regola, decisa prima, sceglie il numero più piccolo con una coerenza entro il 2% della migliore: "
           f"**{st['k']} temi**.",
           f"- **Quanto sono stabili i temi.** Il calcolo è stato rifatto partendo da altri {len(st['stability'])} punti di partenza "
           "casuali (semi). Ogni tema è stato confrontato con il tema più simile del nuovo calcolo, guardando le prime 20 parole "
           "(indice di Jaccard: 1 vuol dire le stesse parole, 0 nessuna in comune). In media l'indice vale "
           f"{it(sum(st['stability']) / len(st['stability']), 3)}, al minimo {it(min(st['stability']), 3)}: ripetendo il calcolo "
           "i temi cambiano parecchio.",
           f"- **Le pronunce.** Pronunce con una materia: {thousands(st['n_pronunce'])}. In media il tema principale pesa "
           f"{it(st['mean_weight'], 2)}; il {it(100 * st['share_multi'], 1)}% delle pronunce ha più di un tema con un peso di almeno 0,2.",
           "- **Controllo con i titoli delle massime.** Dal 2015 il titolo di ogni massima comincia con una voce di classificazione "
           f"(per esempio \"reati e pene\"). Sulle {thousands(st['n_title'])} massime con una voce che compare almeno 30 volte, temi e "
           f"voci vanno d'accordo con un valore di {it(st['nmi_title'], 3)} (informazione mutua normalizzata: 0 nessun legame, 1 "
           f"corrispondenza perfetta), contro {it(st['nmi_title_null'], 3)} se i temi vengono rimescolati a caso.",
           f"- **Controllo con gli articoli della Costituzione.** Con il primo articolo della Costituzione invocato nella massima "
           f"({thousands(st['n_art'])} massime): {it(st['nmi_art'], 3)}, contro {it(st['nmi_art_null'], 3)} rimescolando.\n",
           "## I temi\n",
           "Per ogni tema: quante massime lo hanno come tema principale; le 12 parole che pesano di più, scritte come le legge il "
           "programma (a volte senza accenti, come \"puo\" e \"gia\", e con le abbreviazioni dei testi, come \"lgs\" per decreto "
           "legislativo e \"cod\" per codice); la voce dei titoli delle massime più tipica del tema. \"Quota nel tema\" è la parte delle massime del tema che hanno "
           "quella voce; \"volte la media\" dice quanto la voce è più frequente nel tema che in tutte le massime.\n",
           TABLE_HEAD, "| --- | --- | --- | --- |"]
    out += [f"| {k} | {thousands(n)} | {words} | {txt} |" for k, n, words, txt in rows]
    return "\n".join(out) + "\n"


def labels_only() -> None:
    """Recompute the labels from the saved topic assignment, without refitting the model."""
    m = load_massime()
    pr = pd.read_csv(REPO / "data/processed/topics_pronunce.csv").set_index("pid").topic
    lab = specific_labels(pr, m)
    tj = json.load(open(REPO / "reports/topics.json"))
    tj["labels"] = {str(k): v["label"] for k, v in lab.items()}
    tj["label_details"] = {str(k): v for k, v in lab.items()}
    tj["label_rule"] = "most specific first heading of the massime titles from 2015 (lift), with at least 15 massime and 10% of the topic"
    json.dump(tj, open(REPO / "reports/topics.json", "w"), ensure_ascii=False, indent=1)
    md = (REPO / "reports/topics.md").read_text(encoding="utf-8").splitlines()
    out = []
    for line in md:
        cells = line.split(" | ")
        if line.startswith("| Tema |"):
            line = TABLE_HEAD
        elif line.startswith("| ") and cells[0][2:].strip().isdigit():
            k = int(cells[0][2:].strip())
            line = " | ".join(cells[:3]) + f" | {label_text(lab.get(k, {'label': ''}))} |"
        out.append(line)
    (REPO / "reports/topics.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print({k: (v["label"], round(v["share_in_topic"], 2), round(v["lift"], 1)) for k, v in lab.items()})


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
    spec = specific_labels(pr.set_index("pid").topic, m)
    rows = []
    for k in range(k_star):
        v = spec.get(k, {"label": "", "share_in_topic": 0, "lift": 0})
        labels[k] = v["label"]
        rows.append((k, int((m.topic == k).sum()), ", ".join(vocab[tops[k]]), label_text(v)))
    st = {"n_massime": len(m), "n_vocab": len(vocab), "coherence": res, "k": k_star, "stability": stab,
          "n_pronunce": len(pr), "mean_weight": pr.topic_weight.mean(), "share_multi": (pr.n_topics_02 > 1).mean(),
          "n_title": len(keep), "nmi_title": nmi_title, "nmi_title_null": nmi_title_null,
          "n_art": len(ka), "nmi_art": nmi_art, "nmi_art_null": nmi_art_null}
    (REPO / "reports/topics.md").write_text(render_md(st, rows), encoding="utf-8")
    json.dump({"coherence": res, "k": k_star, "stability": stab, "nmi_title": nmi_title, "nmi_art": nmi_art,
               "labels": labels, "top_words": {int(k): list(vocab[tops[k]]) for k in range(k_star)}},
              open(REPO / "reports/topics.json", "w"), ensure_ascii=False, indent=1)
    print("\n".join(out[:12]))


if __name__ == "__main__":
    import sys
    labels_only() if "--labels-only" in sys.argv else main()
