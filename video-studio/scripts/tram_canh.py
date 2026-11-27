"""Trám cảnh tự động (Hào chốt 27/11): câu nào nói tới thứ có hình trong kho tài nguyên DỰ ÁN (hồ bơi, mặt tiền, sơ đồ…) thì phủ ảnh/video đó lên
đúng lúc nói, ảnh tĩnh đẩy vào/kéo ra chậm và êm; câu dài (> phan_tich.canh_dai) không có hình khớp thì dùng cảnh trám không lời từ xep_canh.py.
Mỗi file dùng một lần, không đè lên cảnh chèn/chữ lớn/cảnh trám Hào đã đặt, không trám 3 giây đầu (hook là mặt người nói).
Khớp theo cụm từ: tên file (ho-boi_01.jpg → "ho boi") + mô tả trong kho/MO-TA.json ({"<đường dẫn kho>": "hồ bơi, mặt tiền"}, Claude viết một lần mỗi file).
Không đoán: câu không có hình khớp → TRAM-CANH.md "cần hình" (đợt 2: motion graphic), Hào duyệt ở cổng 2/3.
Chạy trong video-studio (sau khi có text ghi âm, sau master cut):
  python scripts/tram_canh.py projects/<tên>              trám + ghi TRAM-CANH.md (timeline giữ .bak)
  python scripts/tram_canh.py projects/<tên> --can-mo-ta  liệt kê file kho dự án chưa có mô tả + ảnh nhỏ build/mo-ta/ cho Claude xem"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kho
from cau_hinh import lay

MO_TA = os.path.join(kho.DIR, "MO-TA.json")
DAU = 3.0  # không trám hook


def cum(s):
    """Cụm từ khoá không dấu từ tên file hoặc mô tả: 'ho-boi_01.jpg' → ['ho boi']; 'hồ bơi, mặt tiền' → ['ho boi', 'mat tien']."""
    s = kho.bo_dau(os.path.splitext(os.path.basename(s))[0] if "/" in s or "." in s[-5:] else s)
    out = []
    for p in re.split(r"[,;_]|\s-\s", s.replace("-", " ")):
        w = [x for x in re.findall(r"[a-z]+", p) if x not in ("anh", "video", "img", "dsc", "clip", "file")]
        if len(w) >= 2 or (w and len(w[0]) >= 4):
            out.append(" ".join(w))
    return out


def khop(doan, f, cs):
    """Chỗ câu nhắc tới tài nguyên: cụm 1 từ phải trùng nguyên từ; cụm nhiều từ cần trùng nguyên cụm hoặc ≥ 2 cặp từ liền nhau
    (người nói hay đảo thứ tự: tên file "vincom trung tam thuong mai", lời nói "trung tâm thương mại Vincom").
    Trả (vị trí ký tự trong đoạn, file, cụm) của cụm khớp nhiều nhất, None nếu không khớp."""
    tot = None
    for c in cs:
        w = c.split()
        cap = [" ".join(w[k:k + 2]) for k in range(len(w) - 1)] or w
        vi = [m.start() for p in cap for m in [re.search(r"\b" + re.escape(p) + r"\b", doan)] if m]
        du = len(vi) == len(cap) or len(vi) >= 2
        if du and (tot is None or len(vi) > tot[0]):
            tot = (len(vi), min(vi), c)
    return (tot[1], -tot[0], f, tot[2]) if tot else None  # cùng chỗ nhắc: cụm khớp nhiều cặp từ hơn đứng trước


def tai_nguyen(tl, ten_da):
    """Ảnh/video của dự án trong kho: [(tên kho:…, [cụm từ])]."""
    da = kho.bo_dau(tl.get("meta", {}).get("du_an") or (ten_da.split("_")[2] if ten_da.count("_") >= 3 else ""))
    mt = json.load(open(MO_TA, encoding="utf8")) if os.path.exists(MO_TA) else {}
    out = []
    for t in kho.doc()["tep"]:
        if t.get("lop") == "du-an" and t.get("chu") == da and t["loai"] in ("anh", "video"):
            out.append(("kho:" + t["p"], cum(t["p"]) + [c for x in mt.get(t["p"], "").split(",") for c in cum(x)]))
    return out


def dat(ws, tai, tram, chiem, total, canh_dai=7.0):
    """ws: [[từ, đầu, cuối]] trên video thành phẩm; tai: [(file, [cụm])]; tram: [file raw không lời]; chiem: [(đầu, cuối)] đã có hình.
    Trả (broll mới, báo cáo [(giây, câu, kết quả)])."""
    from phan_tich_loi import cau
    chu = " ".join(kho.bo_dau(w[0]) for w in ws)
    vt, o = [], 0  # vị trí ký tự → chỉ số từ
    for i, w in enumerate(ws):
        vt.append(o); o += len(kho.bo_dau(w[0])) + 1
    da_dung, moi, bc = set(), [], []
    trong = lambda a, b: all(b <= x or a >= y for x, y in chiem + [(m["start"], m["start"] + m["dur"]) for m in moi])
    for a, b in cau(ws):
        t0, t1 = ws[a][1], ws[b][2]
        doan = chu[vt[a]:vt[b] + len(kho.bo_dau(ws[b][0]))]
        co = False
        ung = sorted(x for f, cs in tai if f not in da_dung for x in [khop(doan, f, cs)] if x)
        ung = [x for k, x in enumerate(ung) if k == 0 or x[0] != ung[k - 1][0]]  # một chỗ nhắc một hình: giữ hình khớp nhiều cặp từ nhất
        moc = [max(DAU, ws[max(j for j in range(a, b + 1) if vt[j] <= vt[a] + x[0])][1] - 0.2) for x in ung]  # lúc nhắc tới từng thứ
        het = 0.0
        for k, (vi, _, f, c) in enumerate(ung):
            i = max(j for j in range(a, b + 1) if vt[j] <= vt[a] + vi)
            st = round(max(moc[k], het), 2)  # nhắc dồn dập: hình sau nối ngay khi hình trước đủ 1,5 giây
            den = min(st + 4.0, max(st + 2.5, t1))
            if k + 1 < len(ung):  # liệt kê: hình giữ tới lúc nhắc thứ tiếp theo, tối thiểu 1,5 giây
                den = min(den, max(st + 1.5, moc[k + 1]))
            du = round(den - st, 2)
            if f not in da_dung and st + du <= total and trong(st, st + du):
                moi.append({"start": round(st, 2), "dur": du, "file": f, "in": 0, "tram": True, "ly_do": c})
                da_dung.add(f); co = True; het = st + du
                bc.append((ws[i][1], " ".join(w[0] for w in ws[a:b + 1]), f"{f} (khớp «{c}»)"))
        if co:
            continue
        if t1 - t0 > canh_dai and tram:
            f = next((x for x in tram if x not in da_dung), None)
            st = round(max(DAU, (t0 + t1) / 2 - 1.5), 2)
            if f and trong(st, st + 3):
                moi.append({"start": st, "dur": 3.0, "file": f, "in": 1.0, "tram": True, "ly_do": "câu dài, cảnh trám không lời"})
                da_dung.add(f); bc.append((t0, " ".join(w[0] for w in ws[a:b + 1]), f"{f} (câu dài {t1 - t0:.0f}s)")); continue
        if t1 - t0 >= 4 and t0 >= DAU:
            bc.append((t0, " ".join(w[0] for w in ws[a:b + 1]), "CẦN HÌNH: chưa có ảnh/video khớp (đợt 2: motion graphic) hoặc để mặt người nói"))
    return moi, bc


def chay(pj):
    from ban_dung import doc_loi
    from timeline import layout
    tl, ws = doc_loi(pj)
    T = os.path.join(pj, "timeline.json")
    tl = json.load(open(T, encoding="utf8"))
    total = layout(tl)["total"]
    tl["broll"] = [x for x in tl.get("broll", []) if not x.get("tram")]  # chạy lại: chỉ thay cảnh máy tự trám
    chiem = [(x["start"], x["start"] + x["dur"]) for x in tl["broll"] + tl.get("cards", [])]
    chiem += [(x["start"], x["start"] + x["dur"]) for x in tl.get("texts", []) if x.get("kind") in ("title3d", "hook", "stat")]
    tram = (tl.get("meta", {}).get("xep_canh") or {}).get("canh_tram", [])
    moi, bc = dat(ws, tai_nguyen(tl, os.path.basename(pj)), tram, chiem, total, lay("phan_tich.canh_dai", tl))
    shutil.copy(T, T + ".bak")
    tl["broll"] = sorted(tl["broll"] + moi, key=lambda x: x["start"])
    json.dump(tl, open(T, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    md = ["# Trám cảnh tự động", "", "Ảnh/video kho dự án đặt đúng lúc nói tới; câu dài dùng cảnh không lời. Hào đổi/bỏ ở cổng duyệt.", "",
          "| Giây | Câu | Trám |", "|---|---|---|"] + [f"| {t:.1f} | {c[:90]} | {k} |" for t, c, k in bc]
    open(os.path.join(pj, "TRAM-CANH.md"), "w", encoding="utf8").write("\n".join(md) + "\n")
    return moi, bc


def can_mo_ta(pj):
    """File kho dự án chưa có mô tả: tạo ảnh nhỏ build/mo-ta/<n>.jpg, ghi CAN-MO-TA.md. Trả số file."""
    tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
    mt = json.load(open(MO_TA, encoding="utf8")) if os.path.exists(MO_TA) else {}
    thieu = [f for f, _ in tai_nguyen(tl, os.path.basename(pj)) if f[4:] not in mt]
    if not thieu:
        return 0
    d = os.path.join(pj, "build", "mo-ta"); os.makedirs(d, exist_ok=True)
    md = ["# Cần Claude mô tả ảnh/video kho dự án", "", f"Xem từng ảnh nhỏ, ghi vài cụm từ (hồ bơi, mặt tiền, phòng khách…) vào `{MO_TA}` theo dạng",
          '`{"<đường dẫn kho>": "cụm 1, cụm 2"}`. Mỗi file chỉ làm một lần.', ""]
    for n, f in enumerate(thieu, 1):
        out = os.path.join(d, f"{n:03d}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", kho.duong_dan(f), "-frames:v", "1", "-vf", "scale=320:-2", out])
        if not os.path.exists(out):  # ảnh tĩnh / video ngắn hơn 1 giây
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", kho.duong_dan(f), "-frames:v", "1", "-vf", "scale=320:-2", out])
        md.append(f"- `{f[4:]}` → build/mo-ta/{n:03d}.jpg")
    open(os.path.join(pj, "CAN-MO-TA.md"), "w", encoding="utf8").write("\n".join(md) + "\n")
    return len(thieu)


def _tu_kiem():
    assert cum("20_DU-AN/can-gio/anh/ho-boi_01.jpg") == ["ho boi"] and cum("hồ bơi vô cực, mặt tiền") == ["ho boi vo cuc", "mat tien"]
    assert cum("IMG_0001.jpg") == [] and cum("cong-vien_bien.mp4") == ["cong vien", "bien"]
    w = lambda s, t0, d=0.3: [[x, round(t0 + k * d, 2), round(t0 + (k + 1) * d, 2)] for k, x in enumerate(s.split())]
    ws = (w("Xin chào anh chị.", 0) + w("Dự án có hồ bơi vô cực rất rộng.", 4) + w("Mặt tiền nhìn ra biển.", 9)
          + w("Đây là một câu nói rất dài không có gì để minh hoạ cả mà người xem vẫn phải nghe hết trước khi chuyển ý tiếp.", 12, 0.4)
          + w("Câu này cũng khá dài để thử chỗ cần hình minh hoạ.", 25, 0.5))
    tai = [("kho:da/ho-boi.jpg", ["ho boi"]), ("kho:da/ho-boi-vo-cuc.jpg", ["ho boi vo cuc"]), ("kho:da/mat-tien.mp4", ["mat tien"])]
    moi, bc = dat(ws, tai, ["flycam.mp4"], [(9.0, 11.0)], 40)
    f = {m["file"]: m for m in moi}
    assert khop("du an co trung tam thuong mai vincom", "v", ["vincom trung tam thuong mai"]), "đảo thứ tự vẫn khớp"
    assert dat(ws, list(reversed(tai)), [], [], 40)[0][0]["file"] == "kho:da/ho-boi-vo-cuc.jpg", "cùng chỗ nhắc: chọn cụm khớp dài hơn"
    assert not khop("di thuong xuyen", "v", ["vincom trung tam thuong mai"]) and not khop("ho boi", "x", ["ho dieu hoa"])
    assert "kho:da/ho-boi-vo-cuc.jpg" in f and f["kho:da/ho-boi-vo-cuc.jpg"]["start"] == round(4 + 3 * 0.3 - 0.2, 2), moi   # cụm dài nhất, đúng lúc nói
    assert "kho:da/mat-tien.mp4" not in f, "đè lên cảnh chèn có sẵn 9–11s"
    assert "flycam.mp4" in f and 2.5 <= f["kho:da/ho-boi-vo-cuc.jpg"]["dur"] <= 4, moi                                     # câu dài → cảnh trám
    assert any("CẦN HÌNH" in k for _, _, k in bc), bc
    assert all(m["start"] >= DAU for m in moi)
    # liệt kê nhiều thứ trong một câu: mỗi hình giữ tới lúc nhắc thứ sau, không bỏ sót
    ws2 = w("Xin chào.", 0) + w("Có công viên sinh thái rồi hồ điều hoà và trường học liên cấp nữa.", 4)
    tai2 = [("kho:cv.jpg", ["cong vien sinh thai"]), ("kho:hdh.jpg", ["ho dieu hoa"]), ("kho:th.jpg", ["truong hoc"])]
    m2 = dat(ws2, tai2, [], [], 40)[0]
    assert [m["file"] for m in m2] == ["kho:cv.jpg", "kho:hdh.jpg", "kho:th.jpg"], m2
    assert all(x["start"] + x["dur"] <= y["start"] + 1e-6 for x, y in zip(m2, m2[1:])), m2
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 3 and sys.argv[2] == "--can-mo-ta":
        print(f"{can_mo_ta(os.path.abspath(sys.argv[1]))} file cần mô tả → CAN-MO-TA.md")
    elif len(sys.argv) == 2:
        moi, bc = chay(os.path.abspath(sys.argv[1]))
        print(f"Trám {len(moi)} cảnh · {sum('CẦN HÌNH' in k for _, _, k in bc)} câu cần hình → TRAM-CANH.md")
    else:
        sys.exit(__doc__)
