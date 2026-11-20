"""Thử CẢ QUY TRÌNH trên một dự án mới, đúng như bấm nút trong app (Hào chốt 20/11: lỗi chỉ lộ ra ở dự án mới, nên phải thử cả chuỗi):
tạo dự án → master cut → phụ đề → đối chiếu → bản xem 540 → storyboard → nháp → bản cuối → kiểm bản cuối → kiểm vùng an toàn.
Mỗi bước ghi đạt/lỗi, thời gian, các dòng lỗi cuối vào MỘT file BAO-CAO-THU.md (gửi Claude file này là đủ).
Chạy trong video-studio:
  python scripts/thu_quy_trinh.py <thư mục video | tên dự án có sẵn> [--nhanh]   (--nhanh: chỉ 3 video đầu)
  Windows: bấm đúp thu-quy-trinh.bat
Dự án thử tên zz-thu-<ngày-giờ> (video liên kết cứng, không chép thêm; xoá thư mục đó khi xong). Bản cuối dựng với --da-duyet CHỈ để thử máy, không đăng."""
import os, platform, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
VIDEO = (".mp4", ".mov", ".m4v", ".mkv", ".mts")


def buoc_chay(ten, lenh, log_dir, cho_phep=(0,)):
    """Chạy một bước bằng đúng Python đang chạy (như app). Trả dict kết quả; nhật ký đầy đủ ở log_dir/<số>.log."""
    t0 = time.time()
    p = subprocess.run(lenh, cwd=ROOT, capture_output=True, text=True, encoding="utf8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    f = os.path.join(log_dir, f"{len(os.listdir(log_dir)) + 1:02d}-{ten.split()[0]}.log")
    open(f, "w", encoding="utf8").write(out)
    return {"ten": ten, "dat": p.returncode in cho_phep, "ma": p.returncode, "giay": round(time.time() - t0, 1),
            "cuoi": "\n".join(out.strip().splitlines()[-30:]), "log": f}  # đường dẫn đầy đủ: relpath lỗi khi khác ổ đĩa (Windows C: và D:)


def bao_cao(kq, may, ten_da):
    dat = all(k["dat"] for k in kq)
    md = [f"# Báo cáo thử cả quy trình: {'ĐẠT HẾT' if dat else 'CÓ LỖI'}", "", f"- Dự án thử: `projects/{ten_da}`",
          *[f"- {k}: {v}" for k, v in may.items()], "", "| # | Bước | Kết quả | Thời gian |", "|---|---|---|---|"]
    md += [f"| {i} | {k['ten']} | {'đạt' if k['dat'] else '**LỖI** (mã %s)' % k['ma']} | {k['giay']}s |" for i, k in enumerate(kq, 1)]
    for k in kq:
        if not k["dat"]:
            md += ["", f"## Lỗi ở bước: {k['ten']}", f"Nhật ký đầy đủ: `{k['log']}`", "```", k["cuoi"], "```"]
    return "\n".join(md) + "\n"


def thong_tin_may():
    from ban_nhe import hw
    v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[:1]
    return {"Máy": f"{platform.system()} {platform.release()} ({platform.machine()})", "Python": sys.executable,
            "FFmpeg": (v or ["?"])[0], "Giải nén bằng card NVIDIA": "có" if hw() else "không", "Ngày": time.strftime("%Y-%m-%d %H:%M")}


def thu_muc_nguon(nguon, nhanh):
    """Thư mục video để tạo dự án: thư mục cho sẵn, hoặc build/raw của dự án có sẵn. --nhanh: thư mục tạm chỉ 3 video đầu (liên kết cứng)."""
    pj = os.path.join(ROOT, "projects", nguon)
    d = os.path.join(pj, "build", "raw") if os.path.isdir(os.path.join(pj, "build", "raw")) else nguon
    if not os.path.isdir(d):
        sys.exit(f"Không thấy thư mục video hay dự án: {nguon}")
    if not nhanh:
        return d
    tam = tempfile.mkdtemp(prefix="thu-nhanh-")
    for f in sorted(x for x in os.listdir(d) if x.lower().endswith(VIDEO))[:3]:
        from server import lien_ket
        lien_ket(os.path.join(d, f), os.path.join(tam, f))
    return tam


def chay(nguon, nhanh=False):
    sys.path.insert(0, os.path.join(ROOT, "studio"))
    from server import tao_du_an
    ten = "zz-thu-" + time.strftime("%Y%m%d-%H%M")
    pj = os.path.join(ROOT, "projects", ten)
    log_dir = os.path.join(pj, "build", "thu")
    may, kq, t0 = thong_tin_may(), [], time.time()
    try:
        tao_du_an({"name": ten, "platform": "tiktok", "folder": thu_muc_nguon(nguon, nhanh)})
        os.makedirs(log_dir, exist_ok=True)
        kq.append({"ten": "Tạo dự án", "dat": True, "ma": 0, "giay": round(time.time() - t0, 1), "cuoi": "", "log": "-"})
    except Exception as ex:  # tạo không được thì báo luôn, không có gì để thử tiếp
        print(f"LỖI tạo dự án: {ex}")
        sys.exit(1)
    py, sc = sys.executable, lambda f: os.path.join(HERE, f)
    cac_buoc = [("Master cut (cắt lặng, phân tích hình)", [py, sc("master_cut.py"), pj]),
                ("Phụ đề (nhận dạng giọng)", [py, sc("phu_de.py"), pj]),
                ("Đối chiếu chữ/số", [py, sc("doi_chieu.py"), pj], (0, 2)),  # mã 2 = có mục cần hỏi Hào: không phải lỗi máy
                ("Bản xem 540×960", [py, sc("dung.py"), pj, "--xem"]),
                ("Storyboard", [py, sc("storyboard.py"), pj]),
                ("Dựng nháp", [py, sc("dung.py"), pj, "--nhap"]),
                ("Bản cuối (chỉ để thử)", [py, sc("dung.py"), pj, "--da-duyet"]),
                ("Kiểm bản cuối (khổ, độ dài, tiếng, LUFS)", [py, sc("kiem_cuoi.py"), pj]),
                ("Kiểm vùng an toàn TikTok", [py, sc("kiem_vung.py"), pj])]
    for b in cac_buoc:
        print(f"→ {b[0]}…", flush=True)
        k = buoc_chay(b[0], b[1], log_dir, *b[2:])
        kq.append(k)
        print(f"  {'đạt' if k['dat'] else 'LỖI'} ({k['giay']}s)", flush=True)
        if not k["dat"]:
            break  # các bước sau cần kết quả bước này
    f = os.path.join(pj, "BAO-CAO-THU.md")
    open(f, "w", encoding="utf8").write(bao_cao(kq, may, ten))
    print(f"\nBáo cáo: {f}\nGửi Claude file này. Xong việc có thể xoá thư mục projects/{ten}.")
    return all(k["dat"] for k in kq)


def _tu_kiem():
    d = tempfile.mkdtemp()
    ok = buoc_chay("Bước đạt", [sys.executable, "-c", "print('xin chào')"], d)
    loi = buoc_chay("Bước lỗi", [sys.executable, "-c", "import sys; print('dòng 1'); sys.exit('hỏng rồi')"], d)
    hoi = buoc_chay("Đối chiếu", [sys.executable, "-c", "import sys; sys.exit(2)"], d, (0, 2))
    assert ok["dat"] and not loi["dat"] and loi["ma"] == 1 and "hỏng rồi" in loi["cuoi"] and hoi["dat"], (ok, loi, hoi)
    md = bao_cao([ok, loi], {"Máy": "thử"}, "zz-thu-x")
    assert "CÓ LỖI" in md and "**LỖI** (mã 1)" in md and "hỏng rồi" in md and md.count("## Lỗi") == 1, md
    assert "ĐẠT HẾT" in bao_cao([ok, hoi], {}, "x")
    shutil.rmtree(d)
    print("OK")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--nhanh"]
    if sys.argv[1:] == ["--tu-kiem"]:
        _tu_kiem()
    elif len(a) == 1:
        sys.exit(0 if chay(a[0], "--nhanh" in sys.argv) else 1)
    else:
        sys.exit(__doc__)
