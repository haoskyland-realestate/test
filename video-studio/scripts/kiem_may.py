"""Kiểm máy có đủ công cụ cho app studio chưa (Windows, Mac, Linux). Báo tiếng Việt: đạt / thiếu + cách sửa.
Chạy trong video-studio:  python scripts/kiem_may.py              (nhanh, vài giây)
                           python scripts/kiem_may.py --dung-thu   (thêm: dựng thử video giả 6 giây, 1–3 phút, không cần footage)
chay-studio.bat (Windows) / chay-studio.command (Mac) tự chạy bản nhanh mỗi lần mở app."""
import importlib.util, os, platform, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
WIN = os.name == "nt"
MAC = platform.system() == "Darwin"


def cai(goi_win, goi_mac):
    """Lệnh cài thiếu theo máy: Windows dùng winget, Mac dùng Homebrew (hoặc chạy lại setup-mac.sh)."""
    return f"brew install {goi_mac} (hoặc chạy lại: bash setup-mac.sh)" if MAC else f"winget install {goi_win}"
ket_qua = []  # (đạt?, bắt buộc?, tên, ghi chú / cách sửa)


def ghi(ok, can, ten, note=""):
    ket_qua.append((ok, can, ten, note))


def chay(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf8", errors="replace")
        return r.returncode, r.stdout + r.stderr
    except (OSError, subprocess.TimeoutExpired) as ex:
        return -1, str(ex)


def kiem_python():
    ok = sys.version_info >= (3, 10)
    ghi(ok, True, f"Python {platform.python_version()}", "" if ok else "Cần Python 3.10 trở lên: " + cai("Python.Python.3.12", "python@3.12"))
    utf8 = sys.flags.utf8_mode or not WIN
    ghi(utf8, True, "Chế độ UTF-8 của Python (chữ tiếng Việt)",
        "" if utf8 else "Chạy lại setup-windows.ps1 (đặt PYTHONUTF8=1), hoặc mở app bằng chay-studio.bat")


def kiem_ffmpeg():
    exe = shutil.which("ffmpeg")
    if not exe:
        return ghi(False, True, "FFmpeg", "Chưa cài: " + cai("Gyan.FFmpeg", "ffmpeg") + ", rồi mở lại cửa sổ lệnh")
    _, v = chay(["ffmpeg", "-hide_banner", "-version"])
    ghi(True, True, "FFmpeg", v.splitlines()[0][:60] if v else exe)
    _, f = chay(["ffmpeg", "-hide_banner", "-filters"])
    _, e = chay(["ffmpeg", "-hide_banner", "-encoders"])
    _, d = chay(["ffmpeg", "-hide_banner", "-decoders"])
    can = {"zscale": "chuyển màu HDR của DJI/iPhone (thiếu thì video nhạt)", "tonemap": "chuyển màu HDR", "xfade": "chuyển cảnh",
           "loudnorm": "chuẩn âm lượng", "zoompan": "zoom", "boxblur": "nền mờ khung ngang"}
    thieu = [f"{k} ({v})" for k, v in can.items() if not re.search(rf"\s{k}\s", f)]
    ghi(not thieu, True, "FFmpeg: bộ lọc cần dùng", "Thiếu " + ", ".join(thieu) + ". Cài bản đầy đủ: " + cai("Gyan.FFmpeg", "ffmpeg") if thieu else "")
    thieu = [k for k in ("libx264", "aac") if not re.search(rf"\s{k}\s", e)] + [k for k in ("libvpx-vp9",) if not re.search(rf"\s{k}\s", d)]
    ghi(not thieu, True, "FFmpeg: mã hoá H.264, AAC, đọc VP9", "Thiếu " + ", ".join(thieu) if thieu else "")
    nv = bool(re.search(r"\sh264_nvenc\s", e))
    ghi(nv, False, "FFmpeg: mã hoá bằng card NVIDIA (NVENC)", "" if nv else "Chưa dùng tới; sau này giúp xuất nhanh hơn")
    ghi(bool(shutil.which("ffprobe")), True, "ffprobe", "" if shutil.which("ffprobe") else "Đi kèm FFmpeg; thiếu thì cài lại FFmpeg")


def kiem_node():
    exe = shutil.which("node")
    if not exe:
        return ghi(False, True, "Node.js", "Chưa cài: " + cai("OpenJS.NodeJS.LTS", "node"))
    _, v = chay(["node", "--version"])
    m = re.search(r"v(\d+)", v)
    ok = bool(m and int(m[1]) >= 22)
    ghi(ok, True, f"Node.js {v.strip()}", "" if ok else "HyperFrames cần Node 22 trở lên: " + cai("OpenJS.NodeJS.LTS", "node"))
    ghi(bool(shutil.which("npx")), True, "npx", "" if shutil.which("npx") else "Đi kèm Node.js: cài lại Node")
    gsap = os.path.exists(os.path.join(ROOT, "node_modules", "gsap", "dist", "gsap.min.js"))
    ghi(gsap, True, "Thư viện JS của dự án (npm install)", "" if gsap else "Trong thư mục video-studio chạy: npm install")


def kiem_thu_vien_python():
    for mod, ten, can, sua in (
        ("numpy", "numpy (tính toán)", True, "pip install numpy"),
        ("faster_whisper", "faster-whisper (phụ đề tự động)", False, "pip install faster-whisper"),
        ("cv2", "OpenCV (master cut chấm điểm khung hình)", False, 'pip install "opencv-python-headless<5"'),
        ("opentimelineio", "OpenTimelineIO (xuất Premiere/DaVinci)", False, "pip install opentimelineio otio-fcp-adapter"),
    ):
        ok = importlib.util.find_spec(mod) is not None
        note = "" if ok else sua
        if ok and mod == "cv2":
            import cv2
            ok = hasattr(cv2, "CascadeClassifier")  # OpenCV 5 bỏ bộ nhận mặt người đang dùng
            note = "" if ok else f'OpenCV {cv2.__version__} thiếu nhận mặt: pip install "opencv-python-headless<5"'
        ghi(ok, can, ten, note)


def kiem_gpu():
    if not shutil.which("nvidia-smi"):
        return ghi(False, False, "Card NVIDIA", "Không thấy nvidia-smi: phụ đề chạy bằng CPU (chậm hơn). PC có RTX thì cài driver NVIDIA mới")
    _, v = chay(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"])
    ghi(True, False, "Card NVIDIA", v.strip()[:80])
    if importlib.util.find_spec("ctranslate2"):
        import ctranslate2
        n = ctranslate2.get_cuda_device_count()
        ghi(n > 0, False, "Phụ đề chạy bằng card", "" if n else "faster-whisper chưa thấy CUDA: phụ đề vẫn chạy bằng CPU")


def kiem_o_dia():
    free = shutil.disk_usage(ROOT).free / 1e9
    ghi(free > 20, True, f"Ổ đĩa còn trống {free:.0f} GB", "" if free > 20 else "Nên còn trên 20 GB (bản xem trước, cảnh đã cắt, mô hình phụ đề 1,6 GB)")


def kiem_kho():
    sfx = os.path.join(ROOT, "thu-vien-am-thanh", "hieu-ung.json")
    ghi(os.path.exists(sfx), False, "Kho hiệu ứng âm", "" if os.path.exists(sfx) else "Chạy: python scripts/tao_sfx.py")


def dung_thu():
    """Dựng một video giả 6 giây (hình mẫu của FFmpeg) qua đúng bộ dựng thật: chữ 3D, chuyển cảnh WebGL, hiệu ứng âm."""
    import json
    name = "zz-kiem-may"
    d = os.path.join(ROOT, "projects", name)
    raw = os.path.join(d, "build", "raw")
    os.makedirs(raw, exist_ok=True)
    for f, src in (("a.mp4", "testsrc2"), ("b.mp4", "mandelbrot")):
        chay(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"{src}=s=1080x1920:r=30", "-f", "lavfi", "-i", "sine=f=300:r=44100",
              "-t", "3.5", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", os.path.join(raw, f)])
    tl = {"version": 1, "meta": {"platform": "tiktok", "style": "edit-phim"}, "audio": {"music": None, "voice": True},
          "clips": [{"file": "a.mp4", "in": 0, "dur": 3}, {"file": "b.mp4", "in": 0, "dur": 3}],
          "transitions": [{"type": "gl-CrossZoom", "dur": 0.35}],
          "texts": [{"kind": "title3d", "start": 0.2, "dur": 2.4, "top": "kiểm tra", "big": "MÁY ĐẠT", "sub": "chữ tiếng Việt có dấu"}],
          "sfx": [{"start": 2.8, "dur": 0.6, "file": "whoosh_zoom_01", "vol": 0.8}]}
    json.dump(tl, open(os.path.join(d, "timeline.json"), "w", encoding="utf8"), ensure_ascii=False)
    t = time.time()
    env = dict(os.environ, PYTHONUTF8="1")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "dung.py"), d, "--nhap"], cwd=ROOT, capture_output=True,
                       text=True, encoding="utf8", errors="replace", env=env, timeout=1200)
    out = os.path.join(ROOT, "out", name + ".nhap.mp4")
    ok = r.returncode == 0 and os.path.exists(out)
    ghi(ok, True, f"Dựng thử video giả 6 giây ({time.time() - t:.0f} giây)",
        f"Video: out/{name}.nhap.mp4 (xem rồi xoá được)" if ok else "Lỗi, gửi đoạn này cho Claude:\n" + (r.stdout + r.stderr)[-1500:])
    shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    print(f"Kiểm máy: {platform.system()} {platform.release()}, {platform.machine()}\n")
    for f in (kiem_python, kiem_ffmpeg, kiem_node, kiem_thu_vien_python, kiem_gpu, kiem_o_dia, kiem_kho):
        f()
    if "--dung-thu" in sys.argv and all(ok for ok, can, *_ in ket_qua if can):
        print("Đang dựng thử (1–3 phút)…", flush=True)
        dung_thu()
    for ok, can, ten, note in ket_qua:
        dau = "ĐẠT  " if ok else ("THIẾU" if can else "chưa ")
        print(f"[{dau}] {ten}" + (f"\n         → {note}" if note else ""))
    thieu = [ten for ok, can, ten, _ in ket_qua if can and not ok]
    print("\n" + ("Máy đủ điều kiện chạy app." if not thieu else f"Còn thiếu {len(thieu)} mục bắt buộc ở trên. Sửa xong chạy lại lệnh này."))
    sys.exit(1 if thieu else 0)
