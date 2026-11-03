import json
import threading
import urllib.error
import urllib.request

import pytest
from ofs import demo, media, project as proj
from ofs.server import make_server


@pytest.fixture
def srv(tmp_path):
    s, app = make_server(tmp_path, None, 0)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{s.server_address[1]}", app
    s.shutdown()


def call(url, body=None, headers=None, method=None, raw=None):
    h = dict(headers or {})
    data = raw
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def test_state_save_validate_prompts(srv):
    url, app = srv
    code, st = call(url + "/api/state")
    assert code == 200 and st["name"] == "my_film"
    p = st["project"]
    p["title"] = "عنوان"
    assert call(url + "/api/save", {"project": p}, {"X-OFS": "1"})[0] == 200
    assert proj.load(app.dir)["title"] == "عنوان"
    code, rep = call(url + "/api/validate", {"project": p}, {"X-OFS": "1"})
    assert code == 200 and not rep["ok"] and "no_shots" in [i["code"] for i in rep["issues"]]
    assert call(url + "/api/prompts", {"project": p}, {"X-OFS": "1"})[0] == 200


def test_writes_need_custom_header_and_local_host(srv):
    url, _ = srv
    assert call(url + "/api/save", {"project": {}})[0] == 403
    assert call(url + "/api/save", {"project": {}}, {"X-OFS": "1", "Host": "evil.example"})[0] == 403


def test_path_traversal_blocked_and_upload_stays_in_media(srv):
    url, app = srv
    assert call(url + "/media/..%2f..%2fetc%2fpasswd")[0] in (403, 404)
    code, j = call(url + "/api/upload?name=../../evil.png", headers={"X-OFS": "1"}, raw=b"\x89PNG", method="POST")
    assert code == 200 and j["path"] == "media/evil.png" and (app.dir / "media" / "evil.png").exists()
    assert call(url + "/api/upload?name=x.exe", headers={"X-OFS": "1"}, raw=b"x", method="POST")[0] == 400


def test_render_via_api_refuses_invalid(srv):
    import time
    url, app = srv
    p = proj.load(app.dir)
    p["shots"] = [{"id": "a", "asset": "media/none.png", "duration": 2}]
    assert call(url + "/api/render", {"project": p}, {"X-OFS": "1"})[0] == 200
    for _ in range(50):
        _, job = call(url + "/api/render/status")
        if job["state"] != "running":
            break
        time.sleep(0.1)
    assert job["state"] == "error" and any("not found" in e for e in job["errors"])


def test_synthetic_demo_end_to_end(tmp_path):
    import subprocess, json as j
    res = demo.make_demo(tmp_path / "d")
    out = tmp_path / "d" / "output" / "demo_30s.mp4"
    r = subprocess.run([media.tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)],
                       capture_output=True, text=True, check=True)
    d = j.loads(r.stdout)
    assert abs(float(d["format"]["duration"]) - 30.0) < 0.15
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    assert (v["width"], v["height"]) == (1920, 1080)
    assert any(s["codec_type"] == "audio" for s in d["streams"])
    assert res["production_type"] == "mixed_stills_and_supplied_video"
