#!/usr/bin/env python3
"""
One-time: move results from the first version (outputs/, logs/, runs.csv at the top level)
into batches/batch_01/ so they're archived with the new layout. Safe to re-run.
"""
import csv, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DEST = ROOT / "batches" / "batch_01"
moved = 0
for sub in ["outputs", "logs"]:
    src = ROOT / sub
    if src.is_dir():
        (DEST / sub).mkdir(parents=True, exist_ok=True)
        for f in src.iterdir():
            target = DEST / sub / f.name
            if not target.exists():
                shutil.move(str(f), target); moved += 1
        if not any(src.iterdir()):
            src.rmdir()

old_csv = ROOT / "runs.csv"
if old_csv.exists():
    rows = list(csv.DictReader(open(old_csv)))
    new_csv = DEST / "runs.csv"
    fields = ["id", "batch", "category", "backend", "model", "status", "input_tokens", "output_tokens",
              "cache_creation_tokens", "cache_read_tokens", "cost_usd", "duration_s",
              "html_bytes", "html_lines", "timestamp"]
    write_header = not new_csv.exists()
    DEST.mkdir(parents=True, exist_ok=True)
    with open(new_csv, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if write_header:
            w.writeheader()
        for r in rows:
            r["batch"] = "batch_01"
            w.writerow(r)
    old_csv.rename(ROOT / "runs_v1_backup.csv")
    print(f"Migrated {len(rows)} log rows (backup kept as runs_v1_backup.csv)")
print(f"Moved {moved} files into {DEST}")
