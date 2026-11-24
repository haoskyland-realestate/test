#!/usr/bin/env python3
"""Tìm video "nổ" (outlier) của các kênh TikTok công khai, không cần API key.

Một kênh:   python scripts/nghien_cuu_tiktok.py https://www.tiktok.com/@ten_kenh [--so 30] [--he-so 2] [--ra file.md]
Danh sách:  python scripts/nghien_cuu_tiktok.py --danh-sach nghien-cuu/kenh.txt   (mỗi dòng một link kênh, # là ghi chú)
            -> nghien-cuu/ket-qua/<kenh>_<ngay>.md; kênh đã lấy trong 7 ngày thì bỏ qua (thêm --ep để lấy lại).
Cần: pip install yt-dlp (chạy bằng .venv). Chỉ lấy dữ liệu công khai, không đăng nhập.
Outlier = lượt xem >= he-so x trung vị lượt xem của kênh (trung vị ít bị một video nổ kéo lệch).
Dùng nhẹ để không bị TikTok chặn: nghỉ 20-40s giữa các kênh, cache 7 ngày, kênh lỗi thì bỏ qua và chạy tiếp.
"""
import argparse, datetime, json, pathlib, random, re, statistics, subprocess, sys, time

CACHE_NGAY = 7


def lay_video(url, so):
    # shortcut: dùng yt-dlp qua dòng lệnh, TikTok đổi giao diện thì cập nhật yt-dlp (pip install -U yt-dlp)
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-J", "--flat-playlist",
                        "--playlist-end", str(so), url], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError("yt-dlp lỗi (chưa cài yt-dlp? TikTok chặn?): " + r.stderr[-400:].strip())
    return json.loads(r.stdout).get("entries") or []


def tim_outlier(videos, he_so=2.0):
    """Trả (trung_vi, danh sách outlier giảm dần theo lượt xem). Bỏ video không có lượt xem."""
    co_xem = [v for v in videos if isinstance(v.get("view_count"), (int, float))]
    if len(co_xem) < 5:
        raise ValueError(f"chỉ có {len(co_xem)} video có số lượt xem, chưa đủ (>=5) để tính mức nền")
    tv = statistics.median(v["view_count"] for v in co_xem)
    out = [v for v in co_xem if v["view_count"] >= he_so * max(tv, 1)]
    return tv, sorted(out, key=lambda v: -v["view_count"])


def bao_cao(url, tv, out, tong):
    dong = [f"# Video nổ của {url}", "",
            f"Mức nền (trung vị): {tv:,.0f} lượt xem, trên {tong} video gần nhất. Dữ liệu công khai, lấy ngày {datetime.date.today()}.", "",
            "| Xem | Gấp | Thích | Hook (dòng đầu mô tả) | Link |", "|---|---|---|---|---|"]
    for v in out:
        hook = (v.get("description") or v.get("title") or "").strip().split("\n")[0][:80].replace("|", "/")
        dong.append(f"| {v['view_count']:,} | {v['view_count'] / max(tv, 1):.1f}x | {v.get('like_count', '?')} | {hook} | {v.get('url') or v.get('webpage_url', '')} |")
    return "\n".join(dong) + "\n"


def doc_danh_sach(path):
    return [d.split("#")[0].strip() for d in pathlib.Path(path).read_text(encoding="utf-8").splitlines()
            if d.split("#")[0].strip()]


def ten_kenh(url):
    m = re.search(r"@([\w.\-]+)", url)
    return m.group(1) if m else re.sub(r"\W+", "_", url)[-40:]


def con_cache(thu_muc, kenh, hom_nay):
    """True nếu đã có kết quả của kênh trong CACHE_NGAY ngày gần nhất."""
    for f in thu_muc.glob(f"{kenh}_*.md"):
        try:
            if (hom_nay - datetime.date.fromisoformat(f.stem.rsplit("_", 1)[1])).days < CACHE_NGAY:
                return True
        except ValueError:
            pass
    return False


def chay_danh_sach(path, so, he_so, ep):
    thu_muc = pathlib.Path(path).parent / "ket-qua"
    thu_muc.mkdir(parents=True, exist_ok=True)
    hom_nay, loi, lam = datetime.date.today(), [], 0
    for url in doc_danh_sach(path):
        kenh = ten_kenh(url)
        if not ep and con_cache(thu_muc, kenh, hom_nay):
            print(f"[bỏ qua] {kenh}: đã lấy trong {CACHE_NGAY} ngày (dùng --ep để lấy lại)")
            continue
        if lam:
            time.sleep(random.uniform(20, 40))
        lam += 1
        try:
            vids = lay_video(url, so)
            tv, out = tim_outlier(vids, he_so)
            (thu_muc / f"{kenh}_{hom_nay}.md").write_text(bao_cao(url, tv, out, len(vids)), encoding="utf-8")
            print(f"[xong] {kenh}: {len(out)} video nổ, mức nền {tv:,.0f}")
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as e:
            loi.append(kenh)
            print(f"[lỗi] {kenh}: {e}")
    print(f"\nKết quả ở: {thu_muc}" + (f"\nKênh lỗi: {', '.join(loi)}" if loi else ""))
    return 1 if loi else 0


def tu_kiem():
    import tempfile
    vs = [{"view_count": n, "id": str(n)} for n in (100, 110, 120, 130, 140, 150, 1000)]
    tv, out = tim_outlier(vs, 2)
    assert tv == 130 and [v["view_count"] for v in out] == [1000], (tv, out)
    assert "1,000" in bao_cao("u", tv, out, 7)
    try:
        tim_outlier(vs[:3]); assert False
    except ValueError:
        pass
    assert ten_kenh("https://www.tiktok.com/@lam.phat-long?lang=vi-VN") == "lam.phat-long"
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d); k = d / "kenh.txt"
        k.write_text("# ghi chú\nhttps://www.tiktok.com/@a  # kênh A\n\n", encoding="utf-8")
        assert doc_danh_sach(k) == ["https://www.tiktok.com/@a"]
        hn = datetime.date(2026, 11, 20)
        (d / f"a_{hn - datetime.timedelta(days=3)}.md").write_text("x")
        assert con_cache(d, "a", hn) and not con_cache(d, "b", hn)
        (d / f"c_{hn - datetime.timedelta(days=9)}.md").write_text("x")
        assert not con_cache(d, "c", hn)
    print("tự kiểm đạt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?"); ap.add_argument("--so", type=int, default=30)
    ap.add_argument("--he-so", type=float, default=2.0); ap.add_argument("--ra")
    ap.add_argument("--danh-sach"); ap.add_argument("--ep", action="store_true")
    ap.add_argument("--tu-kiem", action="store_true")
    a = ap.parse_args()
    if a.tu_kiem:
        tu_kiem(); sys.exit()
    if a.danh_sach:
        sys.exit(chay_danh_sach(a.danh_sach, a.so, a.he_so, a.ep))
    if not a.url:
        ap.error("cần link kênh hoặc --danh-sach")
    try:
        vids = lay_video(a.url, a.so)
        tv, out = tim_outlier(vids, a.he_so)
    except (RuntimeError, ValueError) as e:
        sys.exit(str(e))
    md = bao_cao(a.url, tv, out, len(vids))
    open(a.ra, "w", encoding="utf-8").write(md) if a.ra else print(md)
