"""Phụ đề tự động từ giọng nói (tiếng Việt) bằng Whisper, ghi vào timeline.json.
Chạy trong video-studio:  python3 scripts/phu_de.py projects/<tên>
- Mỗi file footage nhận dạng một lần, lưu đệm ở build/transcripts/ (đổi đoạn cắt không phải nhận dạng lại).
- Chỉ thay các phụ đề tự sinh ("auto": true); phụ đề tự gõ giữ nguyên.
Cần: pip install faster-whisper numpy. Lần đầu tải mô hình ~1,6 GB (đổi bằng biến WHISPER_MODEL)."""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout

MAX_WORDS, MAX_SEC, PAUSE = 7, 2.8, 0.45  # một dòng phụ đề: tối đa 7 từ / 2,8 giây; ngừng nói 0,45s thì xuống dòng


UNITS = {"tỷ", "tỉ", "triệu", "nghìn", "ngàn", "trăm", "m2", "m²", "mét", "km", "năm", "tháng", "ngày", "phút", "giờ",
         "%", "phần", "đồng", "vnđ", "usd", "căn", "tầng", "phòng", "lô", "block", "tháp"}


def dinh(a, b):
    """Hai từ phải hiện cùng nhau: số liền số (số điện thoại), số + đơn vị (2,5 tỷ, 120 m2), tên riêng nhiều chữ (Gladia Khang Điền)."""
    if any(ch.isdigit() for ch in a) and (any(ch.isdigit() for ch in b) or re.sub(r"[^\w%²]", "", b.lower()) in UNITS):
        return True
    return a[:1].isupper() and b[:1].isupper() and not re.search(r"[.?!,;:]$", a)


def nhom_tu(words):
    """[(từ, bắt đầu, kết thúc)] theo thời gian → [(bắt đầu, kết thúc, câu)]: ngắt ở dấu câu, chỗ ngừng, hoặc khi dòng dài.
    Thông tin cần liền mạch (số điện thoại, giá, diện tích, tên riêng) không bị ngắt, dù người nói ngừng giữa chừng."""
    lines, cur = [], []
    for w in words:
        stick = cur and dinh(cur[-1][0], w[0]) and len(cur) < MAX_WORDS + 5
        if cur and not stick and (w[1] - cur[-1][2] >= PAUSE or len(cur) >= MAX_WORDS or w[2] - cur[0][1] > MAX_SEC):
            lines.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.?!,;:]$", w[0]):
            lines.append(cur); cur = []
    if cur:
        lines.append(cur)
    return [(ln[0][1], ln[-1][2], dinh_dang(" ".join(x[0] for x in ln))) for ln in lines]


def dinh_dang(text):
    """Số điện thoại tách nhóm dễ đọc (0986 986 049); số, đơn vị và tên riêng được đánh dấu *…* để tô nổi."""
    def phone(m):
        d = re.sub(r"\D", "", m[0])
        return " ".join([d[:4], d[4:7], d[7:]]) if len(d) in (10, 11) and d[0] == "0" else m[0]
    text = re.sub(r"\b\d[\d ]{7,}\d\b", phone, text)
    ws = text.split(" ")
    hl = [False] * len(ws)
    for i, w in enumerate(ws):
        if re.search(r"\d", w):
            hl[i] = True
            if i + 1 < len(ws) and re.sub(r"[^\w%²]", "", ws[i + 1].lower()) in UNITS:
                hl[i + 1] = True
        if i and w[:1].isupper() and (ws[i - 1][:1].isupper() or (i + 1 < len(ws) and ws[i + 1][:1].isupper())):
            hl[i] = True  # tên riêng nhiều chữ (không tính chữ hoa đầu câu đứng một mình)
    return " ".join(f"*{w}*" if h and not w.startswith("*") else w for w, h in zip(ws, hl))


def nhan_dang(path, cache):
    if os.path.exists(cache):
        return json.load(open(cache, encoding="utf8"))
    import numpy as np
    from faster_whisper import WhisperModel
    import ctranslate2
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    if not pcm:
        words = []
    else:
        audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
        name = os.environ.get("WHISPER_MODEL", "large-v3-turbo")
        # PC có card NVIDIA thì thử chạy bằng card; thiếu thư viện CUDA thì tự về CPU
        tries = ([("cuda", "float16")] if ctranslate2.get_cuda_device_count() > 0 else []) + [("cpu", "int8")]
        for k, (dev, ct) in enumerate(tries):
            try:
                segs, _ = WhisperModel(name, device=dev, compute_type=ct).transcribe(
                    audio, language="vi", word_timestamps=True, vad_filter=True, beam_size=5)
                words = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words if w.word.strip()]
                break
            except Exception as ex:
                if k == len(tries) - 1:
                    raise
                print(f"Không chạy được bằng card đồ họa ({ex}); chuyển sang CPU", flush=True)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    json.dump(words, open(cache, "w", encoding="utf8"), ensure_ascii=False)
    return words


def main(proj):
    p = os.path.join(proj, "timeline.json")
    tl = json.load(open(p, encoding="utf8"))
    if (errs := check(tl)):
        sys.exit("timeline.json chưa hợp lệ:\n- " + "\n- ".join(errs))
    L = layout(tl)
    subs = []
    for i, c in enumerate(tl["clips"]):
        raw = os.path.join(proj, "build", "raw", c["file"])
        if not os.path.exists(raw) and c.get("id"):  # tải từ Drive như bộ dựng
            os.makedirs(os.path.dirname(raw), exist_ok=True)
            subprocess.run(["curl", "-sS", "-L", "--retry", "3", "-o", raw,
                            f"https://drive.usercontent.google.com/download?id={c['id']}&export=download&confirm=t"], check=True)
        if not os.path.exists(raw):
            sys.exit(f"Chưa có footage {c['file']} trong build/raw và cảnh không có 'id' Drive để tải")
        print(f"Nhận dạng đoạn {i + 1}: {c['file']}", flush=True)
        words = nhan_dang(raw, os.path.join(proj, "build", "transcripts", c["file"] + ".json"))
        a, b = c["in"], c["in"] + c["dur"]
        # từ nằm trong đoạn cắt (theo điểm giữa của từ), đổi sang giờ trên video thành phẩm
        inside = [(w, L["starts"][i] + max(s, a) - a, L["starts"][i] + min(e, b) - a) for w, s, e in words if a <= (s + e) / 2 < b]
        for s, e, text in nhom_tu(inside):
            subs.append({"start": round(s, 2), "dur": round(max(0.6, e - s + 0.1), 2), "text": text, "auto": True})
    for x, y in zip(subs, subs[1:]):  # không để dòng trước đè dòng sau
        x["dur"] = round(max(0.3, min(x["dur"], y["start"] - x["start"])), 2)
    if subs:
        subs[-1]["dur"] = round(min(subs[-1]["dur"], L["total"] - subs[-1]["start"]), 2)
    tl["subtitles"] = [x for x in tl.get("subtitles", []) if not x.get("auto")] + subs
    tl["subtitles"].sort(key=lambda x: x["start"])
    if (errs := check(tl)):
        sys.exit("Phụ đề tạo ra chưa hợp lệ:\n- " + "\n- ".join(errs))
    tmp = p + ".tmp"
    json.dump(tl, open(tmp, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    print(f"Xong: {len(subs)} dòng phụ đề tự động")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Dùng: python3 scripts/phu_de.py projects/<tên>")
    main(os.path.abspath(sys.argv[1]))
