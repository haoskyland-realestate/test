# Thư viện mẫu video

Mỗi mẫu là một file `.html` trong thư mục này. Chọn mẫu bằng trường `"template"` trong spec (mặc định `cashflow-3d`).

| Mẫu | Mô tả |
|---|---|
| `cashflow-3d` | Hook + ý chính + khối 3D xoay (three.js) |
| `text-only` | Hook + ý chính, không 3D, nhẹ hơn |
| `aerial-city` | Cảnh bay trên thành phố giả lập (thế chỗ flycam khi chưa có footage), không chữ |

## Thêm mẫu mới
1. Sao chép một file mẫu, đổi tên (chỉ dùng chữ, số, gạch ngang), sửa giao diện và animation.
2. Giữ các ký hiệu `__W__`, `__H__`, `__DUR__`, `__RES__` và dòng `const SPEC = /*SPEC*/null;` để hệ thống điền dữ liệu.
3. Giữ animation điều khiển bằng timeline `tl` (không dùng đồng hồ thật) để render lặp lại được.
4. Thử: `./scripts/render.sh videos/demo.json hyperframes` sau khi đặt `"template": "tên-mẫu"`.
Mẫu chỉ có hiệu lực với engine hyperframes.
