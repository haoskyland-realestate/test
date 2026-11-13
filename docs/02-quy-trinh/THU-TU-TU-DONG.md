# Thứ tự làm tự động của Claude (editor AI)

Lập 13/11/2026. Mục tiêu: **ra cùng một kết quả nhưng nhanh nhất, ít lần Hào phải chờ và duyệt nhất**.
File này là bản "máy chạy" của `QUY-TRINH-MOT-VIDEO.md` (bước 6b → 10): Claude làm theo đúng thứ tự dưới đây.

## 1. Ba nguyên tắc sắp thứ tự
1. **Việc không phụ thuộc nhau thì chạy song song.** Ví dụ: nhận dạng giọng (chỉ cần âm thanh) chạy cùng lúc với soi khung hình và đo màu (chỉ cần hình).
2. **Sửa ở gốc, sửa sớm.** Sai ở bước đầu thì mọi bước sau làm lại.
   - Tên riêng sai: sửa trong từ vựng hoặc bảng sửa từ **trước** khi cắt. Không sửa phụ đề sau cắt, vì cắt lại thì phụ đề tự sinh lại và mất phần đã sửa.
   - Cắt và màu chốt **trước** lần dựng đầu, vì đổi hai thứ này là phải cắt lại cảnh, phần chậm nhất.
3. **Việc đắt làm một lần, việc rẻ lặp nhiều lần.**
   - Dựng video là việc đắt nhất. Trước khi dựng, chữ, chuyển cảnh, zoom được kiểm bằng ảnh tĩnh và khung xem trước (vài giây).
   - Bộ dựng nhớ phần đã làm: lần sau chỉ làm lại phần thật sự đổi (mục 4).

## 2. Thứ tự (video nói trước máy hoặc đi xem nhà, có footage)

```
                ┌─ A1. Nhận dạng giọng (có từ vựng dự án) ──┐
footage ─ 0 ────┤                                          ├─ 2. Master cut ─ 3. Đo màu + LUT ─ [DUYỆT 1] ─┐
                └─ A2. Soi footage: khung lưới, HDR, dọc/ngang ┘                                              │
                                                                                                              ▼
   4. Chữ lớn theo kịch bản ─ 5. Chú thích, overlay theo lời ─ 6. Áp mẫu edit (chuyển cảnh, âm, zoom) ─ 7. Kiểm khung tĩnh
                                                                                                              │
                                                    10. Báo cáo ─ 9. Dựng bản cuối ─ [DUYỆT 2] ─ 8. Dựng nháp ┘
```

| # | Việc | Lệnh / công cụ | Cần gì xong trước | Đo được (cloud, video 77 giây) |
|---|---|---|---|---|
| 0 | Đặt footage vào `projects/<tên>/build/raw/`, ghi **từ vựng dự án** vào `meta.tu_vung` (tên dự án, chủ đầu tư, tiện ích, số hay nói: lấy từ BRIEF, KICH-BAN) | app ＋ hoặc Claude | – | – |
| A1 | Nhận dạng giọng | `phu_de.py` (master cut gọi sẵn) | 0 | 78 giây (PC có card NVIDIA nhanh hơn nhiều) |
| A2 | Soi footage: khung lưới, HDR hay không, quay dọc hay ngang, có mặt người không | `contact-sheet.sh`, Claude nhìn ảnh | 0, **chạy cùng lúc A1** | vài giây |
| 1 | **Claude đọc lại lời nhận dạng**: tên riêng, số, từ chuyên ngành. Sai thì thêm vào `meta.sua_tu` (ví dụ `{"chủ tư": "chủ đầu tư"}`). Câu máy tự bịa ("Hãy subscribe", "Cảm ơn." ở cuối) tự bị lọc | Claude | A1 | 1 phút |
| 2 | Master cut: cắt lặng, bỏ nói lặp, nhịp | `master_cut.py` | 1 | khoảng 1–2 phút |
| 3 | Đo màu từng cảnh, cảnh chuẩn, phong cách, LUT | `chinh_mau.py` (skill `chinh-mau`) | 2 (vì cần mốc cắt cuối) | 28 giây |
| **DUYỆT 1** | Gửi Hào **một lần**: báo cáo cắt (`build/master-cut.md`) + ảnh màu trước/sau (`mau/truoc-sau.jpg`) + chỗ phụ đề đã sửa | Hào | 2, 3 | Hào xem 2 phút |
| 4 | Chữ lớn theo kịch bản | `kich_ban.py` / nút 📝 | DUYỆT 1 (chữ bám lời đã cắt) | vài giây |
| 5 | Chú thích theo lời nói, overlay kho | `kho.py` / nút 📍 | 4 | vài giây |
| 6 | Áp mẫu edit: chuyển cảnh, hiệu ứng âm, zoom nhấn ý | `ap_mau.py` | 4, 5 (âm rải theo chữ). Chuyển cảnh mạnh đặt đúng **chỗ đổi phòng hoặc đổi ý** | vài giây |
| 7 | Kiểm khung tĩnh **không cần dựng**: chữ tràn khung, chữ che mặt, chữ đè phụ đề, nhịp | khung xem app (`lop_chu.py`) hoặc chụp vài mốc | 6 | 1 phút |
| 8 | Dựng nháp (chỉ khi cần xem chuyển động) | `dung.py --nhap` | 7 | nhanh hơn bản cuối |
| **DUYỆT 2** | Hào xem nháp hoặc khung demo | Hào | 8 | |
| 9 | Dựng bản cuối | `dung.py` | DUYỆT 2 | lần đầu 74 giây video: khoảng 13 phút |
| 10 | Nghiệm thu: đo âm lượng, màu da, khung hình, báo cáo | skill `bao-cao-nghiem-thu` | 9 | 2 phút |

**Không được đảo:** 1 trước 2 (cắt dùng lời đã sửa); 2 trước 3 (màu đo trên mốc cắt cuối); 4, 5 trước 6 (âm và zoom bám theo chữ); duyệt trước khi ghi LUT (`chinh_mau --ap`) và trước khi dựng bản cuối.
**Được đảo hoặc chạy song song:** A1 với A2; 4 với 3 nếu Hào đã chốt cắt; tải footage từ Drive trong lúc viết kịch bản.

## 3. Hai lần duyệt, không hơn
Hào chỉ bị hỏi **2 lần** cho một video: (1) cắt + màu + phụ đề, gộp một tin; (2) bản nháp hoặc khung demo. Mọi lỗi Claude tự thấy được (chữ tràn, da cam, câu bịa, cảnh lệch màu) thì Claude tự sửa trước khi hỏi.

## 4. Bộ dựng nhớ gì: đổi gì thì làm lại gì
Bộ dựng in thời gian từng bước (`⏱ ...`). Đo trên video 18 giây (13/11):

| Đổi | Làm lại | Thời gian |
|---|---|---|
| Lần đầu | tất cả | 3 phút 40 giây |
| Không đổi gì | chỉ ghép cuối | khoảng 30 giây |
| Chỉ chữ, phụ đề, thẻ | lớp chữ + ghép cuối | 1 phút 38 giây |
| Chỉ âm thanh, zoom, overlay | ghép cuối | khoảng 30 giây |
| Màu hoặc mốc cắt của **một** cảnh | đúng cảnh đó + ghép nền + ghép cuối | tuỳ độ dài cảnh |
| Chuyển cảnh | đoạn chuyển cảnh đó + ghép nền + ghép cuối | |

Vì vậy: **chốt cắt và màu trước** lần dựng đầu, sau đó chỉ chỉnh chữ và âm. Đừng đổi màu sau khi đã dựng nếu không cần.

## 5. Nhiều video cùng lúc
- Nhận dạng giọng của mọi video chạy trước, một lượt (máy rảnh, ban đêm). Đây là bước dài nhất trước khi duyệt.
- Mỗi video vẫn đi đúng thứ tự trên. Dựng bản cuối xếp hàng từng cái một, vì chạy song song làm máy chậm đều.

## 6. Đã làm trong code để thứ tự này có hiệu quả (13/11/2026)
- `dung.py`: in thời gian từng bước. Nhớ cảnh theo đúng bộ lọc (đổi công thức màu hay LUT là tự cắt lại; trước đây có thể dùng nhầm cảnh cũ). Nhớ nền đã ghép và lớp chữ đã dựng.
- `phu_de.py`: `meta.tu_vung` (từ vựng dự án cho nhận dạng), `meta.sua_tu` (bảng sửa từ, áp cho cả phụ đề và master cut, sửa bảng không phải nhận dạng lại), lọc câu bịa. Thử với video Gladia: hết "sông vườn", "chủ tư", "bàn giao kẻ", "Hãy subscribe".
- **Chưa đo** trên PC Windows. Số phút ở trên đo trên máy cloud, không có card đồ hoạ.
