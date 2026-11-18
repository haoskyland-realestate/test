---
name: dung-talking-head
description: Dựng video talking head (Hào nói trước máy) theo đúng 5 bước Hào chốt: text từ giọng nói → AI xác định hook, tiêu đề, từ khoá, số liệu → khung hình → chuyển động và âm → ghép. Dùng khi Hào nói "dựng talking head", "làm video nói trước máy", "chữ theo lời nói".
---

# Dựng talking head: mỗi bước có đầu ra để Hào xem; 2 lần duyệt (storyboard, bản xem 540×960) trước bản cuối

**Không dùng app** (Hào chốt 17/11): Claude chạy thẳng các lệnh dưới đây. Trên PC Windows, mọi lệnh `python` là `.venv\Scripts\python.exe` (tạo bằng `setup-windows.ps1`), chạy trong `video-studio`; trên cloud/Mac là `python3` hoặc `.venv/bin/python`. Thiếu thư viện thì công cụ tự báo lệnh cài đúng.

0. **Tạo dự án từ footage Hào gửi** (nhiều nguồn một lúc: thư mục/file trên máy, link Google Drive, link tải trực tiếp, YouTube/TikTok): `python scripts/du_an_moi.py <ngày>_<tiktok|youtube>_<dự án>_<chủ đề> <nguồn 1> [nguồn 2 …]`; thêm footage sau: `python scripts/du_an_moi.py --them <tên> <nguồn …>`. Rồi `python scripts/master_cut.py projects/<tên>` (cắt lặng, câu vấp, chọn khúc đẹp; báo cáo `build/master-cut.md`) và `python scripts/dung.py projects/<tên> --nhap` một lần (tạo `build/voice.wav`). Gửi Hào báo cáo master cut.

Đọc trước: `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` (quy tắc đối chiếu, tốc độ chữ, bố cục). Công cụ: `video-studio/scripts/ban_dung.py`. Chạy trong `video-studio`.

1. **Text từ giọng nói.** Có `build/voice.wav` (dựng nháp một lần) và `meta.tu_vung`. `python3 scripts/loi_nhip.py projects/<tên>` (nhận dạng) rồi `python3 scripts/ban_dung.py chep projects/<tên>` → `build/LOI-NOI.md`: từng câu, số thứ tự từng từ, giây. **Không sửa, không đoán.** Từ nghe sai thì **đoán ý theo nội dung chủ đề** (vd. "bàn giao kẻ" → "bàn giao kèm"), thêm vào `meta.sua_tu`, báo Hào danh sách chỗ đã sửa. **Không sửa tên người nói** (người nói có thể không phải Hào; lấy đúng tên trong ghi âm). Video mặc định **không có thương hiệu** "Hào Sky Land"; chỉ khi Hào yêu cầu mới thêm `meta.thuong_hieu`. Câu lặp/chỗ vấp: cắt bằng `python scripts/cat_doan.py projects/<tên> <từ> <đến>` (mốc trong khoảng lặng). Lời Hào nói và tài liệu Hào gửi coi là đã xác thực (nguồn "Hào cung cấp, <ngày>").
2. **AI xác định vai trò** (Claude, người dựng chuyên nghiệp). Đọc `LOI-NOI.md`, viết `projects/<tên>/BAN-DUNG.json`:
   - `hook`: 2–4 từ gây chú ý trong **3 giây đầu** (chữ lớn sau đầu).
   - `tieu-de`: mỗi ý/phòng/chủ đề mới một tiêu đề 1–3 từ (chữ lớn), cách nhau ≥ 4 giây.
   - `tu-khoa`: từ cần nhấn trong lời (tô màu, gạch chân, huy hiệu), 1 mỗi cụm là đủ.
   - `so-lieu`: số tiền, diện tích, % → cảnh chèn thẻ số, **bắt buộc `nguon`**.
   - `cta`: lời kêu gọi cuối.
   Chữ hiện ra phải là **chữ Hào đã nói** (`chu`, `nhan` đều được kiểm; sai là công cụ chặn). **Gửi Hào bảng vai trò** (vai, chữ, giây) cùng danh sách từ nghe sai trước khi đi tiếp.
3. **Khung hình.** `python3 scripts/ban_dung.py ap projects/<tên>` → timeline: hook/tiêu đề thành chữ lớn, số liệu thành thẻ, phần còn lại là chữ theo nhịp nói ngang ngực, bố cục tự kẹp vùng an toàn. Rồi `python3 scripts/doi_chieu.py projects/<tên>`.
4. **Chuyển động + âm.** Áp mẫu: `python scripts/ap_mau.py projects/<tên> talking-luxury-01` (hoặc `talking-cam-01`; danh sách mẫu: thư mục `thu-vien-mau/`): chuyển cảnh, âm nhiều lớp, zoom theo từ khoá; mọi chuyển động chậm 1,5 lần, ease in-out.
5. **Storyboard → Hào duyệt** (Hào chốt 17/11, bắt buộc): `python scripts/storyboard.py projects/<tên>` → `STORYBOARD.md` (từng cảnh: giây, hình, lời nói, chữ trên màn hình, chuyển cảnh) + `build/storyboard.jpg` (ảnh lưới) + mục "Phân tích lời nói và chỗ cắt" (`scripts/phan_tich_loi.py`: nói nhanh/chậm, lặp từ, nói vấp, cắt giữa từ; chỉ đề xuất, Hào chọn mục nào thì Claude sửa). Gửi Hào cả hai cùng mục "Cần Hào trả lời". Tự soát trước khi gửi: cảnh trám < 1 giây, chữ chồng chữ, chính tả (đơn vị `ha`, số kiểu Việt). **Chưa duyệt thì không dựng.**
6. **Bản xem 540×960 → Hào duyệt:** `python scripts/dung.py projects/<tên> --xem` → `out/<tên>.xem.mp4` (nhẹ, nhanh, cùng chữ/vị trí với bản cuối). Tự soát bằng máy trước khi gửi: khung đen, hình khớp tiếng, chụp khung ở mỗi vai. Gửi Hào video.
7. **Bản cuối** chỉ khi Hào duyệt bản xem + hết câu hỏi: `python scripts/dung.py projects/<tên>` (bộ dựng tự dừng nếu số/chữ chưa kiểm chứng).
