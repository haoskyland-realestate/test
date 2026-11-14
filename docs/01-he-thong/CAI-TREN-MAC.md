# Chạy app studio trên MacBook

Lập 14/11/2026. MacBook M1 8 GB chạy được app, dựng video ngắn để thử. Video dài, 4K, nhiều chữ sau đầu thì để PC Windows.

## Cài một lần (khoảng 20–30 phút, cần mạng)
1. **Tải mã về Mac:** cài **GitHub Desktop** (desktop.github.com) → đăng nhập GitHub → File → Clone repository → chọn `haoskyland-realestate/test` → lưu vào thư mục `Documents`. Ở thanh trên, đổi nhánh (Current branch) sang `claude/admiring-babbage-gk9i49`.
2. Mở **Terminal** (Spotlight: gõ "Terminal").
3. Gõ (đổi đường dẫn nếu Hào lưu chỗ khác):
   ```
   cd ~/Documents/test/video-studio
   bash setup-mac.sh
   ```
   Script tự cài Homebrew, Node, FFmpeg, Python, thư viện dự án (vào thư mục `.venv`, không đụng Python của máy), rồi **kiểm máy và dựng thử 6 giây**. Có thể hỏi mật khẩu máy Mac lúc cài Homebrew.
4. Cuối màn hình phải thấy "Máy đủ điều kiện chạy app" và dựng thử đạt. Lỗi thì chụp màn hình gửi Claude.

**Lỗi "Thiếu zscale" (14/11/2026):** từ 01/2026 gói `ffmpeg` của Homebrew bị rút gọn, mất bộ lọc zscale. `setup-mac.sh` nay cài `ffmpeg-full` (không tự vào PATH, script tự thêm). Máy đã cài bản cũ thì chạy: `brew install ffmpeg-full` rồi chạy lại `bash setup-mac.sh`.

## Dùng hằng ngày
- Bấm đúp `video-studio/chay-studio.command` (lần đầu Mac có thể chặn: chuột phải → Mở → Mở).
- Mở đúng link có `?t=` in ra (bấm giữ Cmd rồi bấm link). Điện thoại cùng wifi mở link "Điện thoại".
- Lấy mã mới: GitHub Desktop → **Fetch origin** → **Pull**.

## Giới hạn trên Mac 8 GB
- Phụ đề tự động chạy bằng CPU: video 1 phút mất vài phút.
- Chữ sau đầu: khoảng 0,3 giây mỗi khung hình có chữ (video 70 giây có 8 chữ: khoảng 5–7 phút).
- Dựng 1080p được, chậm hơn PC. Không dựng 4K.
- Footage dài nên để trên ổ ngoài hoặc Drive, máy chỉ 256 GB.

**Trạng thái:** script viết 14/11, **chưa chạy thử trên Mac thật** (máy cloud là Linux, chỉ kiểm được cú pháp).
