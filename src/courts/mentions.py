"""Records of the references to other courts in the base text (Considerato in diritto and dispositivo) of the
Constitutional Court's pronunce: one row per mention, independent of the unit of the court network, which is
chosen at analysis time (court or single decision). Each row: court, role of the mention, whether a decision
identifier is written nearby, the identifier as written, the context.
Rules are written by reading only the development half of the pronunce (data/interim/courts_split.csv,
seed 20261123, fixed by sizing.py). The test half is read only after the rules are frozen and registered in
docs/decisions.md: until RULES_FROZEN is True, `--half test` refuses to run.
Rules: version 1 (role of the mention: citation, referring court, preliminary reference to the Court of Justice, other;
identifiers that need a date or a decision word next to the number), written on the development half; not frozen.
Outputs: data/interim/courts_mentions_<half>.csv; with --sheet, data/interim/courts_dev_sheet.md (random
development mentions to read while writing the rules).
Usage: .venv/bin/python src/courts/mentions.py [--half dev|test] [--sheet]
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RULES_FROZEN = False
RULES_VERSION = 2
WINDOW = 300  # characters after the mention searched for an identifier, cut at the end of the sentence
COURTS = {  # capital or small initial on the words after "Corte"/"Consiglio": both are written
    "Cassazione": r"Corte (?:[Ss]uprema )?di [Cc]assazione|\bCassazione\b|\bCass\.",
    "Corte EDU": r"Corte [Ee]uropea dei [Dd]iritti dell['’][Uu]omo|Corte EDU|Corte di Strasburgo|Corte [Ee]uropea dei [Dd]iritti [Uu]mani",
    "Corte di giustizia UE": r"Corte di [Gg]iustizia(?! amministrativa)|CGUE|Corte di Lussemburgo",
    "Consiglio di Stato": r"Consiglio di [Ss]tato|Cons\. ?Stato",
}
MONTH = r"(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)"
DATE = rf"\d{{1,2}}\s+{MONTH}\s+\d{{4}}"
DATE_RANGE = rf"(?:\d{{1,2}}(?:\s+{MONTH})?\s*-\s*)?{DATE}"  # "7 giugno-22 luglio 2013": decision and deposit
NUM = r"(?:n\.|nn\.|numero)\s*\d{1,6}(?:\s*(?:/|del)\s*\d{2,4})?"
DECISION = r"(?:sentenz[ae]|ordinanz[ae]|decreto|decision[ei]|sent\.|ord\.)"
# identifier: date and number, or a decision word right before the number, or (Consiglio di Stato) an opinion with its date
IDENT_IT = rf"{DATE_RANGE}\s*,?\s*{NUM}|{DECISION}\s+{NUM}|parere\s+(?:{NUM}\s+)?(?:del\s+)?{DATE}"
CAP = r"[A-ZÀ-Ý][\w'’.\-]*"
# identifiers in order of strength: the first pattern that matches in the window wins (number or case name before a bare date)
IDENT = {
    "Cassazione": [("numero", IDENT_IT)],
    "Consiglio di Stato": [("numero", IDENT_IT)],
    "Corte di giustizia UE": [("numero di causa", r"\b[CT]-\d{1,4}[/-]\d{2}|caus[ae]\s+(?:riunite\s+)?(?:C-)?\d{1,4}[/-]\d{2}"),
                              ("data", rf"sentenz[ae]\s+(?:del\s+)?{DATE}")],
    "Corte EDU": [("nome del caso", rf"{CAP}(?:\s+{CAP}){{0,4}}\s+(?:c\.|contro|v\.)\s+{CAP}(?:\s+{CAP}){{0,2}}"),
                  ("numero di ricorso", r"ricors[oi]\s+n\.\s*\d{3,6}/\d{2}"),
                  ("data", rf"sentenz[ae]\s+(?:del\s+)?{DATE}")],
}
# role of the mention, checked in this order
REFERRING_AFTER = r"^\s*(?:,\s*(?:sezione|sez\.)[^,;.]{1,40},?\s*)?(?:rimettente|rimettenti|a quo)\b|^[^.;]{0,90}?(?:con l['’]ordinanz[ae]|con ordinanz[ae]|in epigrafe)"
REFERRING_BEFORE = (r"(?:sollevat[aeio]|promoss[aeio]|rimess[aeio]|proposti?|introdott[aeio])\s+(?:[^.;]{0,60}?\s)?dal(?:la|le|l['’])?\s*$|"
                    r"ordinanz[ae] di rimessione[^.;]{0,90}?(?:emess[aeio]|pronunciat[aeio]|adottat[aeio])\s+dal(?:la|le|l['’])?\s*$")
RINVIO = r"rinvio pregiudiziale|questione pregiudiziale|rinvi\w* alla Corte di giustizia|interpretazione pregiudiziale"
CASELAW = (r"giurisprudenz|orientament|indirizz|secondo (?:la|il)|come (?:rilevato|affermato|chiarito|precisato|ritenuto|osservato)|"
           r"interpretazion|sentenz|pronunc|decision|ordinanz|ha (?:affermato|chiarito|ritenuto|stabilito|precisato|escluso)|"
           r"sezioni unite|diritto vivente|massim|criteri|principi|ricostruzion|letto|lettura|elaborat|interpretat")


def role_of(court, text, m, has_ident):
    before, after = text[max(0, m.start() - 160): m.start()], text[m.end(): m.end() + 160]
    if court in ("Cassazione", "Consiglio di Stato") and (re.search(REFERRING_AFTER, after) or re.search(REFERRING_BEFORE, before)):
        return "giudice rimettente"
    if court == "Corte di giustizia UE" and re.search(RINVIO, before + " " + after):
        return "rinvio pregiudiziale"
    if has_ident or re.search(CASELAW, before[-120:] + " " + after[:120], flags=re.I):
        return "citazione"
    return "altro"


def records(df):
    rows = []
    for r in df.itertuples():
        text = r.base
        for court, rx in COURTS.items():
            for m in re.finditer(rx, text):
                after = text[m.end(): m.end() + WINDOW]
                cut = re.search(r"[.;](?:\s|$)(?![^()]*\))", after)  # end of sentence, not inside parentheses
                win = after[: cut.start()] if cut else after
                ident, kind = None, ""
                for kind_, rx_ in IDENT[court]:
                    ident = re.search(rx_, win)
                    if ident:
                        kind = kind_
                        break
                rows.append({"pid": r.pid, "anno": r.anno, "tipo": r.tipo, "court": court, "start": m.start(), "matched": m.group(),
                             "role": role_of(court, text, m, ident is not None),
                             "identified": ident is not None, "identifier_kind": kind, "identifier_raw": ident.group().strip() if ident else "",
                             "context": text[max(0, m.start() - 150): m.end() + WINDOW].replace("\n", " ")})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--half", default="dev", choices=["dev", "test"])
    ap.add_argument("--sheet", action="store_true")
    a = ap.parse_args()
    if a.half == "test" and not RULES_FROZEN:
        raise SystemExit("The test half stays unread until the rules are frozen and registered in docs/decisions.md.")
    split = pd.read_csv(REPO / "data/interim/courts_split.csv")
    keep = set(split.pid[split.half == a.half])
    df = pd.read_pickle(REPO / "data/interim/pronunce.pkl")
    df = df[df.pid.isin(keep)].copy()
    df["base"] = df.diritto.fillna("") + " " + df.dispositivo.fillna("")
    rec = records(df)
    rec.to_csv(REPO / f"data/interim/courts_mentions_{a.half}.csv", index=False)
    print(f"{a.half} half: {len(df):,} pronunce, {len(rec):,} mentions (rules version {RULES_VERSION})")
    print(rec.groupby("court").agg(mentions=("pid", "size"), pronunce=("pid", "nunique"), identified=("identified", "mean")).round(3))
    print(pd.crosstab(rec.court, rec.role))
    if a.sheet and a.half == "dev":
        rng = np.random.default_rng(20261124)
        out = ["# Menzioni di altre corti, metà di sviluppo (per scrivere le regole)\n",
               f"Regole versione {RULES_VERSION}. 40 menzioni a caso per corte (seed 20261124). Per ognuna: è un riferimento alla corte? "
               "Il ruolo è giusto? Se nomina una decisione, l'identificativo estratto è giusto e completo?\n"]
        for court, g in rec.groupby("court"):
            out.append(f"\n## {court}\n")
            for i, (_, x) in enumerate(g.iloc[rng.permutation(len(g))[:40]].iterrows(), 1):
                out.append(f"{i}. pronuncia {x.pid} · ruolo: {x.role} · identificativo: `{x.identifier_raw or '—'}`\n   > {x.context}\n")
        (REPO / "data/interim/courts_dev_sheet.md").write_text("\n".join(out))
        print("sheet: data/interim/courts_dev_sheet.md")


if __name__ == "__main__":
    main()
