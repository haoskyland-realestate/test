---
name: hoc-mau
description: Học phong cách edit từ một video mẫu (TikTok/YouTube) và biến thành mẫu trong thư viện (thu-vien-mau/) để áp cho video của Hào Sky Land. Dùng khi Hào gửi video mẫu và nói "bắt chước", "học style này", "làm mẫu giống video này", "thêm mẫu".
---

# Học mẫu từ một video

Mục tiêu: từ video mẫu ra **một `mau.json` + `MAU.md`** ghép từ thứ kho đã có, để áp bằng nút ✦ hoặc `scripts/ap_mau.py`. Không chép đồ hoạ, âm, logo của người khác: chỉ học **nhịp và cấu trúc**, dùng tài nguyên của Hào.

Đọc trước: `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` (lỗi Hào đã chỉ ra), `docs/04-thu-vien/THU-VIEN-HIEU-UNG.md`, `docs/04-thu-vien/THU-VIEN-TAG.md`, một mẫu có sẵn (`thu-vien-mau/edit-phim-01_chuyen-nghiep/`).

## Các bước
1. **Đo (miễn phí, không dùng AI).** Tải video mẫu về thư mục tạm (không đưa vào repo), chạy trong `video-studio`:
   `python3 scripts/hoc_mau.py <video> <tên-ngắn>` → `thu-vien-mau/_hoc/<tên>/` gồm `luoi.jpg` (ảnh lưới khung), `do.json`, `BAO-CAO.md` (nhịp cắt, chớp trắng, khung đen, đỉnh âm, độ ồn, màu từng đoạn). Thư mục `_hoc/` không lên GitHub.
2. **Nhìn `luoi.jpg` và đọc `BAO-CAO.md`.** Ghi ra: kiểu chữ (màu, hiệu ứng, từ khoá đổi màu), thẻ tên, cảnh chèn (ảnh màn hình, logo, B-roll), chuyển cảnh, khung hình người nói, màu tổng thể. Chữ trên màn hình chưa đọc tự động được (chưa có OCR): đọc bằng mắt từ ảnh lưới, cần thì làm thêm lưới dày quanh đoạn đáng chú ý.
3. **Ghép với kho.** Với mỗi thành phần, chọn cái gần nhất đã có: phong cách (`effects.STYLES`), chuyển cảnh (`TRANSITIONS`, 212 gl-), kiểu chữ/khối (`TEXT_KINDS`, tag), hiệu ứng âm (`SFX`). Thành phần **chưa có** thì ghi vào mục "Còn thiếu" của `MAU.md`, không tự bịa tên; làm thành phần mới chỉ khi Hào đồng ý (tốn token).
4. **Viết mẫu**: thư mục `thu-vien-mau/<loại>-<số>_<tên>/` với `mau.json` (cùng khung với `edit-phim-01`: meta.style, audio, chuyen_canh.chu_ky/dur, sfx, nhip_chu, xem_truoc, mo_ta, dung_cho) và `MAU.md` (số đo đã dựa vào, chỗ nào đoán, còn thiếu gì). Ghi rõ nguồn: "Phân tích video mẫu <ngày>, chỉ lưu phân tích".
5. **Thử, không dựng cả video.** Áp mẫu cho một dự án thử, kiểm bằng `python3 scripts/test_timeline.py`, dựng nháp một đoạn 10–20 giây (`dung.py --nhap`) hoặc chụp vài khung, gửi Hào ảnh + một dòng "giống ở đâu, khác ở đâu".
6. **Vòng góp ý (3–4 vòng là bình thường).** Mỗi vòng sửa nhiều lỗi nhỏ cùng lúc. Lỗi thông số (tốc độ, màu, âm lượng, chuyển cảnh): Hào chỉnh trong app rồi bấm **💾 Lưu chỉnh sửa thành mẫu**. Lỗi vị trí: Hào dùng **📸 Lưu gói góp ý** (ảnh khung + lời), đọc `projects/<tên>/gop-y/<giờ>/y-kien.md`. Lỗi lặp lại cho mọi video thì sửa vào mẫu hoặc mã, không sửa riêng từng video.

## Bài học từ video hướng dẫn mẫu (12 phút, Hào gửi 14/11/2026)
- Chữ hiện chậm lại, mọi chuyển động có ease in-out (tăng tốc nhẹ rồi hãm), chữ đủ to, không để đồ hoạ đè lên người nói, 10 giây đầu phải nhanh gọn.
- Chọn **một** video mẫu nếu muốn giống đúng style đó; 2–3 video nếu muốn một style riêng của Hào Sky Land (máy thấy điểm chung).

## Quy tắc
- Nguồn tài nguyên mới (âm, font, nhạc): chỉ từ nguồn có giấy phép rõ, đã kiểm trang gốc, ghi vào `GIAY-PHEP.md` của kho; Hào duyệt danh sách nguồn trước khi tải. Không tách âm hay hình từ video của người khác.
- Chưa chạy thử thì ghi "chưa thử". Không bịa số đo.
