"""Figures for the report, from the result files in reports/ and data/processed/.
Rules: docs/project_guide.md, section 3 (one message per figure, value axes of
bar charts start at zero, colour only where it carries information).
Usage: .venv/bin/python src/analysis/figures.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
REPO = Path(__file__).resolve().parents[2]
P, R, F = REPO / "data/processed", REPO / "reports", REPO / "reports/figures"
GREY, RED, BLUE = "#9a9a9a", "#c0392b", "#2c5f8a"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
nodes = pd.read_csv(P / "nodes.csv")

def save(fig, name):
    fig.tight_layout(); fig.savefig(F / name, bbox_inches="tight"); plt.close(fig)

# 1. pronunce per year
fig, ax = plt.subplots(figsize=(8, 3.2))
c = pd.crosstab(nodes.anno, nodes.tipo)
ax.plot(c.index, c.S, color=BLUE, label="Sentenze"); ax.plot(c.index, c.O, color=GREY, label="Ordinanze")
ax.set_ylim(0); ax.set_xlabel("Anno di deposito"); ax.set_ylabel("Pronunce"); ax.legend(frameon=False)
ax.set_title("Le pronunce per anno: il picco del 1987–1989 è lo smaltimento dell'arretrato", loc="left", fontsize=10)
save(fig, "fig1_pronunce_per_anno.png")

# 2. source of the drafter by year
fig, ax = plt.subplots(figsize=(8, 3.2))
s = pd.crosstab(nodes.anno, nodes.redattore_source, normalize="index").reindex(columns=["relatore_proxy", "signature", "field", "none"]).fillna(0)
ax.stackplot(s.index, s.relatore_proxy, s.signature, s.field, s["none"], colors=[GREY, "#e0a458", BLUE, "#dddddd"],
             labels=["Solo relatore (firmano tutti i giudici)", "Redattore nelle firme", "Redattore nel campo dei dati", "Non indicato"])
ax.set_ylim(0, 1); ax.set_xlabel("Anno di deposito"); ax.set_ylabel("Quota delle pronunce"); ax.legend(frameon=False, fontsize=8, loc="lower left")
ax.set_title("Chi ha scritto la pronuncia si sa solo dal dicembre 1986", loc="left", fontsize=10)
save(fig, "fig2_fonte_redattore.png")

# 3. citations received: CCDF
fig, ax = plt.subplots(figsize=(5, 3.6))
d = np.sort(nodes.in_deg.values); d = d[d > 0]
x = np.unique(d); ccdf = [(d >= v).mean() for v in x]
ax.loglog(x, ccdf, "o", ms=3, color=BLUE)
ax.set_xlabel("Citazioni ricevute (scala logaritmica)"); ax.set_ylabel("Quota di pronunce con almeno\nquel numero di citazioni")
ax.set_title("Poche pronunce raccolgono moltissime citazioni", loc="left", fontsize=10)
save(fig, "fig3_distribuzione_citazioni.png")

d1 = json.load(open(R / "d1_results.json"))
# 4. concentration observed vs null
fig, axs = plt.subplots(1, 3, figsize=(8, 2.8))
for ax, k, lab in zip(axs, ["top1_share", "gini", "never_cited"], ["Quota di citazioni\nall'1% più citato", "Indice di Gini", "Quota di pronunce\nmai citate"]):
    v = d1["concentration"][k]
    ax.bar(["Osservato", "Atteso\n(nullo)"], [v["observed"], v["null_mean"]], color=[BLUE, GREY])
    ax.errorbar([1], [v["null_mean"]], yerr=[[v["null_mean"] - v["null_lo"]], [v["null_hi"] - v["null_mean"]]], color="k", capsize=3)
    ax.set_title(lab, fontsize=9); ax.set_ylim(0)
fig.suptitle("Le citazioni sono molto più concentrate di quanto vorrebbe il caso", x=0.02, ha="left", fontsize=10)
save(fig, "fig4_concentrazione_vs_nullo.png")

# 5. ageing
fig, ax = plt.subplots(figsize=(6, 3.4))
r = np.array(d1["ageing"]["relative_rate_by_age"][:41], float)
ax.semilogy(range(len(r)), r, color=BLUE); ax.axhline(1, color=GREY, lw=1, ls="--")
ax.text(40, 1.08, "scelta uniforme tra i precedenti disponibili", ha="right", fontsize=8, color=GREY)
ax.set_xlabel("Età del precedente (anni)"); ax.set_ylabel("Frequenza di citazione relativa\n(scala logaritmica)")
ax.set_title("Un precedente è citato soprattutto nei primi anni, poi invecchia", loc="left", fontsize=10)
save(fig, "fig5_invecchiamento.png")

# 6. authority vs citations over time
yr = pd.read_pickle(REPO / "data/interim/d1_yearly.pkl"); y = yr[yr.net == "rete_completa"]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.plot(y.year, y.top1_overlap, color=BLUE)
v = d1["rete_completa"]["top1_overlap_null"]
ax.errorbar([2027.5], [v["mean"]], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], fmt="o", color=GREY, capsize=3)
ax.text(2027, v["hi"] + 0.03, "atteso a parità\ndi citazioni (2026)", fontsize=8, color=GREY, ha="right")
ax.set_ylim(0, 1); ax.set_xlabel("Rete delle pronunce depositate fino all'anno"); ax.set_ylabel("Sovrapposizione tra l'1% più autorevole\ne l'1% più citato")
ax.set_title("Le pronunce più autorevoli (HITS) non sono le più citate", loc="left", fontsize=10)
save(fig, "fig6_authority_vs_citazioni.png")

# 7. D3 forest
d3 = json.load(open(R / "d3_results.json"))
rows = [("PRINCIPALE: sedeva nel collegio, non redattore", d3["primary"]["coef"]["sat_not_drafted"], True)]
rows += [(k, v["coef"]["sat_not_drafted"], False) for k, v in d3["variants"].items()]
fig, ax = plt.subplots(figsize=(8, 5))
for i, (lab, c, main) in enumerate(rows[::-1]):
    ax.errorbar(c["or"], i, xerr=[[c["or"] - c["lo"]], [c["hi"] - c["or"]]], fmt="o", color=RED if main else GREY, capsize=3)
ax.axvline(1, color="k", lw=1)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=8)
ax.set_xlabel("Odds ratio (1 = nessun effetto), con intervallo di confidenza al 95%")
ax.set_title("Sedere nel collegio di un precedente non aumenta la probabilità di citarlo", loc="left", fontsize=10)
save(fig, "fig7_d3_memoria_collegiale.png")

# 8. self vs sat
fig, ax = plt.subplots(figsize=(6.6, 3.2))
c = d3["primary"]["coef"]
cn = d3["variants"].get("controllo per norma impugnata in comune (esplorativo)", {}).get("coef")
rows8 = [("Sedeva nel collegio,\nnon l'ha redatto", c["sat_not_drafted"], GREY), ("L'ha redatto lui", c["self_drafted"], RED)]
if cn:
    rows8.append(("L'ha redatto lui, a parità\ndi norma impugnata (esplorativo)", cn["self_drafted"], BLUE))
for i, (lab, cc, col) in enumerate(rows8):
    ax.errorbar(cc["or"], i, xerr=[[cc["or"] - cc["lo"]], [cc["hi"] - cc["or"]]], fmt="o", color=col, capsize=4)
ax.axvline(1, color="k", lw=1); ax.set_yticks(range(len(rows8))); ax.set_yticklabels([r[0] for r in rows8]); ax.set_ylim(-0.6, len(rows8) - 0.4)
ax.set_xscale("log"); ax.set_xlim(0.7, max(r[1]["hi"] for r in rows8) * 1.25)
ax.set_xticks([0.8, 1, 2, 4, 6]); ax.set_xticklabels(["0,8", "1", "2", "4", "6"]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("Odds ratio rispetto a un precedente deciso in sua assenza (scala log.)")
ax.set_title("Il redattore cita molto di più ciò che ha scritto lui;\naver seduto nel collegio non fa una differenza misurabile", loc="left", fontsize=10)
save(fig, "fig8_d3_redatto_vs_collegio.png")

# 9. D2 caterpillar (label-permutation null within the deposit year)
d2all = json.load(open(R / "d2_results.json"))
d2 = d2all["permutazione_anno"]
t = pd.DataFrame(d2["table"]).sort_values("rapporto").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(8, 3.6))
sig = t.p_holm < 0.05
ax.vlines(t.index, t.lo, t.hi, color=np.where(sig, BLUE, "#cccccc"), lw=1)
ax.plot(t.index, t.rapporto, ".", ms=4, color="k"); ax.axhline(1, color=RED, lw=1)
for n_, i in enumerate(t.index[-3:]):
    ax.annotate(t.nome[i].split()[-1], (i, t.rapporto[i]), fontsize=7, xytext=(-8, [-12, 7, 7][n_]), textcoords="offset points", ha="right")
ax.set_yscale("log"); ax.set_yticks([0.5, 0.75, 1, 1.5, 2]); ax.set_yticklabels(["0,5", "0,75", "1", "1,5", "2"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel(f"{d2['judges_tested']} giudici con almeno 30 pronunce, ordinati per rapporto"); ax.set_ylabel("Citazioni osservate / attese")
ax.set_title(f"Dopo la correzione di Holm, le pronunce di {d2['sig_holm_above']} redattori sono citate più dell'atteso\n"
             f"e quelle di {d2['sig_holm_below']} meno; per gli altri la differenza non si distingue dal caso", loc="left", fontsize=10)
save(fig, "fig9_d2_giudici.png")

# 10. during vs post mandate, with the correlation expected for pronunce drawn at random
pm = t.dropna(subset=["rapporto_post"])
pmr = d2["post_mandate"]
fig, ax = plt.subplots(figsize=(4.6, 4.2))
ax.loglog(pm.rapporto_durante, pm.rapporto_post, "o", ms=4, color=BLUE, alpha=.7)
ax.plot([.3, 3], [.3, 3], color=GREY, lw=1)
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_locator(matplotlib.ticker.FixedLocator([0.5, 1, 2]))
    axis.set_major_formatter(matplotlib.ticker.FixedFormatter(["0,5", "1", "2"]))
    axis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("Osservate / attese durante il mandato"); ax.set_ylabel("Osservate / attese nei 10 anni dopo")
fmt = lambda x: f"{x:.2f}".replace(".", ",")
ax.set_title(f"Durante e dopo il mandato: correlazione {fmt(pmr['spearman_during_post'])},\n"
             f"contro {fmt(pmr['spearman_null_mean'])} (fino a {fmt(pmr['spearman_null_hi'])}) per pronunce prese a caso", loc="left", fontsize=9)
save(fig, "fig10_d2_dopo_mandato.png")
print(sorted(p.name for p in F.glob("*.png")))
