"""Kiểm zoom êm: đo bề rộng ô trắng ở giữa khung theo thời gian qua zoompan thật. Chạy: python3 scripts/test_zoom.py"""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from effects import zoom_bieu_thuc

W, H, FPS = 360, 640, 30
zs = [{"start": 1.0, "dur": 2.0, "scale": 1.08}]
z = zoom_bieu_thuc(zs, FPS)
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=4,drawbox=x=120:y=183:w=120:h=120:color=white:t=fill",
                      "-vf", f"zoompan=z='{z}':x='(iw-iw/zoom)*0.5':y='(ih-ih/zoom)*0.38':d=1:s={W}x{H}:fps={FPS}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                     capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
rong = np.array([(fr[243] > 128).sum() for fr in f], float) / 120  # hàng giữa ô trắng; 1.0 = chưa phóng
assert len(f) == 120, len(f)
assert abs(rong[int(0.9 * FPS)] - 1) < 0.01, rong[27]                       # trước đoạn: chưa phóng
assert abs(rong[int(2.0 * FPS)] - 1.08) < 0.02, rong[60]                    # giữa đoạn: đủ 108%
assert abs(rong[-1] - 1) < 0.01, rong[-1]                                    # sau đoạn: về 100%
assert np.abs(np.diff(rong)).max() < 0.03, np.abs(np.diff(rong)).max()      # không nhảy cỡ giữa hai khung (cũ nhảy 8% trong 1 khung)
assert (np.diff(rong[30:45]) > 0).all() or abs(rong[44] - 1.08) < 0.02       # đẩy vào đi lên đều
print("OK", f"đầu {rong[29]:.3f} · giữa {rong[60]:.3f} · cuối {rong[-1]:.3f} · bước lớn nhất {np.abs(np.diff(rong)).max():.4f}")
