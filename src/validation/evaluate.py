"""Compare the extractor with the gold standard annotated by reading
(data/validation/gold_<which>.txt) and write reports/validation_<which>.md.
Unit: the pair (citing pronuncia, cited pronuncia) in the base text.
Usage: .venv/bin/python src/validation/evaluate.py test|test2|human
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
    "test": "è stato scritto da Claude, l'assistente automatico, leggendo i passi dei testi che contengono una parola chiave "
            "(come \"sentenza\" o \"ordinanza\") o un rimando (`src/validation/sample_passages.py`). Claude li ha letti prima di far "
            "girare il programma su questo campione, senza vederne il risultato. Non l'ha scritto una persona, e non copre i testi interi.",
    "human": "è stato scritto da una persona, che ha letto per intero il testo di base di ogni pronuncia "
             "(`data/validation/human_check.md`) senza vedere il risultato del programma.",
}
ANNOTATOR["test2"] = ANNOTATOR["test"]
SAMPLE_DESC = {
    "test": "Il campione è il primo campione di controllo: 4 pronunce per ogni decennio e tipo (sentenza o ordinanza), estratte a caso "
            "con il seme 20261117. Dopo la prima misura (conservata in `validation_round1.md`) il programma è stato corretto guardando "
            "gli errori di questo campione: i numeri qui sotto non sono più una stima indipendente.",
    "test2": "Il campione è il secondo campione di controllo: solo pronunce fino alla 286/1986, 6 per ogni decennio e tipo, estratte a "
             "caso con il seme 20261118 dopo la correzione del programma e mai usate per metterlo a punto.",
    "human": "Il campione è quello del controllo di una persona: da 3 pronunce per decennio e tipo negli anni 1950–1980 a 1 negli anni "
             "2010–2020 (circa 100 citazioni attese), estratte a caso con il seme 20261119, senza le pronunce dei campioni precedenti.",
}
gold = {}
unclear = 0
for line in (REPO / f"data/validation/gold_{WHICH}.txt").read_text().splitlines():
    if ":" not in line or not line.split(":")[0].strip().isdigit():
        continue  # notes at the end of the file
    pid, rest = line.split(":", 1)
    toks = rest.split()
    unclear += sum("?" in x for x in toks)  # "?/numero": year not understood by the annotator, left out
    gold[int(pid)] = {int(x.split("/")[0]) * 10000 + int(x.split("/")[1]) for x in toks if "?" not in x}
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
def fmt(x):  # Italian format: comma for decimals
    return f"{x:.3f}".replace(".", ",")
def line(d, label):
    tp, fp, fn = d.tp.sum(), d.fp.sum(), d.fn.sum()
    if len(d) == 0:
        return f"| {label} | 0 | 0 | 0 | 0 | 0 | — | — |"
    pl, ph = wilson(tp, tp + fp); rl, rh = wilson(tp, tp + fn)
    P = tp / (tp + fp) if tp + fp else float("nan"); R = tp / (tp + fn) if tp + fn else float("nan")
    return f"| {label} | {len(d)} | {tp + fn} | {tp} | {fp} | {fn} | {fmt(P)} ({fmt(pl)}–{fmt(ph)}) | {fmt(R)} ({fmt(rl)}–{fmt(rh)}) |"
def pid(x):  # internal id (year * 10000 + number) -> "year/number"
    return f"{x // 10000}/{x % 10000}"
out = ["# Controllo del programma che trova le citazioni\n",
       "Prodotto da `src/validation/evaluate.py`. Si contano le coppie \"pronuncia che cita – pronuncia citata\" trovate nel testo di base "
       "(il ragionamento della Corte e il dispositivo).\n",
       f"**Chi ha deciso quali citazioni sono vere.** L'elenco di riferimento (`data/validation/gold_{WHICH}.txt`) " + ANNOTATOR[WHICH] + "\n",
       "**Il campione.** " + SAMPLE_DESC[WHICH] + " È diverso dal campione usato per mettere a punto il programma (2 pronunce per gruppo, "
       f"seme 20261116). Chi vuole controllare a mano trova in `data/validation/gold_{WHICH}.txt`, pronuncia per pronuncia, le citazioni "
       "giudicate vere.\n",
       "**Come si legge la tabella.** \"Trovate giuste\" sono le citazioni vere che il programma ha trovato; \"trovate per errore\" quelle "
       "che ha trovato ma non sono vere; \"mancate\" quelle vere che non ha trovato. La precisione è trovate giuste diviso tutte le trovate; "
       "il richiamo è trovate giuste diviso le citazioni vere. Tra parentesi c'è l'intervallo di confidenza al 95%, calcolato con il metodo "
       "di Wilson: i valori compatibili con i dati." + (f" Citazioni scritte nell'elenco senza un anno riconoscibile, lasciate fuori dal "
       f"calcolo: {unclear}." if unclear else "") + "\n",
       "| Gruppo | Pronunce | Citazioni vere | Trovate giuste | Trovate per errore | Mancate | Precisione | Richiamo |",
       "| --- | --- | --- | --- | --- | --- | --- | --- |",
       line(r, "**Totale**")]
for t in ["S", "O"]: out.append(line(r[r.tipo == t], {"S": "Sentenze", "O": "Ordinanze"}[t]))
for dec in sorted(r.decade.unique()): out.append(line(r[r.decade == dec], f"Anni {dec}"))
for lab, d in [("Fino alla 286/1986", r[r.pid < 19860287]), ("Dalla 287/1986 in poi", r[r.pid >= 19860287])]: out.append(line(d, lab))
out += ["", "Ogni riga degli elenchi qui sotto si legge così: la pronuncia a sinistra (anno/numero) cita quella a destra."]
out += ["", "## Citazioni trovate per errore (trovate dal programma, ma non nell'elenco di riferimento)", ""] + [f"- {pid(a)} → {pid(b)}" for a, b in fp_list]
if not fp_list: out.append("Nessuna.")
out += ["", "## Citazioni mancate (nell'elenco di riferimento, ma non trovate dal programma)", ""] + [f"- {pid(a)} → {pid(b)}" for a, b in fn_list]
if not fn_list: out.append("Nessuna.")
(REPO / f"reports/validation_{WHICH}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[5:20])); print("FP", fp_list); print("FN", fn_list)
