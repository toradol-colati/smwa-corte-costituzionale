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
    "# Controllo umano delle citazioni\n",
    f"{len(s)} pronunce estratte a caso (seed 20261119), mai usate prima. Per ognuna c'è tutto il testo di base: "
    "il «Considerato in diritto» (sentenze) o il «Considerato che» (ordinanze), più il dispositivo.\n",
    "**Cosa annotare**, in `data/validation/gold_human.txt`, sulla riga della pronuncia, separando con spazi:\n",
    "- ogni pronuncia della **Corte costituzionale** citata nel testo, scritta come `anno/numero` (per esempio `2007/348`);",
    "- anche le pronunce citate in elenco, con l'anno detto una volta sola, e quelle \"in pari data\";",
    "- una sola volta per pronuncia citata, anche se compare più volte;",
    "- **non** annotare: sentenze di altre corti (Cassazione, Consiglio di Stato, Corte europea…), ordinanze di rimessione "
    "(\"r.o.\", \"reg. ord.\"), leggi e decreti;",
    "- se l'anno non si capisce, scrivere `?/numero` e aggiungere una nota in fondo al file.\n",
    "Una riga vuota dopo i due punti vuol dire: nessuna citazione. Non guardare i risultati dell'estrattore prima di aver finito.\n",
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
