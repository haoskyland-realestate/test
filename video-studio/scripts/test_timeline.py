"""Kiểm tra nhanh định dạng timeline. Chạy: python3 scripts/test_timeline.py"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout

ok = {
    "version": 1, "meta": {"platform": "tiktok"},
    "clips": [{"file": "a.mp4", "in": 0, "dur": 5}, {"file": "b.mp4", "in": 2, "dur": 4}, {"file": "c.mp4", "in": 0, "dur": 3}],
    "transitions": [{"type": "cube-h"}, {"type": "cut"}],
    "texts": [{"kind": "line", "start": 0.5, "dur": 4, "lines": ["Xin chào"]}],
    "audio": {"music": "synth"},
}
assert check(ok) == [], check(ok)
L = layout(ok)
assert L["starts"] == [0, 5.8, 9.8] and abs(L["total"] - 12.8) < 1e-9, L
assert L["transitions"] == [(5, 0.8, "cube-h"), (9.8, 0.0, "cut")], L


def bad(change, expect):
    tl = copy.deepcopy(ok); change(tl)
    errs = check(tl)
    assert any(expect in m for m in errs), (expect, errs)


bad(lambda t: t["clips"][1].pop("dur"), "Cảnh 2: thiếu 'dur'")
bad(lambda t: t["transitions"].pop(), "Cần 2 chuyển cảnh")
bad(lambda t: t["transitions"][0].update(type="spin"), "kiểu 'spin' chưa có")
bad(lambda t: t["texts"][0].update(start=12), "nằm ngoài video")
bad(lambda t: t["texts"][0].update(kind="section"), "thiếu num, title")
bad(lambda t: t["meta"].update(platform="facebook"), "'platform' phải là")
yt = copy.deepcopy(ok); yt["meta"]["platform"] = "youtube"; yt["audio"]["music"] = "nhac nen.mp3"
assert check(yt) == [], check(yt)
bad(lambda t: t["audio"].update(music="../a.mp3"), "audio.music")
bad(lambda t: t["audio"].update(music="a.exe"), "audio.music")
bad(lambda t: t["meta"].update(style="neon"), "Phong cách 'neon' chưa có")
bad(lambda t: t["clips"][0].update(look="xyz"), "chỉnh màu 'xyz' chưa có")
bad(lambda t: t["texts"][0].update(anim="spin"), "hiệu ứng 'spin' chưa có")
bad(lambda t: t["texts"].append({"kind": "stat", "start": 1, "dur": 2, "value": "abc", "label": "x"}), "phải là số")
bad(lambda t: t["texts"].append({"kind": "checklist", "start": 1, "dur": 2}), "thiếu items")
bad(lambda t: t.update(subtitles=[{"start": 1, "dur": 2}]), "Phụ đề 1: thiếu text")
bad(lambda t: t.update(zooms=[{"start": 1, "dur": 2, "scale": 3}]), "Zoom 1: 'scale' từ 1")
bad(lambda t: t.update(broll=[{"start": 12, "dur": 2, "file": "x.mp4", "in": 0}]), "Cảnh trám 1: 12s")
bad(lambda t: t.update(cards=[{"start": 1, "dur": 2}]), "Minh họa 1: thiếu title")
bad(lambda t: t["audio"].update(music_volume=5), "music_volume")
t2 = copy.deepcopy(ok); t2["transitions"][0]["type"] = "fade"
assert abs(layout(t2)["total"] - 12.5) < 1e-9  # fade mặc định 0.5s

# Mọi timeline.json trong projects/ phải hợp lệ
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "projects")
for name in sorted(os.listdir(root)):
    p = os.path.join(root, name, "timeline.json")
    if os.path.exists(p):
        errs = check(json.load(open(p, encoding="utf8")))
        assert errs == [], (name, errs)
        print("hợp lệ:", name)
print("OK")
