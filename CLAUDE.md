# CLAUDE.md — Hồ sơ dự án Cloud Edit Video (Hào Sky Land)

File này Claude Code tự đọc mỗi phiên. Hào không cần nhắc lại những gì ghi ở đây.

**Đọc trước khi nhận việc:** mục lục `docs/00-MUC-LUC.md`; trước khi dựng video: `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` (lỗi Hào đã chỉ ra); việc nào giao AI nào `docs/01-he-thong/AI-NAO-VIEC-NAO.md` (Claude tự đề xuất chuyển AI khi việc hợp công cụ khác hơn, theo mục 6 của file đó); làm một video `docs/02-quy-trinh/QUY-TRINH-MOT-VIDEO.md`; đặt tên/thư mục `docs/01-he-thong/THU-MUC-VA-DAT-TEN.md`.

## Mục đích
Làm video ngắn đăng TikTok (9:16) và YouTube (16:9) cho thương hiệu Hào Sky Land: bất động sản, góc nhìn dòng tiền, khách mục tiêu là nữ 35–55 tuổi ở trung tâm và khu Đông TP.HCM.

## Người dùng
- Hào, không rành code. Giao việc kiểu "làm giúp tôi"; Claude tự chọn phương án đơn giản nhất và báo lại ngắn gọn bằng tiếng Việt.
- Giải thích thuật ngữ tiếng Anh bằng tiếng Việt trước.
- Giỏ hàng hiện tại: Vinhomes Hóc Môn, Vinhomes Cần Giờ. Các dự án khác chỉ là đã nghiên cứu, không phải đang phân phối.

## Bối cảnh bổ sung (Hào xác nhận 12/11/2026)
- Repo riêng tư. Hào có thể dành cả ngày cho dự án, giới hạn là token.
- Giọng đọc: Hào tự thu. Video đầu: TikTok khoảng 130 giây, từ kịch bản thô, flycam thô, giọng thu và video mẫu cắt cảnh. Hào có bộ logo và màu thương hiệu riêng (chưa gửi).
- Cách làm chính là **cắt ghép footage thật trong app studio** (`docs/02-quy-trinh/QUY-TRINH-MOT-VIDEO.md`). Mẫu đồ họa HyperFrames dùng cho cảnh chữ/số, không phải nguồn chính.

## Cấu trúc
- `docs/`: tài liệu theo thư mục đánh số (`00-MUC-LUC.md`, `01-he-thong/`, `02-quy-trinh/`, `03-ke-hoach/`, `04-thu-vien/`, `05-app/`, `99-luu-tru/` cho cách làm cũ). Thêm/dời tài liệu thì sửa `00-MUC-LUC.md`.
- `mau/`: mẫu để nhân bản: `du-an-video/` (BRIEF, NGUON-SO-LIEU, KICH-BAN, STORYBOARD, DANG-BAI, KET-QUA; app tự chép vào dự án mới), `PROMPT-MAU.md` (câu lệnh cho từng AI).
- `video-studio/thu-vien-am-thanh/`: hiệu ứng âm (`hieu-ung/<nhóm>_<tên>_<số>.wav` + `hieu-ung.json`, tạo bằng `scripts/tao_sfx.py`), `nhac/` chờ kho nhạc. Hàng `sfx` trong timeline, trộn bằng `scripts/am_thanh.py`.
- `video-studio/thu-vien-mau/`: mẫu edit (`<loại>-<số>_<tên>/mau.json + MAU.md`), áp bằng `scripts/ap_mau.py` hoặc app (nút ✦ Thư viện mẫu).
- Tên thư mục video: `<ngày>_<tiktok|youtube>_<dự án>_<chủ đề>`, ví dụ `2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue`.
- `video-studio/projects/<tên>/timeline.json`: **định dạng timeline v1** (cảnh, chuyển cảnh, chữ, âm thanh), mô tả trong `video-studio/scripts/timeline.py`, kiểm tra bằng `scripts/test_timeline.py`. Dựng: `python3 scripts/dung.py projects/<tên>` → `out/<tên>.mp4`. Mẫu: `projects/test90`.
- `video-studio/studio/`: **app timeline** (máy chủ Python `server.py` + trang `index.html`). Chạy: `python3 studio/server.py` (thêm `--lan` cho điện thoại cùng wifi); Windows: bấm đúp `chay-studio.bat`. Mở đúng link có `?t=` (mã khóa).
- `video-studio/videos/*.json`: spec mẫu đồ họa cũ (HyperFrames). Trường `template` chọn mẫu.
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
| Định dạng timeline v1 + `scripts/dung.py` | Xong 12/11: kiểm tra định dạng có test; dựng thử đầu cuối với footage giả (khối 3D, cắt thẳng, chữ, nhạc) OK; chưa dựng lại video test 89s với footage thật |
| Thư viện hiệu ứng v1 (`scripts/effects.py`, danh mục `docs/04-thu-vien/THU-VIEN-HIEU-UNG.md`) | Xong 12/11: 3 phong cách, 4 chỉnh màu, 10 chuyển cảnh, 6 hiệu ứng chữ, 9 khối chữ; demo 41s `projects/thu-vien` dựng với footage thật, đã xem khung hình. Chưa có: âm thanh hiệu ứng thật, màu/logo thật, mẫu bố cục |
| App timeline v2 (`studio/`) | 12/11: giao diện theo ảnh mẫu Hào gửi — 9 tab, khung xem phát được (bản xem trước 540p tự tạo), timeline 7 hàng kéo thả, tách/xoá, hoàn tác/làm lại, Lịch sử, Thư viện, Dựng nháp/Xuất video. Đối chiếu: `docs/05-app/GIAO-DIEN-TINH-NANG.md`. Định dạng thêm `subtitles`, `cards`, `zooms`, `broll`, `audio.voice`. Mẫu: `projects/mau-noi-truoc-may`. Chưa: phụ đề tự sinh từ giọng, cắt khoảng lặng, logo/màu thật. Chưa thử trên Windows/điện thoại thật |
| Khung YouTube 16:9 | Xong 12/11: `meta.platform` = `tiktok` (1080×1920) hoặc `youtube` (1920×1080); bộ dựng, chữ/phụ đề/minh hoạ, chuyển cảnh 3D/gl, khung xem và vùng an toàn theo khung. Footage quay dọc trong khung ngang tự đặt giữa + hai bên nền mờ (`fit`: crop/blur từng đoạn). Dựng thử với footage thật của Hào, đã xem khung hình |
| Dự án mới trong app (nút ＋) | Xong 12/11: duyệt thư mục footage trên máy chạy studio (cả từ điện thoại), mỗi video thành một đoạn; liên kết cứng nên không chép thêm (khác ổ thì chép); nhân bản dự án sang khung kia (tab Khung hình). Nhạc nền từ file .mp3/.wav/.m4a trong thư mục (tự lặp, mờ cuối). Chưa thử trên Windows |
| Video test 89s (`projects/test90`) | Hào duyệt "rất ok" 12/11; âm thanh hiệu ứng chưa ổn, chờ thư mục âm thanh. Footage và bản dựng test đã xóa theo yêu cầu (bản gốc còn trên Drive thư mục "Hào") |
| Tải từ Drive trên cloud | Được: môi trường cloud "test" mở mạng tới drive.usercontent.google.com; thư mục phải chia sẻ bằng link |
| Phụ đề tự động (`scripts/phu_de.py`, nút trong app) | Xong 12/11: faster-whisper large-v3-turbo, tiếng Việt, mốc từng từ, chia dòng ≤7 từ/2,8s; chỉ thay phụ đề `auto`. Thử trên clip thật của Hào (nhận dạng đúng tên dự án, số điện thoại). Môi trường cloud "test" đã mở mạng Hugging Face. Chưa thử trên PC |
| Master cut (`scripts/master_cut.py`, `phan_tich_hinh.py`, nút trong tab Cắt) | Xong 12/11: cắt im lặng theo âm lượng thật (không chỉ mốc từ), chừa nghỉ cuối câu, bỏ tiếng đệm, bỏ lần nói vấp (cụm ≥3 từ lặp sau ngập ngừng), chấm điểm khung hình (nét, sáng, cháy, màu, chuyển động, giật, mặt người nói — OpenCV 4.x), đoạn không lời rút theo nhịp + dời về khúc đẹp nhất, cảnh trám dời về khúc đẹp hơn, phóng xen kẽ ~4s; chữ/phụ đề dời theo; báo cáo `build/master-cut.md`. Test: `scripts/test_master_cut.py`. Thử trên clip thật của Hào. Chưa thử trên PC; ngưỡng mới chỉnh trên vài clip DJI/iPhone |
| Màu (`scripts/mau.py`) | 12/11: footage DJI/iPhone là HDR HLG → chuyển tông hable sang BT.709 ở mọi nơi (nguyên nhân video nhạt); tự cân màu từng cảnh; 9 filter (`effects.LOOKS`, có CSS xem trước); âm lượng −14 LUFS (`loudnorm`) |
| Thư viện chuyên nghiệp (`video-studio/thu-vien-chuyen-nghiep/`, `docs/04-thu-vien/THU-VIEN-CHUYEN-NGHIEP.md`) | 12/11: 10 repo GitHub kiểm chứng giấy phép từ file gốc, thêm dạng submodule: OpenTimelineIO, gl-transitions (214 chuyển cảnh), PySceneDetect, auto-editor, ffmpeg-normalize, DeepFilterNet, Practical-RIFE, Real-ESRGAN, colour, motion-canvas. Đã dùng: chuẩn âm lượng, gl-transitions, OpenTimelineIO; các repo khác là kế hoạch tích hợp |
| Chuyển cảnh gl-transitions | Xong 12/11: 212 chuyển cảnh (`scripts/gl_transitions.json`, tên `gl-<Tên>`) trong Thư viện app, tìm + xem thử WebGL trực tiếp; dựng bằng HyperFrames. Kiểm cả 212 bằng `scripts/kiem_gl.mjs`; dựng thử 3 cái (CrossZoom, BookFlip, Dreamy) với footage thật |
| Xuất Premiere/DaVinci (`scripts/xuat_nle.py`, nút “Premiere/DaVinci”) | Xong 12/11: `out/<tên>.xml` (Premiere), `.otio` (DaVinci), `.srt`; chuyển cảnh → hòa tan, chữ/zoom → marker, cảnh trám hàng V2, giọng hàng A1. Đã đọc lại bằng OTIO (thời lượng khớp). **Chưa mở thử trong Premiere/DaVinci thật** |
| Kho hiệu ứng âm + mẫu `edit-phim-01` ("Mẫu edit video 1 chuyên nghiệp") | Xong 12/11: phân tích video mẫu 55s (chữ, chuyển cảnh, âm: `thu-vien-mau/edit-phim-01_chuyen-nghiep/MAU.md`); 21 âm tự tổng hợp; hàng ♪ Hiệu ứng âm trong app (nghe thử, thêm tại kim, phát khi xem trước); phong cách `edit-phim`, chữ `zoom-blur`, khối `title3d`; áp mẫu tự rải âm. Đã dựng thử video tổng hợp 6s (đo được âm đúng mốc). **Chưa dựng với footage của Hào.** Chưa có: chữ sau người, khoảng lặng trước chuyển cảnh, nhạc |
| Kho tài nguyên (`scripts/kho.py`, nút 📦 Kho) | Xong 13/11: quét thư mục kho trên PC (chỉ đọc tên file) → chỉ mục `video-studio/kho/` (không lên GitHub); app tìm/lọc/xem/nghe; timeline nhận `kho:<đường dẫn>` cho âm (`sfx`), **hàng `overlays` mới** (hoà sáng `screen` hoặc `alpha`, độ đậm) và LUT `.cube` làm màu đoạn. Thử trên cloud bằng kho giả (đường dẫn có dấu cách/hai chấm/dấu): dựng đúng, xem trước đúng. Kho chính trên Drive: "TÀI NGUYÊN EDIT VIDEO" (tài khoản haotruyenthong, ~30 GB: Chú Thích BĐS 15 .mov có alpha, Radar, Overlay, Background, SFX, nhạc). Overlay đặt nhỏ ở một chỗ (`x`, `y`, `size`, neo chân ghim `ax`, `ay` tự đo) + 📍 gắn chú thích theo lời nói; thử với file golf.mov thật: dựng đúng chỗ, đúng cỡ. Chưa thử trên PC; xuất Premiere chưa mang overlay. `docs/04-thu-vien/KHO-TAI-NGUYEN.md` |
| Thư viện lưu trữ (`docs/04-thu-vien/THU-VIEN-LUU-TRU.md`) | 13/11: thiết kế cây kho trên Drive (00_CHUNG / 10_THUONG-HIEU / 20_DU-AN / 90_CHO-PHAN-LOAI / 99_LUU-TRU), tên file, GIAY-PHEP.md; `kho.py` hiểu tầng + `--chon` lấy theo nghĩa (dự án → thương hiệu → chung), `/api/kho/chon`. Tự kiểm đạt. **Đã dời kho thật trên Drive 13/11**: "TÀI NGUYÊN EDIT VIDEO" → `KHO-EDIT` theo cây mới, 15 chú thích + 3 radar đổi tên, nhật ký hoàn tác `99_LUU-TRU/NHAT-KY-DOI*.md`, không xoá gì; logo Hào Sky Land: `10_THUONG-HIEU/hao-sky-land/logo/hao-sky-land_logo_01.png`; quyền chia sẻ đã về "Bị hạn chế". Chưa: giải nén zip, đặt tên 14 overlay số, nút Gợi ý trong app, quét kho thật trên PC |
| Xem trước giống bản xuất (`scripts/lop_chu.py`, `/api/lopchu`) | Xong 13/11: tách phần vẽ lớp chữ khỏi `dung.py` thành `lop_chu.py` (so sánh: HTML giống hệt mã cũ, chỉ thêm hàm tua `window.dat`); khung xem trong app chạy chính trang đó trong khung trong suốt, tua theo kim → thấy đúng kiểu chữ, chuyển động, phụ đề, thẻ của từng mẫu mà không cần dựng. Thử trên Chromium: khớp kim khi phát, đổi mẫu là đổi ngay; dựng thử 6s vẫn đạt |
| Thư viện mẫu edit (nút ✦, 6 mẫu) | Xong 13/11: thêm 5 mẫu tự thiết kế (`talking-head-01` vàng cao cấp, `neon-01`, `chu-dong-01` nhiều màu, `giai-thich-01` thẻ sáng, `sang-trong-01` nghỉ dưỡng) + 4 phong cách, khối `compare` (so sánh 2 cột), kiểu chữ `word-pop`, zoom nhấn ý do mẫu tự thêm (`mau: true`); trang thư viện dạng thẻ có xem trước chuyển động, đọc công thức `MAU.md`; công thức chung `docs/04-thu-vien/CONG-THUC-VIRAL.md`. Dựng thử cả 5 bằng video giả, đã xem khung hình. Chưa dựng với footage của Hào; chưa đo hiệu quả thật |
| Đặt chữ theo kịch bản (`scripts/kich_ban.py`, nút 📝 tab Chữ) | Xong 13/11: cột "Chữ trên màn hình" của `KICH-BAN.md` (`nhãn / *CHỮ LỚN* / dòng dưới`) → khối `title3d` đúng lúc nói, dò trong phụ đề (bỏ dấu, cho lệch 1 từ), không thấy thì theo cột Giây; dự án có mẫu edit thì rải lại âm (giữ chuyển cảnh). Tự kiểm + thử trong app với dự án mẫu. Chưa thử với giọng thật của Hào |
| Sắp xếp tài liệu + phân việc AI | Xong 12/11: docs theo thư mục đánh số, `AI-NAO-VIEC-NAO.md`, quy ước tên/thư mục, nhân bản 3 mức, bộ mẫu `mau/`. Thư mục footage trên PC mới là đề xuất, chưa tạo |
| Đạo diễn màu (`scripts/chinh_mau.py`, skill `chinh-mau`, `docs/04-thu-vien/CHINH-MAU.md`) | 13/11, tự xây (numpy + OpenCV + ffmpeg, không thêm thư viện): đo ám màu/sáng tối/cháy/da từng cảnh → cảnh chuẩn → phong cách có sẵn hoặc từ video mẫu → giữ da + trắng → mỗi cảnh một LUT `lut:mau/cNN.cube` (timeline, app, bộ dựng nhận) → báo cáo `MAU-SAC.md` + ảnh trước/sau; `--ap` chỉ chạy khi Hào duyệt. Tự kiểm đạt; thử trên Gladia (da giữ 38→38%) và 5 clip ngoài trời; dựng thật 18s đúng. Phát hiện: scrim của phong cách `hien-dai` làm tối 62% dưới khung suốt video (chờ Hào quyết). Chưa thử trên PC |
| Nghiệm thu video Gladia (`projects/zz-2026-11-13_tiktok_nghiem-thu`) | 13/11: dựng 74s (cắt lặng, chữ 3D, film burn, chuyển cảnh, âm). Hào: "tạm ổn". Cần sửa: màu da cam (do tự cân tăng rực), chữ nên nằm sau đầu, zoom giật. Mới làm khung demo + `GHI-NHO-NGHIEM-THU.md`; **chưa sửa code** 3 điểm này |
| Manim | Có mã, chưa chạy thử |
| Blender MCP | Mới có hướng dẫn, chưa thử |
| Codespaces (`.devcontainer`) | Chưa thử |
| Windows 11 (`setup-windows.ps1`, `chay-studio.bat`, `scripts/kiem_may.py`) | 13/11: cài một lệnh (winget + npm + pip + đặt PYTHONUTF8 + kiểm máy + dựng thử 6s); `chay-studio.bat` tự kiểm máy mỗi lần mở. Sửa lỗi chắc gặp trên Windows: `npx.cmd`, `python3`, chữ tiếng Việt (UTF-8). `kiem_may.py --dung-thu` đạt trên cloud (57s). **Chưa thử trên PC thật**; script PowerShell chưa chạy thử (máy cloud không có PowerShell) |
| Trang Pages cũ | Có thể đã bị app thay ở gốc; cần chạy lại "Deploy site" và kiểm tra |

## Máy và công cụ (Hào xác nhận 12/11/2026)
- PC Windows 11: Intel i5 "14800KF" (Hào ghi vậy, cần xem lại tên chip), card RTX 5050 (Hào ghi "GTX 5050"; trước đó nói 5060), RAM 64 GB. Máy làm việc nặng.
- MacBook M1 8 GB RAM, 256 GB: chỉ đọc báo cáo, xem kết quả, nghiệm thu. Không dựng 4K trên máy này.
- Anti = Google Antigravity, có chạy Claude Code bên trong (skill `.claude/skills/` dùng được).
- Repo nội bộ (riêng tư).

## Hệ thống làm việc (Hào chốt 12/11/2026)
`docs/01-he-thong/HE-THONG.md`: Anti xây phần mềm · GitHub giữ mã và bản v1 chạy tạm · **PC Windows 11 làm việc nặng** (tải footage, dựng) · Mac đọc báo cáo và nghiệm thu · điện thoại giao việc. Skill dự án: `.claude/skills/` (lap-storyboard, chinh-mau, dung-video, bao-cao-nghiem-thu); MCP: `docs/01-he-thong/MCP-VA-SKILL.md`.

## Kế hoạch đang theo
`docs/03-ke-hoach/KE-HOACH-APP.md`: định dạng timeline → thư viện hiệu ứng → app timeline (PWA PC + điện thoại) → máy chủ cục bộ Windows → âm thanh.

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
4. Thử Windows 11: trong PowerShell ở `video-studio` chạy `.\setup-windows.ps1` (tự kiểm máy + dựng thử), rồi bấm đúp `chay-studio.bat`. Lỗi thì gửi Claude màn hình của `python scripts\kiem_may.py`.
5. Thư viện mẫu: chờ Hào gửi mẫu tham khảo rồi làm (Hào dặn 12/11).
