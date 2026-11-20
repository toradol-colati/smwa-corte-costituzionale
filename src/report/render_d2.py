"""Writes section 3.5 (D2) of reports/relazione_for_dummies.md and summary item 4 from reports/d2_results.json and
reports/d2_strata_check.json. Usage: .venv/bin/python src/report/render_d2.py"""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[2])  # paths below are relative to the repository root
import json, re, sys
d = json.load(open("reports/d2_results.json"))
import csv
SUR = {int(r["judge_id"]): r["surname"].title() for r in csv.DictReader(open("data/processed/judges.csv"))}
f = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
def p(x):
    return "< 0,001" if x < 0.001 else "= " + f(x, 3)
a, at, am, a87, pre = d["permutazione_anno"], d["permutazione_anno_tipo"], d["permutazione_anno_tipo_materia"], d["permutazione_anno_dal_1987"], d["nullo_preregistrato"]
ap = d.get("permutazione_anno_tipo_parametro")
sc = json.load(open("reports/d2_strata_check.json"))
win = d["window_years"]
cit = f"le citazioni che ricevono, nei {win} anni dal deposito, le pronunce che ha redatto" if win else "le citazioni ricevute dalle pronunce che ha redatto"
top = a["table"][:3]
tt = ", ".join(f"{SUR[r['judge_id']]} ({f(r['rapporto'])}; {f(r['lo'])}–{f(r['hi'])})" for r in top)
pm, pmm = a["post_mandate"], am["post_mandate"]
sec = f"""### 3.5 D2 — Pochi redattori si distinguono (esplorativo)

(`reports/d2_results.json`)

**Come si misura.** Per ogni giudice: {cit}, escluse le autocitazioni, divise per quelle attese. L'atteso e la variabilità vengono dal rimescolamento dei redattori: le pronunce di ogni anno si riassegnano a caso tra i redattori di quell'anno, e ogni pronuncia porta con sé le citazioni che ha davvero ricevuto da pronunce di altri redattori. {str(f"{d['permutations']:,}").replace(',', '.')} rimescolamenti; i valori p vengono dal loro conteggio.

- Su {a['judges_tested']} giudici con almeno {d['min_pronunce']} pronunce, dopo la correzione di Holm le pronunce di **{a['sig_holm_above']}** sono citate più dell'atteso e quelle di **{a['sig_holm_below']}** meno; per gli altri la differenza non si distingue dal caso (Figura 9).
- Le differenze tra giudici sono comunque più ampie di quelle dei rimescolamenti: la varianza del logaritmo del rapporto è {f(a['var_ratio_to_null'], 1)} volte quella attesa (p {p(a['p_heterogeneity'])}).
- In testa: {tt}; l'atteso è 1.
- Tenendo conto anche del tipo di pronuncia, {at['sig_holm_above']} sopra e {at['sig_holm_below']} sotto; anche della materia, {am['sig_holm_above']} e {am['sig_holm_below']}; anche dell'articolo della Costituzione invocato più spesso (variante esplorativa del 19/11), {ap['sig_holm_above']} e {ap['sig_holm_below']}. Con le sole pronunce dalla 287/1986, dove il redattore è osservato, {a87['sig_holm_above']} e {a87['sig_holm_below']} su {a87['judges_tested']} giudici.
- **Dopo il mandato.** Per gli {pm['judges']} giudici usciti entro il 2015, chi era citato più dell'atteso in carica lo è anche nei dieci anni successivi: correlazione tra ranghi {f(pm['spearman_during_post'])}. Una parte è meccanica, perché le stesse pronunce restano citate: con pronunce prese a caso dello stesso anno la correlazione sarebbe {f(pm['spearman_null_mean'])} (95%: {f(pm['spearman_null_lo'])}–{f(pm['spearman_null_hi'])}). Il dato osservato sta sopra (p {p(pm['p_above_null'])}); a parità anche di tipo e materia, {f(pmm['spearman_during_post'])} contro {f(pmm['spearman_null_mean'])} ({f(pmm['spearman_null_lo'])}–{f(pmm['spearman_null_hi'])}) (Figura 10). Con la variante per articolo della Costituzione la correlazione è {f(ap['post_mandate']['spearman_during_post'])} e resta dentro quella attesa ({f(ap['post_mandate']['spearman_null_mean'])}; {f(ap['post_mandate']['spearman_null_lo'])}–{f(ap['post_mandate']['spearman_null_hi'])}). Quella variante separa giudice e materia solo in parte: il {f(sc['anno_tipo_parametro']['share_tested_pronunce_in_mixed_strata'] * 100, 1)}% delle pronunce dei giudici testati sta in gruppi con almeno due redattori diversi, il resto non si può scambiare e spinge i rapporti verso 1 (`reports/d2_strata_check.json`). La persistenza dopo il mandato resta quindi incerta.

![Figura 9](figures/fig9_d2_giudici.png)

*Figura 9. Rapporto tra citazioni osservate e attese per le pronunce redatte da ciascun giudice, con l'intervallo al 95% ottenuto ricampionando le sue pronunce. In blu i giudici che si distinguono dal caso dopo la correzione di Holm.*

![Figura 10](figures/fig10_d2_dopo_mandato.png)

*Figura 10. Rapporto tra citazioni osservate e attese durante il mandato e nei dieci anni dopo, per i giudici usciti entro il 2015.*

**Perché D2 è esplorativo.** Il modello nullo fissato prima (ogni citazione ripescata a caso tra le pronunce dello stesso anno) dà lo stesso atteso, ma ignora quanto diversamente sono citate le pronunce: con quel nullo i giudici fuori dall'atteso erano {pre['age_only']['sig_holm_above']} e {pre['age_only']['sig_holm_below']}, con una dispersione {f(pre['age_only']['var_ratio_to_null'], 0)} volte il caso. Passare al rimescolamento dei redattori è il secondo cambiamento fatto in D2 dopo aver visto i risultati (il primo, i valori p dalle deviazioni standard, è ora superato): per questo D2 va letto come esplorativo. Entrambi i nulli restano nel file dei risultati.

Resta il limite della materia: i topic sono grossolani, e i redattori non sono assegnati a caso.

"""
s = open("reports/relazione_for_dummies.md").read()
i, j = s.index("### 3.5 D2"), s.index("### 3.6 D4")
s = s[:i] + sec + s[j:]
summary = (f"4. **Pochi redattori si distinguono.** Su {a['judges_tested']} giudici, dopo la correzione di Holm le pronunce di {a['sig_holm_above']} sono citate più "
           f"di pronunce prese a caso dello stesso anno e quelle di {a['sig_holm_below']} meno. Esplorativo.")
s = re.sub(r"^4\. \*\*[^\n]*$", summary, s, count=1, flags=re.M)
open("reports/relazione_for_dummies.md", "w").write(s)
print(summary)
