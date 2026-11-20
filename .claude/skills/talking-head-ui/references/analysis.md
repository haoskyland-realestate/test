# Phân tích 3 video mẫu (nguồn của style.json)

Cả 3 video: dọc 1080x1920, 29.97 fps, 25–50 s. Đo bằng tách khung 10 fps, dò cảnh cắt (ffmpeg scene) và đo màu điểm ảnh.

| | Video A (podcast, 25 s) | Video B (bất động sản, 28 s) | Video C (phim tài liệu, 50 s) |
|---|---|---|---|
| Preset rút ra | pop-accent | pop-accent | doc-calm |
| Khung người nói | 1 góc 0–20 s, cắt cận có chớp trắng ở 20 s | 1 góc 0–14.4 s | 1 góc 0–24.9 s, không zoom trôi |
| B-roll | không | montage 0.17 s/cảnh × 10 cảnh, đen 1.2 s, rồi 0.4–1.4 s/cảnh | điện ảnh 1.3–7 s/cảnh, giờ vàng |
| Phụ đề | 1 từ/lần, sans hình học đậm trắng, giữa ngực | như A | 1 từ/lần, sans mảnh trắng, giữa ngực |
| Khối nhấn | 7 khối/25 s, hồng + trắng | 4 khối/14 s, có chữ khổng lồ sau đầu | 4 khối/25 s, trắng nghiêng, nằm sau tóc |

## Nhịp dựng
- Người nói giữ một khung rất lâu (14–25 s). Chuyển động đến từ chữ, không từ camera.
- Phụ đề đổi theo từng từ (0.25–0.45 s), cắt cứng, không hiệu ứng. Khi khối nhấn hiện, phụ đề tắt (bản pop).
- Khối nhấn dựng dần theo lời: mỗi dòng hiện đúng lúc được nói, giữ 1.5–3 s rồi thoát cả khối.
- Cắt cận 1.2–1.3x kèm chớp trắng khoảng 0.25 s để đánh dấu câu chốt.
- B-roll bản pop: montage cực nhanh, rồi màn đen ~1.2 s như nhịp nín thở, rồi b-roll kể chuyện. Phụ đề tắt khi b-roll.
- B-roll bản doc: chậm, ánh sáng đẹp, phụ đề vẫn chạy.

## Typography
- Trộn 3–4 vai trò trong một khối, khoảng dòng âm (dòng sau đè nhẹ dòng trước):
  - nối mảnh: sans weight 300 (bản doc: Helvetica Neue UltraLight Italic) — "say is...", "it was", "I think";
  - đậm: sans 800 — "how to keep", "for my";
  - hero: sans 900 rất to, màu nhấn — "listings", "learning", "ONE";
  - script: serif đậm nghiêng (kiểu Playfair Display Black Italic), màu nhấn, xoay ~-3° — "wanna", "unapologetically", "promises";
  - khổng lồ: serif đậm nghiêng viết hoa, rộng gần cả khung, nằm sau đầu — "SOLELY".
- Thay thế có tiếng Việt: Montserrat (sans hình học), Inter (thay Helvetica Neue, có italic 200–900), Playfair Display.
- Màu nhấn đo được: #F800F8–#F800D8 (magenta), gradient sáng ở trên, có quầng sáng hồng (glow). Chữ trắng có bóng mờ nhẹ.

## Hiệu ứng chữ
- Bản pop "smear": chữ lao ngang vào với vệt mờ chuyển động, khung đầu chỉ là một vệt màu nhấn bị nhoè ngang, ổn định sau ~0.2 s. Thoát cũng bằng vệt nhoè.
- Từ script/hero nở và xoay rất chậm trong lúc giữ.
- Bản doc "drift": chữ hiện mờ dần + nhoè → nét + trôi lên rất nhẹ (~0.45 s), độ mờ ~90%. Thoát bằng nhoè + mờ.
- Chữ nằm sau người: chữ đặt giữa nền và lớp người đã tách nền; đầu/tóc che 30–55% chữ.

## Màu hình
- Bản pop: tương phản và bão hoà cao, ấm nhẹ.
- Bản doc: tương phản thấp, ấm, hơi giảm bão hoà, vignette nhẹ.
