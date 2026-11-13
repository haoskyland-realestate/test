"""Lớp chữ động (nền trong suốt): một trang HTML + GSAP dựng từ timeline.json. Dùng chung cho
bộ dựng (dung.py → HyperFrames quay thành video) và khung xem trước của app studio (trang chạy thẳng trong khung,
tua bằng window.dat(giây)), nên xem trước giống bản xuất: cùng chữ, cùng phong cách, cùng chuyển động."""
import html, re

import tag_chu

from timeline import layout, size
from effects import STYLES


def words(text, chars=False):
    esc = (lambda t: "".join(f'<span class="c">{html.escape(ch)}</span>' for ch in t)) if chars else html.escape
    out = []
    text = re.sub(r"\*([^*]+)\*", lambda m: "*" + m[1].replace(" ", "\u00a0") + "*", text)  # *nhiều từ* tô cả cụm, không tách
    for w in text.split(" "):
        m = re.fullmatch(r"\*(.+)\*([^\w]*)", w)  # *từ* hoặc *từ*? : tô màu nhấn, giữ dấu câu cùng dòng
        out.append(f'<span class="nw"><span class="w hl">{esc(m[1])}</span><span class="w">{esc(m[2])}</span></span>' if m
                   else f'<span class="w">{esc(w)}</span>')
    return " ".join(out)


def line(text, cls="", chars=False):
    return f'<div class="line {cls}"><div class="in">{words(text, chars)}</div></div>'


def tao(tl):
    """HTML lớp chữ của cả video (khung W×H theo nền tảng). Cần gsap.min.js nằm cùng địa chỉ."""
    W, H = size(tl)
    YT = W > H
    L = layout(tl)
    starts, total = L["starts"], L["total"]
    style = STYLES[tl.get("meta", {}).get("style", "hien-dai")]
    SP = style["speed"]

    def d(x):  # thời lượng chuyển động theo nhịp của phong cách
        return round(x * SP, 3)


    def anim_in(name, sel, t):
        return {
            "rise": f'tl.fromTo("{sel} .w",{{y:70,opacity:0,filter:"blur(12px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:{d(.55)},ease:"power3.out",stagger:{d(.07)}}},{t:.2f});',
            "mask": f'tl.fromTo("{sel} .line .in",{{yPercent:115}},{{yPercent:0,duration:{d(.7)},ease:"expo.out",stagger:{d(.12)}}},{t:.2f});',
            "blur": f'tl.fromTo("{sel} .w",{{opacity:0,filter:"blur(20px)"}},{{opacity:1,filter:"blur(0px)",duration:{d(.8)},ease:"power2.out",stagger:{d(.04)}}},{t:.2f});',
            "pop": f'tl.fromTo("{sel} .line",{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:{d(.6)},ease:"expo.out",stagger:{d(.12)}}},{t:.2f});',
            "track": f'tl.fromTo("{sel} .line",{{opacity:0,letterSpacing:"0.35em"}},{{opacity:1,letterSpacing:"0em",duration:{d(1.0)},ease:"expo.out",stagger:{d(.15)}}},{t:.2f});',
            "type": f'tl.fromTo("{sel} .c",{{opacity:0}},{{opacity:1,duration:0.01,stagger:{d(.035)}}},{t:.2f});',
            "word-pop": f'tl.fromTo("{sel} .w",{{opacity:0,scale:.3,y:30}},{{opacity:1,scale:1,y:0,duration:{d(.35)},ease:"back.out(2.2)",stagger:{d(.09)}}},{t:.2f});',
            "zoom-blur": f'tl.fromTo("{sel} .line",{{opacity:0,scale:1.35,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out",stagger:{d(.1)}}},{t:.2f});',
        }[name]


    blocks, anims = [], []
    for i, s in enumerate(tl.get("texts", [])):
        st0, du, kind = s["start"], s["dur"], s.get("kind", "line")
        an = s.get("anim") or style["anim"]
        ch = an == "type"
        sel = f"#b{i}"
        a = [anim_in(an, sel, st0 + 0.25)]
        if kind == "tag":  # tag chữ có sẵn: tự lo cả vào, đổi chữ và ra
            body, a = tag_chu.ve(s, sel, d, H, YT)
        elif kind == "hook":
            body = f'<div class="tag">{html.escape(s["tag"])}</div>' + "".join(line(l, "big", ch) for l in s["lines"])
            a.append(f'tl.fromTo("{sel} .tag",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:{d(.5)}}},{st0:.2f});')
        elif kind == "section":
            body = (f'<div class="num">{html.escape(s["num"])}</div><div class="title"><span class="bar"></span>{html.escape(s["title"])}</div>'
                    + "".join(line(l, "", ch) for l in s["lines"]))
            a += [f'tl.fromTo("{sel} .num",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:{d(.6)},ease:"expo.out"}},{st0:.2f});',
                  f'tl.fromTo("{sel} .bar",{{scaleX:0}},{{scaleX:1,duration:{d(.5)},ease:"power3.out"}},{st0 + 0.15:.2f});',
                  f'tl.fromTo("{sel} .title",{{opacity:0,y:30}},{{opacity:1,y:0,duration:{d(.5)}}},{st0 + 0.15:.2f});']
        elif kind == "outro":
            body = ('<div class="brand">HÀO SKY LAND</div><div class="gold"></div>' + "".join(line(l, "", ch) for l in s["lines"])
                    + f'<div class="note">{html.escape(s.get("note", ""))}</div>')
            a += [f'tl.fromTo("{sel} .brand",{{opacity:0,letterSpacing:"40px"}},{{opacity:1,letterSpacing:"10px",duration:{d(1.0)},ease:"expo.out"}},{st0:.2f});',
                  f'tl.fromTo("{sel} .gold",{{scaleX:0}},{{scaleX:1,duration:{d(.7)},ease:"power3.out"}},{st0 + 0.4:.2f});',
                  f'tl.fromTo("{sel} .note",{{opacity:0}},{{opacity:0.7,duration:{d(.6)}}},{st0 + 1.2:.2f});']
        elif kind == "lower":
            body = f'<div class="lbox">{line(s["title"], "lt", ch)}{line(s["sub"], "ls", ch) if s.get("sub") else ""}</div>'
            a.append(f'tl.fromTo("{sel} .lbox",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:{d(.5)},ease:"power3.out"}},{st0:.2f});')
        elif kind == "quote":
            body = ('<div class="qm">“</div>' + "".join(line(l, "q", ch) for l in s["lines"])
                    + (f'<div class="by">— {html.escape(s["by"])}</div>' if s.get("by") else ""))
            a += [f'tl.fromTo("{sel} .qm",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d(.6)},ease:"expo.out"}},{st0:.2f});',
                  f'tl.fromTo("{sel} .by",{{opacity:0}},{{opacity:0.8,duration:{d(.6)}}},{st0 + 1.0:.2f});']
        elif kind == "source":
            body = f'<div class="src">{html.escape(s["text"])}</div>'
            a = [f'tl.fromTo("{sel} .src",{{opacity:0,y:-12}},{{opacity:1,y:0,duration:{d(.5)}}},{st0:.2f});']
        elif kind == "checklist":
            body = ((line(s["title"], "mid", ch) if s.get("title") else "")
                    + "".join(f'<div class="ck"><span class="tick">✓</span><span class="ct">{words(it)}</span></div>' for it in s["items"]))
            a = ([anim_in(an, sel, st0)] if s.get("title") else []) + [
                f'tl.fromTo("{sel} .ck",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:{d(.45)},ease:"power3.out",stagger:{d(.45)}}},{st0 + 0.5:.2f});',
                f'tl.fromTo("{sel} .tick",{{scale:0}},{{scale:1,duration:{d(.4)},ease:"back.out(3)",stagger:{d(.45)}}},{st0 + 0.6:.2f});']
        elif kind == "title3d":  # nhãn nhỏ trên, chữ lớn, dòng nhỏ dưới; kiểu chữ lớn hiện theo phong cách (t3anim)
            t3 = style.get("t3anim", "zoom-blur")
            body = ((f'<div class="t3top">{words(s["top"])}</div>' if s.get("top") else "")
                    + f'<div class="t3big" style="font-size:{min(205, 1250 // max(len(s["big"]), 1))}px">{words(s["big"], t3 == "type")}</div>'  # chữ dài thì nhỏ lại cho vừa khung
                    + (f'<div class="t3sub">{words(s["sub"])}</div>' if s.get("sub") else ""))
            big = {"zoom-blur": f'tl.fromTo("{sel} .t3big",{{opacity:0,scale:1.5,filter:"blur(22px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out"}},{st0 + 0.15:.2f});',
                   "word-pop": f'tl.fromTo("{sel} .t3big .w",{{opacity:0,scale:.3,y:40}},{{opacity:1,scale:1,y:0,duration:{d(.35)},ease:"back.out(2.4)",stagger:{d(.1)}}},{st0 + 0.15:.2f});',
                   "type": f'tl.fromTo("{sel} .t3big .c",{{opacity:0}},{{opacity:1,duration:0.01,stagger:{d(.045)}}},{st0 + 0.15:.2f});',
                   "rise": f'tl.fromTo("{sel} .t3big",{{opacity:0,y:60}},{{opacity:1,y:0,duration:{d(.6)},ease:"power3.out"}},{st0 + 0.15:.2f});'}[t3]
            a = [f'tl.fromTo("{sel} .t3top",{{opacity:0,y:20,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{d(.35)}}},{st0:.2f});', big,
                 f'tl.fromTo("{sel} .t3sub",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:{d(.35)}}},{st0 + 0.45:.2f});']
        elif kind == "compare":  # thẻ so sánh 2 cột
            col = lambda k: f'<div class="col {k}"><div class="cl">{words(s[k + "_label"])}</div><div class="cv">{words(s[k + "_value"])}</div></div>'
            body = ((f'<div class="cmt">{words(s["title"])}</div>' if s.get("title") else "") + f'<div class="cols">{col("a")}<div class="vs">VS</div>{col("b")}</div>'
                    + (f'<div class="cmn">{words(s["note"])}</div>' if s.get("note") else ""))
            a = [f'tl.fromTo("{sel} .cmt",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:{d(.4)}}},{st0:.2f});',
                 f'tl.fromTo("{sel} .col.a",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:{d(.45)},ease:"power3.out"}},{st0 + 0.15:.2f});',
                 f'tl.fromTo("{sel} .col.b",{{opacity:0,x:120}},{{opacity:1,x:0,duration:{d(.45)},ease:"power3.out"}},{st0 + 0.3:.2f});',
                 f'tl.fromTo("{sel} .vs",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:{d(.35)},ease:"back.out(3)"}},{st0 + 0.5:.2f});',
                 f'tl.fromTo("{sel} .cv",{{scale:.6}},{{scale:1,duration:{d(.4)},ease:"back.out(2.5)",stagger:{d(.15)}}},{st0 + 0.55:.2f});',
                 f'tl.fromTo("{sel} .cmn",{{opacity:0}},{{opacity:.85,duration:{d(.4)}}},{st0 + 0.9:.2f});']
        elif kind == "stat":
            dec = int(s.get("decimals", 0))
            body = (f'<div class="stat"><span class="pre">{html.escape(s.get("prefix", ""))}</span><span class="val">0</span>'
                    f'<span class="suf">{html.escape(s.get("suffix", ""))}</span></div>' + line(s["label"], "", ch))
            a += [f'tl.fromTo("{sel} .stat",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d(.5)},ease:"power3.out"}},{st0:.2f});',
                  f'const o{i}={{v:0}};tl.to(o{i},{{v:{s["value"]},duration:{d(1.4)},ease:"power2.out",onUpdate:()=>fmt("{sel} .val",o{i}.v,{dec})}},{st0 + 0.1:.2f});']
        else:
            body = "".join(line(l, "mid", ch) for l in s["lines"])
        if kind != "tag": a.append(f'tl.to("{sel}",{{opacity:0,filter:"blur(14px)",scale:1.08,duration:{d(.3)},ease:"power2.in"}},{st0 + du - 0.35 * SP:.2f});' if kind in ("title3d", "compare")
                 else f'tl.to("{sel}",{{opacity:0,y:-40,duration:{d(.35)},ease:"power2.in"}},{st0 + du - 0.4 * SP:.2f});')
        blocks.append(f'<div id="b{i}" class="clip blk {kind} a-{an}" data-start="{st0:.2f}" data-duration="{du:.2f}" '
                      f'data-track-index="{(6 if kind == "source" else 1 + i % 2)}">{body}</div>')
        anims += a
    # Phụ đề (dưới giữa màn hình) và minh họa (nền phủ kín, chữ + danh sách đánh số)
    for j, x in enumerate(tl.get("subtitles", [])):
        blocks.append(f'<div id="s{j}" class="clip sub" data-start="{x["start"]:.2f}" data-duration="{x["dur"]:.2f}" data-track-index="7"><span>{words(x["text"])}</span></div>')
        # cả dòng bật lên cùng lúc; từ khóa (số, tên riêng) nảy thêm cho nổi
        anims.append(f'tl.fromTo("#s{j} > span",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:0.18,ease:"back.out(2)"}},{x["start"]:.2f});')
        anims.append(f'tl.fromTo("#s{j} .hl",{{scale:1.35}},{{scale:1,duration:0.3,ease:"back.out(3)"}},{x["start"] + 0.06:.2f});')
    for j, x in enumerate(tl.get("cards", [])):
        items = "".join(f'<div class="ci"><b>{k + 1}</b>{words(it)}</div>' for k, it in enumerate(x.get("items", [])))
        blocks.append(f'<div id="k{j}" class="clip card" data-start="{x["start"]:.2f}" data-duration="{x["dur"]:.2f}" data-track-index="8">'
                      f'<div class="cw">{f"""<div class="cs">{html.escape(x["step"])}</div>""" if x.get("step") else ""}'
                      f'<div class="ctt">{html.escape(x["title"])}</div>{items}</div></div>')
        anims += [f'tl.fromTo("#k{j}",{{opacity:0}},{{opacity:1,duration:{d(.25)}}},{x["start"]:.2f});',
                  f'tl.fromTo("#k{j} .ctt",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d(.5)},ease:"expo.out"}},{x["start"] + 0.1:.2f});',
                  f'tl.fromTo("#k{j} .ci",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:{d(.4)},ease:"power3.out",stagger:{d(.35)}}},{x["start"] + 0.45:.2f});']
    # Khung ngang YouTube: giữ nguyên thiết kế chữ của bản dọc, thu nhỏ (zoom) và đặt lại vị trí cho khung 1920×1080.
    # zoom thu nhỏ cả toạ độ của chính khối đó, nên số px ở đây là trước khi nhân 0,62.
    YT_CSS = """
    .scrim{height:48%}
    .blk{zoom:.62;left:150px;right:auto;width:1650px;bottom:190px}
    .outro{left:0;right:0;width:auto;top:330px;bottom:auto}
    .source{top:95px;bottom:auto}
    .sub{zoom:.62;left:0;right:0;top:auto;bottom:120px}
    .card{align-items:center;padding-top:0}
    .cw{zoom:.62;width:1700px}
    .logo{top:44px;left:56px;font-size:24px}
    .title3d,.compare{left:0;right:0;width:auto;top:330px;bottom:auto}
    """
    tags = [x["tag"] for x in tl.get("texts", []) if x.get("kind") == "tag"]
    tag_font = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{tag_chu.FONTS}&display=swap">' if tags else ""
    return (f"""<!doctype html><html lang="vi"><head><meta charset="UTF-8">
    <meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?{style["fonts"]}&display=swap">{tag_font}<style>
    :root{{--scrim:{style["scrim"]};--accent:{style["accent"]};--hl:{style["hl"]};--text:{style["text"]};
     --display:"{style["display"]}",sans-serif;--body:"{style["body"]}",sans-serif;--dw:{style["display_weight"]}}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{width:{W}px;height:{H}px;overflow:hidden;background:transparent;font-family:var(--body);color:var(--text)}}
    #root{{position:relative;width:100%;height:100%}}
    .scrim{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(to top,rgba(var(--scrim),.88),rgba(var(--scrim),.55) 45%,rgba(var(--scrim),0))}}
    .topscrim{{position:absolute;left:0;right:0;top:0;height:14%;background:linear-gradient(to bottom,rgba(var(--scrim),.55),rgba(var(--scrim),0))}}
    .logo{{position:absolute;top:70px;left:64px;font-weight:800;font-size:30px;letter-spacing:6px}}
    .logo i{{display:inline-block;width:10px;height:10px;background:var(--accent);border-radius:50%;margin-right:12px;vertical-align:middle}}
    .prog{{position:absolute;top:0;left:0;height:8px;width:100%;background:var(--accent);transform-origin:left;transform:scaleX(0)}}
    /* vùng an toàn TikTok: chữ chính nằm trên 440px đáy (mô tả, nút của app) */
    .blk{{position:absolute;left:72px;right:140px;bottom:440px}}
    .line{{font-size:58px;font-weight:600;line-height:1.28;margin-top:14px;text-shadow:0 4px 24px rgba(0,0,0,.45);transform-origin:left center}}
    .line.big{{font-family:var(--display);font-size:96px;font-weight:var(--dw);line-height:1.08;letter-spacing:-1.5px;margin-top:6px}}
    .line.mid{{font-family:var(--display);font-size:74px;font-weight:var(--dw);line-height:1.15;letter-spacing:-1px}}
    .a-mask .line{{overflow:hidden;padding-bottom:.12em}} .in{{display:block}}
    .w,.c{{display:inline-block}} .hl{{color:var(--hl)}} .nw{{white-space:nowrap}}
    .tag{{display:inline-block;font-size:30px;font-weight:600;letter-spacing:4px;padding:12px 22px;border:2px solid var(--accent);border-radius:40px;color:var(--hl);margin-bottom:28px}}
    .num{{font-family:var(--display);font-size:230px;font-weight:800;line-height:.9;color:transparent;-webkit-text-stroke:3px var(--hl);transform-origin:left bottom}}
    .title{{position:relative;display:inline-block;font-family:var(--display);font-size:76px;font-weight:var(--dw);margin:10px 0 10px;padding:0 10px}}
    .bar{{position:absolute;left:0;right:0;bottom:8px;height:26px;background:var(--accent);opacity:.85;z-index:-1;transform-origin:left}}
    .outro{{bottom:auto;top:640px;right:72px;text-align:center}}
    .brand{{font-family:var(--display);font-size:84px;font-weight:var(--dw);letter-spacing:10px;white-space:nowrap}}
    .gold{{width:420px;height:6px;background:var(--accent);margin:34px auto 30px;transform-origin:center}}
    .note{{margin-top:60px;font-size:28px;opacity:.7}}
    .lbox{{display:inline-block;padding:18px 30px 22px;border-left:10px solid var(--accent);background:rgba(var(--scrim),.72)}}
    .lt{{font-family:var(--display);font-size:60px;font-weight:var(--dw);margin:0}} .ls{{font-size:38px;font-weight:400;opacity:.85;margin-top:6px}}
    .qm{{font-family:"Playfair Display",serif;font-size:260px;line-height:.6;color:var(--accent);height:130px}}
    .line.q{{font-family:var(--display);font-size:70px;font-weight:var(--dw);font-style:italic;line-height:1.2}}
    .by{{margin-top:26px;font-size:36px;opacity:.8}}
    .source{{bottom:auto;top:150px}}
    .src{{display:inline-block;font-size:28px;padding:10px 20px;border-radius:30px;background:rgba(var(--scrim),.75);border:1px solid var(--accent)}}
    .ck{{display:flex;align-items:center;gap:26px;font-size:54px;font-weight:600;margin-top:26px;text-shadow:0 4px 24px rgba(0,0,0,.45)}}
    .tick{{flex:none;width:68px;height:68px;border-radius:50%;background:var(--accent);color:rgb(var(--scrim));font-size:42px;font-weight:800;display:flex;align-items:center;justify-content:center}}
    .stat{{font-family:var(--display);font-size:200px;font-weight:var(--dw);line-height:1;color:var(--hl);white-space:nowrap}}
    .stat .pre,.stat .suf{{font-size:90px;color:var(--text)}}
    .sub{{position:absolute;left:70px;right:70px;top:1150px;text-align:center;z-index:6}}
    .sub > span{{display:inline-block;font-family:var(--display);font-size:60px;font-weight:800;line-height:1.35;color:#fff;padding:10px 24px;border-radius:20px;background:rgba(var(--scrim),.6);text-shadow:0 3px 10px rgba(0,0,0,.55)}}
    .sub .hl{{display:inline-block;color:#14110a;background:var(--hl);font-size:1.2em;padding:0 14px;border-radius:12px;margin:0 3px;text-shadow:none}}
    .title3d{{left:50px;right:50px;bottom:auto;top:520px;text-align:center}}
    .t3top{{font-size:46px;font-weight:600;text-shadow:0 3px 14px rgba(0,0,0,.6)}}
    .t3big{{font-family:var(--display);font-size:205px;font-weight:var(--dw);line-height:1.02;letter-spacing:-3px;white-space:nowrap}}
    .t3sub{{font-size:42px;font-weight:600;margin-top:6px;text-shadow:0 3px 14px rgba(0,0,0,.6)}}
    .compare{{left:50px;right:50px;bottom:auto;top:560px;text-align:center}}
    .cmt{{font-family:var(--display);font-weight:var(--dw);font-size:64px;margin-bottom:26px;text-shadow:0 4px 18px rgba(0,0,0,.6)}}
    .cols{{display:flex;align-items:center;justify-content:center;gap:22px}}
    .col{{width:400px;padding:30px 22px;border-radius:26px;background:rgba(var(--scrim),.8);border:2px solid var(--accent)}}
    .col.b{{background:var(--accent);color:rgb(var(--scrim))}}
    .cl{{font-size:38px;font-weight:600}} .cv{{font-family:var(--display);font-weight:var(--dw);font-size:76px;line-height:1.1;margin-top:8px}}
    .col.a .cv{{color:var(--hl)}} .vs{{font-family:var(--display);font-weight:var(--dw);font-size:46px;color:var(--accent);text-shadow:0 3px 12px rgba(0,0,0,.6)}}
    .cmn{{margin-top:22px;font-size:34px;text-shadow:0 3px 12px rgba(0,0,0,.7)}}
    .card{{position:absolute;inset:0;background:{style["bg"]};z-index:5;display:flex;align-items:flex-start;justify-content:center;padding-top:340px}}
    .cw{{width:820px}} .cs{{font-size:30px;letter-spacing:6px;text-transform:uppercase;color:var(--hl);text-align:center}}
    .ctt{{font-family:var(--display);font-size:92px;font-weight:var(--dw);text-transform:uppercase;text-align:center;color:var(--hl);margin:10px 0 50px;line-height:1.05}}
    .ci{{display:flex;align-items:center;gap:26px;font-size:46px;font-weight:600;padding:22px 28px;margin-top:18px;border-radius:18px;background:rgba(255,255,255,.06)}}
    .ci b{{flex:none;width:64px;height:64px;border-radius:50%;background:var(--accent);color:{style["bg"]};display:flex;align-items:center;justify-content:center;font-size:36px}}
    {style.get("css", "")}
    {YT_CSS if YT else ""}
    {".blk.tag{left:0;right:0;top:0;bottom:0;width:auto;zoom:" + ("0.62" if YT else "1") + "}.blk.tag>div>div{filter:drop-shadow(0 4px 14px rgba(0,0,0,.55))}" + tag_chu.css(tags) if tags else ""}
    </style></head><body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="{W}" data-height="{H}">
    <div class="clip scrim" data-start="0" data-duration="{total:.2f}" data-track-index="0"></div>
    <div class="clip topscrim" data-start="0" data-duration="{total:.2f}" data-track-index="5"></div>
    <div class="clip logo" data-start="0" data-duration="{starts[-1]:.2f}" data-track-index="3"><i></i>HÀO SKY LAND</div>
    <div class="clip prog" id="prog" data-start="0" data-duration="{total:.2f}" data-track-index="4"></div>
    {chr(10).join(blocks)}
    </div><script>
    // Số kiểu Việt Nam: 1.234,5
    function fmt(sel,v,dec){{document.querySelector(sel).textContent=v.toLocaleString("vi-VN",{{minimumFractionDigits:dec,maximumFractionDigits:dec}});}}
    const tl=gsap.timeline({{paused:true}});
    tl.to("#prog",{{scaleX:1,duration:{total:.2f},ease:"none"}},0);
    {chr(10).join(anims)}
    window.__timelines=window.__timelines||{{}}; window.__timelines["main"]=tl; tl.seek(0);
    // Xem trước trong app (ngoài HyperFrames): tua tới giây t, ẩn/hiện từng lớp theo data-start/data-duration như HyperFrames
    window.dat=function(t){{tl.seek(t);document.querySelectorAll(".clip").forEach(e=>{{const s=+e.dataset.start,d=+e.dataset.duration;e.style.visibility=t>=s&&t<s+d?"visible":"hidden";}});}};
    </script></body></html>""")
