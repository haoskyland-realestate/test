#!/usr/bin/env python3
"""Tìm video "nổ" (outlier) của một kênh TikTok công khai, không cần API key.

Dùng: python scripts/nghien_cuu_tiktok.py https://www.tiktok.com/@ten_kenh [--so 30] [--he-so 2] [--ra file.md]
Cần: pip install yt-dlp (chạy bằng .venv). Chỉ lấy dữ liệu công khai, không đăng nhập.
Outlier = lượt xem >= he-so x trung vị lượt xem của kênh (trung vị ít bị một video nổ kéo lệch).
"""
import argparse, json, statistics, subprocess, sys


def lay_video(url, so):
    # shortcut: dùng yt-dlp qua dòng lệnh, TikTok đổi giao diện thì cập nhật yt-dlp (pip install -U yt-dlp)
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-J", "--flat-playlist",
                        "--playlist-end", str(so), url], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        sys.exit("yt-dlp lỗi (chưa cài yt-dlp? TikTok chặn?):\n" + r.stderr[-600:])
    return json.loads(r.stdout).get("entries") or []


def tim_outlier(videos, he_so=2.0):
    """Trả (trung_vi, danh sách outlier giảm dần theo lượt xem). Bỏ video không có lượt xem."""
    co_xem = [v for v in videos if isinstance(v.get("view_count"), (int, float))]
    if len(co_xem) < 5:
        sys.exit(f"Chỉ có {len(co_xem)} video có số lượt xem, chưa đủ (>=5) để tính mức nền.")
    tv = statistics.median(v["view_count"] for v in co_xem)
    out = [v for v in co_xem if v["view_count"] >= he_so * max(tv, 1)]
    return tv, sorted(out, key=lambda v: -v["view_count"])


def bao_cao(url, tv, out, tong):
    dong = [f"# Video nổ của {url}", "",
            f"Mức nền (trung vị): {tv:,.0f} lượt xem, trên {tong} video gần nhất. Dữ liệu công khai, lấy lúc chạy lệnh.", "",
            "| Xem | Gấp | Thích | Hook (dòng đầu mô tả) | Link |", "|---|---|---|---|---|"]
    for v in out:
        hook = (v.get("description") or v.get("title") or "").strip().split("\n")[0][:80].replace("|", "/")
        dong.append(f"| {v['view_count']:,} | {v['view_count'] / max(tv, 1):.1f}x | {v.get('like_count', '?')} | {hook} | {v.get('url') or v.get('webpage_url', '')} |")
    return "\n".join(dong) + "\n"


def tu_kiem():
    vs = [{"view_count": n, "id": str(n)} for n in (100, 110, 120, 130, 140, 150, 1000)]
    tv, out = tim_outlier(vs, 2)
    assert tv == 130 and [v["view_count"] for v in out] == [1000], (tv, out)
    assert "1,000" in bao_cao("u", tv, out, 7)
    print("tự kiểm đạt")


if __name__ == "__main__":
    if sys.argv[1:] == ["--tu-kiem"]:
        tu_kiem(); sys.exit()
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("--so", type=int, default=30)
    ap.add_argument("--he-so", type=float, default=2.0); ap.add_argument("--ra")
    a = ap.parse_args()
    vids = lay_video(a.url, a.so)
    tv, out = tim_outlier(vids, a.he_so)
    md = bao_cao(a.url, tv, out, len(vids))
    open(a.ra, "w", encoding="utf-8").write(md) if a.ra else print(md)
