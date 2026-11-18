"""Robustness variant: citations found in the massime (texts written by the Ufficio del
massimario, including the editorial notes "Precedenti citati: ..."), added to the base network.
The same grammar and the same checks of src/extract/citations.py are applied.
Outputs: data/processed/edges_citations_with_notes.csv (base edges + pairs found only in the
massime), reports/massime_citations.json
Usage: .venv/bin/python src/extract/citations_massime.py
"""
import glob
import json
import sys
from pathlib import Path

import pandas as pd
from lxml import etree

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "extract"))
from citations import find_mentions  # noqa: E402

df = pd.read_pickle(REPO / "data/interim/pronunce.pkl")
deposit = dict(zip(df.pid, df.data_deposito))
rows = []
n_massime = 0
for path in sorted(glob.glob(str(REPO / "data/raw/massime/*/*.xml"))):
    for p in etree.parse(path).getroot().iter("pronuncia"):
        h = p.find("pronuncia_testata")
        anno = int(h.findtext("anno_pronuncia"))
        pid = anno * 10000 + int(h.findtext("numero_pronuncia"))
        for m in p.findall("massime/massima"):
            n_massime += 1
            for x in find_mentions(m.findtext("testo") or "", default_year=anno):
                if x.get("excluded"):
                    continue
                rows.append((pid, int((x.get("year") or 0) * 10000 + x["number"])))
c = pd.DataFrame(rows, columns=["citing_id", "cited_id"])
n_mentions = len(c)
c = c[c.citing_id.isin(deposit) & c.cited_id.isin(deposit) & (c.citing_id != c.cited_id)]
c = c[c.cited_id.map(deposit) < c.citing_id.map(deposit)]
notes = c.groupby(["citing_id", "cited_id"]).size().rename("n_mentions").reset_index()
base = pd.read_csv(REPO / "data/processed/edges_citations.csv")
full = pd.read_csv(REPO / "data/processed/edges_citations_fulltext.csv")
key = lambda d: set(zip(d.citing_id, d.cited_id))
kb, kn, kf = key(base), key(notes), key(full)
only = notes[[k not in kb for k in zip(notes.citing_id, notes.cited_id)]]
pd.concat([base, only]).to_csv(REPO / "data/processed/edges_citations_with_notes.csv", index=False)
out = {"massime": n_massime, "mentions_in_massime": n_mentions, "pairs_in_massime": len(kn),
       "pairs_also_in_base_text": len(kn & kb), "share_also_in_base_text": len(kn & kb) / len(kn),
       "pairs_also_in_full_text": len(kn & kf), "pairs_only_in_massime": len(kn - kb),
       "base_pairs": len(kb), "base_pairs_found_in_massime": len(kb & kn) / len(kb),
       "network_with_notes_pairs": len(kb | kn), "increase": len(kn - kb) / len(kb)}
json.dump(out, open(REPO / "reports/massime_citations.json", "w"), indent=1)
print(json.dumps(out, indent=1))
