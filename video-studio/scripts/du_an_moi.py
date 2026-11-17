"""Tạo dự án video từ một thư mục footage, KHÔNG cần mở app: mỗi video thành một đoạn (cắt thẳng), file nhạc trong thư mục thành nhạc nền.
Footage không bị chép thêm (liên kết cứng; khác ổ đĩa thì chép). Dùng đúng hàm của app (studio/server.py: tao_du_an).
Chạy trong video-studio:  python scripts/du_an_moi.py "<thư mục footage>" <tên-dự-án> [tiktok|youtube]
Tên dự án theo quy ước: <ngày>_<tiktok|youtube>_<dự án>_<chủ đề>, không dấu cách."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "studio"))
from server import tao_du_an  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    try:
        r = tao_du_an({"folder": os.path.abspath(sys.argv[1]), "name": sys.argv[2], "platform": sys.argv[3] if len(sys.argv) == 4 else "tiktok"})
    except ValueError as ex:
        sys.exit(f"Không tạo được dự án: {ex}")
    print(f"Đã tạo projects/{r['name']} ({r['clips']} đoạn video).")
