// Dùng: node build-hyperframes.mjs <spec.json>  -> engines/hyperframes/dist/
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from "node:fs";
import { buildSync } from "esbuild";
const spec = JSON.parse(readFileSync(process.argv[2], "utf8"));
const portrait = spec.platform !== "youtube"; // tiktok = 9:16, youtube = 16:9
const [W, H] = portrait ? [1080, 1920] : [1920, 1080];
const dir = new URL("../engines/hyperframes/", import.meta.url);
const tpl = spec.template || "cashflow-3d";
if (!/^[\w-]+$/.test(tpl)) throw new Error("Tên mẫu không hợp lệ: " + tpl);
const html = readFileSync(new URL(`templates/${tpl}.html`, dir), "utf8")
  .replaceAll("__RES__", portrait ? "portrait" : "landscape")
  .replaceAll("__W__", W).replaceAll("__H__", H).replaceAll("__DUR__", spec.duration)
  .replace("/*SPEC*/null", JSON.stringify(spec));
const out = new URL("dist/", dir);
mkdirSync(out, { recursive: true });
writeFileSync(new URL("index.html", out), html);
// Đóng gói thư viện cục bộ: render không phụ thuộc CDN/mạng.
copyFileSync(new URL("../../node_modules/gsap/dist/gsap.min.js", dir), new URL("gsap.min.js", out));
buildSync({ stdin: { contents: 'import * as T from "three"; window.THREE = T;', resolveDir: new URL("../../", dir).pathname },
  bundle: true, minify: true, format: "iife", outfile: new URL("three.global.js", out).pathname });
writeFileSync(new URL("package.json", out), '{"name":"hf-dist","private":true,"type":"module"}');
writeFileSync(new URL("hyperframes.json", out), JSON.stringify({
  $schema: "https://hyperframes.heygen.com/schema/hyperframes.json",
  registry: "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  paths: { blocks: "compositions", components: "compositions/components", assets: "assets" },
  media: { autoProxy: true },
}, null, 2));
