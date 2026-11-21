"""Validation of the polarity rules on the blind test sample (src/polarity/draw_sample.py).
Gold: data/validation/gold_polarity_<who>.txt, lines "<item>: 1|0" (1 = the Court distinguishes or
departs from the precedent between ⟦ ⟧). Threshold fixed before the test: precision of the flagged
contexts >= 0.80. Recall is not measurable; the share of distinctions among the not-flagged contexts
that contain a distinguishing word is reported as a sign of what the rules miss.
Output: reports/polarity_validation_<who>.md, reports/polarity_validation_<who>.json
Usage: .venv/bin/python src/polarity/evaluate.py claude|human
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
WHO = sys.argv[1] if len(sys.argv) > 1 else "claude"


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


lab = pd.read_csv(REPO / "data/validation/polarity_test_labels.csv")
gold = {}
for line in (REPO / f"data/validation/gold_polarity_{WHO}.txt").read_text().splitlines():
    k, _, v = line.partition(":")
    if k.strip().isdigit() and v.strip() in ("0", "1"):
        gold[int(k)] = int(v)
# the gold is keyed by item number; the versioned sample ties every item to its context
smp = pd.read_csv(REPO / "data/validation/polarity_test_sample.csv")
assert (smp.set_index("item").context_id == lab.set_index("item").context_id).all(), "sample and labels are misaligned"
t = lab[lab.item.isin(gold)].assign(true=lambda d: d.item.map(gold))
f, nf = t[t.flagged == 1], t[t.flagged == 0]
tp = int(f.true.sum())
prec, (plo, phi) = tp / len(f), wilson(tp, len(f))
miss = int(nf.true.sum())
mlo, mhi = wilson(miss, len(nf))
out = {"annotator": WHO, "items": int(len(t)), "flagged": int(len(f)), "flagged_true": tp, "precision": prec, "precision_lo": plo, "precision_hi": phi,
       "threshold": 0.80, "passed": bool(prec >= 0.80), "not_flagged": int(len(nf)), "not_flagged_true": miss,
       "not_flagged_true_share": miss / len(nf) if len(nf) else float("nan"), "not_flagged_true_lo": mlo, "not_flagged_true_hi": mhi,
       "precision_by_rule": {r: {"n": int(len(g)), "true": int(g.true.sum())} for r, g in f.groupby("rule")}}
json.dump(out, open(REPO / f"reports/polarity_validation_{WHO}.json", "w"), indent=1)
RULE_LABELS = {  # what each rule looks for (src/polarity/lexicon.py)
    "caso_diverso": "il caso di oggi è diverso da quello deciso allora (\"a differenza di quanto deciso\", \"non è assimilabile a quella esaminata\")",
    "non_affermato": "il precedente non ha detto quello che gli si attribuisce (\"la sentenza non ha affermato\")",
    "non_pertinente": "il richiamo al precedente non è pertinente (\"il richiamo non è conferente\")",
    "superamento": "la Corte cambia orientamento (\"superare il precedente\", \"mutamento di giurisprudenza\")",
}


def it(x):  # Italian format: comma for decimals
    return f"{x:.3f}".replace(".", ",")


md = [f"# Le citazioni in cui la Corte prende le distanze da un precedente: controllo delle regole "
      f"({'letto da Claude' if WHO == 'claude' else 'letto da una persona'})\n",
      "Prodotto da `src/polarity/evaluate.py`. Le regole cercano nel testo, intorno a una citazione, le frasi con cui la Corte dice che un "
      "proprio precedente non si applica o non va seguito (`src/polarity/lexicon.py`). Ogni passo controllato è il pezzo di testo intorno a "
      "una citazione (il \"contesto\").\n",
      "**Il campione.** Tutti i passi segnalati dalle regole nella metà dei dati tenuta da parte per la prova, mescolati con passi della "
      "stessa metà che contengono una parola tipica delle distinzioni ma che le regole non hanno segnalato. Chi ha letto i passi non sapeva "
      "quali erano stati segnalati.\n",
      f"- **Precisione** (quanti dei passi segnalati sono davvero distinzioni): **{tp} su {len(f)} = {it(prec)}**; intervallo al 95%, "
      f"calcolato con il metodo di Wilson: {it(plo)}–{it(phi)}. La soglia decisa prima era 0,80: "
      f"{'superata.' if out['passed'] else 'non superata, quindi le regole non sono state usate nelle analisi.'}",
      f"- Tra i {len(nf)} passi non segnalati che contengono una parola tipica delle distinzioni, le vere distinzioni sono {miss} "
      f"({it(miss / len(nf))}; intervallo {it(mlo)}–{it(mhi)}). Quindi le regole ne perdono una parte; e altre distinzioni, scritte senza "
      "quelle parole, sfuggono del tutto. Quante distinzioni le regole perdono davvero non si può misurare: questo numero dà solo un minimo.\n",
      "**I passi segnalati, regola per regola**\n",
      "| Regola | Che cosa cerca | Passi segnalati | Di cui distinzioni vere |", "| --- | --- | --- | --- |"]
md += [f"| `{r}` | {RULE_LABELS.get(r, '')} | {v['n']} | {v['true']} |" for r, v in out["precision_by_rule"].items()]
if WHO == "claude":
    md.append("\n**Attenzione.** Chi ha letto i passi (Claude) aveva anche scritto le regole: il controllo non è indipendente. Il foglio "
              "per il controllo di una persona è `data/validation/polarity_human_check.md`.")
(REPO / f"reports/polarity_validation_{WHO}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(json.dumps(out, indent=1))
