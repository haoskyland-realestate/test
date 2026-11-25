#!/usr/bin/env python3
"""Lấy phụ đề tiếng Việt của vài video YouTube và rút ra CÁCH NÓI của người dẫn, để Claude phân tích phong cách.

Dùng: python scripts/phan_tich_giong_nguoi_noi.py https://www.youtube.com/@khoailangthang/videos [--so 6] [--ra nghien-cuu/phong-cach/khoailangthang.md]
Chọn video: 4 video nhiều xem nhất + (so-4) video mới nhất trong 60 video gần đây.
Ra một file Markdown: số liệu (tốc độ nói, cụm từ lặp) và các đoạn trích NGUYÊN VĂN (mở đầu, giữa, kết) có mốc giờ.
Phải chạy trên PC của Hào (IP nhà): máy chủ cloud bị YouTube chặn. Phụ đề tự động có thể sai chữ.
"""
import argparse, collections, json, pathlib, re, subprocess, sys, tempfile, time


def doc_vtt(txt):
    """VTT -> [(giây, dòng chữ)], bỏ thẻ <c>, bỏ dòng lặp liên tiếp (phụ đề tự động lặp dòng trước)."""
    cues, t = [], None
    for line in txt.splitlines():
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ --> ", line)
        if m:
            t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line or t is None or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if cues and cues[-1][1] == line:
            continue
        cues.append((t, line))
    return cues


def cum_tu(cues, n, toi_thieu):
    tu = [w for _, l in cues for w in re.findall(r"[^\W\d_]+", l.lower())]
    c = collections.Counter(" ".join(tu[i:i + n]) for i in range(len(tu) - n + 1))
    return [(k, v) for k, v in c.most_common(300) if v >= toi_thieu][:25], len(tu)


def trich(cues, bat_dau, do_dai=90):
    return " ".join(l for t, l in cues if bat_dau <= t < bat_dau + do_dai)


def phan_tich(cues, giua=3, do_dai=90):
    """giua = số đoạn trích ở giữa video, do_dai = độ dài mỗi đoạn trích (giây)."""
    if not cues:
        return None
    het = cues[-1][0] + 5
    bi, so_tu = cum_tu(cues, 2, 8)
    tri, _ = cum_tu(cues, 3, 5)
    mocs = [(i + 1) / (giua + 1) for i in range(giua)]
    return {"het_giay": het, "so_tu": so_tu, "tu_moi_phut": round(so_tu / (het / 60)), "cum2": bi, "cum3": tri,
            "doan": [(f"Mở đầu (0 đến {do_dai} giây)", 0, trich(cues, 0, do_dai))] +
                    [(f"Giữa video, phút {int(het * p / 60)}", int(het * p), trich(cues, int(het * p), do_dai)) for p in mocs] +
                    [(f"Kết ({do_dai} giây cuối)", max(het - do_dai, 0), trich(cues, max(het - do_dai, 0), do_dai))]}


def lay_video(url, so):
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "-J", "--flat-playlist", "--playlist-end", "60", url],
                       capture_output=True, text=True, timeout=300)
    if r.returncode:
        sys.exit("yt-dlp lỗi: " + r.stderr[-400:])
    ds = [e for e in json.loads(r.stdout)["entries"] if e.get("id")]
    top = sorted([e for e in ds if e.get("view_count")], key=lambda e: -e["view_count"])[:4]
    moi = [e for e in ds if e not in top][: max(so - 4, 0)]
    return top + moi


def lay_phu_de(vid, thu_muc, ngon_ngu="vi.*,vi"):
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--skip-download", "--write-auto-subs", "--write-subs",
                    "--sub-langs", ngon_ngu, "--sub-format", "vtt", "-o", f"{thu_muc}/%(id)s.%(ext)s",
                    f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=300)
    f = sorted(pathlib.Path(thu_muc).glob(f"{vid}*.vtt"))
    return doc_vtt(f[0].read_text(encoding="utf-8", errors="replace")) if f else []


def tu_kiem():
    v = "WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nxin chào <c>các bạn</c>\n\n00:00:03.000 --> 00:00:05.000\nxin chào các bạn\nhôm nay đi chợ\n\n00:00:05.000 --> 00:00:07.000\nhôm nay đi chợ\nvui lắm\n"
    c = doc_vtt(v)
    assert [l for _, l in c] == ["xin chào các bạn", "hôm nay đi chợ", "vui lắm"], c
    r = phan_tich(c)
    assert r["so_tu"] == 10 and r["doan"][0][2].startswith("xin chào"), r
    print("tự kiểm đạt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?"); ap.add_argument("--so", type=int, default=6); ap.add_argument("--ra")
    ap.add_argument("--tu-kiem", action="store_true")
    ap.add_argument("--ngon-ngu", default="vi.*,vi", help='ngôn ngữ phụ đề, ví dụ "en.*,en" cho kênh nói tiếng Anh')
    ap.add_argument("--giua", type=int, default=3, help="số đoạn trích ở giữa video")
    ap.add_argument("--do-dai", type=int, default=90, help="độ dài mỗi đoạn trích (giây)")
    a = ap.parse_args()
    if a.tu_kiem:
        tu_kiem(); sys.exit()
    if not a.url:
        ap.error("cần link kênh YouTube (kết thúc bằng /videos)")
    ten = re.search(r"@([\w.\-]+)", a.url)
    ra = pathlib.Path(a.ra or f"nghien-cuu/phong-cach/{ten.group(1) if ten else 'kenh'}.md")
    ra.parent.mkdir(parents=True, exist_ok=True)
    out = [f"# Cách nói của {a.url}", "", "Phụ đề tự động YouTube, có thể sai chữ. Các đoạn trích là nguyên văn phụ đề.", ""]
    with tempfile.TemporaryDirectory() as d:
        for e in lay_video(a.url, a.so):
            print("đang lấy:", e.get("title", e["id"])[:70], flush=True)
            r = phan_tich(lay_phu_de(e["id"], d, a.ngon_ngu), a.giua, a.do_dai)
            out += [f"## {e.get('title', e['id'])}", f"Lượt xem: {e.get('view_count')}. Link: https://www.youtube.com/watch?v={e['id']}", ""]
            if not r:
                out += ["(không có phụ đề tiếng Việt)", ""]
            else:
                out += [f"Tốc độ: khoảng {r['tu_moi_phut']} từ mỗi phút ({r['so_tu']} từ trong {r['het_giay'] // 60} phút).", "",
                        "Cụm hai từ lặp nhiều: " + "; ".join(f"{k} ({v})" for k, v in r["cum2"]), "",
                        "Cụm ba từ lặp nhiều: " + "; ".join(f"{k} ({v})" for k, v in r["cum3"]), ""]
                for ten_doan, giay, van in r["doan"]:
                    out += [f"### {ten_doan} (giây {giay})", van, ""]
            time.sleep(5)
    ra.write_text("\n".join(out), encoding="utf-8")
    print("Đã ghi:", ra)
