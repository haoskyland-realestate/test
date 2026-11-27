"""Tự xếp clip quay lộn xộn theo kịch bản (Hào chốt 27/11: video thô không theo thứ tự + kịch bản Google Doc).
Nghe lời từng clip (phu_de.nhan_dang, có lưu đệm), so với từng câu "Lời đọc" của KICH-BAN.md (bỏ dấu, độ trùng từ):
- clip xếp theo câu đầu tiên nó nói; một câu quay nhiều lần → giữ lần khớp nhất, ít vấp nhất, các lần còn lại "dự phòng";
- clip không lời (ít hơn kich_ban.tu_toi_thieu từ) → cảnh trám, để tram_canh.py đặt lên câu hợp;
- câu kịch bản không clip nào nói → "thiếu"; clip có lời mà không khớp câu nào → "không khớp" (để cuối, báo Hào).
Không đoán: chỉ xếp lại, mọi chỗ nghi ngờ ghi vào XEP-CANH.md cho Hào duyệt ở cổng 1. Ghi timeline (giữ .bak) + meta.xep_canh.
Chạy TRƯỚC master cut, trong video-studio:  python scripts/xep_canh.py projects/<tên>   ·   tự kiểm: --tu-kiem"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cau_hinh import lay
from kich_ban import bo_dau, tu


def tach(s):
    return [bo_dau(w) for w in tu(s)]


def do_khop(cau, loi):
    """Tỉ lệ từ của câu kịch bản có trong lời clip (0..1)."""
    c = tach(cau)
    return sum(w in loi for w in c) / len(c) if c else 0


def xep(cau, loi_clip, nguong=0.6, toi_thieu=3, vap=None, dai=None):
    """cau: [(stt, lời đọc)]; loi_clip: {file: [từ đã tách]} theo thứ tự clip hiện có; vap: {file: số chỗ vấp}; dai: {file: giây}.
    Trả {"thu_tu": [file…], "du_phong": {file: file thay}, "canh_tram": [file], "khong_khop": [file], "thieu": [stt], "khop": {file: [(stt, %)]}}."""
    vap, dai = vap or {}, dai or {}
    khop, tram, lech = {}, [], []
    for f, ws in loi_clip.items():
        if len(ws) < toi_thieu:
            tram.append(f); continue
        s = set(ws)
        k = [(stt, round(do_khop(c, s), 2)) for stt, c in cau]
        k = [x for x in k if x[1] >= nguong]
        if k:
            khop[f] = k
        else:  # không khớp câu nào: ít lời (< 8 từ, thường là máy "nghe" nhạc/tiếng gió thành chữ) → cảnh trám; nhiều lời → hỏi Hào
            (tram if len(ws) < 8 else lech).append(f)
    # nhiều lần quay cùng câu: trong các lần khớp gần bằng lần khớp nhất (kém ≤ 10%), giữ lần ít vấp nhất rồi NGẮN nhất
    # (cùng nội dung thì ngắn hơn là ít ngập ngừng/nói lặp: máy nhận dạng thường bỏ qua chỗ lặp nên không thấy vấp trong chữ)
    theo_cau, du_phong = {}, {}
    for f, k in khop.items():
        theo_cau.setdefault(k[0][0], []).append(f)
    giu = []
    for stt, fs in theo_cau.items():
        tb = {f: sum(p for _, p in khop[f]) / len(khop[f]) for f in fs}
        du = [f for f in fs if tb[f] >= max(tb.values()) - 0.1]
        tot = min(du, key=lambda f: (vap.get(f, 0), dai.get(f, 0), -tb[f], f))
        giu.append(tot)
        du_phong.update({f: tot for f in fs if f != tot})
    stt_thu = {stt: i for i, (stt, _) in enumerate(cau)}
    giu.sort(key=lambda f: (stt_thu[khop[f][0][0]], f))
    co = {stt for f in giu for stt, _ in khop[f]}
    return {"thu_tu": giu, "du_phong": du_phong, "canh_tram": tram, "khong_khop": lech,
            "thieu": [stt for stt, _ in cau if stt not in co], "khop": {f: khop[f] for f in giu}}


def bao_cao(kq, cau):
    noi = dict(cau)
    md = ["# Xếp clip theo kịch bản", "", "Máy xếp theo lời nói khớp với cột \"Lời đọc\" của KICH-BAN.md. Hào xem, sai chỗ nào thì nói Claude đổi.", "",
          "| Thứ tự | Clip | Câu kịch bản nói trong clip (độ khớp) |", "|---|---|---|"]
    md += [f"| {i} | {f} | " + ", ".join(f"câu {s} ({int(p * 100)}%)" for s, p in kq["khop"][f]) + " |" for i, f in enumerate(kq["thu_tu"], 1) if f in kq["khop"]]
    if kq["thieu"]:
        md += ["", "## Câu chưa có clip nào nói (CẦN HỎI HÀO: quay thêm, bỏ câu, hay trám bằng hình/chữ)"] + [f"- câu {s}: {noi[s]}" for s in kq["thieu"]]
    if kq["du_phong"]:
        md += ["", "## Lần quay dự phòng (cùng câu, máy chọn lần khớp nhất/ít vấp nhất)"] + [f"- {f} → dùng {g}" for f, g in kq["du_phong"].items()]
    if kq["khong_khop"]:
        md += ["", "## Clip có lời nhưng không khớp câu nào (CHƯA đưa vào video, CẦN HỎI HÀO: thêm câu vào kịch bản hay bỏ)"] + [f"- {f}" for f in kq["khong_khop"]]
    if kq["canh_tram"]:
        md += ["", "## Clip không lời → cảnh trám (tram_canh.py đặt lên câu hợp)"] + [f"- {f}" for f in kq["canh_tram"]]
    return "\n".join(md) + "\n"


def chay(pj):
    from doi_chieu import doc_kich_ban
    import phu_de, phan_tich_loi
    T = os.path.join(pj, "timeline.json")
    tl = json.load(open(T, encoding="utf8"))
    cau = [(stt, loi) for stt, loi, _ in doc_kich_ban(pj) if loi.strip("() ") and not loi.startswith("(")]
    if not cau:
        sys.exit("KICH-BAN.md chưa có cột \"Lời đọc\": chạy kich_ban_doc.py <dự án> <link Google Doc> trước.")
    B, tv = os.path.join(pj, "build"), tl.get("meta", {}).get("tu_vung")
    loi, vap, dai = {}, {}, {}
    for c in tl["clips"]:
        f = c["file"]
        if f in loi:
            continue
        raw = os.path.join(B, "raw", f)
        print(f"Nghe lời: {f}", flush=True)
        ws = phu_de.sua_tu(phu_de.nhan_dang(raw, phu_de.file_dem(B, f, tv, tl), tv, tl), tl.get("meta", {}).get("sua_tu"))
        loi[f] = [w for x in ws for w in tach(x[0])]
        dai[f] = c["dur"] if c.get("in", 0) == 0 else dai.get(f, c["dur"])
        vap[f] = len(phan_tich_loi.vap(ws)) + len(phan_tich_loi.lap(ws)) if ws else 0
    kq = xep(cau, loi, lay("kich_ban.nguong_khop", tl), lay("kich_ban.tu_toi_thieu", tl), vap, dai)
    theo = {c["file"]: c for c in tl["clips"]}
    shutil.copy(T, T + ".bak")
    tl["clips"] = [theo[f] for f in kq["thu_tu"]]
    tl["transitions"] = [{"type": "cut"} for _ in tl["clips"][1:]]
    tl.setdefault("meta", {})["xep_canh"] = {k: kq[k] for k in ("du_phong", "canh_tram", "khong_khop", "thieu")}
    json.dump(tl, open(T, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    open(os.path.join(pj, "XEP-CANH.md"), "w", encoding="utf8").write(bao_cao(kq, cau))
    return kq


def _tu_kiem():
    cau = [(1, "Chào anh chị, em là Hùng ở Saigon Park."), (2, "Dự án rộng tám trăm héc ta."), (3, "Có hai phân khu chính."),
           (4, "Giá dự kiến năm hai không hai bảy."), (5, "Câu này chưa quay.")]
    w = lambda s: tach(s)
    loi = {"IMG_3.MOV": w("có hai phân khu chính giá dự kiến năm hai không hai bảy"),   # một clip nói 2 câu
           "IMG_1.MOV": w("chào anh chị em là Hùng ở Saigon Park"),
           "flycam.mp4": w("ừ"),                                                     # không lời → trám
           "IMG_2a.MOV": w("dự án rộng tám trăm"), "IMG_2b.MOV": w("dự án rộng tám trăm héc ta"),   # câu 2 quay 2 lần
           "IMG_9.MOV": w("hôm nay trời đẹp quá đi thôi mình đi chơi đâu đây nhỉ"),  # nhiều lời, không khớp → hỏi Hào
           "nhac.mp4": w("Where are you")}                                          # máy "nghe" nhạc thành chữ → trám
    kq = xep(cau, loi, vap={"IMG_2b.MOV": 0, "IMG_2a.MOV": 2})
    assert kq["thu_tu"] == ["IMG_1.MOV", "IMG_2b.MOV", "IMG_3.MOV"], kq["thu_tu"]   # IMG_9 không khớp: không đưa vào video
    assert kq["du_phong"] == {"IMG_2a.MOV": "IMG_2b.MOV"} and kq["canh_tram"] == ["flycam.mp4", "nhac.mp4"] and kq["khong_khop"] == ["IMG_9.MOV"], kq
    assert kq["thieu"] == [5] and [s for s, _ in kq["khop"]["IMG_3.MOV"]] == [3, 4], kq
    # lần quay khớp ngang nhau: chọn lần ít vấp hơn
    kq = xep(cau[:1], {"a": w(cau[0][1]), "b": w(cau[0][1])}, vap={"a": 0, "b": 3})
    assert kq["thu_tu"] == ["a"] and kq["du_phong"] == {"b": "a"}, kq
    # chữ y hệt, không thấy vấp (máy bỏ qua chỗ lặp): chọn lần ngắn hơn
    kq = xep(cau[:1], {"a": w(cau[0][1]), "z": w(cau[0][1])}, dai={"a": 5.2, "z": 4.0})
    assert kq["thu_tu"] == ["z"], kq
    md = bao_cao(xep(cau, loi), cau)
    assert "câu 5: Câu này chưa quay." in md and "flycam.mp4" in md and "IMG_9.MOV" in md
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2:
        kq = chay(os.path.abspath(sys.argv[1]))
        print(f"Xếp {len(kq['thu_tu'])} clip · {len(kq['canh_tram'])} cảnh trám · thiếu {len(kq['thieu'])} câu · "
              f"không khớp {len(kq['khong_khop'])} → XEP-CANH.md")
    else:
        sys.exit(__doc__)
