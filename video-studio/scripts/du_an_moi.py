"""Tạo dự án video từ NHIỀU nguồn, KHÔNG cần mở app: thư mục/file trên máy, link Google Drive (thư mục hoặc file), link tải trực tiếp,
YouTube/TikTok (cần yt-dlp). Mỗi video thành một đoạn (cắt thẳng), file nhạc thành nhạc nền. Dùng đúng hàm của app (studio/server.py: tao_du_an).
Chạy trong video-studio:
  python scripts/du_an_moi.py <tên-dự-án> <nguồn 1> [nguồn 2 …] [--youtube]     (--youtube: khung ngang 16:9; mặc định TikTok dọc)
  python scripts/du_an_moi.py "<thư mục hoặc link>" <tên-dự-án> [tiktok|youtube]   (cách gọi cũ, vẫn dùng được)
  python scripts/du_an_moi.py --them <tên-dự-án> <nguồn …>                        (thêm footage vào dự án đã có)
Mọi nguồn gom vào video-studio/tai-ve/<tên-dự-án>/ (file trên máy: liên kết cứng, không chép thêm). Link Drive phải chia sẻ "Bất kỳ ai có đường liên kết".
Tên dự án theo quy ước: <ngày>_<tiktok|youtube>_<dự án>_<chủ đề>, không dấu cách."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "studio"))
from server import tao_du_an, them_nguon, SAFE  # noqa: E402


def doc_tham_so(av):
    """(chế độ, tên, platform, req) từ tham số dòng lệnh."""
    them = av[:1] == ["--them"]
    av = av[1:] if them else av
    pf = "youtube" if "--youtube" in av else "tiktok"
    av = [a for a in av if a != "--youtube"]
    if len(av) in (2, 3) and not SAFE.match(av[0]) and SAFE.match(av[1]):  # cách gọi cũ: nguồn trước, tên sau
        if len(av) == 3:
            pf = av[2]
        av = [av[1], av[0]]
    if len(av) < 2 or not SAFE.match(av[0]):
        sys.exit(__doc__)
    link = [a for a in av[1:] if a.startswith(("http://", "https://"))]
    tep = [a for a in av[1:] if a not in link]
    if thieu := [a for a in tep if not os.path.exists(a)]:
        sys.exit("Không thấy trên máy: " + ", ".join(thieu))
    return ("them" if them else "moi"), av[0], pf, {"name": av[0], "platform": pf, "nguon": link, "tep": tep}


if __name__ == "__main__":
    che_do, ten, pf, req = doc_tham_so(sys.argv[1:])
    bao = lambda i, n, ten, da, tong, nguon=1, so_nguon=1: print(f"\r[link {nguon}/{so_nguon}, file {i}/{n}] {ten}: {da >> 20}/{tong >> 20} MB   ", end="", flush=True)
    try:
        r = (them_nguon(ten, req, bao) if che_do == "them" else tao_du_an(req, bao))
    except ValueError as ex:
        sys.exit(f"\nKhông {'thêm được footage' if che_do == 'them' else 'tạo được dự án'}: {ex}")
    print(f"\n{'Đã thêm' if che_do == 'them' else 'Đã tạo'} projects/{r['name']} ({r['clips']} đoạn video). Tạo bản nhẹ 540p để phân tích và xem nhanh…")
    from ban_nhe import lay
    B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "projects", r["name"], "build")
    for f in sorted(os.listdir(os.path.join(B, "raw"))):
        if f.lower().endswith((".mp4", ".mov", ".m4v", ".mkv", ".mts")):
            lay(B, f)
    print("Xong.")
