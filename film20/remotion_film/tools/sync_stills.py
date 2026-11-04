#!/usr/bin/env python3
"""Copy QA-approved stills (edition20/review/still_qa.json) into public/stills/ and write
src/film/data/approved_stills.json. Workbench-only animatic fallback: strict/Final renders never use stills."""
import json, shutil
from pathlib import Path
R = Path(__file__).resolve().parent.parent
Q = json.loads((R / "edition20/review/still_qa.json").read_text())
dst = R / "public/stills"; dst.mkdir(parents=True, exist_ok=True)
out = {}
for jid in sorted(Q["approved"]):
    src = R / f"edition20/stills_approved/STILL_{jid}.jpg"
    if src.exists():
        shutil.copy(src, dst / src.name); out[jid] = f"stills/{src.name}"
(R / "src/film/data/approved_stills.json").write_text(json.dumps(out, indent=1))
print(len(out), "approved stills synced; missing files:", [j for j in Q["approved"] if j not in out])
