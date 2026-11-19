"""Constitutional parameters (parametri) of every pronuncia, from the massime: the articles of the
Constitution that the question claims to be violated (legge 87/1953, art. 23, lett. b). Used for a
finer subject matter than the topics (decided on 19/11/2026, docs/decisions.md):
  - parameter = a massime `parametri/parametro` entry whose `descrizione` is "Costituzione"
    (constitutional laws and regional statutes are left out); the article as written in `articolo`;
  - pronuncia = the union of the articles of its massime;
  - weight of an article = idf = ln(N / n_a), N pronunce with at least one article, n_a those invoking it:
    art. 3 is invoked in about two thirds of the pronunce and would otherwise make almost every pair similar;
  - main article = the article invoked in most of the pronuncia's massime; ties go to the rarer article.
Outputs: data/processed/parametri_pronunce.csv, reports/parametri.json
Usage: .venv/bin/python src/analysis/parametri.py
"""
import glob
import json
import math
from collections import Counter
from pathlib import Path

import pandas as pd
from lxml import etree

REPO = Path(__file__).resolve().parents[2]


def load():
    rows, mass = [], []
    for path in sorted(glob.glob(str(REPO / "data/raw/massime/*/*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            h = p.find("pronuncia_testata")
            pid = int(h.findtext("anno_pronuncia")) * 10000 + int(h.findtext("numero_pronuncia"))
            for k, m in enumerate(p.findall("massime/massima")):
                arts = {(x.findtext("articolo") or "").strip() for x in m.findall("parametri/parametro")
                        if (x.findtext("descrizione") or "").strip() == "Costituzione"}
                arts.discard("")
                mass.append((pid, k, len(arts) > 0))
                rows += [(pid, k, a) for a in arts]
    return pd.DataFrame(rows, columns=["pid", "massima", "art"]), pd.DataFrame(mass, columns=["pid", "massima", "has"])


def main():
    d, mass = load()
    sets = d.groupby("pid").art.apply(lambda s: sorted(set(s)))
    N = len(sets)
    n_a = Counter(a for s in sets for a in s)
    idf = {a: math.log(N / c) for a, c in n_a.items()}
    counts = d.groupby(["pid", "art"]).massima.nunique().reset_index(name="k")
    counts["idf"] = counts.art.map(idf)
    main_art = counts.sort_values(["pid", "k", "idf"], ascending=[True, False, False]).drop_duplicates("pid").set_index("pid").art
    out = pd.DataFrame({"pid": sets.index, "articles": sets.map("|".join).values, "main_article": main_art.reindex(sets.index).values})
    out.to_csv(REPO / "data/processed/parametri_pronunce.csv", index=False)
    nodes = pd.read_csv(REPO / "data/processed/nodes.csv", usecols=["pid", "anno", "tipo"])
    nodes["main"] = nodes.pid.map(main_art).fillna("nessuno")
    strata = nodes.groupby(["anno", "tipo", "main"]).size()
    dec = mass.assign(dec=mass.pid // 100000 * 10)
    has_p = mass.groupby("pid").has.max()
    info = {"pronunce_with_article": int(N), "massime_with_article_share": float(mass.has.mean()),
            "pronunce_with_massime_and_article_share": float(has_p.mean()),
            "by_decade_massime": {int(k): float(v) for k, v in dec.groupby("dec").has.mean().items()},
            "by_decade_pronunce": {int(k): float(v) for k, v in has_p.groupby(has_p.index // 100000 * 10).mean().items()},
            "distinct_articles": len(n_a), "mean_articles_per_pronuncia": float(sets.str.len().mean()),
            "share_invoking_top": {a: n_a[a] / N for a, _ in n_a.most_common(10)},
            "main_article_top": {k: int(v) for k, v in main_art.value_counts().head(10).items()},
            "strata_year_type_main": int(len(strata)), "pronunce_in_strata_of_2_or_more": float(strata[strata >= 2].sum() / strata.sum())}
    json.dump(info, open(REPO / "reports/parametri.json", "w"), indent=1)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
