"""Config loading (TOML) with defaults. Relative paths resolve against the config file's folder."""
from __future__ import annotations

import copy
import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULTS: dict = {
    "project": {
        "title": "Untitled",
        "chapters_dir": "chapters",
        "media_dir": "media",
        "build_dir": "build",
        "output": "build/output.mp4",
    },
    # name as it appears in the text -> speaker key (must exist in [voices.*]).
    # Add one line per name/alias, e.g.  Victor = "male_lead"
    "characters": {},
    "speakers": {
        # subject pronoun in a dialogue tag ("... he said") -> speaker key
        "pronouns": {"he": "male_lead", "she": "heroine"},
        # used when nobody can be inferred and there is no previous speaker
        "default_dialogue": "heroine",
    },
    "scenes": {"max_scene_words": 110},
    "tts": {
        "kokoro": {
            "model": "models/kokoro/kokoro-v1.0.onnx",
            "voices": "models/kokoro/voices-v1.0.bin",
        },
    },
    "voices": {
        "narrator": {"backend": "kokoro", "voice": "bf_emma", "speed": 1.0},
        "male_lead": {"backend": "kokoro", "voice": "am_michael", "speed": 1.0},
        "heroine": {"backend": "kokoro", "voice": "af_heart", "speed": 1.0},
    },
    "rvc": {
        "enabled": True,
        # {python} {input} {output} {model} {index} {pitch} are filled in. See README.
        "command": "{python} -m rvc_python cli -i {input} -o {output} -mp {model} -ip {index} -pi {pitch} -me rmvpe -v v2",
        "timeout_s": 600,
    },
    "audio": {
        "pause_line": 0.25,
        "pause_speaker": 0.45,
        "pause_scene": 0.7,
        "title_card_seconds": 3.0,
    },
    "video": {
        "width": 1920,
        "height": 1080,
        "fps": 25,
        "crf": 20,
        "preset": "medium",
        "crossfade": 0.6,
        "kenburns_zoom": 0.12,
        "batch": 12,  # clips joined per ffmpeg pass (keeps memory low on weak PCs)
    },
    "subtitles": {
        "enabled": True,
        "font": "Arial",
        "size": 54,  # at 1080p; scaled for other heights
        "max_chars": 84,
        "wrap": 42,
    },
}


def _merge(base: dict, over: dict) -> dict:
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict) and k != "characters":
            _merge(base[k], v)
        else:
            base[k] = v
    return base


@dataclass
class Config:
    data: dict
    root: Path

    def __getitem__(self, k):
        return self.data[k]

    def path(self, p: str | Path) -> Path:
        p = Path(p)
        return p if p.is_absolute() else (self.root / p)

    @property
    def chapters_dir(self) -> Path:
        return self.path(self.data["project"]["chapters_dir"])

    @property
    def media_dir(self) -> Path:
        return self.path(self.data["project"]["media_dir"])

    @property
    def build_dir(self) -> Path:
        return self.path(self.data["project"]["build_dir"])

    @property
    def output(self) -> Path:
        return self.path(self.data["project"]["output"])


def load_config(path: str | Path = "studio.toml") -> Config:
    path = Path(path).resolve()
    data = copy.deepcopy(DEFAULTS)
    if path.exists():
        with open(path, "rb") as f:
            _merge(data, tomllib.load(f))
    return Config(data, path.parent)
