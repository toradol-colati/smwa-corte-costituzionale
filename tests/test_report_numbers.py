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
    # D1
    d1 = load("d1_results.json")
    c, ct = d1["concentration"], d1["concentration_by_type"]
    pc = lambda x, d=1: it(x * 100, d)

    def row(label, k, f):
        return (f"| {label} | {f(c[k]['observed'])} | {f(c[k]['null_mean'])} ({f(c[k]['null_lo'])}–{f(c[k]['null_hi'])}) | "
                f"{f(ct[k]['null_mean'])} ({f(ct[k]['null_lo'])}–{f(ct[k]['null_hi'])}) |")
    out += [
        ("D1 quota 1%", row("Quota di citazioni all'1% più citato", "top1_share", lambda x: pc(x) + "%").replace("%–", "–").replace("%)", ")")),
        ("D1 Gini", row("Indice di Gini", "gini", lambda x: it(x))),
        ("D1 mai citate", row("Pronunce mai citate", "never_cited", lambda x: pc(x) + "%").replace("%–", "–").replace("%)", ")")),
        ("D1 massimo", row("Citazioni della pronuncia più citata", "max", lambda x: it(x, 0))),
        ("D1 per tipo", f"non è mai citato il {pc(ct['observed_by_type']['never_cited_ordinanze'])}% delle ordinanze e il "
                        f"{pc(ct['observed_by_type']['never_cited_sentenze'])}% delle sentenze"),
        ("D1 coda", f"rapporto di verosimiglianza −{it(-d1['tail']['vs_lognormal_R'], 1)}, p < 0,001; esponente stimato "
                    f"{it(d1['tail']['alpha'])} da {d1['tail']['xmin']} citazioni in su"),
    ]
    rc, rp = d1["rete_completa"], d1["replica_agnoloni_pagallo"]
    out += [
        ("D1 sovrapposizione", f"si sovrappongono per il {pc(rc['top1_overlap'])}%; a parità di citazioni ricevute, il caso darebbe il "
                               f"{pc(rc['top1_overlap_null']['mean'])}% ({pc(rc['top1_overlap_null']['lo'])}–{pc(rc['top1_overlap_null']['hi'])})"),
        ("D1 replica", f"sovrapposizione è quella del caso ({pc(rp['top1_overlap'], 0)}% contro {pc(rp['top1_overlap_null']['mean'], 0)}%)"),
        ("D1 replica 30", f"solo {rp['top30_auth_in_top30_cited']} delle prime 30 per authority"),
    ]
    pr = d1["prediction"]
    out.append(("D1 previsione", f"lo aumenta dello {it(-pr['reduction'] * 100)}% ({it(-pr['reduction_hi'] * 100)}–{it(-pr['reduction_lo'] * 100)})"))
    ag, sv = d1["ageing"], d1["survival"]
    out += [
        ("D1b picco", f"({it(ag['relative_rate_by_age'][ag['peak_age']], 1)} volte la scelta uniforme), si dimezza in {ag['half_life_after_peak']} anni "
                      f"e scende sotto la scelta uniforme dopo {ag['age_when_rate_below_1']}"),
        ("D1b durata", f"è {it(sv['median'], 0)} anni: {it(sv['sentenze']['median'], 0)} per le sentenze, {it(sv['ordinanze']['median'], 0)} per le ordinanze"),
        ("D1b ossatura", f"il {pc(sv['share_cited_after_30y'])}% delle pronunce con almeno trent'anni"),
    ]
    # communities, HITS, outcome, Wikipedia
    e = load("extras.json")
    cm, h = e["communities"], e["hits_communities"]
    out += [
        ("Comunità", f"{cm['communities_50plus']} comunità con almeno 50 pronunce, che coprono l'{pc(cm['share_nodes_in_50plus'], 0)}% dei nodi "
                     f"(modularità {it(cm['modularity'])}, contro {it(cm['modularity_rewired'])} ({it(cm['modularity_rewired_lo'], 3)}–"
                     f"{it(cm['modularity_rewired_hi'], 3)}) in {cm['rewirings']} reti ricablate"),
        ("Comunità e topic", f"accordo con i topic {it(cm['nmi_topic'])}, contro {it(cm['nmi_null_mean'], 3)} del caso"),
        ("Infomap", f"({cm['infomap']['communities_50plus']} con almeno 50 pronunce, che coprono solo il {pc(cm['infomap']['share_nodes_in_50plus'], 0)}% dei nodi), "
                    f"l'accordo con Leiden è {it(cm['infomap']['nmi_with_leiden'])} su una scala da 0 a 1 e quello con i topic {it(cm['infomap']['nmi_topic'])}"),
        ("HITS comunità", f"qui il {pc(h['authority_hits']['top1_share_largest_community'])}% dell'1% più autorevole sta in una sola comunità "
                          f"({n(h['authority_hits']['largest_community_size'])} pronunce, anno mediano {h['authority_hits']['largest_community_median_year']}), "
                          f"che raccoglie il {pc(h['authority_mass_in_largest_community'])}% dell'autorità totale, mentre l'1% più citato è sparso in "
                          f"{h['citazioni']['communities_in_top1']} comunità"),
        ("PageRank", f"anno mediano {h['pagerank']['median_year_top1']} nel suo 1% più alto"),
    ]
    es, w = e["esito"], e["wikipedia"]
    out += [
        ("Esito", f"ricevono in dieci anni {it(es['tutte']['media_ill'], 1)} citazioni in media, le altre {it(es['tutte']['media_altre'], 1)}: "
                  f"{it(es['tutte']['rapporto_medie'], 1)} volte ({it(es['tutte']['rapporto_lo'], 1)}–{it(es['tutte']['rapporto_hi'], 1)})"),
        ("Esito sentenze", f"Tra le sole sentenze, {it(es['sentenze']['rapporto_medie'], 1)} volte ({it(es['sentenze']['rapporto_lo'], 1)}–{it(es['sentenze']['rapporto_hi'], 1)})"),
        ("Wikipedia", f"Solo l'{pc(w['base_rate'])}% delle pronunce è richiamato da una voce. Tra l'1% più autorevole la quota è "
                      f"{pc(w['share_in_top1_authority_pct'])}%, tra l'1% più citato {pc(w['share_in_top1_citations_pct'])}%"),
    ]
    # D2
    d2 = load("d2_results.json")
    a, at, am, a87, pre = (d2[k] for k in ["permutazione_anno", "permutazione_anno_tipo", "permutazione_anno_tipo_materia",
                                           "permutazione_anno_dal_1987", "nullo_preregistrato"])
    pm, pmm = a["post_mandate"], am["post_mandate"]
    out += [
        ("D2 Holm", f"le pronunce di **{a['sig_holm_above']}** sono citate più dell'atteso e quelle di **{a['sig_holm_below']}** meno"),
        ("D2 sintesi", f"le pronunce di {a['sig_holm_above']} sono citate più di pronunce prese a caso dello stesso anno e quelle di {a['sig_holm_below']} meno"),
        ("D2 dispersione", f"la varianza del logaritmo del rapporto è {it(a['var_ratio_to_null'], 1)} volte quella attesa"),
        ("D2 varianti", f"Tenendo conto anche del tipo di pronuncia, {at['sig_holm_above']} sopra e {at['sig_holm_below']} sotto; anche della materia, "
                        f"{am['sig_holm_above']} e {am['sig_holm_below']}. Con le sole pronunce dalla 287/1986, dove il redattore è osservato, "
                        f"{a87['sig_holm_above']} e {a87['sig_holm_below']} su {a87['judges_tested']} giudici."),
        ("D2 dopo il mandato", f"correlazione tra ranghi {it(pm['spearman_during_post'])}. Una parte è meccanica"),
        ("D2 dopo il mandato, nullo", f"la correlazione sarebbe {it(pm['spearman_null_mean'])} (95%: {it(pm['spearman_null_lo'])}–{it(pm['spearman_null_hi'])})"),
        ("D2 dopo il mandato, materia", f"{it(pmm['spearman_during_post'])} contro {it(pmm['spearman_null_mean'])} ({it(pmm['spearman_null_lo'])}–{it(pmm['spearman_null_hi'])})"),
        ("D2 nullo fissato", f"con quel nullo i giudici fuori dall'atteso erano {pre['age_only']['sig_holm_above']} e {pre['age_only']['sig_holm_below']}, "
                             f"con una dispersione {it(pre['age_only']['var_ratio_to_null'], 0)} volte il caso"),
    ]
    for r in a["table"][:3]:
        out.append((f"D2 {r['nome']}", f"({it(r['rapporto'])}; {it(r['lo'])}–{it(r['hi'])})"))
    # D4
    d4 = load("d4_results.json")
    o, pv = d4["organo"], d4["provenienza"]
    out += [
        ("D4 organo", f"sono il {pc(o['same_group_share'])}%, contro il {pc(o['null_mean'])}% atteso ({pc(o['null_lo'])}–{pc(o['null_hi'])}); "
                      f"p = {it(o['p'], 3)}, {it(o['p_holm'], 3)} con Holm"),
        ("D4 provenienza", f"{pc(pv['same_group_share'])}% contro {pc(pv['null_mean'])}% ({pc(pv['null_lo'])}–{pc(pv['null_hi'])}); "
                           f"p = {it(pv['p'], 3)}, {it(pv['p_holm'], 3)} con Holm. L'eccesso è del {pc(pv['excess_over_null'])}%"),
    ]
    # network
    nb = load("network_basic.json")
    out += [
        ("Rete", f"{n(nb['nodes'])} pronunce, {n(nb['edges'])} citazioni, nessun ciclo"),
        ("Isolate", f"{n(nb['isolates'])} ({pc(nb['isolates'] / nb['nodes'], 0)}%) non citano e non sono citate"),
        ("Per tipo", f"Una sentenza riceve in media {it(nb['by_type']['S']['in_mean'], 1)} citazioni, un'ordinanza {it(nb['by_type']['O']['in_mean'], 1)}"),
        ("Densità", f"ogni pronuncia cita in media {it(nb['out_deg_mean'], 1)} precedenti, e la densità è {it(nb['density_backward'], 5)}"),
        ("Catena", f"ha {nb['dag_longest_path']} anelli"),
    ]
    return out


def test_report_numbers_match_results():
    missing = [f"{name}: «{phrase}»" for name, phrase in checks() if phrase not in REPORT]
    assert not missing, "Numeri della relazione non allineati ai file dei risultati:\n" + "\n".join(missing)
