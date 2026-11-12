// Kiểm từng chuyển cảnh trong scripts/gl_transitions.json bằng Chrome thật (WebGL): biên dịch được,
// đầu chuyển cảnh (progress 0) là cảnh trước, cuối (progress 1) là cảnh sau. Hiệu ứng không đạt bị loại khỏi danh mục.
// Chạy: node scripts/kiem_gl.mjs   (cần Playwright; chỉ chạy khi cập nhật thư viện)
import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const dir = new URL(".", import.meta.url);
const libPath = new URL("gl_transitions.json", dir);
const lib = JSON.parse(readFileSync(libPath, "utf8"));
const b = await chromium.launch();
const p = await b.newPage();
await p.setContent("<canvas id=c width=90 height=160></canvas>");
await p.addScriptTag({ content: readFileSync(new URL("gl_runtime.js", dir), "utf8") });
const res = await p.evaluate((lib) => {
  const mk = (col) => { const c = document.createElement("canvas"); c.width = 90; c.height = 160; const g = c.getContext("2d"); g.fillStyle = col; g.fillRect(0, 0, 90, 160); return c; };
  const A = mk("rgb(255,0,0)"), B = mk("rgb(0,0,255)");
  const cv = document.getElementById("c"), r = glT(cv, lib), gl = cv.getContext("webgl"), px = new Uint8Array(4);
  const at = (name, t) => { r.draw(name, A, B, t); gl.readPixels(45, 80, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); return [...px]; };
  const out = {};
  for (const name of Object.keys(lib)) {
    try {
      const s = at(name, 0), e = at(name, 1);
      out[name] = s[0] > 200 && s[2] < 60 && e[2] > 200 && e[0] < 60 ? "ok" : `sai màu đầu/cuối ${s} → ${e}`;
    } catch (err) { out[name] = "lỗi: " + String(err.message || err).slice(0, 80); }
  }
  return out;
}, lib);
await b.close();
const bad = Object.entries(res).filter(([, v]) => v !== "ok");
for (const [k, v] of bad) { console.log("loại", k, "-", v); delete lib[k]; }
writeFileSync(libPath, JSON.stringify(lib));
console.log(`Đạt ${Object.keys(lib).length}, loại ${bad.length}`);
