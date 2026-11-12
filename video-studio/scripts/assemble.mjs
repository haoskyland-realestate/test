// Dùng: node scripts/assemble.mjs projects/<tên>/edl.json
// Cắt các cảnh flycam theo EDL (danh sách cắt), cắt khung dọc 9:16, ghép giọng thu, logo, phụ đề -> out/<tên>.mp4
import { readFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { spawnSync } from "node:child_process";

const edlPath = resolve(process.argv[2] ?? "");
if (!existsSync(edlPath)) { console.error("Thiếu file EDL: " + process.argv[2]); process.exit(1); }
const edl = JSON.parse(readFileSync(edlPath, "utf8"));
const dir = dirname(edlPath);
const name = basename(dir);
const [W, H] = edl.platform === "youtube" ? [1920, 1080] : [1080, 1920];
const abs = (p) => resolve(dir, p);
const need = (p, what) => { if (!existsSync(abs(p))) { console.error(`Không thấy ${what}: ${p}`); process.exit(1); } };

if (!edl.scenes?.length) { console.error("EDL chưa có cảnh nào"); process.exit(1); }
const args = ["-y", "-loglevel", "error"];
const filters = [];
let total = 0;
edl.scenes.forEach((s, i) => {
  if (s.image) {
    need(s.image, "ảnh");
    args.push("-loop", "1", "-t", String(s.dur), "-i", abs(s.image));
    total += s.dur;
  } else {
    need(s.clip, "clip");
    if (!(s.out > s.in)) { console.error(`Cảnh ${i + 1}: "out" phải lớn hơn "in"`); process.exit(1); }
    args.push("-ss", String(s.in), "-t", String(s.out - s.in), "-i", abs(s.clip));
    total += s.out - s.in;
  }
  // focus -1..1: dịch khung cắt dọc sang trái/phải khi flycam là khung ngang.
  const fx = ((s.focus ?? 0) + 1) / 2;
  filters.push(`[${i}:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H}:(iw-${W})*${fx}:(ih-${H})/2,fps=30,setsar=1,format=yuv420p[v${i}]`);
});
const n = edl.scenes.length;
filters.push(`${edl.scenes.map((_, i) => `[v${i}]`).join("")}concat=n=${n}:v=1:a=0[base]`);

let last = "base", idx = n;
if (edl.logo) {
  need(edl.logo, "logo"); args.push("-i", abs(edl.logo));
  filters.push(`[${idx}:v]scale=${Math.round(W * 0.2)}:-1[lg]`, `[${last}][lg]overlay=W-w-40:60[withlogo]`);
  last = "withlogo"; idx++;
}
if (edl.captions) {
  need(edl.captions, "file phụ đề");
  // Fontsize/MarginV tính theo thang cao 288 của libass (không phải pixel): 12 ≈ 80px, 45 ≈ 300px trên khung 1920.
  filters.push(`[${last}]subtitles=${edl.captions}:force_style='Fontsize=12,Alignment=2,MarginV=45,Outline=1,Bold=1'[vout]`);
} else filters.push(`[${last}]null[vout]`);

need(edl.voice, "giọng thu"); args.push("-i", abs(edl.voice));
const voiceIdx = idx++;
let audio = `[${voiceIdx}:a]anull[aout]`;
if (edl.music) {
  need(edl.music, "nhạc nền"); args.push("-stream_loop", "-1", "-i", abs(edl.music));
  audio = `[${voiceIdx}:a]anull[va];[${idx}:a]volume=${edl.musicVolume ?? 0.1}[ma];[va][ma]amix=inputs=2:duration=first:normalize=0[aout]`;
}
filters.push(audio);

const probe = spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", abs(edl.voice)], { encoding: "utf8" });
const voiceDur = parseFloat(probe.stdout);
if (Math.abs(voiceDur - total) > 1) console.warn(`CẢNH BÁO: tổng cảnh ${total.toFixed(1)}s, giọng thu ${voiceDur.toFixed(1)}s. Nên chỉnh EDL cho khớp.`);

mkdirSync(resolve(dir, "../../out"), { recursive: true });
const out = resolve(dir, `../../out/${name}.mp4`);
args.push("-filter_complex", filters.join(";"), "-map", "[vout]", "-map", "[aout]",
  "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "-shortest", out);
// cwd = thư mục dự án để đường dẫn phụ đề trong bộ lọc là đường dẫn tương đối.
const r = spawnSync("ffmpeg", args, { cwd: dir, stdio: "inherit" });
if (r.status !== 0) process.exit(r.status ?? 1);
console.log(`Xong: out/${name}.mp4 (cảnh ${total.toFixed(1)}s, giọng ${voiceDur.toFixed(1)}s)`);
