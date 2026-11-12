"""Dựng video từ timeline.json: flycam thật (TikTok dọc 9:16 hoặc YouTube ngang 16:9) + chuyển cảnh khối 3D + chữ động tiếng Việt + nhạc.
Chạy trong video-studio:  python3 scripts/dung.py projects/<tên> [--nhap]   (--nhap: dựng nháp nhanh, chất lượng thấp → out/<tên>.nhap.mp4)
Đầu vào: projects/<tên>/timeline.json (định dạng: scripts/timeline.py). Đầu ra: out/<tên>.mp4.
Bản gốc đặt sẵn ở projects/<tên>/build/raw/<file>, hoặc tự tải từ Drive theo "id" (thư mục chia sẻ bằng link)."""
import json, os, re, subprocess, shutil, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout, size
from effects import STYLES, LOOKS, TRANSITIONS
from mau import khung, tu_can
from am_thanh import tron_sfx

DRAFT = "--nhap" in sys.argv[2:]
if len(sys.argv) < 2 or any(a != "--nhap" for a in sys.argv[2:]):
    sys.exit("Dùng: python3 scripts/dung.py projects/<tên> [--nhap]")
HERE = os.path.abspath(sys.argv[1])
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NAME = os.path.basename(HERE)
OUTNAME = NAME + (".nhap" if DRAFT else "")
CRF, PRESET = ("28", "ultrafast") if DRAFT else ("18", "fast")
tl = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf8"))
errs = check(tl)
if errs:
    sys.exit("timeline.json chưa hợp lệ:\n- " + "\n- ".join(errs))
B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
W, H = size(tl)
FPS = 30
YT = W > H  # khung ngang YouTube
shots = tl["clips"]
L = layout(tl)
starts, total = L["starts"], L["total"]
HF = [shutil.which("npx") or "npx", "--yes", "hyperframes@0.9.37"]  # Windows: npx là npx.cmd, phải tìm đường dẫn đầy đủ
style = STYLES[tl.get("meta", {}).get("style", "hien-dai")]
SP = style["speed"]  # >1: chuyển động chậm hơn (sang trọng, tối giản)

def run(cmd, **kw):
    print("+", " ".join(cmd)[:160]); subprocess.run(cmd, check=True, **kw)

def ff(*a): run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a])

# 1. Tải bản gốc các cảnh được chọn
os.makedirs(f"{B}/raw", exist_ok=True)
for s in shots + tl.get("broll", []):
    p = f"{B}/raw/{s['file']}"
    if not os.path.exists(p):
        if not s.get("id"):
            sys.exit(f"Không thấy {p} và cảnh không có 'id' Drive để tải")
        run(["curl", "-sS", "-L", "--retry", "3", "-o", p,
             f"https://drive.usercontent.google.com/download?id={s['id']}&export=download&confirm=t"])

_m = tl.get("audio", {}).get("music")
if _m not in ("synth", None) and not os.path.exists(f"{B}/raw/{_m}"):
    sys.exit(f"Không thấy file nhạc {B}/raw/{_m} — chép file nhạc vào thư mục đó (hoặc chọn lại trong tab Âm thanh)")

# 2. Cắt từng cảnh về đúng khung (9:16 hoặc 16:9) từ 4K, chỉnh màu theo "look" (mặc định của phong cách), 30fps
for i, s in enumerate(shots):
    look = s.get("look") or style["look"]
    auto = tl.get("meta", {}).get("auto_color", True)  # tự cân màu từng cảnh (mặc định bật)
    key = json.dumps([s["file"], s["in"], s["dur"], s.get("focus", 0), s.get("fit"), look, auto, DRAFT, 3, W])  # 2: có chuyển tông HDR
    kf = f"{B}/shot{i}.key"  # nhớ cảnh đã cắt; đổi file/mốc/lệch khung/màu thì tự cắt lại
    if os.path.exists(f"{B}/shot{i}.mp4") and os.path.exists(kf) and open(kf).read() == key: continue
    ff("-ss", str(s["in"]), "-t", str(s["dur"]), "-i", f"{B}/raw/{s['file']}", "-an",
       "-vf", f"{khung(f'{B}/raw/' + s['file'], W, H, s.get('focus', 0), s.get('fit'))},"
              f"{tu_can(f'{B}/raw/' + s['file'], s['in'], s['dur']) if auto else 'null'},"
              f"{LOOKS[look][1]},fps={FPS},format=yuv420p",
       "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, f"{B}/shot{i}.mp4")
    open(kf, "w").write(key)

# 3. Chuyển cảnh giữa khung cuối cảnh trước và khung đầu cảnh sau:
#    css3d (khối, lật thẻ) dựng bằng HyperFrames; xfade (hòa tan, phóng, trượt...) dựng bằng FFmpeg.
n = len(shots)
TD = f"{B}/tr"; os.makedirs(TD, exist_ok=True)
trs = [(i, d, ty) for i, (_, d, ty) in enumerate(L["transitions"]) if ty != "cut"]
for i, d_tr, ty in trs:
    ff("-sseof", "-0.05", "-i", f"{B}/shot{i}.mp4", "-frames:v", "1", "-q:v", "3", f"{TD}/a{i}.jpg")
    ff("-i", f"{B}/shot{i+1}.mp4", "-frames:v", "1", "-q:v", "3", f"{TD}/b{i}.jpg")
    if TRANSITIONS[ty][1] == "xfade":
        ff("-loop", "1", "-framerate", str(FPS), "-t", str(d_tr), "-i", f"{TD}/a{i}.jpg",
           "-loop", "1", "-framerate", str(FPS), "-t", str(d_tr), "-i", f"{TD}/b{i}.jpg",
           "-filter_complex", f"[0:v][1:v]xfade=transition={TRANSITIONS[ty][2]}:duration={d_tr}:offset=0,format=yuv420p",
           "-t", str(d_tr), "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, f"{B}/tr{i}.mp4")
cube = f"{B}/cube"; shutil.rmtree(cube, ignore_errors=True); os.makedirs(cube)
c3 = [(i, d_tr, ty) for i, d_tr, ty in trs if TRANSITIONS[ty][1] == "css3d"]
faces, tws, off, seg3 = [], [], 0.0, {}
for k, (i, d_tr, ty) in enumerate(c3):
    shutil.copy(f"{TD}/a{i}.jpg", cube); shutil.copy(f"{TD}/b{i}.jpg", cube)
    m = {"h": 0, "v": 1, "flip": 2}[TRANSITIONS[ty][2]]
    d = 0 if m == 2 else (H if m == 1 else W) // 2
    fa = "rotateY(0deg)" if m == 2 else f"translateZ({d}px)"
    fb = {0: f"rotateY(90deg) translateZ({d}px)", 1: f"rotateX(-90deg) translateZ({d}px)", 2: "rotateY(180deg)"}[m]
    faces.append(f"""<div id="t{k}" class="clip stage" data-start="{off}" data-duration="{d_tr}" data-track-index="0">
  <div class="cube" id="c{k}"><img src="a{i}.jpg" style="transform:{fa}"><img src="b{i}.jpg" style="transform:{fb}"></div></div>""")
    tws.append(f'tl.to(st[{k}],{{r:90,duration:{d_tr},ease:"power2.inOut",onUpdate:()=>set({k},{m})}},{off});'
               f'tl.fromTo("#t{k}",{{scale:1}},{{scale:0.86,duration:{d_tr/2},ease:"power1.out",yoyo:true,repeat:1}},{off});'
               f'set({k},{m});')
    seg3[i] = off
    off += d_tr
if c3:
    open(f"{cube}/index.html", "w", encoding="utf8").write(f"""<!doctype html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{style["bg"]}}}
#root{{position:relative;width:100%;height:100%}}
.stage{{position:absolute;inset:0;perspective:2400px}}
.cube{{position:absolute;inset:0;transform-style:preserve-3d}}
.cube img{{position:absolute;inset:0;width:{W}px;height:{H}px;backface-visibility:hidden}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{off}" data-width="{W}" data-height="{H}">
{chr(10).join(faces)}</div><script>
const st=[...Array({len(c3)})].map(()=>({{r:0}}));
// m=0/1: khối xoay ngang/dọc quanh tâm (đẩy lùi nửa cạnh rồi xoay); m=2: lật thẻ 180°.
function set(i,m){{const c=document.getElementById("c"+i);const r=st[i].r;
 if(m==2){{c.style.transform=`rotateY(${{-2*r}}deg)`;return;}}
 const d=m?{H//2}:{W//2};c.style.transform=`translateZ(-${{d}}px) ${{m?"rotateX":"rotateY"}}(${{m?"":"-"}}${{r}}deg)`;}}
const tl=gsap.timeline({{paused:true}});
{chr(10).join(tws)}
window.__timelines["main"]=tl; tl.seek(0);
</script></body></html>""")
    shutil.copy(os.path.join(ROOT, "node_modules/gsap/dist/gsap.min.js"), cube)
    json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}},
              open(f"{cube}/hyperframes.json", "w"))
    open(f"{cube}/package.json", "w").write('{"name":"cube","private":true,"type":"module"}')
    ckey = json.dumps([style["bg"], DRAFT, W] + [[open(f"{B}/shot{i}.key").read(), open(f"{B}/shot{i+1}.key").read(), ty, d_tr] for i, d_tr, ty in c3])
    if not (os.path.exists(f"{B}/cube.mp4") and os.path.exists(f"{B}/cube.key") and open(f"{B}/cube.key").read() == ckey):
        run([*HF, "render", "-o", f"{B}/cube.mp4", "-q", "draft" if DRAFT else "delivery", "--quiet"], cwd=cube)
        open(f"{B}/cube.key", "w").write(ckey)
    for i, d_tr, _ in c3:
        ff("-ss", str(seg3[i]), "-t", str(d_tr), "-i", f"{B}/cube.mp4", "-an", "-vf", f"fps={FPS},format=yuv420p",
           "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, f"{B}/tr{i}.mp4")

# Chuyển cảnh gl-transitions: một khung WebGL trong HyperFrames, các chuyển cảnh nối tiếp, rồi cắt ra từng đoạn
glx = [(i, d_tr, ty) for i, d_tr, ty in trs if TRANSITIONS[ty][1] == "gl"]
if glx:
    from effects import GL_LIB
    gd = f"{B}/glc"; shutil.rmtree(gd, ignore_errors=True); os.makedirs(gd)
    segs, imgs, off, seg_gl = [], [], 0.0, {}
    for i, d_tr, ty in glx:
        shutil.copy(f"{TD}/a{i}.jpg", gd); shutil.copy(f"{TD}/b{i}.jpg", gd)
        imgs.append(f'<img id="a{i}" src="a{i}.jpg"><img id="b{i}" src="b{i}.jpg">')
        segs.append({"name": TRANSITIONS[ty][2], "a": f"a{i}", "b": f"b{i}", "off": off, "d": d_tr})
        seg_gl[i] = off; off += d_tr
    used = {s_["name"]: GL_LIB[s_["name"]] for s_ in segs}
    open(f"{gd}/index.html", "w", encoding="utf8").write(f"""<!doctype html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script><style>
*{{margin:0;padding:0}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}} img{{position:absolute;left:-9999px}}
#gl{{width:{W}px;height:{H}px;display:block}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{off}" data-width="{W}" data-height="{H}">
<canvas id="gl" class="clip" width="{W}" height="{H}" data-start="0" data-duration="{off}" data-track-index="0"></canvas>{"".join(imgs)}</div>
<script>{open(os.path.join(ROOT, "scripts", "gl_runtime.js"), encoding="utf8").read()}
const LIB={json.dumps(used)}, SEG={json.dumps(segs)}, r=glT(document.getElementById("gl"),LIB), st={{t:0}};
function draw(){{const t=st.t, s=SEG.find(x=>t>=x.off&&t<x.off+x.d)||SEG[SEG.length-1];
 const a=document.getElementById(s.a), b=document.getElementById(s.b); if(!a.complete||!b.complete)return;
 r.draw(s.name,a,b,Math.min(1,Math.max(0,(t-s.off)/s.d)));}}
const tl=gsap.timeline({{paused:true}}); tl.to(st,{{t:{off},duration:{off},ease:"none",onUpdate:draw}},0);
window.__timelines["main"]=tl; tl.seek(0); draw();
</script></body></html>""")
    shutil.copy(os.path.join(ROOT, "node_modules/gsap/dist/gsap.min.js"), gd)
    json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}, open(f"{gd}/hyperframes.json", "w"))
    open(f"{gd}/package.json", "w").write('{"name":"glc","private":true,"type":"module"}')
    gkey = json.dumps([DRAFT, W] + [[open(f"{B}/shot{i}.key").read(), open(f"{B}/shot{i+1}.key").read(), ty, d_tr] for i, d_tr, ty in glx])
    if not (os.path.exists(f"{B}/glc.mp4") and os.path.exists(f"{B}/glc.key") and open(f"{B}/glc.key").read() == gkey):
        run([*HF, "render", "-o", f"{B}/glc.mp4", "-q", "draft" if DRAFT else "delivery", "--quiet"], cwd=gd)
        open(f"{B}/glc.key", "w").write(gkey)
    for i, d_tr, _ in glx:
        ff("-ss", str(seg_gl[i]), "-t", str(d_tr), "-i", f"{B}/glc.mp4", "-an", "-vf", f"fps={FPS},format=yuv420p",
           "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, f"{B}/tr{i}.mp4")

# 4. Ghép: cảnh 0, chuyển cảnh 0 (nếu không phải cắt thẳng), cảnh 1, ...
has_tr = {i for i, _, _ in trs}
parts = []
for i in range(n):
    parts.append(f"{B}/shot{i}.mp4")
    if i in has_tr:
        parts.append(f"{B}/tr{i}.mp4")
open(f"{B}/list.txt", "w", encoding="utf8").write("".join(f"file '{p}'\n" for p in parts))
ff("-f", "concat", "-safe", "0", "-i", f"{B}/list.txt", "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, "-pix_fmt", "yuv420p", f"{B}/base.mp4")

# 5. Lớp chữ động (nền trong suốt) theo mốc trong timeline; màu, chữ, nhịp theo phong cách
def words(text, chars=False):
    esc = (lambda t: "".join(f'<span class="c">{html.escape(ch)}</span>' for ch in t)) if chars else html.escape
    out = []
    for w in text.split(" "):
        m = re.fullmatch(r"\*(.+)\*([^\w]*)", w)  # *từ* hoặc *từ*? : tô màu nhấn, giữ dấu câu cùng dòng
        out.append(f'<span class="nw"><span class="w hl">{esc(m[1])}</span><span class="w">{esc(m[2])}</span></span>' if m
                   else f'<span class="w">{esc(w)}</span>')
    return " ".join(out)


def line(text, cls="", chars=False):
    return f'<div class="line {cls}"><div class="in">{words(text, chars)}</div></div>'


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
        "zoom-blur": f'tl.fromTo("{sel} .line",{{opacity:0,scale:1.35,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out",stagger:{d(.1)}}},{t:.2f});',
    }[name]


blocks, anims = [], []
for i, s in enumerate(tl.get("texts", [])):
    st0, du, kind = s["start"], s["dur"], s.get("kind", "line")
    an = s.get("anim") or style["anim"]
    ch = an == "type"
    sel = f"#b{i}"
    a = [anim_in(an, sel, st0 + 0.25)]
    if kind == "hook":
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
    elif kind == "title3d":  # mẫu edit-phim-01: nhãn nhỏ trên, chữ lớn nổi 3D lao vào, dòng nhỏ dưới
        body = ((f'<div class="t3top">{words(s["top"])}</div>' if s.get("top") else "") + f'<div class="t3big" style="font-size:{min(205, 1500 // max(len(s["big"]), 1))}px">{words(s["big"])}</div>'
                + (f'<div class="t3sub">{words(s["sub"])}</div>' if s.get("sub") else ""))
        a = [f'tl.fromTo("{sel} .t3top",{{opacity:0,y:20,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{d(.35)}}},{st0:.2f});',
             f'tl.fromTo("{sel} .t3big",{{opacity:0,scale:1.5,filter:"blur(22px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:{d(.45)},ease:"expo.out"}},{st0 + 0.15:.2f});',
             f'tl.fromTo("{sel} .t3sub",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:{d(.35)}}},{st0 + 0.45:.2f});']
    elif kind == "stat":
        dec = int(s.get("decimals", 0))
        body = (f'<div class="stat"><span class="pre">{html.escape(s.get("prefix", ""))}</span><span class="val">0</span>'
                f'<span class="suf">{html.escape(s.get("suffix", ""))}</span></div>' + line(s["label"], "", ch))
        a += [f'tl.fromTo("{sel} .stat",{{opacity:0,y:40}},{{opacity:1,y:0,duration:{d(.5)},ease:"power3.out"}},{st0:.2f});',
              f'const o{i}={{v:0}};tl.to(o{i},{{v:{s["value"]},duration:{d(1.4)},ease:"power2.out",onUpdate:()=>fmt("{sel} .val",o{i}.v,{dec})}},{st0 + 0.1:.2f});']
    else:
        body = "".join(line(l, "mid", ch) for l in s["lines"])
    a.append(f'tl.to("{sel}",{{opacity:0,filter:"blur(14px)",scale:1.08,duration:{d(.3)},ease:"power2.in"}},{st0 + du - 0.35 * SP:.2f});' if kind == "title3d"
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
.title3d{left:0;right:0;width:auto;top:330px;bottom:auto}
"""
ov = f"{B}/overlay"; shutil.rmtree(ov, ignore_errors=True); os.makedirs(ov)
shutil.copy(os.path.join(ROOT, "node_modules/gsap/dist/gsap.min.js"), ov)
open(f"{ov}/index.html", "w", encoding="utf8").write(f"""<!doctype html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{style["fonts"]}&display=swap"><style>
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
.card{{position:absolute;inset:0;background:{style["bg"]};z-index:5;display:flex;align-items:flex-start;justify-content:center;padding-top:340px}}
.cw{{width:820px}} .cs{{font-size:30px;letter-spacing:6px;text-transform:uppercase;color:var(--hl);text-align:center}}
.ctt{{font-family:var(--display);font-size:92px;font-weight:var(--dw);text-transform:uppercase;text-align:center;color:var(--hl);margin:10px 0 50px;line-height:1.05}}
.ci{{display:flex;align-items:center;gap:26px;font-size:46px;font-weight:600;padding:22px 28px;margin-top:18px;border-radius:18px;background:rgba(255,255,255,.06)}}
.ci b{{flex:none;width:64px;height:64px;border-radius:50%;background:var(--accent);color:{style["bg"]};display:flex;align-items:center;justify-content:center;font-size:36px}}
{style.get("css", "")}
{YT_CSS if YT else ""}
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
window.__timelines["main"]=tl; tl.seek(0);
</script></body></html>""")
json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}},
          open(f"{ov}/hyperframes.json", "w"))
open(f"{ov}/package.json", "w").write('{"name":"overlay","private":true,"type":"module"}')
run([*HF, "render", "-o", f"{B}/overlay.webm", "--format", "webm", "-q", "draft" if DRAFT else "standard", "--quiet"], cwd=ov)

# 6. Âm thanh: giọng gốc của cảnh (nếu bật) + nhạc tổng hợp + tiếng vút ở tâm mỗi chuyển cảnh
audio = tl.get("audio", {})
voice = audio.get("voice", False)
mvol = audio.get("music_volume", 1.0) * (0.25 if voice else 1.0)  # có giọng thì nhạc nhỏ xuống
if audio.get("music", "synth") == "synth":
    wh = [str(t0 + d / 2) for t0, d, ty in L["transitions"] if ty != "cut"] if audio.get("whoosh", True) else []
    run([sys.executable, os.path.join(ROOT, "scripts/music.py"), f"{total:.2f}", f"{B}/music.wav", *wh])
elif audio.get("music"):  # file nhạc của Hào (build/raw/<file>): lặp nếu ngắn hơn video, mờ dần 2 giây cuối
    ff("-stream_loop", "-1", "-i", f"{B}/raw/{audio['music']}", "-vn", "-ac", "2", "-ar", "44100", "-t", f"{total:.2f}",
       "-af", f"afade=t=out:st={max(0, total - 2):.2f}:d=2", f"{B}/music.wav")
else:
    ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{total:.2f}", f"{B}/music.wav")
if voice:
    vparts = []
    for i, c in enumerate(shots):
        raw = f"{B}/raw/{c['file']}"
        has_a = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", raw],
                               capture_output=True, text=True).stdout.strip()
        src = ["-ss", str(c["in"]), "-t", str(c["dur"]), "-i", raw, "-vn"] if has_a else ["-f", "lavfi", "-t", str(c["dur"]), "-i", "anullsrc=r=44100:cl=stereo"]
        ff(*src, "-ac", "2", "-ar", "44100", "-t", str(c["dur"]), f"{B}/v{i}.wav"); vparts.append(f"{B}/v{i}.wav")
        if i < n - 1 and L["transitions"][i][1] > 0:
            ff("-f", "lavfi", "-t", str(L["transitions"][i][1]), "-i", "anullsrc=r=44100:cl=stereo", f"{B}/vs{i}.wav"); vparts.append(f"{B}/vs{i}.wav")
    open(f"{B}/vlist.txt", "w", encoding="utf8").write("".join(f"file '{p}'\n" for p in vparts))
    ff("-f", "concat", "-safe", "0", "-i", f"{B}/vlist.txt", "-c", "copy", f"{B}/voice.wav")

# Cảnh trám: cắt từng đoạn về đúng khung, cùng chỉnh màu của phong cách
brs = tl.get("broll", [])
for k, x in enumerate(brs):
    ff("-ss", str(x["in"]), "-t", str(x["dur"]), "-i", f"{B}/raw/{x['file']}", "-an",
       "-vf", f"{khung(f'{B}/raw/' + x['file'], W, H, x.get('focus', 0), x.get('fit'))},"
              f"{tu_can(f'{B}/raw/' + x['file'], x['in'], x['dur'])},{LOOKS[style['look']][1]},fps={FPS},format=yuv420p",
       "-c:v", "libx264", "-crf", CRF, "-preset", PRESET, f"{B}/br{k}.mp4")

# 7. Ghép cuối: nền (+ zoom) + cảnh trám + lớp chữ trong suốt + âm thanh
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
ins = ["-i", f"{B}/base.mp4", "-c:v", "libvpx-vp9", "-i", f"{B}/overlay.webm", "-i", f"{B}/music.wav"]
fc, cur = [], "0:v"
zs = tl.get("zooms", [])
if zs:  # phóng to khung trong từng đoạn (tính theo số khung hình)
    z = "1"
    for x in reversed(zs):
        z = f"if(between(in,{round(x['start'] * FPS)},{round((x['start'] + x['dur']) * FPS)}),{x['scale']},{z})"
    fc.append(f"[{cur}]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}[z]"); cur = "z"
for k, x in enumerate(brs):
    ins += ["-i", f"{B}/br{k}.mp4"]
    fc.append(f"[{3 + k}:v]setpts=PTS-STARTPTS+{x['start']}/TB[b{k}]")
    fc.append(f"[{cur}][b{k}]overlay=0:0:enable='between(t,{x['start']},{x['start'] + x['dur']})':eof_action=pass[o{k}]"); cur = f"o{k}"
fc.append(f"[{cur}][1:v]overlay=0:0:shortest=1,format=yuv420p[v]")
fc.append(f"[2:a]volume={mvol}[m]")
mix = ["[m]"]
if voice:
    ins += ["-i", f"{B}/voice.wav"]
    fc.append(f"[{3 + len(brs)}:a]anull[vo]"); mix.insert(0, "[vo]")
if tron_sfx(tl.get("sfx", []), total, f"{B}/sfx.wav"):  # hiệu ứng âm (thu-vien-am-thanh/) trộn sẵn thành một file
    ins += ["-i", f"{B}/sfx.wav"]
    fc.append(f"[{3 + len(brs) + bool(voice)}:a]anull[sx]"); mix.append("[sx]")
fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[a0]" if len(mix) > 1 else "[m]anull[a0]")
# Chuẩn âm lượng EBU R128 cho mạng xã hội (−14 LUFS, đỉnh −1,5 dB), cùng thuật toán ffmpeg-normalize dùng
fc.append("[a0]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
   "-c:v", "libx264", "-crf", "28" if DRAFT else "19", "-preset", "veryfast" if DRAFT else "medium",
   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.2f}", os.path.join(ROOT, f"out/{OUTNAME}.mp4"))
print(f"Xong: out/{OUTNAME}.mp4 ({total:.1f}s, {n} cảnh)")
