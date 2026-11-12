"""Áp một mẫu edit (thu-vien-mau/<thư mục>/mau.json) vào timeline: phong cách, nhịp chuyển cảnh, hiệu ứng âm tự rải.
Chạy trong video-studio:  python3 scripts/ap_mau.py projects/<tên> edit-phim-01      (ghi đè timeline.json, giữ bản .bak)
App studio gọi hàm ap() qua máy chủ (tab Thương hiệu → Mẫu edit), hoàn tác được.
Chữ, phụ đề, zoom, cảnh trám bám theo đoạn video của nó khi độ dài chuyển cảnh đổi. Hiệu ứng âm do mẫu thêm có "auto": true;
áp lại mẫu thì chỉ thay các mục đó, mục Hào tự thêm giữ nguyên."""
import copy, glob, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout
from am_thanh import SFX
from effects import STYLES

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MAU = {m["id"]: m for m in (json.load(open(p, encoding="utf8")) for p in sorted(glob.glob(os.path.join(ROOT, "thu-vien-mau", "*", "mau.json"))))}
TIMED = ("texts", "subtitles", "cards", "zooms", "broll", "sfx")


def ap(tl, mau):
    tl = copy.deepcopy(tl)
    tl["sfx"] = [x for x in tl.get("sfx", []) if not x.get("auto")]
    # 1. ghi nhớ mỗi mục thuộc đoạn video nào (như app studio) trước khi đổi chuyển cảnh
    L0 = layout(tl)
    anchor = []
    for k in TIMED:
        for x in tl.get(k, []):
            c = max([i for i, s in enumerate(L0["starts"]) if x["start"] >= s - 1e-6] or [0])
            anchor.append((x, c, x["start"] - L0["starts"][c]))
    # 2. phong cách, âm thanh, nhịp chuyển cảnh
    tl.setdefault("meta", {}).update(mau.get("meta", {}), mau=mau["id"])
    tl.setdefault("audio", {}).update(mau.get("audio", {}))
    cc = mau.get("chuyen_canh", {})
    if cc.get("chu_ky"):
        ky = cc["chu_ky"]
        tl["transitions"] = [{"type": ky[i % len(ky)], **({"dur": cc["dur"][ky[i % len(ky)]]} if ky[i % len(ky)] in cc.get("dur", {}) else {})}
                             for i in range(len(tl["clips"]) - 1)]
    L1 = layout(tl)
    total = L1["total"]
    for x, c, off in anchor:
        x["start"] = round(max(0, min(L1["starts"][c] + off, total - 0.2)), 2)
        x["dur"] = round(max(0.2, min(x["dur"], total - x["start"])), 2)
    # 3. rải hiệu ứng âm: canh "điểm nhấn" của file âm vào đúng lúc hình chạm
    s = mau.get("sfx", {})
    vol = s.get("vol", {})
    sp = STYLES[tl["meta"].get("style", "hien-dai")]["speed"]
    new = []

    def them(name, t):
        if not name or name not in SFX:
            return
        st = round(max(0.0, t - SFX[name]["diem_nhan"]), 2)
        if st >= total - 0.05 or any(y["file"] == name and abs(y["start"] - st) < 0.25 for y in new):
            return  # không chồng hai tiếng giống nhau quá sát
        new.append({"start": st, "dur": round(min(SFX[name]["dai"], total - st), 2), "file": name,
                    "vol": vol.get(SFX[name]["nhom"], 1.0), "auto": True})

    for t0, d, ty in L1["transitions"]:
        if ty == "cut":
            continue
        them(s.get("chuyen_canh", {}).get(ty), t0 + d / 2)  # giữa chuyển cảnh là lúc hình biến đổi mạnh nhất
        r = s.get("truoc_chuyen_canh", {}).get(ty)
        if r in SFX:
            them(r, t0 + d * 0.3)  # tiếng dồn kết thúc ngay khi chuyển cảnh bắt đầu loé
    for x in tl.get("texts", []):
        kind = x.get("kind", "line")
        hit = x["start"] + (0.25 if kind == "title3d" else 0.3) * sp  # chữ chạm đúng cỡ (theo nhịp hiệu ứng chữ trong dung.py)
        them(s.get("chu", {}).get(kind), hit)
        if kind == "stat":
            them(s.get("so_lieu"), x["start"] + 1.5 * sp)  # số chạy xong
        elif kind == "title3d" and re.search(r"\d", x.get("big", "")):
            them(s.get("so_lieu"), hit + 0.12)
    tl["sfx"] += sorted(new, key=lambda y: y["start"])
    return tl


def _tu_kiem():
    tl = {"version": 1, "meta": {"platform": "tiktok"}, "audio": {"music": "synth", "voice": True},
          "clips": [{"file": "a.mp4", "in": 0, "dur": 4}, {"file": "b.mp4", "in": 0, "dur": 3}, {"file": "c.mp4", "in": 0, "dur": 3}],
          "transitions": [{"type": "cut"}, {"type": "cut"}],
          "texts": [{"kind": "title3d", "start": 0.2, "dur": 2, "top": "chỉ từ", "big": "2.4 TỶ"},
                    {"kind": "line", "start": 4.5, "dur": 2, "lines": ["Cảnh hai"]}],
          "sfx": [{"start": 8.0, "dur": 0.2, "file": "chu_click_01"}]}
    m = MAU["edit-phim-01"]
    out = ap(tl, m)
    assert check(out) == [], check(out)
    assert out["meta"]["style"] == "edit-phim" and out["audio"]["music"] is None and out["audio"]["voice"] is True
    assert [t["type"] for t in out["transitions"]] == ["cut", "gl-CrossZoom"]
    assert out["texts"][1]["start"] == 4.5  # cảnh 2 không đổi chỗ (chuyển cảnh mới nằm sau nó)
    assert any(x["file"] == "chu_click_01" and "auto" not in x for x in out["sfx"]), "giữ mục tự thêm tay"
    files = [x["file"] for x in out["sfx"] if x.get("auto")]
    assert "whoosh_zoom_01" in files and "ting_don_01" in files and files.count("chu_swish-pop_01") == 2, files
    wz = next(x for x in out["sfx"] if x["file"] == "whoosh_zoom_01")
    t0, d, _ = layout(out)["transitions"][1]
    assert abs(wz["start"] + SFX["whoosh_zoom_01"]["diem_nhan"] - (t0 + d / 2)) < 0.02
    again = ap(out, m)  # áp lại: không nhân đôi
    assert len(again["sfx"]) == len(out["sfx"]), (len(again["sfx"]), len(out["sfx"]))
    # chuyển cảnh dài hơn đẩy các cảnh sau: chữ của cảnh 3 phải đi theo
    tl2 = copy.deepcopy(tl); tl2["texts"].append({"kind": "line", "start": 7.5, "dur": 1, "lines": ["Cảnh ba"]})
    out2 = ap(tl2, m)
    assert out2["texts"][2]["start"] == round(7.5 + 0.35, 2), out2["texts"][2]
    print("OK", len(out["sfx"]), "hiệu ứng âm")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    if len(sys.argv) != 3 or sys.argv[2] not in MAU:
        sys.exit(f"Dùng: python3 scripts/ap_mau.py projects/<tên> <mẫu>   (mẫu đang có: {', '.join(MAU)})")
    p = os.path.join(sys.argv[1], "timeline.json")
    out = ap(json.load(open(p, encoding="utf8")), MAU[sys.argv[2]])
    if errs := check(out):
        sys.exit("Áp mẫu ra timeline lỗi:\n- " + "\n- ".join(errs))
    shutil.copy(p, p + ".bak")
    json.dump(out, open(p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"Đã áp mẫu {sys.argv[2]}: {sum(1 for x in out['sfx'] if x.get('auto'))} hiệu ứng âm tự rải. Bản cũ: timeline.json.bak")
