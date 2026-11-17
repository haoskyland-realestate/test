# Kho âm thanh

```
thu-vien-am-thanh/
  hieu-ung/          hiệu ứng âm (sound effect): <nhóm>_<tên>_<số>.wav     ← đang có 21 âm tổng hợp
  hieu-ung.json      danh mục: nhóm, mô tả, dùng khi, độ dài, điểm nhấn, nguồn
  nhac/              nhạc nền (chờ Hào gửi kho nhạc)
```
Danh mục đọc dễ: `docs/04-thu-vien/THU-VIEN-AM-THANH.md`.

## Âm đang có
21 âm **tự tổng hợp** bằng `scripts/tao_sfx.py` (không bản quyền, tạo lại được y hệt), dựng theo phân tích video mẫu `thu-vien-mau/edit-phim-01_chuyen-nghiep/MAU.md`. Chất lượng mức khá; âm thu thật của thư viện chuyên nghiệp sẽ giàu hơn.

## Thêm âm thật (khi Hào có kho effect)
1. Đặt tên theo quy ước: `<nhóm>_<tên-không-dấu>_<số>.wav`, ví dụ `whoosh_gio-manh_02.wav`. Nhóm đang dùng: `whoosh`, `chu`, `ting`, `impact`, `riser`, `anh-sang` (thêm nhóm mới được).
2. Đổi sang WAV 48 kHz nếu là mp3: `ffmpeg -i vao.mp3 -ar 48000 whoosh_gio-manh_02.wav`.
3. Thêm một mục vào `hieu-ung.json` (Claude Code làm được): `"whoosh_gio-manh_02": {"nhom": "whoosh", "vi": "...", "dung_khi": "...", "dai": <giây>, "diem_nhan": <giây chạm>, "nguon": "<tên kho, giấy phép>"}`.
4. Muốn mẫu edit dùng âm mới: đổi tên âm trong `thu-vien-mau/<mẫu>/mau.json`.

Chỉ dùng âm có giấy phép rõ (ghi vào trường `nguon`). Chạy lại `tao_sfx.py` chỉ cập nhật âm tổng hợp, không xoá mục tự thêm.
