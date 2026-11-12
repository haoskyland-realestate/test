"""Nhạc nền tổng hợp (không bản quyền) + tiếng 'vút' ở các mốc chuyển cảnh.
Dùng: python3 music.py <tổng giây> <file ra .wav> [mốc chuyển cảnh giây ...]"""
import sys, wave, numpy as np
SR = 44100
total = float(sys.argv[1]); out = sys.argv[2]; whooshes = [float(x) for x in sys.argv[3:]]
n = int(SR * total); t = np.arange(n) / SR
bpm = 96; beat = 60 / bpm; bar = beat * 4
mix = np.zeros(n)
# hợp âm Am - F - C - G, mỗi hợp âm 2 nhịp lớn
chords = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [261.6, 329.6, 392.0], [196.0, 246.9, 293.7]]
for k in range(int(total / (bar * 2)) + 1):
    s = int(k * bar * 2 * SR); e = min(n, int((k + 1) * bar * 2 * SR))
    if s >= n: break
    tt = t[s:e] - t[s]
    env = np.minimum(1, tt / 0.8) * np.minimum(1, (tt[-1] - tt + 0.01) / 0.8)
    for f in chords[k % 4]:
        for h, a in ((1, 1), (2, 0.35), (3, 0.12)):  # vài họa âm cho tiếng pad ấm
            mix[s:e] += a * np.sin(2 * np.pi * f * h * tt + h) * env * 0.05
    bass = chords[k % 4][0] / 2
    mix[s:e] += np.sin(2 * np.pi * bass * tt) * env * 0.12
# trống: kick từ giây 8, hi-hat từ giây 20, tắt 6 giây cuối
def add(at, sig):
    i = int(at * SR); j = min(n, i + len(sig)); mix[i:j] += sig[: j - i]
kt = np.arange(int(0.35 * SR)) / SR
kick = np.sin(2 * np.pi * (45 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9) * 0.5
rng = np.random.default_rng(1)
hat = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90) * 0.05
hat = np.diff(hat, prepend=0)  # bỏ bớt âm trầm
x = 8.0
while x < total - 6:
    add(x, kick)
    if x > 20: add(x + beat / 2, hat); add(x + beat * 1.5, hat)
    x += beat * 2
# tiếng vút: nhiễu lọc dải, to dần rồi nhỏ, đặt giữa tâm chuyển cảnh
for w in whooshes:
    L = int(0.9 * SR); wt = np.arange(L) / L
    noise = rng.standard_normal(L)
    sm = np.convolve(noise, np.ones(8) / 8, mode="same")  # lọc thấp thô
    sig = (sm - np.convolve(sm, np.ones(64) / 64, mode="same")) * np.sin(np.pi * wt) ** 2 * 0.9
    add(max(0, w - 0.45), sig)
mix = np.tanh(mix * 1.4) * 0.8
fade = np.minimum(1, np.minimum(t / 1.5, (total - t) / 3))
st = np.stack([mix * fade, np.roll(mix, 300) * fade], axis=1)
with wave.open(out, "wb") as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
print("music", out, total, "s,", len(whooshes), "whooshes")
