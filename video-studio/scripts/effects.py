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
        "speed": 1.3, "anim": "mask", "look": "am-sang", "t3anim": "rise",
        "css": """
.t3top{letter-spacing:10px;text-transform:uppercase;font-size:32px;color:var(--hl)}
.t3big{font-weight:500;letter-spacing:1px;color:#f4efe6;text-shadow:0 6px 30px rgba(0,0,0,.55)}
.t3sub{font-family:var(--display);font-style:italic;font-weight:500;color:#e8dcc6}
""",
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
        "speed": 0.9, "anim": "zoom-blur", "look": "tuoi-dam", "t3anim": "zoom-blur",
        # CSS riêng của phong cách (bộ dựng chèn vào lớp chữ). Chữ 3D: chồng nhiều lớp bóng xám đậm dần xuống dưới.
        "css": """
.scrim{height:40%;opacity:.7}
.line.big,.line.mid,.t3big{color:#fff;text-shadow:0 2px 0 #e2e2e2,0 4px 0 #c8c8c8,0 6px 0 #b0b0b0,0 8px 0 #999,0 12px 6px rgba(0,0,0,.35),0 18px 30px rgba(0,0,0,.45)}
.sub{top:1380px}
.sub > span{font-family:var(--body);font-size:40px;font-weight:600;padding:8px 22px;border-radius:14px;background:rgba(0,0,0,.5);text-shadow:none}
.sub .hl{font-size:1em}
""",
    },
    "vang-cao-cap": {
        "vi": "Vàng cao cấp: chữ Anton vàng ánh kim căn giữa, từng từ bật ra theo lời, thẻ minh hoạ nền đen viền vàng",
        "bg": "#0b0a08", "scrim": "0,0,0", "accent": "#d9a93f", "hl": "#f3cf6e", "text": "#ffffff",
        "display": "Anton", "body": "Be Vietnam Pro", "display_weight": 400,
        "fonts": "family=Anton&family=Be+Vietnam+Pro:wght@400;600;800",
        "speed": 1.0, "anim": "pop", "look": "am-sang", "t3anim": "word-pop",
        "css": """
.title3d{top:760px}
.sub{top:1290px}
.t3big{text-transform:uppercase;letter-spacing:1px;line-height:1.05}
.t3big .w{background:linear-gradient(180deg,#fff6cf 0%,#f3cf6e 42%,#c78f22 68%,#f7dc8c 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 14px rgba(0,0,0,.6))}
.t3top,.t3sub{font-weight:600;text-shadow:0 3px 14px rgba(0,0,0,.7)}
.ctt{color:#f3cf6e} .card .cw{border:2px solid rgba(217,169,63,.5);border-radius:28px;padding:40px 36px}
.sub > span{font-size:44px;font-weight:700;background:rgba(0,0,0,.55);border-radius:12px;font-family:var(--body)}
""",
    },
    "chu-mau": {
        "vi": "Chữ động nhiều màu: từng từ bật ra, xếp chồng, to nhỏ xen kẽ, trắng – xanh ngọc – cam – hồng",
        "bg": "#0e1117", "scrim": "0,0,0", "accent": "#3fd0c9", "hl": "#ff9a3c", "text": "#ffffff",
        "display": "Be Vietnam Pro", "body": "Be Vietnam Pro", "display_weight": 900,
        "fonts": "family=Be+Vietnam+Pro:wght@500;700;900",
        "speed": 0.85, "anim": "pop", "look": "tuoi-dam", "t3anim": "word-pop",
        "css": """
.title3d{top:640px}
.t3big{font-size:150px !important;white-space:normal;line-height:.98;text-transform:uppercase;-webkit-text-stroke:2px rgba(0,0,0,.25);text-shadow:0 7px 0 rgba(0,0,0,.35)}
.t3big > .w,.t3big > .nw{display:block}
.t3big > :nth-child(4n+1){color:#ffffff} .t3big > :nth-child(4n+2){color:#3fd0c9;font-size:.72em}
.t3big > :nth-child(4n+3){color:#ff9a3c} .t3big > :nth-child(4n){color:#ff6fae;font-size:.72em}
.t3big .hl{color:inherit}
.t3top,.t3sub{font-weight:700;text-shadow:0 3px 12px rgba(0,0,0,.7)}
.sub > span{background:#ffffff;color:#111;text-shadow:none;font-size:46px} .sub .hl{background:#3fd0c9;color:#111}
""",
    },
    "neon-cam": {
        "vi": "Neon cam: chữ cam phát sáng gõ dần theo lời, số nổi cam, thẻ tối viền sáng, khung gần – xa xen kẽ",
        "bg": "#0d0603", "scrim": "10,4,0", "accent": "#ff7a1a", "hl": "#ffb36b", "text": "#ffe9d6",
        "display": "Montserrat", "body": "Montserrat", "display_weight": 900,
        "fonts": "family=Montserrat:wght@500;700;900",
        "speed": 0.95, "anim": "type", "look": "dien-anh", "t3anim": "type",
        "css": """
.t3big,.stat,.ctt{color:#ffb36b;text-shadow:0 0 6px #ff8a2a,0 0 18px #ff6a00,0 0 42px #ff4d00,0 0 80px rgba(255,77,0,.55)}
.t3top,.t3sub{color:#ffe2c4;font-weight:700;text-shadow:0 0 10px rgba(255,120,30,.85)}
.card .cw{border:2px solid #ff7a1a;border-radius:30px;padding:40px 36px;box-shadow:0 0 40px rgba(255,106,0,.45),inset 0 0 30px rgba(255,106,0,.2)}
.sub > span{background:rgba(20,8,0,.7);border:1px solid rgba(255,122,26,.7);font-size:42px;font-weight:700}
.sub .hl{background:#ff7a1a;color:#140800}
""",
    },
    "giai-thich-sang": {
        "vi": "Giải thích sáng: thẻ trắng bo góc, nhãn BƯỚC cam, chữ đen dễ đọc, thẻ minh hoạ nền kem – hợp hướng dẫn thủ tục, quy trình",
        "bg": "#f7f3ec", "scrim": "0,0,0", "accent": "#ff7a1a", "hl": "#ff7a1a", "text": "#ffffff",
        "display": "Be Vietnam Pro", "body": "Be Vietnam Pro", "display_weight": 800,
        "fonts": "family=Be+Vietnam+Pro:wght@500;700;800",
        "speed": 1.0, "anim": "rise", "look": "trong-treo", "t3anim": "rise",
        "css": """
.scrim{opacity:.55}
.t3top{display:inline-block;background:#ff7a1a;color:#fff;padding:8px 22px;border-radius:40px;font-size:36px;font-weight:800;letter-spacing:2px;text-shadow:none;margin-bottom:16px}
.t3big{display:inline-block;color:#1d1d1f;background:#ffffff;padding:6px 34px 16px;border-radius:26px;box-shadow:0 16px 40px rgba(0,0,0,.3);white-space:nowrap}
.t3big .hl{color:#ff7a1a}
.t3sub{display:block;width:max-content;margin:16px auto 0;background:rgba(255,255,255,.94);color:#333;padding:8px 22px;border-radius:14px;text-shadow:none}
.card{color:#1d1d1f} .ctt{color:#1d1d1f} .cs{color:#ff7a1a;font-weight:800}
.ci{background:#ffffff;color:#1d1d1f;box-shadow:0 8px 24px rgba(0,0,0,.08)} .ci b{background:#ff7a1a;color:#fff}
.sub > span{background:#ffffff;color:#1d1d1f;text-shadow:none;font-size:44px} .sub .hl{background:#ff7a1a;color:#fff}
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
    "word-pop": "Từng từ bật ra nảy nhẹ theo nhịp nói",
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
    "title3d": (["big"], "Chữ lớn giữa khung: nhãn nhỏ trên ('top') + chữ lớn + dòng nhỏ dưới ('sub'); kiểu chữ và cách hiện theo phong cách"),
    "tag": (["tag"], "Tag chữ có sẵn khung + chuyển động (scripts/tag_chu.py), chỉ điền ô chữ 'o'; 'y' 0..1 là vị trí dọc"),
    "loi": (["words"], "Chữ theo nhịp lời nói: từng từ hiện đúng lúc nói; từ khoá đỏ phát sáng. 'words' = [[từ, giây bắt đầu, giây kết thúc]], 'hl' = số thứ tự từ khoá, 'y' 0..1 hoặc 'top_px'; 'bam_nguoi': đặt ngang ngực người nói (scripts/loi_nhip.py)"),
    "compare": (["a_label", "a_value", "b_label", "b_value"], "Thẻ so sánh 2 cột (vd. Thuê nhà vs Trả góp), thêm 'title', 'note'"),
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


def zoom_bieu_thuc(zs, fps):
    """Biểu thức zoom của ffmpeg zoompan cho các đoạn phóng: đẩy vào êm (smoothstep: chậm → nhanh → chậm) 0,5 giây rồi lùi ra êm
    ≤1 giây ở cuối đoạn; giữ nguyên giữa đoạn. Thay cho kiểu nhảy cỡ bậc thang cũ (Hào nghiệm thu 13/11: zoom giật).
    shortcut: các đoạn zoom chồng nhau thì cộng dồn, không giới hạn; zoom chồng không phải cách dùng bình thường."""
    S = lambda p: f"(({p})*({p})*(3-2*({p})))"
    terms = []
    for x in zs:
        a, b = x["start"], x["start"] + x["dur"]
        ri, ro = round(min(0.5, x["dur"] / 3), 3), round(min(1.0, x["dur"] / 2.5), 3)
        t = f"(in/{fps})"
        terms.append(f"({x['scale']}-1)*({S(f'clip(({t}-{a})/{ri},0,1)')}-{S(f'clip(({t}-{b - ro:.3f})/{ro},0,1)')})")
    return "1+" + "+".join(terms)
