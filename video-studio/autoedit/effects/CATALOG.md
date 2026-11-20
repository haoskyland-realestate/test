# Danh mục hiệu ứng (người dùng chọn theo từng cảnh hoặc cụm cảnh)
Mỗi hiệu ứng có MÃ. Người dùng chọn mã cho từng cảnh/cụm cảnh ở Bước 5. Hình xem trước nằm ở trang "Bảng chọn hiệu ứng theo cảnh" (artifact). Hiệu ứng nào "chưa có mẫu" vẫn dựng được theo mô tả, nhưng phải chụp khung thử cho người dùng duyệt trước khi dựng cả video.

| Mã | Tên | Dùng khi | Dữ liệu cần | Thời lượng | Trạng thái |
|---|---|---|---|---|---|
| `chart_bars` | Biểu đồ cột | Số liệu theo năm, giá, tăng trưởng | 4–6 nhãn + số thật, cột nhấn, nhãn nhấn | 3–5 s | đã duyệt mẫu |
| `map_route` | Bản đồ + tuyến đường | Vị trí dự án, kết nối giao thông | Ảnh/KML bản đồ, điểm đến, nhãn | 2–10 s | đã duyệt mẫu |
| `amenity_grid` | Lưới tiện ích | Liệt kê tiện ích | Ảnh từng tiện ích, nhãn | 2–6 s | đã duyệt mẫu |
| `tree_diagram` | Nhánh cây | Liệt kê quyền lợi/tính năng đi kèm | Tiêu đề + 3–5 mục con (icon, nhãn, số liệu) | 4–6 s | đã duyệt |
| `note_board` | Bảng ghi chú / điều kiện | Liệt kê điều kiện, yêu cầu, ghi chú | Tiêu đề + 3–5 dòng | 3–6 s | đã duyệt |
| `glass_list` | Danh sách kính mờ | 3 lý do/giá trị/nguyên tắc, vẻ cao cấp | Tiêu đề 2 dòng + 3 mục (tên, dòng phụ, icon) | 4–6 s | đã duyệt |
| `logo_pop` | Icon pop + luồng sáng | Nhắc tên 2–4 sản phẩm/AI/thương hiệu | Tên + ảnh logo (người dùng cung cấp) + mốc nhắc | 3–6 s | đã duyệt |
| `growth_card` | Bảng tăng trưởng | Tốc độ/phần trăm tăng trưởng, "tăng gấp N lần" | Các mốc đường cong, giá trị đỉnh (số thật), nhãn, kỳ | 4–6 s | đã duyệt |
| `popup_notes` | Ảnh có chú thích | Giải thích bằng ảnh | 1 ảnh + 2–3 chú thích (chính + phụ) | 3–5 s | đã duyệt mẫu |
| `photo_cards` | Thẻ ảnh lớn + chữ phụ | Diện tích, cảnh quan, số lượng | 1–3 ảnh + chữ phụ + số đếm | 3–6 s | đã duyệt mẫu |
| `typo` | Typography nhấn từ khóa | Cụm khóa, không có hình cụ thể | 1 cụm ≤ 5 từ; kiểu `typo_gold/fire/bronze/neon_orange/neon_blue` | 2–4 s | đã duyệt mẫu |
| `count_up` | Số đếm / số lớn | Nhấn con số (5, 35%, 0Đ) | Giá trị + đơn vị | 2–3 s | đã duyệt mẫu |
| `warning_stamp` | Cảnh báo | "Coi chừng", "sai lầm" | 1 câu ngắn | 2–4 s | đã duyệt |
| `connect_flow` | Kết nối A → B | "Tích hợp", "nằm sẵn trong" | Tên A, tên B, 2–4 dòng nội dung B | ~6 s | đã duyệt mẫu |
| `feature_card` | Thẻ "đỉnh nhất" | Nhấn một lợi thế | Tiêu đề + cụm nhấn | 3–4 s | mô tả, chưa có mẫu |
| `compare_cards` | So sánh hai thẻ | So sánh trước/sau, A/B | Hai nhóm thông tin | 3–5 s | đã duyệt |
| `screenshot_card` | Ảnh chụp trang web nổi | Nhắc một trang/công cụ thật | 1 ảnh chụp màn hình | 3–4 s | mô tả, chưa có mẫu |
| `product_badge` | Sản phẩm + huy hiệu | Giới thiệu gói, tên, giá | Tên, logo, huy hiệu | 3–4 s | mô tả, chưa có mẫu |
| `metaphor_card` | Hình ẩn dụ | Câu so sánh, ví von | Câu ẩn dụ + hình vẽ | 4–8 s | đã duyệt mẫu |
| `cinematic_break` | Cảnh điện ảnh toàn khung | Đỉnh cảm xúc, 1–2 lần/video | Không | 2–4 s | mô tả, chưa có mẫu |
| `outro_cta` | Kêu gọi hành động | Cuối video | Câu kêu gọi + nút | 2–5 s | đã duyệt mẫu |
| `speaker_only` | Chỉ người nói | Cho video "thở" | Không | tùy | mặc định |

Mô tả chi tiết cách hiện/motion của từng hiệu ứng nằm ở các mục tương ứng trong `CLAUDE.md` (mục "Quy ước chung đã chốt khi duyệt" + bảng "ý đang nói → hình hiện ra", `map_route`, `typo_*`, `photo_cards`, `amenity_grid`, `chart_bars`, `popup_notes`). Màu sắc và bố cục khung hình lấy từ preset đã chọn.

## Gom cảnh
Nhiều cảnh liền nhau cùng một mã = MỘT cụm hiệu ứng liên tục. Ví dụ "Cảnh 1–3: `chart_bars`" nghĩa là dựng một biểu đồ kéo dài qua 3 cảnh, các cột/mục hiện theo nhịp lời nói qua từng cảnh. Không dựng ba biểu đồ riêng.
