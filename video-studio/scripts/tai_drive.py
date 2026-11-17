"""Tải cả thư mục Google Drive (chia sẻ "Bất kỳ ai có đường liên kết") về máy, không cần đăng nhập hay khoá API.
Dùng: python scripts/tai_drive.py "<link thư mục Drive>" <thư mục đích>
App studio (Dự án mới → Từ Google Drive) và scripts/du_an_moi.py dùng cùng hàm này.
Chỉ tải file ở cấp đầu của thư mục (không vào thư mục con); file đã có đủ dung lượng thì bỏ qua (tải lại an toàn)."""
import html, os, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}


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
    fid = id_thu_muc(link)
    with urllib.request.urlopen(urllib.request.Request(f"https://drive.google.com/embeddedfolderview?id={fid}", headers=UA), timeout=60) as r:
        ds = doc_danh_sach(r.read().decode("utf8", "replace"))
    if not ds:
        raise ValueError("Không thấy file nào. Kiểm tra thư mục đã chia sẻ 'Bất kỳ ai có đường liên kết' chưa.")
    return ds


def ten_an_toan(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s).strip() or "file"


def tai(link, dich, bao=lambda **k: None):
    """Tải mọi file của thư mục Drive vào `dich`. bao(i, n, ten, da, tong) báo tiến độ. Trả danh sách tên file."""
    os.makedirs(dich, exist_ok=True)
    ds, ten = liet_ke(link), []
    for i, (fid, tieu_de) in enumerate(ds, 1):
        url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            cd = r.headers.get("Content-Disposition", "")
            try:  # http.client đọc tiêu đề theo latin-1; Drive gửi tên file UTF-8 (tiếng Việt)
                cd = cd.encode("latin-1").decode("utf8")
            except UnicodeError:
                pass
            m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="([^"]+)"', cd)
            f = ten_an_toan(urllib.parse.unquote(m.group(1)) if m else tieu_de)
            tong = int(r.headers.get("Content-Length") or 0)
            p = os.path.join(dich, f)
            if tong and os.path.exists(p) and os.path.getsize(p) == tong:
                ten.append(f); bao(i=i, n=len(ds), ten=f, da=tong, tong=tong); continue
            da = 0
            with open(p + ".tai", "wb") as fh:  # ghi tạm rồi đổi tên: đứt mạng giữa chừng không để lại file hỏng mang tên thật
                while blk := r.read(1 << 20):
                    fh.write(blk); da += len(blk); bao(i=i, n=len(ds), ten=f, da=da, tong=tong)
            if tong and da != tong:
                raise IOError(f"Tải thiếu {f}: {da}/{tong} byte, thử lại")
            os.replace(p + ".tai", p)
        ten.append(f)
    return ten


def _tu_kiem():
    assert id_thu_muc("https://drive.google.com/drive/folders/1DnYN3AS_zmchRuNEz-uySK-EgwEi5ol_?usp=sharing") == "1DnYN3AS_zmchRuNEz-uySK-EgwEi5ol_"
    assert id_thu_muc("https://drive.google.com/open?id=1AbCdEfGhIjK") == "1AbCdEfGhIjK"
    trang = ('<div class="flip-entry" id="entry-AAAAAAAAAA1" tabindex="0"><a href="https://drive.google.com/file/d/AAAAAAAAAA1/view">'
             '<div class="flip-entry-title">c&#7843;nh 1</div></a></div>'
             '<div class="flip-entry" id="entry-BBBBBBBBBB2"><a href="https://drive.google.com/drive/folders/BBBBBBBBBB2">'
             '<div class="flip-entry-title">thư mục con</div></a></div>')
    assert doc_danh_sach(trang) == [("AAAAAAAAAA1", "cảnh 1")], doc_danh_sach(trang)
    assert ten_an_toan('a/b:c?.MOV') == "a_b_c_.MOV"
    try:
        id_thu_muc("không phải link"); raise AssertionError
    except ValueError:
        pass
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 3:
        def in_bao(i, n, ten, da, tong):
            print(f"\r[{i}/{n}] {ten}: {da >> 20}/{tong >> 20} MB   ", end="", flush=True)
        fs = tai(sys.argv[1], sys.argv[2], in_bao)
        print(f"\nXong: {len(fs)} file → {sys.argv[2]}")
    else:
        sys.exit('Dùng: python scripts/tai_drive.py "<link thư mục Drive>" <thư mục đích>')
