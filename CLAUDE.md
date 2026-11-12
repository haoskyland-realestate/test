# CLAUDE.md — Hồ sơ dự án Cloud Edit Video (Hào Sky Land)

File này Claude Code tự đọc mỗi phiên. Hào không cần nhắc lại những gì ghi ở đây. Quy trình chi tiết: `docs/QUY-TRINH.md`.

## Mục đích
Làm video ngắn đăng TikTok (9:16) và YouTube (16:9) cho thương hiệu Hào Sky Land: bất động sản, góc nhìn dòng tiền, khách mục tiêu là nữ 35–55 tuổi ở trung tâm và khu Đông TP.HCM.

## Người dùng
- Hào, không rành code. Giao việc kiểu "làm giúp tôi"; Claude tự chọn phương án đơn giản nhất và báo lại ngắn gọn bằng tiếng Việt.
- Giải thích thuật ngữ tiếng Anh bằng tiếng Việt trước.
- Giỏ hàng hiện tại: Vinhomes Hóc Môn, Vinhomes Cần Giờ. Các dự án khác chỉ là đã nghiên cứu, không phải đang phân phối.

## Bối cảnh bổ sung (Hào xác nhận 12/11/2026)
- Repo riêng tư. Hào có thể dành cả ngày cho dự án, giới hạn là token.
- Giọng đọc: Hào tự thu. Video đầu: TikTok khoảng 130 giây, từ kịch bản thô, flycam thô, giọng thu và video mẫu cắt cảnh. Hào có bộ logo và màu thương hiệu riêng (chưa gửi).
- Cách làm chính là **cắt ghép**: `docs/QUY-TRINH-CAT-GHEP.md`. Mẫu đồ họa HyperFrames dùng cho cảnh chữ/số, không phải nguồn chính.

## Cấu trúc
- `video-studio/videos/*.json`: nội dung video (spec). Trường `template` chọn mẫu.
- `video-studio/engines/hyperframes/templates/`: **thư viện mẫu** (cashflow-3d có khối 3D, text-only). Thêm mẫu mới: xem README trong thư mục đó.
- `video-studio/scripts/assemble.mjs`: cắt ghép flycam + giọng + logo + phụ đề theo `projects/<tên>/edl.json`. `contact-sheet.sh`: ảnh lưới chọn cảnh.
- `video-studio/scripts/render.sh`: spec → engine → FFmpeg → MP4 trong `out/`.
- `video-studio/engines/`: hyperframes (chính), remotion (dự phòng), manim, blender.
- `video-studio/app/`: PWA soạn spec. `.github/workflows/render.yml`: render trên GitHub bằng form. `pages.yml`: đưa trang cũ (`index.html` gốc) và app (`/app/`) lên Pages.
- Windows 11 local: `setup-windows.ps1` (một lần), `chay-video.bat`.

## Trạng thái (cập nhật 12/11/2026)
| Thành phần | Trạng thái |
|---|---|
| HyperFrames + GSAP + three.js | Render OK trong sandbox và trên GitHub Actions |
| Remotion | Render OK trong sandbox (cần Chromium) |
| FFmpeg | OK |
| Cắt ghép (`assemble.mjs`) | Đã dựng video mẫu 33s (`projects/demo`) với cảnh giả, giọng máy, nhạc giả; chưa thử flycam/giọng thật |
| Video test 89s (`projects/test90`) | Hào duyệt "rất ok" 12/11; âm thanh hiệu ứng chưa ổn, chờ thư mục âm thanh. Footage và bản dựng test đã xóa theo yêu cầu (bản gốc còn trên Drive thư mục "Hào") |
| Tải từ Drive trên cloud | Được: môi trường cloud "test" mở mạng tới drive.usercontent.google.com; thư mục phải chia sẻ bằng link |
| Nhận dạng giọng (`hyperframes transcribe`) | Có lệnh, chưa thử tiếng Việt |
| Manim | Có mã, chưa chạy thử |
| Blender MCP | Mới có hướng dẫn, chưa thử |
| Codespaces (`.devcontainer`) | Chưa thử |
| Windows 11 (`setup-windows.ps1`, `chay-video.bat`) | Chưa thử |
| Trang Pages cũ | Có thể đã bị app thay ở gốc; cần chạy lại "Deploy site" và kiểm tra |

## Hệ thống làm việc (Hào chốt 12/11/2026)
`docs/HE-THONG.md`: Anti xây phần mềm · GitHub giữ mã và bản v1 chạy tạm · **PC Windows 11 làm việc nặng** (tải footage, dựng) · Mac đọc báo cáo và nghiệm thu · điện thoại giao việc. Skill dự án: `.claude/skills/` (lap-storyboard, dung-video, bao-cao-nghiem-thu); MCP: `mcp/README.md`.

## Kế hoạch đang theo
`docs/KE-HOACH-APP.md`: định dạng timeline → thư viện hiệu ứng → app timeline (PWA PC + điện thoại) → máy chủ cục bộ Windows → âm thanh.

## Quy tắc làm việc
- Phiên bản nhỏ nhất chạy được trước, mở rộng sau. Không thêm công cụ mới khi chưa dùng hết công cụ hiện có.
- Chưa chạy thử thì ghi "chưa thử", không nói đã xong.
- **Phải hỏi Hào trước:** đăng nội dung công khai, gửi tin cho khách, xóa hoặc ghi đè dữ liệu quan trọng, thay đổi trang đang chạy công khai, phát sinh chi phí. Gộp PR chỉ làm khi Hào cho phép trong phiên đó.
- Đẩy mã lên nhánh `claude/...`, không đẩy thẳng `main`, không ghi đè lịch sử.
- Không đưa vào repo: thu nhập, ngày sinh, thông tin khách, khóa API, token.

## Quy tắc nội dung video bất động sản
- Giọng mộc mạc, thật, ít chữ, có thông tin. Hook rõ trong 2–3 giây đầu. Rất ít emoji.
- Xưng "em" với khách lớn tuổi, "tôi" khi phân tích kiểu chuyên gia.
- Nêu cả lợi ích và rủi ro; ưu tiên số cụ thể (dòng tiền mỗi tháng sau khi trừ tiền vay).
- Mọi dữ kiện dự án (giá, chính sách, tiến độ, pháp lý) phải có nguồn và ngày cập nhật. Chưa xác minh thì để `[...]`, không tự điền.
- Tránh: "cơ hội vàng", "sinh lời chắc chắn", "cam kết lợi nhuận", "cháy hàng", "chốt ngay kẻo lỡ", "sốt đất", "x2 tài sản". Không tạo khan hiếm giả.

## Việc tiếp theo
1. Hào xem video mẫu, chọn engine mặc định.
2. Chạy lại "Deploy site", kiểm tra trang cũ và `/app/`.
3. Làm video thật đầu tiên: chọn một góc dòng tiền cho Vinhomes Hóc Môn hoặc Cần Giờ, có nguồn và ngày.
4. Thử Windows 11 với `setup-windows.ps1`.
