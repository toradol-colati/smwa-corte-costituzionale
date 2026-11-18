"""Parse the raw XML into one table of pronunce with whitespace-normalised text
sections. Output: data/interim/pronunce.pkl (with texts, not versioned) and
data/processed/pronunce.csv (metadata only).

Sections:
  sentenze   fatto  = text between the <fatto> and <diritto> markers
             diritto = text after the <diritto> marker
  ordinanze  the reasoning sits in <epigrafe>; it is split at the first
             "Considerato che" (or equivalent opening, see ORD_SPLIT)
  dispositivo  as in the XML, with the signature block cut off

Usage: .venv/bin/python src/ingest/build_pronunce.py
"""

from __future__ import annotations

import glob
import re
from pathlib import Path

import pandas as pd
from lxml import etree

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "data" / "raw"
HEADER = ["anno_pronuncia", "numero_pronuncia", "tipologia_pronuncia", "presidente",
          "relatore_pronuncia", "redattore_pronuncia", "data_decisione", "data_deposito"]

WS = re.compile(r"\s+")
# opening of the Court's own reasoning in ordinanze
ORD_SPLIT = re.compile(r"\b[Cc]onsiderato[,:]?\s+(?:in diritto|(?:[a-zà-ù]+,?\s+){0,3}che)\b|\bCONSIDERATO[,:]?\s+(?:IN DIRITTO|CHE)\b")
SENT_SPLIT = re.compile(r"\b[Cc]onsiderato[,:]?\s+in\s+diritto\b|\bCONSIDERATO[,:]?\s+IN\s+DIRITTO\b")
# where the signature block starts inside <dispositivo>
SIGN = re.compile(r"\b(?:Cos[iìí]'?\s+deciso|F\.to\s*:)", re.I)


def norm(text: str | None) -> str:
    return WS.sub(" ", text or "").strip()


def itertext(el) -> str:
    return "".join(el.itertext()) if el is not None else ""


def split_testo(testo) -> tuple[str, str, bool]:
    """Return (fatto, diritto, tagged)."""
    if testo is None:
        return "", "", False
    pre, fatto, diritto, where = [testo.text or ""], [], [], "pre"
    for child in testo:
        if child.tag == "fatto":
            where = "fatto"
        elif child.tag == "diritto":
            where = "diritto"
        {"pre": pre, "fatto": fatto, "diritto": diritto}[where].append(child.tail or "")
    tagged = bool(diritto)
    return norm("".join(pre) + " " + "".join(fatto)), norm("".join(diritto)), tagged


def main() -> None:
    rows = []
    for path in sorted(glob.glob(str(RAW / "pronunce" / "*" / "*.xml"))):
        for p in etree.parse(path).getroot().iter("pronuncia"):
            head, body = p.find("pronuncia_testata"), p.find("pronuncia_testo")
            r = {k: (head.findtext(k) or "").strip() for k in HEADER}
            r["collegio"] = norm(itertext(body.find("collegio")))
            epigrafe = norm(itertext(body.find("epigrafe")))
            fatto, diritto, tagged = split_testo(body.find("testo"))
            dispositivo_full = norm(itertext(body.find("dispositivo")))
            m = SIGN.search(dispositivo_full)
            r["dispositivo"] = dispositivo_full[:m.start()] if m else dispositivo_full
            r["firme"] = dispositivo_full[m.start():] if m else ""
            split_how = "tags" if tagged else ""
            if r["tipologia_pronuncia"] == "S":
                if not tagged:
                    whole = norm(itertext(body.find("testo")))
                    m2 = SENT_SPLIT.search(whole)
                    if m2:
                        fatto, diritto, split_how = whole[:m2.start()], whole[m2.end():], "regex"
                    else:
                        fatto, diritto, split_how = "", whole, "none"
                r["intro"] = epigrafe
            else:
                whole = (epigrafe + " " + fatto + " " + diritto).strip()
                m2 = ORD_SPLIT.search(whole)
                if m2:
                    r["intro"], fatto, diritto, split_how = "", whole[:m2.start()], whole[m2.end():], "regex"
                else:
                    r["intro"], fatto, diritto, split_how = "", "", whole, "none"
            r.update(fatto=fatto, diritto=diritto, split_how=split_how)
            rows.append(r)
    df = pd.DataFrame(rows)
    df["anno"] = df.anno_pronuncia.astype(int)
    df["num"] = df.numero_pronuncia.astype(int)
    df["pid"] = df.anno * 10000 + df.num
    df["tipo"] = df.tipologia_pronuncia
    for c in ["data_decisione", "data_deposito"]:
        df[c] = pd.to_datetime(df[c], format="%d/%m/%Y", errors="coerce")
    # data fixes documented in reports/data_inspection.md
    bad = df.data_deposito.dt.year != df.anno
    df.loc[bad, "data_deposito"] = pd.NaT
    df["data_deposito"] = df.groupby("anno").data_deposito.transform(lambda s: s.ffill().bfill())
    df = df.sort_values(["data_deposito", "pid"]).reset_index(drop=True)
    (REPO / "data" / "interim").mkdir(parents=True, exist_ok=True)
    df.to_pickle(REPO / "data" / "interim" / "pronunce.pkl")
    meta = df[["pid", "anno", "num", "tipo", "presidente", "relatore_pronuncia", "redattore_pronuncia",
               "data_decisione", "data_deposito", "split_how"]].copy()
    for c in ["fatto", "diritto", "dispositivo"]:
        meta["len_" + c] = df[c].str.len()
    meta.to_csv(REPO / "data" / "processed" / "pronunce.csv", index=False)
    print(len(df), "pronunce")
    print(pd.crosstab([df.tipo, df.anno // 10 * 10], df.split_how).to_string())


if __name__ == "__main__":
    main()
