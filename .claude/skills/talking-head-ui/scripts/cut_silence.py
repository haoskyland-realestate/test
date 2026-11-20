#!/usr/bin/env python3
"""Cắt khoảng lặng khỏi video talking head, xuất main.mp4 (keyframe mỗi giây cho HyperFrames).

Dùng: python3 -I cut_silence.py input.mp4 assets/main.mp4 [--db -35] [--min 0.45] [--pad 0.12]
In ra JSON danh sách đoạn giữ lại (thời gian gốc) để đối chiếu.
"""
import argparse, json, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--db", type=float, default=-35, help="ngưỡng lặng dB")
ap.add_argument("--min", type=float, default=0.45, help="khoảng lặng tối thiểu để cắt (s)")
ap.add_argument("--pad", type=float, default=0.12, help="giữ lại mỗi bên khoảng lặng (s)")
a = ap.parse_args()

dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.src]))
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.src, "-af", f"silencedetect=n={a.db}dB:d={a.min}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))

keep, t = [], 0.0
for s, e in sil:
    s2, e2 = s + a.pad, e - a.pad
    if e2 - s2 <= 0.05: continue
    if s2 > t: keep.append((t, s2))
    t = e2
if t < dur: keep.append((t, dur))
keep = [(round(s, 3), round(e, 3)) for s, e in keep if e - s > 0.08]

parts = "".join(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[a{i}];" for i, (s, e) in enumerate(keep))
parts += "".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-filter_complex", parts, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out], check=True)
new = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.out]))
print(json.dumps({"ok": True, "source": round(dur, 2), "output": round(new, 2), "removed": round(dur - new, 2), "keep": keep}))
