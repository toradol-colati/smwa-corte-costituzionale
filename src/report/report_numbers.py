"""Numbers quoted in the report that no analysis script stores elsewhere (text preparation,
extraction counts). Every other number of the report is read from reports/*.json.
Output: reports/numbers.json
Usage: .venv/bin/python src/report/report_numbers.py
"""
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
P, I = REPO / "data/processed", REPO / "data/interim"
pr = pd.read_csv(P / "pronunce.csv", usecols=["pid", "tipo", "split_how"])
c = pd.read_csv(P / "citations.csv", usecols=["status", "type_mismatch"])
fail = pr[pr.split_how == "none"]
out = {
    "pronunce": int(len(pr)),
    "split_failed": int(len(fail)), "split_failed_share": float(len(fail) / len(pr)),
    "split_failed_by_type": {k: int(v) for k, v in fail.tipo.value_counts().items()},
    "mentions_valid": int(len(c)), "mentions_same_date": int((c.status == "same_date").sum()),
    "mentions_excluded": int(len(pd.read_csv(I / "citation_excluded.csv", usecols=["status"]))),
    "mentions_errors": int(len(pd.read_csv(I / "citation_errors.csv", usecols=["status"]))),
    "type_mismatch_share": float(c[c.status == "ok"].type_mismatch.mean()),
}
# pronunce without massime have no topic and are left out of D3 (citing and cited)
import numpy as np  # noqa: E402
theta_pid = set(np.load(P / "topics_theta.npz")["pid"])
nt = pr[~pr.pid.isin(theta_pid)]
out["pronunce_without_topic"] = int(len(nt))
out["pronunce_without_topic_by_type"] = {k: int(v) for k, v in nt.tipo.value_counts().items()}
# why they have no topic: no massime at all, or only massime of 50 characters or less (topics.py
# drops them), which are cross-references to another massima ("Ved. ord. 84/57 B.")
import glob  # noqa: E402
from lxml import etree  # noqa: E402
maxlen = {}
for path in sorted(glob.glob(str(REPO / "data/raw/massime/*/*.xml"))):
    for p_ in etree.parse(path).getroot().iter("pronuncia"):
        h = p_.find("pronuncia_testata")
        pid = int(h.findtext("anno_pronuncia")) * 10000 + int(h.findtext("numero_pronuncia"))
        lens = [len((m.findtext("testo") or "").strip()) for m in p_.findall("massime/massima")]
        maxlen[pid] = max(lens) if lens else -1
ml = nt.pid.map(maxlen).fillna(-1)
short, none_ = nt[ml >= 0], nt[ml < 0]
out["without_topic_short_massime"] = int(len(short))
out["without_topic_short_massime_years"] = [int(short.pid.min() // 10000), int(short.pid.max() // 10000)] if len(short) else []
out["without_topic_no_massime"] = int(len(none_))
out["without_topic_no_massime_2026"] = int((none_.pid // 10000 == 2026).sum())
# completeness: the last year is partial (download of 8/11/2026)
nd = pd.read_csv(P / "nodes.csv", usecols=["pid", "anno", "data_deposito"])
last = nd[nd.anno == nd.anno.max()]
out["last_year"] = {"year": int(last.anno.iloc[0]), "pronunce": int(len(last)), "last_number": int((last.pid % 10000).max()),
                    "last_deposit": str(last.data_deposito.max())}
# D3: how much of the self-drafted effect goes away at equal challenged provision, on two scales
d3 = json.load(open(REPO / "reports/d3_results.json"))
sd = d3["primary"]["coef"]["self_drafted"]["or"]
sn = d3["variants"]["controllo per norma impugnata in comune (esplorativo)"]["coef"]["self_drafted"]["or"]
out["d3_self_drafted_scale"] = {"excess_before": sd - 1, "excess_after": sn - 1, "excess_reduction": 1 - (sn - 1) / (sd - 1),
                                "log_reduction": 1 - float(np.log(sn) / np.log(sd))}
json.dump(out, open(REPO / "reports/numbers.json", "w"), indent=1)
print(out)
