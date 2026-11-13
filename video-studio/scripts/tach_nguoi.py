"""Tách người khỏi nền theo từng khung (để đặt chữ phía sau đầu): mặt nạ xám, trắng = người.
Mô hình MODNet (giấy phép Apache-2.0, 25 MB) chạy bằng onnxruntime (đã có sẵn cùng faster-whisper), tải một lần về video-studio/models/.
Chỉ tính ở các khoảng có chữ "sau_dau" (ngoài khoảng đó mặt nạ đen) để nhanh.
Chạy thử: python3 scripts/tach_nguoi.py <video> <giây bắt đầu> <giây kết thúc> <ra.mp4>   ·   tự kiểm: --tu-kiem"""
import json, os, subprocess, sys, urllib.request

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MODEL = os.path.join(ROOT, "models", "modnet.onnx")
URL = "https://huggingface.co/Xenova/modnet/resolve/main/onnx/model.onnx"
IW, IH = 512, 896  # cỡ đưa vào mô hình (bội số 32, gần tỉ lệ 9:16)


def tai_mo_hinh():
    if not os.path.exists(MODEL):
        os.makedirs(os.path.dirname(MODEL), exist_ok=True)
        print("Tải mô hình tách người MODNet (25 MB, một lần)…", flush=True)
        urllib.request.urlretrieve(URL, MODEL + ".tam"); os.replace(MODEL + ".tam", MODEL)
    return MODEL


def thong_so(video):
    st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                                    "-of", "json", video], capture_output=True, text=True, check=True).stdout)["streams"][0]
    a, b = st["r_frame_rate"].split("/")
    return st["width"], st["height"], float(a) / float(b)


def mat_na(video, cuaso, out, le=0.25):
    """cuaso: [(bắt đầu, kết thúc)] giây. Ghi out (mp4 xám, cùng cỡ và số khung hình với video)."""
    import onnxruntime as ort
    W, H, fps = thong_so(video)
    ses = ort.InferenceSession(tai_mo_hinh(), providers=["CPUExecutionProvider"])
    doc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", video, "-vf", f"scale={IW}:{IH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    ghi = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{IW}x{IH}", "-r", f"{fps}", "-i", "-",
                            "-vf", f"scale={W}:{H}:flags=bicubic", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    den, truoc, i, n = np.zeros((IH, IW), np.uint8), None, 0, IW * IH * 3
    while (buf := doc.stdout.read(n)) and len(buf) == n:
        t = i / fps
        if any(a - le <= t <= b + le for a, b in cuaso):
            x = (np.frombuffer(buf, np.uint8).reshape(IH, IW, 3).astype(np.float32) / 127.5 - 1).transpose(2, 0, 1)[None]
            a = ses.run(None, {"input": x})[0][0, 0]
            a = a if truoc is None else 0.6 * a + 0.4 * truoc  # làm mượt theo thời gian: mép tóc không rung
            truoc = a
            ghi.stdin.write((np.clip((a - 0.08) / 0.84, 0, 1) * 255).astype(np.uint8).tobytes())
        else:
            truoc = None
            ghi.stdin.write(den.tobytes())
        i += 1
    doc.wait(); ghi.stdin.close(); ghi.wait()
    if ghi.returncode or i == 0:
        raise RuntimeError("Không tạo được mặt nạ người cho " + video)
    return i


def _tu_kiem():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        v, m = os.path.join(d, "v.mp4"), os.path.join(d, "m.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=gray:s=360x640:r=30:d=2", "-pix_fmt", "yuv420p", v], check=True)
        n = mat_na(v, [(0.5, 1.0)], m)
        W, H, fps = thong_so(m)
        assert (W, H) == (360, 640) and n == 60, (W, H, n)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", m, "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        f = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
        assert len(f) == 60 and f[0].max() < 20 and f[-1].max() < 20  # ngoài khoảng chữ: đen hẳn
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 5:
        print(mat_na(sys.argv[1], [(float(sys.argv[2]), float(sys.argv[3]))], sys.argv[4]), "khung")
    else:
        sys.exit(__doc__)
