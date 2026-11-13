"""Thư viện tag chữ: khung bố cục + chuyển động có sẵn, chỉ điền chữ của Hào (khối chữ kind "tag" trong timeline).
Học bố cục và nhịp từ bộ tag mẫu Hào gửi 13/11/2026 (bộ 1, 10 kiểu); dựng lại bằng HTML/GSAP, không dùng file gốc.
Mỗi tag: {"kind": "tag", "tag": "<tên>", "start", "dur", "o": {ô chữ}, "y": 0..1 (tâm theo chiều dọc, mặc định 0,24: trên mặt người nói)}.
Trong ô chữ: *từ* để tô màu nhấn; ô "doi" của tag doi-chu nhiều chữ cách nhau bằng "|".
Xem thử cả bộ: python3 scripts/tag_chu.py --xem-thu   ·   tự kiểm: python3 scripts/tag_chu.py --tu-kiem"""
import html, json, re, sys

CAM, VANG, KEM = "#d9772b", "#f2b33d", "#f3e6cf"
FONTS = "family=Montserrat:ital,wght@0,500;0,800;0,900;1,800;1,900&family=Oswald:wght@500;600;700&family=Playfair+Display:ital,wght@0,500;1,600&family=Be+Vietnam+Pro:wght@300;400"


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
    return f'<div style="position:absolute;left:0;right:0;top:{top:.0f}px;transform:translateY(-50%);text-align:center">{T["html"](o)}</div>', a


def css(tags):
    return "\n".join(TAGS[t]["css"] for t in sorted(set(tags)) if t in TAGS)


def _xem_thu():
    """Timeline thử: cả bộ tag nối nhau, mỗi tag 2,6 giây (dùng để dựng video xem thử)."""
    return [{"kind": "tag", "tag": k, "start": round(0.3 + i * 2.6, 2), "dur": 2.4, "o": dict(v["o"])} for i, (k, v) in enumerate(TAGS.items())]


def _tu_kiem():
    from lop_chu import tao
    from timeline import check
    tl = {"version": 1, "meta": {"platform": "tiktok", "style": "edit-phim"}, "clips": [{"file": "a.mp4", "in": 0, "dur": 30}],
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
    elif sys.argv[1:] == ["--xem-thu"]:
        print(json.dumps(_xem_thu(), ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)
