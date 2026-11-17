---
name: lap-storyboard
description: Lập storyboard video TikTok/YouTube cho Hào Sky Land từ thư mục footage (Drive hoặc trên máy) và kịch bản. Dùng khi Hào gửi thư mục footage, kịch bản, hoặc nhờ "lên storyboard", "chọn cảnh", "phân tích footage".
---

# Lập storyboard

Đầu ra: `video-studio/projects/<tên>/timeline.json` + `STORYBOARD.md` để Hào duyệt **trước** khi dựng.
Tên thư mục theo `docs/01-he-thong/THU-MUC-VA-DAT-TEN.md` (`<ngày>_<tiktok|youtube>_<dự án>_<chủ đề>`). Chưa có thư mục thì chép `mau/du-an-video/` sang trước.

1. Lấy danh sách clip:
   - Drive: tìm theo `parentId = '<id thư mục>'` bằng công cụ Google Drive. File trên 10 MB không tải qua công cụ được; tải thẳng bằng `curl -L "https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t"` (cần mạng cho `drive.usercontent.google.com`, thư mục phải chia sẻ bằng link).
   - Trên máy: liệt kê thư mục footage.
2. Mỗi clip tạo ảnh lưới để xem nhanh: `video-studio/scripts/contact-sheet.sh <video> <giây giữa các khung>`. Xem ảnh, ghi lại: cảnh gì, quay dọc/ngang, đoạn đẹp (giây), có người nói không.
3. Đọc `BRIEF.md`, `KICH-BAN.md`, `NGUON-SO-LIEU.md` trong thư mục video (nếu có). Không có thì viết bản nháp theo footage, giọng theo `CLAUDE.md` (mộc mạc, nêu cả rủi ro, không từ cấm, không tự điền số liệu dự án: để `[...]`).
4. Tạo `projects/<tên>/timeline.json` theo định dạng trong `video-studio/scripts/timeline.py` (xem mẫu `projects/test90/timeline.json`): `clips` (file, id Drive, in, dur, focus), `transitions` (cut / cube-h / cube-v, mỗi chỗ nối một cái), `texts` (kind hook/section/line/outro, start, dur tính trên video thành phẩm), `audio`. Tên phong cách, chỉnh màu, chuyển cảnh, hiệu ứng chữ, khối chữ: xem `docs/04-thu-vien/THU-VIEN-HIEU-UNG.md`. Có số liệu thì thêm khối `source` (thẻ nguồn). Từ tô vàng viết `*từ*`. Kiểm tra: `python3 scripts/test_timeline.py` (trong `video-studio`).
5. Tạo `STORYBOARD.md` + ảnh lưới `build/storyboard.jpg` bằng `python scripts/storyboard.py projects/<tên>` (đọc timeline: từng cảnh, giây, hình, lời nói, chữ, chuyển cảnh, mục "Cần Hào trả lời"). Thêm tay mục "Chưa có" (giọng, logo, nguồn số liệu…) nếu thiếu.
6. Nhịp TikTok: hook dưới 2–3 giây, cảnh 2,5–5 giây (xem `docs/04-thu-vien/THU-VIEN-MAU.md` mục 1.5). Báo Hào nếu footage không đủ.

Dừng ở đây và hỏi Hào duyệt. Không dựng khi chưa được duyệt. Duyệt xong: dựng bản xem 540×960 (`dung.py --xem`), Hào duyệt tiếp rồi mới dựng bản cuối.
