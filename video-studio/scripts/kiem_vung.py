"""Kiểm vùng an toàn TikTok/Reels/Shorts cho lớp chữ của dự án (cổng bắt buộc trước bản cuối, theo AutoEdit mục 4):
mọi chữ, thẻ, icon phải nằm trong khung: trên 15%, dưới 25% (mép dưới ≤ 75% chiều cao), trái/phải 10%.
Dùng đúng đoạn đo của autoedit/tools/safe_check.py, chạy trên trang lớp chữ thật (lop_chu.tao), tua bằng window.dat(t),
ở giữa và gần cuối mỗi khối chữ/thẻ. Chạy trong video-studio:  python scripts/kiem_vung.py projects/<tên>  (thoát mã 1 nếu có chỗ tràn)
Cần thư viện playwright (pip install playwright); trình duyệt dùng Chrome của HyperFrames nếu máy chưa cài Chromium cho playwright."""
import glob, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from cau_hinh import lay


def gioi_han(tl):
    """Khung an toàn (tỉ lệ khung) từ bảng master nhóm vung."""
    from timeline import size
    W, H = size(tl or {})
    if W > H:  # khung ngang YouTube: vùng an toàn riêng (title-safe); khung dọc theo TikTok/AutoEdit
        t, d, ben = lay("vung.yt_tren", tl), lay("vung.yt_duoi", tl), lay("vung.yt_ben", tl)
    else:
        t, d, ben = lay("vung.tren", tl), lay("vung.duoi", tl), lay("vung.ben", tl)
    return {"t": t, "b": d, "l": ben, "r": round(1 - ben, 6)}


def js_do():
    """Đoạn JS đo chỗ tràn, lấy nguyên từ safe_check.py của AutoEdit (một nguồn duy nhất)."""
    s = open(os.path.join(ROOT, "autoedit", "tools", "safe_check.py"), encoding="utf8").read()
    return re.search(r"JS='''(.*?)'''", s, re.S).group(1)


def moc(tl):
    """Mốc kiểm: giữa và gần cuối mỗi khối chữ/thẻ (lúc chữ đã hiện đủ)."""
    ts = set()
    for x in tl.get("texts", []) + tl.get("cards", []):
        ts.update((round(x["start"] + x["dur"] * .5, 2), round(x["start"] + max(x["dur"] - .25, x["dur"] * .5), 2)))
    return sorted(ts)


def mo_trinh_duyet(p):
    try:
        return p.chromium.launch()
    except Exception:  # chưa cài Chromium cho playwright: dùng Chrome HyperFrames đã tải sẵn
        exe = glob.glob(os.path.expanduser("~/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell*/chrome-headless-shell*"))
        exe = [e for e in exe if os.path.isfile(e) and not e.endswith((".pak", ".dat"))]
        if not exe:
            raise SystemExit("Chưa có trình duyệt để kiểm vùng an toàn: chạy  python -m playwright install chromium")
        return p.chromium.launch(executable_path=exe[0])


def kiem(pj, tl=None):
    """[(giây, mô tả chỗ tràn)]. Rỗng = đạt."""
    from playwright.sync_api import sync_playwright
    from lop_chu import tao
    from timeline import size
    tl = tl or json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    W, H = size(tl)
    d = os.path.join(pj, "build", "vung")
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "node_modules", "gsap", "dist", "gsap.min.js"), d)
    open(os.path.join(d, "index.html"), "w", encoding="utf8").write(tao(tl))
    js, out = js_do(), []
    with sync_playwright() as p:
        b = mo_trinh_duyet(p)
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + os.path.abspath(os.path.join(d, "index.html")))
        pg.wait_for_timeout(1500)  # chờ phông chữ
        for t in moc(tl):
            pg.evaluate(f"window.dat({t})")
            pg.wait_for_timeout(60)
            out += [(t, x) for x in pg.evaluate(js, ["#root", gioi_han(tl)])]
        b.close()
    return out


def _tu_kiem():
    import tempfile
    pj = tempfile.mkdtemp()
    os.makedirs(os.path.join(pj, "build"))
    tl = {"version": 1, "meta": {"platform": "tiktok"}, "clips": [{"file": "a.mp4", "in": 0, "dur": 6}], "transitions": [],
          "texts": [{"kind": "title3d", "start": 0.5, "dur": 2, "top": "kiểm", "big": "TRONG KHUNG"}]}
    assert kiem(pj, tl) == [], kiem(pj, tl)
    tl["texts"].append({"kind": "loi", "start": 3, "dur": 2, "words": [["mép", 3, 3.5], ["dưới", 3.5, 4]], "hl": [], "top_px": 1800})
    assert kiem(pj, tl) == [], "bố cục chữ theo nhịp nói phải tự kẹp vào vùng an toàn"
    tl["cards"] = [{"kieu": "kinh", "start": 4, "dur": 1.5, "title": "x" * 60}]
    assert any("tràn" in x for _, x in kiem(pj, tl)), "chữ quá dài tràn khung phải bị bắt"
    assert gioi_han({"meta": {"platform": "youtube"}}) == {"t": 0.05, "b": 0.88, "l": 0.05, "r": 0.95}   # khung ngang: vùng YouTube
    yt = {**tl, "meta": {"platform": "youtube"}, "cards": [], "texts": tl["texts"][:1]}
    assert kiem(pj, yt) == [], kiem(pj, yt)                                                          # chữ lớn nằm gọn khung YouTube
    shutil.rmtree(pj)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        loi = kiem(os.path.abspath(sys.argv[1]))
        for t, x in loi[:30]:
            print(f"{t:.2f}s: {x}")
        print("Vùng an toàn: ĐẠT" if not loi else f"Vùng an toàn: {len(loi)} chỗ tràn (sửa rồi chạy lại)")
        sys.exit(1 if loi else 0)
    else:
        sys.exit(__doc__)
