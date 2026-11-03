"""Local-only browser UI (stdlib http.server; binds to 127.0.0.1)."""
from __future__ import annotations

import json
import mimetypes
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import media, narration as nar, project as proj, prompts as pr, render as rn, tts, validate as val

STATIC = Path(__file__).parent / "static"
MAX_UPLOAD = 8 * 1024 ** 3


class App:
    def __init__(self, root: Path, current: str | None = None):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.job = {"state": "idle", "stage": "", "progress": 0.0, "message": "", "output": None}
        names = self.projects()
        self.current = current if current in names else (names[0] if names else None)
        if self.current is None:
            self.new_project("my_film")

    def projects(self):
        return sorted(d.name for d in self.root.iterdir() if (d / "project.json").is_file())

    def new_project(self, name):
        if not proj.valid_project_name(name):
            raise ValueError("Project name: letters, digits, space, - or _ only.")
        d = self.root / name
        if (d / "project.json").exists():
            raise ValueError("A project with that name already exists.")
        (d / "media").mkdir(parents=True, exist_ok=True)
        proj.save(d, {"title": name})
        self.current = name

    @property
    def dir(self) -> Path:
        return self.root / self.current

    def safe(self, rel: str) -> Path:
        p = (self.dir / rel).resolve()
        if self.dir.resolve() not in p.parents and p != self.dir.resolve():
            raise PermissionError("path outside project")
        return p

    def start_render(self, data):
        with self.lock:
            if self.job["state"] == "running":
                raise ValueError("A render is already running.")
            self.job = {"state": "running", "stage": "starting", "progress": 0.0, "message": "", "output": None}
        d = self.dir

        def work():
            try:
                res = rn.render(data, d, d / "output" / "film.mp4",
                                lambda s, f: self.job.update(stage=s, progress=f))
                self.job.update(state="done", progress=1.0, output="output/film.mp4",
                                message=res["disclosure"], warnings=[i.message for i in res["report"].warnings])
            except rn.ValidationFailed as e:
                self.job.update(state="error", message="Validation failed", errors=[i.message for i in e.report.errors])
            except Exception as e:  # noqa: BLE001
                self.job.update(state="error", message=str(e))
        threading.Thread(target=work, daemon=True).start()


def make_handler(app: App):
    class H(BaseHTTPRequestHandler):
        server_version = "OFS/0.1"

        def log_message(self, *a):
            pass

        # -- helpers
        def _json(self, obj, code=200):
            b = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(b)

        def _host_ok(self):
            h = (self.headers.get("Host") or "").split(":")[0]
            return h in ("127.0.0.1", "localhost")

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(n)

        def _guard_write(self):
            if not self._host_ok() or self.headers.get("X-OFS") != "1":
                self._json({"error": "forbidden"}, 403)
                return False
            return True

        # -- GET
        def do_GET(self):
            if not self._host_ok():
                return self._json({"error": "forbidden"}, 403)
            u = urlparse(self.path)
            try:
                if u.path == "/":
                    b = (STATIC / "index.html").read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(b)))
                    self.end_headers()
                    return self.wfile.write(b)
                if u.path == "/api/state":
                    return self._json({"name": app.current, "projects": app.projects(),
                                       "project": proj.load(app.dir), "tools": media.tool_versions(),
                                       "motions": proj.MOTIONS, "transitions": proj.TRANSITIONS,
                                       "files": self._files(), "tts": {"model": None}})
                if u.path == "/api/render/status":
                    return self._json(app.job)
                if u.path.startswith("/media/"):
                    return self._serve(unquote(u.path[len("/media/"):]))
                self._json({"error": "not found"}, 404)
            except PermissionError:
                self._json({"error": "forbidden"}, 403)
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)}, 500)

        def _files(self):
            m = app.dir / "media"
            return sorted(p.relative_to(app.dir).as_posix() for p in m.rglob("*") if p.is_file()) if m.is_dir() else []

        def _serve(self, rel):
            p = app.safe(rel)
            if not p.is_file():
                return self._json({"error": "not found"}, 404)
            size = p.stat().st_size
            start, end, code = 0, size - 1, 200
            rng = self.headers.get("Range")
            if rng and (m := re.match(r"bytes=(\d*)-(\d*)", rng)):
                if m.group(1):
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else size - 1
                elif m.group(2):
                    start = max(0, size - int(m.group(2)))
                end = min(end, size - 1)
                code = 206
            self.send_response(code)
            self.send_header("Content-Type", mimetypes.guess_type(p.name)[0] or "application/octet-stream")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            if code == 206:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            with open(p, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)

        # -- POST
        def do_POST(self):
            if not self._guard_write():
                return
            u = urlparse(self.path)
            try:
                if u.path == "/api/upload":
                    return self._upload(parse_qs(u.query))
                data = json.loads(self._body() or b"{}")
                if u.path == "/api/save":
                    proj.save(app.dir, data["project"])
                    return self._json({"saved": True})
                if u.path == "/api/validate":
                    return self._json(val.validate(data["project"], app.dir).to_dict())
                if u.path == "/api/prompts":
                    p = proj.normalize(data["project"])
                    items = pr.build_prompts(p)
                    return self._json({"prompts": items, "markdown": pr.to_markdown(p, items),
                                       "csv": pr.to_csv(items)})
                if u.path == "/api/render":
                    proj.save(app.dir, data["project"])
                    app.start_render(data["project"])
                    return self._json({"started": True})
                if u.path == "/api/narration/plan":
                    return self._json(nar.plan(data["project"], app.dir))
                if u.path == "/api/narration/assemble":
                    try:
                        res = nar.assemble(data["project"], app.dir, app.dir / "output" / "narration_assembled.wav")
                    except ValueError as e:
                        return self._json({"error": str(e)}, 400)
                    res["url"] = "output/narration_assembled.wav"
                    return self._json(res)
                if u.path == "/api/narration/sync":
                    pl = nar.plan(data["project"], app.dir)
                    res = nar.sync_shot_durations(data["project"], pl)
                    return self._json({"project": res["project"], "changed": res["changed"], "estimated": res["estimated"]})
                if u.path == "/api/tts/status":
                    return self._json(tts.status())
                if u.path == "/api/tts/generate":
                    p = proj.normalize(data["project"])
                    try:
                        res = tts.generate(p, app.dir, data.get("segments") or None, overwrite=bool(data.get("overwrite")))
                    except tts.TTSError as e:
                        return self._json({"error": str(e)}, 400)
                    res["project"] = p
                    return self._json(res)
                if u.path == "/api/open":
                    if data["name"] not in app.projects():
                        raise ValueError("unknown project")
                    app.current = data["name"]
                    return self._json({"ok": True})
                if u.path == "/api/new":
                    app.new_project(data["name"])
                    return self._json({"ok": True})
                self._json({"error": "not found"}, 404)
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                self._json({"error": str(e)}, 400)
            except PermissionError:
                self._json({"error": "forbidden"}, 403)
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)}, 500)

        def _upload(self, q):
            name = Path((q.get("name") or [""])[0]).name
            ext = Path(name).suffix.lower()
            if not name or ext not in (media.IMAGE_EXT | media.VIDEO_EXT | media.AUDIO_EXT | {".srt"}):
                return self._json({"error": "unsupported file type"}, 400)
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_UPLOAD:
                return self._json({"error": "file too large"}, 413)
            dest_dir = app.dir / "media"
            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / name
            with open(dest, "wb") as f:
                left = n
                while left > 0:
                    chunk = self.rfile.read(min(1 << 20, left))
                    if not chunk:
                        break
                    f.write(chunk)
                    left -= len(chunk)
            self._json({"path": f"media/{name}"})  # local copy only: nothing leaves this machine

    return H


def make_server(root, project=None, port=8765):
    app = App(Path(root), project)
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(app)), app


def serve(root, project=None, port=8765, open_browser=True):
    srv, app = make_server(root, project, port)
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"Original Film Studio UI: {url}   (Ctrl+C to stop)\nProjects folder: {Path(root).resolve()}")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
