"""Kho tài nguyên edit của Hào (âm, overlay, nền, LUT màu, font, template…) nằm trong một thư mục trên PC
(ví dụ thư mục Google Drive đồng bộ, sau khi giải nén các file .rar). Module này:
- quét thư mục → chỉ mục (loại, thẻ từ tên thư mục/tên file, dung lượng); chỉ đọc tên file, không mở file (quét 30 GB vẫn nhanh);
- đổi tên dạng "kho:<đường dẫn trong kho>" (dùng trong timeline.json) thành đường dẫn thật, chặn đường dẫn thoát ra ngoài kho.
Đường dẫn kho lưu ở video-studio/kho/cau-hinh.json, chỉ mục ở video-studio/kho/chi-muc.json (riêng từng máy, không lên GitHub).
Chạy:  python3 scripts/kho.py <thư mục kho>     (quét và lưu)   ·   python3 scripts/kho.py --tu-kiem
       python3 scripts/kho.py --chon "film burn" [hao-sky-land] [hoc-mon]   (lấy theo nghĩa, chỉ gợi ý)"""
import json, os, re, subprocess, sys, time, unicodedata

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
GOI_Y = [("chu-thich", ("chu thich", "radar", "label", "callout", "location pin", "map pin")),
         ("overlay", ("overlay", "light leak", "leak", "dust", "bui", "khoi", "smoke", "film", "grain", "flare", "bokeh", "lens", "particle", "paper", "giay", "glitch")),
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


# Tầng của kho (THU-VIEN-LUU-TRU.md): thư mục cấp 1 quyết định file thuộc ai. Lấy theo thứ tự dự án → thương hiệu → chung.
TANG = [("thuong-hieu", "thuong hieu"), ("du-an", "du an"), ("cho", "cho phan loai"), ("luu-tru", "luu tru")]


def tang(rel):
    """'10_THUONG-HIEU/hao-sky-land/logo/x.png' → ('thuong-hieu', 'hao-sky-land'); thư mục khác → ('chung', '')."""
    parts = rel.replace("\\", "/").split("/")
    dau = re.sub(r"[^a-z]+", " ", bo_dau(parts[0])).strip()
    for k, w in TANG:
        if w in dau:
            return k, (bo_dau(parts[1]) if k in ("thuong-hieu", "du-an") and len(parts) > 2 else "")
    return "chung", ""


def _cha(d, goc):
    """Thư mục d và các thư mục cha tới gốc kho (tìm GIAY-PHEP.md gần nhất)."""
    while True:
        yield d
        if os.path.normcase(d) == os.path.normcase(goc) or os.path.dirname(d) == d:
            return
        d = os.path.dirname(d)


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
            lop, chu = tang(rel)
            gp = next((os.path.relpath(os.path.join(x, "GIAY-PHEP.md"), goc).replace("\\", "/") for x in _cha(d, goc)
                       if os.path.isfile(os.path.join(x, "GIAY-PHEP.md"))), "")
            out.append({"p": rel, "loai": loai, "dung": dung, "kb": round(size / 1024), "the": the(rel), "lop": lop, "chu": chu, "gp": gp})
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


KHONG_CHEN = ("nen", "plugin", "mau-pm", "font", "khac")  # không tự đưa vào video được


def chon(cm, y, thuong_hieu="", du_an="", loai="", n=5):
    """Lấy theo nghĩa: 'film burn', 'whoosh nhanh', 'chu thich truong hoc' → các file hợp nhất, kèm lý do.
    Điểm = số từ khớp (thẻ trùng hẳn tính hơn khớp một phần); cùng điểm thì tài nguyên của dự án > thương hiệu > chung.
    Bỏ qua: thương hiệu/dự án khác, thư mục chờ phân loại, lưu trữ, file app không chèn được. Không tự chèn: Hào duyệt."""
    ws = [w for w in re.findall(r"[a-z0-9]+", bo_dau(y)) if len(w) > 1]
    th, da = bo_dau(thuong_hieu), bo_dau(du_an)
    kq = []
    for t in cm["tep"]:
        lop, chu = t.get("lop", "chung"), t.get("chu", "")
        if lop in ("cho", "luu-tru") or (lop == "thuong-hieu" and chu != th) or (lop == "du-an" and chu != da):
            continue
        if (loai and loai not in (t["loai"], t["dung"])) or (not loai and t["loai"] in KHONG_CHEN):
            continue
        text, tags = bo_dau(t["p"]), set(t["the"])
        khop = [w for w in ws if w in text]
        if not ws or len(khop) * 2 < len(ws):  # cần khớp ít nhất nửa số từ
            continue
        diem = sum(2 if w in tags else 1 for w in khop) + {"du-an": 0.5, "thuong-hieu": 0.3}.get(lop, 0)
        kq.append((-diem, t["p"], dict(t, diem=round(diem, 1), vi_sao=f"khớp {', '.join(khop)}; tầng {lop}{' ' + chu if chu else ''}"
                                                                     + ("" if t.get("gp") else "; chưa có GIAY-PHEP.md"))))
    return [x[2] for x in sorted(kq)[:n]]


def neo(p):
    """Đo vùng có hình (kênh trong suốt) của file overlay: chân hình (giữa cạnh dưới) và bề rộng hình, theo tỉ lệ khung file.
    Dùng để đặt chú thích/ghim đúng chỗ bấm và tự chọn cỡ. Lưu đệm theo đường dẫn + thời gian sửa. None nếu file không có kênh trong suốt."""
    cache = os.path.join(DIR, "neo.json")
    db = json.load(open(cache, encoding="utf8")) if os.path.exists(cache) else {}
    key = f"{p}|{os.path.getmtime(p)}"
    if key not in db:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,pix_fmt", "-of", "csv=p=0", p],
                           capture_output=True, text=True, timeout=60).stdout.strip().split(",")
        db[key] = None
        if len(r) >= 3 and re.match(r"(argb|rgba|bgra|abgr|yuva|gbrap|ya8|ya16|pal8)", r[2]):
            w0, h0 = int(r[0]), int(r[1])
            out = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-ss", "1", "-i", p, "-frames:v", "3", "-vf",
                                  "alphaextract,cropdetect=limit=24:round=2:reset=0", "-f", "null", "-"], capture_output=True, text=True, timeout=120).stderr
            m = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", out)
            if m:
                w, h, x, y = map(int, m[-1])
                db[key] = {"ax": round((x + w / 2) / w0, 3), "ay": round((y + h) / h0, 3), "bw": round(w / w0, 3)}
        os.makedirs(DIR, exist_ok=True)
        json.dump(db, open(cache, "w", encoding="utf8"), ensure_ascii=False)
    return db[key]


def dat_cho(n, W=1080, cao=0.22):
    """Thông số đặt nhỏ ở một chỗ: chân hình tại giữa khung (0,5; 0,5: trên dòng phụ đề), hình rộng khoảng `cao` bề rộng khung."""
    if not n:
        return {"x": 0.5, "y": 0.5, "size": 0.55}
    return {"x": 0.5, "y": 0.5, "size": round(min(3, max(0.2, cao / max(n["bw"], 0.02))), 2), "ax": n["ax"], "ay": n["ay"]}


def ten_chu_thich(rel):
    """'Chú Thích BĐS/Bản sao của truong-hoc.mov' → 'truong hoc' (tên tiện ích để dò trong lời nói)."""
    t = bo_dau(os.path.splitext(rel.split("/")[-1])[0])
    t = re.sub(r"^(ban sao cua|copy of)\s+", "", t)
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def chu_thich(tl, cm, dur=3.0):
    """Gắn biểu tượng chú thích (thư mục chú thích trong kho) đúng lúc lời nói nhắc tới tiện ích đó.
    Dò trong phụ đề giống cách đặt chữ theo kịch bản (bỏ dấu, cho lệch 1 từ). Mục tự gắn có "auto": "chu-thich"; chạy lại thì thay."""
    from kich_ban import dong_thoi_gian, tim
    from timeline import layout
    tl = json.loads(json.dumps(tl))
    total = layout(tl)["total"]
    stream = dong_thoi_gian(tl.get("subtitles", []))
    tl["overlays"] = [o for o in tl.get("overlays", []) if o.get("auto") != "chu-thich"]
    da = []
    for t in cm["tep"]:
        if t["dung"] != "chu-thich" or t["loai"] != "video":
            continue
        q = ten_chu_thich(t["p"]).split()
        if not q or len(q) > 4 or q[0] in ("label", "rada", "radar", "vi", "thanh"):  # nhãn chung, radar, vị trí dự án: Hào tự đặt
            continue
        cur = 0
        while True:
            sc, idx = tim(stream, q, cur)
            if idx is None or sc < 0.99:
                break
            st = round(max(0.0, stream[idx][2] - 0.2), 2)
            if st < total - 0.5 and not any(abs(st - s) < 1.0 for s, _ in da):
                da.append((st, t["p"]))
            cur = idx + 1
    for st, p in sorted(da):
        that = duong_dan("kho:" + p, cm["goc"])
        try:
            cho = dat_cho(neo(that))
        except (OSError, subprocess.SubprocessError, ValueError):
            cho = dat_cho(None)
        tl["overlays"].append({"start": st, "dur": round(min(dur, total - st), 2), "file": "kho:" + p, "in": 0, "blend": "alpha",
                               "opacity": 1, **cho, "auto": "chu-thich"})
    return tl, [(st, ten_chu_thich(p)) for st, p in sorted(da)]


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
        # chú thích theo lời nói
        for rel in ("Chú Thích BĐS/Bản sao của truong-hoc.mov", "Chú Thích BĐS/Bản sao của sieu thi.mov", "Chú Thích BĐS/Bản sao của Label du an 2.mov",
                    "Bộ Radar BĐS/Bản sao của rada1.mov"):
            p = os.path.join(g, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "wb").write(b"x")
        cm = quet(g)
        assert {t["p"]: t["dung"] for t in cm["tep"]}["Bộ Radar BĐS/Bản sao của rada1.mov"] == "chu-thich"
        assert ten_chu_thich("Chú Thích BĐS/Bản sao của truong-hoc.mov") == "truong hoc"
        tl = {"version": 1, "clips": [{"file": "a.mp4", "in": 0, "dur": 20}], "transitions": [],
              "subtitles": [{"start": 2, "dur": 2, "text": "gần trường học quốc tế"}, {"start": 9, "dur": 2, "text": "đi bộ ra *siêu thị* 5 phút"},
                            {"start": 14, "dur": 2, "text": "lại thêm một trường học nữa"}],
              "overlays": [{"start": 1, "dur": 1, "file": "kho:x.mov", "blend": "screen"}]}
        out, bao = chu_thich(tl, cm)
        assert [b[1] for b in bao] == ["truong hoc", "sieu thi", "truong hoc"], bao
        assert len(out["overlays"]) == 4 and out["overlays"][0]["file"] == "kho:x.mov"
        again, _ = chu_thich(out, cm)
        assert len(again["overlays"]) == 4
    # lấy theo nghĩa, theo tầng
    with tempfile.TemporaryDirectory() as g:
        for rel in ("00_CHUNG/overlay/film-burn/film-burn_cam_01.mp4", "00_CHUNG/am-thanh/whoosh/whoosh_nhanh_01.wav", "00_CHUNG/am-thanh/GIAY-PHEP.md",
                    "10_THUONG-HIEU/hao-sky-land/am-thanh/whoosh_nhanh_hsl.wav", "10_THUONG-HIEU/khac/am-thanh/whoosh_nhanh_khac.wav",
                    "20_DU-AN/hoc-mon/logo/logo-cdt.png", "90_CHO-PHAN-LOAI/whoosh nhanh moi.wav", "99_LUU-TRU/goi/Overlays.rar"):
            p = os.path.join(g, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "wb").write(b"x")
        cm = quet(g)
        by = {t["p"]: t for t in cm["tep"]}
        assert tang("10_THUONG-HIEU/hao-sky-land/x.png") == ("thuong-hieu", "hao-sky-land") and tang("00_CHUNG/x.wav") == ("chung", "")
        assert by["00_CHUNG/am-thanh/whoosh/whoosh_nhanh_01.wav"]["gp"] == "00_CHUNG/am-thanh/GIAY-PHEP.md"
        assert by["00_CHUNG/overlay/film-burn/film-burn_cam_01.mp4"]["gp"] == ""
        r = [x["p"] for x in chon(cm, "whoosh nhanh", thuong_hieu="Hào Sky Land".replace(" ", "-"))]
        assert r == ["10_THUONG-HIEU/hao-sky-land/am-thanh/whoosh_nhanh_hsl.wav", "00_CHUNG/am-thanh/whoosh/whoosh_nhanh_01.wav"], r
        assert [x["p"] for x in chon(cm, "whoosh nhanh")] == ["00_CHUNG/am-thanh/whoosh/whoosh_nhanh_01.wav"]
        assert chon(cm, "film burn")[0]["p"].endswith("film-burn_cam_01.mp4") and chon(cm, "logo") == []
        assert chon(cm, "logo", du_an="hoc-mon")[0]["p"] == "20_DU-AN/hoc-mon/logo/logo-cdt.png"
        assert chon(cm, "overlays") == []  # file nén trong lưu trữ không bao giờ được chọn
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    if sys.argv[1:2] == ["--chon"] and len(sys.argv) >= 3:  # python3 scripts/kho.py --chon "film burn" [thuong-hieu] [du-an]
        for x in chon(doc(), sys.argv[2], *sys.argv[3:5]):
            print(f"kho:{x['p']}   ({x['vi_sao']})")
        sys.exit()
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cm = luu(sys.argv[1])
    dem = {}
    for t in cm["tep"]:
        dem[t["loai"]] = dem.get(t["loai"], 0) + 1
    print(f"Đã quét {len(cm['tep'])} file trong {cm['goc']}:")
    for k, n in sorted(dem.items(), key=lambda x: -x[1]):
        print(f"  {LOAI.get(k, ('', 'Khác'))[1]}: {n}")
