"""Đặt chữ lớn lên video theo kịch bản: đọc cột "Chữ trên màn hình" của KICH-BAN.md, tìm lúc Hào nói cụm đó
trong phụ đề (tự sinh từ giọng), đặt khối chữ 3D (title3d) đúng lúc ấy. Không tìm thấy thì theo cột "Giây", không có thì nối tiếp.
Chạy trong video-studio:  python3 scripts/kich_ban.py projects/<tên>      (ghi đè timeline.json, giữ .bak)
Cách viết ô "Chữ trên màn hình": "chỉ từ / *2.4 TỶ* / cho căn hộ 60–80m2"  (ngăn bằng " / "; phần có *…* là chữ lớn,
  trước nó là nhãn trên, sau nó là dòng dưới; không có * thì phần đầu là chữ lớn); nhiều chữ trong một hàng thì ngăn bằng ";".
Chữ do kịch bản đặt có "kb": true: chạy lại chỉ thay các khối đó, chữ Hào tự thêm giữ nguyên.
Dự án đã áp mẫu edit thì hiệu ứng âm tự rải lại theo chữ mới (giữ chuyển cảnh)."""
import json, os, re, shutil, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout

CHUA_DIEN = re.compile(r"^\(.*\)$|^\[\.\.\.\]$|^-?$")  # ô mẫu như "(hook)", "[...]" hoặc trống


def bo_dau(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tu(s):
    """Tách từ để so: bỏ *, dấu câu; số 2,4 / 2.4 → 2 4; chữ thường."""
    s = unicodedata.normalize("NFC", s).replace("*", " ").replace("\u00a0", " ").lower()
    return re.findall(r"\w+", s)


def doc_bang(md):
    """Các hàng của bảng kịch bản: [{"giay": "0–3", "chu": ["chỉ từ / 2.4 TỶ", ...]}]."""
    rows, cot = [], None
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cot is None:
            if any("Chữ trên màn hình" in c for c in cells):
                cot = {"chu": next(i for i, c in enumerate(cells) if "Chữ trên màn hình" in c),
                       "giay": next((i for i, c in enumerate(cells) if c.lower().startswith("giây")), None)}
            continue
        if set("".join(cells)) <= set("-: ") or len(cells) <= cot["chu"]:
            continue  # dòng kẻ |---|
        chu = [x.strip() for x in cells[cot["chu"]].replace("<br>", ";").split(";")]
        chu = [x for x in chu if x and not CHUA_DIEN.match(x)]
        if chu:
            rows.append({"giay": cells[cot["giay"]] if cot["giay"] is not None else "", "chu": chu})
    return rows


def dong_thoi_gian(subs):
    """Chuỗi từ của phụ đề kèm mốc giờ ước lượng (chia đều thời lượng dòng theo độ dài từ)."""
    out = []
    for x in sorted(subs, key=lambda x: x["start"]):
        ws = tu(x["text"])
        n = sum(len(w) for w in ws) or 1
        acc = 0
        for w in ws:
            out.append((w, bo_dau(w), x["start"] + x["dur"] * acc / n))
            acc += len(w)
    return out


def tim(stream, q, tu_vi_tri):
    """Vị trí khớp tốt nhất của cụm từ q (từ sau tu_vi_tri). Trả (điểm 0..1, chỉ số) hoặc (0, None)."""
    q = [bo_dau(w) for w in q]
    best = (0.0, None)
    for i in range(tu_vi_tri, len(stream) - len(q) + 1):
        win = [s[1] for s in stream[i:i + len(q) + 1]]  # cho lệch 1 từ (ASR thêm/bớt một tiếng)
        hit, j, first = 0, 0, None
        for w in q:
            if w in win[j:]:
                j = win.index(w, j) + 1
                hit += 1
                first = j - 1 if first is None else first
        sc = hit / len(q)
        if sc > best[0] + 1e-9:
            best = (sc, i + first)  # mốc = từ khớp đầu tiên, không phải đầu cửa sổ so
    return best


def tach(chu):
    """Phần có *…* là chữ lớn (trước nó: nhãn trên, sau nó: dòng dưới). Không đánh dấu: 3 phần = trên/lớn/dưới, còn lại phần đầu là chữ lớn."""
    p = [x.strip() for x in chu.split(" / ") if x.strip()]
    i = next((k for k, x in enumerate(p) if "*" in x), 1 if len(p) >= 3 else 0)
    out = {"big": p[i]}
    if i:
        out["top"] = " / ".join(p[:i])
    if p[i + 1:]:
        out["sub"] = " / ".join(p[i + 1:])
    return out


def giay(s):
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)", s or "")
    return float(m[1].replace(",", ".")) if m else None


def dat_chu(tl, md):
    """Trả (timeline mới, báo cáo từng chữ)."""
    tl = json.loads(json.dumps(tl))
    total = layout(tl)["total"]
    stream = dong_thoi_gian(tl.get("subtitles", []))
    tl["texts"] = [x for x in tl.get("texts", []) if not x.get("kb")]
    moi, bao, cur, t_prev = [], [], 0, 0.0
    for row in doc_bang(md):
        for k, chu in enumerate(row["chu"]):
            b = tach(chu)
            sc, idx, phan = 0.0, None, None
            for key in ("big", "top", "sub"):  # chữ lớn thường chính là từ được nói; không có thì thử nhãn/dòng dưới
                if b.get(key) and (q := tu(b[key])):
                    s, i = tim(stream, q, cur)
                    if s >= 0.6 and (idx is None or s > sc + 0.2):
                        sc, idx, phan = s, i, key
            if idx is not None:
                t = stream[idx][2] - (0.15 if phan == "big" else 0.0)  # chữ hiện ngay trước khi nói tới, nhãn trên kịp hiện trước
                cur, cach = idx + 1, f"khớp giọng {sc:.0%}"
            elif k == 0 and giay(row["giay"]) is not None and giay(row["giay"]) >= t_prev:
                t, cach = giay(row["giay"]), "theo cột Giây"
            else:
                t, cach = t_prev + (0.1 if moi else 0.2), "nối tiếp chữ trước"
            t = max(0.0, min(t, total - 1.0))
            moi.append({"kind": "title3d", "start": round(t, 2), "dur": 2.0, **b, "kb": True})
            bao.append((chu, round(t, 2), cach))
            t_prev = t + 1.5
    for a, b in zip(moi, moi[1:] + [None]):  # mỗi chữ ở tới khi chữ sau hiện (1,2–3,5 giây, như video mẫu)
        end = b["start"] - 0.05 if b else a["start"] + 3.0
        a["dur"] = round(max(1.2, min(3.5, end - a["start"], total - a["start"])), 2)
    tl["texts"] = sorted(tl["texts"] + moi, key=lambda x: x["start"])
    if tl.get("meta", {}).get("mau"):
        from ap_mau import MAU, ap
        if tl["meta"]["mau"] in MAU:
            tl = ap(tl, MAU[tl["meta"]["mau"]], chi_am=True)
    return tl, bao


def _tu_kiem():
    md = """| # | Giây | Lời đọc | Chữ trên màn hình (`*từ*` = tô vàng) | Cảnh gợi ý |
|---|---|---|---|---|
| 1 | 0–3 | Chỉ từ 2,4 tỷ cho căn hộ | chỉ từ / *2.4 TỶ* / cho căn hộ 60–80m2 | |
| 2 | 8 | (rủi ro) | Rủi ro / *lãi suất thả nổi*; Không có trong lời | |
| 3 | | (lời kêu gọi) | (lời kêu gọi) | |"""
    tl = {"version": 1, "meta": {"platform": "tiktok", "mau": "edit-phim-01"}, "audio": {"music": None},
          "clips": [{"file": "a.mp4", "in": 0, "dur": 12}], "transitions": [],
          "texts": [{"kind": "line", "start": 9, "dur": 2, "lines": ["tự thêm"]}, {"kind": "title3d", "start": 1, "dur": 1, "big": "cũ", "kb": True}],
          "subtitles": [{"start": 1.0, "dur": 2.0, "text": "chỉ từ *2,4 tỷ* cho căn hộ", "auto": True},
                        {"start": 5.0, "dur": 2.0, "text": "nhưng lãi xuất thả nổi sau ưu đãi", "auto": True}]}
    assert [r["chu"] for r in doc_bang(md)] == [["chỉ từ / *2.4 TỶ* / cho căn hộ 60–80m2"], ["Rủi ro / *lãi suất thả nổi*", "Không có trong lời"]]
    out, bao = dat_chu(tl, md)
    assert check(out) == [], check(out)
    kb = [x for x in out["texts"] if x.get("kb")]
    assert [x["big"] for x in kb] == ["*2.4 TỶ*", "*lãi suất thả nổi*", "Không có trong lời"], kb
    assert kb[0]["top"] == "chỉ từ" and kb[0]["sub"] == "cho căn hộ 60–80m2"
    # "2,4 tỷ" bắt đầu ở từ thứ 3 của dòng 1 → khoảng giây 1,5; chữ hiện sớm 0,15 s
    assert 1.15 < kb[0]["start"] < 1.6, kb[0]
    assert tach("6 TRIỆU / đến khi nhận nhà") == {"big": "6 TRIỆU", "sub": "đến khi nhận nhà"}
    assert tach("Cách ga Metro / *300M*") == {"top": "Cách ga Metro", "big": "*300M*"}
    assert tach("a / b / c") == {"top": "a", "big": "b", "sub": "c"}
    assert bao[1][2].startswith("khớp giọng") and 5.0 < kb[1]["start"] < 6.0, bao  # ASR viết "lãi xuất" vẫn khớp 2/3 từ… sau bỏ dấu
    assert bao[2][2] == "nối tiếp chữ trước", bao
    assert any(x.get("lines") == ["tự thêm"] for x in out["texts"]) and not any(x.get("big") == "cũ" for x in out["texts"])
    assert sum(1 for x in out["sfx"] if x["file"] == "chu_swish-pop_01") == 4 and any(x["file"] == "ting_don_01" for x in out["sfx"])
    again, _ = dat_chu(out, md)
    assert len(again["texts"]) == len(out["texts"]) and len(again["sfx"]) == len(out["sfx"])
    print("OK", [(c, t, h) for c, t, h in bao])


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    if len(sys.argv) != 2:
        sys.exit("Dùng: python3 scripts/kich_ban.py projects/<tên>")
    d = sys.argv[1]
    p, kb = os.path.join(d, "timeline.json"), os.path.join(d, "KICH-BAN.md")
    if not os.path.exists(kb):
        sys.exit(f"Chưa có {kb} (mẫu: mau/du-an-video/KICH-BAN.md)")
    out, bao = dat_chu(json.load(open(p, encoding="utf8")), open(kb, encoding="utf8").read())
    if errs := check(out):
        sys.exit("Timeline sau khi đặt chữ bị lỗi:\n- " + "\n- ".join(errs))
    shutil.copy(p, p + ".bak")
    json.dump(out, open(p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    for chu, t, cach in bao:
        print(f"{t:6.2f}s  {chu}  ({cach})")
    print(f"Đã đặt {len(bao)} chữ. Bản cũ: timeline.json.bak")
