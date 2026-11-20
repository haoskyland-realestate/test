# Preset A: `xanh_gradient` (Xanh Gradient · đầu nhô khỏi khung)
Hợp với: video hướng dẫn, kiến thức, công cụ, bán hàng nhẹ nhàng; cần cảm giác hiện đại, sạch, dễ đọc.
Yêu cầu kỹ thuật: tách người khỏi nền (rembg), chạy chậm hơn trên máy không có GPU.
Mã nguồn giao diện đã duyệt: `reference/storyboard_style_reference.html` (bám theo lớp CSS và thành phần trong đó).

## Phong cách, bố cục, tách người

## Bảng màu
- Nền cảnh: gradient dọc #e9f7ff → #cbe7ff → #8ec4ff, thêm quầng sáng trắng góc trên trái và quầng cyan góc phải. Cảnh cuối (câu chốt) dùng nền xanh đậm #123a8f → #0a2563 → #081a47.
- Thẻ trắng (bo góc ~4 cqw, bóng xanh nhạt), thẻ xanh đậm #17387a → #0a1b48 (để đổi nhịp), viền nét đứt xanh cho thẻ "nhấn".
- Chữ gradient: #46d6ff → #2b73ff → #1a3fd0. Chữ trên nền tối: #ffffff → #a9e4ff → #5cc8ff. Chữ thường màu navy #0b1f4d. Chữ viết tay (OAI Showtilla) màu #1f5eff, nét viền cùng màu .3 cqw để dày lên.
- Nút, ô biểu tượng, cột nhấn: gradient #46d6ff → #2b5fff. Nhãn "pill" navy #14306b → #091a45, chữ trắng, số thứ tự màu #5cc8ff.
- Giữ nguyên phông: BT Danta (chữ in), OAI Showtilla (viết tay), và quy tắc nới khung chữ gradient để không mất dấu.

## Bố cục mọi cảnh (1080×1920, 1 cqw = 10.8 px)
- Phía trên (6 → ~92 cqw): nhãn pill ở đỉnh, dưới là một thẻ nội dung (left/right 6 cqw). Cảnh cuối: số lớn ở giữa trên nền xanh đậm.
- Phía dưới: khung người nói rộng 88 cqw, căn giữa (left 6), cao 88 cqw, đáy sát mép dưới video. Khung bo góc 5 cqw ở hai góc trên, viền trắng .9 cqw, phát sáng xanh. Mép trên của khung nằm thấp hơn đỉnh đầu khoảng 9 cqw: ĐẦU VÀ TÓC NHÔ LÊN KHỎI KHUNG, phần thân nằm trong khung.
- Phụ đề: ĐÃ GỠ khỏi skill, chưa vẽ phụ đề. Kiểu phụ đề mới do người dùng cung cấp sau (xem mục 4 'Phụ đề').
- Mỗi cảnh có thẻ nội dung phía trên theo mẫu: cảnh báo/typography/kêu gọi = thẻ trắng viền nét đứt; tiện ích = thẻ tiêu đề xanh đậm + cây liên kết các dòng có ô biểu tượng; biểu đồ, bản đồ, pop-up = thẻ trắng chứa nội dung; nhắc lại cảnh báo = thẻ xanh đậm; ẩn dụ = thẻ trắng có hình minh họa nét xanh.

## Tách người khỏi nền (bắt buộc cho khung người nói)
- Mục đích: lớp "đầu nhô" là chính người nói đã tách nền, đặt chồng lên đúng vị trí của khung có nền thật. Trong khung hai lớp trùng khớp, chỉ phần tóc/đầu vượt lên trên mép khung là khác.
- Cách làm trên máy này: dùng `rembg` với mô hình `u2net_human_seg` (cài bằng `pip install rembg onnxruntime`, mô hình tự tải về lần đầu). Chạy trên từng khung hình đã thu nhỏ (khoảng 540×960 rồi phóng lại nếu máy chậm), lưu lớp alpha, sau đó làm mịn viền (guided filter hoặc làm mờ nhẹ 1–2 px).
- Làm sạch: chỉ giữ vùng lớn nhất (người nói), bỏ mảng rác (ví dụ mảng gạch trên đầu); nếu khung nào còn rác thì dùng khung gần kề để thay. Khi tách theo video, làm mượt alpha giữa các khung hình liên tiếp để viền tóc không nhấp nháy.
- Cắt khung người nói gần vuông: rộng bằng toàn chiều ngang video đã xoay (1080), cao 1080, bắt đầu cách đỉnh đầu khoảng 30 px (đầu nhô khỏi khung rõ hơn), để thấy đủ đỉnh tóc đến cằm. Người nói chiếm rất lớn khung hình gốc (đầu cao ~45% chiều cao), nên không dùng khung dẹt.
- Kiểm tra bắt buộc: mỗi loại cảnh chụp một khung để người dùng duyệt (thấy đủ đỉnh tóc và cằm, viền tóc sạch, không còn mảng nền) trước khi render đầy đủ.

## Lưu ý khi dựng thật
- Tách người cho cả video sẽ chậm trên máy không có GPU. Cho người dùng biết thời gian ước tính, chạy ở độ phân giải thấp rồi phóng lại, và chỉ tách một lần rồi dùng chung cho mọi cảnh.
- Ảnh/số liệu chưa có: dựng khung giữ chỗ có nhãn "SỐ MẪU", "ẢNH CẦN CHÈN" để duyệt. Bản cuối không được còn nhãn này.

## Kịch bản mẫu 30 giây (6 cảnh, mỗi cảnh ~5 giây, dùng làm khuôn cho cảnh tương ứng)
| Mốc | Cảnh | Hình hiện ra | Motion |
|---|---|---|---|
| 0–5 | Hook cảnh báo | Thẻ trắng nét đứt: tiêu đề, chữ viết tay, số đếm 0→5, 5 nhãn | Tiêu đề trượt lên, dòng so le 0.4 giây, số đếm bước 0.26 giây |
| 5–10 | Liệt kê tính năng | Tiêu đề pill + các dòng thẻ trắng có ô biểu tượng và dấu tích | Mỗi dòng trượt lên đúng lúc nói, cách ~0.5 giây |
| 10–15 | Số liệu | `chart_bars` thẻ trắng, cột xanh, cột cuối đậm + nhãn | Cột mọc lần lượt cách 0.25 giây, nhãn nhấn hiện cuối |
| 15–20 | Ảnh chú thích | `popup_notes` ảnh trong thẻ trắng, ghim xanh + bong bóng | Ghim bật 0.3 giây rồi bong bóng bật 0.4 giây theo từng ý |
| 20–25 | Nhấn từ khóa | Thẻ nét đứt: chữ viết tay + từ khóa gradient + hàng ô mẫu chữ | Ba dòng vào so le, hàng ô mẫu hiện lần lượt |
| 25–30 | Chốt + kêu gọi | Nền xanh đậm, số lớn + ký hiệu nhỏ, nút gradient | Số lớn hiện 0.5 giây, nút trượt lên sau 0.7 giây |

Quy tắc chung: hiệu ứng vào trễ không quá ~0.2 giây sau lời, vào 0.3–0.5 giây, không có hai hiệu ứng lớn cùng lúc. Ý nào không khớp cảnh nào thì dùng `typo_*` hoặc chỉ phụ đề.
