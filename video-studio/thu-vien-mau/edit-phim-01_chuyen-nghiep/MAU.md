# Mẫu edit video 1 chuyên nghiệp (`edit-phim-01`)

Loại: **edit phim**. Lập 12/11/2026 từ video mẫu Hào gửi: review một dự án căn hộ, TikTok dọc 576×1024, 30 khung/giây, 55,5 giây.
Video gốc là của người khác: chỉ lưu bản phân tích này, **không** lưu video, logo hay hình của họ vào repo.

Cách phân tích: xem khung hình mỗi 0,5 giây và mỗi 0,1 giây quanh chỗ chuyển cảnh; dò điểm đổi cảnh tự động (FFmpeg `scdet`); vẽ phổ âm, đo năng lượng theo dải tần và điểm khởi âm. Âm hiệu ứng trộn chung với giọng và nhạc nên phần âm thanh có độ chắc **trung bình**: thời điểm thì chắc, loại âm là suy từ hình dạng phổ.

---

## 1. Bố cục khung hình

| Lớp | Vị trí | Đặc điểm |
|---|---|---|
| Logo | 2 góc trên (trái, phải) | Nhỏ, đứng yên suốt video (logo kênh + logo đơn vị phân phối) |
| **Chữ lớn (tag)** | Giữa, khoảng 25–40% chiều cao | 3 tầng: nhãn nhỏ trên ("chỉ từ"), **chữ rất lớn** ("2.4 TỶ", "QL 13", "6 TRIỆU"), dòng nhỏ dưới ("cho căn hộ 60–80m2"). Trắng, đậm, có độ nổi 3D (bóng xám chồng lớp), đổ bóng mềm |
| Chữ nằm sau người | Cảnh có người dẫn | Ở "QL 13", người dẫn đi **trước** chữ (tách người khỏi nền) |
| Phụ đề | Dưới, khoảng 80% chiều cao | Chữ trắng nhỏ, nền đen mờ bo góc, chạy theo lời nói, mỗi lần 4–8 từ |
| Khẩu hiệu | Dưới cùng | Chữ có chân nghiêng ("Full Circle Living") trượt ngang chậm trên cảnh phối cảnh |
| Ảnh giữa nền mờ | Cảnh tiện ích | Ảnh ngang đặt giữa khung dọc, trên/dưới là ảnh phóng to làm mờ |

## 2. Nhịp dựng

- **Khoảng 20 cảnh trong 55 giây**, trung bình 2,7 giây/cảnh (đếm tay từ ảnh lưới, sai số ±2 cảnh). Cảnh nhanh nhất khoảng 0,7 giây (chuỗi tiện ích lân cận), dài nhất khoảng 9 giây (tháp đêm, chữ đổi liên tục bên trên).
- **Chữ lớn đổi khoảng mỗi 1,5–2,5 giây**, trùng với từ khóa trong lời nói. Khoảng 27 lần chữ lớn trong 55 giây.
- Thứ tự nội dung: giá + diện tích (hook 0–3 giây) → vị trí, giao thông (Metro, QL13, 30 phút về TP) → tiện ích quanh (Aeon, Mega Market, VSIP, chợ) → tiện ích nội khu theo tầng (tầng 9, tầng 21, hồ bơi, BBQ, phòng họp) → căn hộ (100% ban công, phòng ngủ có cửa sổ) → nhắc lại giá + lời kêu gọi.
- Kết bằng **nhắc lại con số mở đầu** ("chỉ từ 2.4 TỶ") rồi lời kêu gọi nói miệng; không có cảnh kết thương hiệu riêng.

## 3. Chuyển cảnh (đã đối chiếu từng khung 0,1 giây)

| Giây | Kiểu | Mô tả | Trong thư viện của mình |
|---|---|---|---|
| 6,9 | Phóng mờ | Hình lao vào tâm, nhòe chuyển động toả tròn, loé sáng nhẹ ở giữa, ~0,3 s | `gl-CrossZoom` |
| 8,3 | Xoay mờ | Nhòe xoáy quanh tâm sang cảnh sa bàn, ~0,3 s | `gl-WhipSpin` |
| 12,7–13,3 | Cháy sáng (light leak) | Loé cam → hồng cháy sáng → cảnh mới, ~0,6 s | `gl-FilmBurn` |
| 16,4 / 17,3 / 18,0 / 20,0 / 20,9 / 22,9 | Cắt thẳng | Chuỗi tiện ích lân cận, mỗi cảnh ~1 s | `cut` |
| 26,3–26,8 | Loé + cháy | Loé trắng vàng, vệt đỏ quét ngang, chữ "TẦNG 9" hiện ngay sau | `gl-FilmBurn` / `gl-Overexposure` |
| 32,7–33,2 | Loé + cháy | Như trên, sang tháp đêm "TẦNG 21" | `gl-FilmBurn` |
| 42,1 | Nhòe hướng | Nhòe dọc nhanh sang nội thất | `gl-CrossZoom` (gần đúng) |
| Còn lại | Cắt thẳng | | `cut` |

**Quy luật:** khoảng 70% là cắt thẳng; chuyển cảnh mạnh đặt ở chỗ **đổi chương** (vị trí → tiện ích ngoài → tiện ích trong → căn hộ). Chuyển cảnh mạnh luôn ngắn (0,3–0,6 s).

## 4. Hiệu ứng chữ

- **Chữ lớn vào:** to hơn và mờ nhòe → thu về đúng cỡ và rõ trong khoảng 0,3–0,4 s (`zoom-blur`, khối `title3d`).
- Nhãn nhỏ trên hiện trước khoảng 0,1–0,2 s; dòng nhỏ dưới hiện sau khoảng 0,3–0,5 s.
- **Chữ ra:** mờ nhòe và tan, không trượt.
- Có lúc chữ hiện **nửa trong suốt** đè lên hình (hiệu ứng kính) khi chuyển cảnh đi qua.

## 5. Âm thanh hiệu ứng (sound effect)

| Loại âm đo được | Khi nào | Đặc điểm phổ | File trong kho |
|---|---|---|---|
| Vụt-bụp ngắn | Mỗi lần chữ lớn hiện (≈0,9 · 2,5 · 8,9 · 11,0 · 12,1 · 14,1 · 19,6 · 20,7 s…) | Vệt dọc 0,1–0,15 s, mạnh ở 5–11 kHz | `chu_swish-pop_01` |
| Ting cao | Khi con số chốt ("6 TRIỆU", "300M") | Vạch ngang 5,2 kHz và 6,2 kHz, dài 0,3–0,7 s | `ting_don_01`, `ting_kep_01` |
| Gió vút | Phóng mờ, xoay mờ (6,7–7,5 s) | Mảng nhiễu rộng, dâng rồi tắt | `whoosh_zoom_01`, `whoosh_xoay_01` |
| Đập trầm | Một số cú chuyển và chữ số (8,5 · 16,9 · 19,4 · 24,2 · 32,5 s) | Năng lượng dưới 120 Hz vọt lên ngắn | `impact_tram_01`, `impact_hit_01` |
| Lấp lánh | Cảnh căn hộ cuối (51–54 s) | Nhiều vạch ting ngắn 3–9 kHz | `ting_lap-lanh_01` |
| Ding kết | Cuối video (≈54,7 s) | Vạch dài 3,6 kHz | `ting_ket_01` |
| **Khoảng lặng trước chuyển cảnh** | 12,85 · 26,2 · 32,6 s | Mọi tần số tắt 0,15–0,2 s ngay trước cú loé | **Chưa làm** (xem mục 7) |

Nhạc nền: có, đều suốt video, nhỏ dưới giọng. Theo Hào dặn, mẫu này **chưa dùng nhạc** (`audio.music: null`); thêm nhạc khi có kho nhạc.

## 6. Mẫu này làm gì khi áp vào một dự án

Áp trong app: tab **Thương hiệu → Mẫu edit → Áp mẫu** (hoàn tác được). Hoặc: `python3 scripts/ap_mau.py projects/<tên> edit-phim-01`.

1. Phong cách `edit-phim`: chữ Montserrat đậm trắng nổi 3D, chữ vào kiểu `zoom-blur`, màu `tuoi-dam`, phụ đề nhỏ nền tối.
2. Chuyển cảnh theo chu kỳ 10 chỗ nối: `cut, CrossZoom, cut, WhipSpin, cut, cut, FilmBurn, cut, cut, Overexposure` (độ dài 0,35–0,6 s). Sau khi áp, nên **đổi tay cho chuyển cảnh mạnh rơi đúng chỗ đổi chương**.
3. Rải hiệu ứng âm (`auto: true`): vút/cháy ở giữa mỗi chuyển cảnh mạnh, chũm chọe ngược dẫn vào cú cháy sáng, vụt-bụp khi chữ lớn hiện, ting khi chữ lớn có con số, đập trầm cho hook, ding cho cảnh kết. Âm lượng theo nhóm trong `mau.json`.
4. Tắt nhạc tổng hợp và tiếng vút cũ của nhạc tổng hợp; giữ nguyên giọng gốc.

Muốn chữ lớn kiểu video mẫu: thêm khối chữ kiểu **`title3d`** (ô "Chữ lớn" bắt buộc, "Nhãn trên", "Dòng dưới" tuỳ chọn).

## 7. Chưa làm được (so với video mẫu)

| Thiếu | Cần gì |
|---|---|
| Chữ nằm sau người | Mô hình tách người khỏi nền (ví dụ MediaPipe hoặc rembg) chạy trên từng khung; chưa thêm |
| Khoảng lặng trước chuyển cảnh | Hạ giọng/nhạc về 0 trong 0,15 s trước cú chuyển; dễ cắt mất chữ cuối câu nên cần chỉnh tay, chưa làm |
| Khẩu hiệu chữ có chân trượt ngang | Khối chữ mới; chưa làm |
| Ảnh giữa nền mờ cho ảnh ngang | Đã có cho đoạn video (`fit: blur`); ảnh tĩnh chưa có |
| Logo 2 góc | Chờ logo thật của Hào (`video-studio/brand/`) |
| Âm hiệu ứng | Âm tự tổng hợp (tạo bằng `scripts/tao_sfx.py`), mức khá; có kho effect thật thì thay file cùng tên |

**Chưa dựng thử** mẫu này với footage của Hào (theo dặn 12/11). Đã thử: kiểm định dạng, áp mẫu vào timeline giả, trộn âm hiệu ứng (đo đúng mốc).
