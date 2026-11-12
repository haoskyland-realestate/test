"""App timeline: máy chủ cục bộ cho trang chỉnh video (PC và điện thoại cùng wifi).
Chạy trong video-studio:  python3 studio/server.py          (chỉ máy này)
                           python3 studio/server.py --lan    (cho điện thoại cùng wifi)
Mở đúng đường link in ra (có mã khóa ?t=...). Chỉ dùng Python có sẵn, không cài thêm."""
import http.server, json, os, re, secrets, shutil, socket, subprocess, sys, time, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from timeline import check, layout  # noqa: E402
from mau import chuyen_tong  # noqa: E402
import effects  # noqa: E402

PROJ = os.path.join(ROOT, "projects")
TOKEN = os.environ.get("STUDIO_TOKEN") or secrets.token_urlsafe(9)
SAFE = re.compile(r"^[\w-]+$")
jobs = {}  # tên dự án -> (tiến trình dựng, có phải nháp)
proxies = {}  # đường dẫn bản xem trước -> tiến trình đang tạo


def effects_json():
    e = effects
    return {"styles": {k: v["vi"] for k, v in e.STYLES.items()}, "looks": {k: {"vi": v[0], "css": v[2]} for k, v in e.LOOKS.items() if k != "trung-tinh"},
            "style_looks": {k: v["look"] for k, v in e.STYLES.items()},
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
        if parts == ["gl_runtime.js"]:  # mã chạy chuyển cảnh WebGL (công khai, không chứa dữ liệu)
            return self.send(200, open(os.path.join(ROOT, "scripts/gl_runtime.js"), "rb").read(), "text/javascript; charset=utf-8")
        if parts[0] != "api" or not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa. Mở đúng link máy chủ in ra."})
        if parts[1:] == ["effects"]:
            return self.send(200, effects_json())
        if parts[1:] == ["gl"]:
            return self.send(200, effects.GL_LIB, extra={"Cache-Control": "max-age=3600"})
        if parts[1:] == ["projects"]:
            return self.send(200, sorted(n for n in os.listdir(PROJ) if self.project(n)))
        if len(parts) < 3 or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if len(parts) == 3:
            tl = json.load(open(os.path.join(d, "timeline.json"), encoding="utf8"))
            return self.send(200, {"timeline": tl, "has_video": os.path.exists(os.path.join(ROOT, "out", name + ".mp4"))})
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if parts[3] == "thumb" and len(parts) == 5:
            return self.thumb(d, parts[4])
        if parts[3] == "video":
            nhap = ".nhap" if q.get("nhap") else ""
            return self.file(os.path.join(ROOT, "out", name + nhap + ".mp4"), "video/mp4")
        if parts[3] == "proxy" and len(parts) == 5:
            return self.proxy(d, parts[4], bool(q.get("check")))
        if parts[3] == "wave" and len(parts) == 5:
            return self.wave(d, parts[4])
        if parts[3] == "history":
            hd = os.path.join(d, "history")
            if len(parts) == 4:
                return self.send(200, sorted((f[:-5] for f in os.listdir(hd) if f.endswith(".json")), reverse=True) if os.path.isdir(hd) else [])
            if len(parts) == 5 and SAFE.match(parts[4]) and os.path.exists(f := os.path.join(hd, parts[4] + ".json")):
                return self.send(200, json.load(open(f, encoding="utf8")))
            return self.send(404, {"error": "Không có phiên bản này"})
        if parts[3] in ("subtitles", "mastercut"):
            key, lg = (":pd", "phu_de.log") if parts[3] == "subtitles" else (":mc", "master_cut.log")
            j, _ = jobs.get(name + key, (None, False))
            log, rp = os.path.join(d, "build", lg), os.path.join(d, "build", "master-cut.md")
            tail = open(log, encoding="utf8", errors="replace").read()[-1200:] if os.path.exists(log) else ""
            return self.send(200, {"running": bool(j and j.poll() is None), "code": j and j.poll(), "log": tail,
                                   "report": open(rp, encoding="utf8").read() if parts[3] == "mastercut" and os.path.exists(rp) else ""})
        if parts[3] == "nle" and len(parts) == 5 and parts[4] in ("otio", "xml", "srt"):  # tải file xuất sang Premiere/DaVinci
            f = os.path.join(ROOT, "out", f"{name}.{parts[4]}")
            if not os.path.exists(f):
                return self.send(404, {"error": "Chưa xuất, bấm nút Xuất sang Premiere/DaVinci trước"})
            return self.send(200, open(f, "rb").read(), "application/octet-stream",
                             {"Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(name)}.{parts[4]}"})
        if parts[3] == "render":
            j, nh = jobs.get(name, (None, False))
            log = os.path.join(d, "build", "render.log")
            tail = open(log, encoding="utf8", errors="replace").read()[-1500:] if os.path.exists(log) else ""
            return self.send(200, {"running": bool(j and j.poll() is None), "code": j and j.poll(), "draft": nh, "log": tail,
                                   "has": {"nhap": os.path.exists(os.path.join(ROOT, "out", name + ".nhap.mp4")),
                                           "xuat": os.path.exists(os.path.join(ROOT, "out", name + ".mp4"))}})
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
                            "-vf", chuyen_tong(raw) + "scale=-2:360", out], check=False)
        if not os.path.exists(out):
            return self.send(500, {"error": "Không tạo được ảnh"})
        self.send(200, open(out, "rb").read(), "image/jpeg", {"Cache-Control": "max-age=3600"})

    def raw(self, d, f):
        if not f or "/" in f or "\\" in f or f.startswith("."):
            return None
        p = os.path.join(d, "build", "raw", f)
        return p if os.path.exists(p) else None

    def proxy(self, d, f, check):
        # Bản xem trước nhẹ (540p H.264 + AAC) để trình duyệt phát được footage 4K/HEVC; tạo nền ở lần đầu.
        raw = self.raw(d, f)
        if not raw:
            return self.send(404, {"error": "Chưa có footage " + f})
        out = os.path.join(d, "build", "proxy", f + ".mp4")
        p = proxies.get(out)
        if p and p.poll() == 0 and os.path.exists(out + ".tmp.mp4"):
            os.replace(out + ".tmp.mp4", out)  # tạo xong: đổi tên thì mới tính là có
        running = bool(p and p.poll() is None)
        failed = bool(p and p.poll() not in (None, 0))
        ready = os.path.exists(out)
        if not ready and not running and not failed:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            proxies[out] = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-vf", chuyen_tong(raw) + "scale=-2:540",
                                             "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-c:a", "aac", "-b:a", "96k",
                                             "-movflags", "+faststart", out + ".tmp.mp4"])
        if check:
            return self.send(200, {"ready": ready, "failed": failed})
        if not ready:
            return self.send(202, {"error": "Đang tạo bản xem trước"})
        self.file(out, "video/mp4")

    def wave(self, d, spec):
        # Sóng âm của một đoạn: "<file>@<giây vào>@<độ dài>"
        m = re.fullmatch(r"(.+)@(\d+(?:\.\d+)?)@(\d+(?:\.\d+)?)", spec)
        raw = m and self.raw(d, m[1])
        if not raw:
            return self.send(404, {"error": "Chưa có footage"})
        out = os.path.join(d, "build", "thumbs", f"wave-{spec}.png")
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", m[2], "-t", m[3], "-i", raw, "-filter_complex",
                            "aformat=channel_layouts=mono,showwavespic=s=800x60:colors=#9cc3ee", "-frames:v", "1", out], check=False)
        if not os.path.exists(out):
            return self.send(404, {"error": "Đoạn này không có tiếng"})
        self.send(200, open(out, "rb").read(), "image/png", {"Cache-Control": "max-age=3600"})

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
        hd = os.path.join(d, "history"); os.makedirs(hd, exist_ok=True)
        shutil.copy(p, os.path.join(hd, time.strftime("%Y%m%d-%H%M%S") + ".json"))
        for old in sorted(os.listdir(hd))[:-30]:  # giữ 30 phiên bản gần nhất
            os.remove(os.path.join(hd, old))
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf8") as fh:
            json.dump(tl, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, p)
        self.send(200, {"ok": True, "total": layout(tl)["total"]})

    def do_POST(self):
        parts, ok = self.route()
        if not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa"})
        if len(parts) != 4 or parts[3] not in ("render", "subtitles", "mastercut", "nle") or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if parts[3] == "nle":  # xuất timeline sang Premiere/DaVinci: nhanh (vài giây), chạy luôn
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "xuat_nle.py"), d], cwd=ROOT, capture_output=True, text=True, timeout=300)
            return self.send(200 if r.returncode == 0 else 500, {"ok": r.returncode == 0, "log": (r.stdout + r.stderr)[-1500:]})
        if parts[3] in ("subtitles", "mastercut"):  # phụ đề tự động / master cut: chạy nền, ghi thẳng vào timeline.json
            key, script = (":pd", "phu_de.py") if parts[3] == "subtitles" else (":mc", "master_cut.py")
            if jobs.get(name + key) and jobs[name + key][0].poll() is None:
                return self.send(409, {"error": "Đang chạy, chờ xong đã"})
            try:
                only = bool((self.body() or {}).get("report_only"))
            except Exception:
                only = False
            os.makedirs(os.path.join(d, "build"), exist_ok=True)
            log = open(os.path.join(d, "build", script.replace(".py", ".log")), "w", encoding="utf8")
            jobs[name + key] = (subprocess.Popen([sys.executable, os.path.join(ROOT, "scripts", script), d] + (["--chi-phan-tich"] if only else []),
                                                 cwd=ROOT, stdout=log, stderr=subprocess.STDOUT), False)
            return self.send(202, {"ok": True})
        if jobs.get(name) and jobs[name][0].poll() is None:
            return self.send(409, {"error": "Đang dựng, chờ xong đã"})
        try:
            draft = bool((self.body() or {}).get("draft"))
        except Exception:
            draft = False
        os.makedirs(os.path.join(d, "build"), exist_ok=True)
        log = open(os.path.join(d, "build", "render.log"), "w", encoding="utf8")
        jobs[name] = (subprocess.Popen([sys.executable, os.path.join(ROOT, "scripts", "dung.py"), d] + (["--nhap"] if draft else []),
                                       cwd=ROOT, stdout=log, stderr=subprocess.STDOUT), draft)
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
