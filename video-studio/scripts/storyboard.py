"""Storyboard để Hào duyệt TRƯỚC khi dựng (Hào chốt 17/11): đọc timeline.json, chia video thành từng cảnh nhìn thấy
(cảnh chính, cảnh trám, thẻ chèn), mỗi cảnh một ảnh + giây + lời nói + chữ trên màn hình + chuyển cảnh.
Chạy trong video-studio:  python3 scripts/storyboard.py projects/<tên>
Ra: projects/<tên>/STORYBOARD.md và projects/<tên>/build/storyboard.jpg (ảnh lưới, số cảnh trùng số trong bảng).
Nhanh (vài chục giây): chỉ cắt một khung mỗi cảnh, không dựng video. Duyệt xong mới chạy dung.py --xem (540×960)."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from timeline import layout

TW, TH = 180, 320  # cỡ ảnh mỗi cảnh trong lưới (9:16)


def canh(tl):
    """Danh sách cảnh nhìn thấy theo thời gian: thẻ chèn > cảnh trám > cảnh chính. Mỗi cảnh: (a, b, loại, chỉ số)."""
    L = layout(tl)
    lop = [(s, s + c["dur"], "clip", i) for i, (s, c) in enumerate(zip(L["starts"], tl["clips"]))]
    lop += [(x["start"], x["start"] + x["dur"], "broll", i) for i, x in enumerate(tl.get("broll", []))]
    lop += [(x["start"], x["start"] + x["dur"], "card", i) for i, x in enumerate(tl.get("cards", []))]
    moc = sorted({round(min(max(t, 0), L["total"]), 2) for a, b, *_ in lop for t in (a, b)} | {0, round(L["total"], 2)})
    hang = {"card": 2, "broll": 1, "clip": 0}
    out = []
    for a, b in zip(moc, moc[1:]):
        if b - a < 0.05:
            continue
        m = (a + b) / 2
        tren = max((q for q in lop if q[0] <= m < q[1]), key=lambda q: (hang[q[2]], q[0]), default=None)
        if tren is None:
            continue
        if out and out[-1][2:] == tren[2:]:
            out[-1] = (out[-1][0], b, *tren[2:])
        else:
            out.append((a, b, *tren[2:]))
    return out


def chu_tren_man(tl, a, b):
    """Chữ lớn/khối chữ (không tính chữ theo nhịp nói) và thẻ chèn hiện trong khoảng [a, b)."""
    v = []
    for x in tl.get("texts", []):
        if x.get("kind") != "loi" and x["start"] < b and x["start"] + x["dur"] > a:
            v.append(" · ".join(str(x[k]) for k in ("top", "big", "sub") if x.get(k)) or " / ".join(map(str, x.get("lines", []))))
    for x in tl.get("cards", []):
        if x["start"] < b and x["start"] + x["dur"] > a:
            v.append(f"[thẻ {x.get('kieu', '')}] " + " · ".join(str(q) for q in [x.get("title"), x.get("value"), x.get("centre")] + x.get("items", []) if q))
    return " ‖ ".join(q for q in v if q).replace("|", "/")


def anh(pj, tl, c, out):
    """Một khung đại diện của cảnh (giữa cảnh), cùng khung cắt và chuyển tông HDR như bộ dựng."""
    import cv2, numpy as np
    from mau import khung
    a, b, loai, i = c
    if loai == "card":
        img = np.full((TH, TW, 3), 24, np.uint8)
        x = tl["cards"][i]
        from kho import bo_dau
        for k, s in enumerate(["THE " + x.get("kieu", "").upper(), bo_dau(str(x.get("value") or x.get("centre") or x.get("title", "")))[:14]]):
            cv2.putText(img, s, (10, 150 + 40 * k), cv2.FONT_HERSHEY_SIMPLEX, 0.6 if k == 0 else 0.8, (120, 200, 255), 2, cv2.LINE_AA)
        cv2.imwrite(out, img)
        return
    L = layout(tl)
    s, x = (L["starts"][i], tl["clips"][i]) if loai == "clip" else (tl["broll"][i]["start"], tl["broll"][i])
    from ban_nhe import lay
    raw = lay(os.path.join(pj, "build"), x["file"])  # bản nhẹ 540p: cắt một khung nhanh hơn 4K HDR nhiều
    t = x.get("in", 0) + ((a + b) / 2 - s)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", raw, "-frames:v", "1",
                    "-vf", khung(raw, TW, TH, x.get("focus", 0), x.get("fit")), out], check=True)


def luoi(files, out, cot=6):
    """Ghép ảnh từng cảnh thành lưới, góc trên ghi số cảnh và giây bắt đầu."""
    import cv2, numpy as np
    o = []
    for k, (f, a) in enumerate(files, 1):
        img = cv2.imread(f) if os.path.exists(f) else np.zeros((TH, TW, 3), np.uint8)
        img = cv2.resize(img, (TW, TH))
        cv2.rectangle(img, (0, 0), (TW, 30), (0, 0, 0), -1)
        cv2.putText(img, f"#{k}  {a:.1f}s", (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
        o.append(cv2.copyMakeBorder(img, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=(40, 40, 40)))
    o += [np.zeros_like(o[0])] * (-len(o) % cot)
    cv2.imwrite(out, np.vstack([np.hstack(o[r:r + cot]) for r in range(0, len(o), cot)]), [cv2.IMWRITE_JPEG_QUALITY, 85])


def lap(pj):
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    cs = canh(tl)
    try:
        from ban_dung import doc_loi
        w = doc_loi(pj)[1]
    except SystemExit:
        w = []  # chưa có text từ ghi âm: bảng vẫn có hình và chữ, chưa có cột lời nói
    tdir = os.path.join(pj, "build", "storyboard")
    os.makedirs(tdir, exist_ok=True)
    L = layout(tl)
    tr = {round(s, 2): t.get("type", "cut") for s, t in zip(L["starts"][1:], tl.get("transitions", []))}
    rows, files = [], []
    for k, c in enumerate(cs, 1):
        a, b, loai, i = c
        f = os.path.join(tdir, f"c{k:02d}.jpg")
        anh(pj, tl, c, f)
        files.append((f, a))
        nguon = (f"thẻ {tl['cards'][i].get('kieu', '')}" if loai == "card" else
                 f"{'trám ' if loai == 'broll' else ''}{(tl['broll'] if loai == 'broll' else tl['clips'])[i]['file']}")
        loi = " ".join(x[0] for x in w if a <= x[1] < b)
        rows.append(f"| {k} | {a:.1f}–{b:.1f} ({b - a:.1f}s) | {nguon} | {loi.replace('|', '/')} | {chu_tren_man(tl, a, b)} | {tr.get(round(a, 2), '')} |")
    luoi(files, os.path.join(pj, "build", "storyboard.jpg"))
    from phan_tich_loi import phan_tich, bao_cao
    phan_tich_md = bao_cao(phan_tich(tl, w, pj)) if w else ["- Chưa có text từ ghi âm (chạy loi_nhip.py) nên chưa phân tích được lời nói."]
    from doi_chieu import kiem
    hoi = kiem(pj)[0]
    md = [f"# STORYBOARD: {os.path.basename(pj)}", "",
          f"> Tạo bằng `scripts/storyboard.py` từ `timeline.json`. {len(cs)} cảnh, {L['total']:.1f} giây. Ảnh lưới: `build/storyboard.jpg` (số # trùng bảng).",
          "> Hào duyệt bảng này trước; duyệt xong Claude dựng bản xem 540×960 (`dung.py --xem`), rồi mới dựng bản cuối.", "",
          "| # | Giây | Hình | Lời nói | Chữ trên màn hình | Chuyển cảnh vào |", "|---|---|---|---|---|---|", *rows, "",
          "## Phân tích lời nói và chỗ cắt (dự đoán, chưa sửa gì)",
          "> Nói nhanh/chậm so với nhịp riêng của Hào, lặp từ, nói vấp, chỗ cắt rơi giữa từ, cảnh quá ngắn/dài. Hào chọn mục nào cần sửa, Claude sửa rồi lập lại storyboard.", "",
          *phan_tich_md, "",
          "## Cần Hào trả lời trước khi dựng bản cuối", *([f"- {h}" for h in hoi] or ["- Không có (cổng đối chiếu đạt)."]), ""]
    open(os.path.join(pj, "STORYBOARD.md"), "w", encoding="utf8").write("\n".join(md))
    return len(cs)


def _tu_kiem():
    tl = {"version": 1, "clips": [{"file": "a.mp4", "in": 0, "dur": 10}, {"file": "b.mp4", "in": 2, "dur": 5}],
          "transitions": [{"type": "cut"}], "broll": [{"file": "r.mp4", "in": 0, "start": 2, "dur": 3}],
          "cards": [{"kieu": "so-lieu", "start": 3, "dur": 1, "title": "x", "value": "271 ha"}],
          "texts": [{"kind": "title3d", "start": 0, "dur": 2, "top": "a", "big": "1.080 ha"}, {"kind": "loi", "start": 0, "dur": 1, "words": []}]}
    got = [(a, b, l) for a, b, l, _ in canh(tl)]
    assert got == [(0, 2, "clip"), (2, 3, "broll"), (3, 4, "card"), (4, 5, "broll"), (5, 10, "clip"), (10, 15, "clip")], got
    assert canh(tl)[-1][3] == 1  # cảnh chính thứ hai
    assert chu_tren_man(tl, 0, 2) == "a · 1.080 ha" and "271 ha" in chu_tren_man(tl, 3, 4)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        pj = os.path.abspath(sys.argv[1])
        print(f"Xong: {lap(pj)} cảnh → {os.path.join(pj, 'STORYBOARD.md')} + build/storyboard.jpg")
    else:
        sys.exit("Dùng: python3 scripts/storyboard.py projects/<tên>")
