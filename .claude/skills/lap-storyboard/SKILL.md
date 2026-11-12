---
name: lap-storyboard
description: Lập storyboard video TikTok/YouTube cho Hào Sky Land từ thư mục footage (Drive hoặc trên máy) và kịch bản. Dùng khi Hào gửi thư mục footage, kịch bản, hoặc nhờ "lên storyboard", "chọn cảnh", "phân tích footage".
---

# Lập storyboard

Đầu ra: `video-studio/projects/<tên>/shots.json` + `storyboard.md` để Hào duyệt **trước** khi dựng.

1. Lấy danh sách clip:
   - Drive: tìm theo `parentId = '<id thư mục>'` bằng công cụ Google Drive. File trên 10 MB không tải qua công cụ được; tải thẳng bằng `curl -L "https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t"` (cần mạng cho `drive.usercontent.google.com`, thư mục phải chia sẻ bằng link).
   - Trên máy: liệt kê thư mục footage.
2. Mỗi clip tạo ảnh lưới để xem nhanh: `video-studio/scripts/contact-sheet.sh <video> <giây giữa các khung>`. Xem ảnh, ghi lại: cảnh gì, quay dọc/ngang, đoạn đẹp (giây), có người nói không.
3. Đọc kịch bản (nếu có). Không có thì viết bản nháp theo footage, giọng theo `CLAUDE.md` (mộc mạc, nêu cả rủi ro, không từ cấm, không tự điền số liệu dự án: để `[...]`).
4. Chép `video-studio/projects/test90` thành `projects/<tên>` (bỏ thư mục `build/`), sửa `shots.json`: mỗi cảnh `file`, `id` (Drive), `in`, `dur`, `kind` (hook / section / line / outro), chữ. Từ cần tô vàng viết `*từ*`.
5. Viết `storyboard.md`: bảng # · giây · cảnh · chữ · chuyển cảnh, và mục "Chưa có" (giọng, logo, nguồn số liệu…).
6. Nhịp TikTok: hook dưới 2–3 giây, cảnh 2,5–5 giây (xem `docs/THU-VIEN-MAU.md` mục 1.5). Báo Hào nếu footage không đủ.

Dừng ở đây và hỏi Hào duyệt. Không dựng khi chưa được duyệt.
