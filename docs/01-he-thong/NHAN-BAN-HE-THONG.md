# Nhân bản

Lập 12/11/2026. Ba mức, từ nhỏ đến lớn.

## Mức 1. Một video mới (hằng tuần)
App studio → nút **＋** → đặt tên theo quy ước (`THU-MUC-VA-DAT-TEN.md`) → chọn thư mục footage → Tạo.
App tự chép các file mẫu trong `mau/du-an-video/` vào thư mục video mới. Không cần làm gì thêm.

Không dùng app: chép thư mục `mau/du-an-video/` thành `video-studio/projects/<tên>/`, rồi nhờ Claude Code tạo `timeline.json`.

## Mức 2. Cùng video, khung khác (TikTok ↔ YouTube)
App → tab **Khung hình** → "Nhân bản dự án này sang …". Footage dùng chung, không tốn thêm ổ. Tên mới chỉ đổi phần nền tảng: `..._tiktok_...` → `..._youtube_...`.

## Mức 3. Cả hệ thống cho thương hiệu hoặc lĩnh vực khác
Ví dụ sau này: kênh huấn luyện cá nhân (PT), quán hải sản. Phần mềm giữ nguyên; chỉ đổi phần "nội dung và thương hiệu".

1. Trên GitHub tạo repo mới (riêng tư) từ repo này: "Use this template" nếu đã bật chế độ mẫu, hoặc tải về rồi đẩy lên repo mới. Việc tạo repo do Hào bấm.
2. Đổi đúng các chỗ sau (Claude Code làm được nếu Hào giao):

| File | Đổi gì |
|---|---|
| `CLAUDE.md` | Mục đích, Người dùng, khách mục tiêu, Quy tắc nội dung (giọng, từ cấm theo ngành), Giỏ hàng; xoá bảng Trạng thái cũ |
| `mau/du-an-video/*.md` | Câu hỏi trong BRIEF, cột trong NGUON-SO-LIEU (ngành khác có thể không cần) |
| `mau/PROMPT-MAU.md` | Khối "quy tắc nội dung", nhóm khách |
| `docs/01-he-thong/THU-MUC-VA-DAT-TEN.md` | Bảng "dự án BĐS" → danh mục của ngành mới; tên thư mục gốc trên PC |
| `video-studio/scripts/dung.py` | Chữ `HÀO SKY LAND` ở cảnh kết (khối `outro`) và logo góc |
| `video-studio/scripts/effects.py` | Màu, font của 3 phong cách (`STYLES`) |
| `video-studio/studio/index.html` | Tên trên tab trình duyệt (`<title>`) |
| `.claude/skills/*/SKILL.md` | Ví dụ và quy tắc nội dung nhắc trong skill |
| `docs/03-ke-hoach/` | Xoá kế hoạch cũ, viết kế hoạch mới |
| `video-studio/projects/` | Xoá các dự án cũ (giữ lại 1 làm mẫu nếu cần) |

3. Giữ nguyên: `video-studio/studio/`, `video-studio/scripts/` (trừ chỗ thương hiệu ở bảng trên), `docs/04-thu-vien/`, `docs/05-app/`, `thu-vien-chuyen-nghiep/`.
4. Kiểm: chạy các file `video-studio/scripts/test_*.py`; mở app, tạo một dự án thử tên `zz-thu`.

**Chưa thử** nhân bản mức 3. Tên thương hiệu hiện còn viết thẳng trong mã (`dung.py`); khi Hào gửi logo/màu thật sẽ gom vào một chỗ (`video-studio/brand/`) để nhân bản chỉ cần thay thư mục đó.
