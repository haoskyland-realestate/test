"""Tạo kho hiệu ứng âm (sound effect) bằng tổng hợp số: âm tự làm, không bản quyền, tạo lại được y hệt (cố định seed).
Chạy trong video-studio:  python3 scripts/tao_sfx.py
Ra: thu-vien-am-thanh/hieu-ung/<nhom>_<ten>_<so>.wav (48 kHz, 16-bit, mono, đỉnh −1 dBFS) + thu-vien-am-thanh/hieu-ung.json
Mỗi âm có "diem_nhan": giây trong file mà tai nghe là lúc "chạm" (đỉnh whoosh, tiếng bụp…), để canh đúng lúc chuyển cảnh/chữ hiện.
Âm dựng theo phân tích video mẫu (thu-vien-mau/edit-phim-01_chuyen-nghiep/MAU.md)."""
import json, os, wave
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "thu-vien-am-thanh")
rng = np.random.default_rng(2026)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(d, pts):
    """Đường bao theo các điểm (giây, mức 0..1), nội suy thẳng."""
    x, y = zip(*pts)
    return np.interp(t_(d), x, y)


def lowpass(x, fc):
    """Lọc thông thấp một cực, tần số cắt đổi theo thời gian (fc là số hoặc mảng)."""
    a = 1 - np.exp(-2 * np.pi * np.broadcast_to(fc, x.shape) / SR)
    y, v = np.empty_like(x), 0.0
    for i in range(len(x)):
        v += a[i] * (x[i] - v)
        y[i] = v
    return y


def band(x, lo, hi):
    """Lọc dải: hai lần thông thấp (dốc hơn một lần) ở cận trên trừ cận dưới."""
    return lowpass(lowpass(x, hi), hi) - lowpass(lowpass(x, lo), lo)


def noise(d):
    return rng.standard_normal(int(d * SR))


def sine(d, f0, f1=None, curve=1.0):
    """Sóng sin quét tần số f0 → f1."""
    tt = t_(d)
    f = f0 + ((f1 or f0) - f0) * (tt / d) ** curve
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def reverb(x, tail=0.8, mix=0.25):
    ir = rng.standard_normal(int(tail * SR)) * np.exp(-6 * t_(tail) / tail)
    ir = lowpass(ir, 5000)
    n = len(x) + len(ir)
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)
    wet /= np.abs(wet).max() + 1e-9
    out = np.zeros(n)
    out[:len(x)] += x / (np.abs(x).max() + 1e-9)
    return out + mix * wet


def ting(d, f, decay=6.0, harm=(1, 2.76, 5.4)):
    """Tiếng 'ting' kim loại: vài hoạ âm lệch (như chuông nhỏ), tắt dần."""
    tt = t_(d)
    s = sum(np.sin(2 * np.pi * f * h * tt) / (k + 1) for k, h in enumerate(harm) if f * h < 18000)  # bỏ hoạ âm quá cao (gây dội tần)
    return s * np.exp(-decay * tt) * np.minimum(1, tt / 0.002)


def ghep(*parts):
    """Cộng các (giây bắt đầu, tín hiệu)."""
    n = max(int(s * SR) + len(x) for s, x in parts)
    out = np.zeros(n)
    for s, x in parts:
        out[int(s * SR):int(s * SR) + len(x)] += x
    return out


# --- Từng âm: (nhóm, tên, mô tả, dùng khi, hàm tạo) -> hàm trả (tín hiệu, điểm nhấn giây) ---
def whoosh(d, peak, f_lo, f_hi, q=0.35):
    """Gió vút: nhiễu lọc dải, tần số giữa và âm lượng lên tới đỉnh rồi xuống."""
    fc = env(d, [(0, f_lo), (peak, f_hi), (d, f_lo * 0.8)])
    x = band(noise(d), fc * (1 - q), fc * (1 + q))
    return x * env(d, [(0, 0), (peak, 1), (d, 0)]) ** 1.6, peak


def whoosh_xoay(d=0.6):
    x, p = whoosh(d, 0.38, 700, 4500)
    return x * (0.6 + 0.4 * np.sin(2 * np.pi * env(d, [(0, 8), (d, 22)]).cumsum() / SR)), p  # rung nhanh dần như xoáy


def whoosh_zoom(d=0.6):
    x, p = whoosh(d, 0.5, 400, 7000, 0.45)
    return x + 0.25 * sine(d, 150, 900, 2) * env(d, [(0, 0), (0.5, 1), (d, 0)]) ** 2, p  # thêm tiếng "vèo" lên cao


def swish_pop():
    w, _ = whoosh(0.16, 0.13, 2500, 9000, 0.5)
    pop = sine(0.07, 900, 250) * np.exp(-60 * t_(0.07))
    return ghep((0, w * 0.8), (0.13, pop)), 0.13


def pop():
    return sine(0.09, 650, 170, 0.6) * np.exp(-45 * t_(0.09)) + 0.15 * band(noise(0.09), 2000, 6000) * np.exp(-200 * t_(0.09)), 0.0


def click():
    return band(noise(0.012), 3000, 12000) * np.exp(-500 * t_(0.012)), 0.0


def tick():
    return ting(0.05, 2100, 90, (1, 1.5)), 0.0


def ting_kep():
    return ghep((0, ting(0.5, 5200)), (0.08, ting(0.6, 6200) * 0.8)), 0.0


def lap_lanh(d=0.9):
    parts = [(s, ting(0.35, f, 10) * a) for s, f, a in zip(np.sort(rng.uniform(0, d - 0.35, 9)), rng.uniform(3000, 9000, 9), rng.uniform(0.4, 1, 9))]
    return reverb(ghep(*parts), 0.6, 0.3), 0.05


def impact_tram():
    d = 0.9
    body = sine(d, 95, 42, 0.5) * np.exp(-5 * t_(d))
    hit = band(noise(0.05), 80, 3000) * np.exp(-90 * t_(0.05))
    return ghep((0, body), (0, hit * 0.6)), 0.0


def impact_boom():
    d = 1.8
    body = sine(d, 70, 32, 0.4) * np.exp(-2.6 * t_(d))
    rumble = lowpass(noise(d), 180) * np.exp(-3 * t_(d)) * 6
    return reverb(ghep((0, body), (0, rumble), (0, band(noise(0.04), 200, 4000) * np.exp(-80 * t_(0.04)))), 1.0, 0.2), 0.0


def hit():
    d = 0.35
    return ghep((0, sine(d, 180, 90) * np.exp(-14 * t_(d))), (0, band(noise(d), 800, 7000) * np.exp(-18 * t_(d)) * 0.7)), 0.0


def riser(d):
    fc = env(d, [(0, 300), (d, 8000)])
    x = band(noise(d), fc * 0.7, fc * 1.3) * env(d, [(0, 0), (d, 1)]) ** 2.2
    x += 0.2 * sine(d, 200, 1600, 2) * env(d, [(0, 0), (d, 1)]) ** 3
    return x, d - 0.01


def reverse_cym(d=1.0):
    x = band(noise(d), 3000, 12000) * np.exp(-4 * t_(d))
    return x[::-1], d - 0.01


def chay_sang(d=0.8):
    """Cháy sáng (đi với chuyển cảnh light leak / film burn): gió ấm + tiếng lách tách."""
    w, p = whoosh(d, 0.3, 500, 3000, 0.6)
    crack = np.zeros(int(d * SR))
    for s in rng.uniform(0.05, d - 0.05, 40):
        i = int(s * SR)
        crack[i:i + 120] += rng.standard_normal(120) * np.exp(-np.arange(120) / 20)
    return w + 0.5 * band(crack, 1500, 9000) * env(d, [(0, 0.2), (0.3, 1), (d, 0)]), p


def flash():
    d = 0.35
    return band(noise(d), 4000, 14000) * env(d, [(0, 0), (0.08, 1), (d, 0)]) ** 2, 0.08


def ding_ket():
    return reverb(ting(1.4, 3600, 3.2, (1, 2.0, 3.01)), 1.2, 0.25), 0.0


SOUNDS = [
    ("whoosh", "nhanh", "Gió vút nhanh 0,45 s", "Chuyển cảnh cắt nhanh, chữ lớn bay vào", lambda: whoosh(0.45, 0.25, 600, 5000)),
    ("whoosh", "cham", "Gió vút chậm 1 s", "Chuyển cảnh chậm (hoà tan, trượt), đổi chương", lambda: whoosh(1.0, 0.6, 300, 3500)),
    ("whoosh", "zoom", "Vút lên cao như lao vào cảnh", "Chuyển cảnh phóng mờ (gl-CrossZoom, zoomin)", whoosh_zoom),
    ("whoosh", "xoay", "Vút có rung xoáy", "Chuyển cảnh xoay (gl-WhipSpin, gl-Swirl)", whoosh_xoay),
    ("whoosh", "quat", "Quất rất ngắn 0,25 s", "Lia máy nhanh, chữ trượt ngang", lambda: whoosh(0.25, 0.12, 1500, 8000, 0.5)),
    ("chu", "swish-pop", "Vụt + bụp nhẹ (0,15 s, nhiều tần cao)", "Chữ lớn hiện (giống video mẫu: mỗi lần chữ to xuất hiện)", swish_pop),
    ("chu", "pop", "Bụp tròn, ngắn", "Chữ nhỏ, nhãn, gạch đầu dòng hiện", pop),
    ("chu", "click", "Tách rất ngắn", "Phụ đề đổi dòng, đánh dấu ✓", click),
    ("chu", "tick", "Tíc gỗ", "Đếm số, từng mục danh sách", tick),
    ("ting", "don", "Ting kim loại 5,2 kHz", "Con số chốt (giá, diện tích), từ khóa quan trọng", lambda: (ting(0.6, 5200), 0.0)),
    ("ting", "kep", "Ting hai nhịp", "Số liệu nổi bật nhất video", ting_kep),
    ("ting", "lap-lanh", "Lấp lánh nhiều ting nhỏ", "Tiện ích sang trọng, cảnh đẹp, logo", lap_lanh),
    ("ting", "ket", "Ding dài vang (3,6 kHz)", "Cảnh kết, lời kêu gọi", ding_ket),
    ("impact", "tram", "Đập trầm ngắn", "Hook giây đầu, chữ số lớn đập vào", impact_tram),
    ("impact", "boom", "Bùm trầm vang dài", "Mở đầu mạnh, sau khoảng lặng, cú chuyển lớn", impact_boom),
    ("impact", "hit", "Đánh gọn", "Nhấn từng ý trong danh sách", hit),
    ("riser", "1s", "Dồn lên 1 giây (kết thúc đột ngột)", "Đặt ngay trước chuyển cảnh lớn", lambda: riser(1.0)),
    ("riser", "2s", "Dồn lên 2 giây", "Trước tiết lộ quan trọng (giá, tiện ích)", lambda: riser(2.0)),
    ("riser", "nguoc", "Tiếng chũm chọe ngược 1 giây", "Dẫn vào cảnh mới, trước chữ lớn", reverse_cym),
    ("anh-sang", "chay", "Gió ấm + lách tách", "Chuyển cảnh cháy sáng / light leak (gl-FilmBurn, gl-BurnThrough)", chay_sang),
    ("anh-sang", "flash", "Loé xì ngắn", "Chuyển cảnh loé trắng (gl-Overexposure, gl-FlashFade)", flash),
]


def luu(path, x):
    x = x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20)
    f = int(0.004 * SR)  # 4 ms vào/ra để không nghe tiếng tách ở đầu/cuối
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    d = os.path.join(OUT, "hieu-ung"); os.makedirs(d, exist_ok=True)
    p = os.path.join(OUT, "hieu-ung.json")
    cat = json.load(open(p, encoding="utf8")) if os.path.exists(p) else {}  # giữ mục Hào tự thêm (file thật), chỉ cập nhật âm tổng hợp
    for nhom, ten, vi, dung, fn in SOUNDS:
        x, p = fn()
        name = f"{nhom}_{ten}_01"
        luu(os.path.join(d, name + ".wav"), x)
        cat[name] = {"nhom": nhom, "vi": vi, "dung_khi": dung, "dai": round(len(x) / SR, 3), "diem_nhan": round(p, 3), "nguon": "tổng hợp (scripts/tao_sfx.py)"}
        assert 0 <= p <= len(x) / SR, name
    json.dump(cat, open(os.path.join(OUT, "hieu-ung.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(len(cat), "hiệu ứng →", d)
