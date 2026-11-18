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
json.dump(out, open(REPO / "reports/numbers.json", "w"), indent=1)
print(out)
