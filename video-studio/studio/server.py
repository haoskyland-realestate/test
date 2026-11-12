"""App timeline: máy chủ cục bộ cho trang chỉnh video (PC và điện thoại cùng wifi).
Chạy trong video-studio:  python3 studio/server.py          (chỉ máy này)
                           python3 studio/server.py --lan    (cho điện thoại cùng wifi)
Mở đúng đường link in ra (có mã khóa ?t=...). Chỉ dùng Python có sẵn, không cài thêm."""
import http.server, json, os, re, secrets, shutil, socket, subprocess, sys, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from timeline import check, layout  # noqa: E402
import effects  # noqa: E402

PROJ = os.path.join(ROOT, "projects")
TOKEN = os.environ.get("STUDIO_TOKEN") or secrets.token_urlsafe(9)
SAFE = re.compile(r"^[\w-]+$")
jobs = {}  # tên dự án -> tiến trình dựng


def effects_json():
    e = effects
    return {"styles": {k: v["vi"] for k, v in e.STYLES.items()}, "looks": {k: v[0] for k, v in e.LOOKS.items()},
            "transitions": {k: {"dur": v[0], "vi": v[3]} for k, v in e.TRANSITIONS.items()},
            "anims": e.TEXT_ANIMS, "kinds": {k: {"need": v[0], "vi": v[1]} for k, v in e.TEXT_KINDS.items()}}


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body=b"", ctype="application/json; charset=utf-8", extra=None):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def route(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        tok = self.headers.get("X-Token") or (q.get("t") or [""])[0]
        parts = [urllib.parse.unquote(p) for p in u.path.strip("/").split("/") if p]
        return parts, secrets.compare_digest(tok, TOKEN)

    def project(self, name):
        if not SAFE.match(name):
            return None
        d = os.path.join(PROJ, name)
        return d if os.path.exists(os.path.join(d, "timeline.json")) else None

    def do_GET(self):
        parts, ok = self.route()
        if not parts:
            return self.send(200, open(os.path.join(ROOT, "studio/index.html"), "rb").read(), "text/html; charset=utf-8")
        if parts[0] != "api" or not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa. Mở đúng link máy chủ in ra."})
        if parts[1:] == ["effects"]:
            return self.send(200, effects_json())
        if parts[1:] == ["projects"]:
            return self.send(200, sorted(n for n in os.listdir(PROJ) if self.project(n)))
        if len(parts) < 3 or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if len(parts) == 3:
            tl = json.load(open(os.path.join(d, "timeline.json"), encoding="utf8"))
            return self.send(200, {"timeline": tl, "has_video": os.path.exists(os.path.join(ROOT, "out", name + ".mp4"))})
        if parts[3] == "thumb" and len(parts) == 5:
            return self.thumb(d, parts[4])
        if parts[3] == "video":
            return self.file(os.path.join(ROOT, "out", name + ".mp4"), "video/mp4")
        if parts[3] == "render":
            j = jobs.get(name)
            log = os.path.join(d, "build", "render.log")
            tail = open(log, encoding="utf8", errors="replace").read()[-1500:] if os.path.exists(log) else ""
            return self.send(200, {"running": bool(j and j.poll() is None), "code": j and j.poll(), "log": tail})
        self.send(404, {"error": "Không có"})

    def thumb(self, d, spec):
        # spec: "<file>@<giây>" -> ảnh nhỏ của khung hình đó (lưu đệm trong build/thumbs)
        f, _, t = spec.rpartition("@")
        if not f or "/" in f or "\\" in f or f.startswith(".") or not re.fullmatch(r"\d+(\.\d+)?", t):
            return self.send(400, {"error": "Tham số ảnh không hợp lệ"})
        raw = os.path.join(d, "build", "raw", f)
        if not os.path.exists(raw):
            return self.send(404, {"error": "Chưa có footage " + f})
        out = os.path.join(d, "build", "thumbs", f"{f}@{t}.jpg")
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", t, "-i", raw, "-frames:v", "1",
                            "-vf", "scale=-2:360", out], check=False)
        if not os.path.exists(out):
            return self.send(500, {"error": "Không tạo được ảnh"})
        self.send(200, open(out, "rb").read(), "image/jpeg", {"Cache-Control": "max-age=3600"})

    def file(self, path, ctype):
        # Hỗ trợ tải từng đoạn (Range) để video tua được trên iPhone/Safari
        if not os.path.exists(path):
            return self.send(404, {"error": "Chưa có video"})
        size = os.path.getsize(path)
        m = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        a, b = 0, size - 1
        if m and (m[1] or m[2]):
            a = int(m[1]) if m[1] else size - int(m[2])
            b = min(int(m[2]), size - 1) if (m[1] and m[2]) else size - 1
        with open(path, "rb") as fh:
            fh.seek(a)
            data = fh.read(b - a + 1)
        self.send(206 if m else 200, data, ctype, {"Accept-Ranges": "bytes", "Content-Range": f"bytes {a}-{b}/{size}"} if m else {"Accept-Ranges": "bytes"})

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 2_000_000:
            raise ValueError("Dữ liệu quá lớn")
        return json.loads(self.rfile.read(n) or b"null")

    def do_PUT(self):
        parts, ok = self.route()
        if not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa"})
        if len(parts) != 3 or parts[:2] != ["api", "p"] or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        try:
            tl = self.body()
            errs = check(tl) if isinstance(tl, dict) else ["Dữ liệu không phải timeline"]
        except Exception as ex:  # JSON hỏng hoặc thiếu trường kiểu sai
            errs = [f"Dữ liệu không đọc được: {ex}"]
        if errs:
            return self.send(400, {"errors": errs})
        p = os.path.join(d, "timeline.json")
        shutil.copy(p, p + ".bak")  # giữ bản trước để khôi phục nếu lưu nhầm
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf8") as fh:
            json.dump(tl, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, p)
        self.send(200, {"ok": True, "total": layout(tl)["total"]})

    def do_POST(self):
        parts, ok = self.route()
        if not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa"})
        if len(parts) != 4 or parts[3] != "render" or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if jobs.get(name) and jobs[name].poll() is None:
            return self.send(409, {"error": "Đang dựng, chờ xong đã"})
        os.makedirs(os.path.join(d, "build"), exist_ok=True)
        log = open(os.path.join(d, "build", "render.log"), "w", encoding="utf8")
        jobs[name] = subprocess.Popen([sys.executable, os.path.join(ROOT, "scripts", "dung.py"), d], cwd=ROOT,
                                      stdout=log, stderr=subprocess.STDOUT)
        self.send(202, {"ok": True})


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    lan = "--lan" in sys.argv
    port = int(os.environ.get("STUDIO_PORT", "8765"))
    srv = http.server.ThreadingHTTPServer(("0.0.0.0" if lan else "127.0.0.1", port), H)
    print(f"App timeline: http://127.0.0.1:{port}/?t={TOKEN}")
    if lan:
        print(f"Điện thoại cùng wifi: http://{lan_ip()}:{port}/?t={TOKEN}")
    srv.serve_forever()
