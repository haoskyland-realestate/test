"""Cổng đối chiếu TRƯỚC KHI DỰNG BẢN CUỐI: chữ và số hiện trên màn hình phải khớp với text từ ghi âm (lời Hào nói) hoặc nguồn số liệu đã duyệt.
KHÔNG đoán ý. Số chưa kiểm chứng được, chỗ còn `[...]`, chỗ lời nói khác kịch bản: báo lại, Claude HỎI Hào rồi mới dựng.
Một số/dữ kiện được coi là đã kiểm chứng khi (a) chính Hào nói trong ghi âm (text nhận dạng giọng trong build/transcripts/), hoặc
(b) có trong NGUON-SO-LIEU.md của dự án với cột "Hào xác nhận" = rồi/có/đã, hoặc (c) Hào đã duyệt riêng trong timeline: meta.da_duyet = ["77 tỷ", ...].
Chạy trong video-studio:  python3 scripts/doi_chieu.py projects/<tên>      (ghi build/doi-chieu.md; mã thoát 2 = cần hỏi Hào)      ·   tự kiểm: --tu-kiem
dung.py gọi hàm kiem() trước bản cuối và dừng nếu còn mục chưa kiểm chứng; sau khi Hào duyệt thì thêm vào meta.da_duyet hoặc chạy dung.py --da-duyet.
shortcut: số được so theo chuỗi chữ số (77, 1m2, 2.4); tên riêng và pháp lý chưa kiểm tự động, nên Claude vẫn phải đọc báo cáo và hỏi khi nghi ngờ."""
import glob, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CHO = re.compile(r"\[\s*\.{2,}\s*\]|\[\s*…\s*\]")


def chuan(s):
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    return re.sub(r"[^a-z0-9.,%]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()


def toks(s):
    return [t.strip(".,") for t in chuan(s).split() if t.strip(".,")]


def so_trong(s):
    return [t for t in toks(s) if re.search(r"\d", t)]


def chu_hien(tl):
    """(vị trí, chuỗi chữ) của mọi chữ hiện trên màn hình, trừ chữ theo nhịp nói (lấy thẳng từ ghi âm)."""
    out = []
    for i, x in enumerate(tl.get("texts", []), 1):
        if x.get("kind") == "loi":
            continue
        v = [str(x.get(k, "")) for k in ("top", "big", "sub", "label", "prefix", "suffix", "title", "text", "tag", "a_label", "a_value", "b_label", "b_value", "note", "by", "num")]
        v += [str(q) for q in x.get("lines", [])] + [str(q) for q in x.get("items", [])] + [str(q) for q in (x.get("o") or {}).values()]
        if x.get("kind") == "stat":
            v.append(str(x.get("value", "")))
        out.append((f"chữ {i} ({x.get('kind', 'line')}, {x['start']}s)", " ".join(q for q in v if q)))
    for j, x in enumerate(tl.get("cards", []), 1):
        v = [str(x.get(k, "")) for k in ("step", "title", "value", "label", "centre")] + [str(q) for q in x.get("items", [])]
        out.append((f"cảnh chèn {j} ({x.get('kieu', 'danh-sach')}, {x['start']}s)", " ".join(q for q in v if q)))
    return out


def loi_noi(pj):
    """Tập từ đã nói trong mọi ghi âm của dự án (text nhận dạng giọng đã lưu), None nếu chưa nhận dạng."""
    fs = glob.glob(os.path.join(pj, "build", "transcripts", "*.json"))
    if not fs:
        return None
    ws = set()
    for f in fs:
        for w in json.load(open(f, encoding="utf8")):
            ws.update(toks(w[0]))
    return ws


def nguon_duyet(pj):
    """Số trong NGUON-SO-LIEU.md ở các dòng Hào đã xác nhận."""
    p = os.path.join(pj, "NGUON-SO-LIEU.md")
    out = set()
    if os.path.exists(p):
        for l in open(p, encoding="utf8"):
            c = [q.strip() for q in l.strip().strip("|").split("|")]
            if len(c) >= 5 and re.match(r"(rồi|có|đã|ok)", c[4].lower()):
                out.update(so_trong(" ".join(c[:2])))
    return out


def doc_kich_ban(pj):
    p = os.path.join(pj, "KICH-BAN.md")
    rows = []
    if os.path.exists(p):
        for l in open(p, encoding="utf8"):
            c = [q.strip() for q in l.strip().strip("|").split("|")]
            if len(c) >= 4 and re.match(r"^\d+$", c[0]):
                rows.append((c[0], c[2], c[3]))
    return rows


def kiem(pj):
    """Trả (danh sách mục cần hỏi Hào, ghi chú). Rỗng = đủ điều kiện dựng."""
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    hoi, ghi = [], []
    noi = loi_noi(pj)
    duyet = {t for d in tl.get("meta", {}).get("da_duyet", []) for t in so_trong(d)} | nguon_duyet(pj)
    if noi is None:
        hoi.append("CHƯA CÓ text từ ghi âm (build/transcripts/): chạy nhận dạng giọng (phu_de.py hoặc master cut) để đối chiếu.")
        noi = set()
    for vt, s in chu_hien(tl):
        if CHO.search(s):
            hoi.append(f"{vt}: còn chỗ trống [...] — Hào điền hoặc bỏ")
        for n in so_trong(s):
            if n in noi or n in duyet:
                ghi.append(f"{vt}: số {n} khớp " + ("lời Hào nói" if n in noi else "nguồn đã duyệt"))
            else:
                hoi.append(f"{vt}: số «{n}» KHÔNG có trong ghi âm và chưa có nguồn đã duyệt — Hào xác nhận nguồn/ngày hoặc bỏ")
    for j, x in enumerate(tl.get("cards", []), 1):
        if x.get("kieu") == "so-lieu" and not str(x.get("nguon", "")).strip():
            hoi.append(f"cảnh chèn {j}: thẻ số liệu thiếu 'nguon' (tên tài liệu + ngày)")
    for stt, loi_doc, chu in doc_kich_ban(pj):  # lời đọc trong kịch bản so với ghi âm
        if "[" in loi_doc[:3] or not loi_doc.strip("() ") or loi_doc.startswith("("):
            continue
        for n in so_trong(loi_doc):
            if noi and n not in noi:
                hoi.append(f"kịch bản dòng {stt}: số «{n}» có trong kịch bản nhưng Hào KHÔNG nói trong ghi âm — kịch bản đổi hay nói sai?")
        thieu = [t for t in toks(loi_doc) if len(t) > 3 and noi and t not in noi]
        if noi and len(thieu) > max(2, len(toks(loi_doc)) // 3):
            ghi.append(f"kịch bản dòng {stt}: lời nói khác kịch bản ({len(thieu)} từ không thấy trong ghi âm: {', '.join(thieu[:6])}…) — theo ghi âm")
    if noi:
        for stt, loi_doc, chu in doc_kich_ban(os.path.abspath(pj)):
            for n in so_trong(chu):
                if n not in noi and n not in duyet:
                    hoi.append(f"kịch bản dòng {stt}: số «{n}» ở cột chữ trên màn hình không có trong ghi âm/nguồn đã duyệt")
    return list(dict.fromkeys(hoi)), ghi


def viet(pj):
    hoi, ghi = kiem(pj)
    md = ["# Đối chiếu ghi âm, kịch bản, chữ trên màn hình", "", "## Cần hỏi Hào trước khi dựng" if hoi else "## Không có mục nào cần hỏi: đủ điều kiện dựng"]
    md += [f"- {h}" for h in hoi] + ["", "## Đã khớp / ghi chú"] + [f"- {g}" for g in ghi]
    os.makedirs(os.path.join(pj, "build"), exist_ok=True)
    open(os.path.join(pj, "build", "doi-chieu.md"), "w", encoding="utf8").write("\n".join(md) + "\n")
    return hoi, ghi


def _tu_kiem():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(f"{t}/build/transcripts")
        json.dump([["khoảng", 0, 1], ["77", 1, 2], ["tỷ", 2, 3]], open(f"{t}/build/transcripts/a.json", "w", encoding="utf8"))
        tl = {"version": 1, "meta": {}, "audio": {}, "clips": [{"file": "a.mp4", "in": 0, "dur": 5}],
              "texts": [{"kind": "title3d", "start": 0, "dur": 2, "big": "77 TỶ", "sub": "diện tích 240m2"}], "cards": []}
        json.dump(tl, open(f"{t}/timeline.json", "w"))
        hoi, ghi = kiem(t)
        assert len(hoi) == 1 and "240m2" in hoi[0] and any("77" in g for g in ghi), (hoi, ghi)   # 77 có trong ghi âm, 240m2 thì không
        tl["meta"]["da_duyet"] = ["240m2 theo bảng giá chủ đầu tư 11/2026"]
        json.dump(tl, open(f"{t}/timeline.json", "w"))
        assert kiem(t)[0] == [], kiem(t)                                                         # Hào đã duyệt riêng
        tl["texts"][0]["sub"] = "giá [...]"
        json.dump(tl, open(f"{t}/timeline.json", "w"))
        assert any("[...]" in h for h in kiem(t)[0])
        open(f"{t}/NGUON-SO-LIEU.md", "w", encoding="utf8").write("| # | dữ kiện | nguồn | ngày | Hào xác nhận | ghi chú |\n|---|---|---|---|---|---|\n| 1 | 77 tỷ | bảng giá | 11/2026 | rồi | |\n")
        assert "77" in nguon_duyet(t)
        os.remove(f"{t}/build/transcripts/a.json")
        assert any("CHƯA CÓ text" in h for h in kiem(t)[0])
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        h, g = viet(os.path.abspath(sys.argv[1]))
        print(open(os.path.join(sys.argv[1], "build", "doi-chieu.md"), encoding="utf8").read())
        sys.exit(2 if h else 0)
    else:
        sys.exit(__doc__)
