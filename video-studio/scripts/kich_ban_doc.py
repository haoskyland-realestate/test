"""Kịch bản từ Google Doc (Hào chốt 27/11: Hào viết kịch bản trên Google Doc, gửi link cùng video thô).
Tải bản chữ của Doc (chia sẻ "Bất kỳ ai có đường liên kết"), tách thành câu đánh số, ghi KICH-BAN.md của dự án
(bảng # / Giây / Lời đọc / Chữ trên màn hình / Cảnh gợi ý — đúng định dạng kich_ban.py, doi_chieu.py, xep_canh.py đọc).
Chạy trong video-studio:
  python scripts/kich_ban_doc.py projects/<tên> <link Google Doc | file .txt/.md>
Không tải được (Doc chưa chia sẻ, mạng chặn docs.google.com) → Claude đọc Doc bằng công cụ Google Docs, lưu ra file .txt rồi chạy lại với file đó.
Bản gốc giữ ở build/kich-ban-goc.txt; KICH-BAN.md cũ (nếu có) lưu .bak."""
import os, re, shutil, sys, urllib.request

ID = re.compile(r"/document/d/([\w-]{20,})")


def tai(nguon):
    """Chữ của kịch bản: link Google Doc (tải bản .txt) hoặc đường dẫn file trên máy."""
    m = ID.search(nguon)
    if not m:
        return open(nguon, encoding="utf8").read()
    url = f"https://docs.google.com/document/d/{m[1]}/export?format=txt"
    with urllib.request.urlopen(url, timeout=60) as r:
        if "text/plain" not in r.headers.get("Content-Type", ""):
            raise ValueError("Doc chưa chia sẻ 'Bất kỳ ai có đường liên kết' (Google trả về trang đăng nhập)")
        return r.read().decode("utf-8-sig")


def tach_cau(van_ban):
    """Mỗi đoạn một hoặc vài câu nói; đoạn dài (> 2 câu) tách theo dấu . ? ! Bỏ dòng trống, tiêu đề kiểu '#', dòng gạch đầu dòng giữ lại chữ."""
    out = []
    for dong in van_ban.replace("\r", "").split("\n"):
        dong = re.sub(r"^\s*(#+|[-*•]|\d+[.)])\s*", "", dong).strip()
        if not dong:
            continue
        cau = [c.strip() for c in re.split(r"(?<=[.?!…])\s+", dong) if c.strip()]
        out += cau if len(cau) > 2 else [" ".join(cau)]
    return out


def bang(cau, ten="kịch bản"):
    o = lambda s: s.replace("|", "/")
    return "\n".join([f"# KỊCH BẢN: {ten}", "",
                      "> Tạo từ Google Doc bằng `scripts/kich_ban_doc.py`. Cột \"Lời đọc\" dùng để tự xếp clip (`xep_canh.py`) và đối chiếu ghi âm; "
                      "cột \"Chữ trên màn hình\" để trống cho Claude/Hào điền (`nhãn / *CHỮ LỚN* / dòng dưới`).", "",
                      "| # | Giây | Lời đọc | Chữ trên màn hình (`*từ*` = tô vàng) | Cảnh gợi ý |", "|---|---|---|---|---|"]
                     + [f"| {i} | | {o(c)} | | |" for i, c in enumerate(cau, 1)]) + "\n"


def ghi(pj, nguon):
    goc = tai(nguon)
    cau = tach_cau(goc)
    if not cau:
        raise ValueError("Kịch bản trống")
    os.makedirs(os.path.join(pj, "build"), exist_ok=True)
    open(os.path.join(pj, "build", "kich-ban-goc.txt"), "w", encoding="utf8").write(goc)
    p = os.path.join(pj, "KICH-BAN.md")
    if os.path.exists(p):
        shutil.copy(p, p + ".bak")
    open(p, "w", encoding="utf8").write(bang(cau, os.path.basename(os.path.abspath(pj))))
    return cau


def _tu_kiem():
    import tempfile
    t = tempfile.mkdtemp()
    f = os.path.join(t, "kb.txt")
    open(f, "w", encoding="utf8").write("# Video Cần Giờ\n\nChào anh chị, em là Hùng.\n\n- Dự án rộng 2.870 ha | ven biển.\n"
                                        "Câu một. Câu hai? Câu ba!\n\n")
    cau = ghi(t, f)
    assert cau == ["Video Cần Giờ", "Chào anh chị, em là Hùng.", "Dự án rộng 2.870 ha | ven biển.", "Câu một.", "Câu hai?", "Câu ba!"], cau
    from doi_chieu import doc_kich_ban  # định dạng phải đọc được bằng bộ đọc đang dùng
    rows = doc_kich_ban(t)
    assert [r[1] for r in rows][2] == "Dự án rộng 2.870 ha / ven biển." and len(rows) == 6, rows
    assert ID.search("https://docs.google.com/document/d/1AbCdEfGhIjKlMnOpQrStUvWxYz123/edit?usp=sharing")[1].startswith("1AbC")
    ghi(t, f)
    assert os.path.exists(os.path.join(t, "KICH-BAN.md.bak"))
    shutil.rmtree(t)
    print("OK")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 3:
        try:
            print(f"Đã ghi KICH-BAN.md: {len(ghi(os.path.abspath(sys.argv[1]), sys.argv[2]))} câu")
        except Exception as ex:
            sys.exit(f"Không đọc được kịch bản: {ex}\nCách khác: Claude đọc Doc bằng công cụ Google Docs, lưu .txt, chạy lại với file đó.")
    else:
        sys.exit(__doc__)
