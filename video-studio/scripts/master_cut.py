"""Master cut: tự cắt khoảng lặng, bỏ câu nói hỏng, chấm điểm khung hình, gợi ý nhịp; ghi timeline mới + báo cáo.
Chạy trong video-studio:  python3 scripts/master_cut.py projects/<tên> [--chi-phan-tich]
- Đoạn có lời nói: giữ phần nói, cắt im lặng (cuối câu chừa nghỉ dài hơn giữa câu), bỏ tiếng đệm "ờ, à, ừm",
  bỏ lần nói vấp trước khi nói lại; mỗi chỗ cắt nhảy xen kẽ phóng 100% / 108% cho đỡ giật.
- Đoạn không lời (flycam, cảnh) và cảnh trám: dời về khúc đẹp nhất cùng độ dài.
- Chữ, minh hoạ, zoom, cảnh trám dời theo; phụ đề tự sinh tạo lại.
Báo cáo: projects/<tên>/build/master-cut.md. Bản cũ: timeline.json.bak (app: Lịch sử)."""
import difflib, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timeline import check, layout
import phan_tich_hinh as pth

FILLERS = {"ờ", "ơ", "à", "ừ", "ừm", "ừa", "hmm", "um", "uh", "ầy"}
CUT_GAP = 0.30          # im lặng dài hơn thì cắt
PAD_IN, PAD_OUT = 0.08, 0.14   # chừa trước khi nói / sau khi dứt lời (giữa câu)
PAD_END = 0.30          # chừa sau cuối câu (dấu chấm, hỏi…) cho có nhịp nghỉ
MIN_PIECE = 0.35        # mẩu ngắn hơn thì bỏ (trừ khi có chữ)
PUNCH = 1.05            # phóng xen kẽ ở các chỗ cắt nhảy (Hào: tối đa 104–106%; dung.py đẩy vào êm)
BEAT = 4.0              # mẩu nói dài: đổi cỡ khung khoảng mỗi 4 giây, ở chỗ ngắt giữa hai từ

norm = lambda w: re.sub(r"[^\w]", "", w.lower())


def nang_luong(path, cache):
    """Âm lượng (dB) từng khung 20ms của tiếng trong file: dùng để biết chỗ nào im thật."""
    if os.path.exists(cache):
        return json.load(open(cache))
    import subprocess
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    n = len(x) // 320
    db = (10 * np.log10((x[:n * 320].reshape(n, 320) ** 2).mean(axis=1) + 1e-10)).round(1).tolist() if n else []
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    json.dump(db, open(cache, "w"))
    return db


def nguong(db):
    """Ngưỡng tiếng nói: nền ồn (mức thấp 20%) + 10 dB, nhưng không cao quá mức to 90% − 6 dB."""
    if not db:
        return -40.0
    d = sorted(db)
    return min(d[len(d) // 5] + 10, d[len(d) * 9 // 10] - 6)


def im(db, thr, a, b):
    """Tỉ lệ khung im (dưới ngưỡng) trong [a, b] giây."""
    fr = db[int(a * 50):max(int(a * 50) + 1, int(b * 50))]
    return sum(v < thr for v in fr) / len(fr) if fr else 1.0


def lam_on_tu(words, db, thr):
    """Từ kéo dài (>0,6s) thường nuốt cả khoảng ngập ngừng phía trước: dời điểm bắt đầu tới lúc tiếng thật sự to lên."""
    out = []
    for w, s, e in words:
        if e - s > 0.6 and db:
            on = next((k / 50 for k in range(int(s * 50), int(e * 50)) if k < len(db) and db[k] >= thr), None)
            s = max(s, on - 0.05) if on is not None else e - 0.45
        out.append([w, s, e])
    return out


def kep_tu(words):
    """Whisper hay kéo dài từ đứng sau khoảng ngập ngừng: từ dài hơn 0,8s thì coi như bắt đầu 0,45s trước khi dứt."""
    return [[w, s if e - s <= 0.8 else e - 0.45, e] for w, s, e in words]


def bo_noi_lai(words):
    """Bỏ lần nói vấp: cụm ≥3 từ lặp lại trong 15 giây, có ngập ngừng trước lần sau → giữ lần sau. Trả (từ còn lại, phần bỏ)."""
    words, dropped = list(words), []
    changed = True
    while changed:
        changed = False
        n = [norm(w[0]) for w in words]
        for j in range(3, len(words) - 2):
            for i in range(j - 3, -1, -1):  # lần nói trước GẦN NHẤT: cụm chung chung ("đây là không") lặp xa không phải nói lại
                if words[j][1] - words[i][1] > 15:
                    break
                if n[i:i + 3] != n[j:j + 3]:
                    continue
                k = 0
                while i - k - 1 >= 0 and n[i - k - 1] == n[j - k - 1] and j - k - 1 > i:
                    k += 1
                i0, j0 = i - k, j - k
                if any(re.search(r"[.?!]$", w[0]) for w in words[i0:j0 - 1]):  # có câu đã nói trọn bên trong: không phải lần nói hỏng
                    continue
                pause = words[j0][1] - words[j0 - 1][2] + max(0, (words[j0][2] - words[j0][1]) - 0.6)
                if pause < 0.4:  # nói liền mạch ("căn tứ lập, 4 căn tứ lập") không phải nói lại
                    continue
                dropped.append((words[i0][1], words[j0 - 1][2], " ".join(w[0] for w in words[i0:j0])))
                words = words[:i0] + words[j0:]
                changed = True
                break
            if changed:
                break
    return words, dropped


def doan_noi(words, a, b, quiet=lambda x, y: True):
    """Từ (đã lọc) trong [a, b] của file → các mẩu giữ lại [(vào, ra, câu)] theo giờ trong file.
    quiet(x, y): khoảng [x, y] có thật sự im không (đo âm lượng); không im thì không cắt."""
    ws = [w for w in words if a <= (w[1] + w[2]) / 2 < b and norm(w[0]) not in FILLERS]
    groups = []
    for w in ws:
        if groups and (w[1] - groups[-1][-1][2] <= CUT_GAP or not quiet(groups[-1][-1][2], w[1])):
            groups[-1].append(w)
        else:
            groups.append([w])
    out = []
    for g in groups:
        end_pad = PAD_END if re.search(r"[.?!]$", g[-1][0]) or g is groups[-1] else PAD_OUT
        s, e = max(a, g[0][1] - PAD_IN), min(b, g[-1][2] + end_pad)
        if out and s < out[-1][1]:  # chừa đệm chồng lên mẩu trước thì nối liền
            out[-1] = (out[-1][0], e, out[-1][2] + " " + " ".join(w[0] for w in g))
        else:
            out.append((s, e, " ".join(w[0] for w in g)))
    return [x for x in out if x[1] - x[0] >= MIN_PIECE or x[2]]


def nhip_phong(pieces, words):
    """Các mốc (giờ trong file) để đổi cỡ khung: đầu mỗi mẩu + chỗ ngắt giữa hai từ gần mỗi 4 giây trong mẩu dài."""
    beats = []
    for s, e, _ in pieces:
        beats.append(s)
        gaps = [(w1[2] + w2[1]) / 2 for w1, w2 in zip(words, words[1:]) if s + 1.5 < w2[1] < e - 1.5]
        t = s + BEAT
        while t < e - 1.5 and gaps:
            g = min(gaps, key=lambda x: abs(x - t))
            if g > beats[-1] + 1.5:
                beats.append(g)
            t = max(t, g) + BEAT
    return beats


def doi_gio(old_tl, new_tl, origin):
    """Hàm đổi giờ cũ → giờ mới. origin[j] = chỉ số đoạn cũ sinh ra đoạn mới j."""
    L0, L1 = layout(old_tl), layout(new_tl)

    def f(t):
        i = max([k for k, s in enumerate(L0["starts"]) if t >= s - 1e-9] or [0])
        c = old_tl["clips"][i]
        end_i = L0["starts"][i] + c["dur"]
        if t >= end_i and i < len(L0["transitions"]):  # đang ở chuyển cảnh sau đoạn i
            last = max(j for j, o in enumerate(origin) if o == i)
            return L1["starts"][last] + new_tl["clips"][last]["dur"] + (t - end_i)
        ft = c["in"] + (t - L0["starts"][i])
        mine = [j for j, o in enumerate(origin) if o == i]
        for j in mine:
            n = new_tl["clips"][j]
            if n["in"] - 1e-6 <= ft < n["in"] + n["dur"]:
                return L1["starts"][j] + ft - n["in"]
        nxt = [j for j in mine if new_tl["clips"][j]["in"] > ft] or [j for j, o in enumerate(origin) if o > i]
        return L1["starts"][nxt[0]] if nxt else L1["total"]
    return f


def cua_so_dep(fs, a, dur, talking):
    """Khúc đẹp nhất dài `dur` giây trong file (điểm trung bình cao nhất). Trả (vào, điểm, điểm khúc hiện tại)."""
    sc = [pth.diem(f, talking)[0] for f in fs]
    n = max(1, int(round(dur * pth.FPS_A)))
    if len(sc) <= n:
        return a, sum(sc) / max(1, len(sc)), sum(sc) / max(1, len(sc))
    pre = [0.0]
    for x in sc:
        pre.append(pre[-1] + x)
    avg = lambda k: (pre[k + n] - pre[k]) / n
    best = max(range(len(sc) - n + 1), key=avg)
    cur = min(len(sc) - n, int(round(a * pth.FPS_A)))
    return best / pth.FPS_A, avg(best), avg(cur)


def tom_tat_khuc(fs, a, b, talking):
    sec = [f for f in fs if a <= f["t"] < b] or fs[:1]
    sc = [pth.diem(f, talking) for f in sec]
    why = {}
    for _, ws in sc:
        for w in ws:
            why[w] = why.get(w, 0) + 1
    return sum(x for x, _ in sc) / len(sc), [w for w, c in sorted(why.items(), key=lambda x: -x[1]) if c >= len(sc) * 0.3]


def nhip(words_per_sec, score):
    if words_per_sec is not None:
        if words_per_sec > 4.2:
            return "nói nhanh: giữ nguyên, không cắt thêm"
        if words_per_sec < 2.3:
            return "nói chậm: đã cắt sát chỗ nghỉ; cân nhắc phóng nhẹ hoặc chèn cảnh trám"
        return "nhịp vừa"
    if score >= 82:
        return "cảnh đẹp, mượt: giữ lâu 2,5–4 giây"
    if score >= 65:
        return "cảnh ổn: 1–2 giây"
    return "cảnh yếu: lướt dưới 1 giây hoặc bỏ"


def main(proj, only_report=False):
    p = os.path.join(proj, "timeline.json")
    tl = json.load(open(p, encoding="utf8"))
    if (errs := check(tl)):
        sys.exit("timeline.json chưa hợp lệ:\n- " + "\n- ".join(errs))
    import phu_de
    B = os.path.join(proj, "build")
    rep = [f"# Báo cáo master cut: {os.path.basename(proj)}", ""]
    L0 = layout(tl)
    new_clips, new_trs, origin, zooms, cover = [], [], [], [], []
    for i, c in enumerate(tl["clips"]):
        raw = os.path.join(B, "raw", c["file"])
        if not os.path.exists(raw):
            sys.exit(f"Chưa có footage {c['file']} (mở dự án trong app hoặc dựng nháp một lần để tải)")
        print(f"Phân tích đoạn {i + 1}: {c['file']}", flush=True)
        fs = pth.phan_tich(raw, os.path.join(B, "analysis", c["file"] + ".json"))
        db = nang_luong(raw, os.path.join(B, "analysis", c["file"] + ".db.json"))
        thr = nguong(db)
        tv = tl.get("meta", {}).get("tu_vung")
        words = lam_on_tu(phu_de.sua_tu(phu_de.nhan_dang(raw, phu_de.file_dem(B, c["file"], tv), tv), tl.get("meta", {}).get("sua_tu")), db, thr)
        a, b = c["in"], c["in"] + c["dur"]
        spoken = [w for w in words if a <= (w[1] + w[2]) / 2 < b]
        talking = bool(spoken) or sum(f["face"] > 0.02 for f in fs) > len(fs) * 0.4
        rep.append(f"## Đoạn {i + 1}: {c['file']} ({a:.1f}–{b:.1f}s, {c['dur']:.1f}s)")
        if spoken:
            kept_words, dropped = bo_noi_lai(words)
            pieces = doan_noi(kept_words, a, b, lambda x, y: im(db, thr, x, y) >= 0.7)
            for s, e, txt in dropped:
                if a <= s < b:
                    rep.append(f"- Bỏ lần nói vấp {s:.1f}–{e:.1f}s: “{txt}”")
            fill = [w[0] for w in spoken if norm(w[0]) in FILLERS]
            if fill:
                rep.append(f"- Bỏ tiếng đệm: {', '.join(fill)}")
            kept = sum(e - s for s, e, _ in pieces)
            rep.append(f"- Giữ {len(pieces)} mẩu nói, {kept:.1f}s / {c['dur']:.1f}s (cắt {c['dur'] - kept:.1f}s im lặng và nói vấp)")
            beats = nhip_phong(pieces, kept_words)
            for k, (s, e, txt) in enumerate(pieces):
                sc, why = tom_tat_khuc(fs, s, e, True)
                wps = len(txt.split()) / max(0.1, e - s)
                pace = f"{wps:.1f} từ/giây · {nhip(wps, sc)}" if e - s >= 2 else "mẩu ngắn"
                rep.append(f"  - {s:.1f}–{e:.1f}s điểm hình {sc:.0f} {('(' + ', '.join(why) + ')') if why else ''} · {pace}: “{txt}”")
                if sc < 50:
                    cover.append((len(new_clips), why))
                nc = dict(c, **{"in": round(s, 2), "dur": round(e - s, 2)})
                if k:
                    new_trs.append({"type": "cut"})
                new_clips.append(nc); origin.append(i)
                zooms.append((len(new_clips) - 1, [b for b in beats if s <= b < e] + [e]))
            if not pieces:
                rep.append("- Không còn lời nói sau khi lọc: giữ nguyên đoạn")
                new_clips.append(dict(c)); origin.append(i)
        else:
            best, bsc, csc = cua_so_dep(fs, a, c["dur"], talking)
            sc, why = tom_tat_khuc(fs, a, b, talking)
            rep.append(f"- Không có lời nói. Điểm hình hiện tại {csc:.0f} {('(' + ', '.join(why) + ')') if why else ''} · {nhip(None, sc)}")
            nc = dict(c)
            cap = 4.0 if sc >= 82 else 2.0 if sc >= 65 else 1.0  # nhịp: cảnh đẹp giữ lâu, cảnh yếu lướt nhanh
            if c["dur"] > cap:
                nc["dur"] = cap
                best, bsc, csc = cua_so_dep(fs, a, cap, talking)
                rep.append(f"- Rút còn {cap:.0f}s theo nhịp")
            if bsc - csc >= 5 and abs(best - a) > 0.3:
                nc["in"] = round(best, 2)
                rep.append(f"- Dời sang khúc đẹp nhất: {best:.1f}s (điểm {csc:.0f} → {bsc:.0f})")
            new_clips.append(nc); origin.append(i)
        if i < len(tl["transitions"]):
            new_trs.append(dict(tl["transitions"][i]))
        rep.append("")
    new = dict(tl, clips=new_clips, transitions=new_trs)
    f = doi_gio(tl, new, origin)
    L1 = layout(new)
    for key in ("texts", "subtitles", "cards", "zooms", "broll"):
        out = []
        for x in tl.get(key, []):
            if key == "subtitles" and x.get("auto"):
                continue  # tạo lại từ giọng nói bên dưới
            if key == "zooms" and x.get("auto"):
                continue
            s, e = f(x["start"]), f(x["start"] + x["dur"])
            # mục nằm trọn trong phần bị cắt thì giữ độ dài cũ (đặt vào đầu mẩu kế), không để co lại
            y = dict(x, start=round(s, 2), dur=round(e - s if e - s >= 0.6 * x["dur"] else x["dur"], 2))
            y["dur"] = round(min(y["dur"], L1["total"] - y["start"]), 2)
            if y["dur"] >= 0.2:
                out.append(y)
        new[key] = out
    nz, flip = 0, False
    for j, bs in zooms:  # phóng xen kẽ theo nhịp, đánh dấu tự sinh để chạy lại không nhân đôi
        for b0, b1 in zip(bs, bs[1:]):
            if flip:
                st = L1["starts"][j] + b0 - new_clips[j]["in"]
                new["zooms"].append({"start": round(st, 2), "dur": round(b1 - b0, 2), "scale": PUNCH, "auto": True}); nz += 1
            flip = not flip
    new["zooms"].sort(key=lambda x: x["start"])
    for k, x in enumerate(new.get("broll", [])):
        raw = os.path.join(B, "raw", x["file"])
        if os.path.exists(raw):
            fs = pth.phan_tich(raw, os.path.join(B, "analysis", x["file"] + ".json"))
            best, bsc, csc = cua_so_dep(fs, x["in"], x["dur"], False)
            if bsc - csc >= 5 and abs(best - x["in"]) > 0.3:
                rep.append(f"- Cảnh trám {k + 1} ({x['file']}): dời {x['in']:.1f}s → {best:.1f}s (điểm {csc:.0f} → {bsc:.0f})")
                x["in"] = round(best, 2)
    for j, why in cover:
        rep.append(f"- Gợi ý: phủ cảnh trám lên mẩu ở {L1['starts'][j]:.1f}s (hình yếu: {', '.join(why) or 'điểm thấp'})")
    rep.insert(2, f"**Trước:** {L0['total']:.1f}s, {len(tl['clips'])} đoạn · **Sau:** {L1['total']:.1f}s, {len(new_clips)} đoạn "
                  f"(ngắn hơn {L0['total'] - L1['total']:.1f}s). Đã thêm {nz} chỗ phóng xen kẽ (đổi cỡ khung khoảng mỗi {BEAT:.0f} giây).\n")
    os.makedirs(B, exist_ok=True)
    open(os.path.join(B, "master-cut.md"), "w", encoding="utf8").write("\n".join(rep) + "\n")
    if only_report:
        print("\n".join(rep)); return
    new.pop("_", None)
    if (errs := check(new)):
        sys.exit("Timeline sau khi cắt chưa hợp lệ (chưa ghi):\n- " + "\n- ".join(errs))
    shutil.copy(p, p + ".bak")
    tmp = p + ".tmp"
    json.dump(new, open(tmp, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    if any(x.get("auto") for x in tl.get("subtitles", [])) or tl.get("audio", {}).get("voice"):
        phu_de.main(proj)
    print(f"Xong master cut: {L0['total']:.1f}s → {L1['total']:.1f}s, {len(new_clips)} đoạn. Báo cáo: build/master-cut.md")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit("Dùng: python3 scripts/master_cut.py projects/<tên> [--chi-phan-tich]")
    main(os.path.abspath(args[0]), "--chi-phan-tich" in sys.argv)
