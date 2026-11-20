# CLAUDE.md: Quy trình edit video tự động (dọc 9:16, tiếng Việt) · Bản chuẩn

Thư mục này là xưởng edit video. Khi người dùng đưa một video thô và nói "edit video này", làm đúng quy trình dưới đây. Luôn nói chuyện bằng tiếng Việt, ngắn gọn.

## 1. Cấu trúc thư mục

```
CLAUDE.md          file này
presets/           cách trình bày trọn bộ (màu, bố cục khung hình, motion): A, B, C
effects/CATALOG.md danh mục hiệu ứng, mỗi hiệu ứng có MÃ để người dùng chọn theo cảnh
effects/picker_template.html      trang CHỌN hiệu ứng bằng hình (Bước 4)
effects/storyboard_template.html  trang STORYBOARD để chốt phương án (Bước 5)
tools/             safe_check.py, matte_person.py, preset_A_example/ (xem mục 12)
reference/         mã giao diện mẫu đã duyệt (ví dụ storyboard_style_reference.html)
input/             video gốc (không sửa)
work/<ten-video>/  file trung gian (audio, transcript, scenes.json, timeline.json, clip đã cắt)
output/            MP4 thành phẩm và khung thử (output/preview/)
assets/            fonts/, images/, nhạc, sound_effect, logo
```
Không sửa file gốc trong `input/`. Mọi thứ khác ghi vào `work/` hoặc `output/`.

## 2. Công cụ và tài nguyên
- FFmpeg (cắt, ghép, trộn âm thanh), Python 3, `faster-whisper` (xem mục 9), `rembg` (tách người, chỉ khi preset cần).
- Skill `hyperframes` và `hyperframes-cli`: dựng lớp đồ họa bằng HTML rồi render MP4. ĐỌC skill `hyperframes` trước khi viết composition; dùng CLI của nó để lint, preview, render. Mọi khung thử cũng phải render bằng HyperFrames/Chromium từ HTML, KHÔNG vẽ bằng PIL.
- Skill `media-use`: chỉ dùng khi cần tìm/tạo nhạc, sound effect, b-roll.
- Thư viện tài nguyên trên máy (người dùng điền đường dẫn thật):
  - Font: `ĐIỀN_ĐƯỜNG_DẪN_THƯ_MỤC_FONT`
  - Sound effect: `ĐIỀN_ĐƯỜNG_DẪN_THƯ_MỤC_SOUND_EFFECT`
  - Nhạc nền: `ĐIỀN_ĐƯỜNG_DẪN_THƯ_MỤC_NHẠC`
  Khi cần dùng thì COPY file vào `assets/` của dự án (không trỏ thẳng ra thư mục ngoài trong composition) để render ổn định và mang sang máy khác vẫn chạy. Chỉ đọc và copy, không sửa, không xóa file trong thư viện gốc. Nếu đường dẫn còn là chữ "ĐIỀN_...", hỏi người dùng đường dẫn trước khi làm bước âm thanh và phông chữ.

## 3. Quy trình (làm lần lượt, báo ngắn sau mỗi bước)

### Bước 0. Chọn preset (TRƯỚC mọi bước khác)
Preset là một cách trình bày trọn bộ (màu, bố cục khung hình, kiểu hiệu ứng, motion). Có 3 preset, mỗi preset là một file trong `presets/`:

| Gọi | Tên | Ý chính | File |
|---|---|---|---|
| A | `xanh_gradient` | Nền xanh sáng, thẻ trắng phía trên, người nói tách nền, đầu nhô khỏi khung | `presets/xanh_gradient.md` |
| B | `cam_kem` | Nền cam đất, thẻ tối viền vàng, khung người nói chữ nhật (không tách nền) | `presets/cam_kem.md` |
| C | `neon_toi` | Nền đen neon cam đỏ, đồ họa toàn khung, người nói là vòng tròn góc trên | `presets/neon_toi.md` |

1. Người dùng nêu preset ("dùng preset A", "kiểu neon tối"...): mở đúng file và ĐỌC KỸ trước khi lập storyboard.
2. Chưa nêu: hỏi một câu bằng bảng trên (kèm ý chính từng preset) và chờ. Không trả lời được thì dùng A.
3. Từ lúc đã chọn: màu, bố cục, phông, motion, cách đặt người nói theo file preset. Các mục còn lại của file này là CHUNG cho mọi preset; khi mâu thuẫn thì preset thắng. Không trộn hai preset trong một video; đổi preset giữa chừng thì dựng lại storyboard.
4. Ghi `"preset": "<tên>"` ở đầu `timeline.json`.
5. Preset quyết định CÁCH TRÌNH BÀY CHUNG. Hiệu ứng cho từng cảnh do người dùng chọn riêng ở Bước 5 (mục 5); hai thứ độc lập nhau.

### Luồng tổng (từ nguồn nội dung tới video)
`Kịch bản hoặc video thô` → `Storyboard + trang CHỌN hiệu ứng (bằng hình)` → `Trang STORYBOARD chốt phương án` → `Sửa đổi (lặp tới khi chốt)` → `Dựng + xem thử nhanh` → `Sửa đổi sau xem thử` → `Render bản chuẩn`. KHÔNG render video trước khi người dùng nói "chốt phương án".

### Bước 1. Nguồn nội dung và kiểm tra video
- Có VIDEO THÔ: `ffprobe` đọc độ dài, độ phân giải, fps, cờ xoay, có âm thanh không. Không phải dọc 9:16 thì hỏi crop hay thêm nền mờ. Mục tiêu xuất: 1080x1920, 30 fps, H.264, AAC. Đi tiếp Bước 2.
- Có KỊCH BẢN (văn bản, người dùng dán hoặc đưa file) mà CHƯA có video (hoặc muốn lên storyboard trước khi quay): bỏ Bước 2–3, tách kịch bản thành cảnh theo ý (1–2 câu mỗi cảnh, ước lượng thời lượng ~2.5 từ/giây), đi thẳng Bước 4 với mốc giây ƯỚC LƯỢNG (ghi rõ "ước lượng"). Khi có video: làm Bước 2–3 rồi KHỚP lời phiên âm với từng câu kịch bản để cập nhật mốc giây thật, giữ nguyên lựa chọn hiệu ứng đã chốt và báo những cảnh lời nói lệch kịch bản.
- Có CẢ kịch bản và video: dùng kịch bản làm chuẩn chính tả cho lời nói/chữ hiển thị (sửa lỗi nghe nhầm của Whisper theo kịch bản), vẫn cắt theo giọng nói thật.

### Bước 2. Phiên âm
Theo mục 9. Xong thì in toàn bộ lời đã nghe được và hỏi người dùng có từ nào sai không (tên riêng, thuật ngữ). Sửa theo phản hồi trước khi đi tiếp.

### Bước 3. Cắt thô
- Cắt khoảng lặng dài hơn 0.5 giây giữa các câu (giữ lại khoảng 0.15–0.2 giây cho tự nhiên); cắt đoạn nói vấp, nói lặp, ậm ừ.
- Khi nghi ngờ một đoạn có nên cắt không: GIỮ lại và đánh dấu để hỏi.
- Mọi mốc ở các bước sau tính theo video ĐÃ CẮT. Lưu `work/<ten>/cut.mp4` và bản đồ thời gian gốc → mới.

### Bước 4. Chia cảnh, gợi ý hiệu ứng, trang CHỌN bằng hình
Từ lời đã sửa (hoặc từ kịch bản) chia lời nói thành các CẢNH ngắn theo ý (thường 2–8 giây; video 30 giây có ~10–15 cảnh). Mỗi cảnh ghi: số thứ tự, mốc giây, lời nói. Với mỗi cảnh, đề xuất MỘT hiệu ứng chính từ `effects/CATALOG.md` (theo mục 5), nói ngắn vì sao. Lưu `work/<ten>/scenes.json`.
TRANG CHỌN BẰNG HÌNH (bắt buộc, KHÔNG chỉ hỏi bằng chữ và KHÔNG render video xem trước ở bước này): tạo `output/chon-hieu-ung.html` bằng cách copy `effects/picker_template.html` rồi thay phần JSON nằm giữa `/*DATA*/` và `/*END*/` bằng
`{"preset":"<tên preset>","base":"../effects/thumbs","scenes":[{"id":1,"t_in":0,"t_out":5,"say":"<lời nói của cảnh>","suggest":["mã_tốt_nhất","mã_2","mã_3"]}]}`.
Mỗi cảnh gợi ý 2–4 mã (mã đầu là đề xuất chính). Hình xem trước ở `effects/thumbs/<preset>/<mã>.jpg`; trang có nút "Xem tất cả hiệu ứng", "Giống cảnh trước (gom cụm)", "Bỏ hiệu ứng", sao chép kết quả. Mở trang cho người dùng (Windows: `start output\chon-hieu-ung.html`) và nói họ chọn xong thì dán kết quả vào đây. Hình trong trang là khung mẫu, chữ thật lấy từ lời người nói. Không mở được trang thì mới dùng bảng chữ: `Cảnh | mốc giây | lời | hiệu ứng đề xuất`.
Cùng lúc, gom MỘT danh sách "CẦN GÌ CHO CẢNH NÀO" (dữ liệu còn thiếu theo cột "Dữ liệu cần": ảnh, số liệu thật, tên, logo, bản đồ có đánh dấu...) để người dùng gửi một lượt. Không bịa số liệu, không dùng ảnh giả trong bản cuối.

### Bước 5. Trang STORYBOARD: chốt phương án, sửa đổi, DỪNG LẠI
1. Người dùng dán kết quả từ trang chọn (dạng "Preset ... Chọn hiệu ứng: Cảnh 1–3: chart_bars; Cảnh 4: map_route"); hoặc "làm hết" (giữ đề xuất); hoặc nêu cảnh muốn đổi. Cảnh không nhắc tới giữ đề xuất; "bỏ" thì `speaker_only`. Cảnh liền nhau cùng hiệu ứng = MỘT cụm liên tục (xem "Gom cảnh" trong `effects/CATALOG.md`).
2. Ghi lựa chọn vào `timeline.json` (mục 10), rồi tạo TRANG STORYBOARD `output/storyboard.html` bằng cách copy `effects/storyboard_template.html` và thay JSON giữa `/*DATA*/` và `/*END*/` bằng
`{"preset":"<tên>","base":"../effects/thumbs","scenes":[{"id":1,"t_in":0,"t_out":4.1,"say":"<lời>","effect":"<mã đã chọn>","need":[{"k":"<dữ liệu cần>","ok":true|false}]}]}`
(`ok:true` khi đã có dữ liệu thật). Trang hiện từng khối cảnh gồm hình hiệu ứng, lời nói, dữ liệu đã có / còn thiếu, ô đổi hiệu ứng và ô ghi chú sửa. Mở trang cho người dùng.
3. Người dùng dán phản hồi: nếu là "Chốt phương án" thì sang Bước 6. Nếu là "Sửa trước khi chốt..." thì áp dụng (đổi hiệu ứng, sửa chữ, thứ tự, thời lượng), cập nhật `timeline.json`, TẠO LẠI `output/storyboard.html` và hỏi lại. Lặp tới khi chốt. Đổi hiệu ứng thì hỏi lại dữ liệu cần của hiệu ứng mới.
4. Dữ liệu còn thiếu vào lúc chốt: dựng khung giữ chỗ có nhãn ("SỐ MẪU", "ẢNH CẦN CHÈN") để duyệt bố cục; bản cuối không được còn nhãn này. Người dùng có thể gửi ảnh thật giữa chừng: thay vào ô tương ứng rồi xuất bản mới (`_v2`, `_v3`...).
5. Chỉ dựng khi người dùng đã chốt. Không render khi chưa chốt.

### Bước 6. Dựng đồ họa bằng HyperFrames và xem thử nhanh
Tạo composition từ `timeline.json`, theo preset đã chọn. Mỗi hiệu ứng là một component dùng lại (mục 6), bám theo trang mẫu trong `effects/reference/`. Kinh nghiệm và công cụ đã chạy được: mục 12 và `tools/`.
- Kiểm tra phông (mục 8). Chạy lint/validate bằng CLI HyperFrames.
- KIỂM TRA VÙNG AN TOÀN (bắt buộc, trước khi chụp khung thử và trước khi render): đánh dấu video người nói và lớp nền bằng `data-safe="ignore"`, rồi chạy `python tools/safe_check.py --html <composition.html> --times <các mốc giữa và cuối mỗi hiệu ứng> --seek "<lệnh seek của HyperFrames>"`. Có dòng "tràn" thì sửa (thu nhỏ/dời hiệu ứng, ngắt dòng chữ) rồi chạy lại cho tới khi tất cả OK.
- KHUNG THỬ: chỉ chụp thử (`output/preview/`) cho hiệu ứng có trạng thái "chưa duyệt / chờ duyệt lại" trong CATALOG hoặc cảnh mới có dữ liệu thật. Hiệu ứng đã duyệt mẫu thì không chụp lại, trừ khi dữ liệu làm chữ tràn. Kiểm tra: đủ đỉnh tóc và cằm, viền sạch, không mất dấu, không tràn chữ.
- BẢN XEM THỬ NHANH: render toàn video 540x960 hoặc `-q draft` (`output/<ten>_preview.mp4`), CÓ vẽ lớp vùng an toàn (xem mục 12) để người dùng thấy. Gửi cho người dùng xem nhịp và nội dung, rồi hỏi sửa gì (SỬA ĐỔI SAU XEM THỬ: chữ, nhịp, vị trí, âm lượng). Sửa xong xuất lại bản xem thử; chỉ render bản chuẩn khi người dùng nói đạt.

### Bước 7. Âm thanh
Sound effect rất nhẹ khi thẻ/nhãn bật lên, nhạc nền nhỏ (thấp hơn giọng nói ít nhất ~18 dB); mức đã cân bằng xem mục 12. Chỉ dùng file từ thư viện ở mục 2 (copy vào `assets/`) hoặc người dùng cung cấp; không tự tải nhạc không rõ bản quyền. Chưa có nhạc/SFX thì bỏ qua, chỉ giữ giọng nói gốc, và nhắc người dùng bỏ file vào `assets/music` và `assets/sfx` (hoặc chỉ đường dẫn) để lần sau có.

### Bước 8. Render và kiểm tra
Sau khi bản xem thử được duyệt, render bản chuẩn ra `output/<ten>_v1.mp4` (bản sạch, KHÔNG có lớp vùng an toàn). Tự kiểm tra: độ dài hợp lý, âm thanh không vỡ/lệch tiếng, chữ không tràn khung, không đè mặt người nói, phông và dấu tiếng Việt đúng trên khung thật. Trích vài khung ở các mốc quan trọng để xem lại. Báo kết quả và những chỗ còn nghi ngờ. Khi sửa, lưu bản mới `_v2`, `_v3`.

## 4. Nguyên tắc trình bày và motion (chung mọi preset)
- Mỗi ý người nói vừa nhắc tới có MỘT hình thể hiện ngay ý đó, hiện đúng lúc họ nói (trễ không quá ~0.2 giây), ở lại đến hết ý rồi biến mất nhường chỗ cho ý kế. Không để khung đồ họa trống khi đang nói về một ý cụ thể; không có hai hình lớn cùng lúc.
- Tối đa ~1 hình lớn mỗi 4–6 giây; giữ nhịp thở, thỉnh thoảng cho người nói toàn khung (`speaker_only`).
- Hiệu ứng vào 0.25–0.45 giây, ease-out, có thể kèm trượt 8–20 px. Thẻ con hiện lần lượt theo đúng nhịp người nói, không hiện cùng lúc. Cụm quan trọng được nhấn bằng một lần tô/đổi màu, không quá 1 cụm mỗi thẻ. Đường nối vẽ ra dần thay vì xuất hiện sẵn. Khi ý kết thúc, hình thu nhỏ hoặc mờ dần trong ≤0.3 giây.
- Chữ trong hình LẤY TỪ LỜI NGƯỜI NÓI hoặc kịch bản/dữ liệu người dùng; không bịa số liệu, tên sản phẩm. Đọc được trên điện thoại: cỡ nhỏ nhất ~28 px trên khung 1080 px; tối đa ~8 từ mỗi dòng.
- VÙNG AN TOÀN (bắt buộc, áp dụng cho MỌI chữ, thẻ, icon, mũi tên (và phụ đề khi có); không có ngoại lệ trừ khi preset ghi rõ): khung 1080x1920, giao diện TikTok/Reels/Shorts che các mép. Nội dung chỉ nằm trong HÌNH CHỮ NHẬT AN TOÀN:
  - Trên: chừa 15% = 288 px (≈ 26.7 cqw). Dưới: chừa 25% = 480 px (≈ 44.4 cqw, tức mép dưới nội dung ≤ y 1440 px ≈ 133.3 cqw). Trái và phải: chừa 10% = 108 px (10 cqw), nút thả tim/bình luận nằm ở mép phải.
  - Ngoại lệ DUY NHẤT: video người nói và các lớp nền được phép tràn ra ngoài vùng này (đánh dấu `data-safe="ignore"`); chữ trên người nói thì vẫn phải an toàn.
  - Hiệu ứng nội dung (khối đồ họa mẫu rộng 100 cqw) được đặt bằng: đỉnh tại y=26.7 cqw, thu 0.80, canh giữa (rộng 80 cqw, từ x=10 đến x=90). Preset C: đỉnh y=36 cqw vì vòng tròn người nói ở góc trên.
  - Phụ đề (khi sau này có): cạnh dưới ở y ≤ 133.3 cqw, cách hai bên ≥ 10 cqw, không che miệng người nói (dịch/thu nhỏ người nói nếu cần).
  - Nếu hiệu ứng không vừa trong hình chữ nhật này thì THU NHỎ hiệu ứng, không để tràn. Chữ nhỏ nhất vẫn ≥ 28 px.
- **Phụ đề: ĐÃ GỠ, MẶC ĐỊNH KHÔNG VẼ PHỤ ĐỀ.** Người dùng sẽ đưa kiểu phụ đề mới (mẫu, màu, cỡ, cách hiện từ); khi có sẽ duyệt mẫu rồi ghi vào đây dưới dạng module `captions`. Cách dùng đã thống nhất: phụ đề là LỰA CHỌN THEO ĐOẠN, không phủ cả video. Đoạn nào cần thì bật phụ đề, đoạn nào đã có hiệu ứng đồ họa thì KHÔNG phụ đề, chỉ dùng hiệu ứng. Mỗi cảnh trong `timeline.json` có cờ `captions: "on"|"off"` (mặc định off); người dùng bật/tắt qua ô ghi chú của trang storyboard (ví dụ "Cảnh 3: bật phụ đề"); chưa có kiểu mới thì chỉ ghi cờ, chưa vẽ. Chữ trong hiệu ứng (tiêu đề, nhãn, số liệu) vẫn giữ, chỉ không có dòng phụ/subtext.
- Người nói: luôn thấy đủ đỉnh tóc và cằm (mắt và miệng phải nằm trong vùng an toàn); nếu người nói cử động nhiều thì cắt lại theo vị trí mặt của từng đoạn, không dùng một vị trí cố định cho cả video.
- NỀN CHUNG: mọi hiệu ứng (trừ cảnh toàn khung như `cinematic_break`, `speaker_only` và `logo_pop` đã có luồng sáng riêng) đều có HAI ĐỐM MÀU MỜ ở nền, nằm dưới mọi đồ họa và dưới người nói, để thẻ kính và thẻ trong suốt có thứ làm mờ và để mọi mẫu đồng bộ nhìn:
  - Đốm 1 (lớn, bên phải): tròn 50 cqw, gradient tâm lệch `--orb2` → `--orb1` (55%) → trong suốt (72%), blur ~1 cqw, độ mờ 0.85, vị trí trái 50 / trên 42 cqw. Đốm 2 (bên trái dưới): tròn 46 cqw, gradient `--orb1` → trong suốt (70%), blur ~2 cqw, độ mờ 0.7, vị trí trái −14 / trên 76 cqw. Cả hai trôi nhẹ chậm (chu kỳ 7 s và 9 s, ngược chiều nhau).
  - Màu CHỈ lấy từ hai token của preset: `--orb1` (màu chính, mặc định = màu nhấn `--h1`) và `--orb2` (màu sáng, mặc định = `--h2`). Muốn đổi cả bộ màu nền thì chỉ sửa hai token này ở preset, không sửa trong từng hiệu ứng.
- Màu, đổ bóng, bo góc, vị trí khung theo preset; không gõ cứng màu trong component, lấy từ token của preset.

## 5. Từ "ý đang nói" đến hiệu ứng

Danh mục đầy đủ (mã, dữ liệu cần, thời lượng, trạng thái duyệt mẫu) nằm ở `effects/CATALOG.md`. Bảng dưới là gợi ý để đề xuất ở Bước 4:

| Khi người nói... | Hiện hình | Mã |
|---|---|---|
| Mở đầu, nêu vấn đề/hook | Tiêu đề lớn + chữ viết tay + số đếm, theo kiểu của preset | `typo`, `count_up` |
| Cảnh báo, "coi chừng", "vẫn phải mua", "sai lầm" | Biểu tượng cảnh báo đỏ + chữ lớn rung nhẹ | `warning_stamp` |
| Nhắc một trang web/công cụ có thật | Ảnh chụp trang nổi như tấm thẻ, có bóng, tô sáng cụm quan trọng (ví dụ "miễn phí") | `screenshot_card` |
| Giới thiệu sản phẩm/gói/tên | Thẻ tối có logo + tên, huy hiệu tròn góc (giá "0Đ", nhãn "MỞ KHÓA") | `product_badge` |
| Liệt kê quyền lợi/tính năng đi kèm | Sơ đồ cây: thẻ cha, đường nối gấp khúc, thẻ con hiện lần lượt (icon, nhãn, số liệu như "×2", "400 GB" kèm thanh) | `tree_diagram` |
| "Kết nối với...", "tích hợp", "nằm sẵn trong" | Bảng nhỏ A có chấm, nét vẽ chạy tới bảng lớn B, chấm đón ở B, nét thành đoạn đứt chạy mãi | `connect_flow` |
| Nhấn một lợi thế "đỉnh nhất" | Thẻ viền nét đứt, huy hiệu ngôi sao, icon lớn (ví dụ ∞), tiêu đề, cụm quan trọng tô như dạ quang | `feature_card` |
| "Chỉ cần gõ/ra lệnh..." | Thanh nhập lệnh rồi mở rộng thành lệnh đầy đủ (KHÔNG gõ từng ký tự; chữ vào bằng `typo_*`) | `prompt_card` (dùng `feature_card`+`typo`) |
| Đưa ví dụ kết quả | Mockup kết quả thật (đề thi trắc nghiệm, sơ đồ từ khóa, trước/sau) | `screenshot_card` |
| Liệt kê 3 lý do/giá trị/nguyên tắc cần vẻ cao cấp | Danh sách thẻ kính mờ có số 01 02 03, quầng sáng phía sau | `glass_list` |
| Nhắc tên 2–4 sản phẩm/AI/thương hiệu liên tiếp | Nền tối có luồng sáng, vệt sáng bay, icon kính pop nảy vào rồi pop ra | `logo_pop` |
| Nói về tốc độ tăng trưởng, phần trăm tăng, "tăng gấp N lần" | Thẻ tối có đường cong đi lên vẽ trái→phải, chấm sáng chạy tới đỉnh và chớp, số lớn đếm lên, dải sáng chất lỏng ở đáy | `growth_card` |
| Liệt kê điều kiện/yêu cầu/ghi chú | Tiêu đề pill + các dòng có ô tích; dòng đang nói sáng và được tích, dòng còn lại mờ | `note_board` |
| Vị trí, giao thông, tiện ích quanh dự án | Bản đồ, zoom vào dự án, tuyến vẽ dần, ghim điểm đến + nhãn | `map_route` |
| Diện tích, cảnh quan, số lượng sản phẩm | Thẻ ảnh lớn viền sáng + chữ phụ so le + số đếm | `photo_cards` |
| Liệt kê tiện ích dự án | Lưới ảnh nhỏ có nhãn hiện lần lượt, kết bằng thẻ tổng | `amenity_grid` |
| Số liệu theo năm, giá, tăng trưởng | Biểu đồ cột mọc lần lượt, cột nhấn có nhãn | `chart_bars` |
| Giải thích bằng ảnh có chú thích | Ảnh có ghim, bong bóng chú thích bật ra theo từng ý | `popup_notes` |
| Nhấn một con số, so sánh | Số lớn/đếm lên, hoặc hai thẻ cạnh nhau | `count_up`, `compare_cards` |
| Ví von, "giống như..." | Thẻ có hình minh họa cho câu so sánh | `metaphor_card` |
| Đỉnh cảm xúc, "sáng tạo", "tưởng tượng" | Cảnh toàn khung điện ảnh (hạt, ánh sáng), RẤT ít: 1–2 lần mỗi video | `cinematic_break` |
| Kêu gọi hành động, kết | Số/cụm lớn + nút hành động | `outro_cta` |
| Không khớp kiểu nào | Cụm khóa bằng `typo_*` hoặc chỉ `speaker_only`, đừng ép hình | `typo`, `speaker_only` |

Thành phần phụ dùng chung: `step_badge` (huy hiệu số bước + tên ở giữa phía trên), `card_stack` (danh sách thẻ có icon trượt lên theo lời), `checklist`, `progress_bars` (thanh chạy đầy so le rồi tích), `captions`.

## 6. Chi tiết các hiệu ứng đã duyệt mẫu
Màu cụ thể (nền, thẻ, gradient, glow) lấy từ preset đã chọn; phần dưới chỉ quy định bố cục và chuyển động. Mọi số đo theo cqw (1 cqw = 1/100 bề rộng khung = 10.8 px trên 1080).

### Quy ước chung đã chốt khi duyệt (áp dụng cho MỌI hiệu ứng)
- **Tiêu đề dạng pill:** KHÔNG dùng số. Bên trái pill là ICON tự vẽ nằm trong vòng tròn khoanh (nền màu nhấn, viền trắng, vòng ngoài màu tiêu đề) nổi hẳn khỏi pill; thứ tự: icon rồi tên. Icon theo nội dung: biểu đồ cột (số liệu), ghim (bản đồ), nhà (tiện ích), danh sách (điều kiện), bong bóng (chú thích), mũ cử nhân, thư, khiên, sao, video, đám mây, hồ bơi, tạ, cây, bếp nướng. Dùng chung cho `chart_bars`, `map_route`, `amenity_grid`, `note_board`, `popup_notes`, `tree_diagram`.
- **Vùng an toàn:** xem mục 4 (trên 15%, dưới 25%, hai bên 10%). Hiệu ứng thu 0.80, đỉnh y=26.7 cqw; Kiểm tra bằng `tools/safe_check.py` ở Bước 6.
- **KHÔNG DÙNG SUBTEXT (dòng phụ) trong bất kỳ hiệu ứng nào:** thẻ, danh sách, bong bóng chú thích, cảnh báo, kết nối, biểu đồ chỉ có chữ chính (tên/tiêu đề/số). Không thêm dòng mô tả nhỏ bên dưới tên hay số. Phụ đề video (lời người nói ở đáy khung, mục 4) là thứ khác và vẫn giữ theo preset.
- **Chữ ép sát:** chữ nhiều lớp (dẫn / cụm khóa / nhãn) phải dính vào nhau, khoảng hở ≤ ~1 cqw hoặc chồng nhẹ bằng margin âm; không để khoảng trống lớn giữa các lớp.
- **Đường nối động:** mọi đường nối (cây, chú thích, tuyến) vẽ bằng nét stroke chạy từ điểm đầu tới điểm cuối, có chấm tròn ở đầu; chấm/thẻ ở đích chỉ hiện KHI nét tới nơi (giống `connect_flow`).
- **Callout có mũi nhọn:** bong bóng/nhãn chỉ vị trí phải có đuôi tam giác chỉ đúng vào điểm.
- **Khung ảnh:** ảnh tiện ích/ảnh nhỏ nằm TRỌN trong khung chữ nhật viền gradient (bo góc ~3 cqw, viền ~0.9 cqw), mọi ô giống nhau.
- **Khoanh nhấn:** thẻ so sánh dùng viền khoanh; thẻ "TRƯỚC" viền nét đứt, nhạt/mờ; thẻ "SAU" viền đậm màu nhấn + glow.

### `map_route` (bản đồ + tuyến đường, ~2–10 giây)
Dùng khi giới thiệu vị trí dự án và kết nối tới các điểm đến.
- Nền: ảnh bản đồ của khách hoặc nền tự dựng từ OSM. Camera zoom vào khu dự án, đi theo từng tuyến (`follow`), cuối lùi ra toàn cảnh. Bản 2 giây: rút gọn, một điểm đến.
- Viền khu dự án: nền phủ tối, khu dự án "khoét" sáng; viền màu nhấn vẽ ra rồi thành NÉT ĐỨT chạy liên tục, có vòng sáng nhấp nhô ở điểm đặt tên.
- Tuyến MẢNH: viền ngoài mỏng, nét chính màu nhấn, ở tâm có NÉT ĐỨT màu kem chạy từ điểm đầu tới cuối; đầu tuyến là chấm sáng nhịp thở.
- Bản rút gọn (trong bảng duyệt): đầu tiên KHOANH khu dự án (viền vẽ ra, vùng bên trong sáng lên, nhãn "DỰ ÁN" có đuôi chỉ vào); sau đó tuyến nét vẽ chạy từ khu dự án tới từng tiện ích, ghim vị trí rơi xuống ở đích, callout có đuôi nhọn chỉ vào ghim. Ảnh bản đồ có đánh dấu khu dự án do NGƯỜI DÙNG gửi; chưa có thì hỏi.
- Điểm đến: ghim + nhãn (tên, thời gian, "qua ..."), nhãn nằm dưới đường, ẩn khi ngoài khung hình.
- Cấu hình `map.json`:
```json
{"image":{"file":"assets/map.jpg","size":[960,1080]},
 "project":{"name":"...","polygon":[[x,y],...],"label_at":[x,y]},
 "routes":[{"id":"r1","name":"...","note":"~20 phút","via":"...","points":[[x,y],...],"from":3.0,"to":6.0,"label":"below"}],
 "camera":[{"t":0,"z":1,"c":[x,y]},{"t":3,"z":1.7,"follow":"r1"}],"captions":[]}  /* captions: tạm để trống, phụ đề đã gỡ */
```
- Quy tắc: đường bám đúng tâm đường trên bản đồ (snap theo distance transform); mỗi tuyến 2–3 giây; nhãn không chồng nhau; cần ít nhất 1 điểm đến.
- Dữ liệu vị trí thật (KML): đọc Polygon (ranh dự án), Placemark (tiện ích), LineString (tuyến) rồi đổi lat/lon sang pixel; cần nền có tọa độ (hiệu chỉnh ảnh bằng ≥3 điểm đối chiếu lat/lon↔pixel, hoặc dựng nền OSM Web Mercator); chưa có LineString thì lấy lộ trình bằng OSRM/ORS và bám đường thật; khu đất vẽ tay không tọa độ thì tách vùng theo màu bằng OpenCV lấy polygon; ghi nguồn OSM theo giấy phép, không lấy ảnh nền từ Google.

### `typo_*` (typography nhấn từ khóa, thay hoàn toàn kiểu gõ chữ)
Cụm khóa/tiêu đề ngắn, mỗi lần 1 cụm, dài 1.6–2.5 giây, nền trong suốt khi đặt trên cảnh người nói (trong preset dùng thẻ thì nằm trong thẻ). Công thức: 3 lớp chữ + 1 chi tiết nhấn.
- Lớp 1 (dòng dẫn): `font_script`, hơi phát sáng. Lớp 2 (cụm khóa): `font_bold`, gradient + glow cùng tông (riêng `typo_bronze`: gradient ánh đồng). Lớp 3 (nhãn/phụ): dòng nhỏ hoặc pill, sát cụm khóa, canh phải.
- Chi tiết nhấn: vệt sáng, nét quét, ghim, nhãn bật ra hoặc icon neon một nét.
- Chữ LẤY TỪ LỜI NGƯỜI NÓI, tối đa ~5 từ mỗi lớp. Không dùng nếu câu không có cụm khóa.

| Mẫu | Bố cục | Chuyển động | Dùng khi |
|---|---|---|---|
| `typo_gold` | chữ viết tay "Giới thiệu" có chữ G HOA lớn hơn (kiểu viết khoa) nằm SÁT trên đầu cụm khóa vàng gradient "THE GRAND"; pill vàng "RA MẮT" SÁT dưới cụm khóa, canh phải | cụm khóa mở từ trái + vệt sáng vàng quét, pill bật ra, vệt tan | tên dự án, sự kiện, "ra mắt" |
| `typo_fire` | dòng nhỏ trắng, cụm khóa cam→đỏ, chữ ký trắng "Từng ngày" SÁT dưới cụm khóa, canh phải | cụm khóa mở từ trái, nét đỏ quét DƯỚI chữ rồi TAN, chữ ký hiện | thị trường nóng, tăng trưởng |
| `typo_bronze` | dòng viết tay + ghim đỏ cùng hàng, SÁT trên cụm khóa ánh đồng; mọi chữ ép sát nhau (không có nhãn phụ bên dưới) | ghim rơi xuống, cụm khóa hiện dần | vị trí, khu vực, cao cấp |
| `typo_neon_orange` | dòng nhỏ; chữ ký neon "lợi thế" bên trái với pill cam "ĐỘC QUYỀN" SÁT DƯỚI, co giãn đúng chiều ngang chữ ký; cụm khóa "LỚN" bên phải cao bằng cả khối (chữ ký + pill) | chữ ký mở, pill bật, cụm khóa mở | khái niệm, lợi thế, từ khóa |
| `typo_neon_blue` | số lớn xanh "12 TỶ"; chữ ký "giá trị" nằm trên MÉP TRÊN số; "lên" và "đến" là hai chữ xếp dọc bên trái, tổng cao bằng số; icon tiền vàng neon ở GÓC TRÊN PHẢI số | chữ ký hiện, "lên/đến" hiện, số mở, icon rơi vào | số liệu, giá, giá trị |

Quy tắc: icon KHÔNG đè lên chữ (cùng hàng dòng đầu ở khoảng trống bên phải, hoặc giữa dòng 1 và 2); vệt/nét quét nằm DƯỚI hoặc qua cụm khóa rồi tan; pill/nhãn sát cụm khóa; chọn icon theo nội dung (tiền, ghim, nhà); mỗi video đổi mẫu và màu qua lại, không dùng cùng một mẫu hai lần liền; không che mặt người nói. Cấu hình: `{"type":"typo_fire","t_in":12.4,"t_out":15.0,"lines":["thị trường đang","TĂNG NHIỆT","Từng ngày"]}`.

### `photo_cards` (thẻ ảnh lớn + chữ phụ + số đếm)
- Bố cục đã chốt: "diện tích" (viết tay) và "CĂN HỘ" SÁT nhau ngay trên ảnh; dưới ảnh cột trái "rộng rãi" (chỉ một dòng, không dòng phụ), cột phải "VIEW SÔNG"; số đếm dưới cùng, hậu tố viết tay ("cư dân") đặt SÁT chân số.
- Mỗi cảnh: dòng dẫn mỏng (trái, trên thẻ) → tiêu đề đậm nghiêng (lệch phải, ép sát dưới dòng dẫn) → thẻ ảnh (pop) → chữ phụ dưới thẻ. Chữ so le: các từ trong cụm lệch độ cao nhẹ, dòng đậm ép sát dòng mỏng.
- Chữ phụ đổi chỗ theo lời nói: từ đơn nhỏ → cụm lớn ở giữa kèm từ nhỏ trái → cụm lớn mới kèm hai từ nhỏ trái/phải (từ nhỏ ở lại, cụm lớn thay nhau).
- Số đếm: nhãn trái, số lớn nghiêng lệch xuống phải đếm từ→đến, hậu tố viết tay xuống dòng dưới.
- Cấu hình: `{type:"photo_cards",scenes:[{dur,kicker,title,image,caption,layout:{kickerX,kickerY,titleX,titleY,titleStagger,titleSize,kickerSize},subs:[{t,out,text,size:"xl|l|m|s",x,y,stagger}],count:{t,prefix,from,to,suffix,dur,y}}]}` (kích thước/vị trí tính theo 1/100 bề rộng khung). Ảnh lấy từ `assets/`, không có thì hỏi.

### `amenity_grid` (lưới tiện ích)
- Mỗi mục: ô ảnh trong KHUNG viền gradient (ảnh nằm trọn), nhãn dưới là chip khoanh-icon + tên; tiêu đề pill theo quy ước chung.
- Ảnh nhỏ viền sáng + nhãn dưới, hiện lần lượt (pop) vào lưới 2 cột theo đúng nhịp người nói liệt kê; cột phải thấp hơn cột trái một nhịp. Tùy chọn thẻ kết (ví dụ mặt bằng: chữ lớn trên, thẻ ảnh giữa, chữ dưới trái, huy hiệu ảnh nhỏ dưới phải).
- Cấu hình: `{type:"amenity_grid",stagger:0.45,hold:1.2,items:[{label,img}],final:{title,img,badge}}`. Tối đa 8 mục mỗi lưới (hơn thì chia 2 lưới). Mỗi mục hiện đúng lúc người nói nhắc tên nó.
- Biến thể "cây liên kết" xem `tree_diagram` bên dưới.

### `connect_flow` (kết nối A → B, ~6 giây)
Dùng khi nhắc "kết nối với...", "tích hợp", "nằm sẵn trong...". A là bảng nhỏ (công cụ/dịch vụ), B là bảng lớn (giao diện hoặc nơi nó được dùng). KHÔNG có chữ nào đè lên đường nối.
- Bố cục: A ở góc trên trái (x 10, y 6, rộng 48, cao 17); B bên dưới rộng gần hết chiều ngang (x 8, y 45, rộng 84, cao 46). Đường nối đi từ GIỮA MÉP DƯỚI của A tới GIỮA MÉP TRÊN của B, cong chữ S mềm (điểm điều khiển cách đầu mút ~55% khoảng cách dọc).
- Trình tự (1×): 0.0 bảng A trượt lên → 0.5 chấm tròn nổi lên ở giữa mép dưới A (viền màu nhấn, quầng sáng, vòng sáng lan) → 0.9 nét gradient vẽ ra từ chấm A, đầu nét sáng chạy về B trong 1.1 giây (ease-out); bảng B trượt lên khi nét đi được ~55% → 2.0 nét chạm B, chấm đón nổi lên ở giữa mép trên B, hai chấm được nối bằng nét liền → từ 2.1 nét thành các đoạn đứt trắng chạy liên tục A→B → từ 2.5 các dòng trong B hiện lần lượt cách 0.4 giây; nút phụ (ví dụ "GMAIL CÁ NHÂN") hiện cuối ở đáy B, tùy chọn.
- Cấu hình: `{type:"connect_flow",a:{title,icon,x,y,w,h},b:{title,x,y,w,h,rows:[{t}],badge},curve:0.5}`. Hai chấm đúng tọa độ hai đầu đường; vẽ bằng SVG (stroke-dasharray + stroke-dashoffset theo độ dài đường, đầu sáng đi theo điểm trên đường). Không đặt nhãn đè lên đường; nếu người dùng muốn nhãn thì đặt lệch ra ngoài đường.

### `chart_bars` (biểu đồ cột)
Tiêu đề lệch phải + thẻ biểu đồ. Cột mọc lần lượt (cách ~0.25 giây), giá trị hiện trên cột, cột cuối nhấn màu đậm kèm nhãn ("+35%"). Cấu hình: `{type:"chart_bars",kicker,title,unit,data:[{label,value}],highlight:<chỉ số cột nhấn>,tag,stagger:0.25}`. Số liệu LÀ SỐ THẬT do người dùng cung cấp; không có thì hỏi, tuyệt đối không bịa. Nhãn nhấn đặt ở góc trên của thẻ, không đè nhãn giá trị của cột.

### `popup_notes` (ảnh có chú thích)
Ảnh/ảnh chụp màn hình; mỗi chú thích gồm ghim (có vòng sáng) + bong bóng (chỉ MỘT dòng chữ chính, không dòng phụ), bật ra đúng lúc người nói nhắc ý đó. Bong bóng không đè nhãn ảnh hay ghim khác. Cấu hình: `{type:"popup_notes",kicker,title,image,notes:[{t,px,py,bx,by,text,sub}]}` (px,py: ghim; bx,by: bong bóng; đều theo % của ảnh). Nội dung lấy từ người dùng, không tự bịa.

### `tree_diagram` (nhánh cây)
Bố cục theo mẫu người dùng đưa: MỘT thẻ cha ở trên (tối, logo trong vòng khoanh, tên, nút nhỏ, huy hiệu tròn góc trên phải như "0Đ"), BA thẻ con trắng bên dưới xếp sát nhau, rộng hơn thẻ cha, thẻ cha nằm giữa so với các thẻ con.
- Trục nằm bên TRÁI các thẻ con. Đường nối đi từ giữa mép TRÁI thẻ cha, ngang sang trái tới trục, xuống dọc theo trục, rẽ ngang vào mép trái từng thẻ con. Có CHẤM tròn ở mép trái thẻ cha và ở mép trái mỗi thẻ con (nơi đường tới).
- Chuyển động: thẻ cha trượt lên, chấm cha nổi lên (0.5 s); nét màu nhấn vẽ ra từ chấm cha, đầu nét của cả 3 nhánh chạy CÙNG tốc độ (~55 cqw/giây) nên nhánh ngắn tới trước; nét tới thẻ con nào thì chấm đón nổi lên và thẻ con đó trượt vào từ phải. Sau khi nét tới nơi, đoạn ĐỨT màu trắng chạy liên tục từ thẻ cha xuống từng thẻ con (cùng pha trên đoạn trục chung). Thẻ con: icon khoanh, tên, dòng phụ, bên phải huy hiệu ("×2", "AI") hoặc thanh chạy đầy.
- Cấu hình: `{type:"tree_diagram",parent:{title,button,badge,icon},items:[{title,icon,value|bar}]}`. Đúng 3 thẻ con (nhiều hơn thì chia hai cụm). Mẫu chạy: `effects/reference/duyet-tat-ca-hieu-ung.html`.

### `glass_list` (danh sách kính mờ, "glassmorphism")
Dùng khi liệt kê 3 ý/lý do/giá trị kèm số thứ tự, cần cảm giác cao cấp, hiện đại. Hợp nhất với preset C và B (nền tối/đậm có màu), preset A dùng bản kính trắng mờ.
- Phía sau: 2 quầng sáng tròn mờ (màu nhấn) trôi chậm, để kính mờ có thứ làm mờ.
- Trên: nhãn viền kính (pill), tiêu đề hai dòng lớn (dòng 1 trắng/màu chữ, dòng 2 gradient màu nhấn, mở từ trái). KHÔNG có dòng phụ (subtext) ở bất cứ chỗ nào của hiệu ứng này. Preset A/B có thêm thẻ kính nghiêng -11° góc phải (chữ ngắn + nút mũi tên tròn); preset C bỏ thẻ này vì chỗ đó là vòng tròn người nói.
- Preset C: vòng người nói được HẠ XUỐNG nằm hẳn trong vùng an toàn (đỉnh y=27.5 cqw, cách mép phải 10 cqw) để mặt không dính giao diện nền tảng; các hiệu ứng khác của C vẫn dùng vị trí cũ (đỉnh y=6) cho tới khi người dùng yêu cầu hạ chung.
- Dưới: BA thẻ kính xếp sát nhau (cao ~13.4 cqw, cách ~2.2 cqw): vòng icon kính, tên (chữ lớn 5 cqw, MỘT dòng, không dòng phụ), số "01 02 03" mờ ở bên phải ngăn bằng vạch mảnh. Thẻ trượt lên lần lượt cách 0.5 giây, mỗi thẻ có vệt sáng quét qua mặt kính.
- Công thức kính: nền gradient trắng 22%→5%, viền trắng 35% (viền trên 65%), `backdrop-filter: blur(2.4cqw) saturate(1.4)`, bóng đổ + viền sáng bên trong. Preset A: nền trắng 70%→28%.
- Cấu hình: `{type:"glass_list",pill,title:["dòng 1","dòng 2"],badge:{lines:[...]},items:[{title,icon,no}]}`. Đúng 3 thẻ. Mẫu chạy: `effects/reference/duyet-tat-ca-hieu-ung.html`.

### `logo_pop` (icon pop + luồng sáng)
Dùng khi người nói nhắc tên 2–4 sản phẩm/công cụ/thương hiệu liên tiếp ("với ba AI này: Claude, Gemini, ChatGPT"). Nền tối cả khối (`dark`), người nói vẫn ở vị trí của preset.
- Nền: vành sáng chân trời (nửa vòng tròn lớn phát sáng màu nhấn) mở dần, một DẢI SÁNG CONG ôm theo đúng đường cong của vành chân trời (cùng bán kính 75 cqw, cao hơn vành ~4 cqw, vẽ ra từ giữa sang hai bên, gradient trắng ở giữa mờ dần hai đầu, làm nhòe bằng blur), quầng sáng mờ sau các icon. Mọi nét sáng đều NHÒE nhẹ (blur ~0.5–1.4 cqw), không sắc cạnh. Các VỆT SÁNG nhỏ (~14 vệt, dài 14–38 cqw, mảnh) bay chéo từ phải xuống trái phía sau, lặp liên tục, mỗi vệt tốc độ và độ trễ khác nhau.
- Icon: thẻ kính bo góc lớn có viền sáng, icon/logo ở giữa. Mỗi icon POP VÀO đúng lúc người nói nhắc tên nó (cách nhau theo lời nói). Chuyển động pop (0.7 s): nhỏ (0.05) → phóng LỚN hơn thật (1.25) → co NHỎ lại một chút (0.9) → về bình thường (1.0). Kết thúc cũng POP RA (0.4 s): phình nhẹ (1.18) rồi co về 0 và mờ, các icon cách nhau 0.1 s.
- Bố cục CÂN ĐỐI qua trục giữa: thẻ giữa 32 cqw ở x=34–66, hai thẻ bên 24 cqw ở x=6–30 và x=70–94 (khe 4 cqw mỗi bên); tổng chiều ngang canh giữa khung. Với 2 hoặc 4 icon thì chia đều, cùng cỡ, vẫn canh giữa.
- Lỗi cần tránh: icon KHÔNG được hiện sẵn ở kích thước thật từ đầu. Hoạt ảnh pop ra không được kích hoạt trước giờ (dùng fill-mode `forwards`, không dùng `both`), nếu không sẽ mất hoạt ảnh pop vào.
- LOGO: dùng ảnh logo do người dùng cung cấp (`assets/logos/<tên>.png`, nền trong suốt). KHÔNG tự vẽ lại logo thương hiệu; chưa có ảnh thì để thẻ chữ tên (như mẫu) và hỏi người dùng logo.
- Cấu hình: `{type:"logo_pop",items:[{name,logo,t_in}],t_out}` (t_in từng icon theo giây trong video; t_out chung). Mẫu chạy: `effects/reference/duyet-tat-ca-hieu-ung.html`.
- Hiệu ứng "pop có nảy" (nhỏ → lớn quá → nhỏ chút → bình thường; thoát: phình rồi về 0) dùng cho MỌI icon/huy hiệu cần "bật ra" nổi bật; còn pop thường (0.3 s, không nảy) giữ cho thẻ.

### `growth_card` (bảng tăng trưởng)
Dùng khi người nói nhắc tốc độ tăng trưởng, phần trăm tăng, "tăng gấp N lần", biểu đồ đi lên. Một thẻ KÍNH MỜ TRONG SUỐT (cùng công thức kính của `glass_list`: nền trắng mờ, viền sáng, `backdrop-filter` blur; nhìn xuyên qua nền) bo góc lớn, có HAI ĐỐM MÀU MỜ phía sau (như `glass_list`) để kính có thứ làm mờ; chữ dùng màu `--glt`/`--glm` của preset. RỘNG BẰNG KHUNG NGƯỜI NÓI phía dưới (88 cqw, tức x=6–94 trên khung; trong hệ toạ độ của khối hiệu ứng thu 0.8 là rộng 110, left −5), cao 72 (bo 9 cqw), canh giữa. Thẻ là nền nên được phép rộng hơn vùng an toàn; mọi chữ và đường cong nằm trong vùng an toàn (đường cong chừa mép 5 cqw mỗi bên thẻ).
- Trong thẻ (trên xuống): chip chọn kỳ ("Tháng ⌄") ở góc trên phải (không có dòng "cập nhật"); đường cong tăng trưởng với 4 chấm mốc; nhãn ("Tỷ lệ chuyển đổi"); SỐ LỚN trắng (12.5 cqw, vừa phải để không lấn thẻ) đếm từ 0 lên giá trị kèm "%"; dòng phụ nhỏ ("tăng so với tháng trước").
- Dải sáng CHẤT LỎNG ở đáy thẻ: 4 khối sáng mờ (màu nhấn, blur ~2.6 cqw) trôi ngang, co giãn và đổi hình bo tròn liên tục (chu kỳ 4.4–7.4 s, lệch pha nhau), cộng viền sáng bên trong đáy thẻ "thở" nhịp chậm. KHÔNG bao giờ dừng, chuyển động nhẹ nhàng.
- Trình tự: thẻ trượt lên (0 s) → đường cong vẽ từ TRÁI sang PHẢI trong 1.8 s (nét chính + lớp nhòe sáng phía sau) bắt đầu 0.5 s → BA chấm mốc nhỏ nổi lên đúng lúc đầu nét đi qua, mỗi chấm thả một vạch dọc mảnh mờ dần xuống → chấm SÁNG NHẤT chạy cùng đầu nét từ mép trái tới đúng đỉnh cao nhất rồi DỪNG ở đó và CHỚP CHỚP liên tục (co 0.62 / mờ 0.45 ↔ đầy, chu kỳ ~0.9 s) → nhãn hiện (1.2 s) → số đếm 0 → giá trị (1.9–3.4 s). Đường cong dùng nội suy Catmull-Rom qua các mốc; thời điểm chấm mốc và chấm sáng tính theo chiều dài nét để khớp đầu nét.
- Dữ liệu thật: các mốc (x, y), giá trị đỉnh, nhãn, kỳ do người dùng/lời nói cung cấp. Không bịa số.
- Cấu hình: `{type:"growth_card",updated,period,label,value,suffix:"%",caption,points:[[x,y],...],peak:<chỉ số điểm cao nhất>,milestones:[chỉ số các điểm mốc]}`. Mẫu chạy: `effects/reference/duyet-tat-ca-hieu-ung.html`.

### `note_board` (bảng điều kiện)
Tiêu đề pill (icon list khoanh); mỗi dòng có icon khoanh riêng (mũ cử nhân, thư, khiên…), tên (một dòng), ô tích bên phải. Các dòng mờ sẵn; dòng đang nói sáng viền và được tích (cách ~1.1 giây). Cấu hình: `{type:"note_board",title,rows:[{t,sub,icon}]}`.

### `popup_notes` (bổ sung)
Chấm trên ảnh hiện trước, rồi NÉT chạy từ chấm tới bong bóng (0.5 giây), bong bóng bật ra đúng khi nét tới nơi.

### `warning_stamp`
Biểu tượng cảnh báo đập xuống (rung nhẹ), chữ lớn "ĐỪNG MUA" mở từ trái, KHÔNG có dòng phụ.

### `compare_cards`
Hai thẻ cạnh nhau: TRƯỚC (viền đứt nhạt, chữ mờ, ô tròn rỗng) và SAU (viền khoanh đậm, glow, ô tích hiện lần lượt).

### `feature_card`, `metaphor_card`
Hai dòng chữ dưới hình ép sát lên trên (khoảng hở ≤ 1.6 cqw). Không đổi gì khác.

### `speaker_only`
Mặt người nói nằm ở NỬA TRÊN khung hình; phụ đề/chữ (nếu có) nằm ở NỬA DƯỚI trong thẻ.

### `count_up` và `big_number`
- `count_up`: số đếm từ 0 đến giá trị cần nhấn (ví dụ "5 THỨ NÀY": đếm 0→5 trong ~1.3 giây, bước ~0.26 giây).
- `big_number` kiểu "0Đ": chữ số rất lớn (~50 cqw), ký hiệu "Đ" nhỏ hơn (~24 cqw) đứng cạnh, chừa lề phải để không bị cắt khi nghiêng.

### Hiệu ứng còn ở dạng mô tả (chưa có mẫu xem)
`feature_card`, `screenshot_card`, `product_badge`, `cinematic_break`: dựng theo mô tả ở bảng mục 5 và `effects/CATALOG.md`, dùng token của preset; BẮT BUỘC chụp khung thử cho người dùng duyệt trước khi dựng cả video. Sau khi người dùng duyệt, ghi quy cách vào mục này.

## 7. Người nói tách nền (chỉ khi preset yêu cầu, ví dụ preset A)
Chi tiết theo file preset. Tóm tắt: dùng `rembg` với mô hình `u2net_human_seg` (`pip install rembg onnxruntime`, mô hình tự tải lần đầu); chạy trên khung đã thu nhỏ (~540×960) rồi phóng lại nếu máy chậm; chỉ giữ vùng lớn nhất (bỏ mảng rác như mảng gạch trên đầu); làm mịn viền (guided filter hoặc làm mờ 1–2 px) và làm mượt alpha giữa các khung liên tiếp để tóc không nhấp nháy; khung nào còn rác thì dùng khung lân cận. Tách một lần rồi dùng chung cho mọi cảnh, báo người dùng thời gian ước tính vì máy không có GPU. Khung người nói gần vuông (rộng bằng ngang video 1080, cao ~1080), bắt đầu cách đỉnh đầu theo preset, vì người nói chiếm rất lớn khung hình gốc (đầu cao ~45%); không dùng khung dẹt.

## 8. Phông chữ (bắt buộc kiểm tra trước khi dựng)
- Phông KHÔNG tải từ mạng (Google Fonts, CDN). Chỉ dùng file cục bộ trong `assets/fonts/`, khai báo `@font-face` đường dẫn tương đối.
- Ba vai phông (KHÔNG tự đổi sang phông khác; chưa có file thì hỏi, không dùng phông dự phòng của hệ thống):

| Vai | Dùng cho | File (trong `assets/fonts/`) |
|---|---|---|
| `font_script` | chữ viết tay/thư pháp: dòng dẫn, chữ ký ("Từng ngày", "nếu thiếu") | `OAI SHOWTILLA.OTF` |
| `font_bold` | cụm khóa đậm, tiêu đề, số lớn | `BTDanta-Bold.otf` (số rất lớn, tiêu đề nhấn: `BTDanta-ExtraBold.otf`) |
| `font_text` | chữ phụ, nhãn, phụ đề | `BTDanta-Medium.otf` |

- Các phông khác trong `assets/fonts/` (OAI AGNIFA, IRONFIST, OTEGLOS, RANGUNA, BROVILE, CHERIONE, LACOTTE, LAWRAISE, PORK-BELLY, QYLEN, THE-RAMBLER, VALTER-STD, `BTDantaVF.ttf`) chỉ dùng khi người dùng yêu cầu rõ. Người dùng gọi phông viết tay là "OAI Showtilla Regular", khớp file `OAI SHOWTILLA.OTF`; không thấy file thì hỏi lại.
- Kiểm tra dấu tiếng Việt trước khi dựng: dựng một khung thử mỗi vai phông chứa chuỗi `ĂÂÊÔƠƯĐ ẰẮẲẴẶ ẦẤẨẪẬ ỆỔỖ ỤỨỮ ỜỚỞỠỢ ăâêôơưđ ằắẳẵặ ầấẩẫậ ệổỗ ụứữ ờớởỡợ`, chụp và mở ra xem. Có ô vuông, thiếu dấu hoặc phông bị thay thì dừng và báo; đạt mới dựng tiếp. Sau khi render, mở 1–2 khung video thật để xác nhận lại.
- Chữ gradient/`background-clip:text`: BT Danta có dấu rất cao nên PHẢI nới khung chữ (padding trên ~0.4em, dưới ~0.25em, bù bằng margin âm), nếu không dấu bị cắt ("ĐỪNG" thành "ĐƯNG").
- BT Danta là phông rộng: cụm khóa 8–13 cqw tùy độ dài, một dòng tối đa ~12 ký tự ở cỡ lớn. Không có bản nghiêng thật; chỗ nghiêng là nghiêng giả, bỏ nghiêng nếu xấu.
- OAI Showtilla nét mảnh: cỡ nhỏ khó đọc; dùng cỡ lớn (≥ 15 cqw cho dòng ký tự) kèm viền ~0.2–0.3 cqw và glow nhẹ; không dùng cho dòng dài.

## 9. Phiên âm trên máy này (đã chạy được)
- Không đưa thẳng video cho `faster-whisper` (lỗi thư viện `av`). FFmpeg tách âm thanh `-vn -ac 1 -ar 16000 -f f32le -` rồi đưa mảng numpy cho `transcribe`, `word_timestamps=True`.
- Máy không có GPU NVIDIA: `WhisperModel('small', device='cpu', compute_type='int8')`, `language='vi'`.
- Ghi kết quả bằng `open(..., encoding='utf-8')`; không `print` ra PowerShell (lỗi bảng mã). Lưu `work/<ten>/transcript.json` (từng từ kèm giây) và `transcript.srt`.
- Model nghe sai nhiều từ (ví dụ "skill", "tiện ích", "typography", tên riêng): luôn đưa lời cho người dùng sửa trước khi chia cảnh.

## 10. Định dạng `timeline.json`
```json
{
  "preset": "xanh_gradient",
  "source": "input/video.MOV",
  "output": {"name": "ten_v1", "size": [1080, 1920], "fps": 30, "language": "vi"},
  "cuts_original_seconds": [[8.24, 8.58]],
  "duration_after_cut": 39.1,
  "scenes": [
    {"id": "s1", "t_in": 0.0, "t_out": 6.0, "effect": "typo_fire",
     "caption": "lời hiển thị", "data": {"lines": ["ĐỪNG MUA SKILL", "nếu thiếu"], "count_up": {"from": 0, "to": 5}}},
    {"id": "s2", "t_in": 6.0, "t_out": 12.0, "effect": "chart_bars", "group": "g1",
     "data": {"title": "BIỂU ĐỒ", "data": [{"label": "2024", "value": "ĐIỀN"}], "highlight": 4}}
  ],
  "captions": {"off_ranges_after_cut": [[24.0, 32.0]]},
  "audio": {"music": null, "sfx": null, "duck_music_under_voice": true}
}
```
- Mốc giây theo video đã cắt. Trường chưa có dữ liệu ghi `"ĐIỀN"` (Claude Code phải hỏi, không tự bịa). Cảnh cùng `group` = một cụm hiệu ứng liên tục.

## 11. Quy tắc làm việc
- Không xóa hay ghi đè file gốc. Không tải file từ nguồn lạ. Không đăng hay gửi video đi đâu.
- Việc nào chưa chắc (đoạn cắt, từ nghe không rõ, nhạc chưa có, dữ liệu thiếu) thì hỏi, đừng đoán.
- Mỗi lần xong một bước lớn, báo ngắn: đã làm gì, file ở đâu, bước kế tiếp.
- Nếu một công cụ lỗi (ví dụ render), nói rõ lỗi là gì rồi đề xuất cách sửa, không lặp lại cùng một lệnh.
- Khung thử luôn render bằng HyperFrames từ HTML (không dùng PIL) và bám đúng mã giao diện mẫu trong `reference/` khi preset có.

## 12. Kinh nghiệm đã chạy được (tools/ và mẫu)
Bổ sung từ dự án thật. Công cụ nằm ở `tools/` (xem `tools/README.md`).

### Thứ tự làm việc
Theo Bước 4 → 5 → 6: chia cảnh, tạo trang chọn hiệu ứng, chờ người dùng dán kết quả, tạo trang storyboard để chốt, rồi mới dựng và xem thử. Dữ liệu thiếu thì dựng khung giữ chỗ để duyệt; bản cuối không được còn nhãn "ẢNH CẦN CHÈN", "SỐ MẪU", "NHÃN n". Khi nghi ngờ lời nói lặp/vấp (nói lại cả câu), cắt đoạn đầu và báo người dùng.

### Vùng an toàn: luôn cho người dùng xem
- Chuẩn hiện hành là mục 4 (trên 15% = 288 px, dưới 25% = từ y 1440 px, hai bên 10% = 108 px); đây là số đo gần đúng, không đo trực tiếp từ app.
- Cách xem: `python build.py guides` (trong `tools/preset_A_example/`) vẽ vùng đỏ gạch chéo và khung xanh lá "VÙNG AN TOÀN" lên video xem thử. Xuất bản chuẩn thì dùng bản sạch. Kết hợp `tools/safe_check.py` để kiểm tự động.
- Đồ họa (thẻ, chữ) đặt trọn trong khung xanh lá; cỡ chữ ~38–44 px là vừa. Thấy "to quá" thì thu nhỏ trước khi hỏi.
- Preset A: khung người nói 950x950 sát đáy video nằm một phần trong vùng che dưới (video được phép tràn). Khi có phụ đề kiểu mới, không được che miệng: dịch hoặc thu nhỏ người nói (mục 4).

### Preset A: người nói tách nền, đầu nhô khỏi khung
- `python -I tools/matte_person.py cut.mp4 person.webm 24` (khoảng 2 phút cho clip 17 giây, máy không GPU).
- Trong HyperFrames: lớp 1 là video thật trong khung (clip-path bo góc), lớp 2 là `person.webm` cùng vị trí và cùng kích thước, chỉ lấy phần trên cùng (`clip-path: inset`) để tóc nhô lên khỏi mép khung. Mép khung nằm khoảng 90–100 px dưới đỉnh tóc.
- Cảnh chỉ người nói: khung mở rộng toàn khung bằng `clip-path` + `scale` của video (không animate width/height), thu lại khi cảnh đồ họa vào.

### Âm thanh đã cân bằng
- Giọng quay điện thoại thường nhỏ (~ −31 dB trung bình): tăng bằng `data-volume="3"` trên `<video data-has-audio>` (đỉnh vẫn dưới −3 dB).
- Nhạc nền `data-volume≈0.055` với file nhạc ~ −14 dB trung bình (thấp hơn giọng hơn 18 dB), mở dần 0.8 giây, tắt dần 1.6 giây.
- SFX nhẹ khi thẻ/nhãn bật lên: thông báo `data-volume≈0.30`, tiếng kim loại lớn một lần ở nút kêu gọi `≈0.22`. Mỗi `<audio>` cần `id`.
- Đo sau khi render: `ffmpeg -i out.mp4 -af volumedetect -vn -f null -` (tổng thể quanh −21 dB trung bình, đỉnh dưới −2 dB).
- Thư viện của người dùng: nhạc `E:\AM THANH\NHAC NEN GOOGLE MUSIC`, sfx `E:\AM THANH\HIEU UNG AM THANH\AM THANH LUXURY` (chỉ copy file cần dùng vào `assets/music`, `assets/sfx` của dự án, không sửa file gốc).

### Lỗi HyperFrames đã gặp
- Phải nạp GSAP trong `<head>`: `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>`.
- Nét SVG thẳng đứng/ngang dùng gradient mặc định sẽ KHÔNG hiện (bbox rộng 0): dùng `gradientUnits="userSpaceOnUse"` hoặc màu đặc.
- `fromTo` mặc định `immediateRender`: hai `fromTo` cùng một phần tử ở hai mốc khác nhau sẽ ghi đè trạng thái đầu; dùng `.to` cho lần sau.
- Thư mục dự án chỉ có MỘT file HTML gốc (`index.html`); file nguồn đặt ngoài.
- Render: `npx hyperframes render -q draft` để xem nhanh, `-q delivery` để xuất bản.
