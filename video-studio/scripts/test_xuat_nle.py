"""Kiểm tra đổi giờ và phụ đề SRT khi xuất sang phần mềm dựng. Chạy: python3 scripts/test_xuat_nle.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xuat_nle import gio_nle, srt

tl = {"version": 1, "clips": [{"file": "a", "in": 0, "dur": 4}, {"file": "b", "in": 0, "dur": 4}, {"file": "c", "in": 0, "dur": 4}],
      "transitions": [{"type": "fade", "dur": 1.0}, {"type": "cut"}]}
f = gio_nle(tl)
assert f(2) == 2 and f(4.5) == 4 and f(6) == 5 and f(10) == 9  # bỏ 1 giây chuyển cảnh chèn thêm
s = srt([{"start": 6, "dur": 1.5, "text": "gọi *0986 986 049*"}], f)
assert s == "1\n00:00:05,000 --> 00:00:06,500\ngọi 0986 986 049\n", repr(s)
print("OK")
