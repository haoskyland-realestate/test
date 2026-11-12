"""Dựng video test ~90s: flycam thật (9:16) + chuyển cảnh khối 3D + chữ động tiếng Việt + nhạc.
Chạy trong video-studio:  python3 projects/test90/make.py
Đầu vào: shots.json cùng thư mục (cảnh, mốc giây, chữ). Đầu ra: out/<tên thư mục>.mp4.
Làm video mới: chép cả thư mục test90 thành projects/<tên>, sửa shots.json, chạy python3 projects/<tên>/make.py.
Bản gốc tải lại từ Drive theo id (link chia sẻ công khai) vào projects/test90/build/raw/."""
import json, os, re, subprocess, shutil, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
B = os.path.join(HERE, "build"); os.makedirs(B, exist_ok=True)
NAME = os.path.basename(HERE)
W, H, FPS, TR = 1080, 1920, 30, 0.8  # TR: độ dài chuyển cảnh 3D (giây)
HF = ["npx", "--yes", "hyperframes@0.9.37"]
cfg = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf8"))
shots = cfg["shots"]

def run(cmd, **kw):
    print("+", " ".join(cmd)[:160]); subprocess.run(cmd, check=True, **kw)

def ff(*a): run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a])

# 1. Tải bản gốc các cảnh được chọn
os.makedirs(f"{B}/raw", exist_ok=True)
for s in shots:
    p = f"{B}/raw/{s['file']}"
    if not os.path.exists(p):
        run(["curl", "-sS", "-L", "--retry", "3", "-o", p,
             f"https://drive.usercontent.google.com/download?id={s['id']}&export=download&confirm=t"])

# 2. Cắt từng cảnh: khung dọc 9:16 từ 4K, chỉnh màu nhẹ, 30fps
for i, s in enumerate(shots):
    if os.path.exists(f"{B}/shot{i}.mp4"): continue  # đã cắt; xóa build/ nếu đổi cảnh
    fx = (s.get("focus", 0) + 1) / 2
    ff("-ss", str(s["in"]), "-t", str(s["dur"]), "-i", f"{B}/raw/{s['file']}", "-an",
       "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2,"
              f"eq=contrast=1.06:saturation=1.12,fps={FPS},format=yuv420p",
       "-c:v", "libx264", "-crf", "18", "-preset", "fast", f"{B}/shot{i}.mp4")

# 3. Khung cuối/đầu của các cảnh kề nhau -> chuyển cảnh khối 3D (CSS 3D trong HyperFrames)
cube = f"{B}/cube"; shutil.rmtree(cube, ignore_errors=True); os.makedirs(cube)
n = len(shots)
for i in range(n - 1):
    ff("-sseof", "-0.05", "-i", f"{B}/shot{i}.mp4", "-frames:v", "1", "-q:v", "3", f"{cube}/a{i}.jpg")
    ff("-i", f"{B}/shot{i+1}.mp4", "-frames:v", "1", "-q:v", "3", f"{cube}/b{i}.jpg")
faces = []
for i in range(n - 1):
    vert = i % 2 == 1  # xen kẽ xoay ngang / xoay dọc
    d = (H if vert else W) // 2
    fb = f"rotateX(-90deg) translateZ({d}px)" if vert else f"rotateY(90deg) translateZ({d}px)"
    faces.append(f"""<div id="t{i}" class="clip stage" data-start="{i*TR}" data-duration="{TR}" data-track-index="0">
  <div class="cube" id="c{i}"><img src="a{i}.jpg" style="transform:translateZ({d}px)"><img src="b{i}.jpg" style="transform:{fb}"></div></div>""")
tw = "\n".join(
    f'tl.to(st[{i}],{{r:90,duration:{TR},ease:"power2.inOut",onUpdate:()=>set({i},{int(i%2==1)})}},{i*TR});'
    f'tl.fromTo("#t{i}",{{scale:1}},{{scale:0.86,duration:{TR/2},ease:"power1.out",yoyo:true,repeat:1}},{i*TR});'
    for i in range(n - 1))
open(f"{cube}/index.html", "w", encoding="utf8").write(f"""<!doctype html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#06121c}}
#root{{position:relative;width:100%;height:100%}}
.stage{{position:absolute;inset:0;perspective:2400px}}
.cube{{position:absolute;inset:0;transform-style:preserve-3d}}
.cube img{{position:absolute;inset:0;width:{W}px;height:{H}px;backface-visibility:hidden}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{(n-1)*TR}" data-width="{W}" data-height="{H}">
{chr(10).join(faces)}</div><script>
const st=[...Array({n-1})].map(()=>({{r:0}}));
// Xoay quanh tâm khối: đẩy khối lùi nửa cạnh rồi xoay, mặt sau (cảnh kế) quay ra trước.
function set(i,v){{const d=v?{H//2}:{W//2};const c=document.getElementById("c"+i);
 c.style.transform=`translateZ(-${{d}}px) ${{v?"rotateX":"rotateY"}}(${{v?"":"-"}}${{st[i].r}}deg)`;}}
const tl=gsap.timeline({{paused:true}});
{tw}
for(let i=0;i<{n-1};i++)set(i,i%2);
window.__timelines["main"]=tl; tl.seek(0);
</script></body></html>""")
for f in ("gsap.min.js",):
    shutil.copy(os.path.join(ROOT, "node_modules/gsap/dist", f), cube)
json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}},
          open(f"{cube}/hyperframes.json", "w"))
open(f"{cube}/package.json", "w").write('{"name":"cube","private":true,"type":"module"}')
if not os.path.exists(f"{B}/cube.mp4"): run([*HF, "render", "-o", f"{B}/cube.mp4", "-q", "delivery", "--quiet"], cwd=cube)

# 4. Ghép: cảnh 0, chuyển 0, cảnh 1, ...
parts, starts, t = [], [], 0.0
for i in range(n):
    starts.append(t); parts.append(f"{B}/shot{i}.mp4"); t += shots[i]["dur"]
    if i < n - 1:
        ff("-ss", str(i * TR), "-t", str(TR), "-i", f"{B}/cube.mp4", "-an", "-vf", f"fps={FPS},format=yuv420p",
           "-c:v", "libx264", "-crf", "18", f"{B}/tr{i}.mp4")
        parts.append(f"{B}/tr{i}.mp4"); t += TR
total = t
open(f"{B}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
ff("-f", "concat", "-safe", "0", "-i", f"{B}/list.txt", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", f"{B}/base.mp4")

# 5. Lớp chữ động (nền trong suốt) theo mốc của từng cảnh
def words(text, cls=""):
    out = []
    for w in text.split(" "):
        m = re.fullmatch(r"\*(.+)\*([^\w]*)", w)  # *từ* hoặc *từ*? : tô vàng, giữ dấu câu
        out.append(f'<span class="w hl">{html.escape(m[1])}</span><span class="w">{html.escape(m[2])}</span>' if m
                   else f'<span class="w">{html.escape(w)}</span>')
    return f'<div class="line {cls}">{" ".join(out)}</div>'
blocks, anims = [], []
for i, s in enumerate(shots):
    st0 = starts[i] + (0.15 if i else 0.4); du = s["dur"] - (0.35 if i else 0.6)
    kind = s.get("kind", "line"); body = ""
    if kind == "hook":
        body = f'<div class="tag">{html.escape(s["tag"])}</div>' + "".join(words(l, "big") for l in s["lines"])
    elif kind == "section":
        body = (f'<div class="num">{s["num"]}</div><div class="title"><span class="bar"></span>{html.escape(s["title"])}</div>'
                + "".join(words(l) for l in s["lines"]))
    elif kind == "outro":
        body = (f'<div class="brand">HÀO SKY LAND</div><div class="gold"></div>' + "".join(words(l) for l in s["lines"])
                + f'<div class="note">{html.escape(s.get("note", ""))}</div>')
    else:
        body = "".join(words(l, "mid") for l in s["lines"])
    blocks.append(f'<div id="b{i}" class="clip blk {kind}" data-start="{st0:.2f}" data-duration="{du:.2f}" data-track-index="{1 + i % 2}">{body}</div>')
    a = [f'tl.fromTo("#b{i} .w",{{y:70,opacity:0,filter:"blur(12px)"}},{{y:0,opacity:1,filter:"blur(0px)",duration:0.55,ease:"power3.out",stagger:0.07}},{st0+0.25:.2f});',
         f'tl.to("#b{i}",{{opacity:0,y:-40,duration:0.35,ease:"power2.in"}},{st0+du-0.4:.2f});']
    if kind == "hook": a.append(f'tl.fromTo("#b{i} .tag",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.5}},{st0:.2f});')
    if kind == "section":
        a.append(f'tl.fromTo("#b{i} .num",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.6,ease:"expo.out"}},{st0:.2f});')
        a.append(f'tl.fromTo("#b{i} .bar",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power3.out"}},{st0+0.15:.2f});')
        a.append(f'tl.fromTo("#b{i} .title",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5}},{st0+0.15:.2f});')
    if kind == "outro":
        a.append(f'tl.fromTo("#b{i} .brand",{{opacity:0,letterSpacing:"40px"}},{{opacity:1,letterSpacing:"10px",duration:1.0,ease:"expo.out"}},{st0:.2f});')
        a.append(f'tl.fromTo("#b{i} .gold",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power3.out"}},{st0+0.4:.2f});')
        a.append(f'tl.fromTo("#b{i} .note",{{opacity:0}},{{opacity:0.7,duration:0.6}},{st0+1.2:.2f});')
    anims += a
ov = f"{B}/overlay"; shutil.rmtree(ov, ignore_errors=True); os.makedirs(ov)
shutil.copy(os.path.join(ROOT, "node_modules/gsap/dist/gsap.min.js"), ov)
open(f"{ov}/index.html", "w", encoding="utf8").write(f"""<!doctype html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}"><script src="gsap.min.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;800&display=swap"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:transparent;font-family:"Be Vietnam Pro",sans-serif;color:#fff}}
#root{{position:relative;width:100%;height:100%}}
.scrim{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(to top,rgba(4,14,24,.88),rgba(4,14,24,.55) 45%,rgba(4,14,24,0))}}
.topscrim{{position:absolute;left:0;right:0;top:0;height:14%;background:linear-gradient(to bottom,rgba(4,14,24,.55),rgba(4,14,24,0))}}
.logo{{position:absolute;top:70px;left:64px;font-weight:800;font-size:30px;letter-spacing:6px}}
.logo i{{display:inline-block;width:10px;height:10px;background:#d4a64a;border-radius:50%;margin-right:12px;vertical-align:middle}}
.prog{{position:absolute;top:0;left:0;height:8px;width:100%;background:#d4a64a;transform-origin:left;transform:scaleX(0)}}
.blk{{position:absolute;left:72px;right:72px;bottom:300px}}
.line{{font-size:58px;font-weight:600;line-height:1.28;margin-top:14px;text-shadow:0 4px 24px rgba(0,0,0,.45)}}
.line.big{{font-size:96px;font-weight:800;line-height:1.08;letter-spacing:-1.5px;margin-top:6px}}
.line.mid{{font-size:74px;font-weight:800;line-height:1.15;letter-spacing:-1px}}
.w{{display:inline-block}} .hl{{color:#f2c766}}
.tag{{display:inline-block;font-size:30px;font-weight:600;letter-spacing:4px;padding:12px 22px;border:2px solid #d4a64a;border-radius:40px;color:#f2c766;margin-bottom:28px}}
.num{{font-size:230px;font-weight:800;line-height:.9;color:transparent;-webkit-text-stroke:3px #f2c766;transform-origin:left bottom}}
.title{{position:relative;display:inline-block;font-size:76px;font-weight:800;margin:10px 0 10px;padding:0 10px}}
.bar{{position:absolute;left:0;right:0;bottom:8px;height:26px;background:#d4a64a;opacity:.85;z-index:-1;transform-origin:left}}
.outro{{bottom:auto;top:640px;text-align:center}}
.brand{{font-size:84px;font-weight:800;letter-spacing:10px;white-space:nowrap}}
.gold{{width:420px;height:6px;background:#d4a64a;margin:34px auto 30px;transform-origin:center}}
.note{{margin-top:60px;font-size:28px;opacity:.7}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="{W}" data-height="{H}">
<div class="clip scrim" data-start="0" data-duration="{total:.2f}" data-track-index="0"></div>
<div class="clip topscrim" data-start="0" data-duration="{total:.2f}" data-track-index="5"></div>
<div class="clip logo" data-start="0" data-duration="{starts[-1]:.2f}" data-track-index="3"><i></i>HÀO SKY LAND</div>
<div class="clip prog" id="prog" data-start="0" data-duration="{total:.2f}" data-track-index="4"></div>
{chr(10).join(blocks)}
</div><script>
const tl=gsap.timeline({{paused:true}});
tl.to("#prog",{{scaleX:1,duration:{total:.2f},ease:"none"}},0);
{chr(10).join(anims)}
window.__timelines["main"]=tl; tl.seek(0);
</script></body></html>""")
json.dump({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}},
          open(f"{ov}/hyperframes.json", "w"))
open(f"{ov}/package.json", "w").write('{"name":"overlay","private":true,"type":"module"}')
run([*HF, "render", "-o", f"{B}/overlay.webm", "--format", "webm", "--quiet"], cwd=ov)

# 6. Âm thanh: nhạc + tiếng vút ở tâm mỗi chuyển cảnh
wh = [str(starts[i + 1] - TR / 2) for i in range(n - 1)]
run(["python3", os.path.join(HERE, "music.py"), f"{total:.2f}", f"{B}/music.wav", *wh])

# 7. Ghép cuối: nền + lớp chữ trong suốt + âm thanh
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
ff("-i", f"{B}/base.mp4", "-c:v", "libvpx-vp9", "-i", f"{B}/overlay.webm", "-i", f"{B}/music.wav",
   "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
   "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
   "-t", f"{total:.2f}", os.path.join(ROOT, f"out/{NAME}.mp4"))
print(f"Xong: out/{NAME}.mp4 ({total:.1f}s, {n} cảnh)")
