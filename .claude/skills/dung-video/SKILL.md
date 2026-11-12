---
name: dung-video
description: Dựng video từ storyboard đã duyệt (shots.json) ra MP4 9:16 có chuyển cảnh khối 3D, chữ động tiếng Việt, nhạc. Dùng khi Hào nói "dựng", "render", "xuất video" cho một dự án trong video-studio/projects.
---

# Dựng video

Chạy trên máy mạnh (PC Windows) hoặc phiên cloud. Cần: Node 22, FFmpeg, Python 3 + numpy, `npm install` trong `video-studio`.

1. Kiểm tra `video-studio/projects/<tên>/shots.json` đã được Hào duyệt.
2. Footage: đặt bản gốc vào `projects/<tên>/build/raw/<file>` (hoặc để trống, `make.py` tự tải từ Drive theo `id`).
3. Chạy trong `video-studio`: `python3 projects/<tên>/make.py` (chạy nền, có thể mất 10–20 phút cho 90 giây). Đổi cảnh thì xóa `projects/<tên>/build/` trước khi dựng lại; chỉ sửa chữ thì không cần.
4. Kết quả: `video-studio/out/<tên>.mp4`. Sau đó dùng skill `bao-cao-nghiem-thu`.

Không đăng video lên đâu. Không đưa footage, `build/`, `out/` lên GitHub (đã có trong .gitignore).
