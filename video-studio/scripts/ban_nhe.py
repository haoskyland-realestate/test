"""Bản nhẹ của footage (Hào chốt 18/11): mỗi file 4K HDR đổi MỘT lần thành bản 540p (cạnh ngắn 540, màu đã chuyển sang thường, giữ tiếng),
lưu ở build/nhe/<file>.mp4. Phân tích hình (master cut), storyboard, bản xem 540×960 và app đều đọc bản này; chỉ bản cuối đọc 4K gốc.
Máy có card NVIDIA thì giải nén bằng card (hw()); lỗi thì tự làm lại bằng CPU."""
import functools, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mau import chuyen_tong
from cau_hinh import lay as cau_hinh

CO = "scale='if(gt(iw,ih),-2,540)':'if(gt(iw,ih),540,-2)'"  # cạnh ngắn 540: dọc 540×960, ngang 960×540


@functools.lru_cache(None)
def hw():
    """["-hwaccel", "cuda"] nếu máy có card NVIDIA và FFmpeg hỗ trợ, ngược lại []."""
    if not shutil.which("nvidia-smi"):
        return []
    out = subprocess.run(["ffmpeg", "-hide_banner", "-hwaccels"], capture_output=True, text=True).stdout
    return ["-hwaccel", "cuda"] if "cuda" in out.split() else []


def duong_dan(B, f):
    return os.path.join(B, "nhe", f + ".mp4")


def lenh(raw, out, dung_card=True):
    return ["ffmpeg", "-nostdin", "-v", "error", "-y", *(hw() if dung_card else []), "-i", raw, "-vf", chuyen_tong(raw) + CO,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(cau_hinh("hinh.nhe_crf")), "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]


def tao(raw, out):
    """Tạo bản nhẹ (ghi tạm rồi đổi tên: dừng giữa chừng không để lại file hỏng). Trả True nếu tạo được."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp.mp4"
    for card in ((True, False) if hw() else (False,)):
        if subprocess.run(lenh(raw, tmp, card)).returncode == 0:
            os.replace(tmp, out)
            return True
    return False


def lay(B, f):
    """Đường dẫn bản nhẹ của build/raw/<f> (tạo nếu chưa có hoặc cũ hơn file gốc); không tạo được thì trả file gốc."""
    raw, p = os.path.join(B, "raw", f), duong_dan(B, f)
    if not os.path.exists(raw):
        return raw
    if os.path.exists(p) and os.path.getmtime(p) >= os.path.getmtime(raw):
        return p
    print(f"Tạo bản nhẹ 540p: {f}", flush=True)
    return p if tao(raw, p) else raw


def _tu_kiem():
    import tempfile
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "raw"))
    raw = os.path.join(d, "raw", "a.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30", "-f", "lavfi", "-i", "sine=f=300",
                    "-t", "1", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", raw], check=True)
    p = lay(d, "a.mp4")
    wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                        capture_output=True, text=True).stdout.strip()
    assert p == duong_dan(d, "a.mp4") and wh == "540,960", (p, wh)
    assert lay(d, "a.mp4") == p and lay(d, "khong-co.mp4").endswith("khong-co.mp4")
    shutil.rmtree(d)
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):  # tạo trước bản nhẹ cho cả dự án
        B = os.path.join(os.path.abspath(sys.argv[1]), "build")
        for f in sorted(os.listdir(os.path.join(B, "raw"))):
            if f.lower().endswith((".mp4", ".mov", ".m4v", ".mkv", ".mts")):
                lay(B, f)
        print("Xong bản nhẹ." + (" (dùng card NVIDIA)" if hw() else ""))
    else:
        sys.exit("Dùng: python3 scripts/ban_nhe.py projects/<tên>")
