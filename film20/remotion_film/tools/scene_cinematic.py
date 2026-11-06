#!/usr/bin/env python3
"""Opening cinematic revision SAMPLE (n001-n017). Picture re-cut only: narration, timing and all sources unchanged.
Writes edition20/scene_tests/cinematic_v2.json and src/film/data/film_timeline_cinematic_v2.json (main timeline untouched)."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_manifest import c, g, h, F  # noqa: E402
R = Path(__file__).resolve().parent.parent
CUTS = {
 "n001": [c("garage_env", F)],
 "n002": [c("garage_env", 1.9), c("ivy_crouch", F, inn=0.0)],                     # cut on "crouched": establishing once, 5.4 s
 "n003": [c("ivy_crouch", 1.4),                                                    # "I looked over the hood": her reaction continues
          c("aftermath_wide", 2.8, inn=0.0),                                       # "A man was sliding down..."
          c("frankie_hand", 2.2, inn=0.2),                                         # cut on "a gun a foot from his open hand"
          c("nico_hands", 7.0, inn=0.0),                                           # "...held a different gun, in his left hand. His right arm..."
          h(F, inn=0.0, rate=0.85, memory=True,                                    # triggered flashback, 30 minutes earlier
            why="'in bay fourteen, with my own two hands': the splint she built at 3:40, triggered by the splint she sees")],
 "n005": [c("ivy_frozen", 1.6, inn=4.0, why="'I went back inside': Ivy turns toward the stairwell door (replaces a second establishing shot)"),
          c("emerald_on", F, inn=0.2, memory=True, why="flash-forward: 'Three days later I married him'")],
 "n006": [c("er_entrance", 9.4, inn=0.0, rate=0.85), c("ivy_walks", 3.3, inn=0.3), g("CODE_EHR", F, beat="arrival")],
 "n009": [c("bay_hands", 2.6), c("nico_bay_cu", F)],
}
d = {"tag": "cinematic_v2", "segments": ["n001", "n017"], "segment_cuts": CUTS}
f = R / "edition20/scene_tests/cinematic_v2.json"; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(json.dumps(d, indent=1))
r = subprocess.run([sys.executable, str(R / "tools/film_build.py"), "--variant", str(f)], cwd=R, capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-800:]); sys.exit(r.returncode)
