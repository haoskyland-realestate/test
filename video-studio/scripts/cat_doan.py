"""Cắt bỏ một đoạn [a, b) giây khỏi video đã lên timeline (câu lặp, chỗ nói vấp, khoảng lặng dài), giữ mọi thứ khác khớp:
tách đoạn chính tại chỗ cắt, dời chữ/thẻ/cảnh trám/zoom/âm phía sau, bỏ từ trong đoạn cắt khỏi text ghi âm đã lưu
và dời số thứ tự từ trong BAN-DUNG.json. Không cần nhận dạng giọng lại.
Chạy trong video-studio:  python3 scripts/cat_doan.py projects/<tên> <từ giây> <đến giây>
Nên chọn a, b trong khoảng lặng (xem phan_tich_loi.py / storyboard). Bản cũ lưu ở timeline.json.bak."""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def cat(tl, ws, bd, a, b):
    """Trả (timeline, từ, BAN-DUNG) sau khi bỏ [a, b). Không sửa dữ liệu đầu vào."""
    tl, ws, bd = json.loads(json.dumps(tl)), [list(w) for w in ws], json.loads(json.dumps(bd or {"vai": []}))
    d = round(b - a, 2)
    f = lambda t: t if t <= a else (a if t < b else round(t - d, 2))
    st, clips, trs = 0.0, [], []
    for i, c in enumerate(tl["clips"]):
        e = st + c["dur"]
        if i:
            trs.append(tl["transitions"][i - 1])
        if st < b and e > a:  # đoạn chính bị cắt: giữ phần trước a và phần sau b
            truoc, sau = max(0.0, a - st), max(0.0, e - b)
            if truoc >= 0.05:
                clips.append({**c, "dur": round(truoc, 2)})
            if sau >= 0.05:
                if truoc >= 0.05:
                    trs.append({"type": "cut"})
                clips.append({**c, "in": round(c["in"] + c["dur"] - sau, 2), "dur": round(sau, 2)})
            elif truoc < 0.05 and trs:
                trs.pop()
        else:
            clips.append(c)
        st = e
    tl["clips"], tl["transitions"] = clips, trs[:len(clips) - 1]
    for k in ("texts", "cards", "broll", "zooms", "sfx", "overlays", "subtitles"):
        giu = []
        for x in tl.get(k, []):
            s, e = x["start"], x["start"] + x["dur"]
            s2, e2 = f(s), f(e)
            if e2 - s2 < 0.05:
                continue
            if "in" in x and a < s < b:
                x["in"] = round(x["in"] + (b - s), 2)
            x["start"], x["dur"] = round(s2, 2), round(e2 - s2, 2)
            if "words" in x:
                x["words"] = [[w, f(w0), f(w1)] for w, w0, w1 in x["words"] if not a <= w0 < b]
            giu.append(x)
        tl[k] = giu
    bo = [i for i, w in enumerate(ws) if a <= w[1] < b]
    ws = [[w[0], f(w[1]), f(w[2])] for i, w in enumerate(ws) if i not in bo]
    for v in bd.get("vai", []):
        v["tu"] = [i - sum(1 for j in bo if j < i) for i in v["tu"]]
    return tl, ws, bd


def _tu_kiem():
    tl = {"version": 1, "clips": [{"file": "v", "in": 0, "dur": 10}], "transitions": [],
          "texts": [{"kind": "title3d", "start": 8, "dur": 1, "big": "X"}], "broll": [{"file": "r", "in": 0, "start": 3, "dur": 4}]}
    ws = [["a", 1, 1.5], ["lặp", 4, 4.5], ["b", 7, 7.5]]
    tl2, ws2, bd2 = cat(tl, ws, {"vai": [{"vai": "tu-khoa", "tu": [2, 2]}]}, 3.8, 5.8)
    assert [(c["in"], c["dur"]) for c in tl2["clips"]] == [(0, 3.8), (5.8, 4.2)] and tl2["transitions"] == [{"type": "cut"}], tl2
    assert tl2["texts"][0]["start"] == 6 and tl2["broll"][0] == {"file": "r", "in": 0, "start": 3, "dur": 2.0}, tl2
    assert ws2 == [["a", 1, 1.5], ["b", 5.0, 5.5]] and bd2["vai"][0]["tu"] == [1, 1], (ws2, bd2)
    from timeline import check
    assert check(tl2) == [], check(tl2)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 4 and os.path.isdir(sys.argv[1]):
        from phu_de import file_dem
        pj, a, b = os.path.abspath(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
        if not 0 <= a < b:
            sys.exit("Cần 0 ≤ từ giây < đến giây")
        T, BD = os.path.join(pj, "timeline.json"), os.path.join(pj, "BAN-DUNG.json")
        tl = json.load(open(T, encoding="utf8"))
        TR = file_dem(os.path.join(pj, "build"), "voice.wav", tl.get("meta", {}).get("tu_vung"))
        ws = json.load(open(TR, encoding="utf8")) if os.path.exists(TR) else []
        bd = json.load(open(BD, encoding="utf8")) if os.path.exists(BD) else None
        tl2, ws2, bd2 = cat(tl, ws, bd, a, b)
        shutil.copy(T, T + ".bak")
        json.dump(tl2, open(T, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        if ws:
            json.dump(ws2, open(TR, "w", encoding="utf8"), ensure_ascii=False)
        if bd:
            json.dump(bd2, open(BD, "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print(f"Đã cắt {b - a:.2f}s ({a:.2f}–{b:.2f}s), bỏ {len(ws) - len(ws2)} từ. Chạy lại ban_dung.py ap + ap_mau nếu dự án dùng bản dựng talking head.")
    else:
        sys.exit("Dùng: python3 scripts/cat_doan.py projects/<tên> <từ giây> <đến giây>")
