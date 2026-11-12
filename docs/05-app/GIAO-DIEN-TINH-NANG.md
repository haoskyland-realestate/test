# Đối chiếu tính năng với ảnh mẫu Hào gửi (12/11/2026)

Ảnh: `docs/05-app/anh-giao-dien/`. App: `video-studio/studio/` (chạy `chay-studio.bat` hoặc `python3 studio/server.py`).
Trạng thái: **Có** = đã làm và thử trên cloud bằng Chromium · **Tạm** = có bản đơn giản · **Chưa**.

| Ảnh mẫu | Trạng thái | Ghi chú |
|---|---|---|
| Tên dự án, thống kê (độ dài, số đoạn cắt, chữ, phụ đề, minh hoạ), "Chưa lưu", phiên bản | Có | Phiên bản = tên phong cách; số phiên bản lưu nằm ở Lịch sử |
| Nút bố cục: ẩn/hiện khung xem, khung chỉnh, timeline, toàn màn hình | Có | |
| Hoàn tác / Làm lại | Có | Ctrl+Z, Ctrl+Shift+Z / Ctrl+Y |
| Thư viện | Có | Xem hiệu ứng; áp dụng thẳng cho chuyển cảnh/khối chữ đang chọn |
| Lịch sử | Có | Mỗi lần Lưu giữ 1 bản, giữ 30 bản; mở lại bản cũ |
| Nhờ AI sửa | Tạm | Soạn sẵn yêu cầu để dán cho Claude Code; gọi AI trong app cần khóa API, có phí → chờ Hào quyết |
| Lưu / Dựng nháp / Xuất video | Có | Nháp: nhanh, chất lượng thấp (`out/<tên>.nhap.mp4`) |
| Khung TikTok 9:16 / YouTube 16:9 | Có (12/11) | Tab Khung hình: đổi khung, nhân bản sang khung kia; vùng an toàn theo khung; đoạn quay dọc trong khung ngang: “Vừa khung” = nền mờ |
| Dự án mới từ thư mục footage | Có (12/11) | Nút ＋ cạnh tên dự án: chọn thư mục trên PC (duyệt được từ điện thoại), chọn khung; nhạc .mp3/.wav trong thư mục chọn được ở tab Âm thanh |
| Đặt chữ theo kịch bản | Có (13/11) | Tab Chữ → 📝: đọc cột "Chữ trên màn hình" của `KICH-BAN.md`, tìm lúc nói trong phụ đề (chịu được lỗi chính tả, lệch dấu), đặt chữ 3D; có bảng báo cáo từng chữ; hoàn tác được. `scripts/kich_ban.py` |
| Kho hiệu ứng âm | Có (12/11) | Tab Hiệu ứng âm, hàng ♪ |
| Thư viện mẫu edit | Có (13/11) | Nút ✦ Thư viện mẫu: 6 thẻ có xem trước chữ chuyển động, lọc theo loại, Áp mẫu, đọc Công thức. Thẻ so sánh 2 cột (khối chữ `compare`) |
| Xuất sang Premiere / DaVinci | Có (12/11) | Nút “Premiere/DaVinci”: tải `.xml` (Premiere), `.otio` (DaVinci), `.srt`. Chưa mở thử trong phần mềm thật |
| Thư viện chuyển cảnh gl-transitions | Có (12/11) | 212 hiệu ứng trong hộp Thư viện, ô tìm, khung xem thử WebGL, nút áp dụng |
| Tab Chữ, Phụ đề, Cắt, Zoom, Minh hoạ, Cảnh trám, Âm thanh, Khung hình, Thương hiệu | Có | Có đếm số mục, tìm kiếm, Thêm |
| Khung xem: phát/dừng, −1s/+1s, mốc giờ, vùng an toàn | Có | Phát bản xem trước nhẹ 540p tự tạo từ footage; chữ, phụ đề, minh hoạ, zoom, cảnh trám hiện đè đúng thời điểm (chữ chưa có chuyển động trong xem trước) |
| Danh sách mục ở giữa (thẻ minh hoạ, phụ đề…) | Có | Ảnh nhỏ cho đoạn cắt và cảnh trám |
| Khung chỉnh bên phải + Phím tắt | Có | Space, ←/→ từng khung, Shift+←/→ 1 giây, S tách, Delete xoá, Ctrl+S lưu |
| Timeline: Tách, Xoá, mốc giờ, thu phóng −/+, Vừa khung | Có | |
| Hàng Chữ, Phụ đề, Minh hoạ, Cảnh trám, Zoom, Video, Giọng nói | Có | Kéo thả để dời, kéo mép phải để đổi độ dài; kim chạy kéo được trên thước |
| Video có dải ảnh, Giọng nói có sóng âm | Có | |
| Phụ đề tự sinh từ giọng nói | Có (12/11) | Nút “Tạo phụ đề từ giọng nói” ở tab Phụ đề, hoặc `python3 scripts/phu_de.py projects/<tên>`. Whisper large-v3-turbo, tiếng Việt; chạy trên cloud (CPU) và PC (card NVIDIA, tự về CPU nếu thiếu thư viện). Thử: clip 43 giây nhận dạng 11–12 giây |
| Tự cắt khoảng lặng ("sau khi cắt", "đoạn đã cắt") | Có (12/11) | Nút “✨ Master cut” ở tab Cắt (`scripts/master_cut.py`): cắt im lặng theo âm lượng thật, bỏ tiếng đệm, bỏ lần nói vấp, chấm điểm khung hình, chọn khúc đẹp, chỉnh nhịp, phóng xen kẽ ~4s; có báo cáo. Thử: clip thật 48,7s → 18,4s |
| Thương hiệu: logo, màu thật | **Chưa** | Chờ Hào gửi; hiện có 3 phong cách |

## Thêm so với ảnh mẫu (theo nhu cầu Hào)
- 10 chuyển cảnh (khối 3D, lật thẻ, hòa tan…), 9 khối chữ (số liệu, danh sách kiểm, thẻ nguồn…), 3 phong cách, 4 chỉnh màu.
- Lỗi nhập liệu báo bằng tiếng Việt khi Lưu.
- Chữ, phụ đề, minh hoạ, zoom, cảnh trám tự dời theo khi đoạn video dài/ngắn hay đổi chỗ.
- Mở được trên điện thoại cùng wifi (bố cục xếp dọc), có mã khóa.

## Việc tiếp theo đề xuất
2. Chuẩn âm lượng (giọng to rõ, mức phổ biến cho TikTok); bản nháp mẫu đang hơi nhỏ (trung bình −28 dB).
3. Logo, màu thật; mẫu bố cục khi Hào gửi.
4. Chữ có chuyển động ngay trong khung xem trước.
