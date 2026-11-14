"""Lưu chỉnh sửa vào mẫu: Hào chỉnh một video (chuyển cảnh, âm lượng, phong cách) cho đến khi ưng, rồi rút công thức đó thành một mẫu mới
trong thu-vien-mau/ để video sau áp mẫu là đã đúng. Mặc định tạo BẢN MỚI (<mẫu>-chinh-N), mẫu gốc giữ nguyên; --ghi-de mới ghi lên mẫu gốc (giữ mau.json.bak).
Chạy trong video-studio:  python3 scripts/luu_vao_mau.py projects/<tên> [--ten "Tên mẫu"] [--ghi-de]      ·   tự kiểm: --tu-kiem
Lưu được: phong cách (meta.style/look), nhịp và độ dài chuyển cảnh, âm lượng hiệu ứng âm theo nhóm, nhạc nền/whoosh.
CHƯA lưu được (mẫu chưa có chỗ chứa): kiểu và tốc độ chữ, cỡ chữ, vị trí chữ, zoom. Phần đó báo lại để Claude Code làm thêm."""
import copy, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from am_thanh import SFX
import ap_mau

ROOT = ap_mau.ROOT
CHUA_LUU = "kiểu/tốc độ/cỡ/vị trí chữ và zoom (mẫu chưa có chỗ chứa)"


def chu_ky(types):
    """Chuỗi chuyển cảnh ngắn nhất lặp lại được thành đúng chuỗi của video (tối đa 10); không lặp thì lấy 10 đầu."""
    for p in range(1, min(len(types), 10) + 1):
        if all(types[i] == types[i % p] for i in range(len(types))):
            return types[:p]
    return types[:10]


def rut(tl, goc=None):
    """Trả (mẫu mới dạng dict, danh sách thay đổi so với mẫu gốc)."""
    base = copy.deepcopy(goc or {})
    m, bao = copy.deepcopy(base), []
    meta = {k: v for k, v in tl.get("meta", {}).items() if k in ("style", "look")}
    if meta and meta != {k: v for k, v in base.get("meta", {}).items() if k in meta}:
        bao.append(f"phong cách: {base.get('meta', {}).get('style', '—')} → {meta.get('style', base.get('meta', {}).get('style'))}")
    m["meta"] = {**base.get("meta", {}), **meta}
    a = {k: v for k, v in tl.get("audio", {}).items() if k in ("whoosh", "music") and (k != "music" or v in (None, "synth"))}
    if a and a != {k: base.get("audio", {}).get(k) for k in a}:
        bao.append("âm nền: " + ", ".join(f"{k}={v}" for k, v in a.items()))
    m["audio"] = {**base.get("audio", {}), **a}
    tr = tl.get("transitions", [])
    if tr:
        ky = chu_ky([t.get("type", "cut") for t in tr])
        dur = {t["type"]: t["dur"] for t in tr if t.get("type") != "cut" and "dur" in t}
        if ky != base.get("chuyen_canh", {}).get("chu_ky") or dur != base.get("chuyen_canh", {}).get("dur", {}):
            bao.append(f"chuyển cảnh: {len(ky)} bước lặp ({', '.join(ky)})")
        m["chuyen_canh"] = {"chu_ky": ky, "dur": dur}
    nhom = {}
    for x in tl.get("sfx", []):
        if x.get("file") in SFX:
            nhom.setdefault(SFX[x["file"]]["nhom"], []).append(x.get("vol", 1.0))
    vol = dict(base.get("sfx", {}).get("vol", {}))
    for g, v in nhom.items():
        tb = round(sum(v) / len(v), 2)
        if abs(tb - vol.get(g, 1.0)) > 0.02:
            bao.append(f"âm lượng nhóm {g}: {vol.get(g, 1.0)} → {tb}")
        vol[g] = tb
    m.setdefault("sfx", {})["vol"] = vol
    return m, bao


def luu(tl, ten=None, ghi_de=False):
    """Ghi mẫu. Trả {id, thu_muc, bao, chua_luu}. Không có mẫu gốc (video chưa áp mẫu nào) thì mẫu mới dựng từ phần chỉnh."""
    gid = tl.get("meta", {}).get("mau")
    goc = ap_mau.MAU.get(gid)
    m, bao = rut(tl, {k: v for k, v in goc.items() if k != "_dir"} if goc else None)
    if goc and ghi_de:
        p = os.path.join(goc["_dir"], "mau.json")
        os.replace(p, p + ".bak")
        m["id"] = gid
        d = goc["_dir"]
    else:
        stem = gid or "mau"
        n = 1
        while f"{stem}-chinh-{n}" in ap_mau.MAU or os.path.exists(os.path.join(ROOT, "thu-vien-mau", f"{stem}-chinh-{n}_chinh-tay")):
            n += 1
        m["id"] = f"{stem}-chinh-{n}"
        m["ten"] = ten or ((goc or {}).get("ten", "Mẫu") + f" (chỉnh {n})")
        m["nguon"] = f"Rút từ video Hào đã chỉnh, mẫu gốc: {gid or 'không có'}"
        d = os.path.join(ROOT, "thu-vien-mau", f"{m['id']}_chinh-tay")
        os.makedirs(d)
    if ten and ghi_de:
        m["ten"] = ten
    json.dump(m, open(os.path.join(d, "mau.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    if not ghi_de or not os.path.exists(os.path.join(d, "MAU.md")):
        open(os.path.join(d, "MAU.md"), "w", encoding="utf8").write(
            f"# {m.get('ten', m['id'])}\n\nRút từ video Hào đã chỉnh. Mẫu gốc: {gid or 'không có'}.\n\nThay đổi so với mẫu gốc:\n" + ("\n".join(f"- {b}" for b in bao) or "- (không đổi gì)") + f"\n\nChưa lưu được: {CHUA_LUU}.\n")
    ap_mau.MAU[m["id"]] = dict(m, _dir=d)
    return {"id": m["id"], "thu_muc": os.path.relpath(d, ROOT), "bao": bao, "chua_luu": CHUA_LUU}


def _tu_kiem():
    import tempfile
    tl = {"meta": {"style": "edit-phim", "mau": "edit-phim-01"}, "audio": {"music": None, "whoosh": False},
          "clips": [], "transitions": [{"type": t, **({"dur": 0.5} if t != "cut" else {})} for t in ["cut", "gl-FilmBurn", "cut"] * 4],
          "sfx": [{"file": "whoosh_nhanh_01", "vol": 0.2, "start": 0, "dur": 0.4}]}
    assert chu_ky(["a", "b", "a", "b", "a"]) == ["a", "b"] and chu_ky(list("abcdefghijkl"))[:3] == ["a", "b", "c"]
    m, bao = rut(tl, {k: v for k, v in ap_mau.MAU["edit-phim-01"].items() if k != "_dir"})
    assert m["chuyen_canh"]["chu_ky"] == ["cut", "gl-FilmBurn", "cut"] and m["chuyen_canh"]["dur"] == {"gl-FilmBurn": 0.5}, m["chuyen_canh"]
    assert m["sfx"]["vol"][SFX["whoosh_nhanh_01"]["nhom"]] == 0.2 and any("âm lượng" in b for b in bao), bao
    assert m["sfx"]["chuyen_canh"] == ap_mau.MAU["edit-phim-01"]["sfx"]["chuyen_canh"]  # phần không chỉnh giữ nguyên
    real = ap_mau.ROOT
    with tempfile.TemporaryDirectory() as t:
        ap_mau.ROOT = globals()["ROOT"] = t
        os.makedirs(os.path.join(t, "thu-vien-mau"))
        r = luu(tl)
        assert r["id"] == "edit-phim-01-chinh-1" and os.path.exists(os.path.join(t, r["thu_muc"], "mau.json")), r
        assert luu(tl)["id"] == "edit-phim-01-chinh-2"
        ap_mau.ROOT = globals()["ROOT"] = real
    ap_mau.MAU.pop("edit-phim-01-chinh-1", None); ap_mau.MAU.pop("edit-phim-01-chinh-2", None)
    assert not os.path.exists(os.path.join(real, "thu-vien-mau", "edit-phim-01-chinh-1_chinh-tay")), "ghi nhầm vào kho thật"
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
        pj = os.path.abspath(sys.argv[1])
        tl = json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8"))
        ten = sys.argv[sys.argv.index("--ten") + 1] if "--ten" in sys.argv else None
        r = luu(tl, ten, "--ghi-de" in sys.argv)
        print(f"Đã lưu mẫu {r['id']} ({r['thu_muc']})"); [print(" -", b) for b in r["bao"]]; print("Chưa lưu được:", r["chua_luu"])
    else:
        sys.exit(__doc__)
