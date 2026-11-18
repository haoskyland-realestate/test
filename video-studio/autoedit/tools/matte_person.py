"""Tách người nói khỏi nền cho preset A (đầu nhô khỏi khung).

Dùng:  python -I tools/matte_person.py work/<ten>/cut.mp4 work/<ten>/person.webm [fps]
Ra:    person.webm (VP9 có alpha, cùng kích thước video gốc). Chép vào assets/ của dự án HyperFrames.
Đo thực tế trên máy không GPU: clip 17 giây (419 khung ở 24 fps) mất khoảng 2 phút.
Cần:   pip install rembg onnxruntime opencv-python-headless numpy ; ffmpeg trong PATH.
"""
import os, sys, glob, subprocess, time
import numpy as np, cv2
from rembg import new_session, remove

src = sys.argv[1]
dst = sys.argv[2]
fps = sys.argv[3] if len(sys.argv) > 3 else '24'          # nên bằng fps của clip đã cắt
work = os.path.splitext(dst)[0] + '_tmp'
fr, out = work + '/frames', work + '/matte'
os.makedirs(fr, exist_ok=True); os.makedirs(out, exist_ok=True)
if not glob.glob(fr + '/*.png'):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', 'fps=' + fps, fr + '/f%04d.png'], check=True)
files = sorted(glob.glob(fr + '/*.png'))

sess = new_session('u2net_human_seg')                      # mô hình tự tải lần đầu
alphas, t0 = [], time.time()
for i, f in enumerate(files):
    im = cv2.imread(f)
    h, w = im.shape[:2]
    small = cv2.resize(im, (w * 3 // 4, h * 3 // 4), interpolation=cv2.INTER_AREA)   # chạy ở độ phân giải thấp cho nhanh
    a = np.array(remove(cv2.cvtColor(small, cv2.COLOR_BGR2RGB), session=sess, only_mask=True))
    if a.ndim == 3: a = a[..., 0]
    bw = (a > 127).astype(np.uint8)                        # chỉ giữ vùng lớn nhất (bỏ mảng rác)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bw)
    if n > 1:
        k = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        a = (a * cv2.dilate((lab == k).astype(np.uint8), np.ones((9, 9), np.uint8))).astype(np.uint8)
    alphas.append(a)
    if i % 50 == 0: print(i, len(files), round(time.time() - t0), 's', flush=True)

for i, f in enumerate(files):                              # làm mượt alpha theo thời gian để tóc không nhấp nháy
    lo, hi = max(0, i - 1), min(len(alphas), i + 2)
    m = cv2.GaussianBlur(np.mean([alphas[j].astype(np.float32) for j in range(lo, hi)], axis=0), (0, 0), 1.2)
    im = cv2.imread(f)
    h, w = im.shape[:2]
    a = cv2.GaussianBlur(cv2.resize(m.astype(np.uint8), (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), 1.0)
    cv2.imwrite(out + '/m%04d.png' % (i + 1), np.dstack([im, a]))

subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', fps, '-i', out + '/m%04d.png', '-c:v', 'libvpx-vp9',
                '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '20', '-auto-alt-ref', '0', dst], check=True)
print('XONG', dst, round(time.time() - t0), 's')
