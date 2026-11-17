---
name: bao-cao-nghiem-thu
description: Kiểm tra một video đã dựng và viết báo cáo nghiệm thu để Hào đọc trên Mac/điện thoại. Dùng sau khi dựng video, hoặc khi Hào nhờ "kiểm tra", "nghiệm thu", "báo cáo" video.
---

# Báo cáo nghiệm thu

Đầu ra: `video-studio/out/<tên>-baocao.md` + `video-studio/out/<tên>-khunghinh.jpg`.

1. Thông số: `ffprobe -v error -show_entries stream=codec_name,width,height,duration -of csv=p=0 out/<tên>.mp4`. Đạt: 1080×1920 (TikTok) hoặc 1920×1080 (YouTube), H.264 + AAC, thời lượng đúng storyboard ±1 giây.
2. Ảnh khung hình: `ffmpeg -i out/<tên>.mp4 -vf "fps=1/5,scale=216:-2,tile=6x4" -frames:v 1 out/<tên>-khunghinh.jpg`. Xem ảnh, kiểm từng cảnh.
3. Kiểm và ghi Đạt / Chưa đạt cho từng mục:
   - Hook: chữ xuất hiện trong 3 giây đầu.
   - Chữ không lỗi dấu, không sót ký hiệu `*`, không bị che (vùng an toàn TikTok: tránh 220px trên, 420px dưới, 140px phải).
   - Không có từ cấm trong `CLAUDE.md`; mọi số liệu dự án có nguồn + ngày, chỗ chưa có ghi `[...]`.
   - Chuyển cảnh chạy (xem khung ở giữa chuyển cảnh), logo, cảnh kết.
   - Âm thanh có, không rè (nghe thử nếu được; nếu không nghe được thì ghi "chưa nghe").
4. Viết báo cáo: tóm tắt 3 dòng, bảng kiểm, việc cần Hào quyết định, phần chưa kiểm.

Không ghi "đạt" cho mục chưa kiểm.
