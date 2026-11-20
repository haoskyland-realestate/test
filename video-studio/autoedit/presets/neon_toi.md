# Preset C: `neon_toi` (Neon Tối · đồ họa toàn khung)
Hợp với: video công nghệ, AI, tin nóng, nhịp nhanh; muốn đồ họa là nhân vật chính, người nói là phụ. Không cần tách nền.

## Màu sắc
- Nền cảnh: `#0d0605`, có vệt sáng cam đỏ mờ ở góc (`rgba(255,90,40,.35)` góc trên phải, `rgba(255,150,40,.25)` góc dưới trái).
- Gradient nhấn: `#ffb347` → `#ff3d2e` (135°). Màu viền/glow: `#ff7a45`.
- Chữ: trắng ấm `#fff2ea`. Từ khóa: gradient lửa `#ffc15a` → `#ff8a2b` → `#ff2d20` kèm glow cam (`drop-shadow 2 cqw`).
- Thẻ: kính mờ (nền trắng 7%, blur 8 px), viền neon cam mảnh .35 cqw, bo góc lớn 4 cqw, glow ngoài.
- Icon: trong khung vuông bo góc có nền gradient nhấn.
- Phông: theo ba vai phông ở mục 8 của `CLAUDE.md` (OAI Showtilla, BT Danta), nhúng bằng @font-face cục bộ.
- Vùng an toàn: theo CLAUDE.md mục 4 (trên 15%, dưới 25%, hai bên 10%); vòng tròn người nói ở góc trên là video nên được phép nằm trong vùng trên, chữ thì không.

## Bố cục (1080×1920)
- Đồ họa chiếm toàn khung, nội dung đặt từ ~42 cqw xuống tới ~128 cqw.
- Người nói thu nhỏ thành vòng tròn 30 cqw ở góc trên phải (top 6, right 6), viền cam, glow đỏ cam (`speaker_pip`). Cảnh nhấn cảm xúc có thể cho người nói toàn khung kèm hình nổi.
- Phụ đề: ĐÃ GỠ khỏi skill, chưa vẽ phụ đề. Kiểu phụ đề mới do người dùng cung cấp sau (xem mục 4 'Phụ đề').
- Cảnh cuối: nền đen quầng lửa, số lớn kem và nút gradient cam đỏ.

## Motion
Glow neon, thẻ kính trượt vào 0.3–0.45 giây, chữ gradient lửa, nhịp nhanh hơn một chút so với preset A và B.

## Kịch bản mẫu 30 giây (6 cảnh, mỗi cảnh ~5 giây, dùng làm khuôn cho cảnh tương ứng)
| Mốc | Cảnh | Hình hiện ra | Motion |
|---|---|---|---|
| 0–5 | Hook cảnh báo | Thẻ kính viền neon: tiêu đề, chữ viết tay, số đếm lửa, 5 nhãn | Thẻ trượt vào kèm glow, số đếm bước 0.26 giây |
| 5–10 | Liệt kê tính năng | Các dòng thẻ kính viền neon có ô biểu tượng cam | Trượt lên lần lượt cách ~0.5 giây |
| 10–15 | Số liệu | `chart_bars` thẻ kính, cột gradient cam đỏ, cột cuối đỏ lửa phát sáng | Cột mọc lần lượt cách 0.25 giây |
| 15–20 | Ảnh chú thích | `popup_notes` ảnh trong thẻ kính, ghim cam + bong bóng trắng | Ghim rồi bong bóng bật theo từng ý |
| 20–25 | Nhấn từ khóa | Thẻ kính: chữ viết tay kem + từ khóa gradient lửa + ô mẫu | Ba dòng vào so le, glow |
| 25–30 | Chốt + kêu gọi | Nền đen quầng lửa, số lớn kem, nút gradient cam đỏ | Số hiện 0.5 giây, nút trượt lên sau 0.7 giây |

Quy tắc chung: hiệu ứng vào trễ không quá ~0.2 giây sau lời, vào 0.3–0.5 giây, không có hai hiệu ứng lớn cùng lúc. Ý nào không khớp cảnh nào thì dùng `typo_*` hoặc chỉ phụ đề.
