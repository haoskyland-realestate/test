"""Định dạng timeline v1: một file timeline.json mô tả cả video. Dùng chung cho bộ dựng và app sau này.

{
  "version": 1,
  "meta": {"platform": "tiktok", "style": "hien-dai"},     # platform: tiktok (dọc 9:16) | youtube (ngang 16:9); phong cách: xem scripts/effects.py
  "clips": [{"file": "a.mp4", "id": "<id Drive>", "in": 13.0, "dur": 9.2, "focus": 0, "look": "am-sang"}],   # fit: crop | blur (bỏ trống: tự chọn)
  "transitions": [{"type": "cube-h"}],          # giữa cảnh i và i+1; tên trong effects.TRANSITIONS
  "texts": [{"kind": "hook", "anim": "rise", "start": 0.4, "dur": 8.6, "tag": "...", "lines": ["..."]}],
  "subtitles": [{"start": 0.2, "dur": 1.8, "text": "Phụ đề theo lời nói"}],
  "cards": [{"start": 5, "dur": 4, "step": "Bước 2", "title": "Giao cho ChatGPT", "items": ["Mở ChatGPT"]}],   # minh họa nền đen
  "zooms": [{"start": 3, "dur": 2, "scale": 1.07}],                    # phóng to khung (1.07 = 7%)
  "broll": [{"start": 8, "dur": 3, "file": "b.mp4", "id": "", "in": 0}],   # cảnh trám: phủ hình, giữ tiếng
  "audio": {"music": "synth", "whoosh": true, "voice": false, "music_volume": 1.0}   # voice: giữ tiếng gốc của cảnh
                                                # music: "synth" (nhạc tổng hợp), null (không nhạc) hoặc tên file nhạc trong build/raw/ (vd "nhac.mp3")
}
Mốc giờ của chữ (start) tính trên video thành phẩm (đã cộng chuyển cảnh). Từ tô vàng viết *từ*.
"""

import re

from effects import STYLES, LOOKS, TRANSITIONS, TEXT_ANIMS, TEXT_KINDS

PLATFORMS = {"tiktok": (1080, 1920, "TikTok / Reels / Shorts dọc 9:16"), "youtube": (1920, 1080, "YouTube ngang 16:9")}
AUDIO_EXT = r"\.(mp3|wav|m4a|aac|flac|ogg)$"


def size(tl):
    """(rộng, cao) khung hình theo nền tảng."""
    return PLATFORMS[tl.get("meta", {}).get("platform", "tiktok")][:2]


def layout(tl):
    """Mốc bắt đầu từng cảnh, vị trí từng chuyển cảnh (bắt đầu, độ dài, kiểu) và tổng thời lượng."""
    starts, trs, t = [], [], 0.0
    clips = tl["clips"]
    for i, c in enumerate(clips):
        starts.append(t)
        t += c["dur"]
        if i < len(clips) - 1:
            tr = tl["transitions"][i]
            d = 0.0 if tr["type"] == "cut" else tr.get("dur", TRANSITIONS[tr["type"]][0])
            trs.append((t, d, tr["type"]))
            t += d
    return {"starts": starts, "transitions": trs, "total": t}


def check(tl):
    """Trả về danh sách lỗi (tiếng Việt). Rỗng là hợp lệ."""
    e = []
    if tl.get("version") != 1:
        e.append("'version' phải là 1")
    meta = tl.get("meta", {})
    if meta.get("platform", "tiktok") not in PLATFORMS:
        e.append("'platform' phải là 'tiktok' (dọc 9:16) hoặc 'youtube' (ngang 16:9)")
    if meta.get("style", "hien-dai") not in STYLES:
        e.append(f"Phong cách '{meta.get('style')}' chưa có (đang có: {', '.join(STYLES)})")
    clips = tl.get("clips") or []
    if not clips:
        e.append("Chưa có cảnh nào trong 'clips'")
    for i, c in enumerate(clips, 1):
        for k in ("file", "in", "dur"):
            if k not in c:
                e.append(f"Cảnh {i}: thiếu '{k}'")
        if not isinstance(c.get("dur", 1), (int, float)) or c.get("dur", 1) <= 0:
            e.append(f"Cảnh {i}: 'dur' phải là số giây lớn hơn 0")
        if not -1 <= c.get("focus", 0) <= 1:
            e.append(f"Cảnh {i}: 'focus' phải từ -1 (lệch trái) đến 1 (lệch phải)")
        if c.get("fit", "crop") not in ("crop", "blur"):
            e.append(f"Cảnh {i}: 'fit' phải là 'crop' (phóng kín, cắt bớt) hoặc 'blur' (giữ trọn hình, nền mờ)")
        if c.get("look", "trung-tinh") not in LOOKS:
            e.append(f"Cảnh {i}: chỉnh màu '{c.get('look')}' chưa có (đang có: {', '.join(LOOKS)})")
    trs = tl.get("transitions", [])
    if clips and len(trs) != len(clips) - 1:
        e.append(f"Cần {len(clips) - 1} chuyển cảnh (giữa các cảnh), đang có {len(trs)}")
    for i, t in enumerate(trs, 1):
        if t.get("type") not in TRANSITIONS:
            e.append(f"Chuyển cảnh {i}: kiểu '{t.get('type')}' chưa có (đang có: {', '.join(TRANSITIONS)})")
    a = tl.get("audio", {})
    if not 0 <= a.get("music_volume", 1.0) <= 2:
        e.append("'audio.music_volume' phải từ 0 đến 2")
    music = a.get("music", "synth")
    if music not in ("synth", None) and not (isinstance(music, str) and re.search(AUDIO_EXT, music, re.I)
                                              and not re.search(r"[\\/]|^\.", music)):
        e.append("'audio.music' phải là 'synth' (nhạc tổng hợp), null (không nhạc) hoặc tên file nhạc .mp3/.wav/.m4a/.aac/.flac/.ogg")
    if e:
        return e
    total = layout(tl)["total"]
    for i, x in enumerate(tl.get("texts", []), 1):
        kind = x.get("kind", "line")
        if kind not in TEXT_KINDS:
            e.append(f"Chữ {i}: kiểu '{kind}' chưa có (đang có: {', '.join(TEXT_KINDS)})")
            continue
        if x.get("anim", "rise") not in TEXT_ANIMS:
            e.append(f"Chữ {i}: hiệu ứng '{x.get('anim')}' chưa có (đang có: {', '.join(TEXT_ANIMS)})")
        if kind == "stat" and not isinstance(x.get("value"), (int, float)):
            e.append(f"Chữ {i}: 'value' của số lớn phải là số")
        missing = [k for k in ["start", "dur"] + TEXT_KINDS[kind][0] if k not in x]
        if missing:
            e.append(f"Chữ {i}: thiếu {', '.join(missing)}")
        elif x["start"] < 0 or x["dur"] <= 0 or x["start"] + x["dur"] > total + 0.01:
            e.append(f"Chữ {i}: {x['start']}s + {x['dur']}s nằm ngoài video ({total:.2f}s)")
    for key, name, need in (("subtitles", "Phụ đề", ["text"]), ("cards", "Minh họa", ["title"]),
                            ("zooms", "Zoom", ["scale"]), ("broll", "Cảnh trám", ["file", "in"])):
        for i, x in enumerate(tl.get(key, []), 1):
            miss = [k for k in ["start", "dur"] + need if k not in x]
            if miss:
                e.append(f"{name} {i}: thiếu {', '.join(miss)}")
            elif x["start"] < 0 or x["dur"] <= 0 or x["start"] + x["dur"] > total + 0.01:
                e.append(f"{name} {i}: {x['start']}s + {x['dur']}s nằm ngoài video ({total:.2f}s)")
            elif key == "zooms" and not 1 <= x["scale"] <= 1.6:
                e.append(f"Zoom {i}: 'scale' từ 1 đến 1.6 (1.07 = phóng 7%)")
    return e
