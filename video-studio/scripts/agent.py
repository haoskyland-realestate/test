"""Agent video (gộp AutoEdit + bộ dựng Cloud Edit, Hào duyệt 18/11): MỘT lệnh tự chạy mọi bước máy móc, dừng ở các cổng cần người,
không đoán. Chạy lại cùng lệnh là làm tiếp từ bước dở. Trạng thái: projects/<tên>/AGENT.json; câu hỏi cho Hào: projects/<tên>/CAN-HOI.md.

Chạy trong video-studio (PC: .venv\\Scripts\\python.exe):
  python scripts/agent.py <tên> [nguồn …] [--preset A|B|C] [--mau <mẫu edit>]   tạo dự án (nguồn: thư mục, file, link) hoặc làm tiếp
      thêm (quy trình chuẩn 27/11, docs/02-quy-trinh/QUY-TRINH-CHUAN.md):
      --kich-ban <link Google Doc | file>   kịch bản → KICH-BAN.md, tự xếp clip lộn xộn theo kịch bản (xep_canh.py)
      --tai-nguyen <link Drive> [--du-an <tên ngắn, vd can-gio>]   ảnh/video dự án vào kho → tự trám cảnh (tram_canh.py)
      --ca-hai                              xong bản TikTok thì dựng thêm bản YouTube 16:9
  python scripts/agent.py <tên> --qua 1        Hào đã trả lời câu hỏi lời nói (đã ghi sửa từ/cắt đoạn)
  python scripts/agent.py <tên> --chon "<kết quả trang chọn hiệu ứng>"   hoặc  --chon "làm hết"
  python scripts/agent.py <tên> --qua 3        Hào "chốt phương án" storyboard
  python scripts/agent.py <tên> --qua 4        Hào duyệt bản xem 540×960 → dựng bản cuối
  python scripts/agent.py <tên> --trang-thai   xem đang ở bước nào

Các bước: 1 nguồn + bản nhẹ (+ kịch bản → xếp clip theo kịch bản, + tài nguyên dự án vào kho) → 2 master cut → 3 ghép giọng + nhận dạng → CỔNG 1 (từ máy nghe không chắc, tên, số, lặp/vấp/cắt nghi ngờ)
→ 4 CLAUDE chia cảnh + vai chữ (BAN-DUNG.json) → 5 trang chọn hiệu ứng → CỔNG 2 (Hào chọn) → CLAUDE đặt vai cho hiệu ứng đã chọn
→ 6 trám cảnh từ kho + đo màu (LUT) + storyboard/kế hoạch dựng → CỔNG 3 (chốt; chốt thì áp LUT) → 7 khung hình + mẫu + bản xem 540×960 có vạch vùng an toàn → CỔNG 4 (duyệt)
→ 8 bản cuối: đối chiếu chữ/số, vùng an toàn, dựng, kiểm bản dựng → ảnh bìa 3 phương án (+ bản YouTube nếu --ca-hai).
Mã thoát: 0 xong · 10 chờ Hào · 20 chờ Claude (đọc lời nói, viết/sửa BAN-DUNG.json) · 1 lỗi."""
import base64, glob, hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "studio"))
AE = os.path.join(ROOT, "autoedit")
PRESET = {"A": "xanh_gradient", "B": "cam_kem", "C": "neon_toi"}
from cau_hinh import lay
CHO_HAO, CHO_CLAUDE = 10, 20
PY = sys.executable


def doc(p, mac_dinh=None):
    return json.load(open(p, encoding="utf8")) if os.path.exists(p) else mac_dinh


def ghi(p, d):
    with open(p, "w", encoding="utf8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)


def chay(*cmd):
    t = time.time()
    r = subprocess.run([PY, *cmd], cwd=ROOT)
    print(f"⏱ {os.path.basename(cmd[0])}: {time.time() - t:.0f}s", flush=True)
    if r.returncode not in (0, 2):  # doi_chieu thoát 2 khi còn câu hỏi: agent tự xử lý
        sys.exit(f"Bước {os.path.basename(cmd[0])} lỗi (mã {r.returncode}). Đọc lỗi ở trên; sửa xong chạy lại agent.")
    return r.returncode


def dung_lai(st, pj, ma, tin_nhan):
    st["cho"] = tin_nhan
    ghi(os.path.join(pj, "AGENT.json"), st)
    print("\n" + "=" * 60 + "\n" + tin_nhan + "\n" + "=" * 60)
    sys.exit(ma)


# ---------- cổng 1: những gì máy không chắc ----------
def cau_hoi_loi(pj, tl, ws, tin):
    """Bảng hỏi Hào: từ nghe không chắc, tên riêng, số; và gợi ý cắt (lặp, vấp, cắt giữa lời) của phan_tich_loi."""
    m = tl.get("meta", {})
    da = {re.sub(r"[^\w%]", "", t).lower() for x in m.get("tu_vung", []) + [str(q) for q in m.get("da_duyet", [])] for t in x.split()}
    dong, gom = [], {}  # mỗi từ hỏi một lần: lần đầu + số lần xuất hiện
    for i, w in enumerate(ws):
        ly = []
        if i < len(tin) and tin[i] < lay("giong.nguong_tin", tl):
            ly.append(f"máy nghe không chắc ({tin[i]:.0%})")
        if re.search(r"\d", w[0]):
            ly.append("con số")
        elif i and w[0][:1].isupper() and not re.search(r"[.?!]$", ws[i - 1][0]):
            ly.append("tên riêng?")
        k = re.sub(r"[^\w%]", "", w[0]).lower()
        if ly and k not in da:
            if k in gom:
                gom[k][1] += 1; continue
            gom[k] = [len(dong), 1]
            dong.append([w[1], w[0], ", ".join(ly), " ".join(x[0] for x in ws[max(0, i - 4):i + 5])])
    dong = [f"| {t:.1f} | **{x}**{f' (×{gom[re.sub(r'[^\w%]', '', x).lower()][1]})' if gom[re.sub(r'[^\w%]', '', x).lower()][1] > 1 else ''} | {ly} | …{ngu}… |"
            for t, x, ly, ngu in dong]
    from phan_tich_loi import phan_tich
    goi_y = [g for g in phan_tich(tl, ws, pj) if g[1] in ("lặp từ", "nói vấp") or "CẮT TIẾNG" in g[2]]  # cảnh dài/ngắn để storyboard, không phải câu hỏi cắt
    return dong, goi_y


# ---------- trang chọn hiệu ứng và storyboard của AutoEdit (một file, ảnh nhúng sẵn: mở được trên điện thoại/Mac) ----------
def trang(mau, du_lieu, preset, ra):
    html = open(os.path.join(AE, "effects", mau), encoding="utf8").read()
    du_lieu = {**du_lieu, "preset": preset, "base": "ANH"}
    html = re.sub(r"/\*DATA\*/.*?/\*END\*/", lambda m: "/*DATA*/" + json.dumps(du_lieu, ensure_ascii=False) + "/*END*/", html, flags=re.S)
    anh = {f"{os.path.basename(os.path.dirname(f))}/{os.path.basename(f)[:-4]}": "data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode()
           for f in glob.glob(os.path.join(AE, "effects", "thumbs", "*", "*.jpg"))}
    vá = ("<script>(function(){var A=" + json.dumps(anh) + ";function f(i){var m=(i.getAttribute('src')||'').match(/^ANH\\/(.+)\\.jpg$/);"
          "if(m&&A[m[1]])i.src=A[m[1]]}new MutationObserver(function(){document.querySelectorAll('img').forEach(f)})"
          ".observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['src']});"
          "document.querySelectorAll('img').forEach(f)})()</script>")
    open(ra, "w", encoding="utf8").write(html.replace("</body>", vá + "</body>"))
    return ra


def canh_du_lieu(bd, ws):
    out = []
    for k, c in enumerate(bd.get("canh", []), 1):
        a, b = c["tu"]
        out.append({"id": k, "t_in": round(ws[a][1], 1), "t_out": round(ws[b][2], 1), "say": " ".join(x[0] for x in ws[a:b + 1]),
                    "suggest": c.get("goi_y") or ["speaker_only"]})
    return out


def doc_chon(text, so_canh):
    """Kết quả dán từ trang chọn → ({số cảnh: mã}, preset hoặc None). 'làm hết' → {} (giữ gợi ý đầu)."""
    if re.search(r"l[aà]m h[eế]t|lam-het", text, re.I):
        return {}, None
    chon = {}
    for a, b, m in re.findall(r"[Cc]ảnh\s*(\d+)\s*(?:[–-]\s*(\d+))?\s*:\s*(bỏ|bo\b|[a-z_]+)", text):
        for k in range(int(a), int(b or a) + 1):
            if 1 <= k <= so_canh:
                chon[k] = "speaker_only" if m in ("bỏ", "bo") else m
    p = re.search(r"[Pp]reset\s*:?\s*([a-z_]+)", text)
    return chon, (p.group(1) if p and p.group(1) in PRESET.values() else None)


# ---------- chạy ----------
def nhan_ban_youtube(ten, pj):
    """Bản YouTube 16:9 của bản TikTok đã duyệt: cùng timeline, chữ, màu, text ghi âm; khung ngang tự đặt (footage dọc: hai bên nền mờ).
    Dựng + kiểm vùng an toàn YouTube + kiểm bản dựng. Trả tên dự án YouTube."""
    import shutil
    from server import tao_du_an, PROJ
    yt = ten.replace("_tiktok_", "_youtube_") if "_tiktok_" in ten else ten + "-youtube"
    py = os.path.join(PROJ, yt)
    if not os.path.exists(os.path.join(py, "timeline.json")):
        tao_du_an({"name": yt, "platform": "youtube", "from": ten})
        for f in ("BAN-DUNG.json", "mau", os.path.join("build", "transcripts"), os.path.join("build", "voice.wav")):  # đối chiếu + LUT dùng lại
            src = os.path.join(pj, f)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(py, f), dirs_exist_ok=True)
            elif os.path.exists(src):
                shutil.copy(src, os.path.join(py, f))
    if chay("scripts/kiem_vung.py", py):
        sys.exit(f"Bản YouTube: chữ tràn vùng an toàn (xem trên). Claude sửa projects/{yt}/timeline.json rồi chạy lại agent.")
    chay("scripts/dung.py", py)
    if chay("scripts/kiem_cuoi.py", py):
        sys.exit("Bản YouTube chưa đạt kiểm tra (xem trên).")
    return yt


def chay_agent(ten, nguon, opt):
    from server import tao_du_an, PROJ
    pj = os.path.join(PROJ, ten)
    if not os.path.exists(os.path.join(pj, "timeline.json")):
        if not nguon:
            sys.exit(f"Chưa có dự án {ten}: thêm nguồn (thư mục/file/link) sau tên.")
        link = [x for x in nguon if x.startswith(("http://", "https://"))]
        tao_du_an({"name": ten, "platform": opt.get("platform", "tiktok"), "nguon": link, "tep": [x for x in nguon if x not in link]},
                  lambda i, n, ten, da, tong, **k: print(f"\rtải {i}/{n} {ten} {da >> 20}/{tong >> 20} MB   ", end="", flush=True))
        print(f"\nĐã tạo dự án {ten}")
    SP = os.path.join(pj, "AGENT.json")
    moi = not os.path.exists(SP)
    st = doc(SP, {"qua": []})
    st["preset"] = PRESET.get(opt.get("preset", ""), st.get("preset") or PRESET[lay("agent.preset")])
    st["mau"] = opt.get("mau") or st.get("mau") or lay("agent.mau")
    if opt.get("qua"):
        st["qua"] = sorted(set(st["qua"]) | {opt["qua"]})
    B = os.path.join(pj, "build")
    T = os.path.join(pj, "timeline.json")
    BD = os.path.join(pj, "BAN-DUNG.json")

    for k in ("kich-ban", "tai-nguyen", "du-an", "ca-hai"):  # nhớ tham số cho các lần chạy sau
        if opt.get(k) is not None:
            st[k] = opt[k]
    if st.get("du-an"):
        tl0 = doc(T); tl0.setdefault("meta", {})["du_an"] = st["du-an"]; ghi(T, tl0)
    if st.get("kich-ban") and not st.get("kb"):
        import kich_ban_doc
        try:
            print(f"Kịch bản: {len(kich_ban_doc.ghi(pj, st['kich-ban']))} câu → KICH-BAN.md", flush=True)
        except Exception as ex:
            dung_lai(st, pj, CHO_CLAUDE, f"CHỜ CLAUDE: không tải được kịch bản ({ex}). Đọc Doc bằng công cụ Google Docs, lưu .txt, "
                     f"chạy lại agent.py {ten} --kich-ban <file .txt>.")
        st["kb"] = True
    if st.get("tai-nguyen") and not st.get("tn"):
        import kho, tai_drive
        goc = kho.goc_kho()
        if not goc:
            dung_lai(st, pj, CHO_HAO, "CẦN HÀO: chưa chọn thư mục kho tài nguyên trên máy (vd thư mục Drive KHO-EDIT). Chạy: python scripts/kho.py <thư mục kho>, rồi chạy lại agent.")
        da = st.get("du-an") or (ten.split("_")[2] if ten.count("_") >= 3 else ten)
        dich = os.path.join(goc, "20_DU-AN", da)
        os.makedirs(dich, exist_ok=True)
        print(f"Tải tài nguyên dự án vào kho: {dich}", flush=True)
        tai_drive.tai_nguon(st["tai-nguyen"], dich)
        kho.luu(goc)
        st["tn"] = True
        ghi(SP, st)
    from doi_chieu import doc_kich_ban
    if not st.get("cat") and not st.get("xep") and any(l.strip("() ") and not l.startswith("(") for _, l, _ in doc_kich_ban(pj)):
        chay("scripts/xep_canh.py", pj)  # trước master cut: xếp clip quay lộn xộn theo kịch bản
        st["xep"] = True
        ghi(SP, st)

    B0 = os.path.join(pj, "build")
    if moi and os.path.exists(os.path.join(B0, "master-cut.md")):  # dự án làm trước khi có agent: đã cắt (có thể đã chỉnh tay), không cắt lại
        st["cat"] = True
    # 1–2. bản nhẹ (master cut tự tạo) + master cut, một lần
    if not st.get("cat"):
        chay("scripts/master_cut.py", pj)
        st["cat"] = True
        ghi(SP, st)
    # 3. ghép giọng đúng mốc video + nhận dạng (đổi cắt thì nhận dạng lại)
    import giong, phu_de
    tl = doc(T)
    tv = tl.get("meta", {}).get("tu_vung")
    cache = phu_de.file_dem(B, "voice.wav", tv, tl)
    if moi and os.path.exists(cache) and os.path.exists(os.path.join(B, "voice.wav")):  # dự án cũ: giữ text đã nhận dạng (BAN-DUNG.json đánh số theo nó)
        st["giong"] = hashlib.sha1(open(os.path.join(B, "voice.wav"), "rb").read()).hexdigest()
    v = giong.tao(B, tl, lambda *a: subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True))
    h = hashlib.sha1(open(v, "rb").read()).hexdigest()
    if st.get("giong") != h:
        for f in (cache, phu_de.file_tin(cache)):
            if os.path.exists(f):
                os.remove(f)
        st["giong"] = h
    phu_de.nhan_dang(v, cache, tv, tl)
    from ban_dung import chep, doc_loi, kiem_ban, kiem_canh
    chep(pj)
    tl, ws = doc_loi(pj)
    tin = doc(phu_de.file_tin(cache), [])

    # CỔNG 1
    if 1 not in st["qua"]:
        dong, goi_y = cau_hoi_loi(pj, tl, ws, tin)
        xc = (tl.get("meta", {}).get("xep_canh") or {})
        hoi_xep = ([f"- Câu kịch bản chưa có clip nào nói: {', '.join(map(str, xc['thieu']))} (quay thêm / bỏ câu / trám hình)"] if xc.get("thieu") else []) + \
                  ([f"- Clip có lời nhưng không khớp câu nào (chưa đưa vào video): {', '.join(xc['khong_khop'])}"] if xc.get("khong_khop") else [])
        if dong or goi_y or hoi_xep:
            md = ["# Cần Hào trả lời trước khi đi tiếp (agent dừng, không đoán)", "",
                  f"Toàn bộ lời nói: `build/LOI-NOI.md`. Trả lời từng dòng: đúng / sửa thành … / cắt. Claude ghi vào `meta.sua_tu`, `meta.da_duyet`, cắt bằng `cat_doan.py`, rồi chạy `agent.py {ten} --qua 1`.", ""]
            if dong:
                md += ["## Từ cần xác nhận (máy nghe không chắc, tên riêng, con số)", "", "| Giây | Từ | Vì sao hỏi | Câu |", "|---|---|---|---|", *dong, ""]
            if hoi_xep:
                md += ["## Thứ tự clip theo kịch bản (chi tiết: XEP-CANH.md)", "", *hoi_xep, ""]
            if goi_y:
                md += ["## Đoạn nghi lặp / vấp / cắt (giữ nguyên cho tới khi Hào nói cắt)", "", "| Giây | Loại | Chi tiết | Đề xuất |", "|---|---|---|---|",
                       *[f"| {t:.1f} | {l} | {nd} | {dx} |" for t, l, nd, dx in goi_y], ""]
            open(os.path.join(pj, "CAN-HOI.md"), "w", encoding="utf8").write("\n".join(md))
            dung_lai(st, pj, CHO_HAO, f"CỔNG 1: {len(dong)} từ cần xác nhận, {len(goi_y)} đoạn nghi lặp/vấp/cắt, {len(hoi_xep)} mục xếp clip "
                     f"→ {os.path.relpath(pj, ROOT)}/CAN-HOI.md")
        st["qua"] = sorted(set(st["qua"]) | {1})

    # 3b. Claude mô tả ảnh/video kho dự án (một lần mỗi file) để trám cảnh tìm đúng hình
    import tram_canh
    if tram_canh.can_mo_ta(pj):
        dung_lai(st, pj, CHO_CLAUDE, f"CHỜ CLAUDE: xem ảnh nhỏ build/mo-ta/*.jpg theo {os.path.relpath(pj, ROOT)}/CAN-MO-TA.md, ghi vài cụm từ mỗi file vào "
                 f"kho/MO-TA.json (không rõ là gì thì ghi \"\"), rồi chạy lại agent.")

    # 4. Claude chia cảnh + vai chữ
    bd = doc(BD)
    if not bd or not bd.get("canh"):
        dung_lai(st, pj, CHO_CLAUDE, f"CHỜ CLAUDE: đọc build/LOI-NOI.md, viết BAN-DUNG.json gồm 'canh' (chia cảnh 2–8 giây theo ý, 2–4 mã gợi ý từ "
                 f"autoedit/QUY-TRINH-AUTOEDIT.md mục 5 / autoedit/HIEU-UNG-MAP.json) và 'vai' (hook, tiêu đề, từ khoá, số liệu có nguồn, cta). Rồi chạy lại agent.")
    loi = kiem_ban({**bd, "canh": [{k: v for k, v in c.items() if k != "chon"} for c in bd["canh"]]}, ws)
    if loi:
        dung_lai(st, pj, CHO_CLAUDE, "CHỜ CLAUDE sửa BAN-DUNG.json:\n- " + "\n- ".join(loi))

    # 5. trang chọn hiệu ứng → CỔNG 2
    if opt.get("chon") is not None:
        chon, pre = doc_chon(opt["chon"], len(bd["canh"]))
        for k, c in enumerate(bd["canh"], 1):
            c["chon"] = chon.get(k, (c.get("goi_y") or ["speaker_only"])[0])
        st["preset"] = pre or st["preset"]
        ghi(BD, bd)
        st["qua"] = sorted(set(st["qua"]) | {2})
    if 2 not in st["qua"]:
        ra = trang("picker_template.html", {"scenes": canh_du_lieu(bd, ws)}, st["preset"], os.path.join(B, "chon-hieu-ung.html"))
        dung_lai(st, pj, CHO_HAO, f"CỔNG 2: Hào mở {os.path.relpath(ra, ROOT)}, chọn hiệu ứng từng cảnh, dán kết quả: agent.py {ten} --chon \"…\" (hoặc --chon \"làm hết\")")
    loi, bao = kiem_canh(bd, ws)
    if loi:
        dung_lai(st, pj, CHO_CLAUDE, "CHỜ CLAUDE đặt vai cho hiệu ứng Hào đã chọn (BAN-DUNG.json):\n- " + "\n- ".join(loi))

    # 6. storyboard → CỔNG 3
    mp = json.load(open(os.path.join(AE, "HIEU-UNG-MAP.json"), encoding="utf8"))
    if 3 not in st["qua"]:
        chay("scripts/ban_dung.py", "ap", pj)
        import ap_mau
        t0 = doc(T)
        t1 = ap_mau.ap(t0, ap_mau.MAU[st["mau"]])
        t1.setdefault("audio", {}).update(voice=True, music=t0.get("audio", {}).get("music"))  # talking head: giữ giọng; nhạc theo dự án, mẫu không tự thêm
        ghi(T, t1)
        chay("scripts/tram_canh.py", pj)  # trám ảnh/video kho dự án + cảnh không lời
        if not st.get("mau_do"):
            chay("scripts/chinh_mau.py", pj)  # đo màu từng cảnh, LUT + ảnh trước/sau (chưa áp)
            st["mau_do"] = True
        chay("scripts/storyboard.py", pj)
        sc = canh_du_lieu(bd, ws)
        for s, c in zip(sc, bd["canh"]):
            m = mp.get(c["chon"], {})
            s.update(effect=c["chon"], name=m.get("ten", c["chon"]),
                     need=[{"k": "có trong bộ dựng" if m.get("co") else "đợt 2: tạm dựng chỉ người nói", "ok": bool(m.get("co"))}])
        ra = trang("storyboard_template.html", {"scenes": sc}, st["preset"], os.path.join(B, "storyboard-chot.html"))
        dung_lai(st, pj, CHO_HAO, "CỔNG 3: Hào xem STORYBOARD.md (kế hoạch dựng: nhịp, vai, zoom, âm) + build/storyboard.jpg, "
                 "TRAM-CANH.md (cảnh trám từ kho), MAU-SAC.md (ảnh trước/sau LUT màu) và "
                 f"{os.path.relpath(ra, ROOT)} (hiệu ứng từng cảnh)." + (("\nLưu ý:\n- " + "\n- ".join(bao)) if bao else "")
                 + f"\n\"Chốt phương án\" → agent.py {ten} --qua 3. Sửa gì thì nói Claude sửa rồi chạy lại.")

    if st.get("mau_do") and not st.get("mau_ap"):  # Hào chốt phương án (gồm màu) → áp LUT từng cảnh
        chay("scripts/chinh_mau.py", pj, "--ap")
        st["mau_ap"] = True
        ghi(SP, st)

    # 7. bản xem 540×960 → CỔNG 4
    if 4 not in st["qua"]:
        chay("scripts/dung.py", pj, "--xem")
        if chay("scripts/kiem_vung.py", pj):
            dung_lai(st, pj, CHO_CLAUDE, "CHỜ CLAUDE: chữ tràn vùng an toàn (xem danh sách ở trên): rút gọn chữ/đổi bố cục rồi chạy lại.")
        dung_lai(st, pj, CHO_HAO, f"CỔNG 4: Hào xem out/{ten}.xem.mp4 (có vạch vùng an toàn). Đạt → agent.py {ten} --qua 4")

    # 8. bản cuối: đối chiếu (dung.py tự dừng), vùng an toàn, dựng, kiểm bản dựng
    if chay("scripts/kiem_vung.py", pj):
        dung_lai(st, pj, CHO_CLAUDE, "CHỜ CLAUDE: chữ tràn vùng an toàn, sửa rồi chạy lại.")
    chay("scripts/dung.py", pj)
    if chay("scripts/kiem_cuoi.py", pj):
        dung_lai(st, pj, CHO_CLAUDE, "CHỜ CLAUDE: bản dựng chưa đạt kiểm tra (xem trên).")
    chay("scripts/anh_bia.py", pj)
    ra = [f"out/{ten}.mp4", f"anh-bia/{ten}/ (3 ảnh bìa TikTok + 3 YouTube, Hào chọn trong ANH-BIA.md)"]
    if st.get("ca-hai"):
        yt = nhan_ban_youtube(ten, pj)
        ra.append(f"out/{yt}.mp4 (YouTube 16:9)")
    st["xong"] = time.strftime("%Y-%m-%d %H:%M")
    dung_lai(st, pj, 0, "XONG, đã qua mọi cổng: " + " · ".join(ra))


def _tu_kiem():
    assert doc_chon("Preset xanh_gradient Chọn hiệu ứng: Cảnh 1–3: chart_bars; Cảnh 4: bỏ", 5) == ({1: "chart_bars", 2: "chart_bars", 3: "chart_bars", 4: "speaker_only"}, "xanh_gradient")
    assert doc_chon("làm hết", 3) == ({}, None) and doc_chon("Cảnh 9: typo", 3) == ({}, None)
    ws = [["Theo", 0, .3], ["Vinhomes", .3, .8], ["Saigon", .8, 1.2], ["Park", 1.2, 1.5], ["rộng", 1.5, 1.8], ["1.080", 1.8, 2.4], ["ha.", 2.4, 2.8]]
    tl = {"version": 1, "meta": {"tu_vung": ["Vinhomes"]}, "clips": [{"file": "a", "in": 0, "dur": 3}], "transitions": []}
    import phan_tich_loi
    goc = phan_tich_loi.phan_tich
    phan_tich_loi.phan_tich = lambda *a: []
    try:
        dong, goi_y = cau_hoi_loi(None, tl, ws, [.9, .99, .5, .95, .95, .9, .9])
    finally:
        phan_tich_loi.phan_tich = goc
    txt = "\n".join(dong)
    assert len(cau_hoi_loi(None, tl, ws + ws, [.9, .99, .5, .95, .95, .9, .9] * 2)[0]) == len(dong)  # nói lại cùng từ: không hỏi thêm dòng
    assert "**Saigon**" in txt and "không chắc" in txt and "**1.080**" in txt and "**Vinhomes**" not in txt, txt  # từ vựng đã biết thì không hỏi
    import tempfile
    ra = trang("picker_template.html", {"scenes": [{"id": 1, "t_in": 0, "t_out": 2, "say": "x", "suggest": ["typo_fire"]}]}, "xanh_gradient",
               os.path.join(tempfile.mkdtemp(), "p.html"))
    s = open(ra, encoding="utf8").read()
    assert '"base": "ANH"' in s and "data:image/jpeg;base64," in s and "xanh_gradient/typo_fire" in s
    print("OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--tu-kiem"]:
        _tu_kiem(); sys.exit()
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    ten, opt, nguon, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--kich-ban", "--tai-nguyen", "--du-an") and i + 1 < len(a):
            opt[a[i][2:]] = a[i + 1]; i += 2
        elif a[i] == "--ca-hai":
            opt["ca-hai"] = True; i += 1
        elif a[i] in ("--preset", "--mau", "--chon", "--qua") and i + 1 < len(a):
            opt[a[i][2:]] = int(a[i + 1]) if a[i] == "--qua" else a[i + 1].upper() if a[i] == "--preset" else a[i + 1]; i += 2
        elif a[i] == "--youtube":
            opt["platform"] = "youtube"; i += 1
        elif a[i] == "--trang-thai":
            print(json.dumps(doc(os.path.join(ROOT, "projects", ten, "AGENT.json"), {}), ensure_ascii=False, indent=1)); sys.exit()
        else:
            nguon.append(a[i]); i += 1
    chay_agent(ten, nguon, opt)
