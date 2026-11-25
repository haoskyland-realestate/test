# Kiến trúc hệ thống (cập nhật 25/11/2026)

Chỉ ghi những gì đã có bằng chứng trong mã. Chưa chạy thử thì ghi "chưa thử". Chi tiết từng tính năng dựng video: bảng "Trạng thái" trong `CLAUDE.md`.

## 1. Danh mục (repository và nguồn ngoài)
| Thành phần | Vai trò | Ghi chú |
|---|---|---|
| Repo `haoskyland-realestate/test` (riêng tư) | Toàn bộ mã, tài liệu, skill, dữ liệu nghiên cứu | Làm việc trên nhánh `claude/...`, `main` chỉ gộp PR khi Hào cho phép |
| `coreyhaines31/marketingskills` (MIT) | 6 skill viết content, chép vào `.claude/skills/` | Nguồn, commit: `.claude/skills/viet-content-hao/NGUON.md` |
| `ScrapeCreators/social-media-research-skills` (MIT) | 7 skill, hiện chưa dùng được (thiếu API key hợp lệ) | `.claude/skills/scrapecreators-api/NGUON.md` |
| Google Sheet "Hào Sky Land - Kế hoạch content hằng ngày" | Bảng kế hoạch, kho ý tưởng, nguồn, theo dõi kết quả | 5 tab: Hôm nay, Kho ý tưởng, Lịch tuần, Theo dõi kết quả, Nguồn |
| Telegram bot `HSL_Content_bot` | Nơi Hào nhận tin 7:00 và 22:00 | Token và chat id nằm trong GitHub Secrets, không có trong repo |
| GitHub Actions | CI (`kiem-tra.yml`), Pages, render, gửi Telegram (`telegram-ban-tin.yml`) | Lịch chạy chỉ hoạt động từ `main` |
| Tác vụ theo lịch (Claude Code cloud) | Agent soạn bản tin: sáng 6:30 (bật), tối 21:40 (tắt) | Chưa gắn kết nối Gmail, Google Sheets |

## 2. Trách nhiệm từng phần trong repo
| Vùng | Trách nhiệm |
|---|---|
| `video-studio/scripts/` (Python, Node) | Dựng video (`dung.py`), agent video (`agent.py`), cắt, phụ đề, màu, âm; công cụ content: `doc_bai_bao.py`, `nghien_cuu_tiktok.py`, `phan_tich_giong_nguoi_noi.py`, `gui_telegram.sh` |
| `video-studio/studio/` | App timeline (máy chủ Python + trang web) |
| `video-studio/engines/` | HyperFrames (chính), Remotion, Manim, Blender |
| `video-studio/nghien-cuu/` | Danh sách kênh (`kenh.txt`), kết quả phân tích, bản tin Telegram (`ban-tin/`) |
| `.claude/skills/` | 22 skill: 8 của dự án video, 7 ScrapeCreators, 6 marketingskills, 1 skill nối `viet-content-hao` |
| `docs/` | Tài liệu theo thư mục đánh số, mục lục `docs/00-MUC-LUC.md` |

## 3. Luồng dữ liệu của trợ lý content
```
Báo uy tín --doc_bai_bao.py (kiểm câu trích nguyên văn)--> agent (skill viet-content-hao)
Kênh tham khảo --nghien_cuu_tiktok.py--> kết quả nghien-cuu/ket-qua/
agent --> Google Sheet (5 tab)
agent --> nghien-cuu/ban-tin/sang.txt | toi.txt --> nhánh claude/awesome-noether-0ega8l
GitHub Actions (00:00 và 15:00 UTC) --gui_telegram.sh--> Telegram
agent --> Gmail (email cho Hào)
```
`gui_telegram.sh` chỉ gửi file có dòng đầu `NGAY: <hôm nay theo giờ Việt Nam>`; sai ngày thì gửi cảnh báo, không gửi tin cũ.

## 4. Phụ thuộc và tương thích
| Phần | Phiên bản (theo CI `kiem-tra.yml`) |
|---|---|
| Python | 3.12 (CI), thư viện: numpy, faster-whisper, opencv-python-headless<5, opentimelineio, onnxruntime, yt-dlp, playwright |
| Node | 22; `video-studio/package.json` có 3 dependency |
| FFmpeg | cài bằng apt (Ubuntu) và choco (Windows) |
| Hệ điều hành | CI chạy Ubuntu và Windows; Mac đã thử tay 14/11 |

Công cụ content chỉ dùng thư viện chuẩn của Python, ngoại trừ `yt-dlp` (đã có trong CI).

## 5. Ràng buộc vận hành và rủi ro đã biết
- Môi trường cloud "test" đã mở thêm 22 tên miền (TikTok, YouTube, 9 báo): dùng chung cho mọi phiên của môi trường này.
- YouTube chặn IP cloud ("Sign in to confirm you're not a bot"): phân tích cách nói phải chạy trên PC (`phan-tich-giong-nguoi-noi.bat`).
- Telegram từ máy GitHub từng bị hết thời gian chờ và 429 (24/11); thông lại ngày 25/11. Nguyên nhân chưa rõ.
- GitHub chạy lịch có thể trễ nhiều giờ (đã gặp 25/11); workflow chọn tin sáng hay tối theo `github.event.schedule`.
- Lần agent tự chạy bản tin đầu tiên (26/11) chưa được kiểm chứng.
