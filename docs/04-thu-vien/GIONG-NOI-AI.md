# Giọng nói AI (Voice Studio): tìm hiểu trước khi tích hợp

Lập 13/11/2026 bằng cách đọc mã nguồn và tài liệu gốc của từng repo (bản mới nhất ngày 12/11/2026). **Chưa cài, chưa chạy thử** cái nào. Số sao, phiên bản có thể đổi.

## Kết luận ngắn
- **Giọng tiếng Việt cho video của Hào: ưu tiên `CIT Voice Studio`.** Làm riêng cho tiếng Việt, giấy phép thoáng (Apache-2.0, mô hình VieNeu-TTS cũng Apache-2.0, ghi rõ dùng được cho thương mại), có bản cài Windows, chạy không cần mạng, có API để app studio gọi.
- **`VoiceStudio` (debpalash):** mạnh hơn, nhiều tính năng hơn, **có sẵn skill cho Claude và MCP**. Nhưng giấy phép AGPL-3.0, không chép mã vào repo của mình được. Bản chạy nhanh bằng card màn hình (OmniVoice GGUF) **chỉ cho dùng phi thương mại**. Hợp để thử, hoặc làm lồng tiếng sang tiếng Anh sau này.
- Hào đang **tự thu giọng**: giọng AI dùng để (1) nghe thử kịch bản trước khi quay, (2) **nhân bản giọng của chính Hào** để sửa một chữ đọc vấp mà khỏi quay lại, (3) làm video lúc bận. Chỉ nhân bản giọng mình có quyền dùng, và nên ghi chú khi cả video là giọng AI.

## So sánh

| | CIT Voice Studio | VoiceStudio |
|---|---|---|
| Repo | `Cuongyd196/cit-voice-studio` (★175) | `debpalash/VoiceStudio` (★~109 nghìn) |
| Tiếng Việt | **25 giọng Việt có sẵn, ba miền Bắc – Trung – Nam**, đọc xen tiếng Anh | Có trong mô hình mặc định OmniVoice (646 ngôn ngữ; tiếng Việt khoảng 8.500 giờ dữ liệu); chưa nghe thử chất lượng |
| Nhân bản giọng | Thu micro 3–8 giây hoặc file MP3/WAV/M4A, có bước cam kết quyền sử dụng | Có (từ bản thu sạch) |
| Lồng tiếng theo phụ đề | Thả file `.srt`, giọng khớp mốc thời gian | Lồng tiếng cả video, dịch sang ngôn ngữ khác |
| Điều khiển cách đọc | Thẻ `[cười]`, `[thở dài]`, `[nghỉ 2s]`; tốc độ 0,75–1,5×; từ điển phát âm | Thiết kế giọng bằng mô tả chữ |
| Nhận dạng giọng (phụ đề) | Không phải trọng tâm | Có (Whisper và nhiều bộ khác) |
| Cài trên Windows | File `.exe` khoảng 367 MB, kèm sẵn mô hình, không cần quyền quản trị | Lệnh PowerShell hoặc `.exe`; hỗ trợ NVIDIA CUDA (một số bộ đọc có ghi bản CUDA 12.8 cho card dòng RTX 50) |
| Máy tối thiểu | 4 nhân, 8 GB RAM, không cần card | Tuỳ bộ đọc; nhiều bộ cần card NVIDIA |
| API | `http://127.0.0.1:8001`: `/voices`, `/api/tts/generate`, `/api/tts/generate-with-subtitles`, `/api/tts/conversation`; tài liệu cho AI ở `/cit-voice-studio.md` | `http://localhost:3900`, kiểu API giống OpenAI (`/v1/audio/speech`, `/v1/audio/transcriptions`) |
| Skill / MCP cho Claude | Chưa có skill; có file hướng dẫn dạng Markdown cho AI | **Có skill `skills/voicestudio/SKILL.md`** và **MCP** ở `http://localhost:3900/mcp` |
| Giấy phép mã | Apache-2.0 | AGPL-3.0 (dùng riêng thoải mái; sửa và phân phối thì phải công khai mã) |
| Giấy phép mô hình | VieNeu-TTS v3 Turbo: Apache-2.0; giọng nước ngoài Supertonic 3: OpenRAIL-M (dùng thương mại được, cấm mạo danh, lừa đảo) | Tuỳ bộ đọc; OmniVoice GGUF (bản chạy bằng card) ghi rõ **chỉ phi thương mại**; bản mặc định **chưa kiểm** |

## Nếu Hào chọn tích hợp: việc sẽ làm (nhỏ nhất chạy được)
1. Hào cài ứng dụng trên PC (file `.exe`), mở lên một lần, chọn hoặc nhân bản giọng.
2. App studio thêm nút **"Đọc thử kịch bản"**: gửi cột "Lời đọc" của `KICH-BAN.md` tới API trên máy, nhận file `.wav` + `.srt`, đặt vào dự án làm hàng giọng nói nháp. Phụ đề có sẵn mốc giờ nên chữ lớn đặt được ngay (nút 📝).
3. Thêm skill `.claude/skills/giong-noi/` để Claude trên PC tự gọi API này khi Hào nói "đọc thử kịch bản".
Phải có máy đang chạy ứng dụng (PC). Phiên cloud không gọi được vào máy của Hào.

## Còn phải kiểm khi thử thật
- Nghe chất lượng giọng Việt của cả hai trên kịch bản BĐS (số, tên dự án, "m2", "tỷ").
- Giấy phép bộ đọc mặc định của VoiceStudio nếu dùng cho video kinh doanh.
- Tốc độ trên PC (RTX 5050) của Hào.
