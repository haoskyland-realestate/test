"""Tải footage từ link về máy (Dự án mới nhiều nguồn, Hào chốt 18/11): Google Drive (thư mục hoặc 1 file, chia sẻ "Bất kỳ ai có đường liên kết",
không cần đăng nhập), link tải trực tiếp (.mp4/.mov…), YouTube/TikTok (cần thư viện yt-dlp; chỉ dùng video của mình/được đồng ý, hoặc làm mẫu học phong cách).
Dùng: python scripts/tai_drive.py "<link>" <thư mục đích>
App studio (Dự án mới, Thêm footage) và scripts/du_an_moi.py dùng cùng các hàm này.
Drive chỉ tải file ở cấp đầu của thư mục; file đã có đủ dung lượng thì bỏ qua (tải lại an toàn)."""
import html, os, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
LUU_Y_BAN_QUYEN = "Lưu ý: chỉ dùng video YouTube/TikTok của chính mình hoặc được chủ video đồng ý; video người khác chỉ để học phong cách, không đưa vào video đăng."


def nhan_dang(url):
    """'drive' | 'youtube' | 'link'. ValueError nếu không phải link http(s)."""
    u = url.strip()
    if not re.match(r"https?://", u, re.I):
        raise ValueError("Link phải bắt đầu bằng http:// hoặc https://")
    host = urllib.parse.urlparse(u).netloc.lower()
    if host.endswith("drive.google.com") or host.endswith("docs.google.com"):
        return "drive"
    if re.search(r"(^|\.)(youtube\.com|youtu\.be|tiktok\.com)$", host):
        return "youtube"
    return "link"


def id_thu_muc(link):
    """ID thư mục từ link Drive (…/folders/<id>…, …?id=<id>) hoặc chính ID."""
    m = re.search(r"folders/([\w-]{10,})", link) or re.search(r"[?&]id=([\w-]{10,})", link) or re.fullmatch(r"\s*([\w-]{10,})\s*", link)
    if not m:
        raise ValueError("Không đọc được link thư mục Google Drive (dạng https://drive.google.com/drive/folders/…)")
    return m.group(1)


def doc_danh_sach(trang):
    """[(id, tên)] các FILE trong trang embeddedfolderview (bỏ thư mục con)."""
    out = []
    for m in re.finditer(r'class="flip-entry" id="entry-([\w-]+)".*?<a href="([^"]+)".*?class="flip-entry-title">([^<]*)<', trang, re.S):
        if "/folders/" not in m.group(2):
            out.append((m.group(1), html.unescape(m.group(3)).strip()))
    return out


def liet_ke(link):
    """[(id, tên)] file trong link Drive: link 1 file (…/file/d/<id>) hoặc thư mục."""
    if m := re.search(r"/file/d/([\w-]{10,})", link):
        return [(m.group(1), "")]
    fid = id_thu_muc(link)
    with urllib.request.urlopen(urllib.request.Request(f"https://drive.google.com/embeddedfolderview?id={fid}", headers=UA), timeout=60) as r:
        ds = doc_danh_sach(r.read().decode("utf8", "replace"))
    if not ds:
        raise ValueError("Không thấy file nào. Kiểm tra thư mục đã chia sẻ 'Bất kỳ ai có đường liên kết' chưa.")
    return ds


def ten_an_toan(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s).strip().lstrip(".") or "file"


def ten_tu_header(r, du_phong):
    cd = r.headers.get("Content-Disposition", "")
    try:  # http.client đọc tiêu đề theo latin-1; Drive gửi tên file UTF-8 (tiếng Việt)
        cd = cd.encode("latin-1").decode("utf8")
    except UnicodeError:
        pass
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="([^"]+)"', cd)
    return ten_an_toan(urllib.parse.unquote(m.group(1)) if m else du_phong)


def tai_url(url, dich, du_phong, bao, i, n):
    """Tải một URL vào `dich` theo khối 1 MB, ghi tạm rồi đổi tên; từ chối trang web. Trả tên file."""
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        if "text/html" in r.headers.get("Content-Type", ""):
            raise ValueError(f"Link này là trang web, không phải file video: {url[:80]}")
        f = ten_tu_header(r, du_phong)
        tong = int(r.headers.get("Content-Length") or 0)
        p = os.path.join(dich, f)
        if tong and os.path.exists(p) and os.path.getsize(p) == tong:
            bao(i=i, n=n, ten=f, da=tong, tong=tong)
            return f
        da = 0
        with open(p + ".tai", "wb") as fh:  # đứt mạng giữa chừng không để lại file hỏng mang tên thật
            while blk := r.read(1 << 20):
                fh.write(blk); da += len(blk); bao(i=i, n=n, ten=f, da=da, tong=tong)
        if tong and da != tong:
            raise IOError(f"Tải thiếu {f}: {da}/{tong} byte, thử lại")
        os.replace(p + ".tai", p)
    return f


def tai(link, dich, bao=lambda **k: None):
    """Tải mọi file của link Drive vào `dich`. bao(i, n, ten, da, tong) báo tiến độ. Trả danh sách tên file."""
    os.makedirs(dich, exist_ok=True)
    ds = liet_ke(link)
    return [tai_url(f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t", dich, tieu_de or fid, bao, i, len(ds))
            for i, (fid, tieu_de) in enumerate(ds, 1)]


def tai_youtube(url, dich, bao=lambda **k: None):
    """YouTube/TikTok bằng yt-dlp (tối đa 4K, gộp hình + tiếng thành mp4). Trả [tên file]."""
    try:
        import yt_dlp
    except ImportError:
        from thu_vien import lenh_cai
        raise ValueError("Chưa cài yt-dlp để tải YouTube/TikTok. Cài: " + lenh_cai(["yt_dlp"]))
    print(LUU_Y_BAN_QUYEN, flush=True)
    ten = []

    def hook(d):
        if d.get("status") == "downloading":
            bao(i=1, n=1, ten=os.path.basename(d.get("filename", "")), da=d.get("downloaded_bytes") or 0,
                tong=d.get("total_bytes") or d.get("total_bytes_estimate") or 0)
        elif d.get("status") == "finished":
            ten.append(d.get("filename"))
    opts = {"format": "bv*[height<=2160]+ba/b", "merge_output_format": "mp4", "outtmpl": os.path.join(dich, "%(title).80s [%(id)s].%(ext)s"),
            "noplaylist": True, "quiet": True, "progress_hooks": [hook], "restrictfilenames": False}
    os.makedirs(dich, exist_ok=True)
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=True)
        return [os.path.basename(y.prepare_filename(info)).rsplit(".", 1)[0] + ".mp4"]


def tai_nguon(url, dich, bao=lambda **k: None):
    """Tải một link bất kỳ (Drive, trực tiếp, YouTube/TikTok) vào `dich`. Trả danh sách tên file đã có trong `dich`."""
    loai = nhan_dang(url)
    if loai == "drive":
        return tai(url, dich, bao)
    if loai == "youtube":
        return tai_youtube(url, dich, bao)
    os.makedirs(dich, exist_ok=True)
    goc = os.path.basename(urllib.parse.urlparse(url).path) or "video.mp4"
    return [tai_url(url, dich, urllib.parse.unquote(goc), bao, 1, 1)]


def xem(url):
    """Xem trước link (không tải): {'loai', 'files': [tên…], 'ghi_chu'}."""
    loai = nhan_dang(url)
    if loai == "drive":
        return {"loai": loai, "files": [t or "1 file Drive" for _, t in liet_ke(url)]}
    if loai == "youtube":
        try:
            import yt_dlp
        except ImportError:
            return {"loai": loai, "files": [url], "ghi_chu": "Chưa cài yt-dlp: bấm Tạo sẽ báo lệnh cài"}
        with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": True}) as y:
            info = y.extract_info(url, download=False)
        return {"loai": loai, "files": [f"{info.get('title', 'video')} ({int(info.get('duration') or 0)}s)"], "ghi_chu": LUU_Y_BAN_QUYEN}
    with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, "Range": "bytes=0-0"}), timeout=60) as r:
        if "text/html" in r.headers.get("Content-Type", ""):
            raise ValueError("Link này là trang web, không phải file video")
        tong = int((r.headers.get("Content-Range") or "/0").rsplit("/", 1)[-1] or 0) or int(r.headers.get("Content-Length") or 0)
        f = ten_tu_header(r, urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(url).path)) or "video.mp4")
    return {"loai": loai, "files": [f + (f" ({tong >> 20} MB)" if tong > 1 else "")]}


def _tu_kiem():
    import http.server, shutil, tempfile, threading
    assert id_thu_muc("https://drive.google.com/drive/folders/1DnYN3AS_zmchRuNEz-uySK-EgwEi5ol_?usp=sharing") == "1DnYN3AS_zmchRuNEz-uySK-EgwEi5ol_"
    assert id_thu_muc("https://drive.google.com/open?id=1AbCdEfGhIjK") == "1AbCdEfGhIjK"
    assert liet_ke("https://drive.google.com/file/d/1AbCdEfGhIjKlm/view?usp=sharing") == [("1AbCdEfGhIjKlm", "")]
    trang = ('<div class="flip-entry" id="entry-AAAAAAAAAA1" tabindex="0"><a href="https://drive.google.com/file/d/AAAAAAAAAA1/view">'
             '<div class="flip-entry-title">c&#7843;nh 1</div></a></div>'
             '<div class="flip-entry" id="entry-BBBBBBBBBB2"><a href="https://drive.google.com/drive/folders/BBBBBBBBBB2">'
             '<div class="flip-entry-title">thư mục con</div></a></div>')
    assert doc_danh_sach(trang) == [("AAAAAAAAAA1", "cảnh 1")], doc_danh_sach(trang)
    assert ten_an_toan('a/b:c?.MOV') == "a_b_c_.MOV" and ten_an_toan("../.x") == "_.x"  # không cho tên ẩn/đi ngược thư mục
    assert [nhan_dang(u) for u in ("https://drive.google.com/drive/folders/x", "https://youtu.be/abc", "https://www.tiktok.com/@a/video/1",
                                   "https://m.youtube.com/watch?v=1", "https://x.com/a.mp4")] == ["drive", "youtube", "youtube", "youtube", "link"]
    for sai in ("không phải link", "ftp://a/b.mp4"):
        try:
            nhan_dang(sai); raise AssertionError(sai)
        except ValueError:
            pass
    # link trực tiếp: máy chủ cục bộ tạm, có file video và một trang web
    goc = tempfile.mkdtemp(); dich = tempfile.mkdtemp()
    open(os.path.join(goc, "canh 1.mp4"), "wb").write(b"\0" * 3_000_000)
    open(os.path.join(goc, "trang.html"), "w").write("<html></html>")
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(s, *a, **k): super().__init__(*a, directory=goc, **k)
        def log_message(s, *a): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    srv.handle_error = lambda *a: None  # xem trước đóng kết nối sớm: bình thường
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}/"
        old = urllib.request._opener
        urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))  # máy chủ cục bộ: không đi qua proxy
        assert xem(base + "canh%201.mp4")["files"] == ["canh 1.mp4 (2 MB)"], xem(base + "canh%201.mp4")
        assert tai_nguon(base + "canh%201.mp4", dich) == ["canh 1.mp4"] and os.path.getsize(os.path.join(dich, "canh 1.mp4")) == 3_000_000
        assert tai_nguon(base + "canh%201.mp4", dich) == ["canh 1.mp4"]  # lần 2: đã đủ, bỏ qua
        try:
            tai_nguon(base + "trang.html", dich); raise AssertionError("phải từ chối trang web")
        except ValueError:
            pass
        assert not any(f.endswith(".tai") for f in os.listdir(dich))
        urllib.request.install_opener(old)
    finally:
        srv.shutdown(); shutil.rmtree(goc); shutil.rmtree(dich)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 3:
        def in_bao(i, n, ten, da, tong):
            print(f"\r[{i}/{n}] {ten}: {da >> 20}/{tong >> 20} MB   ", end="", flush=True)
        fs = tai_nguon(sys.argv[1], sys.argv[2], in_bao)
        print(f"\nXong: {len(fs)} file → {sys.argv[2]}")
    else:
        sys.exit('Dùng: python scripts/tai_drive.py "<link>" <thư mục đích>')
