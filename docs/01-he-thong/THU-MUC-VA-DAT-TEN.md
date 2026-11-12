# Thư mục và cách đặt tên

Lập 12/11/2026. Mục tiêu: tìm bất kỳ file nào trong 10 giây, nhân bản một dự án bằng cách chép một thư mục.

## 1. Năm quy tắc đặt tên (dùng cho mọi nơi: repo, PC, Drive)

1. **Không dấu, không dấu cách, chữ thường, nối bằng gạch ngang:** `hoc-mon`, `dong-tien-cho-thue`. Lý do: Windows, Mac, GitHub, dòng lệnh đều đọc đúng, tìm kiếm không lệch vì dấu.
2. **Ngày đứng đầu, dạng năm-tháng-ngày:** `2026-11-20`. Sắp theo tên là sắp theo thời gian.
3. **Gạch dưới `_` ngăn các phần, gạch ngang `-` nối chữ trong một phần:** `2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue`.
4. **Thư mục cấp trên đánh số** `01-`, `02-`… để thứ tự cố định; `99-luu-tru` cho đồ cũ (không xoá, chỉ dời vào).
5. **Tài liệu Markdown viết HOA:** `KICH-BAN.md`, `NGUON-SO-LIEU.md`. Nhìn là biết file để đọc; mã và dữ liệu viết thường.

### Tên một video (cũng là tên thư mục dự án)
```
<ngày>_<nền tảng>_<dự án BĐS>_<chủ đề>
2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue
2026-11-22_youtube_can-gio_so-sanh-vay-15-nam
```
| Phần | Giá trị dùng | Ghi chú |
|---|---|---|
| ngày | ngày bắt đầu làm | không đổi khi đăng trễ |
| nền tảng | `tiktok`, `youtube` | bản nhân bản sang khung kia đổi đúng phần này |
| dự án BĐS | `hoc-mon`, `can-gio`, `chung` (không riêng dự án nào) | thêm dự án mới thì thêm vào bảng này |
| chủ đề | 2–5 chữ | đủ để nhớ nội dung |

**Tìm kiếm:** gõ `hoc-mon` ra mọi video Hóc Môn; `2026-11` ra mọi video tháng 11; `youtube` ra mọi bản YouTube. Trong app studio, ô chọn dự án sắp theo tên nên tự sắp theo ngày.

Dự án thử nghiệm đặt tên bắt đầu bằng `zz-` (Git bỏ qua, xoá thoải mái).

## 2. Repo (GitHub): mã và tài liệu, không có footage

```
CLAUDE.md                     hồ sơ dự án, Claude tự đọc mỗi phiên
README.md                     cửa vào: chỉ tới docs/00-MUC-LUC.md
docs/
  00-MUC-LUC.md               mục lục + "muốn làm X thì mở file nào"
  01-he-thong/                máy nào làm gì, AI nào làm gì, thư mục, nhân bản, MCP/skill
  02-quy-trinh/               làm một video từng bước, nhịp tuần
  03-ke-hoach/                kế hoạch, trạng thái
  04-thu-vien/                danh mục hiệu ứng, đặc tả mẫu, repo chuyên nghiệp
  05-app/                     tính năng app studio, ảnh giao diện
  99-luu-tru/                 tài liệu của cách làm cũ (đọc để hiểu lịch sử, không làm theo)
mau/                          mẫu để chép khi bắt đầu việc mới
  du-an-video/                các file .md cho một video (app tự chép vào dự án mới)
  PROMPT-MAU.md               câu lệnh mẫu cho từng AI
.claude/skills/               skill: lap-storyboard, dung-video, bao-cao-nghiem-thu
video-studio/                 phần mềm
  studio/                     app timeline (server.py + index.html)  ← dùng hằng ngày
  scripts/                    bộ dựng, phụ đề, master cut, màu, xuất Premiere/DaVinci, test
  projects/<tên video>/       một thư mục cho mỗi video (xem mục 3)
  thu-vien-chuyen-nghiep/     10 repo GitHub tham khảo (submodule)
  engines/, app/, videos/     hệ cũ (mẫu đồ hoạ HyperFrames, form GitHub): còn chạy, ít dùng
  out/                        video dựng ra (không lên GitHub)
```

## 3. Một thư mục video

```
video-studio/projects/2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue/
  BRIEF.md            mục tiêu, nhóm khách, góc dòng tiền, lời kêu gọi
  NGUON-SO-LIEU.md    bảng số liệu: con số · nguồn · ngày · đã xác nhận chưa
  KICH-BAN.md         hook, lời đọc, chữ trên màn hình
  STORYBOARD.md       cảnh · giây · chữ · chuyển cảnh
  timeline.json       file dựng (app studio sửa)
  DANG-BAI.md         tiêu đề, mô tả, hashtag, ảnh bìa
  KET-QUA.md          lượt xem, tin nhắn đúng khách, bài học
  history/            30 bản timeline cũ (app tự lưu, không lên GitHub)
  build/              bản xem trước, cảnh đã cắt, footage liên kết (không lên GitHub)
```
Các file `.md` lên GitHub được (nhẹ), nhưng **không ghi tên, số điện thoại của khách** vào đây.

## 4. PC Windows: kho footage và thành phẩm (đề xuất, **chưa tạo**)

Đặt trên ổ dữ liệu (ví dụ `D:`), cùng ổ với repo để app liên kết footage không tốn thêm chỗ:
```
D:\HaoSkyLand\
  repo\                          bản tải về của repo GitHub này
  01-footage\
    hoc-mon\
      2026-11-15_nha-mau\        mỗi buổi quay một thư mục: ngày_nơi-quay
        DJI_20261115_101804.mp4  giữ tên gốc của máy quay (đổi tên làm mất dấu vết)
    can-gio\
    chung\                       cảnh dùng chung: thành phố, đường, trời
  02-am-thanh\
    nhac\                        nhạc có quyền dùng; mỗi file kèm ghi chú nguồn/giấy phép
    hieu-ung\                    vút, chạm, chuyển
    giong-thu\
  03-thuong-hieu\                logo, bảng màu, font (khi Hào gửi)
  04-thanh-pham\
    2026-11\
      2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue.mp4
      2026-11-20_tiktok_hoc-mon_dong-tien-cho-thue-baocao.md
  05-mau-tham-khao\              video mẫu Hào thích, để làm thư viện mẫu
```
Bấm ＋ trong app → chọn `01-footage\hoc-mon\2026-11-15_nha-mau` → đặt tên theo mục 1.

## 5. Google Drive: chỉ để chuyền và xem

```
Drive/HaoSkyLand/
  footage-chuyen/      đưa footage từ điện thoại lên để PC tải (xong thì xoá bớt, Drive miễn phí chỉ 15 GB)
  thanh-pham/          bản chép của 04-thanh-pham để xem trên Mac/điện thoại
```
Kho chính nằm trên PC; Drive không thay được ổ cứng.

## 6. Khi thêm thứ mới
- Tài liệu mới: chọn đúng thư mục số trong `docs/`, thêm một dòng vào `docs/00-MUC-LUC.md`.
- Tài liệu hết dùng: dời vào `docs/99-luu-tru/`, ghi một dòng lý do trong `99-luu-tru/README.md`.
- Dự án BĐS mới (ngoài Hóc Môn, Cần Giờ): thêm vào bảng "dự án BĐS" ở mục 1.
