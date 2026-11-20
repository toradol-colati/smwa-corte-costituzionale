"""Writes the paragraphs on the full model of section 3.4 (D3) and the matching row of the limits table of
reports/relazione_for_dummies.md from reports/d3_full_check.json, following the reading rule fixed beforehand in
docs/decisions.md. Usage: .venv/bin/python src/report/render_d3_full.py"""
import os
from pathlib import Path as _P
os.chdir(_P(__file__).resolve().parents[2])  # paths below are relative to the repository root
import json
from pathlib import Path
f = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
ci = lambda c: f"{f(c['lo'])}–{f(c['hi'])}"
d = json.load(open("reports/d3_full_check.json"))
H = d["half_threshold"]
b, v1, v4 = d["baseline"], d["v1_fine_young_ages"], d["v4_norme_param"]
p1, p2 = d["v2_period"]["fino al 2000"], d["v2_period"]["dal 2001"]
so, oo = d["v3_type"]["sentenze"], d["v3_type"]["ordinanze"]
seeds = [d["v5_seeds"][k]["sat_not_drafted"]["or"] for k in ["seed+1", "seed+2"]]
others = [b, v1, p1, p2, so, oo] + [d["v5_seeds"][k] for k in ["seed+1", "seed+2"]]
assert all(m["converged"] for m in others), "a model of the check did not converge"
models = others + ([v4] if v4["converged"] else [])
ratios = [m["ratio_present_absent"] for m in models]
all_include_1 = all(r["lo"] < 1 < r["hi"] for r in ratios)
loc = lambda a, c: (a["sat_not_drafted"]["or"] >= H and c["sat_not_drafted"]["hi"] < 1)
period_loc, type_loc = loc(p2, p1), loc(so, oo)
s = lambda m: m["sat_not_drafted"]
old_p = ("Nel modello completo, che usa anche la soglia del giuramento, i precedenti decisi durante il mandato del redattore quando sedeva sono citati meno di quelli "
         "della stessa età decisi prima del suo arrivo (0,88; 0,80–0,96); quando era assente la stima è la stessa, con un intervallo più largo (0,88; 0,77–1,01). "
         "Presenza e assenza, di nuovo, non differiscono.")
new_p = (old_p[:-1] + f": il rapporto tra le due stime, con l'intervallo calcolato dalla covarianza completa, è {f(b['ratio_present_absent']['or'])} "
         f"({ci(b['ratio_present_absent'])}) (`reports/d3_full_check.json`).\n\n"
         "**Da dove viene il 0,88** (esplorativo; varianti, regola di lettura e regola di arresto fissate prima delle stime, `src/analysis/d3_full_check.py`). "
         "Dentro una pronuncia che cita, \"deciso durante il mandato\" vuol dire \"più giovane dell'anzianità del redattore\": il coefficiente si stima solo perché "
         "il modello assume la stessa curva dell'età per redattori di anzianità diversa. ")
if v1["reaches_half"]:
    new_p += f"Con classi di età trimestrali nei primi due anni, dove la frequenza di citazione cresce fino al picco di un anno, la stima sale a {f(s(v1)['or'])} ({ci(s(v1))}): il 0,88 dipende dalle classi di età troppo larghe. "
else:
    new_p += f"Con classi di età trimestrali nei primi due anni, dove la frequenza di citazione cresce fino al picco di un anno, la stima non si sposta ({f(s(v1)['or'])}; {ci(s(v1))}). "
parts = []
if period_loc:
    parts.append(f"più marcato nelle pronunce che citano fino al 2000 ({f(s(p1)['or'])}; {ci(s(p1))}) che in quelle dal 2001 ({f(s(p2)['or'])}; {ci(s(p2))})")
if type_loc:
    parts.append(f"più marcato nelle ordinanze che citano ({f(s(oo)['or'])}; {ci(s(oo))}) che nelle sentenze ({f(s(so)['or'])}; {ci(s(so))})")
if parts:
    overl = lambda a, c: s(a)["lo"] <= s(c)["hi"] and s(c)["lo"] <= s(a)["hi"]
    both_overlap = (not period_loc or overl(p1, p2)) and (not type_loc or overl(oo, so))
    new_p += ("Il deficit è invece " + "; ed è ".join(parts) + ". La regola fissata prima chiama questo \"localizzato\", ma non prevede un test "
              "della differenza tra i gruppi" + (", e gli intervalli si sovrappongono: è una descrizione, non una prova. " if both_overlap else ". "))
    if period_loc and type_loc:
        new_p += "È lo stesso profilo dell'effetto \"l'ha redatto lui\", più forte nelle ordinanze e prima del 2001. "
else:
    new_p += (f"Non si concentra in un periodo (fino al 2000 {f(s(p1)['or'])}, dal 2001 {f(s(p2)['or'])}) né in un tipo di pronuncia che cita "
              f"(ordinanze {f(s(oo)['or'])}, sentenze {f(s(so)['or'])}). ")
V4_NOTE = ("Per questa variante la stima parte dai valori del modello di base, e il calcolo centra ogni pronuncia che cita in modo da non perdere "
           "precisione: \"stesso articolo impugnato\" separa quasi del tutto i precedenti citati dagli altri, e con il calcolo precedente la stima "
           "si fermava prima del massimo. ")
inside = s(v4)["lo"] <= s(b)["or"] <= s(v4)["hi"]
V4_CI = ("La regola guarda la stima puntuale: l'intervallo comprende ancora la stima del modello di base. " if inside
         else "L'intervallo non comprende la stima del modello di base. ")
if not v4["converged"]:
    new_p += ("La variante con disposizione impugnata e articoli della Costituzione non converge, nemmeno partendo dalle stime del modello di base: "
              "la regola di lettura non si applica. ")
elif v4["reaches_half"]:
    new_p += f"A parità di disposizione impugnata e di articoli della Costituzione invocati la stima sale a {f(s(v4)['or'])} ({ci(s(v4))}): secondo la regola fissata prima, il 0,88 si attribuisce alle questioni in comune. " + V4_CI + V4_NOTE
else:
    new_p += f"A parità di disposizione impugnata e di articoli della Costituzione invocati la stima resta {f(s(v4)['or'])} ({ci(s(v4))}): le questioni in comune non lo spiegano. " + V4_NOTE
new_p += f"Con altri due campioni di controlli la stima è {f(seeds[0])} e {f(seeds[1])}. "
rr = [r["or"] for r in ratios]
new_p += (f"In tutte le varianti il rapporto tra presenza e assenza resta compatibile con 1 (stime da {f(min(rr))} a {f(max(rr))}). " if all_include_1
          else f"Il rapporto tra presenza e assenza non è compatibile con 1 in tutte le varianti (stime da {f(min(rr))} a {f(max(rr))}). ")
explained = v1["reaches_half"] or (v4["converged"] and v4["reaches_half"])
if not explained:
    new_p += ("Come stabilito, qui ci si ferma: è un coefficiente secondario, comune a presenza e assenza, identificato solo dalla curva dell'età comune "
              "a redattori di anzianità diversa" + (", concentrato " + ("nelle pronunce fino al 2000 e nelle ordinanze" if period_loc and type_loc else
              "nelle pronunce fino al 2000" if period_loc else "nelle ordinanze") if parts else "") + ", e non spiegato. Non tocca il risultato principale.")
elif v4["converged"] and v4["reaches_half"]:
    new_p += ("Una lettura coerente con questi dati, non verificata separatamente: durante il mandato le questioni ripetute vanno spesso allo stesso "
              "relatore, quindi i precedenti sulla stessa questione decisi in quel periodo sono soprattutto suoi e contano come \"l'ha redatto lui\", "
              "mentre quelli dei colleghi riguardano più spesso altre questioni. Il coefficiente non tocca il risultato principale.")
else:
    new_p += "Il coefficiente non tocca il risultato principale."
import re
R = Path("reports/relazione_for_dummies.md"); t = R.read_text()
i = t.index("Nel modello completo, che usa anche la soglia del giuramento")
j = t.index("\n\n![Figura 7]", i)
t = t[:i] + new_p + t[j:]
t, k = re.subn(r"nel modello completo presenza e assenza non differiscono \(rapporto [0-9,]+; [0-9,]+–[0-9,]+\) \|",
               f"nel modello completo presenza e assenza non differiscono (rapporto {f(b['ratio_present_absent']['or'])}; {ci(b['ratio_present_absent'])}) |", t)
assert k == 1
R.write_text(t)
print({"period_loc": period_loc, "type_loc": type_loc, "explained": explained, "all_include_1": all_include_1})
