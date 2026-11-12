---
name: dung-video
description: Dựng video từ storyboard đã duyệt (timeline.json) ra MP4 9:16 có chuyển cảnh khối 3D, chữ động tiếng Việt, nhạc. Dùng khi Hào nói "dựng", "render", "xuất video" cho một dự án trong video-studio/projects.
---

# Dựng video

Chạy trên máy mạnh (PC Windows) hoặc phiên cloud. Cần: Node 22, FFmpeg, Python 3 + numpy, `npm install` trong `video-studio`.

1. Kiểm tra `video-studio/projects/<tên>/timeline.json` đã được Hào duyệt; chạy `python3 scripts/test_timeline.py` để chắc file hợp lệ.
2. Footage: đặt bản gốc vào `projects/<tên>/build/raw/<file>` (hoặc để trống, bộ dựng tự tải từ Drive theo `id`).
3. Chạy trong `video-studio`: `python3 scripts/dung.py projects/<tên>` (chạy nền; 90 giây mất khoảng 10–20 phút trên cloud). Bộ dựng nhớ cảnh đã cắt: chỉ sửa chữ thì dựng lại nhanh, đổi cảnh thì tự cắt lại cảnh đó.
4. Kết quả: `video-studio/out/<tên>.mp4`. Sau đó dùng skill `bao-cao-nghiem-thu`.

Không đăng video lên đâu. Không đưa footage, `build/`, `out/` lên GitHub (đã có trong .gitignore).
