# Talking head cam: chữ động theo nhịp nói (`talking-cam-01`)

Rút từ phần **kết quả dựng AI** trong video hướng dẫn 12 phút (giây 266–500, bản thứ 2 và thứ 3 sau góp ý). Chỉ học cấu trúc và nhịp; không chép đồ hoạ, người, chữ của video đó.

## Công thức
| Lớp | Cách làm |
|---|---|
| Nền | Phòng tối, ánh cam ấm hai bên; người chiếm gần hết khung dọc |
| Chữ thường | Trắng, nhỏ, đặt ngang cằm–ngực, từng từ hiện đúng lúc nói, tích luỹ thành cụm ≤5 từ |
| **Từ khoá** | Cụm 1–3 từ nằm **riêng một dòng bên dưới**: cam `#ff8a1a`, đậm, nghiêng, VIẾT HOA, phông hẹp, quầng sáng cam (vd. "PROBLEM", "WHAT YOU START", "LOOK AT YOUR LIFE") |
| Cảnh chèn | Mỗi 8–10 giây một thẻ/đồ hoạ (thẻ trắng, dấu ✓ cam, sơ đồ quỹ đạo, thẻ kính mờ) rồi về người nói |
| Nhịp cắt | Cắt thẳng là chính; chớp sáng hoặc phóng mờ khi đổi ý |
| Âm | Tiếng vút nhẹ khi vào cảnh chèn; không nhạc nền ồn |
| Lỗi hay gặp ở vòng đầu | Chữ hiện rồi biến quá nhanh · không có ease in-out · chữ nhỏ · đồ hoạ đè lên người · 10 giây đầu chậm (xem `GHI-NHO-NGHIEM-THU.md`) |

## Cách dùng
1. Áp mẫu (nút ✦) cho dự án talking head. Mẫu đặt kiểu chữ (`meta.loi`), nhịp chuyển cảnh, âm.
2. Dựng nháp một lần (có `build/voice.wav`), điền `meta.tu_vung` và `meta.tu_khoa` (từ cần cam) vào timeline.
3. `python3 scripts/loi_nhip.py projects/<tên> --ngang-nguc` → chữ theo nhịp nói, từ khoá cam.
4. Xem khung, chỉnh `y`/`top_px`; chữ nằm ngang cằm–ngực, không che mặt.

## Chưa có
- Cảnh chèn đồ hoạ (thẻ trắng, ✓ cam, sơ đồ quỹ đạo, thẻ kính mờ): chưa làm; hiện dùng cảnh trám/thẻ minh hoạ có sẵn.
- Cụm từ khoá đang tự chọn theo số, tiền và `meta.tu_khoa`; chọn theo ý nghĩa cần người hoặc Claude.
- Phông Barlow Condensed tải từ Google Fonts khi dựng: máy không có mạng sẽ rơi về phông thay thế (nhìn khác).
