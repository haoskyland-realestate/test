"""Kiểm tra master cut. Chạy: python3 scripts/test_master_cut.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from master_cut import nhip_phong, kep_tu, bo_noi_lai, doan_noi, doi_gio, lam_on_tu, im, nguong

# Từ kéo dài sau ngập ngừng được kẹp lại
assert kep_tu([["xin", 21.1, 22.2]]) == [["xin", 22.2 - 0.45, 22.2]]

# Ba lần chào (giống clip thật của Hào): giữ lần cuối
W = lambda s: [[t, a, b] for t, a, b in s]
words = W([("Xin", 11.1, 11.9), ("chào", 11.9, 12.2), ("anh", 12.2, 12.3), ("chị", 12.3, 12.5), ("thì", 12.5, 12.9), ("đang", 13.8, 14.1),
           ("xin", 19.3, 20.5), ("chào", 20.5, 20.7), ("anh", 20.7, 20.8), ("chị", 20.8, 21.0), ("thì", 21.0, 21.1),
           ("xin", 21.1, 22.2), ("chào", 23.7, 23.9), ("anh", 23.9, 24.0), ("chị", 24.0, 24.1), ("hiện", 24.1, 24.6), ("tại", 24.6, 24.9)])
kept, dropped = bo_noi_lai(kep_tu(words))
assert [w[0] for w in kept] == ["xin", "chào", "anh", "chị", "hiện", "tại"], kept
assert len(dropped) == 2

# Nhắc lại liền mạch không phải nói vấp
s = W([("căn", 29.3, 29.5), ("tứ", 29.5, 29.7), ("lập", 29.7, 29.9), ("4", 29.9, 30.2), ("căn", 30.2, 30.4), ("tứ", 30.4, 30.5), ("lập", 30.5, 30.7)])
assert bo_noi_lai(s)[0] == s

# Cắt im lặng, bỏ tiếng đệm, chừa nghỉ
p = doan_noi(W([("một", 1.0, 1.3), ("hai", 1.4, 1.7), ("ờ", 2.0, 2.3), ("ba.", 3.0, 3.3), ("bốn", 5.0, 5.4)]), 0, 10)
assert [x[2] for x in p] == ["một hai", "ba.", "bốn"], p
assert abs(p[0][0] - 0.92) < 1e-6 and abs(p[0][1] - 1.84) < 1e-6
assert abs(p[1][1] - 3.6) < 1e-6  # cuối câu chừa 0,3s
assert all(0 <= a < b <= 10 for a, b, _ in p)

# Khoảng không im (có tiếng) thì không cắt
p = doan_noi(W([("không", 1.0, 1.3), ("chín", 2.0, 2.3)]), 0, 5, quiet=lambda a, b: False)
assert [x[2] for x in p] == ["không chín"], p

# Âm lượng: im 0–1s, nói 1–2s → từ kéo dài 0,2–2s bắt đầu ở 1s; khoảng 0–1s im
db = [-60.0] * 50 + [-20.0] * 50
thr = nguong(db)
assert -60 < thr < -20
assert abs(lam_on_tu([["số", 0.2, 2.0]], db, thr)[0][1] - 0.95) < 1e-9
assert im(db, thr, 0, 1) == 1.0 and im(db, thr, 1, 2) == 0.0

# Đổi giờ: đoạn 0..10 bị cắt còn [1,3] và [6,8]; chuyển cảnh 0,5s; đoạn sau giữ nguyên
old = {"version": 1, "clips": [{"file": "a", "in": 0, "dur": 10}, {"file": "b", "in": 0, "dur": 4}], "transitions": [{"type": "fade", "dur": 0.5}]}
new = {"version": 1, "clips": [{"file": "a", "in": 1, "dur": 2}, {"file": "a", "in": 6, "dur": 2}, {"file": "b", "in": 0, "dur": 4}],
       "transitions": [{"type": "cut"}, {"type": "fade", "dur": 0.5}]}
f = doi_gio(old, new, [0, 0, 1])
assert abs(f(2) - 1) < 1e-9 and abs(f(7) - 3) < 1e-9          # trong mẩu giữ lại
assert abs(f(4) - 2) < 1e-9                                       # rơi vào chỗ bị cắt → đầu mẩu kế
assert abs(f(10.2) - 4.2) < 1e-9                                  # trong chuyển cảnh
assert abs(f(11) - 5.0) < 1e-9                                    # đoạn sau
# Nhịp đổi cỡ khung: mẩu 12s nói liên tục → mốc ở đầu mẩu và khoảng mỗi 4s, tại chỗ ngắt giữa từ
ws = [["t", k * 0.5, k * 0.5 + 0.4] for k in range(24)]
b = nhip_phong([(0, 12, "")], ws)
assert b[0] == 0 and len(b) == 3 and all(abs(x - y) >= 1.5 for x, y in zip(b, b[1:])), b
assert abs(b[1] - 3.95) < 1e-9, b  # chỗ ngắt gần mốc 4s nhất
print("OK")
