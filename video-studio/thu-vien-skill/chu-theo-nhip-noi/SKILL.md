---
name: chu-theo-nhip-noi
description: Chữ phụ đề theo nhịp lời nói: từng từ hiện đúng lúc người nói, cụm ≤5 từ, thay phụ đề thường. Dùng khi Hào nói "chữ chạy theo lời", "bắt nhịp người nói", "phụ đề kiểu video mẫu".
---

# Chu theo nhip noi (ĐÃ CÓ MÃ)

Quan sát từ video mẫu (Open Residency, Hào gửi 14/11/2026; chỉ học cấu trúc và nhịp, không chép nguyên đồ hoạ): Mẫu: chữ trắng nhỏ ngay cạnh người, tích luỹ từng từ ("and" → "and literally the" → "and literally the play is"), cụm mới thay cụm cũ sau mỗi nhịp nghỉ.

## Cách làm
1. Dựng nháp một lần để có `build/voice.wav`.
2. Ghi `meta.tu_vung` (tên riêng, thuật ngữ) và `meta.tu_khoa` (từ cần đỏ) trong timeline.
3. `python3 scripts/loi_nhip.py projects/<tên> [--ngang-nguc]` → khối chữ `kind: "loi"`.
4. Xem khung (`dung.py --nhap` hoặc chụp vài mốc), chỉnh `y`/`top_px`, cỡ chữ trong `lop_chu.py`.

## Đã có trong repo
`scripts/loi_nhip.py` (gom cụm, từ khoá), `kind: "loi"` trong `lop_chu.py`/`timeline.py`/`effects.py`, `--tu-kiem`.

## Còn thiếu
Cỡ chữ và kiểu theo từng mẫu; tách cụm theo ý nghĩa (đang theo nghỉ 0,4 giây và dấu chấm); lưu kiểu này vào mẫu (nút 💾 chưa lưu chữ).

## Quy tắc
Đọc `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` trước khi dựng. Dữ kiện dự án phải có nguồn và ngày. Chưa chạy thử thì ghi "chưa thử". Hào duyệt trước khi tải tài nguyên mới hoặc tốn chi phí.
