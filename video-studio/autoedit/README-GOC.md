# AutoEdit: edit video dọc 9:16 tiếng Việt bằng Claude Code

Bạn đưa video thô, Claude Code cắt khoảng lặng, chia cảnh, bạn chọn phong cách (preset A/B/C) và hiệu ứng cho từng cảnh, nó dựng đồ họa bằng HyperFrames và render MP4.

## Cách dùng
1. Giải nén thư mục này (ví dụ `D:\AutoEdit`).
2. Máy mới: chạy `cai-dat\chay-cai-dat.bat` một lần (cài Node, Python, Git, FFmpeg, Whisper, Claude Code, HyperFrames). Cần mạng, mất 10–20 phút. Đã cài sẵn rồi thì bỏ qua.
3. Mở PowerShell:
```
cd D:\AutoEdit
claude
```
4. Bỏ video vào thư mục `input\`, rồi nói với Claude Code, ví dụ:
> Edit video input\ten-video.mp4, dùng preset A.

Claude Code đọc `CLAUDE.md`, tự kiểm tra môi trường, rồi hỏi bạn từng bước (preset, hiệu ứng mỗi cảnh, dữ liệu còn thiếu như ảnh, số liệu, bản đồ).

## Trong gói
- `CLAUDE.md`: quy trình đầy đủ (Claude Code tự đọc).
- `effects/thumbs/` và `effects/picker_template.html`: hình xem trước để trang chọn hiệu ứng hiện hình cho từng cảnh.
- `effects/storyboard_template.html`: trang storyboard để xem lại và CHỐT phương án (sửa đổi) trước khi dựng video.
- `tools/`: `safe_check.py` (kiểm vùng an toàn), `matte_person.py` (tách người nói), `preset_A_example/` (dự án mẫu, có chế độ `guides`).
- `presets/`: 3 phong cách trọn bộ. `effects/CATALOG.md`: danh mục hiệu ứng. `effects/reference/`: trang HTML mẫu, mở bằng Chrome để xem chuyển động.
- `tools/safe_check.py`: kiểm tra chữ/đồ họa có nằm trong vùng an toàn TikTok/Reels/Shorts không (Claude Code tự chạy ở Bước 6).
- `assets/fonts/`: phông chữ đã kèm. `mau/timeline_mau.json`: timeline mẫu.

## Lưu ý
- Claude Code không bịa ảnh hay số liệu: dữ liệu thật bạn phải cung cấp.
- Phông chữ kèm theo chỉ dùng nếu bạn có quyền sử dụng; thiếu thì cài phông riêng vào `assets/fonts/`.
