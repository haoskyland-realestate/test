"""Kiểm tra cách chia dòng phụ đề. Chạy: python3 scripts/test_phu_de.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phu_de import nhom_tu

w = lambda t, s, e: (t, s, e)
# ngắt ở dấu câu
assert [x[2] for x in nhom_tu([w("Xin", 0, .3), w("chào.", .3, .6), w("Em", .7, .9), w("là", .9, 1)])] == ["Xin chào.", "Em là"]
# ngắt khi ngừng nói lâu
r = nhom_tu([w("một", 0, .3), w("hai", 1.2, 1.5)])
assert [x[2] for x in r] == ["một", "hai"] and r[1][0] == 1.2
# tối đa 7 từ một dòng
r = nhom_tu([w(str(i), i * .2, i * .2 + .15) for i in range(10)])
assert [len(x[2].split()) for x in r] == [7, 3], r
# không quá 2,8 giây một dòng
r = nhom_tu([w("a", 0, 1.0), w("b", 1.1, 2.0), w("c", 2.1, 3.0)])
assert len(r) == 2, r
assert nhom_tu([]) == []
print("OK")
