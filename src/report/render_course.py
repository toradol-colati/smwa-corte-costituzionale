"""Writes section 3.8 (course measures) of reports/relazione_for_dummies.md from reports/course_measures.json.
Usage: .venv/bin/python src/report/render_course.py"""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[2])  # paths below are relative to the repository root
import json
d = json.load(open("reports/course_measures.json"))
f = lambda x, n=2: f"{(0.0 if abs(x) < 0.5 * 10 ** -n else x):.{n}f}".replace(".", ",")
pct = lambda x: f(x * 100, 1) + "%"
pa, st, sw, br, rb = d["preferential_attachment"], d["structure"], d["small_world"], d["bridges"], d["robustness"]
tr, cl, ii, oi = st["transitivity"], st["avg_local_clustering"], st["corr_in_in"], st["corr_out_in"]
r = rb["after_removal"]
def row(k, lab):
    x = r[k]
    return f"| {lab} | {pct(x['targeted'])} | {pct(x['random_mean'])} ({pct(x['random_lo'])}–{pct(x['random_hi'])}) |"
sec = f"""### 3.8 Le misure del corso (esplorative)

(`reports/course_measures.json`, script `src/analysis/course_measures.py`) Aggiunte il 18/11/2026 per coprire gli argomenti dei libri di testo del corso; non erano nel piano fissato prima. Ognuna ha il suo termine di confronto.

- **Chi è ricco diventa più ricco** (attaccamento preferenziale). Confrontando ogni pronuncia solo con quelle depositate nello stesso anno, le citazioni nuove di un anno crescono con quelle già ricevute come (1 + citazioni)^a, con a = {f(pa['a'])} ({f(pa['lo'])}–{f(pa['hi'])}). Nelle reti del modello nullo di D1, dove le citazioni passate non contano, la stessa stima dà {f(pa['null_mean'])}. Con a = 1 le citazioni nuove crescerebbero in proporzione a quelle già ricevute; qui crescono {"un po' più che in proporzione" if pa['lo'] > 1 else ("meno che in proporzione" if pa['hi'] < 1 else "in proporzione")}. Limite: l'attrattiva propria di ogni pronuncia, che non dipende da quante citazioni ha già, si confonde con l'attaccamento, quindi a ne è un limite superiore.
- **Chiusura triadica.** Se una pronuncia cita due precedenti, quanto spesso uno dei due cita l'altro? Transitività {f(tr['observed'], 3)}, contro {f(tr['null_mean'], 3)} ({f(tr['null_lo'], 3)}–{f(tr['null_hi'], 3)}) nelle {d['reps']} reti rimescolate che conservano citazioni fatte, ricevute ed età: tutte molto sotto il dato vero; clustering locale medio {f(cl['observed'], 3)} contro {f(cl['null_mean'], 3)}. Si usa la rete non orientata: in un grafo aciclico la versione orientata non ha senso.
- **Correlazioni di grado.** Le pronunce molto citate citano pronunce molto citate? Correlazione {f(ii['observed'], 3)}, contro {f(ii['null_mean'], 3)} ({f(ii['null_lo'], 3)}–{f(ii['null_hi'], 3)}) nel nullo. Le pronunce che citano molto citano precedenti molto citati? {f(oi['observed'], 3)} contro {f(oi['null_mean'], 3)} ({f(oi['null_lo'], 3)}–{f(oi['null_hi'], 3)}).
- **Piccolo mondo.** Nella componente gigante ({pct(sw['giant_share'])} delle pronunce, grado medio {f(sw['mean_degree'], 1)}) due pronunce distano in media {f(sw['avg_distance'], 2)} passi, contro {f(sw['er_avg_distance'], 2)} in un grafo casuale con gli stessi nodi e legami; la transitività è {f(sw['transitivity'], 3)} contro {f(sw['er_transitivity'], 4)}. Distanze brevi quasi come in un grafo casuale, e molta più chiusura: è la combinazione che i libri di testo trattano sotto il nome di "piccolo mondo" (Barabási, §3.8; Easley e Kleinberg, cap. 20; letti solo gli indici).
- **Ponti tra filoni.** Le pronunce nell'1% più alto per betweenness (quelle che stanno su molti cammini brevi) hanno in media il {pct(br['top1_betweenness_share_neighbours_outside'])} dei vicini in altre comunità, contro il {pct(br['top1_citations_share_neighbours_outside'])} dell'1% più citato e il {pct(br['all_connected_share_neighbours_outside'])} di tutte le pronunce collegate: sono davvero i ponti tra i filoni. Le due liste hanno in comune il {pct(br['overlap_top1_betweenness_citations'])} delle pronunce.
- **Robustezza.** Togliendo le pronunce più citate la rete si spezza più in fretta che togliendone a caso, ma senza crolli: non c'è un piccolo nucleo di pronunce da cui dipende tutto.

| Pronunce tolte | Componente gigante, togliendo le più citate | Togliendo a caso (min–max su 10 prove) |
| --- | --- | --- |
{row('0.01', '1%')}
{row('0.05', '5%')}
{row('0.1', '10%')}
{row('0.2', '20%')}

Prima di togliere nulla, la componente gigante contiene l'{pct(rb['giant_share_before'])} delle pronunce.

"""
s = open("reports/relazione_for_dummies.md").read()
if "### 3.8 Le misure del corso" in s:
    i = s.index("### 3.8 Le misure del corso"); j = s.index("### 3.9", i)
    s = s[:i] + sec + s[j:]
else:
    j = s.index("## 4. Cosa risponde")
    s = s[:j] + sec + s[j:]
open("reports/relazione_for_dummies.md", "w").write(s)
print(sec)
