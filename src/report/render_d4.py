"""Writes the text of section 3.6 (D4) of reports/relazione_for_dummies.md from reports/d4_results.json.
Usage: .venv/bin/python src/report/render_d4.py"""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[2])  # paths below are relative to the repository root
import json, re
d = json.load(open("reports/d4_results.json"))
f = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")
o, p_ = d["organo"], d["provenienza"]
pv = lambda x: f(x, 3)
txt = f"""(`reports/d4_results.json`) La potenza simulata per un effetto del 20% è {f(o['power_for_20pct'], 2)} per l'organo e {f(p_['power_for_20pct'], 2)} per la provenienza: il test si poteva fare. Le soglie erano fissate prima: un effetto minimo d'interesse del 20% e la correzione di Holm sui due test.

- **Organo di nomina** (Presidente della Repubblica, Parlamento, magistrature): le citazioni tra giudici dello stesso gruppo sono il {f(o['same_group_share']*100)}%, contro il {f(o['null_mean']*100)}% atteso ({f(o['null_lo']*100)}–{f(o['null_hi']*100)}); p = {pv(o['p'])}, {pv(o['p_holm'])} con Holm. Nessun effetto.
- **Provenienza** (professori, magistrati; gli avvocati sono solo {p_['groups'].get('avvocato', 0)}): {f(p_['same_group_share']*100)}% contro {f(p_['null_mean']*100)}% ({f(p_['null_lo']*100)}–{f(p_['null_hi']*100)}); p = {pv(p_['p'])}, {pv(p_['p_holm'])} con Holm. L'eccesso è del {f(p_['excess_over_null']*100)}%, molto sotto l'effetto minimo d'interesse: omofilia trascurabile, non una scoperta. La provenienza è codificata in automatico dalla nota biografica dell'anagrafica dei giudici."""
s = open("reports/relazione_for_dummies.md").read()
i = s.index("### 3.6 D4")
j = s.index("### 3.7", i)
head = s[i:s.index("\n", i) + 1]
s = s[:i] + head + "\n" + txt + "\n\n" + s[j:]
open("reports/relazione_for_dummies.md", "w").write(s)
print(txt)
