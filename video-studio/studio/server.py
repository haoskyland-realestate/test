"""App timeline: máy chủ cục bộ cho trang chỉnh video (PC và điện thoại cùng wifi).
Chạy trong video-studio:  python3 studio/server.py          (chỉ máy này)
                           python3 studio/server.py --lan    (cho điện thoại cùng wifi)
Mở đúng đường link in ra (có mã khóa ?t=...). Chỉ dùng Python có sẵn, không cài thêm."""
import http.server, json, os, re, secrets, shutil, socket, subprocess, sys, time, urllib.parse

os.environ["PYTHONUTF8"] = "1"  # tiến trình con (dựng, phụ đề, master cut) in/ghi tiếng Việt được trên Windows
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from timeline import check, layout, AUDIO_EXT, PLATFORMS  # noqa: E402
from mau import chuyen_tong  # noqa: E402
import effects  # noqa: E402
from am_thanh import SFX, SFX_DIR  # noqa: E402
from ap_mau import MAU, ap  # noqa: E402
from kich_ban import dat_chu  # noqa: E402
from luu_vao_mau import luu as luu_mau  # noqa: E402
import base64  # noqa: E402
from lop_chu import tao as tao_lop_chu  # noqa: E402
import kho  # noqa: E402
import hashlib  # noqa: E402

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
            "anims": e.TEXT_ANIMS, "kinds": {k: {"need": v[0], "vi": v[1]} for k, v in e.TEXT_KINDS.items()},
            "sfx": SFX, "mau": {k: {f: m.get(f, "") for f in ("ten", "loai", "the", "nganh", "mo_ta", "dung_cho", "xem_truoc")} for k, m in MAU.items()}}


VIDEO_EXT = re.compile(r"\.(mp4|mov|m4v|mkv|mts)$", re.I)


def duyet(path):
    """Duyệt thư mục trên máy chạy studio (để chọn thư mục footage từ PC hoặc điện thoại)."""
    path = os.path.abspath(path or os.path.expanduser("~"))
    if not os.path.isdir(path):
        raise ValueError("Không có thư mục " + path)
    names = sorted(os.listdir(path), key=str.lower)
    dirs = [n for n in names if not n.startswith(".") and os.path.isdir(os.path.join(path, n))]
    vids = [n for n in names if VIDEO_EXT.search(n)]
    roots = [f"{c}:\\" for c in "CDEFGH" if os.path.exists(f"{c}:\\")] if os.name == "nt" else []  # ổ đĩa Windows
    return {"path": path, "parent": os.path.dirname(path) if os.path.dirname(path) != path else None,
            "dirs": dirs, "videos": vids, "audio": [n for n in names if re.search(AUDIO_EXT, n, re.I)], "roots": roots}


def lien_ket(src, dst):
    """Đưa file vào build/raw mà không chiếm thêm ổ: liên kết cứng (cùng ổ), không được thì chép."""
    if os.path.exists(dst):
        return
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def thoi_luong(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    try:
        return round(float(out), 2)
    except ValueError:
        return 0


def kiem_ten(req):
    name, platform = str(req.get("name", "")).strip(), req.get("platform", "tiktok")
    if not SAFE.match(name):
        raise ValueError("Tên dự án chỉ gồm chữ, số, gạch ngang (-) hoặc gạch dưới (_), không dấu cách")
    if platform not in PLATFORMS:
        raise ValueError("Khung phải là tiktok hoặc youtube")
    d = os.path.join(PROJ, name)
    if os.path.exists(d):
        raise ValueError(f"Đã có dự án '{name}', chọn tên khác")
    return name, platform, d


TAI = {}  # tiến độ tải nguồn theo tên dự án (app hỏi lại mỗi 2 giây)


def thu_muc_tai(name):
    """Nơi gom footage của dự án trước khi đưa vào build/raw: file Hào tải lên + file tải từ link."""
    return os.path.join(ROOT, "tai-ve", name)


def gom_nguon(name, req, bao=lambda **k: None):
    """Gom mọi nguồn vào tai-ve/<tên>/: link (Drive, trực tiếp, YouTube/TikTok) trong req["nguon"] (và req["drive"] kiểu cũ),
    đường dẫn trên máy trong req["tep"] (lệnh du_an_moi). File Hào tải lên qua /api/tai-len đã nằm sẵn ở đó."""
    from tai_drive import tai_nguon
    dich = thu_muc_tai(name)
    os.makedirs(dich, exist_ok=True)
    urls = [str(u) for u in (req.get("nguon") or [])] + ([str(req["drive"])] if req.get("drive") else [])
    for k, u in enumerate(urls, 1):
        tai_nguon(u, dich, lambda **x: bao(nguon=k, so_nguon=len(urls), **x))
    for p in req.get("tep") or []:
        p = os.path.abspath(p)
        fs = [os.path.join(p, f) for f in (lambda i: i["videos"] + i["audio"])(duyet(p))] if os.path.isdir(p) else [p]
        for f in fs:
            lien_ket(f, os.path.join(dich, os.path.basename(f)))
    return dich


def co_nguon(req):
    return any(req.get(k) for k in ("nguon", "drive", "tep", "da_tai_len"))


def tao_du_an(req, bao=lambda **k: None):
    """Dự án mới: từ nhiều nguồn (file tải lên, link Drive/trực tiếp/YouTube, thư mục/file trên máy) gom vào video-studio/tai-ve/<tên>/,
    hoặc từ một thư mục footage, hoặc nhân bản một dự án (đổi khung). Mỗi video thành một đoạn, cắt thẳng."""
    name, platform, d = kiem_ten(req)
    if co_nguon(req):
        req = {**req, "folder": gom_nguon(name, req, bao)}
    raw = os.path.join(d, "build", "raw")
    if req.get("from"):
        src = os.path.join(PROJ, str(req["from"]))
        if not SAFE.match(str(req["from"])) or not os.path.exists(os.path.join(src, "timeline.json")):
            raise ValueError("Không có dự án nguồn")
        tl = json.load(open(os.path.join(src, "timeline.json"), encoding="utf8"))
        tl.setdefault("meta", {})["platform"] = platform
        os.makedirs(raw)
        sr = os.path.join(src, "build", "raw")
        for f in os.listdir(sr) if os.path.isdir(sr) else []:
            lien_ket(os.path.join(sr, f), os.path.join(raw, f))
    else:
        info = duyet(req.get("folder"))
        if not info["videos"]:
            raise ValueError("Thư mục này không có video (.mp4, .mov, .m4v, .mkv, .mts)")
        os.makedirs(raw)
        clips = []
        for f in info["videos"] + info["audio"]:
            lien_ket(os.path.join(info["path"], f), os.path.join(raw, f))
        for f in info["videos"]:
            if (dur := thoi_luong(os.path.join(raw, f))) > 0.2:
                clips.append({"file": f, "in": 0, "dur": dur})
        if not clips:
            raise ValueError("Không đọc được thời lượng video nào (cần FFmpeg)")
        tl = {"version": 1, "meta": {"platform": platform, "style": "hien-dai", "title": name}, "clips": clips,
              "transitions": [{"type": "cut"}] * (len(clips) - 1), "texts": [], "subtitles": [],
              "audio": {"music": "synth", "whoosh": False, "voice": True, "music_volume": 1.0}}
    if errs := check(tl):
        shutil.rmtree(d, ignore_errors=True)
        raise ValueError("; ".join(errs))
    with open(os.path.join(d, "timeline.json"), "w", encoding="utf8") as fh:
        json.dump(tl, fh, ensure_ascii=False, indent=1)
    # giấy tờ của video (BRIEF, KICH-BAN…): nhân bản thì chép của dự án gốc, dự án mới thì chép mẫu
    md = os.path.join(PROJ, str(req["from"])) if req.get("from") else os.path.join(ROOT, "..", "mau", "du-an-video")
    for f in os.listdir(md) if os.path.isdir(md) else []:
        if f.endswith(".md"):
            shutil.copy(os.path.join(md, f), d)
    return {"ok": True, "name": name, "clips": len(tl["clips"])}


def them_nguon(name, req, bao=lambda **k: None):
    """Thêm footage vào dự án đã có: gom nguồn như dự án mới, video chưa có trong build/raw thành đoạn mới ở cuối (cắt thẳng).
    Không đụng chữ/thẻ đã đặt; bản cũ lưu timeline.json.bak."""
    d = os.path.join(PROJ, name)
    T = os.path.join(d, "timeline.json")
    if not SAFE.match(name) or not os.path.exists(T):
        raise ValueError("Không có dự án này")
    dich = gom_nguon(name, req, bao)
    raw = os.path.join(d, "build", "raw")
    os.makedirs(raw, exist_ok=True)
    tl = json.load(open(T, encoding="utf8"))
    moi = []
    for f in duyet(dich)["videos"] + duyet(dich)["audio"]:
        if not os.path.exists(os.path.join(raw, f)):
            lien_ket(os.path.join(dich, f), os.path.join(raw, f))
            if VIDEO_EXT.search(f) and (dur := thoi_luong(os.path.join(raw, f))) > 0.2:
                moi.append({"file": f, "in": 0, "dur": dur})
    if not moi:
        raise ValueError("Không có video mới (các file này đã có trong dự án)")
    tl["transitions"] = tl.get("transitions", []) + [{"type": "cut"}] * len(moi)
    tl["clips"] = tl["clips"] + moi
    if errs := check(tl):
        raise ValueError("; ".join(errs))
    shutil.copy(T, T + ".bak")
    with open(T, "w", encoding="utf8") as fh:
        json.dump(tl, fh, ensure_ascii=False, indent=1)
    return {"ok": True, "name": name, "clips": len(moi), "them": True}


def chay_nen(name, viec):
    """Tải nguồn có thể mất nhiều phút: chạy nền, app hỏi tiến độ qua /api/newjob?name=."""
    if TAI.get(name, {}).get("buoc") == "tai":
        raise ValueError("Dự án này đang tải, chờ xong")
    TAI[name] = {"buoc": "tai", "i": 0, "n": 0, "ten": "", "da": 0, "tong": 0}

    def chay():
        try:
            TAI[name] = {"buoc": "xong", **viec(lambda **k: TAI.update({name: {"buoc": "tai", **k}}))}
        except Exception as ex:  # lỗi mạng/ổ đĩa/link: báo lại cho app; file tải dở nằm ở tai-ve/ (làm lại sẽ bỏ qua file đủ)
            TAI[name] = {"buoc": "loi", "error": str(ex)}
    __import__("threading").Thread(target=chay, daemon=True).start()


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
            trang = open(os.path.join(ROOT, "studio/index.html"), "rb").read()
            if self.server.server_address[0] == "127.0.0.1":  # chỉ máy này mở được: gắn sẵn mã khoá để mở bằng link localhost không cần ?t= (khung xem trước). Chế độ --lan thì không.
                trang = trang.replace(b'get("t") || ""', b'get("t") || "' + TOKEN.encode() + b'"', 1)
            return self.send(200, trang, "text/html; charset=utf-8")
        if parts == ["gsap.min.js"]:  # thư viện chuyển động cho lớp chữ xem trước (công khai, không chứa dữ liệu)
            return self.send(200, open(os.path.join(ROOT, "node_modules/gsap/dist/gsap.min.js"), "rb").read(), "text/javascript; charset=utf-8",
                             {"Cache-Control": "max-age=86400"})
        if parts == ["gl_runtime.js"]:  # mã chạy chuyển cảnh WebGL (công khai, không chứa dữ liệu)
            return self.send(200, open(os.path.join(ROOT, "scripts/gl_runtime.js"), "rb").read(), "text/javascript; charset=utf-8")
        if parts == ["bang-master"]:  # trang Bảng master (không chứa bí mật; đọc/lưu qua /api/cau-hinh cần mã khoá)
            import bang_master
            return self.send(200, bang_master.tao(True).encode(), "text/html; charset=utf-8")
        if parts[0] != "api" or not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa. Mở đúng link máy chủ in ra."})
        if parts[1:] == ["effects"]:
            return self.send(200, effects_json())
        if parts[1:] == ["cau-hinh"]:  # bảng master + ghi đè riêng dự án (?p=<tên>)
            import bang_master
            p = (urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("p") or [""])[0]
            d = self.project(p) if p else None
            gd = (json.load(open(os.path.join(d, "timeline.json"), encoding="utf8")).get("meta") or {}).get("cau_hinh", {}) if d else {}
            return self.send(200, {"nhom": bang_master.du_lieu()["nhom"], "ghi_de": gd})
        if parts[1:] == ["gl"]:
            return self.send(200, effects.GL_LIB, extra={"Cache-Control": "max-age=3600"})
        if parts[1:] == ["newjob"]:  # tiến độ tạo dự án từ Google Drive
            name = (urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("name") or [""])[0]
            return self.send(200, TAI.get(name) or {"buoc": "khong-co"})
        if parts[1:] == ["xem-link"]:  # xem trước link (Drive, trực tiếp, YouTube/TikTok) trước khi thêm vào giỏ nguồn
            try:
                from tai_drive import xem
                return self.send(200, xem((urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("url") or [""])[0]))
            except Exception as ex:  # link lỗi/không tới được: báo nguyên nhân cho app
                return self.send(400, {"error": f"Không đọc được link: {ex}"})
        if parts[1:] == ["browse"]:
            try:
                return self.send(200, duyet((urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("path") or [""])[0]))
            except (ValueError, OSError) as ex:
                return self.send(400, {"error": str(ex)})
        if len(parts) == 3 and parts[1] == "sfx" and parts[2] in SFX:  # nghe thử một hiệu ứng âm
            return self.file(os.path.join(SFX_DIR, parts[2] + ".wav"), "audio/wav")
        if len(parts) == 3 and parts[1] == "mau" and parts[2] in MAU:  # tài liệu công thức của một mẫu
            f = os.path.join(MAU[parts[2]]["_dir"], "MAU.md")
            return self.send(200, {"md": open(f, encoding="utf8").read() if os.path.exists(f) else ""})
        if parts[1:2] == ["kho"]:
            return self.kho_get(parts[2:], urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
        if parts[1:] == ["projects"]:
            return self.send(200, sorted(n for n in os.listdir(PROJ) if self.project(n)))
        if len(parts) < 3 or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if len(parts) == 3:
            tl = json.load(open(os.path.join(d, "timeline.json"), encoding="utf8"))
            rd = os.path.join(d, "build", "raw")
            return self.send(200, {"timeline": tl, "has_video": os.path.exists(os.path.join(ROOT, "out", name + ".mp4")),
                                   "files": sorted(os.listdir(rd)) if os.path.isdir(rd) else []})
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

    def kho_get(self, sub, q):
        """Kho tài nguyên: tìm kiếm, ảnh thu nhỏ, bản xem trước nhẹ, tải file gốc (chỉ trong thư mục kho)."""
        g = lambda k, v="": (q.get(k) or [v])[0]
        if not sub:
            cm = kho.doc()
            dem = {}
            for t in cm["tep"]:
                dem[t["loai"]] = dem.get(t["loai"], 0) + 1
            return self.send(200, dict(kho.tim(cm, g("q"), g("loai"), int(g("trang", "0") or 0)), goc=cm["goc"], luc=cm.get("luc", ""), dem=dem,
                                       loai={k: [v[1], v[2]] for k, v in kho.LOAI.items()}))
        if sub == ["chon"]:  # lấy theo nghĩa: chỉ gợi ý, Hào bấm thêm mới vào video
            return self.send(200, {"tep": kho.chon(kho.doc(), g("y"), g("th"), g("da"), g("loai"), 8)})
        p = kho.duong_dan("kho:" + g("p"))
        if not p or not os.path.isfile(p):
            return self.send(404, {"error": "Không thấy file trong kho"})
        ext = os.path.splitext(p)[1].lower()
        if sub == ["tep"]:  # file gốc (âm thanh, ảnh, mp4/webm) cho trình duyệt phát thẳng
            ct = {".wav": "audio/wav", ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".ogg": "audio/ogg", ".flac": "audio/flac", ".png": "image/png",
                  ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".mp4": "video/mp4", ".webm": "video/webm"}.get(ext)
            return self.file(p, ct) if ct else self.send(415, {"error": "Loại file này không xem trực tiếp được"})
        if sub == ["thongtin"]:  # có kênh trong suốt không, dài bao lâu, khung bao nhiêu (để app tự chọn cách phủ)
            r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=pix_fmt,width,height:format=duration",
                                "-of", "json", p], capture_output=True, text=True, timeout=60)
            j = json.loads(r.stdout or "{}"); st = (j.get("streams") or [{}])[0]
            pf = st.get("pix_fmt", "")
            alpha = bool(re.match(r"(argb|rgba|bgra|abgr|yuva|gbrap|ya8|ya16|pal8)", pf))
            return self.send(200, {"alpha": alpha, "pix_fmt": pf, "w": st.get("width"), "h": st.get("height"),
                                   "dur": float((j.get("format") or {}).get("duration") or 0), "cho": kho.dat_cho(kho.neo(p)) if alpha else None})
        if sub in (["anh"], ["xem"]):
            alpha = g("alpha") == "1"
            h = hashlib.sha1(f"{p}|{os.path.getmtime(p)}|{alpha}".encode()).hexdigest()[:16]
            out = os.path.join(kho.DIR, sub[0], h + (".jpg" if sub == ["anh"] else ".webm" if alpha else ".mp4"))
            if not os.path.exists(out):
                os.makedirs(os.path.dirname(out), exist_ok=True)
                tmp = out + ".tmp" + os.path.splitext(out)[1]
                if sub == ["anh"]:  # ảnh thu nhỏ: khung ở giây 1 (video) hoặc ảnh thu nhỏ
                    cmd = (["-ss", "1"] if ext in kho.LOAI["video"][0] else []) + ["-i", p, "-frames:v", "1", "-filter_complex",
                           "[0:v]scale=320:200:force_original_aspect_ratio=decrease,format=rgba[f];color=0x3a4652:s=320x200[bg];[bg][f]overlay=(W-w)/2:(H-h)/2",
                           "-q:v", "4", tmp]  # nền xám: file trong suốt (chú thích) vẫn thấy hình
                else:  # bản xem trước 540p tối đa 20 giây; overlay trong suốt giữ kênh alpha (webm VP9)
                    cmd = ["-t", "20", "-i", p, "-an", "-vf", "scale=-2:'min(540,ih)'"] + (
                        ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "1M", "-deadline", "realtime", "-cpu-used", "8", tmp] if alpha else
                        ["-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp])
                r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *cmd], capture_output=True, timeout=300)
                if r.returncode or not os.path.exists(tmp):
                    return self.send(500, {"error": "Không tạo được bản xem trước"})
                os.replace(tmp, out)
            return self.file(out, "image/jpeg" if sub == ["anh"] else "video/webm" if alpha else "video/mp4")
        return self.send(404, {"error": "Không có"})

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
        from ban_nhe import duong_dan, lenh
        out = duong_dan(os.path.join(d, "build"), f)  # dùng chung bản nhẹ 540p với phân tích và bản xem (scripts/ban_nhe.py)
        p = proxies.get(out)
        if p and p.poll() == 0 and os.path.exists(out + ".tmp.mp4"):
            os.replace(out + ".tmp.mp4", out)  # tạo xong: đổi tên thì mới tính là có
        running = bool(p and p.poll() is None)
        failed = bool(p and p.poll() not in (None, 0))
        ready = os.path.exists(out)
        if not ready and not running and not failed:
            os.makedirs(os.path.dirname(out), exist_ok=True)
            proxies[out] = subprocess.Popen(lenh(raw, out + ".tmp.mp4"))
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

    def tai_len(self, name, f):
        """Nhận một file video/nhạc vào tai-ve/<tên dự án>/: ghi theo khối 1 MB (file 4K vài GB không chiếm RAM), ghi tạm rồi đổi tên."""
        from tai_drive import ten_an_toan
        n = int(self.headers.get("Content-Length") or 0)
        if not SAFE.match(name) or ten_an_toan(f) != f or not (VIDEO_EXT.search(f) or re.search(AUDIO_EXT, f, re.I)) or n <= 0:
            return self.send(400, {"error": f"Không nhận file {f}: cần tên dự án hợp lệ và file video (.mp4 .mov .m4v .mkv .mts) hoặc nhạc"})
        dich = thu_muc_tai(name)
        os.makedirs(dich, exist_ok=True)
        p = os.path.join(dich, f)
        con = n
        with open(p + ".tai", "wb") as fh:
            while con > 0 and (blk := self.rfile.read(min(con, 1 << 20))):
                fh.write(blk); con -= len(blk)
        if con:
            os.remove(p + ".tai")
            return self.send(400, {"error": f"Tải lên thiếu {f} (mất kết nối?), thử lại"})
        os.replace(p + ".tai", p)
        return self.send(200, {"ok": True, "file": f, "size": n})

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > 2_000_000:
            raise ValueError("Dữ liệu quá lớn")
        return json.loads(self.rfile.read(n) or b"null")

    def luu_cau_hinh(self, parts):
        """Lưu Bảng master: chung (đổi mac_dinh trong cau-hinh/master.json) hoặc riêng dự án (thay cả meta.cau_hinh). Có .bak."""
        import cau_hinh
        try:
            moi = self.body()
            errs = cau_hinh.kiem(moi) if isinstance(moi, dict) else ["Dữ liệu phải là {id: giá trị}"]
        except Exception as ex:
            errs = [f"Dữ liệu không đọc được: {ex}"]
        if errs:
            return self.send(400, {"errors": errs})
        if len(parts) == 2:
            d = json.load(open(cau_hinh.FILE, encoding="utf8"))
            for g in d["nhom"]:
                for t in g["thong_so"]:
                    if t["id"] in moi:
                        t.setdefault("goc", t["mac_dinh"]); t["mac_dinh"] = moi[t["id"]]
            p, du_lieu = cau_hinh.FILE, d
        else:
            if not (dd := self.project(parts[2])):
                return self.send(404, {"error": "Không có dự án này"})
            p = os.path.join(dd, "timeline.json")
            du_lieu = json.load(open(p, encoding="utf8"))
            meta = du_lieu.setdefault("meta", {})
            meta.pop("cau_hinh", None)
            if moi:
                meta["cau_hinh"] = moi
            if (e := check(du_lieu)):
                return self.send(400, {"errors": e})
        shutil.copy(p, p + ".bak")
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf8") as fh:
            json.dump(du_lieu, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, p)
        cau_hinh.bang.cache_clear()
        self.send(200, {"ok": True})

    def do_PUT(self):
        parts, ok = self.route()
        if not ok:
            return self.send(403, {"error": "Sai hoặc thiếu mã khóa"})
        if parts == ["api", "cau-hinh"] or (len(parts) == 4 and parts[:2] == ["api", "p"] and parts[3] == "cau-hinh"):
            return self.luu_cau_hinh(parts)
        if len(parts) == 4 and parts[:2] == ["api", "tai-len"]:  # Hào gửi video thẳng lên (kéo thả/chọn file, cả từ điện thoại)
            return self.tai_len(parts[2], parts[3])
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
        if parts == ["api", "lopchu"]:  # lớp chữ xem trước: đúng mã bộ dựng dùng, cho timeline đang sửa (chưa cần lưu)
            try:
                tl = (self.body() or {}).get("timeline")
                if not isinstance(tl, dict) or (errs := check(tl)):
                    return self.send(400, {"errors": errs if isinstance(tl, dict) else ["Thiếu timeline"]})
                return self.send(200, tao_lop_chu(tl).encode(), "text/html; charset=utf-8")
            except (ValueError, KeyError, TypeError) as ex:
                return self.send(400, {"errors": [str(ex)]})
        if parts == ["api", "apmau"]:  # áp mẫu edit: trả timeline mới, app tự giữ để hoàn tác rồi Hào bấm Lưu
            try:
                req = self.body() or {}
                tl = req.get("timeline")
                if req.get("id") not in MAU or not isinstance(tl, dict) or (errs := check(tl)):
                    return self.send(400, {"error": "Mẫu không có hoặc timeline đang lỗi, bấm Lưu xem lỗi trước"})
                out = ap(tl, MAU[req["id"]])
                return self.send(200, {"timeline": out, "sfx": sum(1 for x in out.get("sfx", []) if x.get("auto"))})
            except (ValueError, KeyError, TypeError) as ex:
                return self.send(400, {"error": f"Không áp được mẫu: {ex}"})
        if parts == ["api", "luumau"]:  # lưu chỉnh sửa của video vào mẫu (mặc định tạo bản mới, mẫu gốc giữ nguyên)
            try:
                req = self.body() or {}
                tl = req.get("timeline")
                if not isinstance(tl, dict) or (errs := check(tl)):
                    return self.send(400, {"error": "Timeline đang lỗi, bấm Lưu xem lỗi trước"})
                return self.send(200, luu_mau(tl, (req.get("ten") or "").strip()[:80] or None, bool(req.get("ghi_de"))))
            except (ValueError, KeyError, TypeError, OSError) as ex:
                return self.send(400, {"error": f"Không lưu được mẫu: {ex}"})
        if parts == ["api", "kho", "chuthich"]:  # gắn biểu tượng chú thích đúng lúc lời nói nhắc tới tiện ích
            try:
                tl = (self.body() or {}).get("timeline")
                if not isinstance(tl, dict) or (errs := check(tl)):
                    return self.send(400, {"error": "Timeline đang lỗi, bấm Lưu xem lỗi trước"})
                out, bao = kho.chu_thich(tl, kho.doc())
                return self.send(200, {"timeline": out, "bao": bao})
            except (ValueError, KeyError, TypeError) as ex:
                return self.send(400, {"error": str(ex)})
        if parts == ["api", "kho", "quet"]:  # chọn/quét lại thư mục kho tài nguyên (chỉ đọc tên file, không mở file)
            try:
                goc = (self.body() or {}).get("goc") or kho.goc_kho()
                cm = kho.luu(goc)
                return self.send(200, {"ok": True, "goc": cm["goc"], "tong": len(cm["tep"])})
            except (ValueError, OSError) as ex:
                return self.send(400, {"error": str(ex)})
        if parts == ["api", "new"]:
            try:
                req = self.body() or {}
                req.pop("tep", None)  # đường dẫn trên máy chỉ dành cho lệnh du_an_moi, không nhận từ trình duyệt
                if not (req.get("drive") or req.get("nguon")):
                    return self.send(200, tao_du_an(req))
                name = kiem_ten(req)[0]
                chay_nen(name, lambda bao: tao_du_an(req, bao))
                return self.send(200, {"job": name})
            except (ValueError, OSError) as ex:
                return self.send(400, {"error": str(ex)})
        if len(parts) == 4 and parts[:2] == ["api", "p"] and parts[3] == "them-nguon" and self.project(parts[2]):  # thêm footage vào dự án đang mở
            try:
                req = self.body() or {}
                req.pop("tep", None)
                chay_nen(parts[2], lambda bao: them_nguon(parts[2], req, bao))
                return self.send(200, {"job": parts[2]})
            except (ValueError, OSError) as ex:
                return self.send(400, {"error": str(ex)})
        if len(parts) != 4 or parts[3] not in ("render", "subtitles", "mastercut", "nle", "kichban", "gopy") or not (d := self.project(parts[2])):
            return self.send(404, {"error": "Không có dự án này"})
        name = parts[2]
        if parts[3] == "gopy":  # gói góp ý cho Claude Code: lời Hào + mốc giờ + timeline + ảnh khung hình hiện tại
            req = self.body() or {}
            note, t = str(req.get("note") or "").strip()[:4000], req.get("t")
            if not note or not isinstance(req.get("timeline"), dict) or not isinstance(t, (int, float)):
                return self.send(400, {"error": "Cần ghi điều muốn sửa"})
            gd = os.path.join(d, "gop-y", time.strftime("%Y%m%d-%H%M%S"))
            os.makedirs(gd, exist_ok=True)
            json.dump(req["timeline"], open(os.path.join(gd, "timeline.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
            anh = ""
            m = re.match(r"^data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)$", str(req.get("frame") or ""))
            if m and len(m.group(2)) < 8_000_000:
                anh = "khung." + ("png" if m.group(1) == "png" else "jpg")
                open(os.path.join(gd, anh), "wb").write(base64.b64decode(m.group(2)))
            ra = os.path.relpath(gd, os.path.join(ROOT, ".."))
            open(os.path.join(gd, "y-kien.md"), "w", encoding="utf8").write(
                f"# Góp ý cho dự án {name}\n\nMốc giờ: {t:.1f}s\n\nÝ kiến của Hào:\n{note}\n\n"
                + (f"Ảnh khung hình (video gốc, chưa gồm chữ/hiệu ứng): {anh}. Hào nên chụp thêm màn hình app và để cùng thư mục này.\n" if anh else "Chưa có ảnh khung: Hào chụp màn hình app và để cùng thư mục này.\n")
                + "\nCách xử lý cho Claude Code: đọc file này, timeline.json cùng thư mục, `video-studio/docs` liên quan (GHI-NHO-NGHIEM-THU.md). Lỗi chỉ là thông số thì sửa timeline của dự án; lỗi lặp lại cho mọi video thì sửa mẫu (thu-vien-mau/) hoặc mã.\n")
            return self.send(200, {"ok": True, "thu_muc": ra, "anh": bool(anh), "lenh": f"Đọc {ra}/y-kien.md và sửa theo góp ý của Hào."})
        if parts[3] == "kichban":  # đặt chữ theo KICH-BAN.md + giọng nói; trả timeline mới, app giữ để hoàn tác
            kb = os.path.join(d, "KICH-BAN.md")
            if not os.path.exists(kb):
                return self.send(404, {"error": "Dự án chưa có KICH-BAN.md (mẫu: mau/du-an-video/KICH-BAN.md)"})
            try:
                tl = (self.body() or {}).get("timeline")
                if not isinstance(tl, dict) or (errs := check(tl)):
                    return self.send(400, {"error": "Timeline đang lỗi, bấm Lưu xem lỗi trước"})
                out, bao = dat_chu(tl, open(kb, encoding="utf8").read())
            except (ValueError, KeyError, TypeError) as ex:
                return self.send(400, {"error": f"Không đọc được kịch bản: {ex}"})
            return self.send(200, {"timeline": out, "bao": bao})
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
            from thu_vien import thieu, lenh_cai
            t = thieu("numpy", "faster_whisper", *(["cv2"] if script == "master_cut.py" else []))
            if t:  # báo ngay trên app, không chạy rồi mới lỗi giữa chừng
                return self.send(400, {"error": f"Thiếu thư viện {', '.join(t)} trong Python {sys.executable}. Cài: {lenh_cai(t)}"})
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
    print(f"Python: {sys.executable} (bản {sys.version.split()[0]})")
    print(f"App timeline: http://127.0.0.1:{port}/?t={TOKEN}" + ("" if lan else f"  (trên chính máy này mở http://localhost:{port} cũng được)"))
    if lan:
        print(f"Điện thoại cùng wifi: http://{lan_ip()}:{port}/?t={TOKEN}")
    srv.serve_forever()
