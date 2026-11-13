# Mục lục

Cập nhật 12/11/2026. Mỗi khi thêm, dời hay lưu trữ một tài liệu, sửa luôn file này.

## Muốn làm gì thì mở file nào

| Muốn… | Mở |
|---|---|
| Biết việc này nên hỏi AI nào | `01-he-thong/AI-NAO-VIEC-NAO.md` |
| Có câu lệnh chép sẵn cho từng AI | `../mau/PROMPT-MAU.md` |
| Làm một video từ đầu đến cuối | `02-quy-trinh/QUY-TRINH-MOT-VIDEO.md` |
| Biết tuần này làm gì, ngày nào | `02-quy-trinh/NHIP-TUAN.md` |
| Đặt tên video, sắp thư mục footage trên PC | `01-he-thong/THU-MUC-VA-DAT-TEN.md` |
| Nhân bản: video mới, đổi khung, hay cả hệ thống cho ngành khác | `01-he-thong/NHAN-BAN-HE-THONG.md` |
| Biết máy nào làm việc gì (PC, Mac, điện thoại, GitHub, Anti) | `01-he-thong/HE-THONG.md` |
| Cài skill, kết nối Claude với Blender/Drive (MCP) | `01-he-thong/MCP-VA-SKILL.md` |
| Xem app studio có những nút gì | `05-app/GIAO-DIEN-TINH-NANG.md` |
| Chọn chuyển cảnh, filter màu, kiểu chữ | `04-thu-vien/THU-VIEN-HIEU-UNG.md` |
| Xem đặc tả thư viện mẫu (bố cục, khung, chữ, nhịp) | `04-thu-vien/THU-VIEN-MAU.md` |
| Chọn hiệu ứng âm (vút, bụp, ting…), thêm âm thật | `04-thu-vien/THU-VIEN-AM-THANH.md`, `../video-studio/thu-vien-am-thanh/README.md` |
| Dùng mẫu edit có sẵn (6 mẫu: review dự án, chuyên gia vàng, neon, chữ nhiều màu, giải thích, sang trọng), thêm mẫu mới | `../video-studio/thu-vien-mau/README.md` |
| Công thức video giữ người xem: hook, nhịp, khung 60 giây, chọn mẫu theo nội dung | `04-thu-vien/CONG-THUC-VIRAL.md` |
| Dùng kho tài nguyên 30 GB trên Drive (overlay, âm, LUT…) trong app, cách xếp thư mục | `04-thu-vien/KHO-TAI-NGUYEN.md` |
| Biết tài nguyên nằm đâu trên Drive, đặt tên, máy tự chọn tài nguyên theo nghĩa | `04-thu-vien/THU-VIEN-LUU-TRU.md` |
| Giọng nói AI (Voice Studio): so sánh CIT Voice Studio và VoiceStudio, giấy phép, cách tích hợp | `04-thu-vien/GIONG-NOI-AI.md` |
| Xem 10 repo chuyên nghiệp và cái nào đã dùng | `04-thu-vien/THU-VIEN-CHUYEN-NGHIEP.md` |
| Xem kế hoạch, đang ở bước nào | `03-ke-hoach/KE-HOACH-APP.md`, bảng Trạng thái trong `../CLAUDE.md` |
| Hiểu cách làm cũ (không làm theo) | `99-luu-tru/README.md` |

## Cây thư mục

```
docs/
  00-MUC-LUC.md                    ← file này
  01-he-thong/
    AI-NAO-VIEC-NAO.md             phân việc cho từng AI ★
    THU-MUC-VA-DAT-TEN.md          quy ước thư mục, đặt tên (repo, PC, Drive) ★
    NHAN-BAN-HE-THONG.md           nhân bản 3 mức ★
    HE-THONG.md                    vai trò từng máy
    MCP-VA-SKILL.md                skill và MCP
  02-quy-trinh/
    QUY-TRINH-MOT-VIDEO.md         từng bước, ai làm, ra gì ★
    NHIP-TUAN.md                   lịch tuần
  03-ke-hoach/
    KE-HOACH-APP.md                kế hoạch app (đang theo)
    KE-HOACH.md                    kế hoạch tổng ban đầu (một phần đã cũ, xem mục 0 trong file)
  04-thu-vien/
    THU-VIEN-HIEU-UNG.md           tự sinh từ effects.py (222 chuyển cảnh, 9 filter…)
    THU-VIEN-MAU.md                đặc tả mẫu
    CONG-THUC-VIRAL.md             hook, nhịp, khung video, chọn mẫu ★
    THU-VIEN-LUU-TRU.md            cây thư mục kho trên Drive, tầng, lấy theo nghĩa ★
    KHO-TAI-NGUYEN.md              kho tài nguyên edit trên Drive: chuẩn bị, app dùng được gì ★
    GIONG-NOI-AI.md                tìm hiểu Voice Studio (giọng AI tiếng Việt) ★
    THU-VIEN-AM-THANH.md           21 hiệu ứng âm, tự sinh từ hieu-ung.json ★
    THU-VIEN-CHUYEN-NGHIEP.md      10 repo GitHub
  05-app/
    GIAO-DIEN-TINH-NANG.md         tính năng app studio
    anh-giao-dien/                 ảnh mẫu Hào gửi
  99-luu-tru/                      cách làm cũ
mau/
  du-an-video/                     BRIEF, NGUON-SO-LIEU, KICH-BAN, STORYBOARD, DANG-BAI, KET-QUA
  PROMPT-MAU.md                    câu lệnh mẫu 11 bước
```
★ = mới trong lần sắp xếp 12/11/2026.

## Cách tìm nhanh
- **Trong Anti / VS Code:** `Ctrl+P` gõ một phần tên file (`kich-ban`, `ai-nao`); `Ctrl+Shift+F` tìm chữ trong mọi file.
- **Trên GitHub (điện thoại):** mở repo, bấm phím `t` (máy tính) hoặc ô tìm kiếm, gõ tên file.
- **Hỏi Claude:** "mở file hướng dẫn về <việc>": Claude đọc mục lục này trước.
- Tên đều không dấu, chữ thường/HOA cố định, nên gõ không dấu là ra.
