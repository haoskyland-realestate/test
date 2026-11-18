---
name: agent-video
description: Agent edit video talking head (gộp AutoEdit preset A/B/C + bộ dựng Cloud Edit) chạy trên máy bằng MỘT lệnh, dừng ở cổng cần Hào, không đoán. Dùng khi Hào nói "edit video này", "dựng talking head", "làm video nói trước máy", gửi footage/link và muốn ra video, hoặc nói "chốt phương án", "chọn hiệu ứng", "duyệt bản xem".
---

# Agent video: một lệnh, 4 cổng, không suy đoán

Mọi lệnh chạy trong `video-studio` (PC Windows: `.venv\Scripts\python.exe` thay cho `python`). Đọc trước: `CLAUDE.md`, `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md`, `autoedit/QUY-TRINH-AUTOEDIT.md` (quy tắc trình bày, vùng an toàn, phông, mục 5 "ý đang nói → hiệu ứng").

```
python scripts/agent.py <tên> <nguồn…> [--preset A|B|C] [--mau talking-luxury-01]   # tạo / làm tiếp
```
Tên theo `<ngày>_<tiktok|youtube>_<dự án>_<chủ đề>`. Nguồn: thư mục, file, link Drive/trực tiếp/YouTube/TikTok. Chạy lại cùng lệnh là làm tiếp. `--trang-thai` xem đang ở đâu. Mã thoát: 0 xong · 10 chờ Hào · 20 chờ Claude.

## Việc của Claude ở từng điểm dừng
1. **CỔNG 1 (mã 10, `CAN-HOI.md`)**: từ máy nghe không chắc (độ tin cậy < 60%), tên riêng, con số, đoạn nghi lặp/vấp/cắt tiếng. Gửi Hào bảng, KHÔNG tự đoán. Hào trả lời → ghi `meta.sua_tu` (từ nghe sai), `meta.da_duyet` (số/tên đã xác nhận), cắt bằng `scripts/cat_doan.py` (mốc trong khoảng lặng) → `agent.py <tên> --qua 1`. Không sửa tên người nói thành "Hào".
2. **CHỜ CLAUDE (mã 20) — chia cảnh + vai**: đọc `build/LOI-NOI.md`, viết `BAN-DUNG.json` (định dạng ở đầu `scripts/ban_dung.py`):
   - `canh`: cảnh 2–8 giây theo ý, liền nhau; mỗi cảnh 2–4 mã `goi_y` (mã đầu là đề xuất chính) theo `autoedit/QUY-TRINH-AUTOEDIT.md` mục 5; mã có trong `autoedit/HIEU-UNG-MAP.json`.
   - `vai`: hook, tiêu đề, từ khoá, số liệu (bắt buộc `nguon`), thẻ (`the`: checklist/quy-dao/kinh), cta. Chữ hiện ra phải là lời đã nói (công cụ chặn).
3. **CỔNG 2 (mã 10)**: gửi Hào `build/chon-hieu-ung.html` (một file, ảnh nhúng sẵn, mở trên điện thoại). Hào dán kết quả → `agent.py <tên> --chon "<kết quả>"` (hoặc `"làm hết"`). Nếu agent báo "cần vai …" (mã 20): thêm vai đúng loại trong khoảng từ của cảnh rồi chạy lại.
4. **CỔNG 3 (mã 10)**: gửi Hào `STORYBOARD.md` + `build/storyboard.jpg` + `build/storyboard-chot.html`. Hào "chốt phương án" → `--qua 3`. Hào sửa → Claude sửa `BAN-DUNG.json`/timeline rồi chạy lại.
5. **CỔNG 4 (mã 10)**: gửi Hào `out/<tên>.xem.mp4` (540×960, có vạch vùng an toàn). Đạt → `--qua 4` → agent dựng bản cuối, chạy đối chiếu chữ/số, vùng an toàn, `kiem_cuoi.py` (khổ, độ dài, hình khớp tiếng, chớp khung tối, −14 LUFS). Gửi `out/<tên>.mp4`.

## Đợt 1 (18/11): giới hạn đã biết
- Hiệu ứng có trong bộ dựng: chữ lớn (typo), số liệu (count_up), danh sách ✓ (note_board), kính mờ (glass_list), sơ đồ (tree_diagram), kêu gọi (outro_cta), chỉ người nói. Mã khác (map_route, chart_bars, amenity_grid…) = **đợt 2**: cảnh đó dựng chỉ người nói và agent báo; không tự chế hình. `map_route` có thể làm riêng bằng skill `map-location-video` rồi chèn làm cảnh trám.
- Preset A/B/C hiện chỉ quyết định ảnh mẫu trong trang chọn; bố cục khung người nói/nền của preset là đợt 2. Bố cục hiện dùng mẫu edit trong `thu-vien-mau/` (`--mau`).
