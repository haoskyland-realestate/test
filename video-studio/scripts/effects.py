"""Thư viện hiệu ứng v1: một danh mục duy nhất cho bộ kiểm tra timeline, bộ dựng và app sau này.
In danh mục ra Markdown: python3 scripts/effects.py > ../docs/THU-VIEN-HIEU-UNG.md
Đổi màu thương hiệu thật: sửa STYLES bên dưới."""

# Phong cách: màu, chữ, tốc độ chuyển động (speed > 1 là chậm hơn), hiệu ứng chữ và chỉnh màu mặc định.
STYLES = {
    "hien-dai": {
        "vi": "Hiện đại: chữ đậm không chân, vàng nhấn, nhịp nhanh (giống video test đã duyệt)",
        "bg": "#06121c", "scrim": "4,14,24", "accent": "#d4a64a", "hl": "#f2c766", "text": "#ffffff",
        "display": "Be Vietnam Pro", "body": "Be Vietnam Pro", "display_weight": 800,
        "fonts": "family=Be+Vietnam+Pro:wght@400;600;800",
        "speed": 1.0, "anim": "rise", "look": "trung-tinh",
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
}

# Chỉnh màu footage (bộ lọc FFmpeg).
LOOKS = {
    "trung-tinh": ("Trung tính, tăng nhẹ tương phản và độ rực", "eq=contrast=1.06:saturation=1.12"),
    "am-sang": ("Ấm sang: ấm nhẹ, bớt rực, viền tối, hạt phim nhẹ",
                "eq=contrast=1.04:saturation=0.92,colorbalance=rs=0.05:bs=-0.05:rm=0.03:bm=-0.03,vignette=PI/5,noise=alls=6:allf=t"),
    "mat-hien-dai": ("Mát hiện đại: xanh nhẹ, tương phản cao", "eq=contrast=1.12:saturation=1.05,colorbalance=bs=0.05:bm=0.03:rs=-0.03"),
    "nhat-toi-gian": ("Nhạt tối giản: sáng, ít màu, ít tương phản", "eq=contrast=0.94:brightness=0.03:saturation=0.75"),
}

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

# Hiệu ứng chữ vào.
TEXT_ANIMS = {
    "rise": "Từng từ trượt lên, mờ → rõ",
    "mask": "Từng dòng trồi lên từ sau mép (sang trọng)",
    "blur": "Từng từ hiện từ mờ nhòe, không di chuyển (tối giản)",
    "pop": "Từng dòng phóng nhẹ 118% → 100% (hook)",
    "track": "Chữ giãn rộng rồi thu về (tiêu đề sang trọng)",
    "type": "Gõ từng ký tự (phân tích, tin nhanh)",
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
