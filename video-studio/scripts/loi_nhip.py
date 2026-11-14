"""Chữ theo nhịp lời nói (kiểu video mẫu Open Residency): từng từ hiện đúng lúc người nói, gom thành cụm ≤5 từ, từ khoá (số, tiền, tên riêng,
từ trong meta.tu_khoa) đỏ phát sáng. Thay phụ đề thường khi dùng (thay_phu_de). Chữ do công cụ đặt có "auto_loi": true; chạy lại chỉ thay các khối đó.
Chạy trong video-studio (sau khi dựng một lần để có build/voice.wav):  python3 scripts/loi_nhip.py projects/<tên> [--giu-phu-de] [--ngang-nguc]
    --ngang-nguc: đặt cụm chữ ngang ngực người nói (bộ dựng tìm đỉnh đầu rồi cộng xuống), thay cho vị trí cố định.      ·   tự kiểm: --tu-kiem
shortcut: "bám người" mới là ĐẶT THEO VỊ TRÍ ĐẦU TẠI LÚC CỤM BẮT ĐẦU, chưa bám từng khung hình; người đi lại nhiều thì chữ không theo."""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TIEN = {"tỷ", "triệu", "nghìn", "ngàn", "%", "phần", "trăm"}
NGHI = 0.4  # nghỉ dài hơn 0,4 giây thì sang cụm mới


def la_khoa(w, tu_khoa):
    t = re.sub(r"[^\wÀ-ỹ%]", "", w.lower())
    return bool(re.search(r"\d", t) or t in TIEN or t in tu_khoa)


def nhom(words, tu_khoa=(), toi_da=5, nghi=NGHI):
    """words: [[từ, bắt đầu, kết thúc]] → danh sách khối chữ kiểu 'loi'."""
    tk = {re.sub(r"[^\wÀ-ỹ%]", "", t.lower()) for t in tu_khoa}
    cum, out = [], []

    def dong():
        if cum:
            a, b = cum[0][1], cum[-1][2]
            out.append({"kind": "loi", "start": round(max(0, a - 0.05), 2), "dur": round(b - a + 0.5, 2), "words": [list(w) for w in cum],
                        "hl": [k for k, w in enumerate(cum) if la_khoa(w[0], tk)], "auto_loi": True})
            cum.clear()
    for k, w in enumerate(words):
        if cum and (len(cum) >= toi_da or w[1] - cum[-1][2] > nghi or re.search(r"[.?!]$", cum[-1][0])):
            dong()
        cum.append(w)
    dong()
    for k in range(len(out) - 1):  # cụm sau bắt đầu thì cụm trước hết, không chồng chữ
        out[k]["dur"] = round(min(out[k]["dur"], max(0.3, out[k + 1]["start"] - out[k]["start"])), 2)
    return out


def dat(tl, words, giu_phu_de=False, ngang_nguc=False):
    tl = json.loads(json.dumps(tl))
    total = sum(c["dur"] for c in tl["clips"])
    tl["texts"] = [x for x in tl.get("texts", []) if not x.get("auto_loi")]
    moi = nhom(words, tl.get("meta", {}).get("tu_khoa", []))
    for x in moi:
        x["start"] = round(min(x["start"], total - 0.1), 2)
        x["dur"] = round(max(0.1, min(x["dur"], total - x["start"])), 2)
        if ngang_nguc:
            x["bam_nguoi"] = True
    tl["texts"] += moi
    if not giu_phu_de:
        tl["subtitles"] = [x for x in tl.get("subtitles", []) if not x.get("auto")]
    return tl, len(moi)


def _tu_kiem():
    w = [["Đây", 0.2, 0.4], ["là", 0.4, 0.5], ["77", 0.6, 1.0], ["tỷ", 1.0, 1.3], ["một", 2.5, 2.7], ["căn.", 2.7, 3.0], ["Hào", 3.1, 3.3]]
    g = nhom(w, ["Hào"])
    assert len(g) == 3 and g[0]["hl"] == [2, 3] and g[2]["hl"] == [0], g          # nghỉ 1,2 giây → cụm mới; sau dấu chấm → cụm mới; tên riêng đỏ
    assert g[0]["dur"] <= g[1]["start"] - g[0]["start"] + 1e-6, g                  # không chồng cụm
    tl = {"version": 1, "meta": {}, "audio": {}, "clips": [{"file": "a.mp4", "in": 0, "dur": 3.2}], "transitions": [], "subtitles": [{"start": 0, "dur": 1, "text": "x", "auto": True}]}
    out, n = dat(tl, w)
    from timeline import check
    assert n == 3 and out["subtitles"] == [] and check(out) == [], check(out)
    out2, _ = dat(out, w)
    assert len([x for x in out2["texts"] if x.get("auto_loi")]) == 3                # chạy lại không nhân đôi
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) >= 2 and os.path.isdir(sys.argv[1]):
        pj = os.path.abspath(sys.argv[1])
        from phu_de import nhan_dang, file_dem
        tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
        va = os.path.join(pj, "build", "voice.wav")
        if not os.path.exists(va):
            sys.exit("Chưa có build/voice.wav: dựng nháp một lần (dung.py --nhap) rồi chạy lại.")
        words = nhan_dang(va, file_dem(os.path.join(pj, "build"), "voice.wav", tl.get("meta", {}).get("tu_vung")), tl.get("meta", {}).get("tu_vung"))
        out, n = dat(tl, words, "--giu-phu-de" in sys.argv, "--ngang-nguc" in sys.argv)
        import shutil; shutil.copy(os.path.join(pj, "timeline.json"), os.path.join(pj, "timeline.json.bak"))
        json.dump(out, open(os.path.join(pj, "timeline.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
        print(f"Đã đặt {n} cụm chữ theo nhịp nói ({len(words)} từ). Bản cũ: timeline.json.bak")
    else:
        sys.exit(__doc__)
