#!/usr/bin/env python3
"""Tách người khỏi nền cho hiệu ứng chữ nằm sau người (dự phòng khi
`npx hyperframes remove-background` không chạy được).

Dùng: python3 -I cutout.py assets/main.mp4 assets/cutout.webm --windows 8.6-11.4,20-23
Chỉ xử lý các khoảng thời gian cần (khối behindSubject, cộng 0.3 s mỗi đầu);
ngoài khoảng đó khung hình trong suốt. Cần: pip install "rembg[cpu]" pillow numpy
"""
import argparse, json, subprocess, sys
import numpy as np
from PIL import Image
from rembg import new_session, remove

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--windows", default="", help="a-b,c-d (giây); bỏ trống = cả video")
ap.add_argument("--pad", type=float, default=0.3)
ap.add_argument("--model", default="u2net_human_seg")
a = ap.parse_args()

pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
    "stream=width,height,r_frame_rate", "-of", "json", a.src]))["streams"][0]
W, H = pr["width"], pr["height"]; n, d = map(int, pr["r_frame_rate"].split("/")); fps = n / d
wins = [tuple(float(x) for x in w.split("-")) for w in a.windows.split(",") if w]
wins = [(s - a.pad, e + a.pad) for s, e in wins]
need = lambda t: not wins or any(s <= t <= e for s, e in wins)

sess = new_session(a.model)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", f"{n}/{d}",
    "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "32", "-deadline", "realtime", "-cpu-used", "8",
    "-row-mt", "1", "-g", str(round(fps)), a.out], stdin=subprocess.PIPE)
blank = np.zeros((H, W, 4), np.uint8).tobytes()
i = done = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = i / fps
    if need(t):
        img = Image.frombytes("RGB", (W, H), buf)
        small = img.resize((W // 2, H // 2))
        mask = remove(small, session=sess, only_mask=True).resize((W, H), Image.BILINEAR)
        rgba = img.convert("RGBA"); rgba.putalpha(mask)
        enc.stdin.write(rgba.tobytes()); done += 1
    else:
        enc.stdin.write(blank)
    i += 1
    if i % 60 == 0: print(f"{i} khung, {done} đã tách", file=sys.stderr)
enc.stdin.close(); enc.wait(); dec.wait()
print(json.dumps({"ok": enc.returncode == 0, "frames": i, "segmented": done, "out": a.out}))
