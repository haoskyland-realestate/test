"""Phân tích lời nói và chỗ cắt cảnh TRƯỚC khi dựng (Hào yêu cầu 18/11): dự đoán chỗ nói nhanh/chậm, lặp từ, nói vấp
(tiếng đệm, ngập ngừng giữa câu), cắt cảnh rơi giữa từ, cảnh quá ngắn/quá dài. Chỉ đọc, không sửa timeline: Claude đề xuất, Hào duyệt rồi mới cắt.
Chạy trong video-studio:  python3 scripts/phan_tich_loi.py projects/<tên>   → in báo cáo; storyboard.py tự gắn kết quả vào STORYBOARD.md.
Cần text từ ghi âm (loi_nhip.py hoặc phu_de.py đã chạy). Thời gian theo video đã dựng (cùng mốc với LOI-NOI.md)."""
import json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DEM = {"ờ", "ừ", "ừm", "ơ", "à", "hmm", "ừa", "ờm", "ê"}  # tiếng đệm khi đứng riêng
NGAT = 0.6   # lặng giữa câu (từ trước không có dấu câu) dài hơn thế là ngập ngừng
CAU = 0.7    # lặng dài hơn thế coi như hết câu


def chuan(w):
    return re.sub(r"[^\w%]", "", w.lower())


def cau(ws):
    """Chia lời thành câu: hết câu ở dấu . ? ! hoặc lặng > CAU giây. Trả [(i đầu, i cuối)]."""
    out, a = [], 0
    for i, w in enumerate(ws):
        het = re.search(r"[.?!]$", w[0]) or (i + 1 < len(ws) and ws[i + 1][1] - w[2] > CAU) or i == len(ws) - 1
        if het:
            out.append((a, i)); a = i + 1
    return out


def toc_do(ws):
    """Mỗi câu: (a, b, âm tiết/giây, nhãn nhanh/chậm/""). Ngưỡng so với nhịp riêng của người nói (trung vị cả video)."""
    cs = [(a, b, (b - a + 1) / max(ws[b][2] - ws[a][1], 0.2)) for a, b in cau(ws) if b - a >= 3]  # câu ≥ 4 từ mới đủ tin cậy
    if not cs:
        return [], 0
    tv = statistics.median(v for *_, v in cs)
    return [(a, b, v, "nhanh" if v > 1.3 * tv else "chậm" if v < 0.7 * tv else "") for a, b, v in cs], tv


def lap(ws, max_n=8, cach=2):
    """Lặp từ/cụm từ: cùng cụm n từ (n lớn nhất trước) nói lại ngay sau đó; cụm ≥ 3 từ cho phép cách ≤ `cach` từ, cụm ngắn phải liền nhau
    (để "2 phân khu chính, phân khu thấp tầng" không bị coi là lặp). Trả [(i, j, n)]: cụm đầu ở i, lần nói lại ở j."""
    c = [chuan(w[0]) for w in ws]
    out, da = [], set()
    for n in range(max_n, 0, -1):
        for i in range(len(c) - n):
            if i in da or not all(c[i:i + n]):
                continue
            for j in range(i + n, min(i + n + (cach if n >= 3 else 0), len(c) - n) + 1):
                if c[i:i + n] == c[j:j + n] and not (n == 1 and j != i + 1):
                    out.append((i, j, n)); da.update(range(i, j + n)); break
    return sorted(out)


def vap(ws):
    """Nói vấp: tiếng đệm đứng riêng, hoặc lặng > NGAT giây giữa câu (từ trước không có dấu câu). Trả [(i, loại)]."""
    out = [(i, "tiếng đệm") for i, w in enumerate(ws) if chuan(w[0]) in DEM]
    out += [(i + 1, f"ngập ngừng {ws[i + 1][1] - w[2]:.1f}s") for i, w in enumerate(ws[:-1])
            if not re.search(r"[.,?!:;]$", w[0]) and NGAT < ws[i + 1][1] - w[2] <= 2.5]
    return sorted(out)


def cat_canh(cs, ws, cat_tieng=()):
    """Chỗ cắt rơi giữa một từ và cảnh quá ngắn (< 1s, như chớp) hoặc quá dài (> 7s, người xem dễ lướt).
    cat_tieng: mốc cắt cả tiếng (đổi đoạn chính) — cắt giữa từ ở đây nghe bị mất chữ; còn lại chỉ đổi hình (cảnh trám, thẻ), nhẹ hơn."""
    out = []
    for k, (a, b, *_) in enumerate(cs, 1):
        if k > 1 and (w := next((w for w in ws if w[1] + 0.05 < a < w[2] - 0.05), None)):
            out.append((a, f"cảnh #{k}: {'CẮT TIẾNG' if any(abs(a - t) < 0.02 for t in cat_tieng) else 'đổi hình'} giữa từ «{w[0]}»"))
        if b - a < 1:
            out.append((a, f"cảnh #{k} chỉ {b - a:.1f}s (như chớp)"))
        elif b - a > 7:
            out.append((a, f"cảnh #{k} dài {b - a:.1f}s, nên chèn cảnh trám/zoom/chữ"))
    return out


def phan_tich(tl, ws):
    """Danh sách ghi chú [(giây, loại, nội dung, đề xuất)] theo thời gian."""
    from storyboard import canh
    g = []
    td, tv = toc_do(ws)
    for a, b, v, nhan in td:
        if nhan:
            g.append((ws[a][1], f"nói {nhan}", f"«{' '.join(w[0] for w in ws[a:b + 1])}» {v:.1f} âm tiết/giây (bình thường {tv:.1f})",
                      "chữ hiện thưa lại, giữ lâu hơn" if nhan == "nhanh" else "cắt bớt lặng/zoom nhẹ để giữ nhịp"))
    for i, j, n in lap(ws):
        g.append((ws[i][1], "lặp từ", f"«{' '.join(w[0] for w in ws[i:i + n])}» nói 2 lần ({ws[i][1]:.1f}s và {ws[j][1]:.1f}s)",
                  f"cắt lần đầu: {ws[i][1]:.2f}–{ws[j][1]:.2f}s"))
    for i, loai in vap(ws):
        g.append((ws[i][1], "nói vấp", f"{loai} trước «{ws[i][0]}»", "cắt tiếng đệm" if loai == "tiếng đệm" else "cắt bớt khoảng lặng"))
    from timeline import layout
    for t, nd in cat_canh(canh(tl), ws, layout(tl)["starts"][1:]):
        g.append((t, "cắt cảnh", nd, "dời chỗ cắt về khoảng lặng gần nhất" if "giữa từ" in nd else "gộp/kéo dài cảnh" if "chớp" in nd else ""))
    return sorted(g)


def bao_cao(g):
    if not g:
        return ["- Không thấy chỗ nói nhanh/chậm, lặp từ, nói vấp hay cắt cảnh bất thường."]
    return ["| Giây | Loại | Chi tiết | Đề xuất |", "|---|---|---|---|"] + [f"| {t:.1f} | {l} | {nd} | {dx} |".replace("||", "| |") for t, l, nd, dx in g]


def _tu_kiem():
    w = lambda s, t0, d=0.25: [[x, round(t0 + k * d, 2), round(t0 + (k + 1) * d, 2)] for k, x in enumerate(s.split())]
    ws = w("biệt thự đơn lập, song lập, biệt thự đơn lập, song lập, mang phong cách nghỉ dưỡng.", 0)
    assert lap(ws) == [(0, 6, 6)], lap(ws)
    assert lap(w("chia làm 2 phân khu chính, phân khu thấp tầng", 0)) == []  # nói tiếp ý, không phải lặp
    ws2 = w("thì thì dự án", 0) + w("ờ", 2) + w("được chia", 3) + w("làm hai phân khu.", 4.5)
    assert lap(ws2)[0][:3] == (0, 1, 1) and (4, "tiếng đệm") in vap(ws2), (lap(ws2), vap(ws2))
    assert any("ngập ngừng" in l for _, l in vap(ws2))  # "chia" → "làm" lặng 1,0s giữa câu
    nhanh = w("một hai ba bốn năm sáu bảy.", 0, 0.1) + w("một hai ba bốn năm sáu bảy.", 3, 0.25) + w("một hai ba bốn năm sáu bảy.", 6, 0.25)
    assert [x[3] for x in toc_do(nhanh)[0]] == ["nhanh", "", ""], toc_do(nhanh)
    tl = {"version": 1, "clips": [{"file": "a", "in": 0, "dur": 9}, {"file": "b", "in": 0, "dur": 0.5}], "transitions": [{"type": "cut"}]}
    g = cat_canh([(0, 9, "clip", 0), (9, 9.5, "clip", 1)], w("xin chào", 8.9, 0.2), [9])
    assert any("CẮT TIẾNG" in x for _, x in g), g
    assert any("giữa từ" in x for _, x in g) and any("chớp" in x for _, x in g) and any("dài" in x for _, x in g), g
    assert any(x[1] == "lặp từ" for x in phan_tich(tl, ws)), phan_tich(tl, ws)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        from ban_dung import doc_loi
        tl, ws = doc_loi(os.path.abspath(sys.argv[1]))
        print("\n".join(bao_cao(phan_tich(tl, ws))))
    else:
        sys.exit("Dùng: python3 scripts/phan_tich_loi.py projects/<tên>")
