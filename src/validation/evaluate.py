"""Compare the extractor with the gold standard annotated by reading
(data/validation/gold_test.txt) and write reports/validation.md.
Unit: the pair (citing pronuncia, cited pronuncia) in the base text.
Usage: .venv/bin/python src/validation/evaluate.py
"""
import math, sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[2]

def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

WHICH = sys.argv[1] if len(sys.argv) > 1 else "test"
ANNOTATOR = {
    "test": "è stata fatta da Claude leggendo i passi dei testi che contengono una parola chiave o un richiamo "
            "(`src/validation/sample_passages.py`), prima di eseguire l'estrattore su questo campione e senza vederne il risultato. "
            "Non è un'annotazione umana, e non copre i testi interi.",
    "human": "è stata fatta da una persona leggendo per intero il testo di base di ogni pronuncia "
             "(`data/validation/human_check.md`), senza vedere il risultato dell'estrattore.",
}
ANNOTATOR["test2"] = ANNOTATOR["test"]
SAMPLE_DESC = {
    "test": "Campione: primo campione di verifica, 4 pronunce per decennio e tipo, seed 20261117. Dopo la prima misura "
            "(conservata in `validation_round1.md`) l'estrattore è stato corretto guardando gli errori di questo campione: "
            "i numeri qui sotto non sono più una stima indipendente.",
    "test2": "Campione: secondo campione di verifica, solo pronunce fino alla 286/1986, 6 per decennio e tipo, seed 20261118, "
             "estratto dopo la correzione dell'estrattore e mai usato per metterlo a punto.",
    "human": "Campione: controllo umano, da 3 pronunce per decennio e tipo negli anni 1950–1980 a 1 negli anni 2010–2020 "
             "(circa 100 coppie attese), seed 20261119, escluse le pronunce dei campioni precedenti.",
}
gold = {}
for line in (REPO / f"data/validation/gold_{WHICH}.txt").read_text().splitlines():
    pid, rest = line.split(":")
    gold[int(pid)] = {int(x.split("/")[0]) * 10000 + int(x.split("/")[1]) for x in rest.split()}
c = pd.read_csv(REPO / "data/processed/citations.csv")
c = c[c.section.isin(["diritto", "dispositivo"]) & c.citing_id.isin(gold)]
pred = c.groupby("citing_id").cited_id.apply(set).to_dict()
meta = pd.read_csv(REPO / "data/processed/pronunce.csv").set_index("pid")
rows, fp_list, fn_list = [], [], []
for pid, g in gold.items():
    p = pred.get(pid, set())
    rows.append(dict(pid=pid, decade=meta.anno[pid] // 10 * 10, tipo=meta.tipo[pid], tp=len(g & p), fp=len(p - g), fn=len(g - p)))
    fp_list += [(pid, x) for x in sorted(p - g)]; fn_list += [(pid, x) for x in sorted(g - p)]
r = pd.DataFrame(rows)
def line(d, label):
    tp, fp, fn = d.tp.sum(), d.fp.sum(), d.fn.sum()
    pl, ph = wilson(tp, tp + fp); rl, rh = wilson(tp, tp + fn)
    P = tp / (tp + fp) if tp + fp else float("nan"); R = tp / (tp + fn) if tp + fn else float("nan")
    return f"| {label} | {len(d)} | {tp + fn} | {tp} | {fp} | {fn} | {P:.3f} ({pl:.3f}–{ph:.3f}) | {R:.3f} ({rl:.3f}–{rh:.3f}) |"
out = ["# Validazione dell'estrazione delle citazioni\n",
       "Generato da `src/validation/evaluate.py`. Unità: la coppia (pronuncia che cita, pronuncia citata) nel testo di base.\n",
       f"**Chi ha annotato.** L'annotazione di riferimento (`data/validation/gold_{WHICH}.txt`) " + ANNOTATOR[WHICH] + " "
       + SAMPLE_DESC[WHICH] + " È separato "
       "da quello usato per mettere a punto l'estrattore (2 per strato, seed 20261116). Per il controllo a campione di una persona: "
       f"`data/validation/gold_{WHICH}.txt` elenca per ogni pronuncia le citazioni annotate.\n",
       "Intervalli di confidenza al 95% di Wilson.\n",
       "| Strato | Pronunce | Coppie vere | Trovate | False | Mancate | Precisione | Richiamo |", "| --- | --- | --- | --- | --- | --- | --- | --- |",
       line(r, "**Totale**")]
for t in ["S", "O"]: out.append(line(r[r.tipo == t], {"S": "Sentenze", "O": "Ordinanze"}[t]))
for dec in sorted(r.decade.unique()): out.append(line(r[r.decade == dec], f"Anni {dec}"))
for lab, d in [("1956–1986", r[r.pid < 19860287]), ("1987–2026", r[r.pid >= 19860287])]: out.append(line(d, lab))
out += ["", "## Coppie false (trovate dall'estrattore, assenti nell'annotazione)", ""] + [f"- {a} → {b // 10000}/{b % 10000}" for a, b in fp_list]
out += ["", "## Coppie mancate (annotate, non trovate dall'estrattore)", ""] + [f"- {a} → {b // 10000}/{b % 10000}" for a, b in fn_list]
(REPO / f"reports/validation_{WHICH}.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[5:20])); print("FP", fp_list); print("FN", fn_list)
