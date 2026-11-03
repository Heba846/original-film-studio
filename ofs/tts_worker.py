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


def generate(job):
    if not probe()["chatterbox_installed"]:
        out({"ok": False, "error": "chatterbox-tts is not installed in this interpreter (run setup_tts.bat)"}, 2)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")  # never download implicitly
    import torch
    import torchaudio as ta
    device = pick_device(job.get("device", "auto"))
    kind = job.get("model", "turbo")
    try:
        model = load_model(kind, device)
    except Exception as e:  # noqa: BLE001
        out({"ok": False, "error": f"could not load model '{kind}' offline ({e}). If the weights were never "
             "downloaded, run:  python -m ofs tts download --yes"}, 3)
    results = []
    for it in job["items"]:
        try:
            parts = []
            for c in chunks(it["text"]):
                kw = {"audio_prompt_path": it["reference"]}
                if kind == "original":
                    kw.update(exaggeration=job.get("exaggeration", 0.5), cfg_weight=job.get("cfg_weight", 0.5))
                w = model.generate(c, **kw)
                parts.append(w)
                parts.append(torch.zeros(w.shape[0], int(0.15 * model.sr)))
            wav = torch.cat(parts[:-1], dim=1)
            ta.save(it["out"], wav, model.sr)
            results.append({"id": it["id"], "ok": True, "out": it["out"], "sr": model.sr})
        except Exception as e:  # noqa: BLE001
            results.append({"id": it["id"], "ok": False, "error": str(e)})
    out({"ok": all(r["ok"] for r in results), "device": device, "model": kind, "results": results})


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
