"""Pluggable TTS backends. Add one by writing a class with `synth(text, voice_cfg, out_wav)` and
registering it in BACKENDS. Output must be a WAV file (any rate; it is normalised afterwards)."""
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

import numpy as np

from .audio import SR, to_wav24, write_wav
from .config import Config


class SilentBackend:
    """No audio, ~0.4 s/word. For tests and layout/timing previews only."""

    def __init__(self, cfg: Config):
        pass

    def synth(self, text: str, voice: dict, out: Path) -> None:
        n = max(1, len(text.split()))
        write_wav(out, np.zeros(int(n * 0.4 * SR), dtype=np.int16))


class EdgeBackend:
    """Microsoft Edge neural voices via `edge-tts` (free, needs internet, no GPU)."""

    def __init__(self, cfg: Config):
        try:
            import edge_tts  # noqa: F401
        except ImportError:
            raise SystemExit("edge-tts missing: pip install edge-tts")

    def synth(self, text: str, voice: dict, out: Path) -> None:
        import edge_tts

        rate = int(voice.get("rate", 0))
        pitch = int(voice.get("pitch_hz", 0))
        name = voice.get("voice", "en-US-AriaNeural")
        last = None
        for attempt in range(3):
            with tempfile.TemporaryDirectory() as td:
                mp3 = Path(td) / "x.mp3"
                try:
                    asyncio.run(edge_tts.Communicate(text, name, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz").save(str(mp3)))
                    if mp3.stat().st_size == 0:
                        raise RuntimeError("empty audio from Edge TTS")
                    to_wav24(mp3, out)
                    return
                except Exception as e:  # network hiccup -> retry
                    last = e
        raise RuntimeError(f"Edge TTS failed for voice {name}: {last}")


class KokoroBackend:
    """Kokoro-82M through kokoro-onnx. Runs on CPU (about real-time or faster on a laptop)."""

    def __init__(self, cfg: Config):
        try:
            from kokoro_onnx import Kokoro
        except ImportError:
            raise SystemExit("kokoro-onnx missing: pip install kokoro-onnx soundfile")
        k = cfg["tts"]["kokoro"]
        model, voices = cfg.path(k["model"]), cfg.path(k["voices"])
        if not model.exists() or not voices.exists():
            raise SystemExit(f"Kokoro model files not found ({model}, {voices}). Run: film-studio fetch-kokoro")
        self.k = Kokoro(str(model), str(voices))

    def synth(self, text: str, voice: dict, out: Path) -> None:
        v = voice.get("voice", "af_heart")
        lang = voice.get("lang", "en-gb" if v.startswith("b") else "en-us")
        samples, sr = self.k.create(text, voice=v, speed=float(voice.get("speed", 1.0)), lang=lang)
        tmp = out.with_suffix(".raw.wav")
        import wave
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes((np.clip(samples, -1, 1) * 32767).astype(np.int16).tobytes())
        to_wav24(tmp, out) if sr != SR else tmp.replace(out)
        tmp.unlink(missing_ok=True)


BACKENDS = {"silent": SilentBackend, "edge": EdgeBackend, "kokoro": KokoroBackend}


class TTS:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._inst: dict[str, object] = {}

    def synth(self, text: str, voice: dict, out: Path) -> None:
        name = voice["backend"]
        if name not in BACKENDS:
            raise SystemExit(f"Unknown TTS backend '{name}'. Available: {', '.join(BACKENDS)}")
        if name not in self._inst:
            self._inst[name] = BACKENDS[name](self.cfg)
        out.parent.mkdir(parents=True, exist_ok=True)
        self._inst[name].synth(text, voice, out)


FETCH_URLS = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}


def fetch_kokoro(cfg: Config) -> None:
    import urllib.request

    k = cfg["tts"]["kokoro"]
    for key, fname in (("model", "kokoro-v1.0.onnx"), ("voices", "voices-v1.0.bin")):
        dst = cfg.path(k[key])
        if dst.exists():
            print(f"have {dst}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        print(f"downloading {fname} -> {dst} ...")
        urllib.request.urlretrieve(FETCH_URLS[fname], dst)
