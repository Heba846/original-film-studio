"""Standalone worker run by the ISOLATED TTS interpreter (.venv-tts). Not imported by the app.

    python tts_worker.py probe             -> JSON about torch/CUDA/chatterbox (imports torch only)
    python tts_worker.py generate job.json -> synthesises WAVs locally from reference clips
    python tts_worker.py download          -> explicit, user-requested model download (needs network)

STATUS: written against the official resemble-ai/chatterbox README API. NOT executed with the real
model in the authoring environment (no torch, no GPU, no voice recordings).
Nothing here uploads audio anywhere. Without `download`, HF_HUB_OFFLINE=1 stops silent downloads.
"""
import importlib.util
import json
import os
import re
import sys

# Running `python ofs/tts_worker.py` puts ofs/ first on sys.path, where ofs/packaging.py would shadow the
# real `packaging` package that transformers/torch import. Drop the script directory before any import.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != _HERE]


def out(obj, code=0):
    print(json.dumps(obj))
    sys.exit(code)


def probe():
    info = {"chatterbox_installed": importlib.util.find_spec("chatterbox") is not None,
            "torch_installed": importlib.util.find_spec("torch") is not None,
            "cuda": False, "device": "cpu", "python": sys.version.split()[0]}
    if info["torch_installed"]:
        import torch
        info["torch"] = torch.__version__
        info["cuda"] = bool(torch.cuda.is_available())
        info["device"] = "cuda" if info["cuda"] else "cpu"
        if info["cuda"]:
            info["gpu"] = torch.cuda.get_device_name(0)
    return info


def pick_device(want):
    p = probe()
    if want in ("cpu", "cuda"):
        if want == "cuda" and not p["cuda"]:
            raise RuntimeError("device 'cuda' requested but torch.cuda.is_available() is False")
        return want
    return p["device"]


def load_model(kind, device):
    if kind in ("turbo", "nano"):
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        return ChatterboxTurboTTS.from_pretrained(device=device, nano=True) if kind == "nano" \
            else ChatterboxTurboTTS.from_pretrained(device=device)
    from chatterbox.tts import ChatterboxTTS
    return ChatterboxTTS.from_pretrained(device=device)


def chunks(text, limit=280):
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    cur, res = "", []
    for s in sents:
        if cur and len(cur) + len(s) + 1 > limit:
            res.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        res.append(cur)
    return res


def _espeak(it, job):
    """STAND-IN engine for pipeline dry runs ONLY (robotic, not a clone). Needs espeak-ng on PATH."""
    import shutil
    import subprocess
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    if not exe:
        raise RuntimeError("espeak-ng not installed")
    subprocess.run([exe, "-v", it.get("voice", "en-us"), "-s", str(job.get("espeak_wpm", 165)),
                    "-w", it["out"], it["text"]], check=True, capture_output=True)


def generate(job):
    import time
    engine = job.get("engine", "chatterbox")
    skip = bool(job.get("skip_existing"))
    results, model, device, kind = [], None, "cpu", job.get("model", "turbo")
    if engine == "chatterbox":
        if not probe()["chatterbox_installed"]:
            out({"ok": False, "error": "chatterbox-tts is not installed in this interpreter (run setup_tts.bat)"}, 2)
        os.environ.setdefault("HF_HUB_OFFLINE", "1")  # never download implicitly
        device = pick_device(job.get("device", "auto"))
        try:
            model = load_model(kind, device)
        except Exception as e:  # noqa: BLE001
            out({"ok": False, "error": f"could not load model '{kind}' offline ({e}). If the weights were never "
                 "downloaded, run:  python -m ofs tts download --yes"}, 3)
        import torch
        import torchaudio as ta
    last_ref = None
    for n, it in enumerate(job["items"], 1):
        if skip and os.path.isfile(it["out"]) and os.path.getsize(it["out"]) > 1000:
            results.append({"id": it["id"], "ok": True, "out": it["out"], "skipped": True})
            continue
        t0 = time.time()
        try:
            os.makedirs(os.path.dirname(it["out"]), exist_ok=True)
            if engine == "espeak":
                _espeak(it, job)
                wall = time.time() - t0
                results.append({"id": it["id"], "ok": True, "out": it["out"], "wall": round(wall, 3)})
            else:
                ref = it.get("reference") or None
                if ref and ref != last_ref and hasattr(model, "prepare_conditionals") and kind == "original":
                    model.prepare_conditionals(ref, exaggeration=job.get("exaggeration", 0.5))
                    last_ref = ref
                parts = []
                for c in chunks(it["text"]):
                    kw = {}
                    if ref:
                        kw["audio_prompt_path"] = ref
                    if kind == "original":
                        kw.update(exaggeration=job.get("exaggeration", 0.5), cfg_weight=job.get("cfg_weight", 0.5))
                    w = model.generate(c, **kw)
                    parts.append(w)
                    parts.append(torch.zeros(w.shape[0], int(0.15 * model.sr)))
                wav = torch.cat(parts[:-1], dim=1)
                ta.save(it["out"], wav, model.sr)
                wall = time.time() - t0
                results.append({"id": it["id"], "ok": True, "out": it["out"], "sr": model.sr,
                                "audio_seconds": round(wav.shape[1] / model.sr, 3), "wall": round(wall, 3)})
        except Exception as e:  # noqa: BLE001
            results.append({"id": it["id"], "ok": False, "error": str(e)})
        print(f"[tts {n}/{len(job['items'])}] {it['id']} {'ok' if results[-1]['ok'] else 'FAILED'} "
              f"{time.time() - t0:.1f}s", file=sys.stderr, flush=True)
    out({"ok": all(r["ok"] for r in results), "device": device, "model": kind if engine == "chatterbox" else "espeak-ng",
         "engine": engine, "results": results})


def download():
    os.environ.pop("HF_HUB_OFFLINE", None)
    kinds = sys.argv[2:] or ["turbo"]
    for k in kinds:
        load_model(k, "cpu")
    out({"ok": True, "downloaded": kinds})


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "probe":
        out(probe())
    elif cmd == "generate":
        generate(json.load(open(sys.argv[2], encoding="utf-8")))
    elif cmd == "download":
        download()
    out({"ok": False, "error": "usage: probe | generate job.json | download [models]"}, 1)
