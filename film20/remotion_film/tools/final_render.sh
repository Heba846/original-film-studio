#!/usr/bin/env bash
# One final full render. Refuses unless every picture/narration requirement is met (build gate open).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/film_build.py >/dev/null || true
python3 - <<'PY'
import json, sys
g = json.load(open("src/film/data/film_timeline.json"))["gate"]
if not g["final_export_allowed"]:
    sys.exit(f"BLOCKED: {len(g['visual_shots_pending'])} shots pending, {len(g['audio_missing'])} narration missing, "
             f"{g['unresolved_frames']} unresolved frames, {len(g['problems'])} problems")
PY
mkdir -p output/final
npx remotion render src/index.tsx Film20-Final output/final/Film20_Final_720p.mp4 --crf=16 --log=error
cp edition20/out/Film20_captions.srt edition20/out/Film20_chapters.txt edition20/out/Film20_chapters.ffmetadata output/final/
python3 tools/verify_final.py output/final/Film20_Final_720p.mp4 --srt output/final/Film20_captions.srt
echo "output/final/Film20_Final_720p.mp4 + captions/chapters (see output/final/VERIFY.json)"
