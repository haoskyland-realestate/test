# Thư viện lưu trữ tài nguyên edit (thiết kế)

Lập 13/11/2026. Hào chốt: **Drive là kho chính, PC tải khi cần** · **sắp xếp thẳng trên Drive** · **máy tự chọn, Hào duyệt** · sau này có tài nguyên riêng từng dự án, bộ thương hiệu Hào Sky Land, kho nhạc/âm lớn, dùng cho thương hiệu và ngành khác.

## 1. Nguyên tắc: đường dẫn chính là dữ liệu

Hệ thống không cần một bảng dữ liệu riêng phải nhập tay. **Vị trí và tên file đã nói hết**: file thuộc ai (tầng), là gì (loại), dùng vào việc gì (nhóm), đặc điểm gì (tên). Thả file đúng chỗ, đặt tên đúng kiểu, bấm **Quét lại** là máy hiểu.

Lý do chọn cách này (kinh nghiệm thực tế): bảng dữ liệu nhập tay luôn lệch với file thật sau vài tuần. Thư mục thì không lệch được.

## 2. Cây thư mục trên Drive

```
KHO-EDIT/                                  ← chọn thư mục này làm "thư mục kho" trong app
  00_CHUNG/                                dùng cho mọi thương hiệu, mọi ngành
    am-thanh/<nhóm>/                       whoosh, click, impact, riser, ting, may-anh, go-phim, highlight, sang-trong, ve-duong-vien
    nhac/<tâm trạng>/                      sang-trong, nhe-nhang, nhanh, cam-xuc  (+ GIAY-PHEP.md bắt buộc)
    overlay/<nhóm>/                        film-burn, light-leak, bokeh, bui, giay, khoi
    chu-thich/<ngành>/                     bds/  (ghim tiện ích: truong-hoc, benh-vien, sieu-thi…)
    radar/
    nen/<nhóm>/                            luoi, giay, vai, dia-hinh, chuyen-dong
    chuyen-canh/                           chuyển cảnh dạng video
    lut/                                   .cube
    khung/                                 vùng an toàn, khung điện thoại
    font/                                  .ttf/.otf đã giải nén
    tham-khao/                             template AE/Premiere, plugin (app không chạy được, chỉ để xem)
  10_THUONG-HIEU/
    hao-sky-land/                          logo/, mau/ (bảng màu), font/, intro-outro/, am-thanh/ (âm nhận diện), lut/
    <thương hiệu khác>/                    cùng cấu trúc: thêm thương hiệu = chép thư mục này
  20_DU-AN/
    hoc-mon/                               logo-cdt/, phoi-canh/, mat-bang/, tien-ich/, tai-lieu/
    can-gio/
  90_CHO-PHAN-LOAI/                        file mới tải về thả vào đây; Claude đề xuất chỗ, Hào duyệt rồi dời
  99_LUU-TRU/                              file nén gốc đã giải nén, file trùng, đồ không còn dùng (không xoá)
```

**Thứ tự máy lấy:** dự án đang làm → thương hiệu đang làm → chung. Ví dụ video Hóc Môn của Hào Sky Land cần "whoosh": nếu `10_THUONG-HIEU/hao-sky-land/am-thanh/` có whoosh riêng thì lấy cái đó, không có mới lấy trong `00_CHUNG`. Tài nguyên của thương hiệu khác, dự án khác **không bao giờ** bị lấy nhầm. `90_` và `99_` không bao giờ được chọn.

**Thêm ngành khác** (ví dụ ô tô, F&B): thêm `00_CHUNG/chu-thich/oto/`, thêm `10_THUONG-HIEU/<tên>/`. Không phải sửa mã.

## 3. Đặt tên file

```
<nhóm>_<mô tả>_<số>.<đuôi>
whoosh_nhanh_01.wav       film-burn_cam_02.mp4       truong-hoc_ghim-cam_01.mov
```
- Theo 5 quy tắc chung (`docs/01-he-thong/THU-MUC-VA-DAT-TEN.md`): không dấu, chữ thường, `-` nối chữ, `_` ngăn phần.
- Phần mô tả là **từ để máy tìm**: ghi đặc điểm người dùng sẽ gõ (nhanh/chậm, màu, cảm giác). Bỏ chữ thừa: "Bản sao của", "Copy of", "final".
- Tên nhạc thêm nhịp nếu biết: `nhac_sang-trong_piano_90bpm_01.mp3`.

## 4. Giấy phép (bắt buộc với nhạc, nên có với mọi thư mục)

Mỗi thư mục nguồn có một file `GIAY-PHEP.md` ngắn: lấy từ đâu, ngày tải, điều khoản (dùng thương mại được không, có phải ghi nguồn không). Máy tự tìm file này ở thư mục chứa hoặc thư mục cha gần nhất. Khi gợi ý một file chưa có giấy phép, máy ghi rõ **"chưa có GIAY-PHEP.md"** để Hào cân nhắc trước khi dùng cho video kinh doanh.

## 5. Máy tự chọn, Hào duyệt

- **Lệnh:** `python3 scripts/kho.py --chon "film burn" hao-sky-land hoc-mon` → 5 file hợp nhất, mỗi file kèm lý do (khớp từ nào, tầng nào, có giấy phép chưa).
- **App:** địa chỉ `/api/kho/chon?y=<ý muốn>&th=<thương hiệu>&da=<dự án>`; nút trong app chưa làm (xem mục 8).
- **Claude Code trên PC:** câu lệnh kiểu "dùng kho, chọn overlay film burn cho các chuyển cảnh FilmBurn của video `<tên>`": Claude chạy lệnh trên, đưa danh sách để Hào chọn, rồi mới ghi vào `timeline.json`.
- Máy **không tự chèn** vào video. Timeline luôn ghi đường dẫn cụ thể `kho:00_CHUNG/overlay/film-burn/film-burn_cam_01.mp4`, nên video dựng lại sau một năm vẫn ra giống hệt, dù kho có thêm file mới.

## 6. Drive chính, PC tải khi cần

Dùng sẵn **Google Drive cho máy tính** (Google Drive for desktop), không viết thêm phần mềm tải:
- Cài trên PC, chọn chế độ **Phát trực tuyến** (Stream files): thư mục kho hiện như một ổ đĩa (ví dụ `G:\My Drive\KHO-EDIT`) nhưng **không chiếm chỗ**; file chỉ tải về khi app mở hoặc dựng.
- Thư mục hay dùng (`00_CHUNG/am-thanh`, `10_THUONG-HIEU/hao-sky-land`, dự án đang làm): bấm phải → **Sẵn có ngoại tuyến** (Available offline) để luôn có sẵn, không phải chờ.
- File chú thích/radar rất nặng (0,2–2 GB mỗi file): để trực tuyến, chỉ tải khi dùng tới.
- Trong app chọn thư mục kho là `G:\My Drive\KHO-EDIT` rồi Quét. Quét chỉ đọc tên file nên không làm Drive tải 30 GB về.

## 7. Dời kho hiện có sang cây mới (chưa làm, cần Hào cho phép)

Kho "TÀI NGUYÊN EDIT VIDEO" thuộc tài khoản **haotruyenthong**. Tài khoản đang nối với Claude (haoskyland) chỉ có **quyền xem**, nên Claude chưa dời được. Hai cách:
1. **(Khuyên dùng)** Từ haotruyenthong, chia sẻ thư mục "TÀI NGUYÊN EDIT VIDEO" cho haoskyland quyền **Người chỉnh sửa** (Editor). Claude dời từng thư mục theo bảng dưới, ghi nhật ký để hoàn tác.
2. Hào tự kéo thả trên drive.google.com theo bảng dưới (khoảng 15 phút).

Dời trên Drive **không tốn thêm dung lượng, không đổi mã file**, và hoàn tác được (dời ngược lại). Đổi tên thư mục gốc thành `KHO-EDIT`.

| Đang ở | Dời tới |
|---|---|
| ĐÌNH VĂN MEDIA / Tài Nguyên / Chú Thích BĐS | `00_CHUNG/chu-thich/bds/` (bỏ "Bản sao của" trong tên 15 file) |
| ĐÌNH VĂN MEDIA / Tài Nguyên / Bộ Radar BĐS | `00_CHUNG/radar/` |
| ĐÌNH VĂN MEDIA / PLUGIN | `00_CHUNG/tham-khao/plugin/` |
| ĐÌNH VĂN MEDIA / Font Chữ (file .zip) | giải nén vào `00_CHUNG/font/`, file .zip vào `99_LUU-TRU/` |
| OVERLAY | `00_CHUNG/overlay/` (chia `film-burn/`, `light-leak/` theo tên file; file tên số `1.mp4`…`14.mp4` vào `90_CHO-PHAN-LOAI/` chờ xem và đặt tên) |
| BACKGROUD | `00_CHUNG/nen/` |
| SOUND EFFECT / SFF 1, SFF 2: whoosh, MAY ANH, GO BAN PHIM, TIẾNG HIGHLIGHTER, AM THANH LUXURY, AM THANH VE DUONG VIEN | `00_CHUNG/am-thanh/whoosh/`, `may-anh/`, `go-phim/`, `highlight/`, `sang-trong/`, `ve-duong-vien/` |
| SOUND EFFECT / Sound Effect - ThuaanNguyeen.zip | giải nén vào `90_CHO-PHAN-LOAI/`, file .zip vào `99_LUU-TRU/` |
| LIST NHẠC KHÔNG BẢN QUYỀN YOUTUBE | `00_CHUNG/nhac/` + tạo `GIAY-PHEP.md` (tên kiểu Pixabay: kiểm điều khoản) |
| Animated Icons Pack (After Effects) | `00_CHUNG/tham-khao/after-effects/` |
| VÙNG AN TOÀN TIK TOK | `00_CHUNG/khung/` |
| LOGO THƯƠNG HIỆU (INDOCHINE, HAPPY ONE MORI, SETIA, HSL, RISA) | `99_LUU-TRU/logo-chu-dau-tu-khac/` (không thuộc giỏ hàng hiện tại; chỉ dùng khi được phép) |
| 4 thư mục trống của Hào (01_TYPOGRAPHY…04_SOUND_EFFECTS_SFX) và "HAO SKY LAND – THƯ VIỆN EDIT VIDEO" | dời vào `99_LUU-TRU/` (không xoá); tạo mới `10_THUONG-HIEU/hao-sky-land/` |
| Gói người khác chia sẻ dạng .rar (Overlays, PAPER TRANSITION, Tài nguyên tóp tóp) | tải bản sao về, giải nén vào `90_CHO-PHAN-LOAI/` (lưu ý: chép vào Drive của Hào sẽ tính dung lượng) |

**Nhật ký hoàn tác:** mỗi lần dời, Claude ghi một dòng `mã file · tên · thư mục cũ · thư mục mới · giờ` vào `KHO-EDIT/99_LUU-TRU/NHAT-KY-DOI.md`. Muốn hoàn tác: nhờ Claude "dời ngược theo nhật ký".

**Việc của dự án trong repo:** timeline cũ có ghi `kho:` theo đường dẫn cũ sẽ báo thiếu file sau khi dời. Hiện chưa dự án thật nào dùng kho nên không ảnh hưởng.

## 8. Đã làm và chưa làm

| Phần | Trạng thái |
|---|---|
| Máy hiểu tầng (chung / thương hiệu / dự án / chờ / lưu trữ) khi quét | Xong 13/11, có tự kiểm (`python3 scripts/kho.py --tu-kiem`) |
| Lấy theo nghĩa, ưu tiên dự án → thương hiệu → chung, báo giấy phép | Xong 13/11: lệnh `--chon` và địa chỉ `/api/kho/chon`, thử với kho giả |
| Nút "Gợi ý" trong app (gõ ý muốn → chọn trong danh sách) | Chưa làm |
| Mẫu edit tự xin tài nguyên kho theo nghĩa (vd. `edit-phim-01` xin "film burn" cho chuyển cảnh FilmBurn) | Chưa làm: cần đo điểm nhấn của file âm/overlay thật trước |
| Dời kho thật trên Drive | **Chưa làm: chờ quyền chỉnh sửa và lời đồng ý của Hào** |
| Thử trên PC với Drive for desktop | Chưa thử |
