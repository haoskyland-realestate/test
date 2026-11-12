"""Màu: chuyển tông HDR → video thường, và tự cân màu từng cảnh.
DJI Pocket / iPhone mặc định quay HDR (HLG, BT.2020, 10-bit). Không chuyển tông thì video ra bị bạc màu, thiếu tương phản."""
import json, subprocess
from functools import lru_cache

import numpy as np


@lru_cache(maxsize=None)
def chuyen_tong(path):
    """Bộ lọc FFmpeg đặt đầu chuỗi: HDR → SDR BT.709 (hable, giữ vùng sáng không cháy). Video thường: chuỗi rỗng."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                          "-of", "json", path], capture_output=True, text=True).stdout
    st = (json.loads(out or "{}").get("streams") or [{}])[0]
    tin = {"arib-std-b67": "arib-std-b67", "smpte2084": "smpte2084"}.get(st.get("color_transfer", ""))
    if not tin:
        return ""
    # thu về tối đa 1920 điểm ảnh trước (video ra chỉ 1080×1920), chuyển tông trên khung 4K rất chậm
    return (f"scale=-2:'min(ih,1920)':flags=bilinear,zscale=tin={tin}:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
            f"tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")


def do_mau(img):
    """Độ sáng, tương phản, độ rực (Hasler–Süsstrunk) của ảnh BGR."""
    im = img.astype(np.float32)
    g = im.mean(2)
    b, gg, r = im[..., 0], im[..., 1], im[..., 2]
    rg, yb = r - gg, 0.5 * (r + gg) - b
    return float(g.mean()), float(g.std()), float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))


def can_bang(bright, contrast, color):
    """Bộ lọc eq đưa cảnh về mức chuẩn (sáng ~128, tương phản ~58, độ rực ~40). Chỉ tăng, không làm nhạt đi."""
    b = max(-0.03, min(0.06, (128 - bright) / 255 * 0.5))  # nội thất sáng thì giữ sáng, chỉ hạ rất nhẹ
    c = max(1.0, min(1.2, 58 / max(contrast, 1)))
    s = 1.12 if color < 15 else max(1.0, min(1.3, 40 / max(color, 1)))  # cảnh gần như không màu (tường trắng): tăng nhẹ, tránh ngả màu
    return f"eq=brightness={b:.3f}:contrast={c:.3f}:saturation={s:.3f}"


@lru_cache(maxsize=None)
def tu_can(path, start, dur):
    """Đo 3 khung trong đoạn (sau khi chuyển tông) rồi trả bộ lọc tự cân màu cho đoạn đó."""
    vals = []
    for k in (0.2, 0.5, 0.8):
        t = start + dur * k
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf",
                              chuyen_tong(path) + "scale=320:-2,format=bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
        if raw:
            vals.append(do_mau(np.frombuffer(raw, np.uint8).reshape(-1, 320, 3)))
    if not vals:
        return "null"
    return can_bang(*(sum(v[i] for v in vals) / len(vals) for i in range(3)))
