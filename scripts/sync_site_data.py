"""Sincronizza i JSON, le figure PNG e la rete interattiva da reports/ a web/public/.
Sanitizza inoltre eventuali NaN/Infinity scritti da Python in null validi per JSON.parse().
"""
from pathlib import Path
import json
import math
import shutil

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
PUBLIC = ROOT / "web" / "public"

JSON_FILES = [
    "network_basic.json",
    "d1_results.json",
    "d2_results.json",
    "d2_strata_check.json",
    "d3_results.json",
    "d3_absences.json",
    "d3_full_check.json",
    "d4_results.json",
    "precedent_succession.json",
    "topics.json",
    "parametri.json",
    "extras.json",
    "course_measures.json",
    "polarity_validation_claude.json",
    "courts_sizing.json",
    "cositting_network.json",
    "collegio_vs_sedute.json",
    "numbers.json",
    "massime_citations.json",
    "api_fetch.json",
]


def sanitize(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return obj


def main():
    (PUBLIC / "data").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "figures").mkdir(parents=True, exist_ok=True)

    missing = []
    copied_json = 0
    for name in JSON_FILES:
        src = REPORTS / name
        if src.exists():
            raw = json.loads(src.read_text(encoding="utf-8"))
            clean = sanitize(raw)
            (PUBLIC / "data" / name).write_text(
                json.dumps(clean, ensure_ascii=False, allow_nan=False),
                encoding="utf-8",
            )
            copied_json += 1
        else:
            missing.append(name)

    copied_png = 0
    fig_dir = REPORTS / "figures"
    if fig_dir.exists():
        for png in sorted(fig_dir.glob("fig*.png")):
            shutil.copy2(png, PUBLIC / "figures" / png.name)
            copied_png += 1

    html = REPORTS / "rete_interattiva.html"
    if html.exists():
        shutil.copy2(html, PUBLIC / "rete_interattiva.html")
        has_html = True
    else:
        missing.append("rete_interattiva.html")
        has_html = False

    print(
        f"Sincronizzati {copied_json}/{len(JSON_FILES)} JSON, "
        f"{copied_png} PNG, rete_interattiva.html={'OK' if has_html else 'MANCANTE'}."
    )
    if missing:
        print("Mancanti in reports/:", ", ".join(missing))


if __name__ == "__main__":
    main()
