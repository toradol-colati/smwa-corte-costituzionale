"""Test sample for the polarity rules (frozen in commit c9ae7b7, docs/decisions.md 18/11/2026):
all flagged contexts of the test half of the citing pronunce, shuffled with 30 test-half contexts that
contain a distinguishing word but are not flagged. One mention per context, shown between ⟦ ⟧.
The labels are written to a separate file, so that the annotator does not see them.
Outputs: data/validation/polarity_test_sample.csv (no labels), data/validation/polarity_test_labels.csv,
data/validation/polarity_human_check.md, data/validation/gold_polarity_human.txt (template)
Usage: .venv/bin/python src/polarity/draw_sample.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/polarity"))
from lexicon import classify  # noqa: E402

SEED_SPLIT, SEED_SAMPLE = 20261121, 20261122
RAW = (r"diversamente d[ae]|a differenza d|contrariamente a|non (?:è|sono|appare|appaiono|risulta|risultano) (?:pertinent|conferent)|"
       r"inconferent|non pertinent|non conferent|non giova|divers[aeio] (?:fattispecie|situazion|question|ipotes|disciplin|vicend)|"
       r"non (?:è|sono) (?:sovrapponibil|assimilabil|comparabil|analog|equiparabil)|si distingu|discost|superament|rimedit|revirement|"
       r"non (?:ha|hanno) (?:affermato|inteso|stabilito)|non costituisce un precedente|conforto")
if (REPO / "data/validation/polarity_test_labels.csv").exists() and "--force" not in sys.argv:
    sys.exit("The test sample already exists and has been annotated: redrawing it would misalign the gold files. "
             "A new version of the rules needs new data (docs/decisions.md, 18/11/2026).")
x = pd.read_pickle(REPO / "data/interim/polarity_contexts.pkl")
pids = np.sort(x.citing_id.unique())
dev = set(np.random.default_rng(SEED_SPLIT).permutation(pids)[: len(pids) // 2])
x = x[~x.citing_id.isin(dev)].copy()
x["rule"] = [classify(b, m, a) for b, m, a in zip(x.before, x.mention, x.after)]
near = (x.before.str[-150:] + " ⟦M⟧ " + x.after.str[:150]).str.lower()
x["raw"] = near.str.contains(RAW)
flag = x[x.rule.notna()].drop_duplicates("context_id")
flagged_ctx = set(flag.context_id)
miss = x[x.raw & x.rule.isna() & ~x.context_id.isin(flagged_ctx)].drop_duplicates("context_id")
miss = miss.sample(min(30, len(miss)), random_state=SEED_SAMPLE)
s = pd.concat([flag.assign(flagged=1), miss.assign(flagged=0)]).sample(frac=1, random_state=SEED_SAMPLE).reset_index(drop=True)
s["item"] = np.arange(1, len(s) + 1)
s["text"] = (s.before.str[-220:] + " ⟦" + s.mention + "⟧ " + s.after.str[:160]).str.replace("\n", " ")
s[["item", "context_id", "citing_id", "cited_id", "text"]].to_csv(REPO / "data/validation/polarity_test_sample.csv", index=False)
s[["item", "context_id", "flagged", "rule"]].to_csv(REPO / "data/validation/polarity_test_labels.csv", index=False)
head = ["# Il controllo a mano della polarità delle citazioni\n",
        "**A che cosa serve.** Un elenco di regole cerca le citazioni in cui la Corte prende le distanze da un proprio precedente. "
        "Per sapere quanto le regole sbagliano, una persona legge un campione di passi senza sapere che cosa hanno deciso le regole. "
        f"Questo foglio contiene {len(s)} passi, mescolati a caso: alcuni segnalati dalle regole, altri no.\n",
        "**Che cosa fare.** Per ogni passo, la domanda è: **la pronuncia che cita dice che il precedente tra ⟦ ⟧ non è pertinente, che "
        "riguardava un caso diverso, che non è un precedente sulla stessa questione, che non ha affermato ciò che gli si attribuisce, oppure "
        "che è superato?** Scrivere 1 (sì) o 0 (no) in `data/validation/gold_polarity_human.txt`, accanto al numero del passo. Se a prendere "
        "le distanze dal precedente sono il giudice che ha sollevato la questione o una delle parti, e non la Corte, la risposta è 0.\n",
        "Alla fine il comando `.venv/bin/python src/polarity/evaluate.py human` calcola la precisione. Serve solo come verifica: per una "
        "regola decisa prima, non cambia l'esito già misurato.\n"]
body = [f"\n**{r.item}** ({r.citing_id}) … {r.text} …\n" for r in s.itertuples()]
(REPO / "data/validation/polarity_human_check.md").write_text("\n".join(head + body), encoding="utf-8")
gold = REPO / "data/validation/gold_polarity_human.txt"
if not gold.exists():
    gold.write_text("".join(f"{i}:\n" for i in s.item), encoding="utf-8")
print(len(s), "items:", int(s.flagged.sum()), "flagged,", int((1 - s.flagged).sum()), "not flagged")
