"""Optional voice-conversion stage (RVC). Applied to each synthesised line, per speaker.

Per-voice config:  rvc_model = "models/rvc/heroine.pth"   rvc_index = "models/rvc/heroine.index"  rvc_pitch = 0
Skipped (with one warning) when the model path is unset/missing or [rvc] enabled = false.

Two ways to run it:
  1. Automatic: [rvc].command is run once per line (template; edit it to match your RVC install).
  2. Manual: convert the folder build/audio/raw/<speaker>/ in the RVC WebUI / Applio batch tab and
     save results with the SAME file names into build/audio/vc/<speaker>/. Narrate picks them up.
"""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

from .audio import to_wav24
from .config import Config


class VoiceConverter:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.enabled = cfg["rvc"].get("enabled", True)
        self._warned: set[str] = set()

    def _warn(self, key: str, msg: str) -> None:
        if key not in self._warned:
            self._warned.add(key)
            print(f"  [rvc] {msg}")

    def convert(self, speaker: str, voice: dict, raw: Path, manual: Path, out: Path) -> str:
        """Write final line audio to `out`. Returns 'manual' | 'rvc' | 'none'."""
        if manual.exists():
            to_wav24(manual, out)
            return "manual"
        model = voice.get("rvc_model")
        if not self.enabled or not model:
            return "none"
        model_p = self.cfg.path(model)
        if not model_p.exists():
            self._warn(speaker, f"{speaker}: model {model_p} not found - using the plain TTS voice.")
            return "none"
        index = voice.get("rvc_index")
        index_p = self.cfg.path(index) if index else None
        if index_p is not None and not index_p.exists():
            self._warn(speaker + "i", f"{speaker}: index {index_p} not found - converting without index.")
            index_p = None
        tmp = out.with_suffix(".rvc.wav")
        tmpl = self.cfg["rvc"]["command"]
        if index_p is None:  # drop the index flag pair from the template
            tmpl = tmpl.replace("-ip {index}", "")
        cmd = tmpl.format(python=shlex.quote(sys.executable) if sys.platform != "win32" else f'"{sys.executable}"',
                          input=f'"{raw}"', output=f'"{tmp}"', model=f'"{model_p}"',
                          index=f'"{index_p}"' if index_p else "", pitch=int(voice.get("rvc_pitch", 0)))
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=self.cfg["rvc"]["timeout_s"])
        if r.returncode or not tmp.exists():
            raise RuntimeError(f"RVC command failed for {speaker}:\n{cmd}\n{(r.stderr or r.stdout)[-1200:]}")
        to_wav24(tmp, out)
        tmp.unlink(missing_ok=True)
        return "rvc"
