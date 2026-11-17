"""Đạo diễn màu: đo từng cảnh → kế hoạch màu → mỗi cảnh một LUT .cube → kiểm lại bằng số. Chỉ dùng numpy, OpenCV, ffmpeg.
Chạy trong video-studio:
  python3 scripts/chinh_mau.py projects/<tên>                       đo + lập kế hoạch + ảnh trước/sau (CHƯA đụng timeline)
  python3 scripts/chinh_mau.py projects/<tên> --mau <ảnh/video mẫu>  lấy phong cách màu từ video/ảnh mẫu
  python3 scripts/chinh_mau.py projects/<tên> --phong-cach sang-trong --chuan 3 --do-manh 0.7
  python3 scripts/chinh_mau.py projects/<tên> --ap                  Hào duyệt xong: ghi "look": "lut:mau/cNN.cube" vào timeline (giữ .bak)
  python3 scripts/chinh_mau.py --tu-kiem
Ra: projects/<tên>/mau/ (cNN.cube, ke-hoach.json sửa tay được rồi chạy lại với --tu-file, truoc-sau.jpg) + MAU-SAC.md.
Quy trình (học từ agentic-color-grader, MIT; ý "chữ ký màu" từ Colourway, MIT; mã tự viết):
  1. sửa lỗi từng cảnh (ám màu đo trên vùng trắng/xám, sáng tối, cháy) → 2. khớp các cảnh về cảnh chuẩn →
  3. phủ phong cách (có sẵn hoặc đọc từ video mẫu) → 4. giữ màu da và trắng nội thất → 5. đo lại, báo lệch."""
import argparse, json, os, shutil, subprocess, sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mau import chuyen_tong

N_LUT = 33
# Phong cách có sẵn: tint (a, b) cho vùng tối / sáng (đơn vị Lab), nhân độ rực, tương phản (S-curve 0..0.3), độ sáng giữa mong muốn
PHONG_CACH = {
    "tu-nhien": {"vi": "Tự nhiên: chỉ sửa lỗi và đồng nhất, không phủ màu", "toi": (0, 0), "sang": (0, 0), "sat": 1.0, "tuong_phan": 0.05, "p50": None},
    "sang-trong": {"vi": "Sang trọng (nhà mẫu cao cấp): trắng sạch hơi ấm, đen sâu vừa, ít rực, vật liệu giữ thật",
                   "toi": (0, -1.0), "sang": (0.5, 2.5), "sat": 0.95, "tuong_phan": 0.12, "p50": None},
    "am-ap": {"vi": "Ấm áp (gia đình, nắng chiều): vùng sáng vàng ấm, vùng tối trung tính", "toi": (0.5, 0.5), "sang": (1.5, 5.0), "sat": 1.0,
              "tuong_phan": 0.08, "p50": None},
    "hien-dai-mat": {"vi": "Hiện đại mát (căn hộ, văn phòng): vùng tối hơi xanh, trắng trung tính, tương phản rõ",
                     "toi": (-1.0, -3.0), "sang": (0, 0.5), "sat": 0.97, "tuong_phan": 0.16, "p50": None},
    "dien-anh": {"vi": "Điện ảnh nhẹ: vùng tối xanh ngọc, vùng sáng ấm, vẫn giữ da", "toi": (-3.0, -4.0), "sang": (1.5, 4.0), "sat": 0.95,
                 "tuong_phan": 0.18, "p50": None},
}
DA = {"sat": (35, 50), "hue": (12, 24)}  # da người: độ rực HSV %, sắc độ ° (GHI-NHO-NGHIEM-THU.md)


# ---------- đo ----------
def lay_khung(path, t, w=360):
    """Một khung RGB 0..1 (đã chuyển tông HDR như bộ dựng)."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{max(0, t):.2f}", "-i", path, "-frames:v", "1", "-vf",
                          chuyen_tong(path) + f"scale={w}:-2,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    if not raw:
        return None
    return np.frombuffer(raw, np.uint8).reshape(-1, w, 3).astype(np.float32) / 255


def lab(rgb):
    return cv2.cvtColor(np.ascontiguousarray(rgb, np.float32), cv2.COLOR_RGB2LAB)


_MAT = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def vung_da(rgb):
    """Điểm ảnh giữa mặt người nói (mặt lớn nhất), hoặc None."""
    g = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    f = _MAT.detectMultiScale(g, 1.1, 6, minSize=(24, 24))
    if len(f) == 0:
        return None
    x, y, w, h = max(f, key=lambda r: r[2])
    return rgb[y + h // 4:y + 3 * h // 4, x + w // 4:x + 3 * w // 4].reshape(-1, 3)


def do(frames):
    """Số đo của một cảnh (gộp các khung). Y: độ sáng 0..1; ám: a, b Lab của vùng trắng/xám (0 = trung tính)."""
    px = np.concatenate([f.reshape(-1, 3) for f in frames])
    y = px @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    L = lab(px.reshape(-1, 1, 3)).reshape(-1, 3)
    c = np.hypot(L[:, 1], L[:, 2])
    neu = (c < 12) & (L[:, 0] > 30) & (L[:, 0] < 97)
    # ứng viên trắng/xám để cân trắng: ít màu nhất trong vùng sáng vừa (cả khi cảnh ám nặng, không còn điểm nào chroma < 12)
    vung = (L[:, 0] > 30) & (L[:, 0] < 97)
    ung = vung & (c <= np.percentile(c[vung], 30)) if vung.sum() > 100 else np.ones(len(L), bool)
    base = L[ung]
    hsv = cv2.cvtColor(px.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3)
    out = {"p5": float(np.percentile(y, 5)), "p50": float(np.percentile(y, 50)), "p95": float(np.percentile(y, 95)),
           "chay": float((y > 0.985).mean() * 100), "thieu": float((y < 0.02).mean() * 100),
           "am_a": float(base[:, 1].mean()), "am_b": float(base[:, 2].mean()), "trung_tinh": float(neu.mean() * 100),
           "rgb_trang": [float(v) for v in px[ung].mean(0)],
           "ruc": float(hsv[:, 1].mean() * 100)}
    da = [d for d in (vung_da(f) for f in frames) if d is not None]
    if da:
        d = np.concatenate(da)
        h = cv2.cvtColor(d.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3)
        hue, sat = float(np.median(h[:, 0])), float(h[:, 1].mean() * 100)
        if hue <= 45 and sat >= 15:  # nhận nhầm (gáy, đồ vật) thì bỏ
            out.update(da_hue=hue, da_sat=sat)
    return out


def chu_ky(frames):
    """Chữ ký màu của video/ảnh mẫu: phân vị sáng, tint vùng tối/giữa/sáng (Lab a, b), độ rực."""
    px = np.concatenate([f.reshape(-1, 3) for f in frames])
    L = lab(px.reshape(-1, 1, 3)).reshape(-1, 3)
    lo, hi = np.percentile(L[:, 0], [33, 66])
    band = lambda m: (float(L[m, 1].mean()), float(L[m, 2].mean())) if m.sum() else (0.0, 0.0)
    d = do(frames)
    return {**{k: d[k] for k in ("p5", "p50", "p95", "ruc")}, "toi": band(L[:, 0] < lo), "giua": band((L[:, 0] >= lo) & (L[:, 0] < hi)),
            "sang": band(L[:, 0] >= hi)}


# ---------- biến đổi màu (áp lên lưới LUT hoặc ảnh) ----------
def bien_doi(rgb, k):
    """k: thông số một cảnh (xem ke_hoach). Trả (ảnh sau sửa lỗi + khớp, ảnh cuối có phong cách và giữ da)."""
    x = np.clip(rgb * np.array(k["gain"], np.float32), 0, 1)                    # cân trắng
    # sáng tối, nén cháy, tương phản: chỉnh trên độ sáng Y rồi nhân cả 3 kênh theo tỉ lệ → không làm da rực thêm
    Y = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    y = Y ** k["gamma"]
    if k["goi"] < 1:
        t = k["goi"]
        y = np.where(y > t, t + (1 - t) * np.tanh((y - t) / (1 - t)), y)
    s = k["tuong_phan"]
    if s:  # đường cong chữ S: trộn với smoothstep (luôn đơn điệu, giữ 0 và 1)
        y = (1 - s) * y + s * y * y * (3 - 2 * y)
    x = x * (y / np.maximum(Y, 1e-4))[..., None]
    mx = x.max(-1, keepdims=True)  # kênh vượt 1: kéo về, giữ sắc độ
    base = np.clip(np.where(mx > 1, x / np.maximum(mx, 1e-4) * np.minimum(mx, 1), x), 0, 1)
    L = lab(base.reshape(-1, 1, 3)).reshape(-1, 3).copy()
    w = np.clip((L[:, 0] - 20) / 60, 0, 1)                                      # 0 = vùng tối, 1 = vùng sáng
    L[:, 1] += (1 - w) * k["toi"][0] + w * k["sang"][0]
    L[:, 2] += (1 - w) * k["toi"][1] + w * k["sang"][1]
    L[:, 1:] *= k["sat"]
    # giữ da: màu thuộc dải da (sắc độ 20°–75° trong Lab, độ rực vừa) lấy lại gần màu đã sửa lỗi, và không rực quá cũ
    B = lab(base.reshape(-1, 1, 3)).reshape(-1, 3)
    ang = np.degrees(np.arctan2(B[:, 2], B[:, 1])); ch = np.hypot(B[:, 1], B[:, 2])
    da = np.clip(1 - np.abs(ang - 48) / 30, 0, 1) * np.clip((ch - 6) / 8, 0, 1) * np.clip((60 - ch) / 15, 0, 1) * (B[:, 0] > 25)
    da *= k.get("giu_da", 0.9)
    L[:, 1:] = L[:, 1:] * (1 - da[:, None]) + B[:, 1:] * da[:, None]
    cn = np.hypot(L[:, 1], L[:, 2]); tran = (da > 0.3) & (cn > ch * 1.03)  # da không rực hơn sau sửa lỗi quá 3%
    L[tran, 1:] *= (ch[tran] * 1.03 / np.maximum(cn[tran], 1e-3))[:, None]
    # giữ trắng: vùng rất sáng gần trung tính không bị nhuộm quá 1.5 đơn vị
    tr = (B[:, 0] > 88) & (ch < 8)
    L[tr, 1:] = np.clip(L[tr, 1:], B[tr, 1:] - 1.5, B[tr, 1:] + 1.5)
    out = cv2.cvtColor(L.reshape(-1, 1, 3), cv2.COLOR_LAB2RGB).reshape(rgb.shape)
    return base, np.clip(out, 0, 1)


def sua_loi(m, p50_dich=None, giu_am=0.0):
    """Thông số sửa lỗi từ số đo m: cân trắng theo vùng trắng/xám, kéo độ sáng giữa, nén nếu cháy."""
    # cân trắng: đưa trung bình vùng trắng/xám về xám (bù 90%), rồi chừa ấm có chủ ý (giu_am, đơn vị Lab b)
    t = np.array(m["rgb_trang"], np.float32); Y = float(t @ np.array([0.2126, 0.7152, 0.0722], np.float32))
    gain = 1 + 0.9 * (Y / np.maximum(t, 1e-3) - 1)
    gain *= np.array([1 + 0.004 * giu_am, 1, 1 - 0.006 * giu_am], np.float32)
    gain /= gain @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    p50 = min(max(m["p50"], 0.05), 0.95)
    # tối quá thì nâng; cảnh sáng (nội thất trắng) giữ sáng, chỉ hạ khi đang cháy nhiều
    dich = p50_dich if p50_dich else min(max(p50, 0.42), 0.75 if m["chay"] < 2 else 0.68)
    gamma = float(np.clip(np.log(dich) / np.log(p50), 0.72, 1.35))
    goi = 0.88 if m["chay"] > 1.0 else 1.0
    return {"gain": [round(float(v), 4) for v in gain], "gamma": round(gamma, 3), "goi": goi}


def ke_hoach(do_canh, chuan, pc, mau=None, do_manh=0.7):
    """Thông số từng cảnh. Khớp: độ sáng giữa về cảnh chuẩn (mức do_manh); ám màu: mọi cảnh về trung tính như nhau."""
    st = dict(PHONG_CACH[pc])
    if mau:  # phong cách đọc từ mẫu: tint vùng tối/sáng, độ rực tương đối, độ sáng giữa
        st.update(toi=tuple(round(v * do_manh, 2) for v in mau["toi"]), sang=tuple(round(v * do_manh, 2) for v in mau["sang"]),
                  sat=round(float(np.clip(1 + (mau["ruc"] / max(np.mean([d["ruc"] for d in do_canh]), 1) - 1) * do_manh * 0.5, 0.85, 1.15)), 3),
                  p50=round(float(np.clip(mau["p50"], 0.4, 0.65)), 3))
    giu_am = 2.0 if pc in ("sang-trong", "am-ap") else 0.0
    goc = sua_loi(do_canh[chuan], st["p50"], giu_am)
    p50_chuan = do_canh[chuan]["p50"] ** goc["gamma"]
    out = []
    for i, m in enumerate(do_canh):
        p50_dich = (1 - do_manh) * min(max(m["p50"], 0.42), 0.75) + do_manh * p50_chuan
        k = sua_loi(m, p50_dich, giu_am)
        k.update(tuong_phan=st["tuong_phan"], toi=list(st["toi"]), sang=list(st["sang"]), sat=st["sat"], giu_da=0.9)
        if m.get("da_sat", 0) > DA["sat"][1]:  # da đã rực sẵn trong footage: giảm độ rực chung một chút
            k["sat"] = round(k["sat"] * max(0.85, DA["sat"][1] / m["da_sat"]), 3)
        out.append(k)
    return out, st


def viet_cube(path, k):
    g = np.linspace(0, 1, N_LUT, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # .cube: đỏ chạy nhanh nhất
    rgb = np.stack([r, gg, b], -1).reshape(-1, 1, 3)
    out = bien_doi(rgb, k)[1].reshape(-1, 3)
    with open(path, "w") as f:
        f.write(f"TITLE \"HSL chinh_mau\"\nLUT_3D_SIZE {N_LUT}\n")
        f.writelines(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n" for v in out)


# ---------- chạy cho một dự án ----------
def chay(proj, mau_path=None, pc="sang-trong", chuan=None, do_manh=0.7, ap=False, tu_file=False):
    tl_p = os.path.join(proj, "timeline.json")
    tl = json.load(open(tl_p, encoding="utf8"))
    D = os.path.join(proj, "mau"); os.makedirs(D, exist_ok=True)
    raw = lambda c: os.path.join(proj, "build", "raw", c["file"])
    khung = [[f for f in (lay_khung(raw(c), c["in"] + c["dur"] * u) for u in (0.2, 0.5, 0.8)) if f is not None] for c in tl["clips"]]
    do_canh = [do(k) for k in khung]
    if chuan is None:  # cảnh chuẩn: có mặt người, ít cháy, độ sáng giữa gần 0.55
        chuan = min(range(len(do_canh)), key=lambda i: abs(do_canh[i]["p50"] - 0.55) + do_canh[i]["chay"] * 0.05 - (0.1 if "da_sat" in do_canh[i] else 0))
    mau = chu_ky([f for f in (lay_khung(mau_path, t) for t in (1, 3, 5, 8)) if f is not None] or
                 [cv2.cvtColor(cv2.imread(mau_path), cv2.COLOR_BGR2RGB).astype(np.float32) / 255]) if mau_path else None
    kp = os.path.join(D, "ke-hoach.json")
    if tu_file and os.path.exists(kp):
        kh = json.load(open(kp, encoding="utf8")); params, st = kh["canh"], kh["phong_cach"]
    else:
        params, st = ke_hoach(do_canh, chuan, pc, mau, do_manh)
    sau = []
    for i, (k, fr) in enumerate(zip(params, khung)):
        viet_cube(os.path.join(D, f"c{i + 1:02d}.cube"), k)
        sau.append(do([bien_doi(f, k)[1] for f in fr]))
    json.dump({"phong_cach": st, "chuan": chuan, "mau": mau_path and os.path.basename(mau_path), "chu_ky_mau": mau, "canh": params},
              open(kp, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    # ảnh trước/sau: khung giữa mỗi cảnh, tối đa 6 cảnh
    pick = sorted(set([chuan] + list(np.linspace(0, len(khung) - 1, min(6, len(khung))).astype(int))))[:6]
    cols = []
    for i in pick:
        f = khung[i][len(khung[i]) // 2]
        g = lambda x: cv2.resize(x, (round(x.shape[1] * 400 / x.shape[0]), 400))  # cùng chiều cao: clip ngang lẫn dọc
        col = np.vstack([g(f), g(bien_doi(f, params[i])[1])])
        cols.append(cv2.copyMakeBorder((col * 255).astype(np.uint8), 0, 0, 4, 4, cv2.BORDER_CONSTANT, value=(20, 20, 20)))
    cv2.imwrite(os.path.join(D, "truoc-sau.jpg"), cv2.cvtColor(np.hstack(cols), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
    canh_bao = kiem(do_canh, sau, chuan)
    bao_cao(proj, tl, do_canh, sau, params, st, chuan, pick, canh_bao, mau_path)
    if ap:
        shutil.copy(tl_p, tl_p + ".bak")
        for i, c in enumerate(tl["clips"]):
            c["look"] = f"lut:mau/c{i + 1:02d}.cube"
        json.dump(tl, open(tl_p, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return do_canh, sau, canh_bao


def kiem(truoc, sau, chuan):
    """Ngưỡng nghiệm thu (theo agentic-color-grader: sáng ±5/255, màu ±3; da theo GHI-NHO-NGHIEM-THU)."""
    out = []
    for i, (a, b) in enumerate(zip(truoc, sau), 1):
        if abs(b["p50"] - sau[chuan]["p50"]) > 0.08:
            out.append(f"Cảnh {i}: độ sáng giữa {b['p50']:.2f} lệch cảnh chuẩn {sau[chuan]['p50']:.2f} (cảnh khác hẳn ánh sáng? xem ảnh)")
        if abs(b["am_a"] - sau[chuan]["am_a"]) > 3 or abs(b["am_b"] - sau[chuan]["am_b"]) > 3:  # đồng nhất với cảnh chuẩn (tông chung là chủ ý)
            out.append(f"Cảnh {i}: màu vùng trắng/xám (a {b['am_a']:+.1f}, b {b['am_b']:+.1f}) lệch cảnh chuẩn "
                       f"(a {sau[chuan]['am_a']:+.1f}, b {sau[chuan]['am_b']:+.1f})")
        if "da_sat" in b and not DA["sat"][0] - 5 <= b["da_sat"] <= DA["sat"][1] + 3:
            out.append(f"Cảnh {i}: da rực {b['da_sat']:.0f}% (chuẩn {DA['sat'][0]}–{DA['sat'][1]}%)")
        if a["chay"] > 3:
            out.append(f"Cảnh {i}: footage cháy sáng {a['chay']:.1f}% điểm ảnh, không cứu được hoàn toàn (đã nén mềm)")
        if a["thieu"] > 5:
            out.append(f"Cảnh {i}: thiếu sáng {a['thieu']:.1f}% điểm ảnh")
    return out


def bao_cao(proj, tl, truoc, sau, params, st, chuan, pick, cb, mau_path):
    am = lambda m: ("ám vàng" if m["am_b"] > 3 else "ám xanh" if m["am_b"] < -3 else "") + (" ám hồng" if m["am_a"] > 3 else " ám lục" if m["am_a"] < -3 else "")
    da = lambda m: f"{m['da_sat']:.0f}% / {m['da_hue']:.0f}°" if "da_sat" in m else "–"
    rows = [f"| {i + 1}{' ★' if i == chuan else ''} | {c['file'][:22]} {c['in']:.1f}s | {a['p50']:.2f} → {b['p50']:.2f} | "
            f"{a['am_a']:+.1f}, {a['am_b']:+.1f} → {b['am_a']:+.1f}, {b['am_b']:+.1f} {am(a)} | {a['chay']:.1f}% | {a['ruc']:.0f} → {b['ruc']:.0f} | {da(a)} → {da(b)} |"
            for i, (c, a, b) in enumerate(zip(tl["clips"], truoc, sau))]
    md = [f"# Màu sắc: {os.path.basename(proj.rstrip('/'))}", "",
          f"Phong cách: **{st.get('vi', '')}**" + (f" · lấy màu từ mẫu `{os.path.basename(mau_path)}`" if mau_path else ""),
          f"Cảnh chuẩn: **{chuan + 1}** (★). Mỗi cảnh một LUT `mau/cNN.cube`; thông số sửa tay ở `mau/ke-hoach.json` rồi chạy lại với `--tu-file`.", "",
          "![Trước (trên) / sau (dưới)](mau/truoc-sau.jpg)", f"Ảnh: hàng trên là trước, hàng dưới là sau; cảnh {', '.join(str(i + 1) for i in pick)}.", "",
          "| Cảnh | File | Sáng giữa | Ám vùng trắng (a, b) | Cháy | Độ rực | Da (rực / sắc độ) |", "|---|---|---|---|---|---|---|", *rows, "",
          "## Cần Hào xem" if cb else "## Kiểm tra: đạt", *[f"- {x}" for x in cb], "",
          "Duyệt xong: `python3 scripts/chinh_mau.py " + proj + " --ap` (ghi LUT vào từng đoạn, giữ timeline.json.bak), rồi Dựng nháp."]
    open(os.path.join(proj, "MAU-SAC.md"), "w", encoding="utf8").write("\n".join(md) + "\n")


def _tu_kiem():
    rng = np.random.default_rng(1)
    # cảnh ám vàng, tối: tường trắng + mặt người
    img = np.ones((240, 240, 3), np.float32) * np.array([0.80, 0.76, 0.60], np.float32)
    img[60:180, 80:160] = [0.78, 0.52, 0.40]                       # "da"
    img += rng.normal(0, 0.01, img.shape).astype(np.float32)
    img = np.clip(img * 0.5, 0, 1)
    m = do([img])
    assert m["am_b"] > 5, m                                         # đo được ám vàng
    k = sua_loi(m)
    k.update(tuong_phan=0.0, toi=[0, 0], sang=[0, 0], sat=1.0)
    base, fin = bien_doi(img, k)
    m2 = do([fin])
    assert abs(m2["am_b"]) < 3 and abs(m2["am_a"]) < 3, m2          # hết ám
    assert m2["p50"] > m["p50"], (m["p50"], m2["p50"])              # sáng lên
    # phong cách ấm vùng sáng nhưng da không bị đẩy rực
    k2 = dict(k, sang=[3, 8], sat=1.2, giu_da=0.9)
    _, f2 = bien_doi(img, k2)
    ruc = lambda x: cv2.cvtColor(np.ascontiguousarray(x[60:180, 80:160]), cv2.COLOR_RGB2HSV)[..., 1].mean()
    assert ruc(f2) < ruc(base) * 1.10, (ruc(base), ruc(f2))  # phong cách cực mạnh (rực 1,2 + ấm 8): da tăng không quá 10%
    st = PHONG_CACH["sang-trong"]
    _, f3 = bien_doi(img, dict(k, toi=list(st["toi"]), sang=list(st["sang"]), sat=st["sat"], tuong_phan=st["tuong_phan"]))
    assert ruc(f3) < ruc(base) * 1.05, (ruc(base), ruc(f3))  # phong cách thật: da gần như giữ nguyên
    # trắng vẫn trắng
    w = np.ones((10, 10, 3), np.float32) * 0.97
    Lw = lab(bien_doi(w, dict(k2, gain=[1, 1, 1], gamma=1, goi=1))[1])
    assert abs(Lw[..., 2].mean()) < 2.5, Lw[..., 2].mean()
    # LUT ghi đúng định dạng và tương đương hàm
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "t.cube"); viet_cube(p, k2)
        lines = open(p).read().splitlines()
        assert lines[1] == f"LUT_3D_SIZE {N_LUT}" and len(lines) == 2 + N_LUT ** 3
        r, g, b = map(float, lines[2 + N_LUT - 1].split())  # đỏ max, xanh lá 0, xanh dương 0
        ref = bien_doi(np.array([[[1, 0, 0]]], np.float32), k2)[1][0, 0]
        assert np.allclose([r, g, b], ref, atol=1e-4), ([r, g, b], ref)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("du_an"); a.add_argument("--mau"); a.add_argument("--phong-cach", default="sang-trong", choices=list(PHONG_CACH))
    a.add_argument("--chuan", type=int, help="số thứ tự cảnh chuẩn (1, 2…)"); a.add_argument("--do-manh", type=float, default=0.7)
    a.add_argument("--ap", action="store_true"); a.add_argument("--tu-file", action="store_true")
    o = a.parse_args()
    truoc, sau, cb = chay(o.du_an, o.mau, o.phong_cach, o.chuan - 1 if o.chuan else None, o.do_manh, o.ap, o.tu_file)
    print(f"Xong {len(sau)} cảnh. Báo cáo: {o.du_an}/MAU-SAC.md · ảnh: {o.du_an}/mau/truoc-sau.jpg" + (" · đã ghi LUT vào timeline" if o.ap else ""))
    for x in cb:
        print(" -", x)
