# Làm một video, từ chủ đề đến đăng

Lập 12/11/2026, theo hệ thống hiện tại (app studio trên PC). Thay cho `99-luu-tru/QUY-TRINH-FORM-GITHUB.md` và `99-luu-tru/QUY-TRINH-CAT-GHEP.md`.
Câu lệnh cho từng bước: `mau/PROMPT-MAU.md` (cùng số thứ tự). Chọn AI: `01-he-thong/AI-NAO-VIEC-NAO.md`.

| # | Bước | Ai / công cụ | Ở đâu | Ra gì | Xong khi |
|---|---|---|---|---|---|
| 0 | Tạo thư mục video | Hào bấm ＋ trong app studio (hoặc Claude Code) | PC | `projects/<tên>/` có sẵn các file mẫu | Tên đúng quy ước `THU-MUC-VA-DAT-TEN.md` |
| 1 | Chọn góc | Claude | điện thoại | `BRIEF.md` | Có "một ý khách cần nhớ" |
| 2 | Lấy số liệu | NotebookLM + Hào xác nhận | điện thoại / máy tính | `NGUON-SO-LIEU.md` | Mỗi số có nguồn + ngày + "đã xác nhận" |
| 3 | Tin mới (nếu cần) | Claude tìm web | điện thoại | thêm dòng vào `NGUON-SO-LIEU.md` | Có đường dẫn gốc |
| 4 | Kịch bản | Claude | điện thoại | `KICH-BAN.md` | Qua 4 ô kiểm cuối mẫu |
| 5 | Kiểm chéo (video quan trọng) | ChatGPT hoặc Gemini | điện thoại | ghi chú sửa | Đã sửa hoặc bỏ qua có lý do |
| — | **Quay** | Hào | ngoài hiện trường | footage vào `D:\HaoSkyLand\01-footage\<dự án>\<ngày_nơi>` | |
| 6 | Storyboard (video ghép cảnh) | Claude Code, skill `lap-storyboard` | PC | `STORYBOARD.md`, `timeline.json` | **Hào duyệt** |
| 6b | Video nói trước máy | App: Cắt → ✨ Master cut | PC | `timeline.json` đã cắt, báo cáo | Hào xem lại trong app |
| 7 | Phụ đề | App: Phụ đề → Tạo phụ đề từ giọng nói | PC | phụ đề trong timeline | Hào đọc lại tên riêng, số |
| 8 | Chữ, zoom, cảnh trám, chuyển cảnh, nhạc | Hào trong app (hoặc Claude Code sửa bằng lời) | PC / điện thoại cùng wifi | `timeline.json` | Xem trước ổn |
| 9 | Dựng nháp → xem → Xuất video | App | PC | `out/<tên>.mp4` | |
| 10 | Nghiệm thu | Claude Code, skill `bao-cao-nghiem-thu` | PC | `out/<tên>-baocao.md` | Không còn mục "chưa đạt" quan trọng |
| 11 | Chỉnh tay (nếu cần) | Premiere / DaVinci qua nút "Premiere/DaVinci" | PC | file dự án phần mềm đó | |
| 12 | Gói đăng | Claude + Canva | điện thoại | `DANG-BAI.md`, ảnh bìa | |
| 13 | **Đăng** | **Hào** | điện thoại | bài đăng | Claude không đăng |
| 14 | Ghi kết quả +1/+3/+7 ngày | Hào ghi, Claude tổng hợp cuối tuần | điện thoại | `KET-QUA.md` | |
| 15 | Bản khung kia (TikTok ↔ YouTube) | App: Khung hình → Nhân bản | PC | thư mục mới, cùng footage | Lặp lại 8–14 |

## Rút gọn khi bận (video nói trước máy, 60 giây)
1 → 2 → 4 → quay → 0 → 6b → 7 → 9 → 13. Bỏ 5, 10, 11 nếu không có số liệu mới.

## Khi gặp lỗi
- App báo lỗi đỏ: chụp màn hình, gửi Claude Code trên PC (hoặc phiên cloud kèm file `projects/<tên>/build/*.log`).
- Video có `[...]`: số liệu chưa xác nhận, quay lại bước 2.
- Cần quay lại bản cũ: app → Lịch sử (30 bản gần nhất).

## Quy tắc an toàn
- Không đăng, không gửi khách khi Hào chưa đồng ý.
- Không cam kết lợi nhuận hay tăng giá; luôn nêu rủi ro cạnh lợi ích.
- Không đưa thông tin khách, thu nhập, khoá API vào repo.
