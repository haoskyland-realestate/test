# Quy trình làm video (TikTok / YouTube)

Mục tiêu: mỗi tuần ra video đều, không để việc viết kịch bản và dựng làm Hào trì hoãn. Hào chỉ cần chọn chủ đề và sửa; phần còn lại có sẵn.

## Nhịp tuần
| Ngày | Việc | Ai làm | Ra gì |
|---|---|---|---|
| Thứ 2 | Chọn 1 góc phân tích dòng tiền hoặc 1 câu khách hay hỏi | Hào | 1 dòng chủ đề |
| Thứ 2 | Soạn bản nháp: hook, 3 ý chính, lời kêu gọi | Claude | Spec JSON + lời đọc |
| Thứ 3 | Kiểm dữ kiện: nguồn và ngày cho mọi con số | Hào (Claude hỗ trợ tra) | Spec không còn `[...]` |
| Thứ 3 | Render và xem thử | Hào bấm, Claude xử lý lỗi | MP4 |
| Thứ 4 | Đăng TikTok / YouTube | Hào | Bài đăng |
| Chủ nhật | Xem bài nào có tương tác hoặc tin nhắn từ đúng nhóm khách | Hào + Claude | Giữ lại, phát triển tiếp |

Claude chỉ chuẩn bị bản nháp. Đăng bài và nhắn khách luôn do Hào quyết định.

## Làm một video, từng bước
1. **Chủ đề.** Hào nói một câu, ví dụ "dòng tiền Vinhomes Cần Giờ cho người giữ 5 năm". Claude hỏi lại tối đa 3 câu nếu thiếu thông tin trọng yếu.
2. **Bản nháp.** Claude viết hook, 3 ý chính, kết. Văn phong theo `CLAUDE.md`. Chỗ chưa có số liệu thật để `[...]`.
3. **Kiểm dữ kiện.** Mỗi số liệu có nguồn (chủ đầu tư, văn bản nhà nước, báo uy tín) và ngày. Chưa xác minh thì bỏ khỏi video hoặc nói rõ là ước tính.
4. **Render.** Cách dễ nhất, làm từ điện thoại hoặc máy tính:
   GitHub → Actions → **Render video** → Run workflow → điền tiêu đề, hook, ý chính (ngăn bằng `|`), TikTok hoặc YouTube, số giây → chờ khoảng 2 phút → mở run → mục **Artifacts** → tải `video`.
5. **Xem và sửa.** Chữ sai, ý thừa thì sửa nội dung rồi render lại. Không sửa mã.
6. **Đăng.** Hào đăng, kèm mô tả ngắn và một lời kêu gọi tự nhiên (nhắn tin để nhận bảng dòng tiền, ví dụ).
7. **Ghi lại.** Vài chữ: chủ đề, ngày đăng, kết quả (lượt xem, tin nhắn). Dùng cho tổng kết tuần.

## Chọn mẫu (chỉ hyperframes)
Mặc định `cashflow-3d` (chữ + khối 3D). Muốn nhẹ hơn dùng `text-only`. Thêm mẫu mới theo `video-studio/engines/hyperframes/templates/README.md`.

## Chọn engine
- **hyperframes** (mặc định): chữ chuyển động và khối 3D. Đã chạy ổn.
- **remotion**: dự phòng, chỉ chữ ở bản mẫu. Đọc kỹ giấy phép nếu bán dịch vụ làm video.
- **manim**: biểu đồ động cho số liệu. Chưa thử.
- **Blender MCP**: cảnh 3D, chỉ làm trên máy Windows local. Chưa thử.

## Khi gặp lỗi
- Render đỏ trên Actions: gửi đường dẫn run cho Claude, Claude đọc log và sửa.
- Video có chữ `[...]`: chưa điền số liệu thật, quay lại bước 3.
- Không hiện nút Run workflow: workflow chưa nằm trên `main`.

## Chuyển sang Windows 11 (sau này)
1. Chạy `video-studio/setup-windows.ps1` một lần, đóng và mở lại PowerShell.
2. Bấm đúp `chay-video.bat` để render `videos/demo.json`.
3. Khi ổn định mới thêm Blender MCP và PC RTX 5060. Chưa thử trên Windows.

## Quy tắc an toàn
- Không đăng, không gửi khách khi chưa có sự đồng ý của Hào.
- Không cam kết lợi nhuận hay tăng giá. Luôn nêu rủi ro cạnh lợi ích.
- Không đưa thông tin khách, thu nhập, khóa API vào repo.

## Mốc 4 tuần đầu
- Tuần 1: xem video mẫu, chốt engine, đăng 1 video thật đầu tiên.
- Tuần 2–3: 2 video mỗi tuần, ghi lại kết quả.
- Tuần 4: xem lại bài nào hiệu quả, quyết định có thử Manim hoặc Windows local không.
Không tăng khối lượng khi chưa giữ đều được nhịp 1–2 video mỗi tuần.
