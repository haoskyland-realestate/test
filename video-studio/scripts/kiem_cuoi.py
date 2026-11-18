"""Kiểm video đã dựng bằng máy (các phép đo trước làm tay cho Saigon Park, 17–18/11):
khổ hình đúng nền tảng, độ dài đúng timeline, hình khớp tiếng, không chớp khung tối (tối đột ngột ≤ 3 khung rồi sáng lại),
âm lượng −14 LUFS ±1. Chạy trong video-studio:  python scripts/kiem_cuoi.py projects/<tên> [file.mp4]  (thoát mã 1 nếu có lỗi)"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def dai(f, loai):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", f"{loai}:0", "-show_entries", "stream=duration,width,height",
                        "-of", "json", f], capture_output=True, text=True).stdout
    s = (json.loads(o or "{}").get("streams") or [{}])[0]
    return float(s.get("duration") or 0), s.get("width"), s.get("height")


def chop_toi(sang, fps=30):
    """Giây có khung tối chớp: độ sáng tụt dưới nửa rồi trở lại trong ≤ 3 khung (khung đen lọt giữa hai cảnh)."""
    out = []
    for i in range(1, len(sang) - 1):
        if sang[i] < 0.5 * sang[i - 1]:
            j = next((k for k in range(i, min(i + 4, len(sang))) if sang[k] >= 0.8 * sang[i - 1]), None)
            if j is not None:
                out.append(round(i / fps, 2))
    return out


def kiem(f, tl):
    from timeline import size, layout
    loi = []
    W, H = size(tl)
    vd, w, h = dai(f, "v")
    ad, _, _ = dai(f, "a")
    tong = layout(tl)["total"]
    if (w, h) not in ((W, H), (W // 2, H // 2)):
        loi.append(f"khổ {w}×{h}, cần {W}×{H} (hoặc bản xem {W // 2}×{H // 2})")
    if abs(vd - tong) > 0.15:
        loi.append(f"độ dài hình {vd:.2f}s khác timeline {tong:.2f}s")
    if abs(vd - ad) > 0.1:
        loi.append(f"hình {vd:.2f}s và tiếng {ad:.2f}s lệch nhau")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=32:57,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = 32 * 57
    sang = [sum(raw[i:i + n]) / n for i in range(0, len(raw) - n + 1, n)]
    if (c := chop_toi(sang)):
        loi.append("chớp khung tối ở giây " + ", ".join(map(str, c[:10])))
    e = subprocess.run(["ffmpeg", "-nostats", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    if m and abs(float(m[-1]) + 14) > 1:
        loi.append(f"âm lượng {m[-1]} LUFS, chuẩn −14 ±1")
    return loi, {"khổ": f"{w}×{h}", "độ dài": round(vd, 2), "LUFS": float(m[-1]) if m else None}


def _tu_kiem():
    assert chop_toi([80, 80, 20, 20, 80, 80]) == [0.07]          # 2 khung đen giữa hai cảnh sáng
    assert chop_toi([80, 80, 20, 20, 20, 20, 20, 25]) == []      # cảnh tối thật (đêm, thẻ nền tối): không báo
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) in (2, 3) and os.path.isdir(sys.argv[1]):
        pj = os.path.abspath(sys.argv[1])
        f = sys.argv[2] if len(sys.argv) == 3 else os.path.join(HERE, "..", "out", os.path.basename(pj) + ".mp4")
        loi, so = kiem(f, json.load(open(os.path.join(pj, "timeline.json"), encoding="utf8")))
        print(f"{os.path.basename(f)}: {so}")
        print("\n".join("- LỖI: " + x for x in loi) or "Kiểm bản dựng: ĐẠT")
        sys.exit(1 if loi else 0)
    else:
        sys.exit(__doc__)
