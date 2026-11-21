"""Write the sheet for the human check of the citation extractor (check of 17/11/2026).
For every pronuncia of the "human" sample (src/validation/sample_passages.py) the sheet shows the
whole base text (Considerato in diritto or Considerato che, plus the dispositivo), never the output
of the extractor. The annotator writes the citations in data/validation/gold_human.txt, one line
per pronuncia: "<pid>: <year>/<number> <year>/<number> ...". Then:
    .venv/bin/python src/validation/evaluate.py human
Outputs: data/validation/human_check.md, data/validation/gold_human.txt (template, only if missing)
Usage: .venv/bin/python src/validation/human_sheet.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "validation"))
from sample_passages import sample  # noqa: E402

s = sample("human")
head = [
    "# Il controllo a mano delle citazioni\n",
    "**A che cosa serve.** Un programma ha cercato in tutte le pronunce le citazioni di altre pronunce della Corte. Per sapere quanto sbaglia "
    "bisogna confrontarlo con la lettura di una persona. Questo foglio contiene "
    f"{len(s)} pronunce estratte a caso (seme 20261119), mai usate prima per costruire o provare il programma. Per ognuna c'è tutto il testo "
    "di base: il ragionamento della Corte («Considerato in diritto» nelle sentenze, «Considerato che» nelle ordinanze) e il dispositivo, cioè "
    "la decisione.\n",
    "**Che cosa fare.** Leggere ogni pronuncia per intero e scrivere in `data/validation/gold_human.txt`, sulla riga che comincia con il numero "
    "della pronuncia, le pronunce della Corte che cita, separate da spazi:\n",
    "- ogni pronuncia della **Corte costituzionale** citata nel testo, scritta come `anno/numero` (per esempio `2007/348` per la sentenza n. 348 "
    "del 2007);",
    "- anche quelle citate in un elenco con l'anno detto una volta sola (\"sentenze n. 26 e n. 320 del 2007\" diventa `2007/26 2007/320`) e "
    "quelle \"in pari data\" (dello stesso giorno della pronuncia che cita);",
    "- ogni pronuncia citata una volta sola, anche se compare più volte;",
    "- **non** scrivere: le sentenze di altre corti (Cassazione, Consiglio di Stato, Corte europea…), le ordinanze con cui un giudice porta la "
    "questione alla Corte (citate come \"r.o.\" o \"reg. ord.\"), leggi e decreti;",
    "- se l'anno non si capisce, scrivere `?/numero` e aggiungere una nota in fondo al file.\n",
    "Se una pronuncia non cita nessun'altra pronuncia, la sua riga resta vuota dopo i due punti. Non guardare i risultati del programma prima "
    "di aver finito. Alla fine il comando `.venv/bin/python src/validation/evaluate.py human` confronta la lettura con il programma e scrive i "
    "risultati in `reports/validation_human.md`. Tempo stimato: 3–5 ore.\n",
]
body = []
for r in s.itertuples():
    base = (r.diritto or "").strip() + "\n\n[DISPOSITIVO]\n\n" + (r.dispositivo or "").strip()
    body += [f"\n## {r.pid}: {'sentenza' if r.tipo == 'S' else 'ordinanza'} n. {r.pid % 10000} del {r.anno}\n", base, ""]
(REPO / "data/validation/human_check.md").write_text("\n".join(head + body), encoding="utf-8")
gold = REPO / "data/validation/gold_human.txt"
if not gold.exists():
    gold.write_text("".join(f"{p}:\n" for p in s.pid), encoding="utf-8")
print(len(s), "pronunce;", s.groupby([s.anno // 10 * 10, "tipo"]).size().to_dict())
