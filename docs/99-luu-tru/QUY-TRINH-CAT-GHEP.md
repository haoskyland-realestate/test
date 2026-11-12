# Quy trình cắt ghép video từ flycam + giọng thu

Dùng khi Hào có: video flycam thô, giọng tự thu, kịch bản. Chạy trên máy có file (Windows local hoặc phiên Claude Code có file). Video thô nặng nên không đưa lên GitHub.

1. **Chuẩn bị.** Tạo `video-studio/projects/<tên>/media/`, bỏ vào đó giọng thu và flycam. Logo và bộ nhận diện để ở `video-studio/brand/`. Kịch bản (văn bản) để cạnh đó.
2. **Phụ đề.** Nhận dạng giọng thu thành chữ có mốc thời gian (`npx hyperframes@0.9.37 transcribe`), đối chiếu với kịch bản, Hào đọc lại tên riêng và số liệu, lưu thành `captions.srt`.
3. **Chọn cảnh.** `scripts/contact-sheet.sh <video flycam>` tạo ảnh lưới có mốc giờ. Claude xem ảnh, ghép từng đoạn kịch bản với cảnh flycam phù hợp, viết `edl.json` (xem `projects/mau/`). Hào xem và sửa.
4. **Dựng.** `node scripts/assemble.mjs projects/<tên>/edl.json` → `out/<tên>.mp4` (9:16, giọng thu, logo, phụ đề, cảnh kết).
5. **Duyệt và sửa.** Xem video; sai cảnh thì sửa mốc `in`/`out` trong EDL rồi dựng lại. Tổng thời lượng cảnh nên khớp giọng thu (máy cảnh báo nếu lệch hơn 1 giây).
6. **Đăng** do Hào quyết định.

Đã thử với dữ liệu giả (video thử nghiệm, giọng giả): cắt khung dọc, logo, phụ đề tiếng Việt, cảnh kết đều hiện đúng. **Chưa thử** với flycam thật, giọng thật, nhận dạng giọng tiếng Việt và nhạc nền (`music` trong EDL).
