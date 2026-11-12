# Kế hoạch: app timeline (PC + điện thoại) và thư viện hiệu ứng

Lập 12/11/2026, sau khi Hào duyệt video test 89 giây. Âm thanh hiệu ứng chưa ổn: chờ thư mục âm thanh riêng của Hào.

## Kết luận: làm theo thứ tự này

1. **Định dạng timeline chung** (một file JSON mô tả cả video): nền móng, làm trước.
2. **Thư viện hiệu ứng v1** + trang xem trước: dùng được ngay trong cách dựng hiện tại.
3. **App timeline v1**: xem, sửa chữ, chỉnh thời lượng, chọn hiệu ứng, xem trước nháp.
4. **Máy chủ cục bộ trên Windows**: duyệt thư mục footage, tạo bản nhẹ, nút "Dựng video".
5. **Âm thanh** (khi có thư mục của Hào): thư viện tiếng hiệu ứng, nhạc, giọng thu, tự hạ nhạc khi có giọng.
6. **Kéo thả và cắt trên timeline**, tối ưu điện thoại, Claude tự chuyển storyboard thành timeline.

### Vì sao không làm giao diện trước
- Giao diện chỉ là cách chỉnh một file timeline. Nếu định dạng chưa chốt, giao diện sẽ phải viết lại.
- Hiện cách dựng nằm trong `projects/test90/make.py`, hiệu ứng viết cứng trong mã. Cần tách hiệu ứng thành thư viện thì app mới có cái để chọn.
- Thư viện hiệu ứng tạo giá trị ngay cho video thật (ưu tiên số 1 là ra video tạo khách), app thì phải đợi xong mới dùng được.

### Không làm (để khỏi phân tán)
- Không cố làm một CapCut/Premiere đầy đủ. App chỉ làm phần riêng của Hào: dựng tự động từ kịch bản + mẫu thương hiệu, sửa nhẹ, dựng lại. Chỉnh tinh từng khung hình thì xuất sang Premiere (xem câu hỏi 3).
- Không làm app riêng cho iOS/Android: một web app (PWA) chạy trên cả PC và điện thoại.

## Chi tiết từng bước

### Bước 1. Định dạng timeline v1 (dự kiến 13–14/11)
Một file `timeline.json` cho mỗi video:
- `meta`: tên, nền tảng (TikTok 9:16 / YouTube 16:9), fps, thương hiệu (logo, màu, font).
- `tracks.video`: cảnh (file, mốc vào/ra, lệch khung, chỉnh màu).
- `tracks.transition`: chuyển cảnh giữa hai cảnh (tên hiệu ứng + thông số).
- `tracks.text`: khối chữ (kiểu: mở đầu / mục số / dòng / kết, nội dung, hiệu ứng vào/ra, mốc giờ).
- `tracks.audio`: giọng, nhạc, tiếng hiệu ứng (để trống chờ thư mục âm thanh).

Việc: viết định dạng, chuyển `shots.json` của video test sang, sửa bộ dựng đọc `timeline.json`. Có kiểm tra tự động: file sai định dạng thì báo lỗi rõ ràng bằng tiếng Việt.
Xong khi: dựng lại video test từ `timeline.json` ra kết quả như cũ.

### Bước 2. Thư viện hiệu ứng v1 (dự kiến 15–18/11)
Mỗi hiệu ứng là một file riêng, có tên, mô tả tiếng Việt, thông số chỉnh được, ảnh/clip xem trước.

| Nhóm | Hiệu ứng v1 |
|---|---|
| Chuyển cảnh | khối 3D ngang, khối 3D dọc (đã có), lật thẻ, phóng xuyên, trượt có mờ chuyển động, mờ dần |
| Chữ vào | từng từ trượt lên (đã có), gõ chữ, hiện theo dòng, phóng nhẹ, quét sáng |
| Khối chữ | mở đầu có thẻ, mục số viền vàng (đã có), tiêu đề dưới màn hình, câu trích, cảnh kết thương hiệu |
| Màu | trung tính, ấm, tương phản cao |
| Âm thanh | **chờ thư mục của Hào** |

Trang "thư viện" (mở trên điện thoại được): lưới hiệu ứng, bấm để xem chạy thử.
Xong khi: video test dựng lại với hiệu ứng chọn từ thư viện, đổi hiệu ứng chỉ cần đổi tên trong `timeline.json`.

### Bước 3. App timeline v1 (dự kiến 19–25/11)
- Giao diện: PC thì timeline nằm ngang bên dưới, khung xem trước ở trên; điện thoại thì xem trước ở trên, danh sách cảnh cuộn dọc bên dưới.
- Làm được: xem video nháp trong trình duyệt (chữ và chuyển cảnh chạy thật, footage dùng bản nhẹ), sửa chữ, kéo dài/rút ngắn cảnh bằng thanh trượt, chọn hiệu ứng từ thư viện, lưu `timeline.json`.
- Chưa làm: kéo thả cắt nhiều lớp, ghi âm trong app.
Xong khi: Hào sửa một câu chữ và một hiệu ứng trên điện thoại, xem lại ngay không cần dựng.

### Bước 4. Máy chủ cục bộ trên Windows (dự kiến 26/11–2/12)
Footage nặng nằm trên máy Windows, nên app chạy từ máy đó:
- Một lệnh khởi động (bấm đúp file `.bat`), mở `localhost` trên PC; điện thoại cùng wifi mở bằng địa chỉ máy.
- Chọn thư mục footage → tự tạo bản nhẹ và ảnh lưới cảnh.
- Nút "Dựng video" → chạy bộ dựng, báo tiến độ, ra file MP4.
Xong khi: dựng được video từ footage trên máy Hào, điều khiển từ điện thoại.
Rủi ro: chưa thử trên Windows; dựng trên máy cần Chrome và FFmpeg (đã có `setup-windows.ps1`, chưa thử).

### Bước 5. Âm thanh (khi có thư mục của Hào)
Thư viện tiếng hiệu ứng (vút, chạm, chuyển), nhạc nền có giấy phép rõ, giọng thu; tự hạ nhạc khi có giọng; phụ đề từ giọng.

### Bước 6. Mở rộng
Kéo thả trên timeline, cắt clip, nhiều lớp chữ; Claude đọc kịch bản + ảnh lưới footage → đề xuất `timeline.json` để Hào duyệt; xuất XML sang Premiere nếu cần.

## Mốc tổng

| Mốc | Dự kiến | Hào có gì |
|---|---|---|
| Định dạng timeline | 14/11 | Video test dựng từ một file timeline |
| Thư viện hiệu ứng v1 | 18/11 | Trang xem 15+ hiệu ứng, đổi hiệu ứng bằng tên |
| App timeline v1 | 25/11 | Sửa chữ, thời lượng, hiệu ứng trên PC/điện thoại, xem nháp |
| Chạy trên Windows | 2/12 | Dựng từ footage trên máy, bấm từ điện thoại |
| Âm thanh | sau khi có thư mục | Tiếng hiệu ứng, nhạc, giọng |

Mốc phụ thuộc lượng token mỗi ngày và thời gian Hào duyệt. Nếu thiếu thời gian, giữ Bước 1–2 (ra video tốt hơn ngay), lùi Bước 3–4.

## Câu hỏi cần Hào chốt
1. App chạy từ máy Windows của Hào (khuyến nghị: footage ở đó, không tốn phí) hay chạy trên cloud (tiện hơn nhưng tải footage nặng, có thể tốn phí)?
2. Mức sửa trong app: sửa nhẹ (chữ, thời lượng, hiệu ứng) như kế hoạch, hay cần cắt ghép đầy đủ như CapCut?
3. Có cần xuất sang Premiere để chỉnh tinh không?
