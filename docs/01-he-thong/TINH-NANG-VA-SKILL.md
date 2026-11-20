# Toàn bộ hệ thống: mục tiêu, ghi nhớ, tính năng, skill

Đóng gói ngày 17/11/2026. Đây là bản đồ một trang của mọi thứ Hào đã cùng Claude xây. Chi tiết từng phần nằm ở file được trỏ tới; trạng thái mới nhất luôn ở bảng "Trạng thái" trong `CLAUDE.md`.

## 1. Mục tiêu

- Làm video ngắn cho thương hiệu Hào Sky Land: TikTok dọc 9:16 và YouTube ngang 16:9. Nội dung bất động sản, góc nhìn dòng tiền. Khách mục tiêu là nữ 35–55 tuổi ở trung tâm và khu Đông TP.HCM.
- Cách làm (Hào chốt 17/11): Hào **giao việc thẳng cho Claude Code** trên PC (qua Anti) hoặc trên cloud. Claude chạy lệnh, Hào duyệt video nháp rồi duyệt bản cuối.
  - App studio vẫn còn trong repo, chỉ xoá khi Hào test đạt trên PC và đồng ý xoá.
- Hướng phát triển: một hệ thống dựng có AI hỗ trợ. Mỗi lần sửa lỗi là sửa tận gốc trong bộ dựng (dùng lại cho mọi video), không vá riêng từng video.

## 2. Ghi nhớ bắt buộc (Claude đọc trước khi làm)

| Ghi nhớ | Ở đâu |
|---|---|
| Hồ sơ dự án, trạng thái, quy tắc | `CLAUDE.md` (Claude Code tự đọc mỗi phiên) |
| Lỗi Hào đã chỉ ra khi nghiệm thu: màu da, chữ sau đầu, zoom, chính tả… | `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` |
| Đối chiếu trước bản cuối: chữ/số trên màn hình phải khớp ghi âm hoặc nguồn đã duyệt | `scripts/doi_chieu.py` (bộ dựng tự dừng nếu chưa khớp) |
| Thông tin Hào nói hoặc gửi là đã xác thực ("Hào cung cấp, <ngày>"); từ nghe sai được sửa theo ngữ cảnh (`meta.sua_tu`) và báo lại | `CLAUDE.md`, mục Quy tắc làm việc |
| Chính tả: đơn vị viết thường đúng chuẩn (`1.080 ha`, `50 m²`) kể cả khi tiêu đề viết hoa; số kiểu Việt (`1.080`, `3,3`) | `ban_dung.hoa()`, `meta.sua_tu` |
| Chuyển động: mọi chữ ease in-out, chậm lại (`meta.cham_chu`) | `lop_chu.em_dan()` |
| Hai lần duyệt trước bản cuối (Hào chốt 17/11): storyboard → bản xem 540×960 → bản cuối | `scripts/storyboard.py`, `dung.py --xem` |
| Không sao chép tài nguyên người khác; học cấu trúc, tự dựng lại | `thu-vien-mau/README.md` |
| Mặc định không có thương hiệu "Hào Sky Land"; chỉ thêm `meta.thuong_hieu` khi Hào yêu cầu. Tên người nói theo đúng ghi âm, không tự đổi thành "Hào" (Hào chốt 18/11) | `CLAUDE.md`, `lop_chu.py` |
| Phải hỏi Hào trước: đăng công khai, gửi tin cho khách, xoá/ghi đè dữ liệu quan trọng, đổi trang công khai, phát sinh chi phí, gộp vào `main` | `CLAUDE.md` |
| Không đưa vào repo: thu nhập, ngày sinh, thông tin khách, khoá API, token | `CLAUDE.md` |

## 3. Quy trình chính

1. **Talking head (Hào nói trước máy):** skill `dung-talking-head`, 5 bước:
   - (0) tạo dự án từ thư mục footage;
   - (1) text từ giọng;
   - (2) AI chọn hook, tiêu đề, từ khoá, số liệu (`BAN-DUNG.json`);
   - (3) khung hình;
   - (4) chuyển động và âm;
   - (5) storyboard, Hào duyệt;
   - (6) bản xem 540×960, Hào duyệt;
   - (7) bản cuối.
2. **Video flycam/cắt ghép:** `QUY-TRINH-MOT-VIDEO.md` → `lap-storyboard` → `dung-video` → `bao-cao-nghiem-thu`.
3. **Thứ tự tự động khi dựng:** `docs/02-quy-trinh/THU-TU-TU-DONG.md`.

## 4. Tính năng (lệnh chạy trong `video-studio/`)

Trên PC thay `python3` bằng `.venv\Scripts\python.exe`.

| Nhóm | Tính năng | Lệnh / file | Đã thử |
|---|---|---|---|
| Dự án | Tạo dự án / thêm footage từ nhiều nguồn: kéo thả hoặc chọn video (cả điện thoại), link Google Drive (thư mục hoặc file), link tải trực tiếp, YouTube/TikTok; giỏ nguồn trong app (＋ và ＋ Footage) hoặc lệnh | `scripts/du_an_moi.py`, `scripts/tai_drive.py` | Cloud (tải lên, Drive, link trực tiếp); YouTube/TikTok chưa thử (mạng cloud chặn) |
| Dự án | Định dạng timeline v1 (cảnh, chữ, âm, cảnh chèn, zoom, B-roll, overlay) | `scripts/timeline.py`, test `test_timeline.py` | Cloud |
| Dựng | Cắt bỏ một đoạn (câu lặp, chỗ vấp, khoảng lặng) và tự dời mọi thứ phía sau | `scripts/cat_doan.py projects/<tên> <từ> <đến>` | Cloud (Saigon Park) |
| Duyệt | Phân tích lời nói và chỗ cắt: nói nhanh/chậm (so với nhịp riêng), lặp từ, nói vấp, cắt giữa từ, cảnh quá ngắn/dài + đề xuất; tự gắn vào storyboard | `scripts/phan_tich_loi.py projects/<tên>` | Cloud (Saigon Park: bắt câu lặp "biệt thự đơn lập, song lập") |
| Dựng | Bản nhẹ 540p (cạnh ngắn 540, màu đã chuyển, giữ tiếng) tạo một lần mỗi file; master cut, storyboard, bản xem, app đọc bản này; card NVIDIA tự dùng để giải nén 4K | `scripts/ban_nhe.py` (tự gọi) | Cloud (file 4K 17s: phân tích 44s → 6s, tạo bản nhẹ 38s một lần) |
| Duyệt | Storyboard từng cảnh (giây, ảnh, lời nói, chữ, chuyển cảnh) + ảnh lưới | `scripts/storyboard.py projects/<tên>` | Cloud (Saigon Park 24 cảnh, 46s) |
| Dựng | Dựng MP4: bản xem 540×960 `--xem` để Hào duyệt, nháp `--nhap`, bản cuối; nhớ bước đã làm | `scripts/dung.py projects/<tên>` | Cloud, Mac (dựng thử 6s) |
| Dựng | Tự cắt im lặng, nói vấp, chọn khúc đẹp, zoom xen kẽ | `scripts/master_cut.py`, `phan_tich_hinh.py` | Cloud |
| Giọng | Phụ đề/text từ giọng (Whisper tiếng Việt, mốc từng từ) | `scripts/phu_de.py` | Cloud |
| Chữ | Chữ theo nhịp nói, từ khoá phát sáng, ngang ngực người nói | `scripts/loi_nhip.py` | Cloud |
| Chữ | AI chọn vai chữ từ lời nói (hook/tiêu đề/số liệu/CTA) | `scripts/ban_dung.py chep|ap` | Cloud |
| Chữ | Chữ theo kịch bản (cột "Chữ trên màn hình") | `scripts/kich_ban.py` | Cloud |
| Chữ | Lớp chữ HTML/GSAP, cảnh chèn đồ hoạ (số liệu, quỹ đạo, checklist, kính) | `scripts/lop_chu.py` | Cloud |
| Chữ | 66 tag chữ trong 6 bộ | `scripts/tag_chu.py`, `docs/04-thu-vien/THU-VIEN-TAG.md` | Cloud |
| Chữ | Chữ nằm sau đầu người (tách người MODNet) | `scripts/tach_nguoi.py` | Cloud |
| Kiểm | Cổng đối chiếu chữ/số với ghi âm và nguồn | `scripts/doi_chieu.py` | Cloud |
| Màu | HDR (iPhone/DJI) → video thường, tự cân màu | `scripts/mau.py` | Cloud |
| Màu | Đạo diễn màu: mỗi cảnh một LUT, giữ da | `scripts/chinh_mau.py` | Cloud |
| Âm | Kho hiệu ứng âm (bộ `hsl_*` của Hào + âm tự tổng hợp + Mixkit) | `thu-vien-am-thanh/`, `scripts/am_thanh.py`, `tao_sfx.py`, `tai_sfx_mien_phi.py` | Cloud (chưa nghe bằng tai) |
| Âm | Nhạc nền tự nhỏ khi nói, làm sạch giọng, −14 LUFS | trong `dung.py` | Cloud |
| Hiệu ứng | 212 chuyển cảnh gl-transitions + chuyển cảnh 3D, 9 filter màu | `scripts/effects.py`, `gl_transitions.json`, `kiem_gl.mjs` | Cloud |
| Mẫu | Áp mẫu edit (8 mẫu) | `scripts/ap_mau.py`, `thu-vien-mau/` | Cloud |
| Mẫu | Học mẫu từ video tham khảo; lưu chỉnh sửa thành mẫu | `scripts/hoc_mau.py`, `luu_vao_mau.py` | Cloud |
| Kho | Kho tài nguyên trên PC/Drive (chỉ đọc tên file) | `scripts/kho.py`, `docs/04-thu-vien/KHO-TAI-NGUYEN.md` | Cloud (kho giả) |
| Xuất | Sang Premiere (`.xml`), DaVinci (`.otio`), phụ đề `.srt` | `scripts/xuat_nle.py` | Cloud (chưa mở trong Premiere/DaVinci) |
| Máy | Kiểm máy, dựng thử, tự kiểm mọi tính năng | `scripts/kiem_may.py --dung-thu --tu-kiem` | Cloud, Mac |
| App (tạm giữ) | App timeline trên trình duyệt | `studio/server.py`, `chay-studio.bat` | Mac (mở được) |
| Cũ | Mẫu đồ hoạ HyperFrames/Remotion, `assemble.mjs`, `render.sh` | `engines/`, `videos/` | Cloud |

## 5. Skill

**Skill của Claude Code** (`.claude/skills/`; Claude tự dùng khi Hào nói đúng việc):

| Skill | Dùng khi Hào nói |
|---|---|
| `dung-talking-head` | "dựng talking head", "video nói trước máy", "chữ theo lời nói" |
| `lap-storyboard` | "lên storyboard", "chọn cảnh", gửi thư mục footage + kịch bản |
| `dung-video` | "dựng", "render", "xuất video" |
| `chinh-mau` | "chỉnh màu", "da bị cam", "lấy màu video mẫu" |
| `hoc-mau` | gửi video mẫu: "học style này", "làm mẫu giống video này" |
| `bao-cao-nghiem-thu` | "kiểm tra", "nghiệm thu", "báo cáo" video |
| `talking-head-ui` | "talking head ui", "lớp chữ cho CapCut", "chữ nền trong suốt": dựng lớp chữ động (phụ đề từng cụm, khối chữ nhấn, chữ sau người) bằng HyperFrames từ `edit-plan.json`, độc lập với `dung.py` |

**Kho skill thiết kế** (`video-studio/thu-vien-skill/`, công thức dựng lại, không phải mã):
- am-thanh-theo-nhip
- canh-bong-nguoi-ai
- canh-chen-the-mang-xa-hoi
- chu-bam-nguoi
- chu-theo-nhip-noi
- chuyen-canh-chop-sang
- cta-cuoi-video
- the-ten-giai-ma
- tim-nguon-mien-phi
- tu-khoa-phat-sang

**Mẫu edit** (`video-studio/thu-vien-mau/`):
- edit-phim-01 (chuyên nghiệp)
- talking-head-01 (vàng cao cấp)
- talking-cam-01 (chữ cam theo nhịp nói)
- talking-luxury-01 (sang trọng châu Âu)
- neon-01
- chu-dong-01
- giai-thich-01
- sang-trong-01 (nghỉ dưỡng)

## 6. Repo tự chứa: cái gì nằm trong repo, cái gì tải khi chạy

- **Trong repo:**
  - toàn bộ mã, tài liệu, skill, mẫu, kho âm thanh;
  - 214 chuyển cảnh gl-transitions (chép sẵn kèm giấy phép MIT).
  - Không còn liên kết submodule (gỡ 17/11): 9 repo tham khảo khác chưa dùng tới. Khi cần thì cài bằng pip/npm (`docs/04-thu-vien/THU-VIEN-CHUYEN-NGHIEP.md`).
- **Cài một lần** (`setup-windows.ps1` / `setup-mac.sh`): Node, FFmpeg, Python 3.12 vào `.venv` cùng numpy, faster-whisper, OpenCV, OpenTimelineIO, onnxruntime, và gói npm.
- **Tự tải lần đầu chạy** (cần mạng):
  - mô hình Whisper (Hugging Face);
  - MODNet (`video-studio/models/`);
  - phông chữ Google Fonts khi dựng lớp chữ.
- **Không lên GitHub** (theo thiết kế):
  - footage và video dựng ra (`build/`, `out/`);
  - chỉ mục kho tài nguyên (`video-studio/kho/`);
  - `.venv`, `node_modules`.

## 7. Đưa về PC (Windows 11)

```powershell
git clone https://github.com/haoskyland-realestate/test.git C:\HSL
cd C:\HSL\video-studio
.\setup-windows.ps1                                   # cài một lần + kiểm máy + dựng thử 6s
.venv\Scripts\python.exe scripts\kiem_may.py --tu-kiem   # chạy mọi bài tự kiểm tính năng
```

Sau đó mở thư mục `C:\HSL` bằng Anti (Claude Code). Claude tự đọc `CLAUDE.md` và các skill, rồi Hào giao việc như trên cloud. Lấy bản mới: `git pull`.
