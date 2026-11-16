---
name: dung-talking-head
description: Dựng video talking head (Hào nói trước máy) theo đúng 5 bước Hào chốt: text từ giọng nói → AI xác định hook, tiêu đề, từ khoá, số liệu → khung hình → chuyển động và âm → ghép. Dùng khi Hào nói "dựng talking head", "làm video nói trước máy", "chữ theo lời nói".
---

# Dựng talking head: 5 bước, mỗi bước có đầu ra để Hào xem

Đọc trước: `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` (quy tắc đối chiếu, tốc độ chữ, bố cục). Công cụ: `video-studio/scripts/ban_dung.py`. Chạy trong `video-studio`.

1. **Text từ giọng nói.** Có `build/voice.wav` (dựng nháp một lần) và `meta.tu_vung`. `python3 scripts/loi_nhip.py projects/<tên>` (nhận dạng) rồi `python3 scripts/ban_dung.py chep projects/<tên>` → `build/LOI-NOI.md`: từng câu, số thứ tự từng từ, giây. **Không sửa, không đoán.** Từ nghe sai (vd. "kẻ" có thể là "kèm") thì ghi lại để hỏi Hào; Hào xác nhận thì thêm `meta.sua_tu`.
2. **AI xác định vai trò** (Claude, người dựng chuyên nghiệp). Đọc `LOI-NOI.md`, viết `projects/<tên>/BAN-DUNG.json`:
   - `hook`: 2–4 từ gây chú ý trong **3 giây đầu** (chữ lớn sau đầu).
   - `tieu-de`: mỗi ý/phòng/chủ đề mới một tiêu đề 1–3 từ (chữ lớn), cách nhau ≥ 4 giây.
   - `tu-khoa`: từ cần nhấn trong lời (tô màu, gạch chân, huy hiệu), 1 mỗi cụm là đủ.
   - `so-lieu`: số tiền, diện tích, % → cảnh chèn thẻ số, **bắt buộc `nguon`**.
   - `cta`: lời kêu gọi cuối.
   Chữ hiện ra phải là **chữ Hào đã nói** (`chu`, `nhan` đều được kiểm; sai là công cụ chặn). **Gửi Hào bảng vai trò** (vai, chữ, giây) cùng danh sách từ nghe sai trước khi đi tiếp.
3. **Khung hình.** `python3 scripts/ban_dung.py ap projects/<tên>` → timeline: hook/tiêu đề thành chữ lớn, số liệu thành thẻ, phần còn lại là chữ theo nhịp nói ngang ngực, bố cục tự kẹp vùng an toàn. Rồi `python3 scripts/doi_chieu.py projects/<tên>`.
4. **Chuyển động + âm.** Áp mẫu (vd. `talking-cam-01`: `ap_mau.py projects/<tên> talking-cam-01` hoặc nút ✦): chuyển cảnh, âm nhiều lớp, zoom theo từ khoá; mọi chuyển động chậm 1,5 lần, ease in-out.
5. **Xem khung tĩnh rồi ghép.** `dung.py --nhap`, chụp khung ở mỗi vai (hook, tiêu đề, từ khoá, số liệu), gửi Hào. **Hào duyệt + hết câu hỏi** mới chạy `dung.py` bản cuối (bộ dựng tự dừng nếu số/chữ chưa kiểm chứng).
