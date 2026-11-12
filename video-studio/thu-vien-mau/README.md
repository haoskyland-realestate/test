# Thư viện mẫu edit

Mỗi mẫu một thư mục `<loại>-<số>_<tên-ngắn>/`:
- `mau.json`: cấu hình máy đọc (phong cách, nhịp chuyển cảnh, hiệu ứng âm tự rải). Định nghĩa trường: `scripts/ap_mau.py`.
- `MAU.md`: phân tích video mẫu gốc (bố cục, nhịp, chuyển cảnh, chữ, âm) + mẫu làm được gì, chưa làm được gì.

Áp mẫu: app → nút **✦ Thư viện mẫu** (đầu trang) → Áp mẫu, hoặc `python3 scripts/ap_mau.py projects/<tên> <id>`.

| Id | Tên | Loại | Từ video mẫu |
|---|---|---|---|
| `edit-phim-01` | Mẫu edit video 1 chuyên nghiệp | edit phim | Review căn hộ 55 s, chữ 3D giữa khung, chuyển cảnh phóng/xoay/cháy sáng |
| `talking-head-01` | Chuyên gia vàng cao cấp | talking head | Chữ Anton vàng ánh kim, từng từ bật ra, zoom nhấn ý |
| `neon-01` | Neon cam ánh sáng | talking head | Chữ cam phát sáng gõ dần, khung gần – xa xen kẽ |
| `chu-dong-01` | Chữ động nhiều màu | tin nhanh | Chữ xếp chồng 4 màu, to nhỏ xen kẽ, lia nhanh |
| `giai-thich-01` | Thẻ giải thích sáng | giải thích | Thẻ trắng, nhãn BƯỚC cam, so sánh 2 cột |
| `sang-trong-01` | Sang trọng nghỉ dưỡng | sang trọng | Chữ có chân kem, chuyển cảnh mơ màng, nhịp chậm |

5 mẫu sau (13/11) tự thiết kế theo thể loại phổ biến, chỉnh cho khách BĐS của Hào. Công thức chung: `docs/04-thu-vien/CONG-THUC-VIRAL.md`. Trường hiển thị ở thư viện: `ten`, `loai`, `the` (nhãn trên thẻ), `nganh`, `mo_ta`, `dung_cho`, `xem_truoc` (nền, chữ mẫu, CSS, kiểu chuyển động)

Thêm mẫu mới: Hào gửi video mẫu → Claude phân tích theo cách của `edit-phim-01/MAU.md` → tạo thư mục mới, số tiếp theo. Không lưu video gốc của người khác vào repo.
