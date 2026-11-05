#!/usr/bin/env bash
# Delivery copy of the verified CRF16 master: <480 MiB, faststart, H.264 1280x720 24 fps, AAC copied unchanged.
set -euo pipefail
cd "$(dirname "$0")/.."
M=output/final/Film20_Final_720p.mp4; O=output/final/delivery; mkdir -p $O
LIM=$((480*1024*1024))
sz=$(stat -c %s $M)
if [ "$sz" -lt "$LIM" ]; then
  ffmpeg -v error -y -i $M -c copy -movflags +faststart $O/Film20_Final_720p_delivery.mp4; echo "master under limit: remuxed with faststart"
else
  for crf in 18 20; do
    ffmpeg -v error -y -i $M -map 0:v:0 -map 0:a:0 -c:v libx264 -preset fast -crf $crf -pix_fmt yuv420p -r 24 -c:a copy -movflags +faststart $O/Film20_Final_720p_delivery.mp4
    s=$(stat -c %s $O/Film20_Final_720p_delivery.mp4); echo "crf $crf -> $s bytes"
    [ "$s" -lt "$LIM" ] && break
  done
fi
D=$O/Film20_Final_720p_delivery.mp4
python3 - "$M" "$D" <<'PY'
import json, subprocess, sys, hashlib
m, d = sys.argv[1:]
def pr(p): return json.loads(subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p],capture_output=True,text=True).stdout)
def nf(p): return int(subprocess.run(["ffprobe","-v","error","-count_packets","-select_streams","v:0","-show_entries","stream=nb_read_packets","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip().strip(","))
def apk(p): return hashlib.sha256(subprocess.run(["ffmpeg","-v","error","-i",p,"-map","0:a:0","-c","copy","-f","adts","-"],capture_output=True).stdout).hexdigest()
A, B = pr(m), pr(d)
va = next(s for s in B["streams"] if s["codec_type"]=="video"); aa = next(s for s in B["streams"] if s["codec_type"]=="audio")
dec = subprocess.run(["ffmpeg","-v","error","-i",d,"-f","null","-"],capture_output=True,text=True).stderr.strip()
moov_first = open(d,"rb").read(64*1024).find(b"moov") != -1
r = {"master": {"bytes": int(A["format"]["size"]), "frames": nf(m), "dur_s": float(A["format"]["duration"])},
     "delivery": {"bytes": int(B["format"]["size"]), "MiB": round(int(B["format"]["size"])/2**20,1), "frames": nf(d), "dur_s": float(B["format"]["duration"]),
                  "video": f'{va["codec_name"]} {va["width"]}x{va["height"]} {va["r_frame_rate"]} {va.get("pix_fmt")}', "audio": f'{aa["codec_name"]} {aa.get("sample_rate")} Hz {aa.get("channels")} ch',
                  "faststart": moov_first, "decode_errors": dec[:500] or "none"},
     "audio_identical_to_master": apk(m) == apk(d)}
r["pass"] = (r["delivery"]["frames"] == r["master"]["frames"] and abs(r["delivery"]["dur_s"]-r["master"]["dur_s"]) < 0.05 and r["audio_identical_to_master"]
             and va["width"]==1280 and va["height"]==720 and va["r_frame_rate"]=="24/1" and r["delivery"]["bytes"] < 480*2**20 and moov_first and not dec)
open("output/final/delivery/DELIVERY_VERIFY.json","w").write(json.dumps(r, indent=1)); print(json.dumps(r, indent=1))
PY
