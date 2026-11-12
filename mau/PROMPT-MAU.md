# Câu lệnh mẫu cho từng AI

Chép nguyên khối, thay phần `<...>`. Chọn AI theo `docs/01-he-thong/AI-NAO-VIEC-NAO.md`.
Số thứ tự đi theo `docs/02-quy-trinh/QUY-TRINH-MOT-VIDEO.md`.

## Khối "quy tắc nội dung" (dán kèm khi nhờ AI ngoài repo: ChatGPT, Gemini)
```
Quy tắc: tiếng Việt mộc mạc, chân thành, ít chữ, có số cụ thể. Hook rõ trong 3 giây đầu.
Xưng "em" với khách lớn tuổi, "tôi" khi phân tích kiểu chuyên gia. Rất ít emoji.
Luôn nêu cả lợi ích và rủi ro. Số liệu chưa có nguồn thì để [...], không tự điền.
Không dùng: cơ hội vàng, sinh lời chắc chắn, cam kết lợi nhuận, cháy hàng, chốt ngay kẻo lỡ, sốt đất, x2 tài sản.
Không tạo khan hiếm giả, không hứa tăng giá.
Khách mục tiêu: nữ 35–55 tuổi, tài sản lớn, ở trung tâm và khu Đông TP.HCM, quan tâm dòng tiền.
```

## 1. Chọn góc nội dung: Claude
```
Tuần này làm 1 video <TikTok/YouTube> về <Vinhomes Hóc Môn/Cần Giờ/chung>.
Kết quả tuần trước: <dán KET-QUA.md hoặc "chưa có">.
Đề xuất 3 góc dòng tiền cho nhóm khách trong CLAUDE.md. Mỗi góc: câu hỏi của khách, một ý cần nhớ, số liệu cần có.
Khuyến nghị 1 góc và lý do. Sau khi tôi chọn, điền BRIEF.md theo mẫu mau/du-an-video/BRIEF.md.
```

## 2. Đọc hồ sơ dự án: NotebookLM (đã nạp tài liệu gốc vào sổ của dự án)
```
Liệt kê mọi con số về giá, diện tích, chính sách thanh toán, hỗ trợ lãi suất, tiến độ, pháp lý trong các nguồn.
Mỗi dòng: con số | tên nguồn | trang | ngày của tài liệu.
Chỗ nào các nguồn mâu thuẫn thì ghi rõ. Không suy đoán ngoài tài liệu.
```
Chép kết quả vào `NGUON-SO-LIEU.md`, Hào đánh dấu "đã xác nhận" từng dòng.

## 3. Tìm tin mới: Claude (tìm web)
```
Tìm tin về <lãi suất vay mua nhà / hạ tầng gần dự án X / ...> từ <tháng/năm> đến nay.
Chỉ lấy nguồn gốc (cơ quan nhà nước, ngân hàng, chủ đầu tư) hoặc báo uy tín. Mỗi tin: nội dung, đường dẫn, ngày đăng.
Tách rõ: thông tin chính thức / dự kiến / nhận định.
```

## 4. Viết kịch bản: Claude
```
Đọc BRIEF.md và NGUON-SO-LIEU.md của video <tên>.
Viết KICH-BAN.md theo mẫu mau/du-an-video/KICH-BAN.md, dài <số> giây, theo quy tắc nội dung trong CLAUDE.md.
Số chưa có trong NGUON-SO-LIEU.md để [...]. Đưa 2 phương án hook, khuyến nghị 1.
```

## 5. Kiểm chéo kịch bản: ChatGPT hoặc Gemini
```
<dán khối quy tắc nội dung>
Đây là kịch bản: <dán KICH-BAN.md>
Đóng vai một chị 45 tuổi có 30 tỷ, đang cân nhắc mua để cho thuê.
Chỉ ra 3 chỗ chị thấy khó tin, khó hiểu hoặc giống quảng cáo. Không viết lại kịch bản.
```

## 6. Storyboard: Claude Code (PC hoặc phiên cloud)
```
Lập storyboard cho video <tên> từ thư mục footage <đường dẫn trên PC hoặc link Drive>, theo KICH-BAN.md.
Dùng skill lap-storyboard. Dừng để tôi duyệt, chưa dựng.
```

## 7. Sửa timeline bằng lời: Claude Code (hoặc nút "Nhờ AI sửa" trong app, chép câu lệnh nó tạo)
```
Sửa video <tên>: <ví dụ: đổi chữ cảnh 3 thành "...", thêm zoom 7% ở giây 12, đổi chuyển cảnh 2 thành gl-CrossZoom>.
Chạy python3 scripts/test_timeline.py trong video-studio rồi báo đã đổi gì.
```

## 8. Nghiệm thu: Claude Code
```
Nghiệm thu video <tên> bằng skill bao-cao-nghiem-thu. Ghi rõ mục nào chưa kiểm.
```

## 9. Đăng bài: Claude
```
Đọc KICH-BAN.md của <tên>. Soạn DANG-BAI.md: 3 phương án tiêu đề (dưới 60 ký tự), mô tả 2–3 câu có lời kêu gọi tự nhiên, 3–5 hashtag, chữ cho ảnh bìa (tối đa 6 chữ).
Không dùng từ cấm. Tôi sẽ tự đăng.
```

## 10. Ảnh bìa: Canva (qua Claude) hoặc ChatGPT
```
Ảnh bìa <9:16 hoặc 16:9>, nền là khung hình <mô tả/đính kèm>, chữ lớn "<chữ ảnh bìa>", màu thương hiệu <...>.
Ít chữ, đọc được trên điện thoại. Không thêm logo chủ đầu tư.
```
Ảnh minh hoạ do AI vẽ (không phải ảnh dự án thật) phải có chữ "ảnh minh hoạ".

## 11. Tổng kết tuần: Claude
```
Đây là KET-QUA.md của các video tuần này: <dán>.
Video nào có tin nhắn đúng nhóm khách? Vì sao có thể như vậy (nêu rõ đây là giả thuyết)?
Đề xuất giữ gì, đổi gì cho tuần sau. Ngắn gọn.
```
