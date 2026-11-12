"""Định dạng timeline v1: một file timeline.json mô tả cả video. Dùng chung cho bộ dựng và app sau này.

{
  "version": 1,
  "meta": {"platform": "tiktok"},
  "clips": [{"file": "a.mp4", "id": "<id Drive>", "in": 13.0, "dur": 9.2, "focus": 0}],
  "transitions": [{"type": "cube-h"}],          # giữa cảnh i và i+1; kiểu: cut, cube-h, cube-v
  "texts": [{"kind": "hook", "start": 0.4, "dur": 8.6, "tag": "...", "lines": ["..."]}],
  "audio": {"music": "synth", "whoosh": true}
}
Mốc giờ của chữ (start) tính trên video thành phẩm (đã cộng chuyển cảnh). Từ tô vàng viết *từ*.
"""

TRANSITIONS = {"cut": 0.0, "cube-h": 0.8, "cube-v": 0.8}  # tên: độ dài mặc định (giây)
TEXT_KINDS = {"hook": ["tag", "lines"], "section": ["num", "title", "lines"], "line": ["lines"], "outro": ["lines"]}


def layout(tl):
    """Mốc bắt đầu từng cảnh, vị trí từng chuyển cảnh (bắt đầu, độ dài, kiểu) và tổng thời lượng."""
    starts, trs, t = [], [], 0.0
    clips = tl["clips"]
    for i, c in enumerate(clips):
        starts.append(t)
        t += c["dur"]
        if i < len(clips) - 1:
            tr = tl["transitions"][i]
            d = 0.0 if tr["type"] == "cut" else tr.get("dur", TRANSITIONS[tr["type"]])
            trs.append((t, d, tr["type"]))
            t += d
    return {"starts": starts, "transitions": trs, "total": t}


def check(tl):
    """Trả về danh sách lỗi (tiếng Việt). Rỗng là hợp lệ."""
    e = []
    if tl.get("version") != 1:
        e.append("'version' phải là 1")
    if tl.get("meta", {}).get("platform", "tiktok") != "tiktok":
        e.append("Hiện chỉ hỗ trợ 'platform': 'tiktok' (khung dọc 9:16)")
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
    trs = tl.get("transitions", [])
    if clips and len(trs) != len(clips) - 1:
        e.append(f"Cần {len(clips) - 1} chuyển cảnh (giữa các cảnh), đang có {len(trs)}")
    for i, t in enumerate(trs, 1):
        if t.get("type") not in TRANSITIONS:
            e.append(f"Chuyển cảnh {i}: kiểu '{t.get('type')}' chưa có (đang có: {', '.join(TRANSITIONS)})")
    music = tl.get("audio", {}).get("music", "synth")
    if music not in ("synth", None):
        e.append("'audio.music' hiện chỉ nhận 'synth' (nhạc tổng hợp) hoặc null (không nhạc)")
    if e:
        return e
    total = layout(tl)["total"]
    for i, x in enumerate(tl.get("texts", []), 1):
        kind = x.get("kind", "line")
        if kind not in TEXT_KINDS:
            e.append(f"Chữ {i}: kiểu '{kind}' chưa có (đang có: {', '.join(TEXT_KINDS)})")
            continue
        missing = [k for k in ["start", "dur"] + TEXT_KINDS[kind] if k not in x]
        if missing:
            e.append(f"Chữ {i}: thiếu {', '.join(missing)}")
        elif x["start"] < 0 or x["dur"] <= 0 or x["start"] + x["dur"] > total + 0.01:
            e.append(f"Chữ {i}: {x['start']}s + {x['dur']}s nằm ngoài video ({total:.2f}s)")
    return e
