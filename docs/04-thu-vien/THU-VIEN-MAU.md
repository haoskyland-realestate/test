# Thư viện mẫu video Hào Sky Land: đặc tả chi tiết

Viết theo cách một biên tập viên dùng After Effects/Premiere nhiều năm sẽ tổ chức một bộ mẫu: **hệ thống thiết kế chung** trước, rồi **bộ thành phần** (chữ, chuyển cảnh, đồ họa), rồi **mẫu bố cục** cho từng kiểu nội dung. Mẫu nào cũng ghép từ cùng một bộ thành phần, nên đổi phong cách (sang trọng / tối giản) chỉ là đổi một file cấu hình.

Ký hiệu trạng thái: **[có]** đã chạy trong video test 89s · **[mới]** chưa làm.

---

## Phần 1. Hệ thống thiết kế chung

### 1.1 Khung hình và vùng an toàn
TikTok/Reels 9:16, 1080×1920:
- Trên cùng 220px: tránh (tên tài khoản, thanh tìm kiếm của app).
- Dưới cùng 420px: tránh (mô tả, nút).
- Bên phải 140px: tránh (nút tim, bình luận, chia sẻ).
- Chữ chính nằm trong vùng giữa: x 72–940, y 260–1500. **[có một phần]**: video test đặt chữ ở đáy 300px, cần nâng lên trên vùng mô tả.

YouTube 16:9, 1920×1080: vùng an toàn chữ 90% khung, tiêu đề cách mép 96px.

### 1.2 Chữ
- Tối đa 2 họ chữ cho mỗi video: **chữ tiêu đề** + **chữ nội dung**.
  - Hiện đại: Be Vietnam Pro (đậm 800 cho tiêu đề, 400–600 cho nội dung). **[có]**
  - Sang trọng: chữ có chân cho tiêu đề (ví dụ Playfair Display hoặc Cormorant Garamond) + Be Vietnam Pro cho nội dung. **[mới]**, cần kiểm tra font hiển thị đủ dấu tiếng Việt trước khi dùng.
- Cỡ chữ (khung 1080 rộng): tiêu đề lớn 96 · tiêu đề 72 · nội dung 54 · phụ đề 46 · nhãn 28.
- Mỗi dòng 18–22 ký tự trên khung dọc, tối đa 2–3 dòng mỗi nhịp.
- Thời gian đọc: tối thiểu 0,3 giây mỗi từ + 1 giây. Máy kiểm tra tự động, cảnh báo nhịp chữ quá ngắn. **[mới]**
- Bóng chữ mềm hoặc nền tối dần thay vì viền dày. **[có]**

### 1.3 Màu: 3 bộ phong cách
| Bộ | Nền/tối | Nhấn | Chữ | Chỉnh màu footage |
|---|---|---|---|---|
| **Sang trọng** | xanh navy #0B1B2B | vàng champagne #D4A64A | kem #F4EFE6 | ấm nhẹ, giảm bão hòa, tương phản mềm, hạt phim nhẹ |
| **Tối giản** | trắng #FAFAF8 hoặc đen #111 | 1 màu nhấn duy nhất | xám đậm #222 | trung tính, sáng, ít tương phản |
| **Ấm tự nhiên** | be #EFE7DA | xanh rêu #5B6B4E | nâu #3A2E25 | ấm, xanh lá dịu |

Khi có bộ màu thật của Hào, thay vào bộ "Sang trọng" làm mặc định. Mỗi bộ là một file `styles/<tên>.json`.

### 1.4 Chuyển động
- Vào: nhanh rồi chậm dần (expo.out), 0,4–0,7 giây. Ra: nhanh dần (power2.in), 0,3–0,4 giây. **[có]**
- So le giữa các từ 50–80ms. **[có]**
- Không quá 2 thứ chuyển động cùng lúc trên màn hình.
- Phong cách sang trọng: chậm hơn 30%, không nảy, không rung.
- Chuyển động nhanh thì thêm mờ chuyển động.

### 1.5 Nhịp dựng
- TikTok: hook dưới 2 giây; 5 giây đầu cắt cảnh mỗi 1,5–3 giây; sau đó mỗi cảnh 2,5–5 giây; cứ 7–10 giây có một "điểm ngắt" (đổi cỡ cảnh, chữ lớn, âm thanh nhấn).
- Video 130 giây: khoảng 30–45 cảnh. Video test 89 giây mới có 9 cảnh, mỗi cảnh 9,2 giây, **quá chậm cho TikTok**, cần chia nhỏ.
- Ngữ pháp chuyển cảnh: 80% cắt thẳng; chỉ dùng chuyển cảnh nổi bật khi sang chương mới, tối đa một lần mỗi 10 giây.

### 1.6 Âm thanh (chờ thư mục của Hào)
- Độ lớn cuối cùng khoảng -14 LUFS (mức phổ biến cho mạng xã hội). Giọng rõ nhất; nhạc thấp hơn giọng 8–12 dB khi có giọng.
- Tiếng "vút" đặt sớm 2 khung hình trước điểm cắt; tiếng nhấn khi số liệu hiện; tiếng tăng dần dẫn vào hook.
- Mỗi tiếng/nhạc phải ghi rõ nguồn và giấy phép.

---

## Phần 2. Bộ thành phần

### 2.1 Hiệu ứng chữ (12)
| Tên | Mô tả | Hợp phong cách |
|---|---|---|
| Trượt từng từ | Từng từ trượt lên, mờ → rõ **[có]** | Hiện đại |
| Gõ chữ | Hiện từng ký tự, có con trỏ | Phân tích, tin nhanh |
| Mở mặt nạ | Chữ trồi lên từ sau đường kẻ | Sang trọng, tối giản |
| Giãn khoảng chữ | Chữ hoa giãn rộng rồi thu về **[có]** (cảnh kết) | Sang trọng |
| Hiện theo dòng | Mỗi dòng trượt nhẹ, so le | Mọi kiểu |
| Bút dạ quang | Vệt màu quét sau từ khóa | Phân tích, chuyên gia |
| Gạch chân vẽ | Đường gạch chân tự vẽ | Tối giản |
| Phóng nhẹ | Chữ lớn phóng 110% → 100% | Hook |
| Đếm số | Số chạy từ 0 đến giá trị | Phân tích |
| Mờ vào | Mờ nhòe → nét, không di chuyển | Sang trọng |
| Tách chữ | Từng chữ cái rơi vào chỗ | Tiêu đề chương |
| Phụ đề karaoke | Từ đang nói được tô màu, theo giọng | Chuyên gia |

### 2.2 Khối chữ và đồ họa (14)
- Tiêu đề mở đầu có thẻ nhãn **[có]** · Mục số viền vàng **[có]** · Cảnh kết thương hiệu **[có]**
- Thanh tên dưới màn hình (tên, chức danh) · Câu trích lớn · Thẻ câu hỏi khách hỏi
- Thẻ nguồn "Nguồn: …, cập nhật …", **bắt buộc** khi có số liệu
- Danh sách kiểm (✓ từng mục hiện dần) · Điểm cộng / điểm cần kiểm tra (2 cột)
- Biểu đồ cột, đường, tròn có số chạy · Bảng so sánh 2 phương án
- Ghim bản đồ + đường đi (vị trí, thời gian di chuyển) · Mũi tên / vòng tròn chỉ vào chi tiết · Nhãn phòng và diện tích `[m²]`

### 2.3 Chuyển cảnh (12)
| Tên | Dùng khi |
|---|---|
| Cắt thẳng | Mặc định |
| Hòa tan | Đổi thời gian, cảm xúc chậm |
| Tối dần / sáng dần | Mở và kết chương |
| Khối 3D ngang / dọc **[có]** | Sang chương mới |
| Lật thẻ 3D | Đổi phương án, so sánh |
| Phóng xuyên | Từ ngoài vào trong nhà, từ xa vào gần |
| Lia nhanh có mờ | Năng lượng, đổi cảnh cùng hướng |
| Trượt có mờ | Danh sách, từng mục |
| Quét mặt nạ | Tối giản |
| Vệt sáng | Sang trọng |
| Khớp hình | Hai cảnh có hình giống nhau (cửa → cửa) |
| Cháy phim | Dùng rất ít, kiểu hoài niệm |

### 2.4 Lớp phủ và màu
Hạt phim nhẹ · Vệt sáng · Viền tối · Thanh tiến trình **[có]** · Logo góc **[có]** · 5 bộ chỉnh màu (trung tính, ấm sang, mát hiện đại, tương phản cao, nhạt tối giản).

### 2.5 Ảnh chuyển 3D mô phỏng (2.5D)
Từ ảnh tĩnh (phối cảnh của chủ đầu tư, ảnh chụp dự án), làm cho ảnh "sống" như có camera bay:
1. **Mức 1, nhanh, miễn phí:** đẩy máy chậm + nghiêng phối cảnh 3D nhẹ (CSS 3D, như khối chuyển cảnh đang dùng). Làm trước.
2. **Mức 2, thị sai thật:** tách tiền cảnh/hậu cảnh bằng bản đồ độ sâu (mô hình AI ước lượng độ sâu chạy trên máy), rồi dịch hai lớp với tốc độ khác nhau. Nặng hơn, hợp với Mac/PC hơn cloud.
3. **Mức 3:** ảnh làm vân bề mặt cho mô hình 3D (three.js), camera bay quanh. Chỉ khi thật cần.
Lưu ý: ảnh phối cảnh của chủ đầu tư là tài liệu có bản quyền; chỉ dùng khi được phép, ghi "Ảnh phối cảnh minh họa".

---

## Phần 3. Mẫu bố cục theo kiểu nội dung

Mỗi mẫu là một thư mục: `cau-truc.json` (các nhịp, thời lượng, ô cần điền), `vi-du/` (video mẫu), `README.md` (khi nào dùng). Thời lượng ghi cho bản TikTok khoảng 60–130 giây.

### 3.1 Phân tích dòng tiền
Dùng khi: giải thích một bài toán đầu tư bằng số. Phong cách: sang trọng hoặc tối giản.
| Nhịp | Giây | Hình | Chữ/đồ họa |
|---|---|---|---|
| Hook | 0–3 | Cảnh đẹp nhất hoặc mặt Hào | Câu hỏi có số: "Mỗi tháng còn lại bao nhiêu?" (phóng nhẹ) |
| Bối cảnh | 3–15 | Flycam, đường, tiện ích | 1–2 dòng, thẻ nguồn nếu có số |
| Luận điểm 1–3 | 15–90 | Mỗi luận điểm: 1 cảnh minh họa + 1 đồ họa số | Mục số, biểu đồ, đếm số, bút dạ quang |
| Rủi ro | 90–110 | Cảnh trung tính | "Điểm cần kiểm tra" (danh sách kiểm) |
| Kết | 110–130 | Hào hoặc cảnh đẹp | Tóm 1 câu + lời kêu gọi + cảnh kết |
Ô cần điền: số liệu kèm nguồn và ngày (bắt buộc), 3 luận điểm, 1 rủi ro.

### 3.2 Chuyên gia nói trước máy
Dùng khi: Hào nói trực tiếp. Phong cách: hiện đại.
- Hình chính là Hào nói; chèn cảnh minh họa mỗi 5–8 giây.
- Cắt bỏ khoảng lặng; mỗi lần cắt nhảy thì phóng 100% ↔ 110% để không bị giật.
- Phụ đề karaoke theo giọng, từ khóa tô vàng.
- Thanh tên lần đầu xuất hiện; từ khóa bật lên bên cạnh mặt.
Ô cần điền: video Hào nói (có tiếng), danh sách cảnh minh họa.

### 3.3 Review dự án (đi xem nhà)
Dùng khi: đi thực tế như video test. Phong cách: sang trọng.
| Nhịp | Hình | Đồ họa |
|---|---|---|
| Mở | Flycam bay tới | Tên dự án + ghim bản đồ (khi đã có tên) |
| Vị trí | Đường, kết nối | Đường đi + thời gian di chuyển (có nguồn) |
| Tiện ích | Công viên, sân chơi | Danh sách kiểm: đã vận hành / đang xây |
| Bên trong | Đi trong nhà | Nhãn phòng, diện tích `[m²]` |
| Đánh giá | Hào nói | Điểm cộng / điểm cần kiểm tra (**không chấm điểm sao**) |
| Kết | Flycam rời đi | Cảnh kết |

### 3.4 Ảnh 3D mô phỏng
Dùng khi: dự án chưa xây, chỉ có ảnh phối cảnh. Mỗi ảnh 3–4 giây với chuyển động 2.5D (mục 2.5), nhạc êm, chữ tối giản, ghi chú "Ảnh phối cảnh minh họa".

### 3.5 Tối giản
Một dòng chữ mỗi cảnh, nhiều khoảng trống, đẩy máy chậm, hòa tan, chữ có chân + chữ mảnh. Hợp câu chuyện, cảm xúc.

### 3.6 Sang trọng
Chuyển động chậm (quay 60 khung hình phát ở 30), đường kẻ vàng mảnh, chữ hoa giãn khoảng, vệt sáng, hạt phim nhẹ, màu ấm, nhạc piano/dây. Hợp giới thiệu sản phẩm cao cấp, khách VIP.

### 3.7 Thêm sau
Cập nhật chính sách (có ngày hiệu lực, nguồn) · So sánh 2 phương án (chia đôi màn hình) · Hỏi đáp khách hay hỏi.

---

## Phần 4. Cấu trúc thư mục mẫu
```
video-studio/library/
  brand/        logo, styles/sang-trong.json, toi-gian.json, am-tu-nhien.json, fonts
  text/         mỗi hiệu ứng chữ: code + ảnh xem trước
  graphics/     khối chữ, biểu đồ, bản đồ, thẻ nguồn
  transitions/  mỗi chuyển cảnh: code + xem trước
  looks/        bộ chỉnh màu, lớp phủ
  audio/        tiếng hiệu ứng, nhạc (từ thư mục của Hào, kèm giấy phép)
  layouts/      phan-tich/, chuyen-gia/, review/, anh-3d/, toi-gian/, sang-trong/
```

## Phần 5. Thứ tự làm
1. Hệ thống thiết kế (1.1–1.5) + 3 file phong cách.
2. Thành phần dùng nhiều nhất: 6 hiệu ứng chữ, 6 khối chữ (gồm thẻ nguồn), 6 chuyển cảnh, 3 bộ màu.
3. Mẫu **Review** (đã có footage) → mẫu **Phân tích** → **Chuyên gia** (cần video Hào nói) → **Ảnh 3D** (cần ảnh phối cảnh) → Tối giản, Sang trọng.
4. Âm thanh khi có thư mục của Hào.
Mỗi mẫu xong phải kèm một video ví dụ để Hào duyệt.
