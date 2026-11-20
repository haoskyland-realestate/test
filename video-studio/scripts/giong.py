"""Ghép giọng nói của các đoạn chính thành build/voice.wav, đúng mốc thời gian của video dựng ra (dùng chung cho dung.py và agent.py:
agent nhận dạng giọng trên chính file này mà không phải dựng cả video)."""
import os, subprocess

from timeline import layout


def tao(B, tl, ff):
    """ff(*tham số ffmpeg): hàm chạy ffmpeg của nơi gọi. Đoạn không có tiếng thì chèn lặng; chuyển cảnh có độ dài thì chèn lặng bằng đó."""
    shots, L = tl["clips"], layout(tl)
    n, vparts = len(shots), []
    for i, c in enumerate(shots):
        raw = f"{B}/raw/{c['file']}"
        has_a = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", raw],
                               capture_output=True, text=True).stdout.strip()
        src = ["-ss", str(c["in"]), "-t", str(c["dur"]), "-i", raw, "-vn"] if has_a else ["-f", "lavfi", "-t", str(c["dur"]), "-i", "anullsrc=r=44100:cl=stereo"]
        ff(*src, "-ac", "2", "-ar", "44100", "-t", str(c["dur"]), f"{B}/v{i}.wav"); vparts.append(f"{B}/v{i}.wav")
        if i < n - 1 and L["transitions"][i][1] > 0:
            ff("-f", "lavfi", "-t", str(L["transitions"][i][1]), "-i", "anullsrc=r=44100:cl=stereo", f"{B}/vs{i}.wav"); vparts.append(f"{B}/vs{i}.wav")
    open(f"{B}/vlist.txt", "w", encoding="utf8").write("".join(f"file '{p}'\n" for p in vparts))
    ff("-f", "concat", "-safe", "0", "-i", f"{B}/vlist.txt", "-c", "copy", f"{B}/voice.wav")
    return f"{B}/voice.wav"
