# Preset B: `cam_kem` (Cam Đất · hai khung)
Hợp với: video bán hàng, bất động sản, khuyến mãi; cần cảm giác ấm, mạnh. Không cần tách nền nên dựng nhanh, ổn định, hợp máy yếu.

## Màu sắc
- Nền cảnh: gradient cam đất `#e0683c` → `#bf4a24`, quầng sáng `#e9774a` góc trên trái, vân sọc mảnh trắng 3.5% (172°).
- Thẻ: nền tối `#2a1710` → `#120a07`, viền vàng `#ffc27a` .6 cqw, bo góc 3 cqw, bóng cam `rgba(255,170,70,.5)`.
- Chữ: kem `#fff2ea`. Từ khóa: gradient `#ffe6cb` → `#ffa55f` → `#f58a3f`, đổ bóng khối `#b9481b` + bóng mềm. Nghiêng giả (BT Danta không có bản nghiêng thật), bỏ nghiêng nếu xấu.
- Pill: nền `#ffd9a8` → `#ffb066`, chữ `#3a1608`. Nhấn: cam `#f0701f`, cột nhấn `#ff7a45` → `#c93a12`.
- Phông: BT Danta (chữ in), OAI Showtilla (viết tay), theo mục "Phông chữ" chung.

## Bố cục (1080×1920, 1 cqw = 10.8 px)
- Phía trên: pill tiêu đề ở đỉnh, thẻ tối nội dung (left/right 6 cqw, top ~19, cao ~70).
- Phía dưới: khung người nói chữ nhật gần vuông, rộng 88 cqw, cao ~80 cqw, bo góc 4 cqw hai góc trên, viền vàng `#ffc27a` .8 cqw, glow cam. Cắt từ video gốc tỉ lệ ~0.905 (bắt đầu cách đỉnh khung hình ~7% chiều cao), phải thấy đủ đỉnh tóc và cằm, không dùng khung dẹt.
- Phụ đề: ĐÃ GỠ khỏi skill, chưa vẽ phụ đề. Kiểu phụ đề mới do người dùng cung cấp sau (xem mục 4 'Phụ đề').
- Cảnh cuối: nền nâu đen `#120a07`, số lớn + nút cam.
- Cảnh minh họa phụ (tiện ích, biểu đồ, bản đồ, ảnh chú thích) dùng khung người nói nhỏ ở góc trên trái (rộng 44, cao 50 cqw) khi nội dung cần chiếm phần lớn khung.

## Motion
Như quy tắc motion chung; nhấn bằng bóng cam và viền vàng; chữ khóa có đổ bóng khối.

## Kịch bản mẫu 30 giây (6 cảnh, mỗi cảnh ~5 giây, dùng làm khuôn cho cảnh tương ứng)
| Mốc | Cảnh | Hình hiện ra | Motion |
|---|---|---|---|
| 0–5 | Hook cảnh báo | Thẻ tối viền vàng: tiêu đề, chữ viết tay, số đếm 0→5, 5 nhãn | Như preset A nhưng bóng cam, chữ nghiêng đổ bóng khối |
| 5–10 | Liệt kê tính năng | Các dòng thẻ tối viền vàng có ô biểu tượng cam | Trượt lên lần lượt cách ~0.5 giây |
| 10–15 | Số liệu | `chart_bars` thẻ tối, cột cam, cột cuối đỏ cam + nhãn | Cột mọc lần lượt cách 0.25 giây |
| 15–20 | Ảnh chú thích | `popup_notes` ảnh trong thẻ tối, ghim cam + bong bóng kem | Ghim rồi bong bóng bật theo từng ý |
| 20–25 | Nhấn từ khóa | Thẻ tối: chữ viết tay trắng + từ khóa gradient vàng/cam + ô mẫu | Ba dòng vào so le |
| 25–30 | Chốt + kêu gọi | Nền nâu đen, số lớn kem, nút cam | Số hiện 0.5 giây, nút trượt lên sau 0.7 giây |

Quy tắc chung: hiệu ứng vào trễ không quá ~0.2 giây sau lời, vào 0.3–0.5 giây, không có hai hiệu ứng lớn cùng lúc. Ý nào không khớp cảnh nào thì dùng `typo_*` hoặc chỉ phụ đề.
