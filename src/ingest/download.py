"""Download the Constitutional Court open data archives into data/raw/.

Every downloaded file is recorded in data/raw/MANIFEST.csv with its URL,
download time (UTC) and SHA-256, because the portal is updated weekly and the
manifest is the only record of which data version produced the results.

Archives are extracted next to the zip, each into its own directory, refusing
any member whose path would escape that directory.

Usage (from the repository root):
    python3 -I src/ingest/download.py            # all datasets
    python3 -I src/ingest/download.py giudici    # one group
"""

from __future__ import annotations

import csv
import hashlib
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://dati.cortecostituzionale.it/opendata"

# Source page: https://dati.cortecostituzionale.it/Scarica_i_dati/Scarica_i_dati
# XML is used for every archive: the CSV/JSON massime stop at 2015.
DATASETS: dict[str, list[str]] = {
    "pronunce": [
        f"{BASE}/distribuzione/CC_OpenPronunce_1956_1980.zip",
        f"{BASE}/distribuzione/CC_OpenPronunce_1981_2000.zip",
        f"{BASE}/distribuzione/CC_OpenPronunce_2001_oggi.zip",
    ],
    "massime": [
        f"{BASE}/distribuzione/CC_OpenMassime_1956_1980.zip",
        f"{BASE}/distribuzione/CC_OpenMassime_1981_2000.zip",
        f"{BASE}/distribuzione/CC_OpenMassime_2001_oggi.zip",
    ],
    "giudici": [
        f"{BASE}/Anagrafica_giudici/Cc_Opendata_AnagraficaGiudici.zip",
    ],
}

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFEST = RAW_DIR / "MANIFEST.csv"
MANIFEST_FIELDS = ["file", "url", "downloaded_at", "sha256"]
USER_AGENT = "smwa-corte-costituzionale/0.1 (academic research)"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    partial = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)
    partial.replace(target)


def safe_extract(archive: Path, destination: Path) -> list[str]:
    """Extract archive into destination; yearly archives nested inside are
    extracted too, so destination ends up holding one XML per year."""
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    names = []
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            out_path = (destination / member.filename).resolve()
            if root != out_path and root not in out_path.parents:
                raise ValueError(f"Unsafe path in {archive.name}: {member.filename}")
            names.append(member.filename)
        zf.extractall(destination)
    for inner in [destination / name for name in names if name.lower().endswith(".zip")]:
        names.extend(safe_extract(inner, destination))
        inner.unlink()
    return names


def append_manifest(rows: list[dict[str, str]]) -> None:
    new_file = not MANIFEST.exists()
    with MANIFEST.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)


def main(groups: list[str]) -> None:
    unknown = set(groups) - DATASETS.keys()
    if unknown:
        sys.exit(f"Unknown dataset group(s): {', '.join(sorted(unknown))}")
    rows = []
    for group in groups:
        group_dir = RAW_DIR / group
        group_dir.mkdir(parents=True, exist_ok=True)
        for url in DATASETS[group]:
            target = group_dir / url.rsplit("/", 1)[1]
            print(f"Downloading {url}", flush=True)
            download(url, target)
            checksum = sha256_of(target)
            members = safe_extract(target, group_dir / target.stem)
            print(f"  {target.stat().st_size:,} bytes, sha256 {checksum[:12]}…, {len(members)} file(s)")
            rows.append({
                "file": str(target.relative_to(REPO_ROOT)),
                "url": url,
                "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "sha256": checksum,
            })
    append_manifest(rows)
    print(f"Manifest updated: {MANIFEST.relative_to(REPO_ROOT)} (+{len(rows)} rows)")


if __name__ == "__main__":
    main(sys.argv[1:] or list(DATASETS))
