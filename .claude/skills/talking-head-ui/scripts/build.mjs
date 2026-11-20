#!/usr/bin/env node
// talking-head-ui builder: edit-plan.json + style.json -> dự án HyperFrames.
// Dùng: node build.mjs <projectDir> [--plan edit-plan.json] [--style <skill>/style.json]
// projectDir phải có assets/main.mp4 (và các file plan trỏ tới) + node_modules đã cài (xem setup.sh).
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const proj = path.resolve(args[0] || ".");
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const plan = JSON.parse(fs.readFileSync(path.resolve(proj, opt("--plan", "edit-plan.json")), "utf8"));
const style = JSON.parse(fs.readFileSync(path.resolve(opt("--style", path.join(here, "..", "style.json"))), "utf8"));

const W = style.canvas.width, H = style.canvas.height;
const P = style.presets[plan.meta.preset];
if (!P) throw new Error(`preset không tồn tại: ${plan.meta.preset}`);
const C = { ...P.colors, ...(plan.meta.accent ? { accent: plan.meta.accent, accentGradient: null, accentGlow: hexA(plan.meta.accent, 0.35) } : {}) };
const D = +plan.meta.duration;
const r3 = (n) => Math.round(n * 1000) / 1000;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const warn = [];

function hexA(hex, a) {
  const h = hex.replace("#", ""); const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${a})`;
}

// ---------- fonts: copy @fontsource files (latin, latin-ext, vietnamese) ----------
const FAM = { "sans-geo": "thu-geo", "sans-neo": "thu-neo", "serif-disp": "thu-serif" };
function buildFonts() {
  const req = createRequire(path.join(proj, "package.json"));
  const out = path.join(proj, "assets", "fonts"); fs.mkdirSync(out, { recursive: true });
  let css = "";
  for (const [key, f] of Object.entries(style.fonts)) {
    if (key === "note") continue;
    let pkgDir;
    try { pkgDir = path.dirname(req.resolve(`${f.package}/package.json`)); }
    catch { throw new Error(`Thiếu ${f.package}. Chạy setup.sh trong ${proj}`); }
    for (const face of f.faces) {
      const [w, st] = face.split("-");
      const file = path.join(pkgDir, st === "italic" ? `${w}-italic.css` : `${w}.css`);
      const src = fs.readFileSync(file, "utf8");
      for (const block of src.split("/*").slice(1)) {
        const name = block.slice(0, block.indexOf("*/")).trim();
        if (!/-(latin|latin-ext|vietnamese)-\d/.test(name)) continue;
        const woff = block.match(/url\(\.\/files\/([^)]+\.woff2)\)/)[1];
        const range = (block.match(/unicode-range:\s*([^;]+);/) || [])[1];
        fs.copyFileSync(path.join(pkgDir, "files", woff), path.join(out, woff));
        css += `@font-face{font-family:'${FAM[key]}';font-style:${st};font-weight:${w};font-display:block;src:url('assets/fonts/${woff}') format('woff2');${range ? `unicode-range:${range};` : ""}}\n`;
      }
    }
  }
  return css;
}
const fontCss = buildFonts();

// ---------- helpers ----------
function roleCss(roleName) {
  const r = style.roles[roleName];
  return `font-family:'${FAM[r.font]}';font-weight:${r.weight};font-style:${r.style};letter-spacing:${r.tracking}em;${r.case === "upper" ? "text-transform:uppercase;" : ""}`;
}
function fitSize(roleName, text, maxW, override) {
  const r = style.roles[roleName];
  const base = override || r.size;
  const chars = [...text].length || 1;
  const fit = Math.floor(maxW / (chars * r.widthFactor * (r.case === "upper" ? 1.12 : 1)));
  if (fit < base) warn.push(`co chữ "${text}" ${base}→${Math.max(fit, 28)}px để vừa ${maxW}px`);
  return Math.max(Math.min(base, fit), 28);
}
function accentFill(roleName) {
  const r = style.roles[roleName];
  if (!r.accent) return `color:${C.text};text-shadow:${C.captionShadow};`;
  if (C.accentGradient) return `background:linear-gradient(180deg,${C.accentGradient.join(",")});-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 ${GLOW}px ${C.accentGlow});`;
  return `color:${C.accent};filter:drop-shadow(0 0 ${GLOW}px ${C.accentGlow});`;
}
const GLOW = style.effects?.glowBlur ?? 8;
const inWindows = (t0, t1, wins) => wins.some(([a, b]) => t0 < b && t1 > a);

// ---------- windows ----------
const broll = plan.broll || [];
const emph = plan.emphasis || [];
const brollWins = broll.map((b) => [b.start, b.end]);
const emphWins = emph.map((e) => [e.start, e.end]);
for (const e of emph) if (e.behindSubject && !plan.source.cutout) warn.push(`khối ${e.id} behindSubject nhưng thiếu source.cutout: sẽ nằm trước người`);
for (const e of emph) if (inWindows(e.start, e.end, brollWins)) warn.push(`khối ${e.id} chồng lên b-roll`);
const dipWins = (plan.transitions || []).filter((t) => t.type === "dip-black").map((t) => [t.at, t.at + (t.duration || style.transitions["dip-black"].duration)]);
for (const e of emph) if (inWindows(e.start, e.end, dipWins)) warn.push(`khối ${e.id} chồng lên màn đen: kết thúc khối trước màn đen`);

// ---------- captions composition (captions + front emphasis) ----------
const A = style.animations;
let capHtml = "", capJs = "", capCss = "";
const capRole = P.caption.role;
let ci = 0;
for (const c of plan.captions) {
  let s = c.start, e = c.end;
  if (!P.caption.showDuringBroll && inWindows(s, e, brollWins)) continue;
  if (P.caption.hideWhileEmphasis && inWindows(s, e, emphWins)) continue;
  if (e - s < P.caption.minHold) e = s + P.caption.minHold;
  if (e > D) e = D;
  if (e <= s) continue;
  const id = `cap${ci++}`;
  const size = fitSize(capRole, c.text, 900);
  const fill = c.accent ? accentFill("hero") : `color:${C.text};opacity:${C.textOpacity ?? 1};text-shadow:${C.captionShadow};`;
  capHtml += `    <div id="${id}" class="clip cap" data-start="${r3(s)}" data-duration="${r3(e - s)}" style="top:${P.caption.y - size / 2}px"><span class="cap-in" style="font-size:${size}px;${roleCss(capRole)}${fill}">${esc(c.text)}</span></div>\n`;
  const an = A[P.caption.enter];
  const capDur = r3(Math.min(an.duration, Math.max(0.1, (e - s) / 4)));
  capJs += `  tl.fromTo("#${id} .cap-in", ${JSON.stringify(an.from)}, {...${JSON.stringify(an.to)}, duration:${capDur}, ease:"${an.ease}"}, ${r3(s)});\n`;
}

function emphBlock(e) {
  const anc = { ...style.anchors[e.anchor] };
  if (e.offset) { anc.x += e.offset.x || 0; anc.y += e.offset.y || 0; }
  const maxW = e.anchor === "head-band" ? anc.w : Math.min(anc.w, P.emphasis.maxWidth);
  const enter = e.enter || P.emphasis.enter, exit = e.exit || P.emphasis.exit;
  let html = `    <div id="${e.id}" class="clip emph" data-start="${r3(e.start)}" data-duration="${r3(e.end - e.start)}" data-layout-allow-overlap style="left:${anc.x}px;top:${anc.y}px;width:${anc.w}px;text-align:${anc.align}">\n`;
  let js = "";
  e.lines.forEach((ln, i) => {
    const size = fitSize(ln.role, ln.text, maxW, ln.size);
    const lid = `${e.id}-l${i}`;
    const gap = i === 0 ? 0 : Math.round(P.emphasis.lineGapEm * size);
    const r = style.roles[ln.role];
    const rot = r.rotate ? `transform:rotate(${r.rotate}deg);` : "";
    const al = ln.align ? `text-align:${ln.align};` : "";
    const ind = ln.indent ? `padding-left:${ln.indent}px;` : "";
    const op = r.accent ? 1 : (C.textOpacity ?? 1);
    html += `      <div id="${lid}" class="line" data-layout-allow-occlusion style="margin-top:${gap}px;${al}${ind}">` +
      (enter === "smear" && (r.accent || !A.smear.streak.onlyAccent) ? `<div class="streak" style="height:${Math.round(size * A.smear.streak.heightEm)}px;top:${Math.round(size * 0.35)}px;background:${r.accent ? C.accent : "rgba(255,255,255,0.85)"}"></div>` : "") +
      `<span class="settle"><span class="txt" style="font-size:${size}px;line-height:1;${roleCss(ln.role)}${accentFill(ln.role)}opacity:${op};${rot}">${esc(ln.text)}</span></span></div>\n`;
    const at = r3(Math.max(e.start, Math.min(ln.at ?? e.start, e.end - A[enter].duration - 0.4)));
    const an = A[enter];
    const f = { ...an.from }, t = { ...an.to };
    if ("blur" in f) { f.filter = `blur(${f.blur}px)`; delete f.blur; }
    if ("blur" in t) { t.filter = `blur(${t.blur}px)`; delete t.blur; }
    if (t.opacity === 0.92 || t.opacity === 1) t.opacity = 1;
    js += `  tl.fromTo("#${lid}", ${JSON.stringify(f)}, {...${JSON.stringify(t)}, duration:${an.duration}, ease:"${an.ease}"}, ${at});\n`;
    if (enter === "smear" && (r.accent || !A.smear.streak.onlyAccent)) {
      const sk = A.smear.streak;
      js += `  tl.fromTo("#${lid} .streak", {opacity:0, scaleX:0.6, filter:"blur(${sk.blur}px)"}, {opacity:${sk.peakOpacity}, scaleX:${sk.peakScaleX}, duration:${sk.peakAt}, ease:"power2.inOut"}, ${at});\n`;
      js += `  tl.to("#${lid} .streak", {opacity:0, duration:${r3(sk.duration - sk.peakAt)}, ease:"power2.inOut"}, ${r3(at + sk.peakAt)});\n`;
    }
    if (r.accent && ln.role !== "giant") {
      const settleDur = r3(Math.max(0.3, e.end - at - 0.4));
      js += `  tl.fromTo("#${lid} .settle", {scale:1}, {scale:${A["accent-settle"].scaleTo}, duration:${settleDur}, ease:"${A["accent-settle"].ease}"}, ${r3(at + 0.2)});\n`;
    }
  });
  html += `    </div>\n`;
  if (exit !== "cut") {
    const ex = A[exit]; const t = { ...ex.to };
    if ("blur" in t) { t.filter = `blur(${t.blur}px)`; delete t.blur; }
    const st = r3(e.end - ex.duration - ex.stagger * (e.lines.length - 1) - 0.02);
    js += `  tl.to(${JSON.stringify(e.lines.map((_, i) => `#${e.id}-l${i}`))}, {...${JSON.stringify(t)}, duration:${ex.duration}, ease:"${ex.ease}", stagger:${ex.stagger}}, ${st});\n`;
  }
  return { html, js };
}

let behindHtml = "", behindJs = "";
for (const e of emph) {
  const b = emphBlock(e);
  if (e.behindSubject && plan.source.cutout && plan.source.video) { behindHtml += b.html; behindJs += b.js; }
  else { capHtml += b.html; capJs += b.js; }
}

const blockCss = `
  .cap{position:absolute;left:0;width:${W}px;text-align:center;overflow:visible}
  .cap-in{display:inline-block;line-height:1;white-space:nowrap}
  .emph{position:absolute;overflow:visible}
  .line{position:relative;white-space:nowrap;line-height:1}
  .settle{display:inline-block;position:relative;z-index:1}
  .txt{display:inline-block;padding:0 0.06em}
  .streak{position:absolute;left:0;right:0;border-radius:999px;opacity:0;z-index:0}`;

function sceneFile(id, html, js, extraCss = "") {
  return `<template>
  <style>
${fontCss}
  #root{position:absolute;inset:0;overflow:visible}
${blockCss}
${extraCss}
  </style>
  <div id="root" data-composition-id="${id}" data-width="${W}" data-height="${H}" data-start="0" data-duration="${D}">
${html}  </div>
  <script>
  const tl = gsap.timeline({ paused: true });
${js}  window.__timelines["${id}"] = tl;
  </script>
</template>
`;
}

// ---------- fx composition ----------
let fxHtml = "", fxJs = "", fi = 0;
const T = style.transitions;
const fxList = [...(plan.transitions || [])];
for (const cam of plan.camera || []) if (cam.transition && cam.transition !== "cut") fxList.push({ at: cam.at, type: cam.transition });
for (const t of fxList) {
  const id = `fx${fi++}`;
  if (t.type === "flash-white") {
    const d = t.duration || T["flash-white"].duration;
    fxHtml += `    <div id="${id}" class="clip fx" data-start="${r3(t.at)}" data-duration="${r3(d)}"><div class="fill" style="background:${C.flash}"></div></div>\n`;
    fxJs += `  tl.fromTo("#${id} .fill", {opacity:${T["flash-white"].fromOpacity}}, {opacity:0, duration:${d}, ease:"${T["flash-white"].ease}"}, ${r3(t.at)});\n`;
  } else if (t.type === "dip-black") {
    const d = t.duration || T["dip-black"].duration, fi_ = T["dip-black"].fadeIn, fo = T["dip-black"].fadeOut;
    fxHtml += `    <div id="${id}" class="clip fx" data-start="${r3(t.at)}" data-duration="${r3(d)}"><div class="fill" style="background:${C.dip}"></div></div>\n`;
    fxJs += `  tl.fromTo("#${id} .fill", {opacity:0}, {opacity:1, duration:${fi_}, ease:"power2.inOut"}, ${r3(t.at)});\n`;
    fxJs += `  tl.to("#${id} .fill", {opacity:0, duration:${fo}, ease:"power2.inOut"}, ${r3(t.at + d - fo - 0.01)});\n`;
  } else if (t.type === "dip-cut") {
    const d = t.duration || T["dip-cut"].duration;
    fxHtml += `    <div id="${id}" class="clip fx" data-start="${r3(t.at - d)}" data-duration="${r3(d)}"><div class="fill" style="background:#000"></div></div>\n`;
    fxJs += `  tl.fromTo("#${id} .fill", {opacity:0}, {opacity:${T["dip-cut"].darken}, duration:${d}, ease:"power2.inOut"}, ${r3(t.at - d)});\n`;
  }
}
const fxCss = `  .fx{position:absolute;inset:0}\n  .fill{position:absolute;inset:0;opacity:0}`;

// ---------- root ----------
const cams = [...(plan.camera || [])].sort((a, b) => a.at - b.at);
if (!cams.length || cams[0].at > 0) cams.unshift({ at: 0, scale: 1, x: 0, y: 0 });
let camJs = "";
for (const c of cams) camJs += `  tl.set(["#cam-a","#cam-b"], {scale:${c.scale}, x:${c.x || 0}, y:${c.y || 0}}, ${r3(c.at)});\n`;

let brHtml = "", brJs = "", bi = 0;
for (const b of broll) {
  const id = `br${bi++}`, dur = r3(b.end - b.start);
  const isImg = /\.(jpe?g|png|webp)$/i.test(b.src);
  const media = isImg
    ? `<img id="${id}" class="clip media" src="${b.src}" data-start="${r3(b.start)}" data-duration="${dur}" alt="">`
    : `<video id="${id}" class="clip media" src="${b.src}" data-start="${r3(b.start)}" data-duration="${dur}" data-media-start="${b.mediaStart || 0}" muted playsinline></video>`;
  brHtml += `    <div id="${id}-w" class="frame" style="z-index:5">${media}</div>\n`;
  const mv = { "push-in": [1, 1.08, 0], "pull-out": [1.08, 1, 0], "drift-left": [1.06, 1.06, -40], "drift-right": [1.06, 1.06, 40] }[b.move || "none"];
  if (mv) brJs += `  tl.fromTo("#${id}-w", {scale:${mv[0]}, x:0}, {scale:${mv[1]}, x:${mv[2]}, duration:${dur}, ease:"sine.inOut"}, ${r3(b.start)});\n`;
}

let audioHtml = "";
const au = plan.audio || {};
if (au.music) audioHtml += `    <audio id="music" class="clip" src="${au.music.src}" data-start="0" data-duration="${D}" data-volume="${au.music.volume ?? 0.12}" data-fade-out="${au.music.fadeOut ?? 1.5}"></audio>\n`;
(au.sfx || []).forEach((s, i) => { audioHtml += `    <audio id="sfx${i}" class="clip" src="${s.src}" data-start="${r3(s.at)}" data-volume="${s.volume ?? 0.6}"></audio>\n`; });

const cut = plan.source.video ? plan.source.cutout : null;
// Không có video nguồn = chế độ overlay: nền trong suốt, render ra .mov/.webm để chồng lên video khác.
const BG = plan.source.video ? "#000" : "transparent";
const index = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script src="assets/gsap.min.js"></script>
<style>
  html,body{margin:0;background:${BG}}
  #main{position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${BG}}
  .frame{position:absolute;inset:0;transform-origin:50% 40%}
  .media{position:absolute;left:0;top:0;width:${W}px;height:${H}px;object-fit:cover}
  .host{position:absolute;inset:0}
</style>
</head>
<body>
  <div id="main" data-composition-id="main" data-start="0" data-duration="${D}" data-width="${W}" data-height="${H}">
    <div id="cam-a" class="frame" style="z-index:1">${plan.source.video ? `<video id="aroll" class="clip media" src="${plan.source.video}" data-start="0" data-duration="${D}" data-has-audio="true" data-volume="${plan.source.volume ?? 1}" playsinline></video>` : ""}</div>
    <div id="behind" class="host" data-composition-id="behind" data-composition-src="compositions/behind.html" data-start="0" data-duration="${D}" data-width="${W}" data-height="${H}" data-track-kind="graphics" style="z-index:2"></div>
    <div id="cam-b" class="frame" style="z-index:3">${cut ? `<video id="cutout" class="clip media" src="${cut}" data-start="0" data-duration="${D}" muted playsinline data-layout-allow-occlusion></video>` : ""}</div>
${brHtml}    <div id="fx" class="host" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="${D}" data-width="${W}" data-height="${H}" data-track-kind="graphics" style="z-index:8"></div>
    <div id="text" class="host" data-composition-id="text" data-composition-src="compositions/text.html" data-start="0" data-duration="${D}" data-width="${W}" data-height="${H}" data-track-kind="captions" style="z-index:7"></div>
${audioHtml}  </div>
  <script>
  const tl = gsap.timeline({ paused: true });
${camJs}${brJs}  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
  </script>
</body>
</html>
`;

fs.mkdirSync(path.join(proj, "compositions"), { recursive: true });
fs.writeFileSync(path.join(proj, "index.html"), index);
fs.writeFileSync(path.join(proj, "compositions", "text.html"), sceneFile("text", capHtml, capJs));
fs.writeFileSync(path.join(proj, "compositions", "behind.html"), sceneFile("behind", behindHtml, behindJs));
fs.writeFileSync(path.join(proj, "compositions", "fx.html"), sceneFile("fx", fxHtml, fxJs, fxCss));
// gsap local copy (CDN có thể bị chặn)
try {
  const req = createRequire(path.join(proj, "package.json"));
  fs.copyFileSync(path.join(path.dirname(req.resolve("gsap/package.json")), "dist", "gsap.min.js"), path.join(proj, "assets", "gsap.min.js"));
} catch { warn.push("không tìm thấy gsap trong node_modules: chạy setup.sh"); }

console.log(JSON.stringify({ ok: true, project: proj, captions: ci, emphasis: emph.length, broll: broll.length, fx: fi, warnings: warn }, null, 2));
