# Thư viện mẫu edit

Mỗi mẫu một thư mục `<loại>-<số>_<tên-ngắn>/`:
- `mau.json`: cấu hình máy đọc (phong cách, nhịp chuyển cảnh, hiệu ứng âm tự rải). Định nghĩa trường: `scripts/ap_mau.py`.
- `MAU.md`: phân tích video mẫu gốc (bố cục, nhịp, chuyển cảnh, chữ, âm) + mẫu làm được gì, chưa làm được gì.

Áp mẫu: app → tab **Thương hiệu → Mẫu edit → Áp mẫu**, hoặc `python3 scripts/ap_mau.py projects/<tên> <id>`.

| Id | Tên | Loại | Từ video mẫu |
|---|---|---|---|
| `edit-phim-01` | Mẫu edit video 1 chuyên nghiệp | edit phim | Review căn hộ 55 s, chữ 3D giữa khung, chuyển cảnh phóng/xoay/cháy sáng |

Thêm mẫu mới: Hào gửi video mẫu → Claude phân tích theo cách của `edit-phim-01/MAU.md` → tạo thư mục mới, số tiếp theo. Không lưu video gốc của người khác vào repo.
