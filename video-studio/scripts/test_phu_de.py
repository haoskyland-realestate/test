"""Kiểm tra cách chia dòng phụ đề. Chạy: python3 scripts/test_phu_de.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phu_de import nhom_tu, dinh_dang

w = lambda t, s, e: (t, s, e)
# ngắt ở dấu câu
assert [x[2] for x in nhom_tu([w("Xin", 0, .3), w("chào.", .3, .6), w("Em", .7, .9), w("là", .9, 1)])] == ["Xin chào.", "Em là"]
# ngắt khi ngừng nói lâu
r = nhom_tu([w("một", 0, .3), w("hai", 1.2, 1.5)])
assert [x[2] for x in r] == ["một", "hai"] and r[1][0] == 1.2
# tối đa 7 từ một dòng
r = nhom_tu([w(chr(97 + i), i * .2, i * .2 + .15) for i in range(10)])
assert [len(x[2].split()) for x in r] == [7, 3], r
# không quá 2,8 giây một dòng
r = nhom_tu([w("a", 0, 1.0), w("b", 1.1, 2.0), w("c", 2.1, 3.0)])
assert len(r) == 2, r
assert nhom_tu([]) == []
# Số điện thoại bị ngắt nhịp nói vẫn hiện cùng một dòng, tách nhóm, tô nổi
r = nhom_tu([w("liên", 0, .2), w("hệ", .2, .4), w("em", .4, .6), w("0986", .6, 1.4), w("986049", 2.2, 3.4), w("Cảm", 3.9, 4.1), w("ơn", 4.1, 4.3)])
assert r[0][2] == "liên hệ em *0986* *986* *049*", r
assert r[1][2] == "Cảm ơn", r
# Số + đơn vị, tên riêng nhiều chữ
assert dinh_dang("giá 2,5 tỷ một căn") == "giá *2,5* *tỷ* một căn"
assert dinh_dang("dự án Gladia Khang Điền thì") == "dự án *Gladia* *Khang* *Điền* thì"
assert dinh_dang("Xin chào anh chị") == "Xin chào anh chị"
r = nhom_tu([w("dự", 0, .2), w("án", .2, .4), w("Gladia", .4, .8), w("Khang", 1.5, 1.8), w("Điền", 1.8, 2.0)])
assert len(r) == 1, r
print("OK")
