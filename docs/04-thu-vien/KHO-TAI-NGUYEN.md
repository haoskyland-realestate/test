# Kho tài nguyên edit (khoảng 30 GB trên Google Drive)

Lập 13/11/2026. App studio đọc kho này **trên PC** (nút **📦 Kho**). Kho không đưa lên GitHub và không chép vào từng dự án.

## Hiện trạng trên Drive (Claude xem ngày 13/11/2026)
- Thư mục Hào tự tạo: `01_TYPOGRAPHY_AND_FONTS`, `02_COLOR_PALETTES_AND_LUTS`, `03_MOTION_GRAPHICS_PRESETS`, `04_SOUND_EFFECTS_SFX`, và "HAO SKY LAND – THƯ VIỆN EDIT VIDEO": **đang trống**.
- Tài nguyên thật là các kho **người khác chia sẻ, dạng file nén**: "NỀN OVERLAY/Overlays.rar" (2,2 GB), "SOUND EFFECT/Sound Effect - ThuaanNguyeen.rar" (1,9 GB), "PAPER TRANSITION/…rar" (170 MB), thư mục "Tài nguyên tóp tóp" (brush, font vintage, podium, plugin Eye Candy).
- **Giấy phép chưa rõ:** đây là gói người khác chia sẻ. Trước khi dùng trong video kinh doanh, nên hỏi lại nguồn gốc hoặc ưu tiên gói có ghi rõ "free for commercial use".

## Chuẩn bị trên PC (làm một lần)
1. Cài **Google Drive cho máy tính**. Với thư mục kho, chọn **"Sẵn có ngoại tuyến" (Available offline)**: nếu để chế độ phát trực tuyến, mỗi lần app tạo ảnh thu nhỏ là Drive tải file đó về, chậm.
2. Giải nén các file `.rar` (7-Zip miễn phí) vào đúng thư mục theo bảng dưới. File `.rar` còn nằm trong kho thì app chỉ báo "cần giải nén".
3. Mở app → **📦 Kho** → chọn thư mục gốc của kho → app quét (chỉ đọc tên file, 30 GB vẫn nhanh). Thêm hay giải nén file mới thì bấm **Quét lại**.

### Cách xếp thư mục (giữ 4 thư mục Hào đã đặt, thêm phần còn lại)
```
<KHO>\
  01_TYPOGRAPHY_AND_FONTS\        font .ttf/.otf (app chưa dùng trực tiếp, xem mục cuối)
  02_COLOR_PALETTES_AND_LUTS\     LUT .cube → dùng làm màu cho đoạn video
  03_MOTION_GRAPHICS_PRESETS\     .mogrt, .aep, preset Premiere/AE (chỉ tham khảo)
  04_SOUND_EFFECTS_SFX\<nhóm>\     âm .wav/.mp3 → hàng ♪ Hiệu ứng âm
  05_OVERLAYS\<nhóm>\              lá sáng, bụi, khói, giấy, lens flare (.mp4/.mov/.png)
  06_BACKGROUNDS\                 nền ảnh/video
  07_TRANSITIONS\                 chuyển cảnh dạng video (paper transition…) → phủ như overlay
  08_PLUGINS\                     bộ cài plugin (chỉ tham khảo)
```
Tên thư mục và tên file chính là thẻ để tìm: đặt rõ nghĩa ("Light Leak", "Whoosh", "Giay xe") thì tìm nhanh. App tìm không cần dấu.

## App dùng được gì
| Loại | Trong app | Cách vào video |
|---|---|---|
| Âm thanh (.wav, .mp3, .m4a, .flac…) | ▶ nghe thử | **+ Âm tại kim** → hàng ♪ Hiệu ứng âm |
| Overlay nền đen (lá sáng, bụi, khói, flare) | Ảnh thu nhỏ | **+ Phủ hoà sáng** → hàng ✦ Overlay (chế độ hoà sáng: phần đen biến mất) |
| Overlay nền trong suốt (.mov alpha, .png) | Ảnh thu nhỏ | **+ Phủ trong suốt** |
| Chuyển cảnh dạng video (paper transition) | Ảnh thu nhỏ | Phủ đúng chỗ nối hai đoạn (hoà sáng hoặc trong suốt tuỳ file) |
| LUT màu (.cube) | Biểu tượng 🎨 | **Dùng màu cho đoạn ở kim** (xem đúng màu khi Dựng nháp) |
| Font, template Premiere/AE (.mogrt, .aep), plugin, brush, .psd | Biểu tượng | **Chỉ tham khảo**: app chưa chạy được các phần mềm này |
| File nén (.rar, .zip) | 🗜 | Giải nén trên PC rồi Quét lại |

Trong timeline, tài nguyên kho ghi dạng `"kho:<đường dẫn trong kho>"`. Chuyển sang PC khác chỉ cần chọn lại thư mục kho, không phải sửa dự án. Thiếu file thì bộ dựng dừng và nói rõ file nào.

## Nhờ Claude dùng kho để thiết kế
Claude Code trên PC đọc được chỉ mục `video-studio/kho/chi-muc.json` (danh sách file, loại, thẻ). Ví dụ câu lệnh:
- "Từ kho, chọn 3 overlay và 3 tiếng vút hợp mẫu `sang-trong-01` cho video `<tên>`, thêm vào timeline ở các chỗ chuyển cảnh."
- "Xem các template trong `03_MOTION_GRAPHICS_PRESETS` (ảnh xem trước nếu có) rồi làm một mẫu edit mới theo phong cách đó" (giống cách đã làm `edit-phim-01` từ video mẫu).

## Giới hạn hiện tại
- Khung xem trước trong app chỉ hiện **một overlay cùng lúc** và gần đúng; bản dựng thì đủ và chính xác. LUT chỉ thấy khi Dựng nháp.
- Font trong kho chưa nạp vào được chữ của mẫu; sẽ thêm khi Hào chọn font thương hiệu.
- Xuất sang Premiere/DaVinci chưa mang theo overlay.
- **Chưa thử trên PC với kho thật.** Đã thử trên cloud bằng kho giả (overlay hoà sáng, overlay trong suốt .mov và .png, LUT, âm; đường dẫn có dấu cách, dấu hai chấm, chữ có dấu): dựng ra đúng.
