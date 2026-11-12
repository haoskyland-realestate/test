"""Thư viện hiệu ứng v1: một danh mục duy nhất cho bộ kiểm tra timeline, bộ dựng và app sau này.
In danh mục ra Markdown: python3 scripts/effects.py > ../docs/04-thu-vien/THU-VIEN-HIEU-UNG.md
Đổi màu thương hiệu thật: sửa STYLES bên dưới."""

# Phong cách: màu, chữ, tốc độ chuyển động (speed > 1 là chậm hơn), hiệu ứng chữ và chỉnh màu mặc định.
STYLES = {
    "hien-dai": {
        "vi": "Hiện đại: chữ đậm không chân, vàng nhấn, nhịp nhanh (giống video test đã duyệt)",
        "bg": "#06121c", "scrim": "4,14,24", "accent": "#d4a64a", "hl": "#f2c766", "text": "#ffffff",
        "display": "Be Vietnam Pro", "body": "Be Vietnam Pro", "display_weight": 800,
        "fonts": "family=Be+Vietnam+Pro:wght@400;600;800",
        "speed": 1.0, "anim": "rise", "look": "tuoi-dam",
    },
    "sang-trong": {
        "vi": "Sang trọng: navy + vàng champagne, tiêu đề chữ có chân, chuyển động chậm, màu ấm có viền tối",
        "bg": "#0b1b2b", "scrim": "8,20,33", "accent": "#c9a45c", "hl": "#e8cf96", "text": "#f4efe6",
        "display": "Playfair Display", "body": "Be Vietnam Pro", "display_weight": 700,
        "fonts": "family=Playfair+Display:wght@500;700&family=Be+Vietnam+Pro:wght@400;600",
        "speed": 1.3, "anim": "mask", "look": "am-sang",
    },
    "toi-gian": {
        "vi": "Tối giản: đen trắng, một màu nhấn nhạt, chữ mảnh, hiện mờ dần, màu nhạt",
        "bg": "#111111", "scrim": "17,17,17", "accent": "#e8e2d6", "hl": "#ffffff", "text": "#f5f5f2",
        "display": "Be Vietnam Pro", "body": "Be Vietnam Pro", "display_weight": 600,
        "fonts": "family=Be+Vietnam+Pro:wght@300;400;600",
        "speed": 1.2, "anim": "blur", "look": "nhat-toi-gian",
    },
    "edit-phim": {
        "vi": "Edit phim (mẫu edit-phim-01): chữ trắng nổi 3D giữa khung, lao vào mờ → rõ, nhịp nhanh, màu rực, phụ đề nhỏ nền tối",
        "bg": "#0a0a0c", "scrim": "0,0,0", "accent": "#ffffff", "hl": "#ffffff", "text": "#ffffff",
        "display": "Montserrat", "body": "Montserrat", "display_weight": 900,
        "fonts": "family=Montserrat:wght@500;600;800;900",
        "speed": 0.9, "anim": "zoom-blur", "look": "tuoi-dam",
        # CSS riêng của phong cách (bộ dựng chèn vào lớp chữ). Chữ 3D: chồng nhiều lớp bóng xám đậm dần xuống dưới.
        "css": """
.scrim{height:40%;opacity:.7}
.line.big,.line.mid,.t3big{color:#fff;text-shadow:0 2px 0 #e2e2e2,0 4px 0 #c8c8c8,0 6px 0 #b0b0b0,0 8px 0 #999,0 12px 6px rgba(0,0,0,.35),0 18px 30px rgba(0,0,0,.45)}
.sub{top:1380px}
.sub > span{font-family:var(--body);font-size:40px;font-weight:600;padding:8px 22px;border-radius:14px;background:rgba(0,0,0,.5);text-shadow:none}
.sub .hl{font-size:1em}
""",
    },
}

# Bộ màu lọc (filter): áp sau bước chuyển tông HDR và tự cân màu từng cảnh (scripts/mau.py).
# (mô tả, bộ lọc FFmpeg, bộ lọc CSS gần giống để xem trước trong app)
LOOKS = {
    "tu-nhien": ("Tự nhiên: màu thật, chỉ tự cân", "null", "none"),
    "tuoi-dam": ("Tươi đậm: rực, tương phản rõ, hợp mạng xã hội",
                 "eq=contrast=1.06:saturation=1.08,vibrance=intensity=0.18", "contrast(1.06) saturate(1.22)"),
    "trong-treo": ("Trong trẻo: sáng, nhẹ, trời xanh, hợp nội thất và nhà mẫu",
                   "eq=brightness=0.035:gamma=1.04:saturation=1.08,colorbalance=bh=0.03:rh=-0.01", "brightness(1.07) saturate(1.1)"),
    "am-sang": ("Ấm sang: ấm nhẹ, bớt rực, viền tối, hạt phim nhẹ",
                "eq=contrast=1.04:saturation=0.95,colorbalance=rs=0.04:bs=-0.04:rm=0.03:bm=-0.03,vignette=PI/5,noise=alls=4:allf=t",
                "sepia(0.15) saturate(0.95) contrast(1.04)"),
    "dien-anh": ("Điện ảnh: vùng tối xanh ngọc, da và nắng cam ấm",
                 "colorbalance=rs=-0.06:gs=0.01:bs=0.07:rh=0.07:gh=0.02:bh=-0.06,eq=contrast=1.08:saturation=1.05,vignette=PI/6",
                 "contrast(1.08) saturate(1.1) sepia(0.12) hue-rotate(-6deg)"),
    "nang-chieu": ("Nắng chiều: vàng ấm, dịu", "colorbalance=rm=0.06:gm=0.02:bm=-0.08:rh=0.04:bh=-0.05,eq=saturation=1.08",
                   "sepia(0.25) saturate(1.2)"),
    "mat-hien-dai": ("Mát hiện đại: xanh nhẹ, tương phản cao", "eq=contrast=1.12:saturation=1.05,colorbalance=bs=0.05:bm=0.03:rs=-0.03",
                     "contrast(1.12) saturate(1.05) hue-rotate(8deg)"),
    "nhat-toi-gian": ("Nhạt tối giản: sáng, ít màu, ít tương phản", "eq=contrast=0.94:brightness=0.03:saturation=0.75",
                      "contrast(0.94) brightness(1.03) saturate(0.75)"),
    "den-trang": ("Đen trắng tương phản", "hue=s=0,eq=contrast=1.2", "grayscale(1) contrast(1.2)"),
}
LOOKS["trung-tinh"] = LOOKS["tu-nhien"]  # tên cũ, giữ để timeline cũ vẫn chạy

# Chuyển cảnh: (độ dài mặc định giây, cách dựng, tham số, mô tả). css3d dựng bằng HyperFrames, xfade bằng FFmpeg.
TRANSITIONS = {
    "cut": (0.0, None, None, "Cắt thẳng (mặc định, dùng nhiều nhất)"),
    "cube-h": (0.8, "css3d", "h", "Khối 3D xoay ngang: sang chương mới"),
    "cube-v": (0.8, "css3d", "v", "Khối 3D xoay dọc: sang chương mới"),
    "flip": (0.8, "css3d", "flip", "Lật thẻ 3D: đổi phương án, so sánh"),
    "fade": (0.5, "xfade", "fade", "Hòa tan: đổi thời gian, cảm xúc chậm"),
    "dip": (0.6, "xfade", "fadeblack", "Tối dần rồi sáng: mở/kết chương"),
    "zoom": (0.5, "xfade", "zoomin", "Phóng xuyên: từ xa vào gần, ngoài vào trong"),
    "slide": (0.4, "xfade", "slideleft", "Trượt ngang: danh sách, từng mục"),
    "wipe": (0.5, "xfade", "wipeleft", "Quét ngang: tối giản"),
    "circle": (0.6, "xfade", "circleopen", "Mở vòng tròn: tiết lộ, nhấn mạnh"),
}

# 212 chuyển cảnh từ thư viện gl-transitions (MIT, thu-vien-chuyen-nghiep/gl-transitions), dựng bằng WebGL.
# Danh mục sinh bởi scripts/tao_gl_transitions.py, đã kiểm từng cái bằng scripts/kiem_gl.mjs. Tên dùng: "gl-<Tên>".
import json as _json, os as _os
GL_LIB = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "gl_transitions.json"), encoding="utf8"))
_GL_VI = {  # tên tiếng Việt cho các hiệu ứng hợp video bất động sản; đặt lên đầu danh sách
    "CrossZoom": "Phóng chéo mờ chuyển động", "Dreamy": "Mơ màng, sang trọng", "DreamyZoom": "Phóng mơ màng",
    "WhipPan": "Lia nhanh ngang", "WhipTilt": "Lia nhanh dọc", "LightWipe": "Quét ánh sáng", "LensFlare": "Lóe sáng ống kính",
    "FilmBurn": "Cháy phim", "Directional": "Trượt theo hướng", "ZoomInOut": "Phóng vào rồi ra", "BookFlip": "Lật sách",
    "InvertedPageCurl": "Cuộn trang", "Doorway": "Mở cửa", "CircleIris": "Mở mống mắt tròn", "WindowBlinds": "Rèm cửa sổ",
    "GlowDissolve": "Hòa tan phát sáng", "CameraShake": "Rung máy", "DefocusBlur": "Mất nét rồi rõ", "Morph": "Biến hình mềm",
    "Swirl": "Xoáy",
}
for _n in sorted(GL_LIB, key=lambda n: (n not in _GL_VI, n)):
    _vi = _GL_VI.get(_n)
    TRANSITIONS["gl-" + _n] = (0.8, "gl", _n, (f"{_vi} · " if _vi else "") + f"{GL_LIB[_n]['desc'] or _n} (gl-transitions)")

# Hiệu ứng chữ vào.
TEXT_ANIMS = {
    "rise": "Từng từ trượt lên, mờ → rõ",
    "mask": "Từng dòng trồi lên từ sau mép (sang trọng)",
    "blur": "Từng từ hiện từ mờ nhòe, không di chuyển (tối giản)",
    "pop": "Từng dòng phóng nhẹ 118% → 100% (hook)",
    "track": "Chữ giãn rộng rồi thu về (tiêu đề sang trọng)",
    "type": "Gõ từng ký tự (phân tích, tin nhanh)",
    "zoom-blur": "Cả dòng lao vào từ to và mờ → đúng cỡ và rõ (mẫu edit-phim-01)",
}

# Khối chữ: (trường bắt buộc, mô tả).
TEXT_KINDS = {
    "hook": (["tag", "lines"], "Mở đầu: thẻ nhãn + câu lớn"),
    "section": (["num", "title", "lines"], "Mục số viền + tiêu đề có thanh nhấn"),
    "line": (["lines"], "Một hai dòng chữ lớn"),
    "outro": (["lines"], "Cảnh kết thương hiệu (có thể thêm 'note')"),
    "lower": (["title"], "Thanh tiêu đề dưới màn hình (thêm 'sub' cho dòng phụ)"),
    "quote": (["lines"], "Câu trích lớn có dấu ngoặc (thêm 'by' cho người nói)"),
    "source": (["text"], "Thẻ nguồn nhỏ, bắt buộc khi có số liệu: 'Nguồn: …, cập nhật …'"),
    "checklist": (["items"], "Danh sách kiểm, từng mục hiện dần có dấu ✓ (thêm 'title')"),
    "stat": (["value", "label"], "Số lớn chạy từ 0 (thêm 'prefix', 'suffix', 'decimals')"),
    "title3d": (["big"], "Chữ lớn nổi 3D giữa khung: nhãn nhỏ trên ('top') + chữ lớn + dòng nhỏ dưới ('sub') — mẫu edit-phim-01"),
}


def catalog_md():
    out = ["# Thư viện hiệu ứng v1", "", "Tự sinh từ `video-studio/scripts/effects.py`. Dùng tên ở cột đầu trong `timeline.json`.", ""]
    out += ["## Phong cách (`meta.style`)", "| Tên | Mô tả |", "|---|---|"] + [f"| `{k}` | {v['vi']} |" for k, v in STYLES.items()]
    out += ["", "## Chỉnh màu (`look` của từng cảnh, mặc định theo phong cách)", "| Tên | Mô tả |", "|---|---|"] + [f"| `{k}` | {v[0]} |" for k, v in LOOKS.items()]
    out += ["", "## Chuyển cảnh (`transitions[].type`, đổi độ dài bằng `dur`)", "| Tên | Mặc định | Mô tả |", "|---|---|---|"] + [f"| `{k}` | {v[0]}s | {v[3]} |" for k, v in TRANSITIONS.items()]
    out += ["", "## Hiệu ứng chữ (`texts[].anim`, mặc định theo phong cách)", "| Tên | Mô tả |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in TEXT_ANIMS.items()]
    out += ["", "## Khối chữ (`texts[].kind`)", "| Tên | Trường bắt buộc | Mô tả |", "|---|---|---|"] + [f"| `{k}` | {', '.join(v[0])} | {v[1]} |" for k, v in TEXT_KINDS.items()]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(catalog_md(), end="")
