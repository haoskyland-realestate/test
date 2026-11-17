# Kho skill thiết kế (phong cách video mẫu Open Residency)

Mỗi thư mục là một bản **thiết kế skill** theo đúng khuôn `SKILL.md` của Claude Code. Chưa nằm trong `.claude/skills/` để không làm dài danh sách skill mỗi phiên.
**Bật một skill:** chép thư mục đó vào `.claude/skills/` (đã chắc nó chạy được thì mới chép). Skill đang chạy thật: `.claude/skills/` (hoc-mau, chinh-mau, dung-video, lap-storyboard, bao-cao-nghiem-thu).

| Skill | Trạng thái | Việc |
|---|---|---|
| `chu-theo-nhip-noi` | ĐÃ CÓ MÃ | Chữ phụ đề theo nhịp lời nói: từng từ hiện đúng lúc người nói, cụm ≤5 từ, thay phụ đề thường |
| `tu-khoa-phat-sang` | MỘT PHẦN | Từ khoá đỏ phát sáng: số, tiền, rủi ro, tên dự án nổi lên to hơn, nghiêng, phát sáng đỏ |
| `chu-bam-nguoi` | MỘT PHẦN | Chữ bám theo người nói: đặt chữ ngang ngực/đầu người, di chuyển theo khi người đi |
| `the-ten-giai-ma` | CHƯA BUILD | Thẻ tên người nói: vạch đỏ đứng, tên chữ hoa kiểu máy chữ, dòng chức danh nhỏ, chữ giải mã (nhiễu rồi rõ dần) |
| `canh-chen-the-mang-xa-hoi` | CHƯA BUILD | Cảnh chèn thẻ bài đăng nổi trên nền tối (ảnh chụp bài, số liệu, đoạn đỏ nhấn) |
| `canh-bong-nguoi-ai` | CHƯA BUILD | Cảnh rộng bóng người ngồi bàn do AI tạo (Flow) để chèn giữa các cảnh nói |
| `chuyen-canh-chop-sang` | ĐÃ CÓ | Chuyển cảnh chớp sáng/cháy sáng đúng nhịp đổi ý |
| `am-thanh-theo-nhip` | ĐÃ CÓ | Hiệu ứng âm theo nhịp chữ và chuyển cảnh: vào, chạm, trầm, lấp lánh, ra; đổi cao độ để không nhàm |
| `tim-nguon-mien-phi` | MỘT PHẦN | Tìm và đưa tài nguyên miễn phí, rõ giấy phép vào kho (âm, font, nhạc, hình) |
| `cta-cuoi-video` | CHƯA BUILD | Thẻ kêu gọi cuối video: thanh tìm kiếm với tên kênh Hào Sky Land (mẫu cuối video 2 là thanh tìm kiếm TikTok) |

Trạng thái: **ĐÃ CÓ** (mã chạy, đã thử), **ĐÃ CÓ MÃ** (mã chạy, chưa thử trên footage thật), **MỘT PHẦN** (làm được một phần, xem mục Còn thiếu), **CHƯA BUILD** (chỉ có thiết kế).
Thứ tự build đề xuất: `chu-theo-nhip-noi` (cỡ chữ, kiểu) → `chu-bam-nguoi` (bám từng khung) → `the-ten-giai-ma` → `tu-khoa-phat-sang` (cụm lớn) → `canh-chen-the-mang-xa-hoi` → còn lại.
