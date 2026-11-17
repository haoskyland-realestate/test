"""Thư viện tag chữ: khung bố cục + chuyển động có sẵn, chỉ điền chữ của Hào (khối chữ kind "tag" trong timeline).
Học bố cục và nhịp từ bộ tag mẫu Hào gửi 13/11/2026 (bộ 1, 10 kiểu); dựng lại bằng HTML/GSAP, không dùng file gốc.
Mỗi tag: {"kind": "tag", "tag": "<tên>", "start", "dur", "o": {ô chữ}, "y": 0..1 (tâm theo chiều dọc, mặc định 0,24: trên mặt người nói)}.
Trong ô chữ: *từ* để tô màu nhấn; ô "doi" của tag doi-chu nhiều chữ cách nhau bằng "|".
Xem thử cả bộ: python3 scripts/tag_chu.py --xem-thu   ·   tự kiểm: python3 scripts/tag_chu.py --tu-kiem"""
import html, json, re, sys

CAM, VANG, KEM = "#d9772b", "#f2b33d", "#f3e6cf"
FONTS = ("family=Montserrat:ital,wght@0,500;0,800;0,900;1,800;1,900&family=Oswald:wght@500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;1,600"
         "&family=Be+Vietnam+Pro:wght@300;400;500;600&family=Dancing+Script:wght@700")


def e(t):
    """Thoát HTML, *từ* → tô nhấn."""
    return re.sub(r"\*([^*]+)\*", r'<span class="nh">\1</span>', html.escape(t))


# Mỗi tag: tên tiếng Việt, dùng cho, ô chữ mẫu, html(o), css, vao(sel, t, d) → [lệnh GSAP]
TAGS = {
    "thanh-doc": dict(
        ten="Thanh dọc + 2 tầng chữ", dung="Nhấn một ưu điểm: chữ đậm + dòng mảnh bên dưới",
        o={"tren": "VỊ TRÍ *VÀNG*", "duoi": "sát trục chính"},
        html=lambda o: f'<div class="td"><i class="tdb"></i><div><div class="tdt">{e(o["tren"])}</div><div class="tdd">{e(o.get("duoi", ""))}</div></div></div>',
        css=f""".td{{display:inline-flex;align-items:stretch;gap:22px;text-align:left}}
.td .tdb{{display:block;flex:none;width:12px;margin:6px 0;background:{CAM};transform-origin:top}}
.tdt{{font:900 112px/1 Montserrat;color:#fff;letter-spacing:1px}} .tdt .nh{{background:linear-gradient(transparent 15%,{CAM}cc 15%,{CAM}cc 92%,transparent 92%);padding:0 10px}}
.tdd{{font:300 72px/1.1 'Be Vietnam Pro';color:{KEM};letter-spacing:10px;margin-top:6px}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .tdb",{{scaleY:0}},{{scaleY:1,duration:{d(.35)},ease:"power3.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .tdt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{d(.5)},ease:"power3.out"}},{t + .1:.2f});',
                             f'tl.fromTo("{s} .tdd",{{opacity:0,letterSpacing:"30px"}},{{opacity:1,letterSpacing:"10px",duration:{d(.6)},ease:"expo.out"}},{t + .35:.2f});']),
    "chong-tuong-phan": dict(
        ten="Chữ chồng tương phản", dung="Đối lập hai ý: A chứ không phải B",
        o={"a": "DÒNG TIỀN", "nho": "mới là điều", "phu": "không phải", "b": "GIÁ BÁN"},
        html=lambda o: (f'<div class="ct"><div class="cta">{e(o["a"])}</div><div class="ctn">{e(o.get("nho", ""))}</div>'
                        f'<div class="ctr"><span class="ctp">{e(o.get("phu", ""))}</span> <span class="ctb">{e(o["b"])}</span></div></div>'),
        css=f""".ct{{display:inline-block;text-align:left}}
.cta{{font:italic 900 128px/1 Montserrat;color:{VANG};letter-spacing:2px}} .ctn{{font:400 34px/1.2 'Be Vietnam Pro';color:#fff;margin:4px 0 0 90px}}
.ctr{{margin-top:2px}} .ctp{{font:italic 800 40px Montserrat;color:{CAM}}} .ctb{{font:900 76px Montserrat;color:#fff}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .cta",{{opacity:0,x:160,letterSpacing:"40px"}},{{opacity:1,x:0,letterSpacing:"2px",duration:{d(.55)},ease:"expo.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .ctn",{{opacity:0}},{{opacity:1,duration:{d(.3)}}},{t + .3:.2f});',
                             f'tl.fromTo("{s} .ctp",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:{d(.4)},ease:"power3.out"}},{t + .4:.2f});',
                             f'tl.fromTo("{s} .ctb",{{opacity:0,x:-140,filter:"blur(10px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out"}},{t + .5:.2f});']),
    "rai-so-le": dict(
        ten="Chữ rải so le", dung="Liệt kê 3–4 điểm ngắn: tiện ích, ưu điểm",
        o={"1": "Gần trường", "2": "gần chợ", "3": "đi bộ", "4": "ra biển"},
        html=lambda o: ('<div class="rs">' + "".join(f'<div class="rr">{"".join(f"""<span class="r r{k}">{e(o[str(k)])}</span>""" for k in ks if o.get(str(k)))}</div>'
                                                    for ks in ((1, 2), (3, 4))) + "</div>"),
        css=f""".rs{{display:inline-block;text-align:left}} .rr{{white-space:nowrap}} .rr + .rr{{margin:-6px 0 0 -70px}}
.rs .r{{display:inline-block;font:600 86px/1.05 Oswald;margin-right:22px}} .rs .r2,.rs .r4{{position:relative;top:26px}}
.rs .r1,.rs .r4{{color:#fff}} .rs .r2,.rs .r3{{color:{KEM}}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .r",{{opacity:0,y:30,scale:.7}},{{opacity:1,y:0,scale:1,duration:{d(.35)},ease:"back.out(2.2)",stagger:{d(.18)}}},{t:.2f});']),
    "so-tron": dict(
        ten="Số lớn + vòng tròn", dung="Một con số nổi bật (phải có nguồn và ngày)",
        o={"so": "30%", "nhan": "VỐN TỰ CÓ"},
        html=lambda o: f'<div class="st"><i class="sc"></i><div class="sn">{e(o["so"])}</div><div class="sl">{e(o.get("nhan", ""))}</div></div>',
        css=f""".st{{position:relative;display:inline-block;text-align:center;padding:0 40px}}
.sc{{position:absolute;width:250px;height:250px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#f0a050,{CAM} 60%,#a24c12);right:-30px;top:-40px;z-index:0}}
.sn{{position:relative;font:900 250px/.95 Montserrat;color:#fff;background:linear-gradient(180deg,#fff 30%,#f6c27f 70%,{CAM});-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 6px 0 #00000088);-webkit-text-stroke:3px #ffffffaa}}
.sl{{position:relative;font:800 92px/1 Montserrat;color:#fff;letter-spacing:2px;margin-top:4px}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .sn",{{opacity:0,scale:1.6,filter:"blur(20px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.5)},ease:"expo.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .sc",{{opacity:0,x:260,rotation:180}},{{opacity:1,x:0,rotation:0,duration:{d(.6)},ease:"power3.out"}},{t + .1:.2f});',
                             f'tl.fromTo("{s} .sl",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{d(.35)}}},{t + .35:.2f});']),
    "gach-chan": dict(
        ten="Câu + gạch chân", dung="Cảnh báo, sai lầm, điều cần nhớ",
        o={"cau": "Sai lầm khi vay", "duoi": "lần đầu mua nhà"},
        html=lambda o: f'<div class="gc"><div class="gct">{e(o["cau"])}</div><i class="gcl"></i><div class="gcd">{e(o.get("duoi", ""))}</div></div>',
        css=f""".gc{{display:inline-block;text-align:center}} .gct{{font:600 100px/1.05 Oswald;color:#fff}} .gct .nh{{color:{VANG}}}
.gcl{{display:block;height:7px;background:#fff;margin:10px 0 14px;transform-origin:left}} .gcd{{font:300 44px 'Be Vietnam Pro';color:#fff;letter-spacing:14px;opacity:.9}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .gcl",{{scaleX:0}},{{scaleX:1,duration:{d(.45)},ease:"power3.inOut"}},{t:.2f});',
                             f'tl.fromTo("{s} .gct",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d(.45)},ease:"expo.out"}},{t + .25:.2f});',
                             f'tl.fromTo("{s} .gcd",{{opacity:0,letterSpacing:"30px"}},{{opacity:.9,letterSpacing:"14px",duration:{d(.6)},ease:"expo.out"}},{t + .45:.2f});']),
    "thanh-ten": dict(
        ten="Thanh tên (logo + tên)", dung="Giới thiệu dự án, người nói, thương hiệu",
        o={"logo": "HSL", "ten": "VINHOMES CẦN GIỜ", "mo_ta": "Hào Sky Land · tư vấn dòng tiền"},
        html=lambda o: (f'<div class="tt"><div class="ttb"><span class="ttl">{e(o.get("logo", "HSL"))}</span><span class="ttx"><b>{e(o["ten"])}</b>'
                        f'<small>{e(o.get("mo_ta", ""))}</small></span></div><i class="ttc"></i></div>'),
        css=f""".tt{{position:relative;display:inline-flex;align-items:stretch}}
.ttb{{display:flex;align-items:center;gap:22px;background:linear-gradient(90deg,{CAM},#b85d1d);padding:16px 40px 16px 18px;transform-origin:left}}
.ttl{{font:800 34px/1 Montserrat;color:#fff;border:3px solid #fff;padding:10px 12px}} .ttx b{{display:block;font:800 50px/1.05 Montserrat;color:#fff}}
.ttx small{{display:block;font:400 28px 'Be Vietnam Pro';color:#ffe9d0;margin-top:4px}} .ttc{{width:22px;background:#fff;transform-origin:left}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .ttc",{{scaleX:0}},{{scaleX:1,duration:{d(.2)}}},{t:.2f});',
                             f'tl.fromTo("{s} .ttb",{{scaleX:0}},{{scaleX:1,duration:{d(.5)},ease:"power3.out"}},{t + .1:.2f});',
                             f'tl.fromTo("{s} .ttl,{s} .ttx",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:{d(.35)},stagger:{d(.12)}}},{t + .45:.2f});']),
    "doi-chu": dict(
        ten="Đổi chữ cuối", dung="Một ý, nhiều đáp án: phù hợp an cư → cho thuê → nghỉ dưỡng",
        o={"tren": "Phù hợp", "doi": "an cư|cho thuê|nghỉ dưỡng"},
        html=lambda o: (f'<div class="dc"><div class="dct">{e(o["tren"])}</div><div class="dcw">'
                        + "".join(f'<span class="dcd">{e(w.strip())}</span>' for w in o["doi"].split("|")) + "</div></div>"),
        css=f""".dc{{display:inline-block;text-align:center}} .dct{{font:500 92px/1.1 'Playfair Display';color:#fff}}
.dcw{{position:relative;height:120px}} .dcd{{position:absolute;left:50%;top:0;transform:translateX(-50%);white-space:nowrap;font:italic 600 100px/1.1 'Playfair Display';
 color:{VANG};text-shadow:0 0 24px #f2b33d66;opacity:0}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .dct",{{opacity:0,y:20,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{d(.45)}}},{t:.2f});'],
        doi=True),
    "ba-tang": dict(
        ten="Chữ chồng 3 tầng", dung="Khẩu hiệu ngắn, cảm xúc: tầng giữa là chữ chính",
        o={"tren": "SỐNG", "giua": "XANH", "duoi": "MỖI NGÀY"},
        html=lambda o: f'<div class="bt"><div class="btt">{e(o.get("tren", ""))}</div><div class="btg">{e(o["giua"])}</div><div class="btd">{e(o.get("duoi", ""))}</div></div>',
        css=f""".bt{{display:inline-block;text-align:center;line-height:1}} .btt{{font:600 64px Oswald;color:#fff;position:relative;z-index:2}}
.btg{{font:700 170px/.9 Oswald;color:{VANG};text-shadow:0 8px 0 #00000077;margin:-14px 0}} .btd{{font:600 78px Oswald;color:#fff;position:relative;z-index:2}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .btt,{s} .btd",{{opacity:0,y:(i)=>i?40:-40}},{{opacity:1,y:0,duration:{d(.4)},ease:"power3.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .btg",{{opacity:0,scale:1.4,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.5)},ease:"expo.out"}},{t + .3:.2f});']),
    "hop-trang": dict(
        ten="Hộp trắng + nhãn", dung="Điểm cần kiểm tra, mục quan trọng",
        o={"hop": "Điều cần kiểm tra", "nhan": "TRƯỚC KHI ĐẶT CỌC"},
        html=lambda o: f'<div class="ht"><div class="htb"><span>{e(o["hop"])}</span></div><div class="htn">{e(o.get("nhan", ""))}</div></div>',
        css=f""".ht{{display:inline-block;text-align:left}} .htb{{background:linear-gradient(90deg,#fff 75%,#cfcfcf);padding:10px 34px;transform-origin:left}}
.htb span{{font:600 72px/1.1 Oswald;color:#1b1b1b}} .htn{{font:italic 800 44px Montserrat;color:{VANG};margin:10px 0 0 24px;letter-spacing:1px}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .htb",{{scaleX:0}},{{scaleX:1,duration:{d(.45)},ease:"power3.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .htb span",{{opacity:0}},{{opacity:1,duration:{d(.25)}}},{t + .3:.2f});',
                             f'tl.fromTo("{s} .htn",{{opacity:0,x:60}},{{opacity:1,x:0,duration:{d(.4)},ease:"power3.out"}},{t + .4:.2f});']),
    "buoc-so": dict(
        ten="Bước + số lớn", dung="Các bước, thứ tự, danh sách đánh số",
        o={"chu": "Bước", "so": "1"},
        html=lambda o: f'<div class="bs"><span class="bsc">{e(o.get("chu", "Bước"))}</span><span class="bsn">{e(o["so"])}</span></div>',
        css=f""".bs{{display:inline-flex;align-items:flex-end;gap:6px}} .bsc{{font:800 120px/1 Montserrat;color:#fff;text-shadow:0 0 30px #ffffff55}}
.bsn{{font:700 230px/.8 Oswald;color:{VANG};text-shadow:0 8px 0 #00000077}}""",
        vao=lambda s, t, d: [f'tl.fromTo("{s} .bsc",{{opacity:0,x:-60,filter:"blur(10px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:{d(.4)},ease:"power3.out"}},{t:.2f});',
                             f'tl.fromTo("{s} .bsn",{{opacity:0,y:120,scale:.6}},{{opacity:1,y:0,scale:1,duration:{d(.5)},ease:"back.out(2.4)"}},{t + .2:.2f});']),
}

for _v in TAGS.values():
    _v["bo"] = 1

# ---------- Biểu tượng (vẽ nét, theo màu chữ) ----------
ICON = {
    "nha": '<path d="M4 11 12 4l8 7v9h-5v-6H9v6H4z"/>',
    "toa-nha": '<path d="M5 21V4h9v17M14 9h5v12M8 7h3M8 11h3M8 15h3M3 21h18"/>',
    "ghim": '<path d="M12 21s-6-6.2-6-11a6 6 0 0 1 12 0c0 4.8-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>',
    "dien-thoai": '<path d="M6 3h4l1.5 4.5-2.5 1.5a11 11 0 0 0 6 6l1.5-2.5L21 14v4a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
    "sao": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "the": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.4"/>',
}


def icon(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round">{ICON.get(k, "")}</svg>'


# ---------- Khung 1: chữ chồng dòng (bộ 3, 4, 5) ----------
# Một dòng viết gọn "kiểu màu cỡ x.. y..|chữ"; kiểu: tay (viết tay) · dam · dam-n (đậm nghiêng) · serif · serif-hoa · hep (chữ hẹp) · nho · nho-hoa ·
# hh (nhãn huy hiệu) · icon-<tên>; màu: trang vang kim cam xanh hong luc kem; sang = phát sáng; số = cỡ chữ px; x40 / x-40 lệch ngang; y-20 chồng lên dòng trên.
CSS_DONG = """
.dg{display:inline-block;text-align:center;line-height:1}.dg .l{display:block;white-space:nowrap}
.dg .tay{font-family:'Dancing Script';font-weight:700;font-size:64px}.dg .dam{font:900 110px Montserrat;text-transform:uppercase}
.dg .dam-n{font:italic 900 110px Montserrat;text-transform:uppercase}.dg .serif{font:500 104px 'Playfair Display'}
.dg .serif-hoa{font:600 96px 'Playfair Display';text-transform:uppercase;letter-spacing:4px}.dg .hep{font:700 112px Oswald;text-transform:uppercase}
.dg .nho{font:400 40px 'Be Vietnam Pro'}.dg .nho-hoa{font:600 34px 'Be Vietnam Pro';text-transform:uppercase;letter-spacing:6px}
.dg .hh{display:inline-block;font:800 34px Montserrat;text-transform:uppercase;padding:8px 20px;border-radius:8px;background:#fff;color:#141414}
.dg .ic{width:84px;height:84px;display:inline-block}
.dg .trang{color:#fff}.dg .vang{color:#ffd166}.dg .cam{color:#ff8a3d}.dg .xanh{color:#5ee7ff}.dg .hong{color:#ff5fa2}.dg .luc{color:#8ff0a4}.dg .kem{color:#f3e6cf}
.dg .kim{background:linear-gradient(180deg,#fff6d5 10%,#f2c14e 55%,#a8741a);-webkit-background-clip:text;background-clip:text;color:transparent}
.dg .hh.vang{background:#ffd166;color:#141414}.dg .hh.xanh{background:#5ec8ff;color:#06263a}.dg .hh.hong{background:#ff5fa2;color:#fff}.dg .hh.cam{background:#ff8a3d;color:#fff}
.dg .sang{filter:drop-shadow(0 0 6px currentColor) drop-shadow(0 0 16px currentColor)}
.dg::after{content:"";display:block;clear:both}.dg .ben{float:left;margin:0 18px 0 0;line-height:.82}.dg .ben~.l{text-align:left}.dg .duoi{clear:both;text-align:center;margin-top:12px}.dg .kim.sang{filter:drop-shadow(0 0 14px #f2c14e88)}
"""
FONT_CLS = ("tay", "dam", "dam-n", "serif", "serif-hoa", "hep", "nho", "nho-hoa", "hh")


def _dong(spec, chu):
    kieu, _, mau = spec.partition("|")
    tk = kieu.split()
    cls = [t for t in tk if not re.fullmatch(r"-?\d+|[xy]-?\d+", t) and not t.startswith("icon-")]
    st = [f"font-size:{t}px" for t in tk if re.fullmatch(r"\d+", t)]
    st += [f"transform:translateX({t[1:]}px)" for t in tk if re.fullmatch(r"x-?\d+", t)]
    st += [f"margin-top:{t[1:]}px" for t in tk if re.fullmatch(r"y-?\d+", t)]
    ic = next((t[5:] for t in tk if t.startswith("icon-")), None)
    noi = (icon(ic) + " " if ic else "") + "".join(f'<span class="w">{e(w)}</span> ' for w in chu.split())
    return f'<span class="l {" ".join(cls)}" style="{";".join(st)}">{noi.strip()}</span>'


def _dong_vao(sel, t, d, n, tung_tu=False):
    a = []
    for i in range(n):
        q = f"{sel} .l:nth-child({i + 1})"
        a.append(f'(()=>{{const el=document.querySelector("{q}");if(!el)return;const c=el.classList;'
                 f'if(c.contains("tay"))tl.fromTo(el,{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{d(.55)},ease:"power2.out"}},{t + i * .14:.2f});'
                 f'else if(c.contains("hh"))tl.fromTo(el,{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:{d(.4)},ease:"power3.out"}},{t + i * .14:.2f});'
                 f'else if(c.contains("nho")||c.contains("nho-hoa"))tl.fromTo(el,{{opacity:0,y:16,letterSpacing:"14px"}},{{opacity:1,y:0,letterSpacing:c.contains("nho-hoa")?"6px":"0px",duration:{d(.5)}}},{t + i * .14:.2f});'
                 + (f'else tl.fromTo(el.querySelectorAll(".w,.ic"),{{opacity:0,y:40,scale:.7,filter:"blur(8px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:{d(.35)},ease:"back.out(2)",stagger:{d(.12)}}},{t + i * .3:.2f});'
                    if tung_tu else
                    f'else tl.fromTo(el,{{opacity:0,scale:1.35,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out"}},{t + i * .14:.2f});')
                 + "})();")
    return a


def dang_dong(ten, dung, bo, dong, tung_tu=False):
    """Đăng một tag kiểu chồng dòng. dong: danh sách 'kiểu|chữ mẫu'; ô chữ o["1"], o["2"]… thay chữ từng dòng."""
    TAGS[ten] = dict(
        ten=ten, dung=dung, bo=bo, o={str(i + 1): x.partition("|")[2] for i, x in enumerate(dong)},
        html=lambda o, dong=dong: '<div class="dg">' + "".join(_dong(x, o.get(str(i + 1), x.partition("|")[2])) for i, x in enumerate(dong)) + "</div>",
        css=CSS_DONG, vao=lambda s, t, d, n=len(dong), tt=tung_tu: _dong_vao(s, t, d, n, tt))


# ---------- Khung 2: thanh tên kim loại (bộ 2) ----------
MAU_THANH = {"do": ("#ff6b6b", "#c8102e", "#7a0a1c"), "xanh": ("#6ec1ff", "#1565d8", "#0a2f7a"), "vang": ("#ffe08a", "#d9a21b", "#8a5a08")}
CSS_THANH = """
.th{display:inline-flex;align-items:center;gap:0;text-align:left;position:relative}
.th .tb{position:relative;overflow:hidden;display:flex;align-items:center;gap:18px;padding:16px 46px 16px 26px;color:#fff;transform-origin:left;
 background:linear-gradient(180deg,var(--a) 0%,var(--b) 55%,var(--c) 100%);box-shadow:0 8px 24px #0006}
.th .tb b{display:block;font:800 52px/1.05 Montserrat;text-transform:uppercase;text-shadow:0 2px 0 #0004}.th .tb small{display:block;font:500 28px 'Be Vietnam Pro';opacity:.9;margin-top:4px}
.th .tb .ic{width:58px;height:58px;flex:none}.th .sh{position:absolute;top:0;bottom:0;width:30%;left:-40%;background:linear-gradient(100deg,transparent,#ffffffaa,transparent)}
.th .duoi{width:18px;align-self:stretch;background:#fff;transform-origin:left}.th .so{width:96px;height:96px;border-radius:50%;background:#fff;color:var(--b);display:flex;
 align-items:center;justify-content:center;font:900 60px Montserrat;margin-right:-24px;z-index:2;box-shadow:0 6px 18px #0006}
.th.vat .tb{clip-path:polygon(4% 0,100% 0,96% 100%,0 100%)}.th.luc .tb{clip-path:polygon(5% 0,95% 0,100% 50%,95% 100%,5% 100%,0 50%);padding:16px 70px}
.th.vien .tb{border-radius:60px;padding-left:16px}.th.vien .ic{background:#fff;color:var(--b);border-radius:50%;padding:10px;width:70px;height:70px}
.th.ten .tb{clip-path:polygon(0 0,92% 0,100% 50%,92% 100%,0 100%);padding-right:90px}
"""


def dang_thanh(ten, dung, hinh, tieu, phu="", ic=None, so=None, mau="do"):
    def ht(o, hinh=hinh):
        a, b, c = MAU_THANH.get(o.get("mau", mau), MAU_THANH["do"])
        trai = f'<div class="so">{e(o["so"])}</div>' if o.get("so") else ""
        bieu = icon(o["icon"]) if o.get("icon") else ""
        duoi = '<i class="duoi"></i>' if hinh in ("chu-nhat",) else ""
        return (f'<div class="th {hinh}" style="--a:{a};--b:{b};--c:{c}">{trai}<div class="tb">{bieu}<span><b>{e(o["tieu_de"])}</b>'
                + (f'<small>{e(o["phu"])}</small>' if o.get("phu") else "") + f'</span><i class="sh"></i></div>{duoi}</div>')
    o = {"tieu_de": tieu, "phu": phu, "mau": mau, **({"icon": ic} if ic else {}), **({"so": so} if so else {})}
    TAGS[ten] = dict(ten=ten, dung=dung, bo=2, o=o, html=ht, css=CSS_THANH, vao=lambda s, t, d: [
        f'tl.fromTo("{s} .so",{{scale:0}},{{scale:1,duration:{d(.4)},ease:"back.out(2.5)"}},{t:.2f});',
        f'tl.fromTo("{s} .tb",{{scaleX:0}},{{scaleX:1,duration:{d(.5)},ease:"power3.out"}},{t + .1:.2f});',
        f'tl.fromTo("{s} .duoi",{{scaleX:0}},{{scaleX:1,duration:{d(.25)}}},{t + .45:.2f});',
        f'tl.fromTo("{s} .tb span,{s} .tb .ic",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:{d(.35)},stagger:{d(.08)}}},{t + .4:.2f});',
        f'tl.fromTo("{s} .sh",{{left:"-40%"}},{{left:"120%",duration:{d(.8)},ease:"power1.inOut"}},{t + .7:.2f});'])


# ---------- Bộ 2: thanh tên (12, chọn màu do / xanh / vang trong ô "mau") ----------
dang_thanh("thanh-lo-dat", "Diện tích, lô đất", "vat", "Lô đất [...] m²", "Vinhomes Hóc Môn", mau="xanh")
dang_thanh("thanh-gia-thue", "Giá thuê, giá từ (có nguồn)", "chu-nhat", "CĂN HỘ [...]", "giá thuê từ [...] triệu/tháng")
dang_thanh("thanh-loai-can", "Tên loại căn", "chu-nhat", "CĂN 2 PHÒNG NGỦ", "[...] m² · view nội khu", ic="nha", mau="vang")
dang_thanh("thanh-so", "Ý số 1, 2, 3", "vat", "Tầm nhìn rộng", "view toàn cảnh", so="1")
dang_thanh("thanh-tien-ich", "Tiện ích", "ten", "Tiện ích nội khu", "hồ bơi · công viên · trường học", ic="sao", mau="xanh")
dang_thanh("thanh-du-an", "Tên dự án", "luc", "VINHOMES CẦN GIỜ", "dự án đang phân phối")
dang_thanh("thanh-lien-he", "Kêu gọi liên hệ", "vien", "LIÊN HỆ HÀO", "để nhận bảng tính dòng tiền", ic="dien-thoai")
dang_thanh("thanh-ban-tin", "Bản tin, cập nhật có ngày", "chu-nhat", "BẢN TIN BĐS [...]", "cập nhật ngày [...]")
dang_thanh("thanh-dich-vu", "Dịch vụ", "luc", "TƯ VẤN DÒNG TIỀN", "miễn phí bảng tính", mau="vang")
dang_thanh("thanh-vi-tri", "Vị trí, kết nối", "ten", "Vị trí dự án", "cách trung tâm [...] km", ic="ghim")
dang_thanh("thanh-chinh-sach", "Chính sách (phải có nguồn)", "vat", "CHÍNH SÁCH [...]", "nguồn: chủ đầu tư, ngày [...]", ic="the")
dang_thanh("thanh-nguoi-noi", "Tên người nói", "vien", "LÊ DƯƠNG HÀO", "Hào Sky Land", ic="sao", mau="vang")

# ---------- Bộ 3: tiêu đề phối chữ viết tay + đậm + phát sáng ----------
dang_dong("td-uu-dai", "Ưu đãi có số (phải có nguồn)", 3, ["tay trang 60 x-120|Ưu đãi", "dam vang sang 120 y-10|[...] triệu"])
dang_dong("td-buoc-thuc-hien", "Số bước + tiêu đề", 3, ["hep cam 200 ben|5", "dam trang 72|Bước", "dam trang 72|mua nhà", "hh cam duoi|đúng quy trình"])
dang_dong("td-de-dang", "Câu ngắn hai màu", 3, ["dam trang 96|dễ dàng", "dam-n xanh sang 96 y-12|vay vốn"])
dang_dong("td-so-huu", "Không gian sống", 3, ["tay trang 54 x-160|Sở hữu", "dam xanh sang 84|Không Gian Sống", "tay xanh 56 x140 y-6|đẳng cấp"])
dang_dong("td-can-ho-mau", "Giới thiệu căn mẫu", 3, ["tay kem 50 x-140|Căn hộ mẫu", "dam vang 76|VINHOMES HÓC MÔN", "nho kem 30 x180|Hào Sky Land"])
dang_dong("td-uu-dai-vang", "Ưu đãi nổi bật", 3, ["dam trang 56 x-150|Ưu đãi", "tay vang sang 120 y-80 x80|Vàng", "hh xanh y-6|[...] / tháng"])
dang_dong("td-biet-thu", "Loại hình + phong cách", 3, ["tay trang 52 x-150|Biệt thự", "dam xanh 76|PHONG CÁCH", "tay trang 52 x150|hiện đại"])
dang_dong("td-mot-can", "Số + chữ viết tay", 3, ["hep cam 200 ben|1", "dam trang 90|Căn hộ", "tay vang 64|đáng sống"])
dang_dong("td-so-huu-ngay", "Loại căn", 3, ["tay hong 50 x-160|Phù hợp", "serif-hoa trang 96|CĂN 2 NGỦ", "tay vang 48 x170|gia đình trẻ"])
dang_dong("td-bo-ra", "Số tiền lớn (có nguồn)", 3, ["tay trang 54 x-130|Vốn từ", "hep vang sang 160 y-10|[...] tỷ", "tay trang 50 x120|cho căn 2 ngủ"])
dang_dong("td-thang-hoa", "Cảm xúc, khoảnh khắc", 3, ["tay trang 46 x-150|Khoảnh khắc", "serif vang sang 96|Về Nhà", "tay vang 46 x170|bình yên"])
dang_dong("td-luu-giu", "Câu cảm xúc 3 tầng", 3, ["serif trang 56 x-150|Lưu giữ", "tay trang 130 y-6|Tổ ấm", "serif trang 50 x110|cho con", "hh vang y10|sống xanh mỗi ngày"])

# ---------- Bộ 4: 15 hiệu ứng bất động sản (chữ có chân sang trọng + viết tay + biểu tượng) ----------
dang_dong("bds-song-sang", "Phong cách sống", 4, ["tay vang 56 x-120|Đậm chất", "serif-hoa kim 96|SỐNG XANH", "serif kem 40|trong từng không gian"])
dang_dong("bds-tam-diem", "Vị trí trung tâm", 4, ["nho-hoa kem 28|đầu tư dự án", "serif-hoa kim 100|TÂM ĐIỂM", "tay trang 56 x120 y-10|kết nối khu Tây Bắc"])
dang_dong("bds-ben-song", "Không gian + biểu tượng tòa nhà", 4, ["dam trang 44 icon-toa-nha|không gian", "dam trang 76|BÊN DÒNG SÔNG", "tay trang 50 x120 y-6|nhịp sống khác biệt"])
dang_dong("bds-bieu-tuong", "Danh hiệu + nhãn", 4, ["tay trang 50 x-110|Biểu tượng", "serif kim sang 110 y-10|Sống Xanh", "hh vang|trong lòng thành phố"])
dang_dong("bds-cham-bien", "Biển, nghỉ dưỡng", 4, ["tay trang 50 x-150|một bước", "serif kim 110 y-6|Chạm Biển", "hh xanh|Cần Giờ", "tay trang 48 x110 y4|nghỉ dưỡng"])
dang_dong("bds-dinh-danh", "Định danh dự án", 4, ["tay trang 50|Định danh", "serif xanh sang 110 y-6|Đô Thị Biển", "dam-n trang 38|Vinhomes Cần Giờ"])
dang_dong("bds-vi-tri", "Vị trí", 4, ["tay trang 54 x-90|Vị trí", "serif vang sang 120 y-16|Kết Nối", "serif trang 40|[...] phút về trung tâm"])
dang_dong("bds-view-song", "Loại căn + view", 4, ["tay trang 50 x-60|Căn hộ", "serif-hoa trang 100|VIEW SÔNG", "tay trang 50 x120 y-8|thoáng mát"])
dang_dong("bds-toa-do", "Tọa độ + ghim", 4, ["dam trang 50 x-90|Tọa độ", "dam xanh sang 100 icon-ghim|Trục Chính", "serif trang 40|gần hạ tầng [...]"])
dang_dong("bds-dai-do-thi", "Tên đại đô thị + nhãn", 4, ["dam-n xanh 40 x-120|Đại đô thị", "hh xanh 56|VINHOMES HÓC MÔN"])
dang_dong("bds-bao-chung", "Cam kết của chủ đầu tư (có nguồn)", 4, ["tay trang 54 x-100|Pháp lý", "dam vang 66|RÕ RÀNG", "nho kem 28|nguồn: [...]"])
dang_dong("bds-khong-gian-mo", "Căn hộ + biểu tượng nhà", 4, ["serif trang 70 icon-nha|Căn Hộ", "hep trang 86|KHÔNG GIAN MỞ", "serif kem 36|nâng tầm cuộc sống"])
dang_dong("bds-song-dinh", "Khám phá", 4, ["serif kem 36|Khám phá không gian", "serif-hoa kim 100|SỐNG XANH", "dam-n trang 30 x-160|VINHOMES", "tay xanh 50 x110 y-30|Hóc Môn"])
dang_dong("bds-oc-dao", "Xanh giữa đô thị", 4, ["dam luc 66|ỐC ĐẢO", "dam luc sang 120 y-6|XANH", "nho-hoa trang 28|giữa lòng", "tay luc 66 x60 y-6|Đô Thị"])
dang_dong("bds-dong-tien", "Dòng tiền", 4, ["tay trang 48 x-140|Bài toán", "dam luc sang 86|DÒNG TIỀN", "tay trang 50 x150 y-10|mỗi tháng", "hh xanh y8|sau khi trừ tiền vay"])

# ---------- Bộ 5: talking head (chữ hiện từng từ cạnh người nói; đặt x 0,3 hoặc 0,7) ----------
dang_dong("th-mang-lai", "Lợi ích chính", 5, ["nho trang 34 x-60|em mang lại", "dam-n xanh sang 84 y-6|BẢNG TÍNH"], True)
dang_dong("th-hang-c", "Loại căn + nhãn", 5, ["hh xanh 40|CĂN 2 NGỦ", "dam-n xanh 64 y4|vừa túi tiền"], True)
dang_dong("th-day-la", "Câu dài 3 nhịp", 5, ["dam trang 50|đây là", "dam xanh sang 64 y-6|căn dành cho", "dam xanh sang 64 x40 y-8|gia đình"], True)
dang_dong("th-con-so", "Con số nóng (có nguồn)", 5, ["dam-n trang 44 x-90|lãi vay", "dam-n cam sang 120 y-10|[...]%", "nho trang 34 x60|năm đầu"], True)
dang_dong("th-dep-nhat", "So sánh nhất", 5, ["dam vang 46 x-80|VIEW", "dam-n cam sang 92 y-10|đẹp nhất", "nho trang 32|toàn dự án"], True)
dang_dong("th-chat-luong", "Hai cụm đối", 5, ["nho trang 34 x-70|Pháp lý", "dam-n xanh 76|RÕ RÀNG", "nho trang 32 x80|không thể bỏ qua"], True)
dang_dong("th-tam-tri", "Câu cảm xúc", 5, ["nho trang 34|cho", "dam cam 56 y-4|GIA ĐÌNH BẠN", "dam trang 80 y8|Tổ ấm"], True)
dang_dong("th-chan", "Nỗi đau + giải pháp", 5, ["dam trang 76|Chán", "nho trang 34|đi thuê nhà?", "dam-n xanh sang 70 y6|có nhà riêng"], True)
dang_dong("th-an-toan", "Từ khoá an toàn", 5, ["nho trang 32 x-70|công nghệ", "dam trang 100|AN TOÀN", "nho trang 30 x80|cho cả nhà"], True)
dang_dong("th-ben-bi", "Một từ khoá nhấn", 5, ["nho trang 32 x-80|độ", "dam-n xanh sang 92|BỀN BỈ", "nho trang 30 x60|theo năm tháng"], True)

# ---------- Bộ 6: ưu đãi (phiếu, top, nhãn giảm, đổi chữ) ----------
dang_dong("ud-glow", "Tiêu đề hai màu", 6, ["dam hong sang 96|SỐNG XANH", "dam trang 96 y-10|MỖI NGÀY"])
dang_dong("ud-giam-den", "Nhãn giảm (có nguồn)", 6, ["hh hong 40 icon-the|chiết khấu đến", "dam trang 130 y6|[...]%"])
dang_dong("ud-bieu-tuong", "Danh hiệu + nhãn hồng", 6, ["tay trang 50 x-100|Biểu tượng", "serif vang sang 104 y-14|An Cư", "hh hong|nâng tầm tổ ấm"])
dang_dong("ud-top", "Top N", 6, ["hep hong 200 ben|3", "tay hong 60|Top", "dam trang 40|LÝ DO NÊN MUA", "dam vang 56|Ở THỰC"])
dang_dong("ud-buoc-cham", "Số bước", 6, ["hep vang 200 ben|4", "tay vang 60|Bước", "dam trang 56|CHUẨN BỊ VỐN", "nho trang 30|trước khi xem nhà"])
TAGS["ud-phieu"] = dict(ten="ud-phieu", dung="Phiếu 2 ô: chính sách, quà (có nguồn)", bo=6, o={"a1": "HỖ TRỢ", "a2": "LÃI [...]", "b1": "QUÀ TẶNG", "b2": "[...]"},
    html=lambda o: (f'<div class="ph"><div class="pc"><small>{e(o["a1"])}</small><b>{e(o["a2"])}</b></div><i class="pd"></i>'
                    f'<div class="pc"><small>{e(o["b1"])}</small><b>{e(o["b2"])}</b></div></div>'),
    css=""".ph{display:inline-flex;align-items:stretch;background:linear-gradient(180deg,#ff6b81,#e0284f);border-radius:18px;box-shadow:0 10px 30px #0007;overflow:hidden}
.ph .pc{padding:18px 40px;text-align:center;color:#fff}.ph .pc small{display:block;font:800 28px Montserrat;opacity:.9}.ph .pc b{display:block;font:900 72px/1.05 Montserrat}
.ph .pd{width:0;border-left:4px dashed #ffffffaa;margin:14px 0}""",
    vao=lambda s, t, d: [f'tl.fromTo("{s} .ph",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:{d(.45)},ease:"power3.out"}},{t:.2f});',
                         f'tl.fromTo("{s} .pc",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{d(.35)},stagger:{d(.15)}}},{t + .3:.2f});'])
TAGS["ud-doi-hop"] = dict(ten="ud-doi-hop", dung="Phương pháp + đổi chữ trong hộp sáng", bo=6, o={"tren": "Giải pháp", "chinh": "VAY [...]%", "doi": "lãi cố định|ân hạn gốc|trả góp đều"},
    html=lambda o: (f'<div class="dh"><div class="dht">{e(o["tren"])}</div><div class="dhc">{e(o["chinh"])}</div><div class="dhw">'
                    + "".join(f'<span class="dcd">{e(w.strip())}</span>' for w in o["doi"].split("|")) + "</div></div>"),
    css=""".dh{display:inline-block;text-align:center}.dht{font-family:'Dancing Script';font-weight:700;font-size:56px;color:#fff;margin-left:-160px}
.dhc{font:700 120px/1 Oswald;color:#7ff2c8;text-transform:uppercase}.dhw{position:relative;height:110px;margin-top:8px;background:linear-gradient(90deg,transparent,#ffffff22,transparent)}
.dhw .dcd{position:absolute;left:50%;top:6px;transform:translateX(-50%);white-space:nowrap;font:500 84px 'Playfair Display';color:#7ff2c8;opacity:0}""",
    vao=lambda s, t, d: [f'tl.fromTo("{s} .dht",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{d(.5)}}},{t:.2f});',
                         f'tl.fromTo("{s} .dhc",{{opacity:0,scale:1.3,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out"}},{t + .2:.2f});'],
    doi=True)


def ve(s, sel, d, H, YT=False):
    """HTML khối + lệnh GSAP (vào, đổi chữ, ra) cho một tag. s: mục texts kind 'tag'."""
    T = TAGS[s["tag"]]
    o = {**T["o"], **{k: str(v) for k, v in s.get("o", {}).items()}}
    st, du = s["start"], s["dur"]
    a = T["vao"](sel, st, d)
    if T.get("doi"):  # đổi chữ: chia đều thời gian đứng cho từng chữ
        n = len(o["doi"].split("|")); hold = max(0.6, (du - 1.0) / n)
        for k in range(n):
            t0 = st + 0.35 + k * hold
            a.append(f'tl.fromTo("{sel} .dcd:nth-child({k + 1})",{{opacity:0,y:30,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{d(.35)}}},{t0:.2f});')
            if k < n - 1:
                a.append(f'tl.to("{sel} .dcd:nth-child({k + 1})",{{opacity:0,y:-30,filter:"blur(10px)",duration:{d(.25)}}},{t0 + hold - .25:.2f});')
    # ra: vệt nhoè ngang (như bộ mẫu)
    a.append(f'tl.to("{sel} > div",{{opacity:0,x:-90,scaleX:1.25,filter:"blur(16px)",duration:{d(.3)},ease:"power2.in"}},{st + du - .32:.2f});')
    top = float(s.get("y", 0.24)) * H / (0.62 if YT else 1)
    lech = (float(s.get("x", 0.5)) - 0.5) * 100  # x: tâm theo chiều ngang (talking head đặt 0,3 hoặc 0,7 cạnh người nói)
    return (f'<div style="position:absolute;left:0;right:0;top:{top:.0f}px;transform:translate({lech:.0f}%,-50%);text-align:center">{T["html"](o)}</div>', a)


def css(tags):
    return "\n".join(dict.fromkeys(TAGS[t]["css"] for t in sorted(set(tags)) if t in TAGS))  # khung chung chỉ chèn CSS một lần


def _xem_thu():
    """Timeline thử: cả bộ tag nối nhau, mỗi tag 2,6 giây (dùng để dựng video xem thử)."""
    return [{"kind": "tag", "tag": k, "start": round(0.3 + i * 2.6, 2), "dur": 2.4, "o": dict(v["o"])} for i, (k, v) in enumerate(TAGS.items())]


def _tu_kiem():
    from lop_chu import tao
    from timeline import check
    tl = {"version": 1, "meta": {"platform": "tiktok", "style": "edit-phim"}, "clips": [{"file": "a.mp4", "in": 0, "dur": 200}],
          "transitions": [], "texts": _xem_thu()}
    assert check(tl) == [], check(tl)
    p = tao(tl)
    for k, v in TAGS.items():
        for cls in re.findall(r'class="(\w+)"', v["html"](v["o"]))[:1]:
            assert f".{cls}" in v["css"], (k, cls)
    assert p.count('class="clip blk tag') == len(TAGS) and "Oswald" in p and "VỐN TỰ CÓ" in p
    bad = dict(tl, texts=[{"kind": "tag", "tag": "khong-co", "start": 0, "dur": 2}])
    assert check(bad), "tag lạ phải bị báo"
    assert "&lt;b&gt;" in ve({"tag": "buoc-so", "start": 0, "dur": 2, "o": {"so": "<b>"}}, "#x", lambda x: x, 1920)[0]  # chữ được thoát HTML
    print("OK", len(TAGS), "tag")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif sys.argv[1:] == ["--md"]:  # bảng danh mục cho docs/04-thu-vien/THU-VIEN-TAG.md
        TEN_BO = {1: "Bộ 1: tag cơ bản", 2: "Bộ 2: thanh tên kim loại (ô mau: do / xanh / vang)", 3: "Bộ 3: tiêu đề viết tay + đậm + phát sáng",
                  4: "Bộ 4: bất động sản sang trọng", 5: "Bộ 5: talking head (chữ hiện từng từ, đặt x 0,3 hoặc 0,7)", 6: "Bộ 6: ưu đãi"}
        for bo, ten in TEN_BO.items():
            print(f"\n### {ten}\n| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |\n|---|---|---|")
            for k, v in TAGS.items():
                if v["bo"] == bo:
                    print(f"| `{k}` | {v['dung']} | " + " · ".join(f"{a}: {b}" for a, b in v["o"].items()).replace("|", "\\|") + " |")
    elif sys.argv[1:] == ["--xem-thu"]:
        print(json.dumps(_xem_thu(), ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)
