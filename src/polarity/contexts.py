"""Contexts of the citations in the base text, for the polarity analysis (adapted form of
sentiment analysis, decided by Umberto on 18/11/2026).
A context is the sentence that contains the mention: from the previous sentence end to the next one,
where a sentence ends with ". " followed by a capital letter or a quote, and the word before the
period is not an abbreviation (n., art., cfr., v., ...). At most 400 characters before and 250 after.
Output: data/interim/polarity_contexts.pkl (one row per mention)
Usage: .venv/bin/python src/polarity/contexts.py
"""
import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
ABBR = {"n", "nn", "art", "artt", "cfr", "v", "vd", "sent", "sentt", "ord", "ordd", "lett", "cod", "proc", "pen", "civ", "cost",
        "reg", "l", "d", "lgs", "r", "c", "p", "s", "g", "u", "ss", "pag", "pagg", "par", "cap", "co", "num", "ecc", "cit", "op", "rel"}
END = re.compile(r"\.\s+(?=[A-ZÀ-ÚÈÉ«\"“(])")


def boundaries(text):
    """Positions where a sentence ends (index after the period)."""
    out = [0]
    for m in END.finditer(text):
        w = re.search(r"([A-Za-zÀ-ú]+)\s*$", text[max(0, m.start() - 12):m.start()])
        if w and w.group(1).lower() in ABBR:
            continue
        out.append(m.start() + 1)
    out.append(len(text))
    return out


def context(text, bounds, a, b):
    import bisect
    i = bisect.bisect_right(bounds, a) - 1
    j = bisect.bisect_left(bounds, b)
    s, e = max(bounds[i], a - 400), min(bounds[min(j, len(bounds) - 1)], b + 250)
    return s, e


def main():
    df = pd.read_pickle(REPO / "data/interim/pronunce.pkl").set_index("pid")
    c = pd.read_csv(REPO / "data/processed/citations.csv")
    c = c[c.section.isin(["diritto", "dispositivo"]) & (c.status == "ok")].copy()
    rows, cache = [], {}
    for r in c.itertuples():
        key = (r.citing_id, r.section)
        if key not in cache:
            t = df.loc[r.citing_id, r.section] or ""
            cache = {key: (t, boundaries(t))}
        t, bd = cache[key]
        s, e = context(t, bd, r.char_start, r.char_end)
        rows.append((r.citing_id, r.cited_id, r.section, r.char_start, r.char_end, s, e,
                     t[s:r.char_start], t[r.char_start:r.char_end], t[r.char_end:e]))
    out = pd.DataFrame(rows, columns=["citing_id", "cited_id", "section", "m_start", "m_end", "c_start", "c_end", "before", "mention", "after"])
    out["context_id"] = out.groupby(["citing_id", "section", "c_start"]).ngroup()
    out.to_pickle(REPO / "data/interim/polarity_contexts.pkl")
    print(len(out), "mentions;", out.context_id.nunique(), "contexts;", out.citing_id.nunique(), "citing pronunce")


if __name__ == "__main__":
    main()
