"""Kho tài nguyên edit của Hào (âm, overlay, nền, LUT màu, font, template…) nằm trong một thư mục trên PC
(ví dụ thư mục Google Drive đồng bộ, sau khi giải nén các file .rar). Module này:
- quét thư mục → chỉ mục (loại, thẻ từ tên thư mục/tên file, dung lượng); chỉ đọc tên file, không mở file (quét 30 GB vẫn nhanh);
- đổi tên dạng "kho:<đường dẫn trong kho>" (dùng trong timeline.json) thành đường dẫn thật, chặn đường dẫn thoát ra ngoài kho.
Đường dẫn kho lưu ở video-studio/kho/cau-hinh.json, chỉ mục ở video-studio/kho/chi-muc.json (riêng từng máy, không lên GitHub).
Chạy:  python3 scripts/kho.py <thư mục kho>     (quét và lưu)   ·   python3 scripts/kho.py --tu-kiem"""
import json, os, re, sys, time, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIR = os.path.join(ROOT, "kho")
CAU_HINH, CHI_MUC = os.path.join(DIR, "cau-hinh.json"), os.path.join(DIR, "chi-muc.json")

# loại: (đuôi file, tên tiếng Việt, app dùng được không)
LOAI = {
    "am-thanh": ((".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".aif", ".aiff"), "Âm thanh", True),
    "video": ((".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"), "Video / overlay", True),
    "anh": ((".png", ".jpg", ".jpeg", ".webp", ".gif"), "Ảnh / nền", True),
    "lut": ((".cube",), "LUT màu", True),
    "font": ((".ttf", ".otf"), "Font chữ", False),
    "mau-pm": ((".mogrt", ".aep", ".aet", ".prproj", ".prfpset", ".ffx", ".drfx", ".setting", ".psd", ".ai", ".abr", ".atn", ".json"),
               "Template / preset phần mềm khác (tham khảo)", False),
    "plugin": ((".aex", ".plugin", ".8bf", ".exe", ".msi", ".pkg", ".dmg", ".zxp"), "Plugin / bộ cài (tham khảo)", False),
    "nen": ((".rar", ".zip", ".7z"), "File nén: cần giải nén", False),
}
DUOI = {e: k for k, (es, _, _) in LOAI.items() for e in es}
# Từ trong tên → nhóm dùng (để gợi ý cách dùng; tên thư mục kho thường đã ghi rõ)
GOI_Y = [("overlay", ("overlay", "light leak", "leak", "dust", "bui", "khoi", "smoke", "film", "grain", "flare", "bokeh", "lens", "particle", "paper", "giay", "glitch")),
         ("chuyen-canh", ("transition", "chuyen canh", "chuyen")), ("nen", ("background", "nen", "bg", "backdrop")),
         ("chu", ("title", "text", "typography", "chu", "tag", "lower third", "callout")), ("sfx", ("sfx", "sound", "effect", "whoosh", "hieu ung"))]


def bo_dau(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def the(rel):
    """Thẻ tìm kiếm từ đường dẫn: từng thư mục + các từ trong tên file, không dấu, chữ thường."""
    parts = rel.replace("\\", "/").split("/")
    words = re.findall(r"[a-z0-9]+", bo_dau(" ".join(parts[:-1] + [os.path.splitext(parts[-1])[0]])))
    return sorted({w for w in words if len(w) > 1 and not w.isdigit()})


def quet(goc):
    goc = os.path.abspath(goc)
    if not os.path.isdir(goc):
        raise ValueError("Không có thư mục " + goc)
    out = []
    for d, dirs, files in os.walk(goc):
        dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x != "__MACOSX")
        for f in sorted(files):
            if f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            p = os.path.join(d, f)
            rel = os.path.relpath(p, goc).replace("\\", "/")
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            loai = DUOI.get(ext, "khac")
            text = bo_dau(rel)
            dung = next((g for g, ks in GOI_Y if any(k in text for k in ks)), "")
            out.append({"p": rel, "loai": loai, "dung": dung, "kb": round(size / 1024), "the": the(rel)})
    return {"goc": goc, "luc": time.strftime("%Y-%m-%d %H:%M"), "tep": out}


def luu(goc):
    os.makedirs(DIR, exist_ok=True)
    cm = quet(goc)
    json.dump({"goc": cm["goc"]}, open(CAU_HINH, "w", encoding="utf8"), ensure_ascii=False)
    json.dump(cm, open(CHI_MUC, "w", encoding="utf8"), ensure_ascii=False)
    return cm


def doc():
    return json.load(open(CHI_MUC, encoding="utf8")) if os.path.exists(CHI_MUC) else {"goc": "", "tep": []}


def goc_kho():
    return json.load(open(CAU_HINH, encoding="utf8")).get("goc", "") if os.path.exists(CAU_HINH) else ""


def duong_dan(ten, goc=None):
    """'kho:overlay/la sang 01.mov' → đường dẫn thật; None nếu không phải tên kho hoặc thoát ra ngoài kho."""
    if not isinstance(ten, str) or not ten.startswith("kho:"):
        return None
    goc = os.path.abspath(goc or goc_kho())
    if not goc or not os.path.isdir(goc):
        return None
    p = os.path.abspath(os.path.join(goc, ten[4:]))
    return p if os.path.commonpath([p, goc]) == goc else None


def tim(cm, q="", loai="", trang=0, moi_trang=60):
    """Tìm trong chỉ mục: mọi từ của q (không dấu) phải có trong đường dẫn."""
    ws = bo_dau(q).split()
    kq = [t for t in cm["tep"] if (not loai or t["loai"] == loai or t["dung"] == loai) and all(w in bo_dau(t["p"]) for w in ws)]
    return {"tong": len(kq), "tep": kq[trang * moi_trang:(trang + 1) * moi_trang]}


def _tu_kiem():
    import tempfile
    with tempfile.TemporaryDirectory() as g:
        for rel in ("04_SOUND_EFFECTS_SFX/Whoosh/Whoosh Fast 01.wav", "Overlays/Light Leaks/Light Leak 03.mov", "Nền/bg xanh.png",
                    "02_COLOR_PALETTES_AND_LUTS/Cinematic Warm.cube", "Fonts/SVN-Gilroy Bold.otf", "Titles/Lower Third.mogrt",
                    "Overlays.rar", ".DS_Store", "__MACOSX/x.wav"):
            p = os.path.join(g, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "wb").write(b"x" * 2048)
        cm = quet(g)
        by = {t["p"]: t for t in cm["tep"]}
        assert len(cm["tep"]) == 7, list(by)  # bỏ file ẩn và __MACOSX
        assert by["Overlays/Light Leaks/Light Leak 03.mov"]["loai"] == "video" and by["Overlays/Light Leaks/Light Leak 03.mov"]["dung"] == "overlay"
        assert by["04_SOUND_EFFECTS_SFX/Whoosh/Whoosh Fast 01.wav"]["loai"] == "am-thanh"
        assert by["Nền/bg xanh.png"]["dung"] == "nen" and "nen" in by["Nền/bg xanh.png"]["the"]
        assert by["02_COLOR_PALETTES_AND_LUTS/Cinematic Warm.cube"]["loai"] == "lut" and by["Overlays.rar"]["loai"] == "nen"
        assert tim(cm, "light leak")["tong"] == 1 and tim(cm, "", "am-thanh")["tong"] == 1 and tim(cm, "nen")["tong"] >= 1
        assert duong_dan("kho:Nền/bg xanh.png", g) == os.path.join(g, "Nền", "bg xanh.png")
        assert duong_dan("kho:../../etc/passwd", g) is None and duong_dan("whoosh_zoom_01", g) is None
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cm = luu(sys.argv[1])
    dem = {}
    for t in cm["tep"]:
        dem[t["loai"]] = dem.get(t["loai"], 0) + 1
    print(f"Đã quét {len(cm['tep'])} file trong {cm['goc']}:")
    for k, n in sorted(dem.items(), key=lambda x: -x[1]):
        print(f"  {LOAI.get(k, ('', 'Khác'))[1]}: {n}")
