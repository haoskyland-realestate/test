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
MAU = {m["id"]: dict(m, _dir=os.path.dirname(p)) for p in sorted(glob.glob(os.path.join(ROOT, "thu-vien-mau", "*", "mau.json")))
       for m in [json.load(open(p, encoding="utf8"))]}
TIMED = ("texts", "subtitles", "cards", "zooms", "broll", "sfx")


def ap(tl, mau, chi_am=False):
    """chi_am=True: chỉ rải lại hiệu ứng âm (giữ phong cách và chuyển cảnh Hào đã chỉnh), dùng khi chữ vừa đổi."""
    tl = copy.deepcopy(tl)
    tl["sfx"] = [x for x in tl.get("sfx", []) if not x.get("auto")]
    tl["zooms"] = [z for z in tl.get("zooms", []) if not z.get("mau")]  # zoom do mẫu thêm; zoom của master cut ("auto") giữ
    # 1. ghi nhớ mỗi mục thuộc đoạn video nào (như app studio) trước khi đổi chuyển cảnh
    L0 = layout(tl)
    anchor = []
    for k in TIMED:
        for x in tl.get(k, []):
            c = max([i for i, s in enumerate(L0["starts"]) if x["start"] >= s - 1e-6] or [0])
            anchor.append((x, c, x["start"] - L0["starts"][c]))
    # 2. phong cách, âm thanh, nhịp chuyển cảnh
    if not chi_am:
        tl.setdefault("meta", {}).update(mau.get("meta", {}), mau=mau["id"])
        tl.setdefault("audio", {}).update(mau.get("audio", {}))
    cc = mau.get("chuyen_canh", {})
    if cc.get("chu_ky") and not chi_am:
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

    def them(name, t, vol_=None, pitch=1.0, hp=None, cach=0.25):
        if not name or name not in SFX:
            return
        st = round(max(0.0, t - SFX[name]["diem_nhan"]), 2)
        if st >= total - 0.05 or any(y["file"] == name and abs(y["start"] - st) < cach for y in new):
            return  # không chồng hai tiếng giống nhau quá sát
        new.append({"start": st, "dur": round(min(SFX[name]["dai"], total - st), 2), "file": name,
                    "vol": vol_ if vol_ is not None else vol.get(SFX[name]["nhom"], 1.0), "auto": True,
                    **({"pitch": pitch} if pitch != 1.0 else {}), **({"hp": hp} if hp else {})})

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
    # 3b. thiết kế âm theo nhịp chữ (mẫu có "nhip_chu"): vào (vút, đỉnh trùng lúc chữ chạm) → chạm (ở trên) → trầm (chữ mở đầu, số lớn)
    #     → lấp lánh (số tiền, %) → ra (rất nhỏ, bỏ nếu chữ sau tới sát). Đổi cao độ ±4% luân phiên, lọc trầm tiếng vút.
    nc = mau.get("nhip_chu")
    if nc:
        v = nc.get("vol", {})
        ds = sorted((x for x in tl.get("texts", []) if x.get("kind", "line") in ("title3d", "hook", "stat", "tag", "line")), key=lambda x: x["start"])
        for k, x in enumerate(ds):
            kind = x.get("kind", "line")
            hit = x["start"] + (0.25 if kind in ("title3d", "tag") else 0.3) * sp
            pitch = (1.0, 0.96, 1.04)[k % 3]
            so = bool(re.search(r"\d", x.get("big", "") + json.dumps(x.get("o", {}), ensure_ascii=False)))
            them(nc.get("vao"), hit, v.get("vao", .45), pitch, hp=150, cach=0.4)
            if k == 0 or kind == "hook" or (so and re.search(r"tỷ|tỉ|triệu|%", (x.get("big", "") + json.dumps(x.get("o", {}), ensure_ascii=False)).lower())):
                them(nc.get("tram"), hit, v.get("tram", .55), cach=0.6)
            if so and nc.get("lap_lanh"):  # lấp lánh thay tiếng ting số liệu (hai tiếng ting chồng nhau nghe rối)
                new[:] = [y for y in new if not (y["file"] == s.get("so_lieu") and abs(y["start"] - hit) < 0.4)]
                them(nc.get("lap_lanh"), hit + 0.08, v.get("lap_lanh", .3), pitch)
            ra = x["start"] + x["dur"] - 0.2 * sp
            if k + 1 >= len(ds) or ds[k + 1]["start"] - ra > 0.6:
                them(nc.get("ra"), ra, v.get("ra", .22), pitch, hp=200, cach=0.4)
    tl["sfx"] += sorted(new, key=lambda y: y["start"])
    # 4. zoom nhấn ý đúng lúc chữ lớn hiện (xen_ke: cách một chữ một zoom → khung gần/xa xen kẽ)
    zc = mau.get("zoom_chu")
    if zc:
        k = 0
        for x in sorted(tl.get("texts", []), key=lambda x: x["start"]):
            if x.get("kind") not in ("title3d", "compare", "stat"):
                continue
            k += 1
            if zc.get("xen_ke") and k % 2 == 0:
                continue
            st = round(x["start"] + 0.1, 2)
            du = round(min(zc.get("dur", 1.2), x["dur"], total - st), 2)
            if du > 0.3 and not any(z["start"] < st + du and st < z["start"] + z["dur"] for z in tl["zooms"]):
                tl["zooms"].append({"start": st, "dur": du, "scale": zc.get("scale", 1.08), "mau": True})
        tl["zooms"].sort(key=lambda z: z["start"])
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
    # mẫu có nhip_chu: tiếng lấp lánh thay tiếng ting số liệu ở chữ có số
    assert "whoosh_zoom_01" in files and "ting_lap-lanh_01" in files and "ting_don_01" not in files and files.count("chu_swish-pop_01") == 2, files
    wz = next(x for x in out["sfx"] if x["file"] == "whoosh_zoom_01")
    t0, d, _ = layout(out)["transitions"][1]
    assert abs(wz["start"] + SFX["whoosh_zoom_01"]["diem_nhan"] - (t0 + d / 2)) < 0.02
    again = ap(out, m)  # áp lại: không nhân đôi
    assert len(again["sfx"]) == len(out["sfx"]), (len(again["sfx"]), len(out["sfx"]))
    # chuyển cảnh dài hơn đẩy các cảnh sau: chữ của cảnh 3 phải đi theo
    tl2 = copy.deepcopy(tl); tl2["texts"].append({"kind": "line", "start": 7.5, "dur": 1, "lines": ["Cảnh ba"]})
    out2 = ap(tl2, m)
    assert out2["texts"][2]["start"] == round(7.5 + 0.35, 2), out2["texts"][2]
    # nhịp chữ: tiếng vút có đỉnh đúng lúc chữ chạm, đập trầm chỉ ở chữ đầu và chữ có tiền, cao độ luân phiên
    vz = [x for x in out["sfx"] if x["file"] == "whoosh_nhanh_01"]
    hit0 = 0.2 + 0.25 * STYLES["edit-phim"]["speed"]
    assert vz and abs(vz[0]["start"] + SFX["whoosh_nhanh_01"]["diem_nhan"] - hit0) < 0.02 and vz[0]["hp"] == 150, vz
    assert len([x for x in out["sfx"] if x["file"] == "impact_tram_01"]) == 1  # chữ đầu "2.4 TỶ"; chữ "Cảnh hai" không có
    assert any(x["file"] == "ting_lap-lanh_01" for x in out["sfx"]) and any(x.get("pitch") == 0.96 for x in out["sfx"])
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
