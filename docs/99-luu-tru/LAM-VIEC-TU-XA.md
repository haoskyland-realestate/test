# Cách giao việc từ điện thoại và làm từ xa trên MacBook

Mục tiêu của Hào: giao việc từ điện thoại (Claude app / Cowork), hoặc làm thẳng trên MacBook M1 kiểu điều khiển từ xa. Ưu tiên miễn phí (không tốn thêm ngoài gói Claude đang dùng).

## 3 cách, so sánh

| | A. Phiên cloud (như hiện tại) | B. MacBook chạy Claude Code, điều khiển từ điện thoại | C. Cowork trên Claude Desktop (Mac) |
|---|---|---|---|
| Giao việc từ điện thoại | Có | Có (Remote Control, hiện trong app Claude Code) | Có khi máy bật |
| Footage nằm ở đâu | Phải tải từ Drive mỗi phiên | Ngay trên Mac | Ngay trên Mac |
| Dữ liệu sau phiên | **Mất** khi phiên kết thúc (chỉ còn mã đã đẩy lên GitHub) | Giữ nguyên | Giữ nguyên |
| Tốc độ dựng | Chỉ CPU, video 90s mất 10–20 phút | Nhanh hơn (chip M1, tùy RAM), chưa đo | Như B |
| Mở CapCut/DaVinci để sửa tay | Không | Có, cùng máy | Có |
| Điều kiện | Không cần máy tính | Mac phải bật, có mạng, không ngủ | Như B |
| Chi phí thêm | 0 (dùng hạn mức gói Claude) | 0 | 0 |
| Hợp với | Kịch bản, storyboard, viết mã, làm mẫu, dựng video ngắn | Dựng video thật từ footage, sửa tay, lưu kho mẫu | Việc văn phòng: sắp xếp file, tài liệu |

## Khuyến nghị: kết hợp A + B
- **A (cloud, từ điện thoại)** cho việc không cần footage: viết kịch bản, storyboard, xây thư viện mẫu, sửa mã. Mã luôn đẩy lên GitHub nên không mất.
- **B (MacBook)** cho việc dựng video thật: footage để sẵn trên Mac, bấm việc từ điện thoại, Mac dựng.
- PC RTX 5060 để sau, khi B chạy ổn và cần dựng nhanh hơn.

## Thiết lập B (làm một lần trên Mac)
1. Cài Claude Code trên Mac (theo hướng dẫn chính thức), đăng nhập cùng tài khoản.
2. Tải repo này về Mac, cài công cụ: Node.js 22, FFmpeg, Python (sẽ có `setup-mac.sh` để chạy một lệnh, **chưa viết**).
3. Trong thư mục repo chạy `claude remote-control` (hoặc dùng Claude Desktop). Phiên này sẽ hiện trong app Claude Code trên điện thoại.
4. Giữ Mac không ngủ khi đang dựng (ví dụ lệnh `caffeinate`), cắm sạc.
5. Footage để trong `video-studio/projects/<tên>/media/` hoặc thư mục đồng bộ Google Drive trên Mac.

Lưu ý: phiên cloud hiện tại **không** kết nối được tới Mac (chưa có thư mục máy tính nào được chia sẻ). Việc trên Mac phải làm trong phiên chạy trên chính Mac.

## Chưa kiểm
- Chưa thử bộ dựng trên macOS / chip M1 (đã thử trên Linux).
- Chưa đo tốc độ dựng trên M1, chưa biết RAM của máy Hào.
