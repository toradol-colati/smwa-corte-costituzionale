"""Extract citations to Constitutional Court pronunce from the text of pronunce.

A mention is: a type keyword (sentenza, ordinanza, sent., ord., ...) followed by a
list of numbers with their year. The grammar handles lists with the year stated
once ("sentenze n. 26 e n. 320 del 2007", "nn. 26 e 320 del 2007"), mixed years,
the slash form ("n. 26/2007"), missing spaces, and the old date form
("sentenza 26 giugno 1956, n. 1"). Mentions of other courts, of referral orders
and of administrative acts are discarded by a context filter.

Usage: .venv/bin/python src/extract/citations.py
Outputs (see .claude/rules/data.md):
  data/processed/citations.csv, data/processed/edges_citations.csv,
  data/interim/citation_errors.csv, citation_excluded.csv,
  citation_same_date.csv, citation_type_mismatch.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]

MONTHS = "gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre"
KEYWORD = re.compile(
    r"\b(sentenz[ae]|ordinanz[ae]|sentt?\.|ordd?\.|decision[ei]|pronunc(?:e|ia)|pronunzi[ae]|C(?:orte)?\.?\s*cost\.)(?![a-z])", re.I)
# optional words between the keyword and the first number
FILLER = re.compile(
    r"\s*(?:\(|,)?\s*(?:(?:di|della|dalla|nella)\s+(?:questa|stessa)\s+Corte|della\s+Corte(?:\s+costituzionale)?|"
    r"costituzional[ei]|interpretativ[ae](?:\s+di\s+rigetto)?|già\s+citat[ae]|citat[ae]|richiamat[ae]|"
    r"menzionat[ae]|ricordat[ae]|predett[ae]|suddett[ae]|precedent[ei]|anzidett[ae]|medesim[ae]|stess[ae]|"
    r"recent[ei]|additiv[ae]|coev[ae]|successiv[ae]|numer[oi])\s*,?", re.I)
NUM_MARK = re.compile(r"\s*,?\s*(?:nn?\s*[\.,]|numer[oi]|n\b)\s*", re.I)
NUMBER = re.compile(r"\s*(\d{1,4})(?!\d)")
YEAR_FULL = re.compile(
    r"\s*,?\s*(?:del(?:l['’]\s*anno)?|in data|dell['’])\s*(?:\d{1,2}\s*°?\s*(?:%s)\s+)?((?:19|20)\d{2})(?!\d)" % MONTHS, re.I)
YEAR_SLASH = re.compile(r"\s*/\s*((?:19|20)\d{2}|\d{2})(?!\d)")
SEP = re.compile(r"\s*(?:,|;|\be(?:d)?\b|\bnonché\b|\boltre\s+a\b|-)\s*", re.I)
# old form: "sentenza 26 giugno 1956, n. 1" / "sentenza del 5 giugno 1956 n. 1"
DATE_FORM = re.compile(
    r"\s*(?:del(?:l['’])?|in data)?\s*\d{1,2}\s*°?(?:\s*(?:,|e)\s*\d{1,2}\s*°?)*\s*(?:%s)\s+((?:19|20)\d{2})\s*,?\s*(?:nn?\s*\.|numero)\s*(\d{1,4})(?!\d)"
    r"((?:\s*(?:,|e|ed)\s*(?:nn?\s*\.\s*)\d{1,4}(?!\d)(?!\s*(?:del\s+(?:19|20)|/)))*)" % MONTHS, re.I)
SAME_DATE = re.compile(r"\s*,?\s*(?:(?:in|di)\s+pari\s+data|della\s+stessa\s+data|in\s+data\s+odierna)", re.I)

OTHER_COURT = re.compile(
    r"Cassazione|\bCass\.|Consiglio di Stato|Cons\.\s*(?:di\s*)?Stato|\bTAR\b|T\.A\.R\.|Tribunale amministrativo|"
    r"Corte dei conti|Corte EDU|Corte europea|Corte di giustizia|CGUE|CEDU|Corte di Strasburgo|sezioni unite|"
    r"sez(?:ione|\.)\s+(?:un|[IVX]+\b|prima|seconda|terza|quarta|quinta|sesta|lavoro|penale|civile)|adunanza plenaria|"
    r"Corte suprema|Corte d['’]\s*appello|Tribunale|Pretore|Pretura|giudice di pace|Giudice per le indagini|"
    r"giudice\s+(?:a quo|rimettente|istruttore|tutelare|conciliatore)|Commissione tributaria|Corte di assise|"
    r"Corte militare|Conseil|Bundesverfassungsgericht|protezione civile|ministerial[ei]|sindacal[ei]|"
    r"Presidente del Consiglio dei ministri n\.|ordinanza[- ]ingiunzione|Collegio arbitrale|Alta Corte", re.I)
COURT_NAME = re.compile(
    r"Cassazione|\bCass\.|Consiglio di Stato|Cons\.\s*(?:di\s*)?Stato|\bTAR\b|T\.A\.R\.|Tribunale amministrativo|"
    r"Corte dei conti|Corte EDU|Corte europea|Corte di giustizia|CGUE|Corte di Strasburgo|sezioni unite|sez\.\s*un|"
    r"adunanza plenaria|Corte suprema|Corte d['’]\s*appello|Corte di assise|Corte militare|Commissione tributaria|"
    r"Tribunale(?:\s+(?:ordinario|militare|superiore))?\s+d|Pretore di|Giudice di pace di|Alta Corte|"
    r"protezione civile|ministerial[ei]|sindacal[ei]|ordinanza[- ]ingiunzione", re.I)
CLAUSE_BREAK = re.compile(r"[;»):]|\bche\b|\. ")
OWN_COURT = re.compile(r"questa Corte|Corte costituzionale|la Corte ha|della Corte\b(?! d[ei])|giurisprudenza costituzionale", re.I)
REFERRAL = re.compile(
    r"reg(?:istro|\.)\s*ord|\br\.\s*o\.|registro ordinanze|registro ricorsi|reg\.\s*ric|iscritt[ae] a[il] n|"
    r"\bemess[ae]\s+(?:il|in data|dal|dalla)|\bpronunciat[ae]\s+(?:il|dal|dalla)\b|di rimessione|di rinvio|"
    r"Gazzetta Ufficiale|\bG\.\s*U\.|ordinanz[ae]\s+in epigrafe|ordinanz[ae]\s+indicat[ae]|atto di promovimento", re.I)


def find_mentions(text: str, default_year: int | None = None) -> list[dict]:
    """All candidate (kind, number, year) mentions with character offsets and the
    reason for exclusion, if any."""
    out = []
    for kw in KEYWORD.finditer(text):
        kind = kw.group(1).lower()[:3]
        pos = kw.end()
        items: list[tuple[int, int | None, int, int]] = []  # number, year, start, end
        m = DATE_FORM.match(text, pos)
        if m:
            while m:
                items.append((int(m.group(2)), int(m.group(1)), kw.start(), m.end()))
                for extra in re.findall(r"\d{1,4}", m.group(3) or ""):
                    items.append((int(extra), int(m.group(1)), kw.start(), m.end()))
                pos = m.end()
                s2 = SEP.match(text, pos)
                m = DATE_FORM.match(text, s2.end()) if s2 and s2.end() > pos else None
                while m is None and s2 and s2.end() > pos:  # ", e 30 ottobre ..."
                    s3 = SEP.match(text, s2.end())
                    if not s3 or s3.end() == s2.end():
                        break
                    m, s2 = DATE_FORM.match(text, s3.end()), s3
        else:
            while True:
                f = FILLER.match(text, pos)
                if f and f.end() > pos:
                    pos = f.end()
                else:
                    break
        pending: list[int] = []  # indexes of items waiting for a year
        first = not items
        while True:
            start = pos
            mark = NUM_MARK.match(text, pos)
            if mark:
                pos = mark.end()
            elif first:
                # the first number must be introduced by n./nn., except "sent. 174/1972"
                if not re.match(r"\s*\d{1,4}\s*/\s*(?:19|20)\d{2}(?!\d)", text[pos:pos + 14]):
                    break
            num = NUMBER.match(text, pos)
            if not num:
                pos = start
                break
            if not mark and not (first and not items):
                # a bare number continues a list only if a year follows it somewhere
                # ("nn. 26 e 320 del 2007") or the previous item was also bare
                look = text[num.end():num.end() + 60]
                if not re.match(r"(?:\s*(?:,|e|ed)\s*(?:nn?\.\s*)?\d{1,4})*\s*,?\s*(?:del\s+(?:19|20)\d{2}|/\s*\d{2})", look):
                    pos = start
                    break
            n = int(num.group(1))
            pos = num.end()
            year = None
            y = YEAR_SLASH.match(text, pos) or YEAR_FULL.match(text, pos)
            if y:
                year = int(y.group(1))
                if year < 100:
                    year += 1900 if year >= 56 else 2000
                pos = y.end()
            elif default_year and SAME_DATE.match(text, pos):
                year = default_year
                pos = SAME_DATE.match(text, pos).end()
            items.append((n, year, kw.start(), pos))
            if year is None:
                pending.append(len(items) - 1)
            else:
                for i in pending:
                    items[i] = (items[i][0], year, items[i][2], items[i][3])
                pending = []
            first = False
            sep = SEP.match(text, pos)
            if not sep or sep.end() == pos:
                break
            # allow "e" + "n." or bare number; stop at a new keyword
            if KEYWORD.match(text, sep.end()):
                break
            pos = sep.end()
        if not items:
            continue
        before = text[max(0, kw.start() - 140):kw.start()]
        cut = max(before.rfind(". "), before.rfind("; "))
        ctx_before = before[cut + 1:] if cut >= 0 else before
        after = text[items[-1][3]:items[-1][3] + 70]
        reason = ""
        near = text[max(0, kw.start() - 75):kw.start()]
        oc = [m.end() for m in COURT_NAME.finditer(near)]
        own = [m.end() for m in OWN_COURT.finditer(near)]
        prev = out[-1] if out else None
        if oc and (not own or max(oc) > max(own)) and not CLAUSE_BREAK.search(near[max(oc):]):
            reason = "other_court_before"
        elif (prev and prev["excluded"] == "other_court_before" and 0 <= kw.start() - prev["char_end"] <= 12
              and not CLAUSE_BREAK.search(text[prev["char_end"]:kw.start()].replace(";", ""))):
            reason = "other_court_before"
        elif re.match(r"\s*,?\s*(?:\)|,)?\s*(?:del(?:la|le|l['’])?|dal(?:la|l['’])?|emess[ae] dal(?:la)?|res[ae] dal(?:la)?|pronunciat[ae] dal(?:la)?)\s*(?:Corte di\s+)?(?:%s)" % OTHER_COURT.pattern, after, re.I):
            reason = "other_court_after"
        elif (re.search(r"reg(?:istro|\.)?\s*(?:ord|ric)|\br\.\s*o\.?\s*$|\br\.\s*$", text[max(0, kw.start() - 14):kw.end()], re.I)
              or REFERRAL.search(text[kw.start():items[-1][3]])
              or re.match(r"\s*,?\s*(?:del\s+)?(?:reg(?:istro|\.)\s*ord|registro ordinanze|r\.\s*o\.)", after, re.I)):
            reason = "referral_order"
        for n, year, s, e in items:
            out.append({"kind": kind, "number": n, "year": year, "char_start": s, "char_end": e,
                        "raw_match": text[s:e], "excluded": reason if year else "no_year"})
    return out


def run() -> None:
    df = pd.read_pickle(REPO / "data" / "interim" / "pronunce.pkl")
    deposit = dict(zip(df.pid, df.data_deposito))
    kind_of = dict(zip(df.pid, df.tipo))
    rows = []
    for r in df.itertuples():
        for section in ["intro", "fatto", "diritto", "dispositivo"]:
            for m in find_mentions(getattr(r, section) or "", default_year=r.anno):
                m.update(citing_id=r.pid, section=section)
                rows.append(m)
    c = pd.DataFrame(rows)
    c["cited_id"] = (c.year.fillna(0) * 10000 + c.number).astype("int64")
    c["exists"] = c.cited_id.isin(deposit)
    c["citing_dep"] = c.citing_id.map(deposit)
    c["cited_dep"] = c.cited_id.map(deposit)
    c["status"] = "ok"
    c.loc[c.excluded != "", "status"] = "excluded"
    ok = c.status == "ok"
    c.loc[ok & ~c.exists, "status"] = "error_missing"
    c.loc[ok & c.exists & (c.cited_dep > c.citing_dep), "status"] = "error_future"
    c.loc[ok & c.exists & (c.cited_id == c.citing_id), "status"] = "error_self"
    c.loc[(c.status == "ok") & (c.cited_dep == c.citing_dep), "status"] = "same_date"
    c["type_mismatch"] = c.exists & (c.kind.isin(["sen", "ord"])) & (
        c.kind.map({"sen": "S", "ord": "O"}) != c.cited_id.map(kind_of))
    interim, proc = REPO / "data" / "interim", REPO / "data" / "processed"
    cols = ["citing_id", "cited_id", "raw_match", "section", "char_start", "char_end", "kind", "status", "type_mismatch"]
    c[c.status == "excluded"][cols + ["excluded"]].to_csv(interim / "citation_excluded.csv", index=False)
    c[c.status.str.startswith("error")][cols].to_csv(interim / "citation_errors.csv", index=False)
    c[c.status == "same_date"][cols].to_csv(interim / "citation_same_date.csv", index=False)
    good = c[c.status.isin(["ok", "same_date"])]
    good[good.type_mismatch][cols].to_csv(interim / "citation_type_mismatch.csv", index=False)
    good[cols].to_csv(proc / "citations.csv", index=False)
    for name, sections in [("edges_citations", ["diritto", "dispositivo"]),
                           ("edges_citations_fulltext", ["intro", "fatto", "diritto", "dispositivo"])]:
        g = good[good.section.isin(sections) & (good.status == "ok")]
        g.groupby(["citing_id", "cited_id"]).size().rename("n_mentions").reset_index().to_csv(proc / f"{name}.csv", index=False)
    print(c.status.value_counts().to_string())
    print("excluded reasons:", c[c.status == "excluded"].excluded.value_counts().to_dict())
    base = good[good.section.isin(["diritto", "dispositivo"]) & (good.status == "ok")]
    print("base-text edges:", base.drop_duplicates(["citing_id", "cited_id"]).shape[0],
          "citing:", base.citing_id.nunique(), "type mismatch share:", round(base.type_mismatch.mean(), 4))


if __name__ == "__main__":
    run()
