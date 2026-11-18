"""The main numbers of the report must match the result files (reports/*.json).
Each check is a phrase of the report with the number in its context, rebuilt from the JSON:
a bare number would match anywhere. When a result changes, the test fails until the report
is updated. Usage: .venv/bin/pytest tests/test_report_numbers.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REPORT = (REPO / "reports/relazione_for_dummies.md").read_text(encoding="utf-8")


def load(name):
    return json.load(open(REPO / "reports" / name))


def it(x, d=2):
    """Italian decimal: 1.234 -> '1,23'."""
    return f"{x:.{d}f}".replace(".", ",")


def n(x):
    """Italian thousands: 46969 -> '46.969'."""
    return f"{int(x):,}".replace(",", ".")


def ci(c, d=2):
    return f"{it(c['lo'], d)}–{it(c['hi'], d)}"


def checks():
    out = []
    d3 = load("d3_results.json")
    p, v = d3["primary"], d3["variants"]
    s, sd = p["coef"]["sat_not_drafted"], p["coef"]["self_drafted"]
    out += [
        ("D3 principale, sintesi", f"odds ratio {it(s['or'])}, intervallo di confidenza al 95% da {it(s['lo'])} a {it(s['hi'])}"),
        ("D3 principale, tabella", f"(risultato principale) | **{it(s['or'])}** | {ci(s)} |"),
        ("D3 redatto da lui, tabella", f"| l'ha redatto lui | {it(sd['or'])} | {ci(sd)} |"),
        ("D3 redatto da lui, sintesi", f"odds ratio {it(sd['or'])} ({ci(sd)})"),
        ("D3 base", f"Base: {n(p['strata'])} pronunce che citano, {n(p['cases'])} citazioni, di cui {n(p['cases_absent'])} "
                    f"a precedenti decisi in assenza del redattore; {p['clusters']} redattori."),
    ]
    for key, phrase in [("senza autocitazioni del redattore", "senza autocitazioni"),
                        ("solo pronunce dalla 287/1986 (redattore osservato)", "solo dal 1987, dove il redattore è osservato,"),
                        ("senza gli anni dell'arretrato (citanti 1987-1989 escluse)", "senza gli anni dell'arretrato"),
                        ("testo intero (anche Ritenuto in fatto)", "sul testo intero"),
                        ("con le citazioni delle massime (note editoriali)", "aggiungendo le citazioni delle massime")]:
        c = v[key]["coef"]["sat_not_drafted"]
        out.append((f"D3 variante: {key}", f"{phrase} {it(c['or'])} ({ci(c)})"))
    seeds = d3["seed_sensitivity_or"]
    out.append(("D3 altri campioni", f"con altri cinque campioni di controlli tra {it(min(seeds))} e {it(max(seeds))}"))
    for key, label in [("solo ordinanze che citano", "ordinanze"), ("solo sentenze che citano", "sentenze"),
                       ("citanti fino al 2000", "prima del 2001"), ("citanti dal 2001", "dopo")]:
        out.append((f"D3 redatto da lui: {key}", f"({it(v[key]['coef']['self_drafted']['or'])})"))
    f = d3["full"]["coef"]
    out.append(("D3 modello completo", f"sia quando sedeva ({it(f['sat_not_drafted']['or'])}; {ci(f['sat_not_drafted'])}) "
                                       f"sia quando era assente ({it(f['in_mandate_absent']['or'])}; {ci(f['in_mandate_absent'])})"))
    num = load("numbers.json")
    out += [
        ("Testi senza divisione", f"In {num['split_failed']} testi ({it(num['split_failed_share'] * 100, 1)}% delle pronunce: "
                                  f"{num['split_failed_by_type']['O']} ordinanze e {num['split_failed_by_type']['S']} sentenze)"),
        ("Menzioni valide", f"| Menzioni valide in tutto il testo | {n(num['mentions_valid'])} |"),
        ("Menzioni scartate", f"senza anno) | {n(num['mentions_excluded'])} |"),
        ("Menzioni errate", f"inesistenti o successive | {n(num['mentions_errors'])} |"),
        ("Stesso giorno", f"tenute a parte | {n(num['mentions_same_date'])} |"),
        ("Tipo scritto diverso", f"Nell'{it(num['type_mismatch_share'] * 100, 1)}% delle menzioni"),
    ]
    return out


def test_report_numbers_match_results():
    missing = [f"{name}: «{phrase}»" for name, phrase in checks() if phrase not in REPORT]
    assert not missing, "Numeri della relazione non allineati ai file dei risultati:\n" + "\n".join(missing)
