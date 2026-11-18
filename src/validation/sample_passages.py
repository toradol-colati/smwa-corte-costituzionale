"""Draw stratified samples of pronunce (decade x type) and print, for each, the
passages of the base text that may contain a citation. The passage finder is
deliberately loose and independent of the extractor: every type keyword or
citation cue, with generous context. Used to annotate the gold standard by reading.

Usage: .venv/bin/python src/validation/sample_passages.py dev|test [--with-extractor]
"""
import re, sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "extract"))
SEEDS = {"dev": (20261116, 2), "test": (20261117, 4)}  # test2: 20261118, 6 per stratum; human: 20261119
CUE = re.compile(r"sentenz|ordinanz|\bsentt?\.|\bordd?\.|decision[ei]\b|pronunc|pronunz|\bcfr\b|ex plurimis|ex multis|giurisprudenza|precedent", re.I)

def draw(df, seed, k):
    return df.groupby(["decade", "tipo"], group_keys=False)[df.columns.tolist()].apply(lambda g: g.sample(min(k, len(g)), random_state=seed))

def sample(which):
    """dev: tuning. test: first held-out sample. test2: second held-out sample,
    pronunce up to 286/1986 only, drawn after the extractor was extended."""
    df = pd.read_pickle(REPO / "data" / "interim" / "pronunce.pkl")
    df["decade"] = df.anno // 10 * 10
    dev, test = draw(df, 20261116, 2), draw(df, 20261117, 4)
    test = test[~test.pid.isin(dev.pid)]
    if which == "dev":
        s = dev
    elif which == "test":
        s = test
    else:
        old = df[(df.pid < 19860287) & ~df.pid.isin(dev.pid) & ~df.pid.isin(test.pid)]
        test2 = draw(old, 20261118, 6)
        if which == "test2":
            s = test2
        else:  # human: check by a person on full texts, never seen before (check of 17/11/2026)
            rest = df[~df.pid.isin(dev.pid) & ~df.pid.isin(test.pid) & ~df.pid.isin(test2.pid)]
            per_decade = {1950: 3, 1960: 3, 1970: 3, 1980: 3, 1990: 2, 2000: 2, 2010: 1, 2020: 1}  # about 100 pairs in all
            s = pd.concat([g.sample(min(per_decade[dec], len(g)), random_state=20261119)
                           for (dec, _t), g in rest.groupby(["decade", "tipo"])])
    return s.sort_values("pid")

def passages(text):
    spans = []
    for m in CUE.finditer(text):
        a, b = max(0, m.start() - 70), min(len(text), m.end() + 210)
        if spans and a <= spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], b)
        else:
            spans.append([a, b])
    return [(a, b) for a, b in spans if re.search(r"\d", text[a:b])]

if __name__ == "__main__":
    which = sys.argv[1]
    withx = "--with-extractor" in sys.argv
    if withx:
        from citations import find_mentions
    for r in sample(which).itertuples():
        base = (r.diritto or "") + " ¶ " + (r.dispositivo or "")
        print(f"\n### {r.pid} {r.tipo} split={r.split_how} len={len(base)}")
        ms = find_mentions(base) if withx else []
        for a, b in passages(base):
            print("  «" + base[a:b] + "»")
            if withx:
                got = [f"{m['year']}/{m['number']}" + (f"[X:{m['excluded']}]" if m['excluded'] else "") for m in ms if a <= m['char_start'] < b]
                print("     =>", got)
