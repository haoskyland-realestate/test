"""Bản dựng talking head theo từng bước, AI (Claude Code) quyết định vai trò chữ từ CHÍNH lời Hào nói:
  1. chep  : text từ ghi âm → build/LOI-NOI.md (từng câu, số thứ tự từng từ, giây). Không sửa, không đoán.
  2. (AI)  : Claude đọc LOI-NOI.md, viết BAN-DUNG.json trong dự án: chữ nào là hook, tiêu đề, từ khoá, số liệu, kêu gọi (theo số thứ tự từ).
             Gửi Hào bảng vai trò để duyệt. Chữ hiện ra PHẢI là chữ Hào nói (công cụ chặn nếu khác); số liệu cần nguồn.
  3. ap    : BAN-DUNG.json → khung hình trong timeline: hook = chữ lớn sau đầu 0–3 s; tiêu đề = chữ lớn; số liệu = cảnh chèn thẻ số;
             từ khoá = tô màu trong chữ theo nhịp nói; phần còn lại = chữ theo nhịp nói (ngang ngực). Rồi đối chiếu (doi_chieu.py).
  4. Xem khung tĩnh (dung.py --nhap, chụp vài mốc) → Hào duyệt bố cục.
  5. Chuyển động + âm: áp mẫu (vd. talking-cam-01) → dựng bản cuối (dung.py) → ghép.
Chạy trong video-studio:  python3 scripts/ban_dung.py chep projects/<tên>   ·   python3 scripts/ban_dung.py ap projects/<tên>   ·   tự kiểm: --tu-kiem
BAN-DUNG.json: {"vai": [{"vai": "hook|tieu-de|tu-khoa|so-lieu|cta", "tu": [từ đầu, từ cuối], "chu": "(tuỳ chọn) chữ hiện, phải gồm từ đã nói",
                         "sub": "(tuỳ chọn) dòng dưới chữ lớn", "sau_dau": true/false, "cua_hao": true = câu Hào tự viết (không cần là lời đã nói),
                         "nhan": "(tuỳ chọn) nhãn nhỏ trên, cũng phải là lời đã nói", "nguon": "(số liệu) tài liệu + ngày"}]}"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doi_chieu import toks
import loi_nhip

VAI = ("hook", "tieu-de", "tu-khoa", "so-lieu", "cta")


def doc_loi(pj):
    from phu_de import file_dem
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    f = file_dem(os.path.join(pj, "build"), "voice.wav", tl.get("meta", {}).get("tu_vung"))
    if not os.path.exists(f):
        sys.exit("Chưa có text từ ghi âm: chạy loi_nhip.py hoặc phu_de.py trước (cần build/voice.wav).")
    from phu_de import sua_tu  # từ nghe sai đã sửa theo ngữ cảnh (meta.sua_tu), áp mỗi lần đọc
    return tl, sua_tu(json.load(open(f, encoding="utf8")), tl.get("meta", {}).get("sua_tu"))


def chep(pj):
    tl, w = doc_loi(pj)
    out, cau = ["# Lời nói (text từ ghi âm, chưa sửa)", "", "Số trong ngoặc vuông là số thứ tự từ, dùng cho `BAN-DUNG.json`.", ""], []
    for i, x in enumerate(w):
        cau.append(f"[{i}]{x[0]}")
        if re.search(r"[.?!,]$", x[0]) or i == len(w) - 1:
            a = i - len(cau) + 1
            out.append(f"- **{w[a][1]:.1f}–{x[2]:.1f}s**: " + " ".join(cau)); cau = []
    open(os.path.join(pj, "build", "LOI-NOI.md"), "w", encoding="utf8").write("\n".join(out) + "\n")
    return len(w)


def kiem_ban(bd, w):
    """Lỗi của bản dựng: vai sai, khoảng từ sai, chữ hiện không phải lời đã nói, số liệu thiếu nguồn."""
    loi, noi = [], set(t for x in w for t in toks(x[0]))
    for k, v in enumerate(bd.get("vai", []), 1):
        a, b = (list(v.get("tu") or []) + [None, None])[:2]
        if v.get("vai") not in VAI:
            loi.append(f"mục {k}: vai '{v.get('vai')}' không có (dùng {', '.join(VAI)})")
        elif not (isinstance(a, int) and isinstance(b, int) and 0 <= a <= b < len(w)):
            loi.append(f"mục {k}: 'tu' phải là [từ đầu, từ cuối] trong 0–{len(w) - 1}")
        else:
            for f in (() if v.get("cua_hao") else ("chu", "nhan", "sub")):  # cua_hao: câu Hào tự viết cho màn hình (Hào cung cấp = đã xác thực)
                la = [t for t in toks(v.get(f, "")) if t not in noi]
                if la:
                    loi.append(f"mục {k}: chữ «{', '.join(la)}» trong '{f}' KHÔNG có trong lời nói — không tự thêm chữ, hỏi Hào")
            if v["vai"] == "so-lieu" and not str(v.get("nguon", "")).strip():
                loi.append(f"mục {k}: số liệu cần 'nguon' (vd. 'lời Hào nói, chưa đối chiếu bảng giá')")
    return loi


def ap(tl, w, bd):
    tl = json.loads(json.dumps(tl))
    total = sum(c["dur"] for c in tl["clips"])
    vai = bd.get("vai", [])
    lon = [v for v in vai if v["vai"] in ("hook", "tieu-de", "so-lieu")]   # các khoảng thay bằng chữ lớn hoặc cảnh chèn
    trong = lambda i: any(v["tu"][0] <= i <= v["tu"][1] for v in lon)
    khoa = {i for v in vai if v["vai"] in ("tu-khoa", "cta") for i in range(v["tu"][0], v["tu"][1] + 1)}
    tl["texts"] = [x for x in tl.get("texts", []) if not (x.get("auto_loi") or x.get("ban_dung"))]
    tl["cards"] = [x for x in tl.get("cards", []) if not x.get("ban_dung")]
    # chữ theo nhịp nói cho phần còn lại; từ khoá do AI chọn (không dùng luật đoán số/tiền)
    con = [(i, x) for i, x in enumerate(w) if not trong(i)]
    nhom_tu, cur = [], []
    for i, x in con:
        if cur and i != cur[-1][0] + 1:
            nhom_tu.append(cur); cur = []
        cur.append((i, x))
    nhom_tu += [cur] if cur else []
    for doan in nhom_tu:
        for g in loi_nhip.nhom([x for _, x in doan]):
            gi = [i for i, x in doan if [x[0], x[1], x[2]] in g["words"]]
            g["hl"] = [k for k, i in enumerate(gi) if i in khoa]
            g["bam_nguoi"] = True
            g["start"] = round(min(g["start"], total - 0.1), 2); g["dur"] = round(max(0.1, min(g["dur"], total - g["start"])), 2)
            tl["texts"].append(g)
    for v in lon:
        a, b = v["tu"]
        st, en = max(0, w[a][1] - 0.1), w[b][2]
        chu = v.get("chu") or " ".join(x[0] for x in w[a:b + 1]).strip(".,!?")
        if v["vai"] == "so-lieu":
            tl["cards"].append({"kieu": "so-lieu", "start": round(st, 2), "dur": round(min(max(2.0, en - st + 0.6), total - st), 2), "title": v.get("nhan", ""),
                                "value": chu.upper(), "label": v.get("nhan_duoi", ""), "nguon": v["nguon"], "ban_dung": True})
        else:
            tl["texts"].append({"kind": "title3d", "start": round(st, 2), "dur": round(min(max(1.8, en - st + 0.8), total - st), 2), "top": v.get("nhan", ""),
                                "big": chu.upper(), "sub": v.get("sub", ""), "sau_dau": v.get("sau_dau", v["vai"] == "hook"), "ban_dung": True, "vai": v["vai"]})
    tl["texts"].sort(key=lambda x: x["start"])
    return tl


def _tu_kiem():
    w = [["Giá", 0.0, 0.3], ["khoảng", 0.3, 0.6], ["77", 0.6, 0.9], ["tỷ", 0.9, 1.2], ["một", 1.2, 1.4], ["căn.", 1.4, 1.7],
         ["Bếp", 2.0, 2.3], ["đảo", 2.3, 2.6], ["rộng", 2.6, 2.9], ["lắm.", 2.9, 3.2]]
    bd = {"vai": [{"vai": "so-lieu", "tu": [2, 3], "nhan": "giá khoảng", "nguon": "lời nói"}, {"vai": "hook", "tu": [6, 7]}, {"vai": "tu-khoa", "tu": [8, 8]}]}
    assert kiem_ban(bd, w) == [], kiem_ban(bd, w)
    assert any("KHÔNG có" in e for e in kiem_ban({"vai": [{"vai": "hook", "tu": [0, 1], "chu": "GIÁ RẺ"}]}, w))   # chữ Hào không nói → chặn
    assert any("nguon" in e for e in kiem_ban({"vai": [{"vai": "so-lieu", "tu": [2, 3]}]}, w))
    tl = {"version": 1, "meta": {}, "audio": {}, "clips": [{"file": "a.mp4", "in": 0, "dur": 4}], "transitions": []}
    out = ap(tl, w, bd)
    from timeline import check
    assert check(out) == [], check(out)
    big = [x for x in out["texts"] if x.get("ban_dung")]
    assert big[0]["big"] == "BẾP ĐẢO" and big[0]["sau_dau"] and out["cards"][0]["value"] == "77 TỶ", (big, out["cards"])
    loi = [x for x in out["texts"] if x.get("kind") == "loi"]
    assert not any(q[0] in ("77", "Bếp") for x in loi for q in x["words"]), loi    # phần đã thành chữ lớn/thẻ không lặp lại
    assert any(x["hl"] and x["words"][x["hl"][0]][0] == "rộng" for x in loi), loi  # từ khoá do bản dựng chọn
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 3 and sys.argv[1] in ("chep", "ap") and os.path.isdir(sys.argv[2]):
        pj = os.path.abspath(sys.argv[2])
        if sys.argv[1] == "chep":
            print(f"Đã viết build/LOI-NOI.md ({chep(pj)} từ). Bước tiếp: Claude viết BAN-DUNG.json, gửi Hào bảng vai trò.")
        else:
            tl, w = doc_loi(pj)
            bd = json.load(open(os.path.join(pj, "BAN-DUNG.json"), encoding="utf8"))
            loi = kiem_ban(bd, w)
            if loi:
                sys.exit("BẢN DỰNG CHƯA ĐẠT, hỏi Hào:\n- " + "\n- ".join(loi))
            import shutil; shutil.copy(os.path.join(pj, "timeline.json"), os.path.join(pj, "timeline.json.bak"))
            json.dump(ap(tl, w, bd), open(os.path.join(pj, "timeline.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
            print("Đã đặt khung hình theo BAN-DUNG.json (bản cũ: timeline.json.bak). Bước tiếp: doi_chieu.py, dung.py --nhap để xem khung.")
    else:
        sys.exit(__doc__)
