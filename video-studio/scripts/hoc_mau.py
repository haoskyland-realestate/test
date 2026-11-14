"""Học từ video mẫu (bước đo, KHÔNG dùng AI): đo nhịp cắt, chớp sáng (chuyển cảnh cháy sáng), nhịp âm, độ ồn, màu từng đoạn,
làm ảnh lưới khung hình. Kết quả vào thu-vien-mau/_hoc/<tên>/ : luoi.jpg, do.json, BAO-CAO.md. Claude Code đọc ba file đó
(skill hoc-mau) rồi ghép với kho để viết mau.json. Video mẫu chỉ để đo, KHÔNG chép vào repo.
Chạy trong video-studio:  python3 scripts/hoc_mau.py <video mẫu> [tên]      ·   tự kiểm: --tu-kiem"""
import json, os, re, subprocess, sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SR = 16000


def chay(*a, **k):
    return subprocess.run(a, capture_output=True, text=True, **k)


def thong_tin(v):
    j = json.loads(chay("ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", v).stdout)
    s = next(x for x in j["streams"] if x["codec_type"] == "video")
    a, b = s["r_frame_rate"].split("/")
    return {"dai": round(float(j["format"]["duration"]), 2), "rong": s["width"], "cao": s["height"], "fps": round(float(a) / float(b), 2),
            "co_tieng": any(x["codec_type"] == "audio" for x in j["streams"])}


def mau_nho(v, fps=2, w=64):
    """Khung nhỏ w×(tỉ lệ) mỗi 1/fps giây → mảng (n, h, w, 3)."""
    ti = thong_tin(v)
    h = max(2, round(w * ti["cao"] / ti["rong"]) // 2 * 2)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", v, "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw[: len(raw) // (w * h * 3) * (w * h * 3)], np.uint8).reshape(-1, h, w, 3)


def cat_canh(v, nguong=0.3):
    o = chay("ffmpeg", "-nostdin", "-i", v, "-vf", f"select='gt(scene,{nguong})',showinfo", "-f", "null", "-").stderr
    return [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", o)]


def am_thanh(v):
    """Đỉnh âm (tiếng vút, tiếng chạm): thời điểm năng lượng tăng vọt; kèm độ ồn tích hợp LUFS."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", v, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    if len(raw) < SR:
        return {"lufs": None, "dinh": []}
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = SR // 50
    e = np.sqrt(np.convolve(x * x, np.ones(hop) / hop, "valid")[::hop])
    luc = np.maximum(np.diff(e, prepend=e[0]), 0)  # tăng năng lượng đột ngột
    nguong = max(np.percentile(luc, 97), 1e-4)
    dinh, cuoi = [], -1.0
    for i in np.where(luc >= nguong)[0]:
        t = i / 50
        if t - cuoi >= 0.3:
            dinh.append(round(float(t), 2)); cuoi = t
    o = chay("ffmpeg", "-nostdin", "-i", v, "-af", "loudnorm=print_format=summary", "-f", "null", "-").stderr
    m = re.search(r"Input Integrated:\s*(-?[\d.]+)", o)
    return {"lufs": float(m.group(1)) if m else None, "dinh": dinh}


def phan_tich(v):
    ti = thong_tin(v)
    k = mau_nho(v)
    luma = k.mean(axis=(1, 2, 3))
    chop = [round(i / 2, 1) for i in range(1, len(luma) - 1) if luma[i] > 200 and luma[i] > luma[i - 1] + 40]  # chớp trắng
    toi = [round(i / 2, 1) for i in range(len(luma)) if luma[i] < 12]
    cc = cat_canh(v)
    seg = []
    n = max(1, int(ti["dai"] // 10))
    for s in range(n):
        a, b = int(s * len(k) / n), int((s + 1) * len(k) / n)
        px = k[a:b].reshape(-1, 3).astype(np.float32)
        mx, mn = px.max(1), px.min(1)
        seg.append({"tu": round(s * ti["dai"] / n, 1), "sang": round(float(px.mean()) / 2.55, 1), "ruc": round(float(((mx - mn) / np.maximum(mx, 1)).mean()) * 100, 1),
                    "rgb": [int(c) for c in px.mean(0)]})
    return {"thong_tin": ti, "cat": cc, "so_cat_tren_10s": round(len(cc) / max(ti["dai"], 1) * 10, 1), "chop_trang": chop, "khung_den": toi,
            "am": am_thanh(v) if ti["co_tieng"] else {"lufs": None, "dinh": []}, "mau_theo_doan": seg}


def luoi(v, ra, moi=None, cot=6, hang=4):
    d = thong_tin(v)["dai"]
    moi = moi or max(0.5, d / (cot * hang))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", v, "-vf", f"fps=1/{moi:.2f},scale=240:-2,tile={cot}x{hang}", "-frames:v", "1", ra], check=True)
    return moi


def viet(v, ten=None):
    ten = re.sub(r"[^\w-]+", "-", ten or os.path.splitext(os.path.basename(v))[0]).strip("-")[:40] or "mau"
    d = os.path.join(ROOT, "thu-vien-mau", "_hoc", ten)
    os.makedirs(d, exist_ok=True)
    r = phan_tich(v)
    r["moi_o_luoi_giay"] = round(luoi(v, os.path.join(d, "luoi.jpg")), 2)
    json.dump(r, open(os.path.join(d, "do.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    t = r["thong_tin"]
    open(os.path.join(d, "BAO-CAO.md"), "w", encoding="utf8").write(
        f"# Đo video mẫu: {ten}\n\n- Cỡ {t['rong']}×{t['cao']}, {t['fps']} khung/giây, dài {t['dai']} giây.\n"
        f"- Số lần cắt/chuyển cảnh: {len(r['cat'])} ({r['so_cat_tren_10s']} lần mỗi 10 giây). Mốc: {', '.join(map(str, r['cat'][:30]))}{'…' if len(r['cat']) > 30 else ''}\n"
        f"- Chớp trắng (hợp chuyển cảnh cháy sáng/flash): {r['chop_trang'] or 'không thấy'}\n- Khung đen: {r['khung_den'] or 'không thấy'}\n"
        f"- Độ ồn: {r['am']['lufs']} LUFS; đỉnh âm (gồm cả chỗ bắt đầu nói; nghi tiếng vút/chạm khi trùng mốc chữ hoặc chuyển cảnh): {len(r['am']['dinh'])} chỗ, đầu tiên: {r['am']['dinh'][:12]}\n"
        f"- Màu theo từng đoạn: " + "; ".join(f"{s['tu']}s sáng {s['sang']}% rực {s['ruc']}%" for s in r["mau_theo_doan"]) + "\n\n"
        "Chưa đo được (cần Claude nhìn `luoi.jpg`): kiểu chữ, màu chữ, đồ hoạ, nội dung cảnh chèn. Chữ cần OCR (chưa cài, chờ Hào duyệt).\n")
    return d, r


def _tu_kiem():
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        v = os.path.join(t, "v.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=red:s=180x320:r=30:d=2", "-f", "lavfi", "-i", "color=c=blue:s=180x320:r=30:d=2",
                        "-f", "lavfi", "-i", "color=c=white:s=180x320:r=30:d=0.5", "-f", "lavfi", "-i", "color=c=red:s=180x320:r=30:d=2",
                        "-filter_complex", "[0][1][2][3]concat=n=4", "-pix_fmt", "yuv420p", v], check=True)
        r = phan_tich(v)
        assert len(r["cat"]) >= 3 and abs(r["cat"][0] - 2.0) < 0.2, r["cat"]
        assert r["chop_trang"], r  # đoạn trắng 0,5 giây
        assert r["thong_tin"]["rong"] == 180 and not r["thong_tin"]["co_tieng"]
        luoi(v, os.path.join(t, "l.jpg"), 0.5, 4, 2)
        assert os.path.getsize(os.path.join(t, "l.jpg")) > 500
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
        d, r = viet(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print("Đã đo xong:", os.path.relpath(d, ROOT), "| cắt", len(r["cat"]), "| chớp trắng", len(r["chop_trang"]), "| đỉnh âm", len(r["am"]["dinh"]))
    else:
        sys.exit(__doc__)
