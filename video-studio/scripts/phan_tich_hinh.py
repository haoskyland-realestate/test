"""Chấm điểm khung hình của một file video (OpenCV): độ nét, sáng/tối, cháy sáng, màu, chuyển động, rung giật, khuôn mặt.
Dùng: python3 scripts/phan_tich_hinh.py <video>   → in điểm từng giây (để xem và chỉnh ngưỡng)."""
import json, os, subprocess, sys
import numpy as np

FPS_A, W_A = 5, 320  # phân tích 5 khung/giây ở khung rộng 320px là đủ, nhanh
_face = None


def khung(path):
    """Giải mã video thành ảnh xám nhỏ + ảnh màu nhỏ, 5 khung/giây (đã xoay đúng chiều)."""
    # khung đầu cho biết kích thước thật sau khi FFmpeg tự xoay (video quay dọc)
    import cv2
    png = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-frames:v", "1", "-vf", f"scale={W_A}:-2", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    H = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR).shape[0]
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vf", f"fps={FPS_A},scale={W_A}:{H}", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W_A, 3)


def phan_tich(path, cache=None):
    """Mỗi khung (5/giây): t, nét, sáng, tương phản, cháy (%), màu, chuyển động, giật, mặt (diện tích, lệch tâm)."""
    if cache and os.path.exists(cache):
        return json.load(open(cache))
    import cv2
    global _face
    _face = _face or cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
    fr = khung(path)
    out, prev, prev_mv = [], None, 0.0
    for k, bgr in enumerate(fr):
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        sharp = float(cv2.Laplacian(g, cv2.CV_64F).var())
        b, gg, r = [bgr[..., i].astype(np.float32) for i in range(3)]
        rg, yb = r - gg, 0.5 * (r + gg) - b
        color = float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))  # độ rực màu (Hasler–Süsstrunk)
        clip = float(((g < 8) | (g > 247)).mean() * 100)
        mv = 0.0
        if prev is not None:
            flow = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 2, 13, 2, 5, 1.1, 0)
            mv = float(np.median(np.hypot(flow[..., 0], flow[..., 1])))  # chuyển động chung của khung (px/khung)
        faces = _face.detectMultiScale(g, 1.15, 5, minSize=(24, 24))
        fa, fo = 0.0, 1.0
        if len(faces):
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            fa = float(w * h / g.size)
            fo = float(abs((x + w / 2) / g.shape[1] - 0.5) + abs((y + h / 2) / g.shape[0] - 0.4))
        out.append({"t": round(k / FPS_A, 2), "sharp": round(sharp, 1), "bright": round(float(g.mean()), 1), "contrast": round(float(g.std()), 1),
                    "clip": round(clip, 2), "color": round(color, 1), "motion": round(mv, 2), "jerk": round(abs(mv - prev_mv), 2),
                    "face": round(fa, 4), "face_off": round(fo, 3)})
        prev, prev_mv = g, mv
    if cache:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        json.dump(out, open(cache, "w"))
    return out


def diem(f, talking=False):
    """Điểm 0–100 cho một khung + danh sách lỗi/điểm cộng (tiếng Việt)."""
    s, why = 70.0, []
    if f["sharp"] < 40: s -= 35; why.append("mờ")
    elif f["sharp"] < 90: s -= 15; why.append("hơi mờ")
    elif f["sharp"] > 250: s += 8
    if f["bright"] < 45: s -= 25; why.append("tối")
    elif f["bright"] > 215: s -= 20; why.append("quá sáng")
    if f["clip"] > 15: s -= 15; why.append("cháy/mất chi tiết")
    if f["contrast"] < 25: s -= 10; why.append("nhạt")
    if f["color"] > 45: s += 8; why.append("màu đẹp")
    # chuyển động tính bằng px/khung ở khung rộng 320px, 5 khung/giây (đi bộ cầm gimbal thường 4–9)
    if f["jerk"] > max(3.5, 0.7 * f["motion"]): s -= 22; why.append("giật")
    elif f["motion"] > 14: s -= 15; why.append("lia quá nhanh")
    elif 0.4 < f["motion"] <= 9 and f["jerk"] < max(1.2, 0.35 * f["motion"]): s += 10; why.append("chuyển động mượt")
    if talking:
        if f["face"] == 0: s -= 30; why.append("mất mặt người nói")
        elif f["face_off"] > 0.35: s -= 10; why.append("mặt lệch khung")
        elif f["face"] > 0.04: s += 5
    return max(0.0, min(100.0, s)), why


if __name__ == "__main__":
    fs = phan_tich(sys.argv[1])
    talking = sum(f["face"] > 0.02 for f in fs) > len(fs) * 0.4  # mặt đủ lớn trong phần lớn thời gian
    print("người nói trước máy" if talking else "cảnh (không có người nói)")
    for k in range(0, len(fs), FPS_A):
        sec = fs[k:k + FPS_A]
        avg = lambda key: sum(f[key] for f in sec) / len(sec)
        sc = [diem(f, talking) for f in sec]
        why = sorted({w for _, ws in sc for w in ws})
        print(f"{k // FPS_A:3d}s điểm {sum(x for x, _ in sc) / len(sc):5.1f}  nét {avg('sharp'):6.0f} sáng {avg('bright'):4.0f} "
              f"màu {avg('color'):4.0f} động {avg('motion'):4.1f} giật {avg('jerk'):4.1f} mặt {avg('face'):.3f}  {', '.join(why)}")
