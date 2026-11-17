"""Kiểm thư viện Python TRƯỚC khi chạy việc nặng (master cut, phụ đề, chữ sau đầu), báo rõ đang dùng Python nào và lệnh cài đúng cho chính Python đó.
Lỗi Hào gặp 17/11 trên PC: app chạy bằng một bản Python khác bản đã cài thư viện → "No module named 'cv2'" giữa chừng.
Dùng:  from thu_vien import can;  can("cv2", "numpy")      ·   tự kiểm: python scripts/thu_vien.py --tu-kiem"""
import importlib.util, sys

GOI = {"numpy": "numpy", "cv2": '"opencv-python-headless<5"', "faster_whisper": "faster-whisper",
       "opentimelineio": "opentimelineio otio-fcp-adapter", "onnxruntime": "onnxruntime"}


def thieu(*mods):
    return [m for m in mods if importlib.util.find_spec(m) is None]


def lenh_cai(mods):
    return f'"{sys.executable}" -m pip install ' + " ".join(GOI.get(m, m) for m in mods)


def can(*mods):
    """Thiếu thì dừng với lời nhắn tiếng Việt (không traceback), chỉ cài đúng gói còn thiếu."""
    t = thieu(*mods)
    if t:
        sys.exit(f"THIẾU THƯ VIỆN: {', '.join(t)}\nPython đang dùng: {sys.executable} (bản {sys.version.split()[0]})\n"
                 f"Cài vào đúng Python này:  {lenh_cai(t)}\nHoặc chạy lại setup-windows.ps1 / setup-mac.sh rồi mở app bằng chay-studio.")


if __name__ == "__main__":
    assert thieu("os", "json") == [] and thieu("khong_co_goi_nay_123") == ["khong_co_goi_nay_123"]
    assert sys.executable in lenh_cai(["cv2"]) and "opencv-python-headless" in lenh_cai(["cv2"])
    try:
        can("khong_co_goi_nay_123"); raise AssertionError("phải dừng")
    except SystemExit as e:
        assert "THIẾU THƯ VIỆN" in str(e.code) and sys.executable in str(e.code)
    print("OK")
