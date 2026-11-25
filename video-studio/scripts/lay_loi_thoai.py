#!/usr/bin/env python3
"""Lấy LỜI THOẠI của video TikTok công khai (tải âm thanh bằng yt-dlp, phiên âm bằng faster-whisper) để phân tích phong cách.

Kênh:   python scripts/lay_loi_thoai.py quangvinhrealestate namrealty [--toi-da 300] [--moi 5]
Video lẻ: python scripts/lay_loi_thoai.py --kenh ten_kenh --video <link1> <link2> ...
Chọn video của kênh: các video NỔ (từ 2 lần mức nền của chính kênh) + N video mới nhất. Mỗi video lấy tối đa --toi-da giây đầu.
Ra: nghien-cuu/loi-thoai/<kenh>.md (mốc giây, câu, link, lượt xem). Phiên âm tự động nên có thể sai chữ; chỉ dùng nội bộ để học cấu trúc.
"""
import argparse, json, pathlib, random, re, subprocess, sys, tempfile, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nghien_cuu_tiktok import lay_video, tim_outlier  # noqa: E402
from phan_tich_giong_nguoi_noi import cum_tu  # noqa: E402


def chon(entries, he_so=2.0, moi=5):
    """Trả (mức nền, danh sách video đã chọn, tập id video nổ). Kênh ít dữ liệu thì chỉ lấy video mới nhất."""
    try:
        tv, out = tim_outlier(entries, he_so)
    except ValueError:
        tv, out = 0, []
    chon_ = {}
    for e in out + entries[:moi]:
        chon_.setdefault(e["id"], e)
    return tv, list(chon_.values()), {e["id"] for e in out}


def mm_ss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def tai_am_thanh(url, thu_muc):
    vid = url.rstrip("/").split("/")[-1].split("?")[0]
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "-f", "ba/b", "-o", f"{thu_muc}/%(id)s.%(ext)s", url],
                   capture_output=True, text=True, timeout=300)
    f = sorted(pathlib.Path(thu_muc).glob(f"{vid}.*"))
    return f[0] if f else None


def nghe(model, path, toi_da):
    import numpy as np
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-ar", "16000", "-ac", "1", "-t", str(toi_da), "-f", "f32le", "-"]
    audio = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    segs, _ = model.transcribe(audio, language="vi", beam_size=1, vad_filter=True)
    return [(s.start, s.text.strip()) for s in segs if s.text.strip()]


def thong_tin_video(url):
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "-j", "--no-download", url], capture_output=True, text=True, timeout=120)
    if r.returncode:
        return {"id": url.rstrip("/").split("/")[-1].split("?")[0], "url": url}
    d = json.loads(r.stdout.splitlines()[0])
    return {"id": d["id"], "url": url, "view_count": d.get("view_count"), "like_count": d.get("like_count"),
            "duration": d.get("duration"), "description": d.get("description") or d.get("title")}


def md_video(e, cues, no):
    tieu = (e.get("description") or e.get("title") or e["id"]).strip().split("\n")[0][:110]
    dong = [f"## {tieu}", f"Xem: {e.get('view_count')} | Thích: {e.get('like_count')} | Dài: {e.get('duration')}s | {'VIDEO NỔ' if no else 'video mới'} | {e.get('url')}", ""]
    dong += [f"[{mm_ss(t)}] {c}" for t, c in cues] or ["(không nhận ra lời nói)"]
    return "\n".join(dong) + "\n"


def tu_kiem():
    es = [{"id": str(i), "view_count": v} for i, v in enumerate([100, 110, 120, 130, 140, 150, 1000, 105])]
    tv, ds, no = chon(es, 2, 2)
    assert no == {"6"} and [e["id"] for e in ds] == ["6", "0", "1"], (ds, no)
    tv, ds, no = chon([{"id": "a"}, {"id": "b"}, {"id": "c"}], 2, 2)  # thiếu số liệu: chỉ lấy video mới nhất
    assert no == set() and [e["id"] for e in ds] == ["a", "b"]
    assert mm_ss(75) == "01:15"
    assert "VIDEO NỔ" in md_video({"id": "x", "view_count": 5}, [(3, "chào")], True) and "[00:03] chào" in md_video({"id": "x"}, [(3, "chào")], False)
    print("tự kiểm đạt")


def chay_kenh(model, ten, url, videos, toi_da, thu_muc_ra):
    tong, md = 0, [f"# Lời thoại @{ten}", "", "Phiên âm tự động (Whisper), có thể sai chữ. Chỉ dùng nội bộ để học cấu trúc.", ""]
    cues_all = []
    with tempfile.TemporaryDirectory() as tmp:
        for e, no in videos:
            print(f"  {ten}: {e['id']} ({e.get('view_count')} xem)", flush=True)
            try:
                p = tai_am_thanh(e["url"], tmp)
                cues = nghe(model, p, toi_da) if p else []
            except Exception as ex:  # shortcut: bỏ qua video lỗi, kênh vẫn chạy tiếp
                print("   lỗi:", str(ex)[:120], flush=True)
                cues = []
            md.append(md_video(e, cues, no))
            cues_all += cues
            tong += 1 if cues else 0
            time.sleep(random.uniform(3, 6))
    if cues_all:
        bi, so_tu = cum_tu(cues_all, 2, 6)
        tri, _ = cum_tu(cues_all, 3, 4)
        md.insert(3, "Cụm hai từ lặp: " + "; ".join(f"{k} ({v})" for k, v in bi) + "\n\nCụm ba từ lặp: " + "; ".join(f"{k} ({v})" for k, v in tri) + f"\n\nTổng {so_tu} từ trong {len(cues_all)} câu.\n")
    pathlib.Path(thu_muc_ra).mkdir(parents=True, exist_ok=True)
    f = pathlib.Path(thu_muc_ra) / f"{ten}.md"
    f.write_text("\n".join(md), encoding="utf-8")
    print(f"  -> {f} ({tong}/{len(videos)} video có lời thoại)", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("kenh", nargs="*"); ap.add_argument("--video", nargs="*"); ap.add_argument("--ten")
    ap.add_argument("--toi-da", type=int, default=300); ap.add_argument("--moi", type=int, default=5)
    ap.add_argument("--ra", default="nghien-cuu/loi-thoai"); ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        tu_kiem(); sys.exit()
    from faster_whisper import WhisperModel
    model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
    if a.video:
        vs = [(thong_tin_video(u), False) for u in a.video]
        chay_kenh(model, a.ten or "video-le", None, vs, a.toi_da, a.ra)
    for k in a.kenh:
        ten = k.split("@")[-1].strip("/").split("?")[0]
        url = k if k.startswith("http") else f"https://www.tiktok.com/@{ten}"
        try:
            ds = lay_video(url, 30)
        except RuntimeError as ex:
            print(f"[lỗi] {ten}: {str(ex)[:150]}", flush=True)
            continue
        tv, chon_, no = chon(ds, 2.0, a.moi)
        print(f"{ten}: mức nền {tv:,.0f}, chọn {len(chon_)} video ({len(no)} nổ)", flush=True)
        chay_kenh(model, ten, url, [(e, e["id"] in no) for e in chon_], a.toi_da, a.ra)
