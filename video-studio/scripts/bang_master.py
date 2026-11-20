"""Trang Bảng master (Hào chốt 19/11): xem + chỉnh mọi thông số dựng trong cau-hinh/master.json.
- App studio mở /bang-master?t=<mã>&p=<dự án>: Lưu chung (ghi master.json) hoặc Lưu riêng dự án (ghi timeline meta.cau_hinh).
- Không có máy chủ (artifact trên điện thoại/Mac): chỉnh rồi bấm "Sao chép thay đổi", dán cho Claude áp.
Chạy trong video-studio:
  python scripts/bang_master.py --html <file.html>   trang tự chứa (bản đăng artifact)
  python scripts/bang_master.py --md                 ghi docs/04-thu-vien/BANG-MASTER.md (bảng đọc/in)"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cau_hinh

MD = os.path.join(HERE, "..", "..", "docs", "04-thu-vien", "BANG-MASTER.md")


def du_lieu():
    d = json.load(open(cau_hinh.FILE, encoding="utf8"))
    for g in d["nhom"]:
        for t in g["thong_so"]:
            t.setdefault("goc", t["mac_dinh"])  # giá trị gốc khi lập bảng (19/11): nút "về gốc"
            t["nguyen"] = cau_hinh.la_nguyen(t)  # JS không phân biệt 4 và 4.0: máy chủ báo sẵn ô nào cần số nguyên
    return d


CSS = """
:root{--bg:#f3f4f2;--panel:#fff;--fg:#1d2321;--muted:#5d6a66;--line:#d9dedb;--accent:#0f766e;--accent-soft:#d6efeb;--changed:#b45309;--changed-soft:#fdf0dc;--err:#b91c1c;
--f-ui:"Be Vietnam Pro",system-ui,sans-serif;--f-num:"JetBrains Mono",ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121615;--panel:#1a201e;--fg:#e4ebe8;--muted:#93a39e;--line:#2c3532;--accent:#4fd1c0;--accent-soft:#16332f;--changed:#f0a64a;--changed-soft:#3a2a12;--err:#f87171;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121615;--panel:#1a201e;--fg:#e4ebe8;--muted:#93a39e;--line:#2c3532;--accent:#4fd1c0;--accent-soft:#16332f;--changed:#f0a64a;--changed-soft:#3a2a12;--err:#f87171;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:14px/1.5 var(--f-ui);margin:0}
.wrap{max-width:980px;margin:0 auto;padding-block:20px 120px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1{font-size:22px;margin:0;text-wrap:balance}
.sub{color:var(--muted);margin:4px 0 14px;max-width:70ch}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
.bar input[type=search]{flex:1 1 220px;min-width:0;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg);font:inherit}
select,button,.bar input{font:inherit}
select{padding:7px 8px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg)}
.tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px;margin-bottom:10px}
.tab{flex:0 0 auto;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:5px 12px;cursor:pointer;white-space:nowrap}
.tab[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.tab .n{font-family:var(--f-num);font-size:11px;margin-left:4px;opacity:.75}
.tab .d{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--changed);margin-left:5px;vertical-align:middle}
.gr h2{font-size:16px;margin:18px 0 2px}
.gr .gd{color:var(--muted);margin:0 0 8px;max-width:75ch}
.row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,300px);gap:6px 18px;padding:12px 14px;background:var(--panel);border:1px solid var(--line);border-radius:8px;margin-bottom:8px}
.row.doi{border-color:var(--changed);background:linear-gradient(90deg,var(--changed-soft),var(--panel) 40%)}
.row .ten{font-weight:600}
.row .id{font-family:var(--f-num);font-size:11.5px;color:var(--muted);margin-left:6px}
.row .mt{color:var(--muted);font-size:13px;margin-top:3px;max-width:70ch}
.row .meta{font-family:var(--f-num);font-size:11.5px;color:var(--muted);margin-top:5px;display:flex;flex-wrap:wrap;gap:4px 12px}
.ctl{display:flex;flex-direction:column;gap:6px;justify-content:center;min-width:0}
.ctl .h{display:flex;gap:8px;align-items:center}
.ctl input[type=range]{flex:1;min-width:0;accent-color:var(--accent)}
.ctl input[type=number],.ctl input[type=text]{width:100%;min-width:0;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font-family:var(--f-num)}
.ctl input[type=number]{width:96px;flex:0 0 96px}
.ctl .dv{font-size:12px;color:var(--muted);white-space:nowrap}
.ctl .tag{font-size:12px;color:var(--changed);display:flex;gap:8px;align-items:center}
.lk{background:none;border:0;color:var(--accent);cursor:pointer;padding:0;text-decoration:underline;font-size:12px}
.err{color:var(--err);font-size:12px}
.sw{display:flex;gap:8px;align-items:center;cursor:pointer}
.sw input{width:18px;height:18px;accent-color:var(--accent)}
.foot{position:fixed;left:0;right:0;bottom:0;background:var(--panel);border-top:1px solid var(--line);
padding-top:10px;padding-bottom:calc(10px + env(safe-area-inset-bottom,0px));padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.foot .in{max-width:980px;margin:0 auto;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.foot .st{flex:1 1 200px;min-width:0;color:var(--muted)}
.btn{border:1px solid var(--accent);background:var(--accent);color:var(--bg);border-radius:6px;padding:8px 14px;cursor:pointer;font-weight:600}
.btn.ph{background:transparent;color:var(--accent)}
.btn:disabled{opacity:.45;cursor:default}
button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
textarea.out{width:100%;min-height:80px;margin-top:8px;font-family:var(--f-num);font-size:12px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);padding:8px}
@media (max-width:640px){.row{grid-template-columns:minmax(0,1fr)}}
"""

JS = r"""
const D = JSON.parse(document.getElementById("du-lieu").textContent);
const Q = new URLSearchParams(location.search), TOK = Q.get("t") || "", DA = Q.get("p") || "";
const APP = !!TOK;  // mở từ app studio (có mã khoá): lưu thẳng được; không thì chỉ sao chép
const T = {}; D.nhom.forEach(g => g.thong_so.forEach(t => (T[t.id] = t)));
let pham = DA ? "du-an" : "chung", ghiDe = {}, gt = {}, nap = {}, tab = D.nhom[0].id, tim = "";
const $ = s => document.querySelector(s);
const bang = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const chuan = id => pham === "chung" ? T[id].goc : T[id].mac_dinh;   // mốc so sánh: chung so với gốc, dự án so với bảng chung
function datLai() {
  gt = {}; for (const id in T) gt[id] = pham === "du-an" && id in ghiDe ? ghiDe[id] : T[id].mac_dinh;
  nap = JSON.parse(JSON.stringify(gt)); ve();
}
function loi(t, v) {
  if (t.kieu === "so") { if (typeof v !== "number" || isNaN(v)) return "cần số"; if (t.nguyen && !Number.isInteger(v)) return "cần số nguyên"; if (v < t.min || v > t.max) return `ngoài khoảng ${t.min}–${t.max}`; }
  if (t.kieu === "ds" && !v.length) return "cần ít nhất một mục";
  if (t.kieu === "chuoi" && !String(v).trim()) return "cần chữ";
  return "";
}
const e = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const khoa = t => pham === "du-an" && t.chi_chung;  // thông số chỉ chỉnh ở bảng chung (bản nhẹ, phân tích hình, agent)
const hien = v => Array.isArray(v) ? v.join(", ") : typeof v === "boolean" ? (v ? "bật" : "tắt") : String(v);
function o(t) {
  const v = gt[t.id], id = "c-" + t.id.replace(".", "-"), dis = khoa(t) ? " disabled" : "";
  if (t.kieu === "so") return `<div class="h"><input type="range" id="${id}-r" min="${t.min}" max="${t.max}" step="${t.buoc}" value="${v}" aria-label="${e(t.ten)}"${dis}>
    <input type="number" id="${id}" min="${t.min}" max="${t.max}" step="${t.buoc}" value="${v}" aria-label="${e(t.ten)}"${dis}><span class="dv">${t.don_vi || ""}</span></div>`;
  if (t.kieu === "bat") return `<label class="sw"><input type="checkbox" id="${id}" ${v ? "checked" : ""}${dis}> <span>${v ? "Bật" : "Tắt"}</span></label>`;
  if (t.kieu === "chon") return `<select id="${id}" aria-label="${e(t.ten)}"${dis}>${t.lua_chon.map(x => `<option ${x === v ? "selected" : ""}>${e(x)}</option>`).join("")}</select>`;
  return `<input type="text" id="${id}" value="${e(hien(v))}" aria-label="${e(t.ten)}"${dis}>`;
}
function dong(t) {
  const doi = !bang(gt[t.id], chuan(t.id)), sai = loi(t, gt[t.id]);
  const nhan = pham === "chung" ? `gốc ${hien(t.goc)}` : `bảng chung ${hien(t.mac_dinh)}`;
  return `<div class="row${doi ? " doi" : ""}" data-id="${t.id}"><div><span class="ten">${e(t.ten)}</span><span class="id">${t.id}</span>
    <div class="mt">${e(t.mo_ta)}</div><div class="meta">${khoa(t) ? "<span>chỉ chỉnh ở bảng chung</span>" : ""}<span>${e(nhan)}</span>${t.kieu === "so" ? `<span>khoảng ${t.min}–${t.max} ${t.don_vi || ""}</span>` : ""}<span>dùng ở ${t.dung_o}</span></div></div>
    <div class="ctl">${o(t)}${doi ? `<div class="tag">Khác ${pham === "chung" ? "gốc" : "bảng chung"} <button class="lk" data-ve="${t.id}">về ${pham === "chung" ? "gốc" : "bảng chung"}</button></div>` : ""}${sai ? `<div class="err">${sai}</div>` : ""}</div></div>`;
}
function ve() {
  const k = tim.trim().toLowerCase();
  const khop = t => !k || (t.ten + " " + t.id + " " + t.mo_ta).toLowerCase().includes(k);
  $("#tabs").innerHTML = D.nhom.map(g => `<button class="tab" role="tab" aria-selected="${!k && g.id === tab}" data-tab="${g.id}">${g.ten}<span class="n">${g.thong_so.length}</span>${g.thong_so.some(t => !bang(gt[t.id], chuan(t.id))) ? '<span class="d" title="có thông số đã đổi"></span>' : ""}</button>`).join("");
  $("#ds").innerHTML = D.nhom.filter(g => k || g.id === tab).map(g => {
    const ts = g.thong_so.filter(khop); if (!ts.length) return "";
    return `<section class="gr"><h2>${g.ten}</h2><p class="gd">${g.mo_ta || ""}</p>${ts.map(dong).join("")}</section>`;
  }).join("") || `<p class="sub">Không có thông số nào khớp “${tim}”.</p>`;
  trangThai();
}
function thayDoi() { return Object.keys(T).filter(id => !bang(gt[id], chuan(id))); }
function chuaLuu() { return Object.keys(T).filter(id => !bang(gt[id], nap[id])); }
function trangThai() {
  const d = thayDoi(), c = chuaLuu(), sai = Object.keys(T).some(id => loi(T[id], gt[id]));
  $("#st").textContent = `${d.length} thông số khác ${pham === "chung" ? "gốc" : "bảng chung"}` + (c.length ? ` · ${c.length} chưa lưu` : "") + (sai ? " · có giá trị sai" : "");
  $("#luu").hidden = !APP; $("#luu").disabled = !c.length || sai;
}
function doc(t, el) {
  if (t.kieu === "so") return parseFloat(el.value);
  if (t.kieu === "bat") return el.checked;
  if (t.kieu === "ds") return el.value.split(",").map(x => x.trim()).filter(Boolean);
  return el.value;
}
document.addEventListener("input", ev => {
  const r = ev.target.closest(".row"); if (!r) return;
  const t = T[r.dataset.id], el = ev.target; let v = doc(t, el);
  if (t.kieu === "so") { const khac = el.type === "range" ? r.querySelector("input[type=number]") : r.querySelector("input[type=range]"); khac.value = el.value; v = Math.round(v * 1e6) / 1e6; }
  gt[t.id] = v;
  if (t.kieu === "bat") el.nextElementSibling.textContent = v ? "Bật" : "Tắt";
  const doi = !bang(v, chuan(t.id)); r.classList.toggle("doi", doi); trangThai();
});
document.addEventListener("change", ev => { if (ev.target.closest(".row")) setTimeout(ve); });  // vẽ lại sau sự kiện blur/click đang chạy
document.addEventListener("click", ev => {
  const b = ev.target.closest("[data-tab],[data-ve]"); if (!b) return;
  if (b.dataset.tab) { tab = b.dataset.tab; tim = ""; $("#tim").value = ""; }
  else gt[b.dataset.ve] = JSON.parse(JSON.stringify(chuan(b.dataset.ve)));
  ve();
});
$("#tim").addEventListener("input", e => { tim = e.target.value; ve(); });
$("#pham").addEventListener("change", e => { pham = e.target.value; datLai(); });
function vanBan() {
  const d = thayDoi();
  const dau = pham === "chung" ? "Bảng master — đổi bảng chung:" : `Bảng master — ghi đè riêng dự án ${DA || "<tên dự án>"}:`;
  return d.length ? dau + "\n" + d.map(id => `${id} = ${Array.isArray(gt[id]) ? JSON.stringify(gt[id]) : gt[id]}`).join("; ") : dau + "\n(không đổi gì)";
}
$("#chep").addEventListener("click", async () => {
  const s = vanBan(), out = $("#ra"); out.hidden = false; out.value = s;
  try { await navigator.clipboard.writeText(s); $("#st").textContent = "Đã sao chép. Dán cho Claude để áp."; }
  catch { out.select(); $("#st").textContent = "Chưa sao chép tự động được: chọn sẵn ô bên dưới, bấm sao chép thủ công."; }
});
async function api(m, url, body) {
  const r = await fetch(url, { method: m, headers: { "X-Token": TOK, "Content-Type": "application/json" }, body: body && JSON.stringify(body) });
  const j = await r.json(); if (!r.ok) throw new Error((j.errors || [j.error]).join("; ")); return j;
}
$("#luu").addEventListener("click", async () => {
  try {
    if (pham === "chung") { const c = {}; chuaLuu().forEach(id => (c[id] = gt[id])); await api("PUT", "/api/cau-hinh", c); chuaLuu().forEach(id => (T[id].mac_dinh = gt[id])); }
    else { const g = {}; thayDoi().forEach(id => (g[id] = gt[id])); await api("PUT", `/api/p/${encodeURIComponent(DA)}/cau-hinh`, g); ghiDe = g; }
    nap = JSON.parse(JSON.stringify(gt)); ve();
    $("#st").textContent = pham === "chung" ? "Đã lưu bảng chung (bản cũ: master.json.bak)." : `Đã lưu riêng dự án ${DA} (bản cũ: timeline.json.bak).`;
  } catch (e) { $("#st").textContent = "Chưa lưu: " + e.message; }
});
(async () => {
  $("#pham").innerHTML = `<option value="chung">Bảng chung (mọi dự án)</option>` + (DA ? `<option value="du-an">Riêng dự án ${DA}</option>` : "");
  $("#pham").value = pham;
  if (APP) {
    try { const j = await api("GET", "/api/cau-hinh" + (DA ? "?p=" + encodeURIComponent(DA) : ""));
      j.nhom.forEach(g => g.thong_so.forEach(t => (T[t.id].mac_dinh = t.mac_dinh))); ghiDe = j.ghi_de || {}; }
    catch (e) { $("#st").textContent = "Không đọc được từ máy chủ: " + e.message; }
  } else $("#che-do").textContent = "Bản xem: chỉnh rồi bấm “Sao chép thay đổi” và dán cho Claude. Lưu thẳng chỉ có trong app studio (nút ⚙ Bảng master).";
  datLai();
})();
"""


def tao(day_du=False):
    """HTML trang bảng master. day_du: thêm <!doctype> + meta (máy chủ app gửi thẳng); artifact tự bọc khung nên không cần."""
    d = du_lieu()
    n = sum(len(g["thong_so"]) for g in d["nhom"])
    dl = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    dau = ('<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           if day_du else "")
    return f"""{dau}<title>Bảng master dựng</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600&family=JetBrains+Mono:wght@400&display=swap">
<style>{CSS}</style>{"</head><body>" if day_du else ""}
<div class="wrap">
<h1>Bảng master dựng</h1>
<p class="sub">{n} thông số của toàn bộ quy trình: cắt, nhận dạng giọng, phụ đề, chữ, thẻ, zoom, âm thanh, hình, vùng an toàn, kiểm bản cuối, agent. Ghi đè riêng dự án thắng bảng chung. <span id="che-do"></span></p>
<div class="bar"><input type="search" id="tim" placeholder="Tìm thông số (vd. lặng, zoom, LUFS, cỡ chữ)" aria-label="Tìm thông số">
<select id="pham" aria-label="Phạm vi"></select></div>
<div class="tabs" id="tabs" role="tablist"></div>
<div id="ds"></div>
</div>
<div class="foot"><div class="in"><span class="st" id="st"></span>
<button class="btn ph" id="chep">Sao chép thay đổi</button><button class="btn" id="luu" hidden>Lưu</button></div>
<div class="in"><textarea class="out" id="ra" hidden readonly aria-label="Thay đổi để dán cho Claude"></textarea></div></div>
<script type="application/json" id="du-lieu">{dl}</script>
<script>{JS}</script>{"</body></html>" if day_du else ""}"""


def md():
    d = du_lieu()
    out = ["# Bảng master dựng", "", "Sinh tự động từ `video-studio/cau-hinh/master.json` bằng `python scripts/bang_master.py --md`. Đừng sửa tay file này.", "",
           "- **Chỉnh:** app studio → ⚙ Bảng master (Lưu chung hoặc riêng dự án), hoặc bản xem artifact → \"Sao chép thay đổi\" → dán cho Claude, hoặc nói thẳng \"chỉnh X thành Y\".",
           "- **Thứ tự ưu tiên:** ghi đè riêng dự án (`timeline.json` → `meta.cau_hinh`) > bảng chung (`mac_dinh`).",
           "- **Kiểm:** giá trị ngoài khoảng hoặc id gõ nhầm bị chặn (`timeline.check`, máy chủ app, `cau_hinh.py --tu-kiem`).", ""]
    for g in d["nhom"]:
        out += [f"## {g['ten']} (`{g['id']}`)", "", g.get("mo_ta", ""), "", "| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |", "|---|---|---|---|---|---|---|"]
        for t in g["thong_so"]:
            v = lambda x: ", ".join(x) if isinstance(x, list) else ("bật" if x is True else "tắt" if x is False else str(x))
            kh = f"{t['min']}–{t['max']} {t.get('don_vi', '')}".strip() if t["kieu"] == "so" else ("/".join(map(str, t["lua_chon"])) if t["kieu"] == "chon" else "")
            out.append(f"| {t['ten']} | `{t['id']}` | {v(t['mac_dinh'])} | {v(t['goc'])} | {kh} | {t['dung_o']} | {t['mo_ta']} |".replace("\n", " "))
        out.append("")
    return "\n".join(out)


def _tu_kiem():
    h = tao()
    dl = h.split('id="du-lieu">')[1].split("</script>")[0]
    d = json.loads(dl.replace("<\\/", "</"))
    assert sum(len(g["thong_so"]) for g in d["nhom"]) == len(cau_hinh.bang())
    assert tao(True).startswith("<!doctype html>") and "</script>" not in dl
    assert md().count("| `") == len(cau_hinh.bang())
    print("OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--tu-kiem"]:
        _tu_kiem()
    elif a[:1] == ["--html"] and len(a) == 2:
        open(a[1], "w", encoding="utf8").write(tao())
        print("Đã ghi", a[1])
    elif a == ["--md"]:
        open(MD, "w", encoding="utf8").write(md() + "\n")
        print("Đã ghi", os.path.abspath(MD))
    else:
        sys.exit(__doc__)
