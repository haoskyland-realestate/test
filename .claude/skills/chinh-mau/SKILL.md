---
name: chinh-mau
description: Đạo diễn màu cho một dự án video: đo từng cảnh (ám màu, sáng tối, cháy, màu da), chọn cảnh chuẩn, lấy phong cách màu có sẵn hoặc từ video/ảnh mẫu, tạo mỗi cảnh một LUT, giữ màu da và trắng nội thất, kiểm lại bằng số, gửi ảnh trước/sau cho Hào duyệt. Dùng khi Hào nói "chỉnh màu", "cân màu", "match màu", "màu đồng nhất", "lấy màu video mẫu", "da bị cam/xanh", "ám vàng".
---

# Chỉnh màu như đạo diễn hình ảnh

Luật màu và ý nghĩa từng số: `docs/04-thu-vien/CHINH-MAU.md`. Lỗi đã nghiệm thu: `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md`. Đọc cả hai trước.
Công cụ: `video-studio/scripts/chinh_mau.py` (numpy, OpenCV, ffmpeg; không cài thêm gì). Chạy trong `video-studio`.

## Các bước
1. **Có footage:** dự án đã có `timeline.json` và footage trong `projects/<tên>/build/raw/`. Video mẫu (nếu Hào gửi) để ở `projects/<tên>/build/raw/` hoặc trong kho.
2. **Xem trước khi quyết:** chạy `bash scripts/contact-sheet.sh` hoặc lấy vài khung, **tự nhìn ảnh** để biết: nội thất hay ngoài trời, phân khúc (cao cấp, nghỉ dưỡng, căn hộ), có người nói không, ánh sáng gì (nắng, đèn vàng, đèn trắng, trộn).
3. **Chọn phong cách** theo bảng trong `CHINH-MAU.md` (mặc định nhà mẫu cao cấp: `sang-trong`). Có video mẫu thì thêm `--mau <file>`.
4. **Chạy (chưa đụng timeline):**
   `python3 scripts/chinh_mau.py projects/<tên> --phong-cach <tên> [--mau <file>] [--chuan <số cảnh>] [--do-manh 0.7]`
5. **Đọc kết quả, tự sửa trước khi gửi Hào:**
   - Mở `projects/<tên>/MAU-SAC.md` và **nhìn** `projects/<tên>/mau/truoc-sau.jpg` (trên là trước, dưới là sau).
   - Mục "Cần Hào xem" có cảnh lệch thì sửa `mau/ke-hoach.json` (thông số từng cảnh), rồi chạy lại kèm `--tu-file`.
   - Cảnh cố ý khác ánh sáng (ngoài trời so với trong nhà, cảnh đêm) thì được lệch độ sáng; ghi lý do vào báo cáo.
6. **Gửi Hào** ảnh `truoc-sau.jpg` cùng 3–5 dòng tóm tắt: ám gì đã sửa, cảnh chuẩn nào, da bao nhiêu %, cảnh nào không cứu được (cháy). **Chờ Hào duyệt.**
7. **Hào duyệt:** chạy thêm `--ap` để ghi `"look": "lut:mau/cNN.cube"` vào từng đoạn (giữ `timeline.json.bak`), rồi dựng bằng skill `dung-video`. Bộ dựng tự tắt tự cân màu cũ ở đoạn có LUT này.
8. **Kiểm bản dựng:** đo vài khung của `out/<tên>.mp4`. Nếu lớp chữ có dải tối (scrim) thì đo ở khung không có chữ.

## Không làm
- Không đẩy độ rực chung để video "nịnh mắt": da người phải nằm trong 35–50% (`CHINH-MAU.md`).
- Không nhuộm tường, trần trắng thành vàng hay xanh. Gỗ, đá, vải giữ đúng màu vật liệu thật: khách mua nhà dựa vào màu đó.
- Không dùng repo màu giấy phép GPL (ví dụ color-matcher). Không tải mô hình AI nặng khi chưa hỏi Hào.
- Không ghi đè timeline khi Hào chưa duyệt (`--ap` chỉ chạy sau khi duyệt).
