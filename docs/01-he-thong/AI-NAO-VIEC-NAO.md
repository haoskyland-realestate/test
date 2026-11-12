# AI nào làm việc nào

Lập 12/11/2026. Claude đọc file này trước khi nhận một việc mới, để biết nên tự làm hay đề xuất Hào chuyển sang công cụ khác. Hào đọc file này khi phân vân "việc này hỏi AI nào".

Khả năng và hạn mức của từng AI thay đổi theo gói và theo thời gian. Mục nào ghi **(kiểm lại)** là chưa xác minh với gói Hào đang dùng.

---

## 1. Năm câu hỏi để chọn đúng AI (đi từ trên xuống, gặp "có" thì dừng)

| # | Câu hỏi | Nếu "có" thì dùng |
|---|---|---|
| 1 | Việc này **gửi cho khách, đăng công khai, tốn tiền** hay **xoá dữ liệu**? | **Không giao AI làm.** AI chỉ soạn nháp, Hào bấm gửi/đăng/xoá |
| 2 | Cần **sửa file trong repo, chạy lệnh, dựng video, xử lý footage**? | **Claude Code**: phiên cloud nếu không cần footage, **PC Windows** (Anti hoặc `claude remote-control`) nếu cần footage |
| 3 | Câu trả lời phải **dựa trên tài liệu gốc có trích dẫn** (hồ sơ chủ đầu tư, pháp lý, bảng giá)? | **NotebookLM**: chỉ trả lời từ nguồn đã nạp, có chỉ chỗ trích. Kết quả chép sang `NGUON-SO-LIEU.md` của video kèm nguồn + ngày |
| 4 | Cần **viết tiếng Việt theo giọng Hào** (kịch bản, caption, tin nhắn nháp), phân tích, lập kế hoạch? | **Claude** (app/chat). Cần lưu thành file trong dự án thì dùng **Claude Code** |
| 5 | Cần **hình ảnh**: ảnh bìa, ảnh minh hoạ, đồ hoạ? | **Canva** (có kết nối sẵn với Claude) cho ảnh bìa theo mẫu thương hiệu; **ChatGPT** tạo ảnh minh hoạ. Ảnh AI phải ghi "ảnh minh hoạ" |

Không câu nào khớp: hỏi Claude trước, Claude sẽ chỉ chỗ.

**Không AI nào là nguồn số liệu.** Giá, chính sách, tiến độ, pháp lý chỉ lấy từ văn bản gốc (chủ đầu tư, cơ quan nhà nước) hoặc báo uy tín, có ngày. AI chỉ giúp đọc, tóm tắt, đối chiếu.

---

## 2. Bảng nhanh: việc → AI

| Việc | AI chính | Dự phòng | Đầu vào | Đầu ra, lưu ở đâu |
|---|---|---|---|---|
| Đọc hồ sơ dự án (PDF chủ đầu tư, bảng giá, pháp lý), hỏi đáp có trích dẫn | NotebookLM | Claude (đính kèm file) | File gốc từ chủ đầu tư/đại lý | `NGUON-SO-LIEU.md` trong thư mục video: số liệu + nguồn + ngày |
| Tìm tin mới trên mạng (lãi suất, hạ tầng, tin dự án) | Claude (tìm web) | Gemini, ChatGPT | Câu hỏi + khoảng thời gian | Đường dẫn gốc + ngày, chép vào `NGUON-SO-LIEU.md` |
| Chọn góc nội dung tuần, lên ý tưởng | Claude | ChatGPT | Nhóm khách, câu khách hay hỏi, kết quả tuần trước | `BRIEF.md` |
| Viết kịch bản, hook, lời đọc | Claude | ChatGPT (xin thêm 3 hook khác để so) | `BRIEF.md`, `NGUON-SO-LIEU.md` | `KICH-BAN.md` |
| Kiểm chéo kịch bản (giọng, từ cấm, lời hứa quá đà) | Claude (lượt đọc riêng, "đóng vai khách 45 tuổi khó tính") | ChatGPT hoặc Gemini (góc nhìn thứ hai) | `KICH-BAN.md` | Ghi chú sửa ngay trong file |
| Chọn cảnh từ footage, lập storyboard | Claude Code (skill `lap-storyboard`) | — | Thư mục footage + `KICH-BAN.md` | `STORYBOARD.md` + `timeline.json` |
| Cắt khoảng lặng, bỏ câu vấp, chọn khúc đẹp | App studio: nút **Master cut** (chạy trên máy, không cần mạng) | auto-editor (chưa tích hợp) | Footage nói trước máy | `timeline.json`, báo cáo `build/master-cut.md` |
| Phụ đề tiếng Việt từ giọng nói | App studio: nút **Tạo phụ đề** (faster-whisper chạy trên máy) | Claude sửa chính tả sau | Footage có giọng | Phụ đề trong `timeline.json`; xuất `.srt` |
| Sửa timeline bằng lời ("đổi chữ cảnh 3", "thêm zoom") | Claude Code | Sửa tay trong app studio | `timeline.json` | `timeline.json` (app tự giữ 30 bản cũ ở Lịch sử) |
| Áp phong cách + nhịp chuyển cảnh + hiệu ứng âm theo video mẫu | App studio: Thương hiệu → **Mẫu edit → Áp mẫu** (không cần AI) | Claude Code: `scripts/ap_mau.py` | `timeline.json` | `timeline.json` (hàng ♪ Hiệu ứng âm) |
| Phân tích video mẫu Hào tìm được thành mẫu mới | Claude Code (xem khung hình, phổ âm) | — | File video mẫu | `video-studio/thu-vien-mau/<mẫu mới>/` |
| Dựng video | App studio (Dựng nháp / Xuất video) trên PC | Claude Code (skill `dung-video`) | `timeline.json` + footage | `video-studio/out/<tên>.mp4` |
| Chỉnh tay chi tiết (màu kỹ, hiệu ứng đặc biệt) | Premiere / DaVinci (nút "Premiere/DaVinci" trong app) | CapCut | `.xml` / `.otio` / `.srt` | File dự án của phần mềm đó |
| Nghiệm thu video | Claude Code (skill `bao-cao-nghiem-thu`) | Hào xem trên Mac/điện thoại | `out/<tên>.mp4` | `out/<tên>-baocao.md` |
| Ảnh bìa (thumbnail) | Canva (Claude gọi được qua kết nối) | ChatGPT tạo ảnh | Tiêu đề, ảnh khung đẹp nhất | Thư mục thành phẩm |
| Ảnh/clip minh hoạ không có thật (phòng khách mẫu, sơ đồ dòng tiền) | ChatGPT tạo ảnh; công cụ tạo video AI **(kiểm lại công cụ, giấy phép)** | Mẫu HyperFrames trong repo | Mô tả chi tiết (xem prompt mẫu) | Ghi rõ "ảnh minh hoạ" trên video |
| Caption, mô tả, hashtag khi đăng | Claude | ChatGPT | `KICH-BAN.md` | `DANG-BAI.md` trong thư mục video |
| Tổng kết tuần (bài nào có tin nhắn đúng khách) | Claude (đọc số liệu Hào dán, hoặc Google Sheets qua kết nối) | — | Số liệu từ TikTok/YouTube Studio | `KET-QUA.md` trong thư mục video, tổng hợp tuần |
| Viết, sửa phần mềm của hệ thống này | Claude Code trong Anti (PC) | Claude Code phiên cloud | Repo | Đẩy lên nhánh `claude/...` |
| Việc văn phòng trên máy (sắp file, đổi tên hàng loạt) | Claude Code trên PC | — | Thư mục trên PC | Theo quy ước `THU-MUC-VA-DAT-TEN.md` |

---

## 3. Từng AI: dùng khi nào, không dùng khi nào

### 3.1 Claude (app trên điện thoại / máy tính, claude.ai)
- **Dùng khi:** viết tiếng Việt theo giọng Hào; phân tích dòng tiền; lập kế hoạch; đọc file đính kèm; tìm tin trên web; làm việc với Google Drive, Docs, Sheets, Gmail (chỉ soạn nháp), Lịch, Notion, Canva qua kết nối (connector: chỗ nối Claude với ứng dụng khác) đã bật.
- **Không dùng khi:** cần chạy lệnh, sửa nhiều file trong repo, xử lý video (dùng Claude Code); cần câu trả lời chỉ dựa trên tài liệu gốc (dùng NotebookLM).
- **Lưu ý:** Claude đã có hồ sơ của Hào (Personal Instructions). Trong repo này còn có `CLAUDE.md`.

### 3.2 Claude Code: phiên cloud (giao từ điện thoại)
- **Dùng khi:** viết/sửa mã, viết tài liệu trong repo, lập storyboard từ Drive, sửa `timeline.json`, việc không cần footage nặng.
- **Không dùng khi:** cần footage 4K lâu dài (máy cloud bị xoá khi phiên kết thúc; chỉ còn những gì đã đẩy lên GitHub); cần mở CapCut/Premiere.
- **Lưu ý:** mạng của phiên cloud (môi trường "test") mở thêm Google Drive và Hugging Face (nơi tải mô hình nhận dạng giọng); trang ngoài danh sách có thể bị chặn, cần mở thêm trong cài đặt môi trường.

### 3.3 Claude Code trên PC Windows (trong Anti, hoặc `claude remote-control` để điều khiển từ điện thoại)
- **Dùng khi:** việc nặng có footage: tạo dự án từ thư mục footage, master cut, phụ đề, dựng, nghiệm thu, xuất Premiere/DaVinci; sắp xếp thư mục footage.
- **Không dùng khi:** máy tắt hoặc ngủ (việc treo giữa chừng).
- **Lưu ý:** skill trong `.claude/skills/` dùng được ở đây. **Chưa thử trên PC.**

### 3.4 Anti (Google Antigravity)
- **Dùng khi:** xây phần mềm trên PC: mở repo, xem mã, chạy app studio, Claude Code chạy bên trong.
- **Không dùng khi:** chỉ cần viết nội dung (dùng Claude app cho nhẹ).
- **Lưu ý:** Anti đọc cùng `CLAUDE.md` và `docs/` nên theo cùng quy tắc.

### 3.5 NotebookLM (Google)
- **Dùng khi:** nạp hồ sơ dự án (PDF, Google Docs, đường dẫn web, video YouTube) rồi hỏi: "chính sách thanh toán đợt 1 là gì, trang nào?". Mỗi dự án bất động sản một sổ (notebook) riêng, ví dụ "Vinhomes Hóc Môn – hồ sơ 11/2026".
- **Không dùng khi:** viết kịch bản theo giọng Hào (dùng Claude); tìm tin mới chưa có trong nguồn đã nạp.
- **Lưu ý:** chỉ đúng như tài liệu đã nạp: tài liệu cũ thì câu trả lời cũ. Ghi ngày của tài liệu vào tên nguồn. Hạn mức số nguồn **(kiểm lại)**.

### 3.6 ChatGPT (OpenAI)
- **Dùng khi:** cần góc nhìn thứ hai (xin thêm hook, so hai cách mở đầu); tạo ảnh minh hoạ.
- **Không dùng khi:** làm nguồn số liệu; việc cần đọc repo này.
- **Lưu ý:** ChatGPT không đọc `CLAUDE.md`. Dán kèm phần "Quy tắc nội dung" (giọng, từ cấm) mỗi lần nhờ viết.

### 3.7 Gemini (Google)
- **Dùng khi:** góc nhìn thứ hai; việc đang nằm trong Google Docs/Gmail/Drive mà Hào mở sẵn.
- **Không dùng khi:** làm nguồn số liệu; việc trong repo.
- **Lưu ý:** tính năng thay đổi theo gói **(kiểm lại)**. Như ChatGPT, phải dán kèm quy tắc nội dung.

### 3.8 AI chạy ngay trên máy (đã có trong app studio, miễn phí, không gửi dữ liệu ra ngoài)
| Công cụ | Nút trong app | Làm gì | Ghi chú |
|---|---|---|---|
| faster-whisper (mô hình large-v3-turbo) | Phụ đề → "Tạo phụ đề từ giọng nói" | Nghe giọng tiếng Việt, ra phụ đề có mốc từng từ | Lần đầu tải mô hình khoảng 1,6 GB; có card NVIDIA thì nhanh hơn |
| Master cut (đo âm lượng + OpenCV chấm điểm khung hình) | Cắt → "✨ Master cut" | Cắt im lặng, bỏ câu vấp, chọn khúc đẹp, phóng xen kẽ | Không phải AI tạo sinh, là đo đạc; ngưỡng mới chỉnh trên vài clip |

### 3.9 Phần mềm dựng tay (không phải AI, nằm cuối dây chuyền)
- **Premiere Pro / DaVinci Resolve:** chỉnh màu kỹ, hiệu ứng đặc biệt. Nhận file `.xml`/`.otio` từ app. **Chưa mở thử.**
- **CapCut:** chỉnh nhanh trên điện thoại/máy tính, mẫu xu hướng. Chưa rõ nhận file xuất từ app **(kiểm lại)**.

---

## 4. Chuyền việc giữa các AI: luôn qua file trong thư mục video

Mỗi video có một thư mục `video-studio/projects/<tên>/`. Mọi AI đọc và ghi vào đó, nên đổi AI giữa chừng không mất gì:

```
BRIEF.md          ← mục tiêu, nhóm khách, góc dòng tiền        (Claude + Hào)
NGUON-SO-LIEU.md  ← số liệu + nguồn + ngày                    (NotebookLM → Hào xác nhận)
KICH-BAN.md       ← hook, lời đọc, chữ trên màn hình           (Claude)
STORYBOARD.md     ← cảnh nào, giây nào                         (Claude Code)
timeline.json     ← file dựng                                  (app studio / Claude Code)
DANG-BAI.md       ← tiêu đề, mô tả, hashtag, ảnh bìa           (Claude)
KET-QUA.md        ← lượt xem, tin nhắn đúng khách, bài học     (Hào ghi, Claude tổng hợp)
```
Mẫu các file: `mau/du-an-video/`. Với AI ngoài repo (ChatGPT, Gemini, NotebookLM): dán nội dung file vào, lấy kết quả dán ngược lại vào file.

---

## 5. Câu lệnh mẫu

Mỗi câu lệnh thay phần `<...>`. Bản đầy đủ để chép: `mau/PROMPT-MAU.md`.

- **NotebookLM, đọc hồ sơ:** "Liệt kê mọi con số về giá, diện tích, chính sách thanh toán, tiến độ trong các nguồn. Mỗi dòng: con số, nguồn nào, trang nào, ngày của tài liệu. Không suy đoán ngoài tài liệu."
- **Claude, kịch bản:** "Đọc `BRIEF.md` và `NGUON-SO-LIEU.md` của `<tên>`. Viết kịch bản TikTok `<số>` giây theo quy tắc nội dung trong `CLAUDE.md`. Hook trong 3 giây đầu. Số nào chưa có trong `NGUON-SO-LIEU.md` để `[...]`."
- **ChatGPT/Gemini, góc nhìn thứ hai:** "Đây là quy tắc giọng: `<dán mục Quy tắc nội dung>`. Đây là kịch bản: `<dán>`. Đóng vai một chị 45 tuổi có 30 tỷ, chỉ ra 3 chỗ chị thấy không tin hoặc khó hiểu. Không viết lại."
- **Claude Code, từ điện thoại:** "Tạo storyboard cho dự án `<tên>` từ thư mục Drive `<link>`, theo `KICH-BAN.md`." / "Sửa timeline `<tên>`: `<yêu cầu>`."

---

## 6. Những việc Claude phải tự đề xuất chuyển AI

Claude nói rõ một câu, ví dụ "việc này nên làm bằng NotebookLM vì…", khi:
- Hào hỏi số liệu dự án mà chưa có tài liệu gốc → đề nghị Hào gửi tài liệu, nạp vào NotebookLM, rồi chép kết quả vào `NGUON-SO-LIEU.md`.
- Việc cần footage mà đang ở phiên cloud → đề nghị làm trên PC.
- Hào nhờ "đăng", "gửi khách" → Claude chỉ soạn nháp, nhắc Hào tự bấm.
- Hào xin ảnh dự án thật → không tạo ảnh AI giả làm ảnh thật; dùng ảnh gốc của chủ đầu tư hoặc ghi "ảnh minh hoạ".

## 7. Chi phí
Mặc định dùng gói đang có, không đăng ký thêm. Công cụ nào cần trả phí thì Claude hỏi Hào trước. Hạn mức từng gói **(kiểm lại)** khi Hào bắt đầu dùng đều.
