"""Build one single Markdown file with the whole project, for reading it in one place.

Part 1 is the guide (docs/handbook.md). The appendices contain, in full, every other file of the
repository that can be read as text: instructions and rules, working documents, the report and the
reports written by the programs, the result files (JSON), the programs and the tests, the sheets for the
hand checks. The figures are embedded in the file (as data URIs), so that the report shows them.
Left out, and listed at the top of the file: the data tables (data/raw, data/interim, data/processed),
the interactive page (reports/rete_interattiva.html), the literature PDFs.

The file is written to progetto_completo.md at the root of the repository and kept out of git (.gitignore),
because it repeats files that are already in the repository.
Usage: .venv/bin/python src/report/single_file.py [--out PATH] [--extra FILE ...]
       --extra adds files from outside the repository at the end (for example a draft kept outside it).
"""
import argparse
import base64
import re
import subprocess
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

APPENDICES = [
    ("A", "Istruzioni, regole e configurazione",
     ["README.md", "CLAUDE.md", ".claude/rules/data.md", ".claude/rules/network-analysis.md", ".claude/settings.json",
      ".gitignore", "pytest.ini", "requirements.txt", "requirements.lock"]),
    ("B", "I documenti di lavoro",
     ["docs/spec.md", "docs/decisions.md", "docs/context.md", "docs/data_schema.md", "docs/context_corti.md",
      "docs/sources.md", "docs/course_mapping.md", "docs/project_guide.md"]),
    ("C", "La relazione e i report",
     ["reports/relazione_for_dummies.md", "reports/validation.md", "reports/validation_round1.md",
      "reports/validation_test.md", "reports/validation_test2.md", "reports/data_inspection.md",
      "reports/sparql_reconciliation.md", "reports/judges_quality.md", "reports/topics.md", "reports/d3_results.md",
      "reports/polarity_validation_claude.md"]),
    ("D", "I file dei risultati (i numeri, scritti dai programmi)",
     None),  # filled in main(): the manifest and every reports/*.json
    ("E", "I programmi e i controlli automatici, nell'ordine in cui girano",
     ["src/ingest/download.py", "src/ingest/inspect_raw.py", "src/ingest/sparql_check.py", "src/ingest/build_pronunce.py",
      "src/extract/citations.py", "src/extract/citations_massime.py", "src/validation/sample_passages.py",
      "src/validation/evaluate.py", "src/validation/human_sheet.py", "src/judges/build_judges.py",
      "src/analysis/topics.py", "src/analysis/parametri.py", "src/networks/build.py", "src/networks/cositting.py",
      "src/ingest/fetch_api.py", "src/analysis/d1_pronunce.py", "src/analysis/d2_d4_giudici.py",
      "src/analysis/d2_strata_check.py", "src/analysis/d3_memoria_collegiale.py", "src/analysis/d3_absences.py",
      "src/analysis/d3_full_check.py", "src/analysis/precedent_succession.py", "src/analysis/extras.py",
      "src/analysis/course_measures.py", "src/analysis/figures.py", "src/analysis/interactive.py",
      "src/analysis/interactive_template.html", "src/report/report_numbers.py", "src/report/plain_intros.py",
      "src/report/single_file.py", "src/courts/sizing.py", "src/courts/mentions.py", "src/polarity/contexts.py",
      "src/polarity/lexicon.py", "src/polarity/draw_sample.py", "src/polarity/evaluate.py",
      "tests/test_citations.py", "tests/test_report_numbers.py"]),
    ("F", "I fogli per i controlli a mano e le letture di riferimento",
     ["data/validation/human_check.md", "data/validation/gold_test.txt", "data/validation/gold_test2.txt",
      "data/validation/gold_human.txt", "data/validation/polarity_human_check.md",
      "data/validation/polarity_test_sample.csv", "data/validation/polarity_test_labels.csv",
      "data/validation/gold_polarity_claude.txt", "data/validation/gold_polarity_human.txt"]),
]
LANG = {".py": "python", ".json": "json", ".csv": "csv", ".html": "html", ".lock": "text", ".txt": "text",
        ".ini": "ini", "": "text"}


def demote(md, levels):
    """Push every Markdown heading down by `levels` (at most level 6), outside fenced code blocks."""
    out, fence = [], None
    for line in md.split("\n"):
        m = re.match(r"^(`{3,}|~{3,})", line)
        if m:
            mark = m.group(1)[0]
            if fence is None:
                fence = mark
            elif fence == mark:
                fence = None
        elif fence is None:
            h = re.match(r"^(#{1,6})(\s.*)$", line)
            if h:
                line = "#" * min(6, len(h.group(1)) + levels) + h.group(2)
        out.append(line)
    return "\n".join(out)


def anchor(code, path):
    return f"{code.lower()}-{re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "progetto_completo.md"))
    ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args()

    appendices = []
    for code, title, files in APPENDICES:
        if code == "D":
            files = ["data/raw/MANIFEST.csv"] + sorted(str(p.relative_to(REPO)) for p in (REPO / "reports").glob("*.json"))
        appendices.append((code, title, files))
    missing = [f for _, _, fs in appendices for f in fs if not (REPO / f).exists()]
    if missing:
        raise SystemExit(f"missing files: {missing}")
    commit = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%h del %ad", "--date=short"],
                            capture_output=True, text=True).stdout.strip()
    figures = sorted((REPO / "reports/figures").glob("*.png"), key=lambda p: int(re.search(r"fig(\d+)", p.name).group(1)))

    head = [
        "# Il progetto completo, in un unico file",
        "",
        f"Questo file contiene tutto il progetto in un solo posto. È stato creato il {date.today():%d/%m/%Y} dal programma "
        f"`src/report/single_file.py`, a partire dal repository nello stato dell'ultima modifica salvata ({commit}). "
        "Se il lavoro cambia, il file si ricrea con lo stesso programma: non va corretto a mano.",
        "",
        "**Come è fatto.**",
        "",
        "- **Prima parte: la guida** (sezioni 0–20). Spiega tutto il progetto in linguaggio semplice. Quando la guida nomina "
        "un file (per esempio `docs/decisions.md`), quel file è riportato per intero più avanti, in un'appendice, con il suo "
        "percorso nel titolo: si trova nell'indice qui sotto.",
        "- **Appendici A–F: tutti i file del repository che si possono leggere come testo**, per intero e senza modifiche, "
        "tranne una: i titoli interni di ogni file sono stati abbassati di livello, perché stiano sotto il titolo del file.",
        "- **Appendice G: le figure**, dentro il file. Le stesse figure compaiono anche nella relazione (appendice C).",
        "",
        "**Che cosa non c'è, e perché.**",
        "",
        "- Le tabelle dei dati (`data/raw/`, `data/interim/`, `data/processed/`): sono troppo grandi (alcune decine di "
        "megabyte) e non si leggono come testo. Che cosa contiene ogni tabella, e quale programma la scrive, è nelle "
        "sezioni 5 e 17 della guida.",
        "- La rete interattiva (`reports/rete_interattiva.html`): è una pagina da aprire in un browser.",
        "- I PDF della letteratura (`literature/`): sono protetti dal diritto d'autore.",
        "",
        "## Indice",
        "",
        "- [La guida (sezioni 0–20)](#guida)",
    ]
    for code, title, files in appendices:
        head.append(f"- [Appendice {code} — {title}](#appendice-{code.lower()})")
        head += [f"  - [{code}.{i} `{f}`](#{anchor(code, f)})" for i, f in enumerate(files, 1)]
    head.append("- [Appendice G — Le figure](#appendice-g)")
    if a.extra:
        head.append("- [Appendice H — File fuori dal repository](#appendice-h)")
    head += ["", '<a id="guida"></a>', ""]

    guide = (REPO / "docs/handbook.md").read_text(encoding="utf-8")
    guide = guide.split("\n", 1)[1].lstrip("\n")  # its title is replaced by the title of this file
    body = [guide.rstrip("\n"), ""]

    for code, title, files in appendices:
        body += [f'<a id="appendice-{code.lower()}"></a>', "", f"## Appendice {code} — {title}", ""]
        for i, f in enumerate(files, 1):
            p = REPO / f
            text = p.read_text(encoding="utf-8")
            body += [f'<a id="{anchor(code, f)}"></a>', "", f"### {code}.{i} `{f}`", ""]
            if p.suffix == ".md":
                if f == "reports/relazione_for_dummies.md":  # images point to the definitions at the end of this file
                    text = re.sub(r"!\[([^\]]*)\]\(figures/([\w\-]+)\.png\)", r"![\1][\2]", text)
                body += [demote(text.rstrip("\n"), 3), ""]
            else:
                body += ["````" + LANG.get(p.suffix, "text"), text.rstrip("\n"), "````", ""]

    body += ['<a id="appendice-g"></a>', "", "## Appendice G — Le figure", "",
             "Scritte da `src/analysis/figures.py` in `reports/figures/`. Che cosa mostra ognuna è nella sezione 5.18 della guida.", ""]
    for p in figures:
        body += [f"### {p.name}", "", f"![{p.stem}][{p.stem}]", ""]
    if a.extra:
        body += ['<a id="appendice-h"></a>', "", "## Appendice H — File fuori dal repository", ""]
        for i, f in enumerate(a.extra, 1):
            p = Path(f).resolve()
            body += [f"### H.{i} `{p.name}`", "", demote(p.read_text(encoding="utf-8").rstrip("\n"), 3), ""]
    # image definitions: invisible lines, used by the report and by appendix G
    body += [""] + [f"[{p.stem}]: data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}" for p in figures]

    out = Path(a.out)
    out.write_text("\n".join(head + body) + "\n", encoding="utf-8")
    n = sum(len(fs) for _, _, fs in appendices)
    print(f"{out}: {out.stat().st_size / 1e6:.1f} MB, guide + {n} files + {len(figures)} figures + {len(a.extra)} extra")


if __name__ == "__main__":
    main()
