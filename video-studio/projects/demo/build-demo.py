"""Tạo tài liệu cho video mẫu: giọng đọc giả (espeak-ng), phụ đề, logo/cảnh kết giả, nhạc giả, và edl.json.
Chạy trong thư mục video-studio: python3 projects/demo/build-demo.py  (cần ffmpeg, espeak-ng, Pillow)."""
import json, subprocess, wave, os, struct, math
from PIL import Image, ImageDraw, ImageFont

D = "projects/demo"; M = f"{D}/media"; os.makedirs(M, exist_ok=True)
SENT = [
  "Trước khi nói về căn nào, em hỏi chị một câu: mục tiêu của chị là gì?",
  "Ở để ở, hay giữ để có dòng tiền?",
  "Nếu để có dòng tiền, con số cần nhìn là tiền còn lại mỗi tháng, sau khi trừ tiền vay.",
  "Rồi tự hỏi tiếp: nếu giữ năm năm, rủi ro lớn nhất là gì?",
  "Có lợi ích thì có rủi ro. Nói rõ cả hai, chị quyết định sẽ chắc hơn.",
  "Hào Sky Land. Nhắn em nếu chị muốn cùng tính thử.",
]
GAP, TAIL = 0.35, 0.6
rate = 22050
pcm, durs = b"", []
for i, t in enumerate(SENT):
    w = f"{M}/s{i}.wav"
    subprocess.run(["espeak-ng", "-v", "vi", "-s", "140", "-w", w, t], check=True)
    with wave.open(w) as f:
        rate = f.getframerate(); data = f.readframes(f.getnframes())
    durs.append(len(data) / 2 / rate)
    pad = TAIL if i == len(SENT) - 1 else GAP
    pcm += data + b"\0\0" * int(rate * pad)
with wave.open(f"{M}/voice.wav", "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(pcm)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{M}/voice.wav", "-af", "volume=2.0", "-c:a", "aac", f"{M}/voice.m4a"], check=True)

def ts(x): return f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x%1*1000):03}"
t0, srt, scenes = 0.0, "", []
# clip: nguồn video; in: mốc bắt đầu; focus: lệch khung dọc khi cắt từ video ngang
plan = [("aerial", 2, 0), ("aerial", 8, -0.7), ("card", 0, 0), ("aerial", 16, 0.7), ("aerial", 22, -0.3), (None, 0, 0)]
for i, (t, d) in enumerate(zip(SENT, durs)):
    seg = d + (TAIL if i == len(SENT) - 1 else GAP)
    srt += f"{i+1}\n{ts(t0)} --> {ts(t0+d)}\n{t}\n\n"
    src, start, focus = plan[i]
    if src is None: scenes.append({"image": "media/outro.png", "dur": round(seg, 2)})
    else:
        path = "../../out/aerial.hyperframes.mp4" if src == "aerial" else "../../out/card.hyperframes.mp4"
        scenes.append({"clip": path, "in": start, "out": round(start + seg, 2), "focus": focus})
    t0 += seg
open(f"{D}/captions.srt", "w", encoding="utf8").write(srt)

# logo và cảnh kết GIẢ (chữ), thay bằng bộ nhận diện thật của Hào
font = lambda s: ImageFont.truetype(subprocess.check_output(["fc-match", "-f", "%{file}", "Inter:bold"]).decode(), s)
logo = Image.new("RGBA", (720, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(logo)
d.text((4, 4), "HÀO SKY LAND", font=font(88), fill=(0, 0, 0, 120)); d.text((0, 0), "HÀO SKY LAND", font=font(88), fill=(255, 255, 255, 235))
logo.save(f"{M}/logo.png")
out = Image.new("RGB", (1080, 1920), (11, 27, 43)); d = ImageDraw.Draw(out)
d.text((540, 860), "HÀO SKY LAND", font=font(96), fill=(255, 255, 255), anchor="mm")
d.rectangle((340, 930, 740, 934), fill=(201, 164, 92))
d.text((540, 1010), "Nhắn em nếu chị muốn cùng tính thử", font=font(44), fill=(210, 220, 230), anchor="mm")
out.save(f"{M}/outro.png")

# nhạc nền GIẢ: hợp âm êm, chỉ để thử tính năng trộn nhạc
secs = int(t0) + 3
samples = bytearray()
for n in range(rate * secs):
    t = n / rate; env = min(1, t / 2, (secs - t) / 2)
    v = sum(math.sin(2 * math.pi * f * t) for f in (220, 277.2, 329.6)) / 3 * (0.6 + 0.4 * math.sin(t * 0.6)) * env
    samples += struct.pack("<h", int(v * 12000))
with wave.open(f"{M}/music.wav", "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate); f.writeframes(bytes(samples))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{M}/music.wav", "-c:a", "aac", f"{M}/music.m4a"], check=True)

json.dump({"platform": "tiktok", "voice": "media/voice.m4a", "music": "media/music.m4a", "musicVolume": 0.07,
           "logo": "media/logo.png", "captions": "captions.srt", "scenes": scenes},
          open(f"{D}/edl.json", "w"), ensure_ascii=False, indent=2)
print("Tổng", round(t0, 1), "giây;", len(scenes), "cảnh")
