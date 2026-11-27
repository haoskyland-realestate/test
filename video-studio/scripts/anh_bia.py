"""Ảnh bìa (thumbnail), Hào chốt 27/11: mỗi video tự tạo 3 phương án cho TikTok (1080×1920) và YouTube (1280×720), Hào chọn.
- Khung nền: 3 khung đẹp nhất của bản dựng (phan_tich_hinh.diem: nét, sáng, có mặt người nói, không chớp), cách nhau ≥ 3 giây.
- Chữ: hook trong BAN-DUNG.json (vai "hook", hoặc chữ lớn đầu tiên); chưa có thì 6 từ đầu lời nói. Chữ đã qua cổng đối chiếu, không bịa.
- 3 kiểu: A chữ trên nền tối dần · B dải chữ dưới · C chữ vàng nhấn giữa. Chữ nằm trong vùng an toàn (bảng master).
- Lưu video-studio/anh-bia/<dự án>/ (không lên GitHub) + ANH-BIA.md (Hào ghi phương án chọn) + dòng trong anh-bia/KHO-ANH-BIA.md.
Chạy trong video-studio:  python scripts/anh_bia.py projects/<tên> [video.mp4]   ·   tự kiểm: --tu-kiem"""
import base64, html, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
KHO = os.path.join(ROOT, "anh-bia")
FONT = os.path.join(ROOT, "autoedit", "assets", "fonts", "danta-xbold.otf")  # phông Hào có quyền dùng (gói AutoEdit)
from ban_dung import hoa  # viết hoa như chữ lớn trong video: giữ đơn vị viết thường (1.080 ha, 75 m², không "HA")
KHO_ANH = {"tiktok": (1080, 1920), "youtube": (1280, 720)}


def chon_khung(cac, n=3, cach=3.0, dau=0.5, cuoi=1.0):
    """cac: [(giây, điểm)] → n mốc điểm cao nhất, cách nhau ≥ cach giây, bỏ 0,5 giây đầu và 1 giây cuối."""
    het = max((t for t, _ in cac), default=0)
    out = []
    for t, d in sorted(cac, key=lambda x: -x[1]):
        if dau <= t <= het - cuoi and all(abs(t - u) >= cach for u in out):
            out.append(t)
        if len(out) == n:
            break
    return sorted(out)


def chu_hook(pj, ws):
    bd = json.load(open(os.path.join(pj, "BAN-DUNG.json"), encoding="utf8")) if os.path.exists(os.path.join(pj, "BAN-DUNG.json")) else {}
    for v in bd.get("vai", []):
        if v.get("vai") == "hook":
            return v.get("chu") or " ".join(w[0] for w in ws[v["tu"][0]:v["tu"][1] + 1])
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    lon = [x for x in tl.get("texts", []) if x.get("kind") == "title3d" and x.get("big")]
    if lon:
        return lon[0]["big"]
    import re
    dau = []  # chưa có hook đã duyệt: câu đầu tới dấu câu đầu tiên, tối đa 8 từ (chữ tạm, ghi rõ trong ANH-BIA.md)
    for w in ws[:8]:
        dau.append(w[0])
        if re.search(r"[,.?!]$", w[0]):
            break
    return " ".join(dau).rstrip(",.") + " …" * (len(dau) == 8)


def trang(nen, chu, kieu, W, H, vung):
    """HTML một ảnh bìa: nền là khung hình (cover), chữ theo kiểu A/B/C, gói trong vùng an toàn."""
    t, d, l = vung["t"] * H, vung["b"] * H, vung["l"] * W
    co = int(min(W * 0.11, H * 0.075) if W < H else H * 0.12)
    nen64 = base64.b64encode(open(nen, "rb").read()).decode()
    font = base64.b64encode(open(FONT, "rb").read()).decode() if os.path.exists(FONT) else ""
    vi = {"A": f"top:{t}px;bottom:auto", "B": f"top:auto;bottom:{H - d}px", "C": f"top:{(t + d) / 2 - co * 1.2}px;bottom:auto"}[kieu]
    phu = {"A": "linear-gradient(#000c,#0000 55%)", "B": "linear-gradient(#0000 45%,#000d)", "C": "radial-gradient(#0006,#0000 70%)"}[kieu]
    mau = "#ffd23f" if kieu == "C" else "#fff"
    return f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:bia;src:url(data:font/otf;base64,{font})}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.nen{{position:absolute;inset:0;background:url(data:image/jpeg;base64,{nen64}) center {'42%' if W > H else '30%'}/cover}}
.phu{{position:absolute;inset:0;background:{phu}}}
.chu{{position:absolute;left:{l}px;right:{l}px;{vi};font:{co}px/1.08 bia,'Arial Black',sans-serif;color:{mau};
 text-align:{'left' if W > H else 'center'};text-wrap:balance;text-shadow:0 4px 18px #000c;letter-spacing:-.01em;overflow-wrap:anywhere}}
</style><div class="nen"></div><div class="phu"></div><div class="chu" id="chu">{html.escape(hoa(chu))}</div>"""


def chup(trangs, W, H):
    """Chụp danh sách (html, file png) bằng Chromium; trả True nếu chữ nằm gọn vùng an toàn ở mọi ảnh."""
    from playwright.sync_api import sync_playwright
    from kiem_vung import mo_trinh_duyet  # Chromium của playwright, thiếu thì Chrome đi kèm HyperFrames
    gon = True
    with sync_playwright() as p:
        b = mo_trinh_duyet(p)
        pg = b.new_page(viewport={"width": W, "height": H})
        for h, out in trangs:
            pg.set_content(h)
            pg.wait_for_timeout(200)
            r = pg.eval_on_selector("#chu", "e=>{const b=e.getBoundingClientRect();return [b.top,b.bottom,e.scrollWidth<=e.clientWidth]}")
            gon &= r[0] >= 0 and r[1] <= H and r[2]
            pg.screenshot(path=out)
        b.close()
    return gon


def khung_sach(pj, tl, t, out, W, H):
    """Khung sạch ở giây t của video thành phẩm: lấy thẳng từ footage gốc (không phụ đề, không vạch), cùng khung cắt và chuyển tông như bộ dựng.
    Trả False nếu lúc đó đang là cảnh trám/thẻ (ảnh bìa nên là mặt người nói)."""
    from storyboard import canh
    from timeline import layout
    from mau import khung  # khung() đã gồm chuyển tông HDR → màu thường
    c = next((c for c in canh(tl) if c[0] <= t < c[1]), None)
    if not c or c[2] != "clip":
        return False
    x = tl["clips"][c[3]]
    raw = os.path.join(pj, "build", "raw", x["file"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{x.get('in', 0) + t - layout(tl)['starts'][c[3]]:.2f}", "-i", raw, "-frames:v", "1",
                    "-vf", khung(raw, W, H, x.get("focus", 0), x.get("fit")), "-q:v", "2", out], check=True)
    return os.path.exists(out)


def tao(pj, video=None):
    import cv2
    from phan_tich_hinh import phan_tich, diem
    from kiem_vung import gioi_han
    ten = os.path.basename(os.path.abspath(pj))
    video = video or next((p for p in (os.path.join(ROOT, "out", f"{ten}{s}.mp4") for s in ("", ".nhap", ".xem")) if os.path.exists(p)), None)
    if not video:
        sys.exit("Chưa có video dựng (out/<tên>.mp4): dựng xong rồi tạo ảnh bìa.")
    fs = phan_tich(video)
    noi = sum(f["face"] > 0.02 for f in fs) > len(fs) * 0.4
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    from storyboard import canh
    mat = [(a, b) for a, b, loai, _ in canh(tl) if loai == "clip"]  # chỉ chọn lúc đang là người nói (không cảnh trám/thẻ)
    moc = chon_khung([(f["t"], diem(f, noi)[0]) for f in fs if any(a + 0.3 <= f["t"] < b - 0.3 for a, b in mat)])
    try:
        from ban_dung import doc_loi
        ws = doc_loi(pj)[1]
    except SystemExit:
        ws = []
    chu = chu_hook(pj, ws)
    tam = not any(v.get("vai") == "hook" for v in (json.load(open(os.path.join(pj, "BAN-DUNG.json"), encoding="utf8")).get("vai", [])
                                                  if os.path.exists(os.path.join(pj, "BAN-DUNG.json")) else []))
    d = os.path.join(KHO, ten); os.makedirs(d, exist_ok=True)
    nen = []
    from timeline import size
    Wv, Hv = size(tl)
    for k, t in enumerate(moc):
        f = os.path.join(d, f"khung-{k + 1}.jpg")
        if not khung_sach(pj, tl, t, f, Wv, Hv):  # không lấy được từ footage gốc: lấy từ video thành phẩm
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", "-q:v", "2", f], check=True)
        nen.append(f)
    kq, gon = [], True
    for nen_tang, (W, H) in KHO_ANH.items():
        vung = gioi_han({"meta": {"platform": "youtube" if W > H else "tiktok"}})
        ds = [(trang(nen[k % len(nen)], chu, kieu, W, H, vung), os.path.join(d, f"{nen_tang}-{kieu}.png")) for k, kieu in enumerate("ABC")]
        gon &= chup(ds, W, H)
        kq += [p for _, p in ds]
    md = [f"# Ảnh bìa: {ten}", "", f"- Chữ: «{chu}» ({'CHỮ TẠM: chưa có hook trong BAN-DUNG.json, Hào sửa chữ' if tam else 'từ hook đã duyệt'}) · khung nền ở giây {', '.join(f'{t:.1f}' for t in moc)} của `{os.path.basename(video)}`",
          f"- Chữ nằm gọn vùng an toàn: {'đạt' if gon else 'CHƯA (chữ dài quá, rút gọn hook)'}", "", "| Phương án | TikTok 1080×1920 | YouTube 1280×720 |", "|---|---|---|"]
    md += [f"| {kieu} | tiktok-{kieu}.png | youtube-{kieu}.png |" for kieu in "ABC"] + ["", "Hào chọn: …", ""]
    open(os.path.join(d, "ANH-BIA.md"), "w", encoding="utf8").write("\n".join(md))
    open(os.path.join(KHO, "KHO-ANH-BIA.md"), "a", encoding="utf8").write(f"- {time.strftime('%Y-%m-%d')} · {ten} · «{chu}» · {ten}/ANH-BIA.md\n")
    return kq, gon


def _tu_kiem():
    import tempfile
    assert chon_khung([(0.2, 99), (2, 90), (3, 80), (6, 85), (9, 70), (9.8, 100), (10, 10)]) == [2, 6, 9], "điểm cao, cách 3s, bỏ đầu/cuối"
    d = tempfile.mkdtemp()
    nen = os.path.join(d, "n.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=540x960", "-frames:v", "1", nen], check=True)
    from kiem_vung import gioi_han
    for (W, H), pf in (((1080, 1920), "tiktok"), ((1280, 720), "youtube")):
        v = gioi_han({"meta": {"platform": pf}})
        ds = [(trang(nen, "77 tỷ cho một căn biệt thự", k, W, H, v), os.path.join(d, f"{pf}{k}.png")) for k in "ABC"]
        assert chup(ds, W, H), f"chữ hook ngắn phải nằm gọn vùng an toàn {pf}"
        assert "1.080 ha" in trang(nen, "rộng 1.080 ha", "A", W, H, v), "đơn vị viết thường (Hào nhắc lỗi 800 Ha)"
        import cv2
        assert cv2.imread(ds[0][1]).shape[:2] == (H, W)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) in (2, 3):
        kq, gon = tao(os.path.abspath(sys.argv[1]), sys.argv[2] if len(sys.argv) == 3 else None)
        print(f"{len(kq)} ảnh bìa → {os.path.dirname(kq[0])}" + ("" if gon else "  (chữ chưa nằm gọn vùng an toàn: rút gọn hook)"))
    else:
        sys.exit(__doc__)
