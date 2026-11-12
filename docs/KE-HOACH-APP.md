# Kế hoạch: app timeline (PC + điện thoại) và thư viện hiệu ứng

> **Cập nhật 12/11/2026 theo trả lời của Hào:** làm từ xa trên **MacBook M1** (không phải Windows) và giao việc từ điện thoại, ưu tiên miễn phí (xem `LAM-VIEC-TU-XA.md`). App cần **cắt ghép đầy đủ kiểu CapCut**, có thư mục mẫu (xem `THU-VIEN-MAU.md`). Các bước bên dưới đã đổi theo.

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
- Cắt ghép đầy đủ kiểu CapCut làm **theo từng đợt**: đợt 1 nhiều lớp, cắt, kéo thả, chọn mẫu; đợt 2 khung hình chính (keyframe), phụ đề theo giọng. Một app cắt ghép đầy đủ là việc nhiều tháng, nên trong lúc chờ, phần chỉnh tinh dùng phần mềm miễn phí trên Mac (CapCut bản máy tính, DaVinci Resolve) qua file xuất XML (DaVinci nhận được; CapCut chưa chắc nhận, cần thử).
- Không làm app riêng cho iOS/Android: một web app (PWA) chạy trên cả PC và điện thoại.

## Chi tiết từng bước

### Bước 1. Định dạng timeline v1: **XONG 12/11** (`scripts/timeline.py`, `scripts/dung.py`, test)
Một file `timeline.json` cho mỗi video:
- `meta`: tên, nền tảng (TikTok 9:16 / YouTube 16:9), fps, thương hiệu (logo, màu, font).
- `tracks.video`: cảnh (file, mốc vào/ra, lệch khung, chỉnh màu).
- `tracks.transition`: chuyển cảnh giữa hai cảnh (tên hiệu ứng + thông số).
- `tracks.text`: khối chữ (kiểu: mở đầu / mục số / dòng / kết, nội dung, hiệu ứng vào/ra, mốc giờ).
- `tracks.audio`: giọng, nhạc, tiếng hiệu ứng (để trống chờ thư mục âm thanh).

Việc: viết định dạng, chuyển `shots.json` của video test sang, sửa bộ dựng đọc `timeline.json`. Có kiểm tra tự động: file sai định dạng thì báo lỗi rõ ràng bằng tiếng Việt.
Xong khi: dựng lại video test từ `timeline.json` ra kết quả như cũ.

### Bước 2. Thư viện hiệu ứng v1: **XONG 12/11** (`scripts/effects.py`, demo `projects/thu-vien`)
Đặc tả đầy đủ: `THU-VIEN-MAU.md` (hệ thống thiết kế, 12 hiệu ứng chữ, 14 khối đồ họa, 12 chuyển cảnh, 6 mẫu bố cục). Bước này làm phần 1–2 của đặc tả; mẫu bố cục làm dần sau.
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

### Bước 3. App timeline v1: **XONG bản đầu 12/11** (`video-studio/studio/`). Thư viện mẫu bố cục để sau, chờ Hào gửi mẫu.
- Giao diện: PC thì timeline nằm ngang bên dưới, khung xem trước ở trên; điện thoại thì xem trước ở trên, danh sách cảnh cuộn dọc bên dưới.
- Làm được: xem video nháp trong trình duyệt (chữ và chuyển cảnh chạy thật, footage dùng bản nhẹ), sửa chữ, kéo dài/rút ngắn cảnh bằng thanh trượt, chọn hiệu ứng từ thư viện, lưu `timeline.json`.
- Chưa làm: kéo thả cắt nhiều lớp, ghi âm trong app.
Xong khi: Hào sửa một câu chữ và một hiệu ứng trên điện thoại, xem lại ngay không cần dựng.

### Bước 4. Chạy trên PC Windows (đổi lại theo `HE-THONG.md`: PC làm việc nặng, Mac nghiệm thu)
**Phần mềm xong 12/11, chưa thử trên PC thật:** nút ＋ Dự án mới chọn thư mục footage trên PC (cả từ điện thoại cùng wifi), tự tạo bản xem trước 540p, nút Dựng nháp/Xuất video, khung TikTok 9:16 hoặc YouTube 16:9. Còn lại: Hào chạy `setup-windows.ps1` một lần rồi bấm đúp `chay-studio.bat`.

#### (Bản cũ) Chạy trên MacBook
Footage nặng nằm trên MacBook, nên app chạy từ máy đó (đổi từ Windows theo Hào):
- `setup-mac.sh` cài công cụ một lần; một lệnh khởi động app, mở `localhost` trên Mac; điện thoại cùng wifi mở bằng địa chỉ máy. Giao việc cho Claude từ điện thoại qua Remote Control.
- Chọn thư mục footage → tự tạo bản nhẹ và ảnh lưới cảnh.
- Nút "Dựng video" → chạy bộ dựng, báo tiến độ, ra file MP4.
Xong khi: dựng được video từ footage trên máy Hào, điều khiển từ điện thoại.
Rủi ro: chưa thử trên macOS/M1; chưa biết RAM máy; dựng cần Chrome và FFmpeg.

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
| Chạy trên MacBook | 2/12 | Dựng từ footage trên Mac, bấm từ điện thoại |
| Âm thanh | sau khi có thư mục | Tiếng hiệu ứng, nhạc, giọng |

Mốc phụ thuộc lượng token mỗi ngày và thời gian Hào duyệt. Nếu thiếu thời gian, giữ Bước 1–2 (ra video tốt hơn ngay), lùi Bước 3–4.

## Đã chốt (12/11/2026)
1. Làm từ xa: phiên cloud cho kịch bản/mã/mẫu; MacBook cho dựng footage thật. Miễn phí.
2. Cắt ghép đầy đủ kiểu CapCut, làm theo đợt; chỉnh tinh tạm dùng CapCut/DaVinci miễn phí.
3. Mẫu: phân tích, chuyên gia, review, ảnh 3D mô phỏng, tối giản, sang trọng.

## Còn chờ
- Thư mục âm thanh của Hào.
- Logo, bộ màu thật.
- RAM của MacBook (để biết dựng 4K được nặng tới đâu).
