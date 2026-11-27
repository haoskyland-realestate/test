# Quy trình chuẩn dựng video (bộ não của hệ thống)

> Viết lại từ ghi âm 5 phút của Hào ngày 27/11/2026 (thư mục `vi` trên Drive). Đây là **nguồn chính** cho cách làm một video. Claude đọc file này trước khi dựng.
> Khi quy trình đổi, sửa ở đây trước, rồi mới sửa code.
> Cách chạy: một lệnh `agent.py` (skill `agent-video`). Agent tự làm phần máy, dừng ở cổng cần Hào, không đoán.

## Hào gửi gì

| Thứ | Ví dụ | Ghi chú |
|---|---|---|
| **Video thô** | thư mục clip iPhone/DJI, link Drive | Quay **không cần theo thứ tự**, một câu quay nhiều lần cũng được |
| **Kịch bản** | link Google Doc (chia sẻ "Bất kỳ ai có đường liên kết") | Mỗi đoạn/câu là một ý; máy dùng để xếp clip và đối chiếu lời nói |
| **Tài nguyên dự án** | link Drive thư mục ảnh/video Vinhomes Cần Giờ, Happy One Elite… | Dùng để trám cảnh; vào kho tầng `20_DU-AN/<dự án>/` |
| **Video mẫu âm thanh** (tuỳ chọn) | video có cách đặt nhạc/hiệu ứng âm hay | Học cách đặt âm (đợt 2) |

Lệnh:
```
python scripts/agent.py <ngày>_tiktok_<dự-án>_<chủ-đề> <thư mục/link video thô> --kich-ban <link Google Doc> --tai-nguyen <link Drive tài nguyên> --du-an <dự-án> [--ca-hai]
```

## 10 bước

| # | Bước (lời Hào) | Máy làm | Công cụ | Cổng | Trạng thái |
|---|---|---|---|---|---|
| 1 | Đọc video thô + kịch bản, tự phân tích, lập kế hoạch | Tải kịch bản Doc → `KICH-BAN.md`; nghe lời từng clip, **xếp clip theo kịch bản**, chọn lần quay ít vấp/ngắn nhất, clip không lời thành cảnh trám; master cut (cắt lặng, vấp) | `kich_ban_doc.py`, `xep_canh.py`, `master_cut.py` | **Cổng 1**: từ nghe chưa rõ, tên, số, câu thiếu clip, clip lạ (`CAN-HOI.md`, `XEP-CANH.md`) | Có (27/11) |
| 2 | Lấy ảnh/video trong link tài nguyên dự án để **trám cảnh** | Tải vào kho, Claude ghi mô tả từng ảnh một lần (`kho/MO-TA.json`), đặt ảnh/video đúng lúc người nói nhắc tới; ảnh tĩnh đẩy vào/kéo ra chậm | `tram_canh.py`, `kho.py`, `tai_drive.py` | Cổng 3 (`TRAM-CANH.md`) | Có (27/11) |
| 3 | Cảnh không có tư liệu → **agent tự tạo motion graphic**; kho **skill motion graphic 1, 2, 3…** lớn dần | Hiện ghi "CẦN HÌNH" trong `TRAM-CANH.md`; tạm dùng thẻ số liệu/danh sách/sơ đồ có sẵn | `cards`, `tag_chu.py`, `autoedit/` (7/22 hiệu ứng) | Cổng 2 (chọn hiệu ứng) | **Đợt 2** |
| 4 | Luồng thứ hai: **tìm ý tưởng trên web** (Pinterest, trang thiết kế, báo) bằng trình duyệt trên PC | **Chỉ tham khảo** bố cục/màu/kiểu chữ rồi tự vẽ lại, ghi nguồn; **không chèn ảnh của người khác** (Hào chốt 27/11, tránh bản quyền) | trình duyệt trên PC | — | **Đợt 2** |
| 5 | Cắt cảnh, chữ động, mẫu phụ đề, thư viện mẫu | Chữ theo nhịp nói, chữ lớn, thẻ, mẫu edit | `ban_dung.py`, `ap_mau.py`, `lop_chu.py`, `thu-vien-mau/` | Cổng 2, 3 | Có |
| 6 | **Kho âm thanh** vài nghìn file | Hiện dùng 58 âm trong repo + kho trên PC qua `kho.py` (chỉ mục tên, không chép); học cách đặt âm từ video mẫu | `kho.py`, `am_thanh.py`, `hoc_mau.py` | Cổng 3 | Một phần, **đợt 2** rải âm tự động từ kho lớn |
| 7 | **Kế hoạch dựng như editor 10 năm**: hook, nhấn, zoom in/out chữ và khung **mượt, không giật** | `STORYBOARD.md` có phần "Nhịp dựng" + cột Vai/Zoom/Âm cho từng cảnh; zoom êm (ease in-out, neo 38%) | `storyboard.py`, `master_cut.py`, `lop_chu.py` | **Cổng 3** (chốt phương án) | Có |
| 8 | **LUT màu** cho đồng chất | Đo từng cảnh, mỗi cảnh một LUT, giữ màu da/trắng; ảnh trước/sau; chốt cổng 3 thì áp | `chinh_mau.py` | Cổng 3 (`MAU-SAC.md`) | Có (tự động trong agent 27/11) |
| 9 | Xuất **TikTok và YouTube**, chữ nằm trong **vùng an toàn** của cả hai | Bản xem 540×960 có vạch vùng an toàn → bản cuối → kiểm vùng an toàn + kiểm bản dựng; `--ca-hai` dựng thêm bản 16:9 | `dung.py`, `kiem_vung.py`, `kiem_cuoi.py`, `agent.nhan_ban_youtube` | **Cổng 4** (duyệt bản xem) | Có (vùng YouTube 27/11) |
| 10 | **Kho ảnh bìa** cho từng video | 3 phương án TikTok + 3 YouTube: khung sạch lúc người nói, chữ hook đã duyệt; lưu `anh-bia/<dự án>/`, sổ `anh-bia/KHO-ANH-BIA.md` | `anh_bia.py` | Hào chọn trong `ANH-BIA.md` | Có (27/11) |

## Quy tắc giữ nguyên (từ CLAUDE.md)
- Không đoán: chữ/số trên màn hình phải là lời đã nói hoặc nguồn đã duyệt. Không rõ thì hỏi ở cổng.
- Người nói có thể không phải Hào: tên theo ghi âm.
- Mặc định không có thương hiệu Hào Sky Land, trừ khi Hào nói "edit cần thương hiệu của tôi".
- Hai lần duyệt trước bản cuối: storyboard (cổng 3), rồi bản xem 540×960 (cổng 4).

## Đợt 2 (chưa làm)
1. Kho skill motion graphic đánh số (`motion-graphic/01-…`), agent tự tạo cảnh cho câu "CẦN HÌNH".
2. Tham khảo web trên PC (chỉ ý tưởng, ghi nguồn).
3. Rải âm tự động từ kho âm lớn, học từ video mẫu âm thanh.
