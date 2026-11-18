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
md = [f"# Polarità delle citazioni: validazione ({'Claude' if WHO == 'claude' else 'controllo umano'})\n",
      "Generato da `src/polarity/evaluate.py`. Campione: tutti i contesti segnalati della metà di prova, mescolati con contesti della stessa metà "
      "che hanno una parola di distinzione ma non sono segnalati; annotati senza vedere l'etichetta. Unità: il contesto.\n",
      f"- Precisione dei contesti segnalati: **{tp} su {len(f)} = {prec:.3f}** (intervallo di Wilson {plo:.3f}–{phi:.3f}); soglia fissata prima: 0,80. "
      f"{'Superata.' if out['passed'] else 'NON superata: niente analisi.'}",
      f"- Tra i {len(nf)} contesti non segnalati che hanno una parola di distinzione, le vere distinzioni sono {miss} ({miss / len(nf):.3f}; {mlo:.3f}–{mhi:.3f}): "
      "il lessico ne perde una parte, e altre forme sfuggono del tutto. La quota trovata è un limite inferiore.\n",
      "| Regola | Contesti segnalati | Veri |", "| --- | --- | --- |"]
md += [f"| {r} | {v['n']} | {v['true']} |" for r, v in out["precision_by_rule"].items()]
if WHO == "claude":
    md.append("\nL'annotatore (Claude) ha scritto anche le regole: l'annotazione non è indipendente. Il foglio per una persona è `data/validation/polarity_human_check.md`.")
(REPO / f"reports/polarity_validation_{WHO}.md").write_text("\n".join(md), encoding="utf-8")
print(json.dumps(out, indent=1))
