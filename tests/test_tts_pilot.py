"""TTS: plumbing with a MOCK runner (NOT a voice-quality test) + the real worker's graceful failure path.
Pilot: structure, continuity, and a SYNTHETIC (tone) end-to-end assembly check."""
import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest
from conftest import make_wav
from ofs import media, narration as nar, packaging, pilot, project as proj, prompts as pr, tts, validate as val

ROOT = Path(__file__).resolve().parent.parent
HAVE_CB = importlib.util.find_spec("chatterbox") is not None


def mock_runner(cmd):
    """Pretends to be the TTS worker: writes tone WAVs. Proves plumbing only - these are NOT voices."""
    if cmd[2] == "probe":
        return SimpleNamespace(stdout=json.dumps({"chatterbox_installed": True, "torch_installed": True, "cuda": False,
                                                  "device": "cpu"}), stderr="")
    job = json.load(open(cmd[3], encoding="utf-8"))
    res = []
    for it in job["items"]:
        assert Path(it["reference"]).is_file()
        make_wav(it["out"], 0.7, 300)
        res.append({"id": it["id"], "ok": True, "out": it["out"]})
    return SimpleNamespace(stdout=json.dumps({"ok": True, "device": "cpu", "model": job["model"], "results": res}), stderr="")


@pytest.fixture
def gen_project(pdir):
    make_wav(pdir / "media" / "ref_h.wav", 1.0)
    make_wav(pdir / "media" / "ref_l.wav", 1.0)
    p = pilot.build_pilot()
    p["speakers"][0]["reference_audio"] = "media/ref_h.wav"
    p["speakers"][1]["reference_audio"] = "media/ref_l.wav"
    return p


def test_generation_blocked_without_consent_or_reference(pdir):
    p = pilot.build_pilot()
    probs = tts.generation_problems(p, pdir)
    assert any("no local reference audio" in x for x in probs)
    p["speakers"][0]["consent_confirmed"] = False
    assert any("consent" in x for x in tts.generation_problems(p, pdir))
    p["speakers"][1]["reference_audio"] = "media/missing.wav"
    assert any("not found" in x for x in tts.generation_problems(p, pdir))
    with pytest.raises(tts.TTSError):
        tts.generate(p, pdir, runner=mock_runner)


def test_mock_generation_plumbing_marks_segments_generated_and_assembles(gen_project, pdir):
    p = gen_project
    res = tts.generate(p, pdir, runner=mock_runner)
    assert res["ok"] and len(res["generated"]) == 6
    g = p["narration_segments"][0]
    assert g["source"] == "generated" and g["audio"] == "media/generated/n01.wav"
    side = json.loads((pdir / "media" / "generated" / "n01.wav.json").read_text())
    assert side["engine"] == "chatterbox" and "embedding" not in json.dumps(side).lower()
    pl = nar.assemble(p, pdir, pdir / "o.wav")
    assert pl["all_measured"] and abs(pl["total"] - (6 * 0.7 + 0.6 + 0.3 + 2.0 + 0.8 + 0.25)) < 0.1
    # second call: nothing left to generate (imported/generated audio is never overwritten silently)
    assert tts.generate(p, pdir, runner=mock_runner)["generated"] == []


def test_status_without_isolated_env_is_honest(monkeypatch):
    monkeypatch.delenv("OFS_TTS_PYTHON", raising=False)
    monkeypatch.setattr(tts, "ROOT", Path("/nonexistent"))
    st = tts.status()
    assert st["available"] is False and st["inference_tested_in_this_repo"] is False and "Imported audio works" in st["message"]


def test_status_with_mock_probe(monkeypatch):
    monkeypatch.setenv("OFS_TTS_PYTHON", sys.executable)
    st = tts.status(runner=mock_runner)
    assert st["available"] and st["device"] == "cpu" and st["inference_tested_in_this_repo"] is False


@pytest.mark.skipif(HAVE_CB, reason="chatterbox is installed here")
def test_real_worker_reports_not_installed_instead_of_crashing(tmp_path):
    job = tmp_path / "j.json"
    job.write_text(json.dumps({"items": [], "model": "turbo", "device": "auto"}))
    r = subprocess.run([sys.executable, str(ROOT / "ofs" / "tts_worker.py"), "generate", str(job)], capture_output=True, text=True)
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert r.returncode == 2 and out["ok"] is False and "not installed" in out["error"]
    r = subprocess.run([sys.executable, str(ROOT / "ofs" / "tts_worker.py"), "probe"], capture_output=True, text=True)
    info = json.loads(r.stdout.strip().splitlines()[-1])
    assert info["chatterbox_installed"] is False and info["device"] in ("cpu", "cuda")


def test_main_app_never_imports_torch_or_chatterbox():
    r = subprocess.run([sys.executable, "-c", "import sys, ofs.server, ofs.tts, ofs.cli; "
                        "assert 'torch' not in sys.modules and 'chatterbox' not in sys.modules; print('ok')"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.stdout.strip() == "ok", r.stderr


def test_voice_data_is_gitignored_and_never_zipped(tmp_path):
    ig = (ROOT / ".gitignore").read_text()
    for pat in ("voices/", "*.pt", "*.safetensors", "*.ckpt", "*.npy", "*.wav", ".venv-tts/", "projects/*/media/"):
        assert pat in ig
    root = tmp_path / "r"
    for f in ("ofs/a.py", "projects/p/project.json", "projects/p/voices/ref.wav", "projects/p/media/x.wav",
              "projects/p/extra/model.safetensors", "projects/p/extra/emb.npy", "projects/p/extra/ok.srt"):
        (root / f).parent.mkdir(parents=True, exist_ok=True)
        (root / f).write_bytes(b"x")
    packaging.make_zip(root, tmp_path / "z.zip")
    names = zipfile.ZipFile(tmp_path / "z.zip").namelist()
    assert any(n.endswith("project.json") for n in names) and any(n.endswith("ok.srt") for n in names)
    assert not any(n.endswith((".wav", ".safetensors", ".npy")) for n in names)


def test_no_credentials_or_secrets_in_source():
    import re
    bad = re.compile(r"(hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})")
    for f in list((ROOT / "ofs").rglob("*.py")) + list(ROOT.glob("*.bat")) + list((ROOT / "projects").rglob("*.json")):
        assert not bad.search(f.read_text(encoding="utf-8")), f


# ---------------- pilot ----------------
AUTHOR_TEXT = {
    "n01": "Two shots. That's all it took.",
    "n04": "Go back inside, Dottoressa. You were never here.",
}


def test_pilot_structure_text_and_editorial_marking():
    p = pilot.build_pilot()
    assert 4 <= len(p["shots"]) <= 6 and [s["id"] for s in p["speakers"]] == ["heba", "lion"]
    segs = {g["id"]: g for g in p["narration_segments"]}
    for k, v in AUTHOR_TEXT.items():
        assert segs[k]["text"] == v
    joined = " ".join(g["text"] for g in p["narration_segments"])
    assert "plaster splint I had built for him forty minutes earlier, in an exam room, with my own two hands." in joined
    assert "I was an ER doctor." in joined and "Now I was the witness he couldn't afford to leave behind." in joined
    assert "married into a family" not in joined          # the premature line is NOT in the narration text...
    assert "married into a family" in p["notes"] and "married into a family" in segs["n06"]["original_text"]   # ...but kept in notes
    assert segs["n06"]["editorial"] and not any(segs[k]["editorial"] for k in ("n01", "n02", "n03", "n04", "n05"))
    assert segs["n03"]["pause_after"] == 2.0 and segs["n04"]["speaker"] == "lion"
    assert all(g["speaker"] == "heba" for k, g in segs.items() if k != "n04")
    assert all(s["consent_confirmed"] and not s["reference_audio"] for s in p["speakers"])   # no invented recordings
    assert all(g["audio"] == "" for g in p["narration_segments"])
    assert sorted(x for s in p["shots"] for x in s["segments"]) == sorted(segs)


def test_pilot_notes_record_complete_film_decision():
    n = pilot.build_pilot()["notes"]
    assert "COMPLETE short film" in n and "satisfying ending" in n and "NOT a cliffhanger paywall" in n


def test_pilot_prompts_carry_visual_continuity_and_stay_non_graphic():
    items = pr.build_prompts(pilot.build_pilot())
    allp = {i["shot_id"]: i for i in items}
    nico_shots = [i for i in items if "Nico" in i["image_prompt"]]
    assert nico_shots
    for i in nico_shots:
        ip = i["image_prompt"]
        assert "gray eyes" in ip and "black hair" in ip and "LEFT eyebrow" in ip
        assert any("RIGHT forearm" in n and "LEFT hand" in n for n in i["continuity_notes"])
    for i in items:
        assert "Brooklyn hospital parking garage" in i["image_prompt"] and "wet concrete" in i["image_prompt"]
        assert "orange" in i["image_prompt"] and "no blood" in i["image_prompt"] and "gore" in i["negative_prompt"]
        assert "OPTIONAL motion" in i["optional_motion_prompt"] and i["animatic_motion"]
    ivy = allp["s05"]["image_prompt"]
    assert "freckles" in ivy and "knot" in ivy and "pen" in ivy and "navy" in ivy and "late twenties" in ivy
    assert "LEFT hand" in allp["s03"]["image_prompt"] and "RIGHT forearm" in allp["s03"]["image_prompt"]
    assert allp["s06"]["narration"][0]["editorial_proposal"] is True
    md = pr.to_markdown(pilot.build_pilot(), items)
    assert "editorial proposal" in md and "animatic" in md


def test_pilot_validation_is_honest_about_missing_recordings(tmp_path):
    p = pilot.build_pilot()
    r = val.validate(p, tmp_path)
    errs = set(i.code for i in r.errors)
    assert errs == {"missing_file", "segment_no_audio"}      # nothing else wrong: structure/ids/timing are consistent


def test_pilot_synthetic_dryrun_end_to_end(tmp_path):
    res = pilot.dryrun(tmp_path / "d")
    out = tmp_path / "d" / "output" / "pilot_dryrun.mp4"
    r = subprocess.run([media.tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    assert (v["width"], v["height"]) == (1920, 1080) and any(s["codec_type"] == "audio" for s in d["streams"])
    p = proj.load(tmp_path / "d")
    pl = nar.plan(p, tmp_path / "d")
    assert pl["all_measured"]
    assert abs(float(d["format"]["duration"]) - (pl["total"] + 0.5)) < 0.1     # picture length computed from REAL audio
    assert res["production_type"] == "animatic_slideshow" and res["narration"] == "segments"
    assert "SYNTHETIC" in p["title"]
