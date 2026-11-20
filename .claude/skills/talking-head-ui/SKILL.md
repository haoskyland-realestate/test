---
name: talking-head-ui
description: Dựng lớp chữ động kiểu talking head dọc 9:16 (phụ đề từng cụm, khối chữ nhấn xếp chồng, chữ sau người, chớp trắng, montage b-roll) bằng HyperFrames từ một file kế hoạch JSON, hoặc xuất riêng lớp chữ nền trong suốt để ghép trong CapCut. Dùng khi Hào nói "talking head ui", "lớp chữ cho CapCut", "chữ nền trong suốt", hoặc muốn phong cách pop hồng / phim tài liệu từ 3 video mẫu. Dựng talking head đầy đủ theo 5 bước thì dùng `dung-talking-head`.
---

# talking-head-ui

Biến video người nói dọc 9:16 thành video có lớp chữ động kiểu mạng xã hội, dựng trên HyperFrames. Phong cách đo từ 3 video mẫu (`references/analysis.md`). Hai preset:
- `pop-accent`: chữ trắng + hồng magenta phát sáng, vệt nhoè lao vào, cắt cận có chớp trắng, montage nhanh.
- `doc-calm`: chữ trắng mảnh nghiêng kiểu phim tài liệu, chữ nằm sau người, b-roll chậm.

Skill này **độc lập** với bộ dựng `video-studio/scripts/dung.py` (định dạng timeline v1). Nó tự sinh một dự án HyperFrames riêng. Kết quả có thể là MP4 hoàn chỉnh, hoặc chỉ lớp chữ nền trong suốt để Hào ghép trong CapCut.

## Ngôn ngữ JSON
- `style.json`: hệ thiết kế cố định (phông, vai trò chữ, màu, hoạt ảnh, chuyển cảnh, nhịp, vị trí). Sửa khi muốn đổi phong cách chung, ví dụ màu thương hiệu.
- `edit-plan.json`: kế hoạch riêng từng video theo `edit-plan.schema.json` (phụ đề, khối nhấn, camera, b-roll, chuyển cảnh, âm thanh). Claude viết file này; `scripts/build.mjs` sinh dự án HyperFrames. Ví dụ: `examples/`.

`<SKILL>` dưới đây là thư mục chứa file này: `.claude/skills/talking-head-ui`.

## Quy trình
0. Tạo dự án ngoài repo hoặc trong `video-studio/projects/<tên>/thu/` (không đưa footage lên GitHub): `bash <SKILL>/scripts/setup.sh <dự án>` (Node ≥ 22, ffmpeg). Trên Windows chạy lệnh trong Git Bash hoặc WSL.
1. Video thô vào `<dự án>/work/raw.mp4`, đưa về 1080x1920. Chưa rõ preset thì hỏi một câu: `pop-accent` hay `doc-calm`.
2. Cắt lặng: `python3 -I <SKILL>/scripts/cut_silence.py work/raw.mp4 assets/main.mp4`. `meta.duration` = độ dài main.mp4.
3. Phiên âm: dùng `video-studio/scripts/phu_de.py` (faster-whisper, đã chạy tốt với tiếng Việt), hoặc `npx hyperframes transcribe assets/main.mp4 --model small --language vi --json` (không dùng model `.en`). Tên riêng, con số phải đúng lời nói; không bịa chữ hay cam kết. Người nói có thể không phải Hào: giữ đúng tên đã nói.
4. Xem lưới khung hình 1 khung/giây để chọn chỗ đặt chữ không đè mặt, chỗ cắt cận, chỗ chèn b-roll.
5. Viết `edit-plan.json`:
   - Phụ đề: 1–3 âm tiết theo cụm nghĩa, 0.3–0.7 s, một cụm mỗi lúc; `accent` chỉ 1–2 cụm.
   - Khối nhấn: pop mỗi 3–6 s, doc mỗi 6–12 s; 2–4 dòng trộn vai trò (`light`/`heavy`/`hero`/`script`/`giant`; doc: `doc-thin`/`doc-bold`); mỗi dòng có `at` đúng lúc được nói; sau dòng cuối phải còn ≥0.6 s đứng yên trước khi thoát; không chồng lên b-roll hay màn đen.
   - Camera: pop cắt cận 1.18–1.32x mỗi 8–20 s với `flash-white`.
   - B-roll chỉ dùng file Hào gửi. Nhạc/sfx chỉ khi có file.
6. Chữ sau người (`behindSubject`): `npx hyperframes remove-background`; lỗi thì `scripts/cutout.py` với rembg.
7. `node <SKILL>/scripts/build.mjs <dự án>`, rồi `npx hyperframes check --json` và `snapshot` để xem.
8. Duyệt xong: `npx hyperframes render -q delivery -o out/<tên>.mp4`.

## Chế độ chỉ lớp chữ cho CapCut
`source.video: null` → nền trong suốt; `npx hyperframes render --format mov` (ProRes 4444). Giao trong một .zip:
- `*_alpha_prores4444.mov`: CapCut máy tính, giữ bóng chữ;
- `*_nen-den_dung-Screen.mp4`: ghép lên nền đen, dùng hoà trộn Screen trong CapCut; chạy cả trên điện thoại nhưng mất bóng chữ;
- 2 đoạn thử 5 giây và file hướng dẫn.

Bản duyệt trên điện thoại luôn là MP4 đã ghép lên nền tối (#282828) và nền sáng. Không gửi .mov/.webm để duyệt: điện thoại bỏ qua độ trong suốt nên vùng nhoè, quầng sáng hiện thành mảng màu.

Kiểm tra trước khi giao: mỗi khối nhấn xem 3 thời điểm (vào, giữ, ra) trên nền tối và nền sáng; không có vạch thừa, chữ trắng đọc được trên nền sáng.

## Quy tắc chuyển động (Hào duyệt 19/11/2026)
Mọi chuyển động dùng ease in-out (`*.inOut`). Chữ nhấn vào 0.5 s (pop) / 0.75 s (doc), thoát 0.34 s / 0.55 s. Vệt nhoè chỉ cho dòng màu nhấn, giãn ngang tối đa 1.1. Phụ đề hiện trong tối đa 1/4 thời lượng cụm (0.1–0.2 s). Chữ trắng luôn có bóng 2 lớp.

## Sửa theo phản hồi
Chữ to/nhỏ: `size` của dòng hoặc `roles.<vai>.size`. Đổi màu: `meta.accent`. Nhanh/chậm: `animations` trong style.json. Luôn build lại sau khi sửa.

## Trạng thái
- Đã thử trên cloud: dựng 2 preset với video mẫu, chữ sau người (cutout bằng rembg), bản overlay 60 s 360p nền trong suốt.
- Chưa thử: footage thật của Hào, trên PC/Mac, nhập file .mov vào CapCut (chờ Hào báo cách nào hiện đúng).
- Phông: Montserrat, Inter, Playfair Display (OFL, có tiếng Việt). Tách người bằng AI có thể nhấp nháy ở tóc, tay, micro.
