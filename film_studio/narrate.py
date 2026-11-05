"""Step 2: scenes.json -> per-line TTS (+ optional RVC) -> scene audio, narration.wav, timeline.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from .audio import SR, read_wav, silence, write_wav
from .config import Config
from .subtitles import line_cues
from .tts import TTS
from .vc import VoiceConverter


def _key(text: str, voice: dict) -> str:
    return hashlib.sha1(json.dumps([text, voice], sort_keys=True).encode()).hexdigest()[:16]


def run(cfg: Config, force: bool = False) -> Path:
    b = cfg.build_dir
    doc = json.loads((b / "scenes.json").read_text(encoding="utf-8"))
    voices, au = cfg["voices"], cfg["audio"]
    tts, vc = TTS(cfg), VoiceConverter(cfg)
    max_chars = cfg["subtitles"]["max_chars"]
    titles = {c["id"]: c["title"] for c in doc["chapters"]}

    items, cues, t0, seen_ch = [], [], 0.0, set()
    chunks: list[np.ndarray] = []

    def add_item(entry: dict, audio: np.ndarray, scene_cues: list[dict]):
        nonlocal t0
        dur = len(audio) / SR
        entry.update(start=round(t0, 3), duration=round(dur, 3))
        for c in scene_cues:
            cues.append({**c, "start": round(c["start"] + t0, 3), "end": round(c["end"] + t0, 3)})
        items.append(entry)
        chunks.append(audio)
        t0 += dur

    total_lines = sum(len(s["lines"]) for s in doc["scenes"])
    done = 0
    for sc in doc["scenes"]:
        if sc["chapter"] not in seen_ch:
            seen_ch.add(sc["chapter"])
            if au["title_card_seconds"] > 0:
                add_item({"id": f"{sc['chapter']}-title", "kind": "title", "chapter": sc["chapter"],
                          "title": titles[sc["chapter"]]}, silence(au["title_card_seconds"]), [])
        parts, scene_cues, off, prev = [], [], 0.0, None
        for i, ln in enumerate(sc["lines"]):
            spk = ln["speaker"]
            if spk not in voices:
                raise SystemExit(f"{sc['id']} line {i}: speaker '{spk}' has no [voices.{spk}] in the config")
            voice = voices[spk]
            stem = f"{sc['id']}-{i:03d}"
            raw = b / "audio" / "raw" / spk / f"{stem}.wav"
            man = b / "audio" / "vc" / spk / f"{stem}.wav"
            fin = b / "audio" / "final" / spk / f"{stem}.wav"
            meta = fin.with_suffix(".json")
            key = _key(ln["text"], {k: v for k, v in voice.items()})
            key += "m" if man.exists() else ""
            if force or not fin.exists() or not meta.exists() or json.loads(meta.read_text()).get("key") != key:
                fin.parent.mkdir(parents=True, exist_ok=True)
                tts.synth(ln["text"], voice, raw)
                how = vc.convert(spk, voice, raw, man, fin)
                if how == "none":
                    fin.write_bytes(raw.read_bytes())
                meta.write_text(json.dumps({"key": key, "vc": how}))
            wav = read_wav(fin)
            if prev is not None:
                gap = au["pause_speaker"] if prev != spk else au["pause_line"]
                parts.append(silence(gap))
                off += gap
            d = len(wav) / SR
            scene_cues += line_cues(ln["text"], off, d, max_chars)
            parts.append(wav)
            off += d
            prev = spk
            done += 1
        parts.append(silence(au["pause_scene"]))
        print(f"  {sc['id']}: {len(sc['lines'])} lines ({done}/{total_lines})")
        add_item({"id": sc["id"], "kind": "scene", "chapter": sc["chapter"], "image": sc.get("image")},
                 np.concatenate(parts), scene_cues)

    write_wav(b / "narration.wav", np.concatenate(chunks))
    tl = {"total": round(t0, 3), "chapters": doc["chapters"], "items": items, "cues": cues}
    out = b / "timeline.json"
    out.write_text(json.dumps(tl, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"narration: {t0 / 60:.1f} min, {len(items)} segments -> {b / 'narration.wav'}")
    return out
