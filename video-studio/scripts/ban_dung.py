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
                         "nhan": "(tuỳ chọn) nhãn nhỏ trên, cũng phải là lời đã nói", "nguon": "(số liệu) tài liệu + ngày"}],
               vai "the" (cảnh chèn thẻ): {"vai": "the", "tu": [a, b], "kieu": "checklist|quy-dao|kinh", "title": "...", "items": ["..."], "centre": "...", "sub": "..."}
               (mọi chữ phải là lời đã nói),
               "canh": [{"tu": [a, b], "goi_y": ["mã AutoEdit", ...], "chon": "mã Hào chọn"}]  (agent.py: chia cảnh + hiệu ứng, xem autoedit/HIEU-UNG-MAP.json)}"""
import json, re, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doi_chieu import toks
import loi_nhip
from cau_hinh import lay

VAI = ("hook", "tieu-de", "tu-khoa", "so-lieu", "cta", "the")
KIEU_THE = ("checklist", "quy-dao", "kinh")
MAP_HU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "autoedit", "HIEU-UNG-MAP.json")


def hoa(s):
    """Viết hoa chữ lớn nhưng giữ đơn vị viết thường đúng chính tả (1.080 ha, 50 m²)."""
    return re.sub(r"(\d) (HA|M²|M2|KM)\b", lambda m: m.group(1) + " " + m.group(2).lower(), s.upper())


def doc_loi(pj):
    from phu_de import file_dem
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    f = file_dem(os.path.join(pj, "build"), "voice.wav", tl.get("meta", {}).get("tu_vung"), tl)
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
            if v["vai"] == "the" and v.get("kieu") not in KIEU_THE:
                loi.append(f"mục {k}: thẻ cần 'kieu' là {', '.join(KIEU_THE)}")
            for f in (() if v.get("cua_hao") else ("chu", "nhan", "sub", "title", "centre", "items")):  # cua_hao: câu Hào tự viết cho màn hình (Hào cung cấp = đã xác thực)
                la = [t for t in toks(" ".join(v[f]) if isinstance(v.get(f), list) else v.get(f, "")) if t not in noi]
                if la:
                    loi.append(f"mục {k}: chữ «{', '.join(la)}» trong '{f}' KHÔNG có trong lời nói — không tự thêm chữ, hỏi Hào")
            if v["vai"] == "so-lieu" and not str(v.get("nguon", "")).strip():
                loi.append(f"mục {k}: số liệu cần 'nguon' (vd. 'lời Hào nói, chưa đối chiếu bảng giá')")
    return loi + kiem_canh(bd, w)[0]


def kiem_canh(bd, w):
    """(lỗi, báo) của danh sách cảnh: khoảng từ hợp lệ, liền nhau không chồng; mã hiệu ứng có trong danh mục; cảnh đã chọn hiệu ứng
    có khối thì phải có vai tương ứng nằm trong cảnh (Claude đặt). Hiệu ứng chưa có khối (đợt 2) chỉ báo, cảnh đó dựng chỉ người nói."""
    canh = bd.get("canh") or []
    if not canh:
        return [], []
    mp = json.load(open(MAP_HU, encoding="utf8"))
    loi, bao, truoc = [], [], -1
    for k, c in enumerate(canh, 1):
        a, b = (list(c.get("tu") or []) + [None, None])[:2]
        if not (isinstance(a, int) and isinstance(b, int) and truoc < a <= b < len(w)):
            loi.append(f"cảnh {k}: 'tu' phải là [từ đầu, từ cuối], tăng dần, không chồng cảnh trước, trong 0–{len(w) - 1}"); continue
        truoc = b
        for m in list(c.get("goi_y") or []) + ([c["chon"]] if c.get("chon") else []):
            if m not in mp:
                loi.append(f"cảnh {k}: mã hiệu ứng '{m}' không có trong danh mục")
        m = c.get("chon")
        if m in mp:
            muon = mp[m]
            if not muon["co"]:
                bao.append(f"cảnh {k} ({w[a][1]:.1f}s): '{m}' chưa có trong bộ dựng (đợt 2) → dựng chỉ người nói")
            elif muon["vai"] and not any((v.get("vai") == muon["vai"] or (muon["vai"], v.get("vai")) == ("tieu-de", "hook")) and (muon.get("kieu") in (None, v.get("kieu")))
                                         and v["tu"][0] <= b and v["tu"][1] >= a for v in bd.get("vai", [])):
                loi.append(f"cảnh {k} chọn '{m}': cần vai '{muon['vai']}'{' kiểu ' + muon['kieu'] if muon.get('kieu') else ''} trong từ {a}–{b}")
    return loi, bao


def ap(tl, w, bd):
    tl = json.loads(json.dumps(tl))
    total = sum(c["dur"] for c in tl["clips"])
    vai = bd.get("vai", [])
    lon = [v for v in vai if v["vai"] in ("hook", "tieu-de", "so-lieu", "the")]   # các khoảng thay bằng chữ lớn hoặc cảnh chèn
    trong = lambda i: any(v["tu"][0] <= i <= v["tu"][1] for v in lon)
    khoa = {i for v in vai if v["vai"] in ("tu-khoa", "cta") for i in range(v["tu"][0], v["tu"][1] + 1)}
    tl["texts"] = [x for x in tl.get("texts", []) if not (x.get("auto_loi") or x.get("ban_dung"))]
    tl["cards"] = [x for x in tl.get("cards", []) if not x.get("ban_dung")]
    tl["subtitles"] = [x for x in tl.get("subtitles", []) if not x.get("auto")]  # chữ theo nhịp nói thay phụ đề máy tự sinh (không hiện một câu hai lần); phụ đề Hào tự gõ giữ
    # chữ theo nhịp nói cho phần còn lại; từ khoá do AI chọn (không dùng luật đoán số/tiền)
    # chữ lớn hiện lâu hơn lúc nói (tối thiểu 1,8s, thêm 0,8s) nên bỏ chữ theo nhịp nói rơi vào lúc đó, tránh chồng chữ
    LON_MIN, LON_THEM = lay("the.chu_lon_min", tl), lay("the.chu_lon_them", tl)
    hien = [(max(0, w[v["tu"][0]][1] - 0.1), max(w[v["tu"][0]][1] - 0.1 + LON_MIN, w[v["tu"][1]][2] + LON_THEM)) for v in lon if v["vai"] not in ("so-lieu", "the")]
    che = lambda x: any(a <= x[1] < b for a, b in hien)
    con = [(i, x) for i, x in enumerate(w) if not trong(i) and not che(x)]
    nhom_tu, cur = [], []
    for i, x in con:
        if cur and i != cur[-1][0] + 1:
            nhom_tu.append(cur); cur = []
        cur.append((i, x))
    nhom_tu += [cur] if cur else []
    for doan in nhom_tu:
        for g in loi_nhip.nhom([x for _, x in doan], tl=tl):
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
            tl["cards"].append({"kieu": "so-lieu", "start": round(st, 2), "dur": round(min(max(lay("the.so_lieu_min", tl), en - st + lay("the.so_lieu_them", tl)), total - st), 2), "title": v.get("nhan", ""),
                                "value": hoa(chu), "label": v.get("nhan_duoi", ""), "nguon": v["nguon"], "ban_dung": True})
        elif v["vai"] == "the":
            tl["cards"].append({"kieu": v["kieu"], "start": round(st, 2), "dur": round(min(max(lay("the.the_min", tl), en - st + lay("the.the_them", tl)), total - st), 2),
                                "title": v.get("title", ""), "items": list(v.get("items") or []), "centre": v.get("centre", ""),
                                "sub": v.get("sub", ""), "ban_dung": True})
        else:
            tl["texts"].append({"kind": "title3d", "start": round(st, 2), "dur": round(min(max(LON_MIN, en - st + LON_THEM), total - st), 2), "top": v.get("nhan", ""),
                                "big": hoa(chu), "sub": v.get("sub", ""), "sau_dau": v.get("sau_dau", v["vai"] == "hook"), "ban_dung": True, "vai": v["vai"]})
    tl["texts"].sort(key=lambda x: x["start"])
    return tl


def _tu_kiem():
    w = [["Giá", 0.0, 0.3], ["khoảng", 0.3, 0.6], ["77", 0.6, 0.9], ["tỷ", 0.9, 1.2], ["một", 1.2, 1.4], ["căn.", 1.4, 1.7],
         ["Bếp", 2.0, 2.3], ["đảo", 2.3, 2.6], ["to", 2.6, 2.9], ["rộng", 4.0, 4.3], ["lắm.", 4.3, 4.6]]
    bd = {"vai": [{"vai": "so-lieu", "tu": [2, 3], "nhan": "giá khoảng", "nguon": "lời nói"}, {"vai": "hook", "tu": [6, 7]}, {"vai": "tu-khoa", "tu": [9, 9]}]}
    assert kiem_ban(bd, w) == [], kiem_ban(bd, w)
    assert any("KHÔNG có" in e for e in kiem_ban({"vai": [{"vai": "hook", "tu": [0, 1], "chu": "GIÁ RẺ"}]}, w))   # chữ Hào không nói → chặn
    assert any("nguon" in e for e in kiem_ban({"vai": [{"vai": "so-lieu", "tu": [2, 3]}]}, w))
    tl = {"version": 1, "meta": {}, "audio": {}, "clips": [{"file": "a.mp4", "in": 0, "dur": 5}], "transitions": [],
          "subtitles": [{"start": 0, "dur": 1, "text": "Giá khoảng", "auto": True}, {"start": 2, "dur": 1, "text": "Hào tự gõ"}]}
    out = ap(tl, w, bd)
    assert [x["text"] for x in out["subtitles"]] == ["Hào tự gõ"], "phụ đề tự sinh bỏ (đã có chữ theo nhịp nói), phụ đề tự gõ giữ"
    from timeline import check
    assert check(out) == [], check(out)
    big = [x for x in out["texts"] if x.get("ban_dung")]
    assert big[0]["big"] == "BẾP ĐẢO" and big[0]["sau_dau"] and out["cards"][0]["value"] == "77 TỶ", (big, out["cards"])
    loi = [x for x in out["texts"] if x.get("kind") == "loi"]
    assert not any(q[0] in ("77", "Bếp") for x in loi for q in x["words"]), loi    # phần đã thành chữ lớn/thẻ không lặp lại
    assert any(x["hl"] and x["words"][x["hl"][0]][0] == "rộng" for x in loi), loi  # từ khoá do bản dựng chọn
    assert not any(q[0] == "to" for x in loi for q in x["words"]), loi  # nói lúc chữ lớn còn hiện: bỏ, không chồng chữ
    # thẻ + cảnh: chữ trong thẻ phải là lời đã nói; cảnh chọn hiệu ứng có khối thì phải có vai tương ứng
    the = {"vai": "the", "tu": [6, 10], "kieu": "checklist", "title": "Bếp đảo", "items": ["rộng"]}
    assert kiem_ban({"vai": [the]}, w) == [] and any("KHÔNG có" in e for e in kiem_ban({"vai": [{**the, "items": ["sang"]}]}, w))
    assert ap(tl, w, {"vai": [the]})["cards"][0]["kieu"] == "checklist"
    c = {"vai": [the], "canh": [{"tu": [0, 5], "chon": "count_up"}, {"tu": [6, 10], "chon": "note_board"}]}
    assert any("cần vai 'so-lieu'" in e for e in kiem_ban(c, w)) and not any("cảnh 2" in e for e in kiem_ban(c, w)), kiem_ban(c, w)
    assert kiem_canh({"canh": [{"tu": [0, 5], "chon": "chart_bars"}]}, w)[1] and kiem_canh({"canh": [{"tu": [0, 5], "chon": "xyz"}]}, w)[0]
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
