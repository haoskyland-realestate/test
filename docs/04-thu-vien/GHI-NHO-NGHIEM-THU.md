# Ghi nhớ nghiệm thu: lỗi đã gặp và cách dựng đúng

Mỗi lần Hào nghiệm thu một video, ghi lại ở đây: Hào thấy gì, nguyên nhân, cách sửa, đã đưa vào phần mềm chưa. **Claude đọc file này trước khi dựng video mới.**

---

## Lần 1: video Gladia (13/11/2026)

Dự án `projects/zz-2026-11-13_tiktok_nghiem-thu` (video thô 77 giây, Hào đi giới thiệu nhà mẫu, quay một mạch bằng DJI, 1728×3072, 60 khung/giây). Hào nhận xét: "tạm ổn", chưa cần dựng lại; chỉ xem khung demo cho 3 điểm sau.

### 1. Màu da bị cam, bị cháy

![Màu da](anh-nghiem-thu/2026-11-13_1-mau-da.jpg)

| | Độ rực của da (vùng giữa mặt) |
|---|---|
| Video gốc của máy quay | 38–45% |
| Bản đã dựng | **51–74%** (cam hẳn, gần cháy) |
| Màu mới (demo) | 39–47% |

**Nguyên nhân (đã đo):** hai bước cùng đẩy màu lên:
1. `mau.tu_can` thấy cảnh nội thất toàn màu trắng (ít màu) nên **tăng độ rực tới 1,3 lần**. Trong cảnh trắng, thứ có màu duy nhất là da người, nên da bị đẩy mạnh nhất.
2. Phong cách `edit-phim` dùng màu `tuoi-dam` (+8% độ rực, +18% vibrance) cộng thêm lần nữa.

**Cách dựng đúng:**
- Cảnh có người nói trong nội thất trắng: **không tăng độ rực khi tự cân** (tối đa 1,05).
- Thêm bước **giữ màu da**: giảm 14% độ rực riêng vùng đỏ/vàng, ngả lạnh nhẹ (6800K, trộn 35%):
  `eq=contrast=1.05:saturation=1.04,huesaturation=colors=r+y:saturation=-0.14,colortemperature=temperature=6800:mix=0.35`
- Kiểm tra bằng số, không bằng mắt: da (vùng giữa mặt) nên ở **35–50% độ rực, sắc độ 14–20°**. Vượt 55% là cam.
- Trắng của tủ, tường phải vẫn trắng sạch (đã kiểm trong demo).

**Trạng thái (13/11):** đã làm. `mau.tu_can` không tăng rực quá 5%. Bộ đạo diễn màu `scripts/chinh_mau.py` (`CHINH-MAU.md`) có bước giữ da: thử với video này, da giữ 38→38%, kể cả khi lấy màu từ ảnh mẫu tông cam (38→40%). Chưa dựng lại video Gladia.

### 2. Chữ che mặt: phải đặt chữ sau đầu

![Chữ sau đầu](anh-nghiem-thu/2026-11-13_2-chu-sau-dau.jpg)

**Hào nhận xét:** chữ lớn (GLADIA, 77 TỶ…) đè lên mặt. Dân edit chuyên nghiệp đặt chữ **sau đầu**: chữ to vẫn nổi mà mặt người nói không bị che.

**Cách dựng đúng:**
- Đặt chữ lớn **ngang trán hoặc ngang tai**, khoảng 1/3 trên của khung (không đặt giữa khung).
- Tách người ra khỏi nền (mặt nạ người), rồi xếp lớp theo thứ tự: **video → chữ → người**. Chữ bị đầu và vai che một phần là đúng ý đồ: tạo chiều sâu.
- Nhãn nhỏ phía trên ("biệt thự đơn lập") đặt cao hơn đỉnh đầu, không để đầu che.
- Chữ có số liệu (giá, diện tích) **không được** để đầu che mất chữ số. Nếu đầu nằm giữa khung thì dời số sang hai bên hoặc lên cao.
- Khi người đi lại (không đứng yên) thì chỉ dùng chữ sau đầu ở cảnh đứng nói; cảnh đi bộ để chữ ở trên cao như cũ.

**Trạng thái (13/11, Hào yêu cầu làm):** đã làm cho cả video. Thêm `"sau_dau": true` vào khối chữ (vd. `title3d`). Bộ dựng:
1. dựng nền ra file;
2. tách người từng khung bằng **MODNet** (giấy phép Apache-2.0, 25 MB, chạy bằng onnxruntime có sẵn, tự tải về `video-studio/models/` lần đầu), chỉ ở khoảng có chữ, làm mượt mép theo thời gian;
3. ghép nền → chữ → người.

**Tự đặt chữ ngang đầu:** bộ dựng tìm đỉnh đầu ở giây thứ 0,8 của mỗi chữ (tính cả zoom), đặt khối chữ để khoảng 30% dưới của chữ lớn nằm sau đầu. Đặt tay thì ghi `top_px`. Dòng nhỏ dưới chữ lớn (`sub`) thường bị đầu che, nên chữ sau đầu nên để thông tin chính ở chữ lớn và nhãn trên.
Mã: `scripts/tach_nguoi.py`, `dung.py`. Tốc độ trên cloud: khoảng 0,3 giây mỗi khung hình. Khung xem trước của app chưa hiện hiệu ứng này, phải Dựng nháp mới thấy. Vật ở tiền cảnh (mặt bàn đá) cũng được tính là "người", nên chữ đặt thấp sẽ bị che.

### 3. Zoom in / zoom out chưa đẹp

![Zoom](anh-nghiem-thu/2026-11-13_3-zoom.jpg)

**Nguyên nhân:** master cut tự thêm "phóng xen kẽ" kiểu nhảy cỡ: **100% → 108% trong đúng 1 khung hình**, phóng vào **tâm khung** (không theo mặt), giữ nguyên vài giây rồi nhảy về. Người xem thấy như máy giật, và có lúc đầu bị đẩy lệch.

**Cách dựng đúng:**
- **Đẩy vào êm** (push-in) 0,4–0,6 giây có gia tốc (chậm → nhanh → chậm), tối đa **104–106%**, không phải 108%.
- **Neo theo mặt**: mặt nằm ở khoảng 1/3 trên của khung khi phóng, không phóng vào tâm.
- Chỉ phóng khi **có lý do**: câu chốt, con số, chữ lớn hiện ra. Không rải đều mỗi 4 giây.
- Phóng xong thì **lùi ra rất chậm** (1–2 giây) hoặc giữ đến chỗ cắt tiếp theo. Không nhảy về 100% giữa câu.
- Cắt nhảy giữa hai mẩu nói cùng góc máy: đổi cỡ 100% ↔ 104% **ngay tại chỗ cắt** thì được (che vết cắt). Không đổi cỡ giữa một mẩu.
- Video đi bộ (máy đang di chuyển) thì hạn chế zoom, vì chuyển động của máy đã đủ.

**Trạng thái (14/11): đã sửa.** `effects.zoom_bieu_thuc`: đẩy vào êm (chậm → nhanh → chậm) 0,5 giây, lùi ra êm ≤1 giây, neo ở 38% chiều cao khung (42% với YouTube) thay vì tâm; `master_cut.PUNCH` giảm 1,08 → 1,05. Đo bằng dựng thật ô trắng 240px: 240 → 259 (×1,08) đúng mốc 1,0–3,0s, hết lệch giờ, bước lớn nhất mỗi khung ~2px (trước nhảy 8% trong 1 khung). Kiểm: `scripts/test_zoom.py`. **Chưa làm:** neo theo mặt thật (hiện neo cố định), chỉ phóng khi có lý do (chữ lớn, câu chốt) thay vì rải xen kẽ. Chưa thử trên footage thật của Hào.

### Những điều khác của lần này (đã sửa trong code)
- Cắt khoảng lặng từng bỏ mất 13 giây mở đầu vì một câu nói lặp lại. Đã sửa: chỉ bỏ lần nói trước gần nhất, và không bỏ đoạn có câu đã nói trọn (`master_cut.py`, có bài kiểm thử).
- Chữ dài ("PHÒNG KHÁCH") tràn khung. Đã sửa: chữ dài tự thu nhỏ (`lop_chu.py`).
- Phụ đề tự nhận dạng còn sai từ chuyên ngành ("chủ tư", "sông vườn"). Lần sau nhận dạng kèm danh sách từ của dự án (Gladia, chủ đầu tư, sân vườn, bàn giao…) thì đúng hơn hẳn.

---

## Việc cần làm để áp dụng (theo thứ tự)
1. ~~Màu da~~: xong 13/11 (`chinh_mau.py`, chặn tăng rực trong `tu_can`).
2. ~~Zoom êm~~: xong 14/11 (còn: neo theo mặt thật, phóng theo chữ lớn).
3. ~~Chữ sau đầu~~: xong 13/11 (`sau_dau`, MODNet).

---

## Lần 2: video Gladia, chữ sau đầu + âm theo nhịp chữ (13/11/2026)
Hào: "ưng hiệu ứng chữ lúc ban đầu hơn (chữ trắng nổi 3D lao vào), nhưng vẫn giữ chữ phía sau đầu; kết hợp bộ âm cho nhịp chữ như chuyên gia âm thanh".

### Luật âm theo nhịp chữ (mẫu có `nhip_chu`, mã `ap_mau.py`)
| Lớp | Thời điểm | Âm mặc định | Âm lượng | Luật |
|---|---|---|---|---|
| Vào | **đỉnh** tiếng vút trùng khung chữ chạm | `whoosh_nhanh_01` | 0,45 | lọc trầm 150 Hz (không lấn giọng); hai tiếng vút cách nhau ≥ 0,4 s |
| Chạm | khung chữ dừng | `chu_swish-pop_01` (theo mẫu) | 0,55 | có sẵn từ trước |
| Trầm | chỉ chữ **đầu tiên** và chữ có **tiền, %** | `impact_tram_01` | 0,55 | không đặt cho mọi chữ: nghe nhàm, mất sức nặng |
| Lấp lánh | chữ có số | `ting_lap-lanh_01` | 0,3 | thay tiếng ting số liệu cũ (hai tiếng ting chồng nhau nghe rối) |
| Ra | lúc chữ tan | `whoosh_quat_01` | 0,22 | bỏ nếu chữ sau tới trong 0,6 s; lọc trầm 200 Hz |
| Chung | | | | cao độ luân phiên 100% / 96% / 104% để tai không nhận ra một tiếng lặp lại; cả bài chuẩn −14 LUFS sau khi trộn |

---

## Bài học từ video hướng dẫn dạy AI học style (14/11/2026, Hào gửi, 12 phút)
Quy trình người làm video dùng: một video mẫu và câu lệnh liệt kê rõ phải phân tích gì (nhịp, chữ, hiệu ứng, chuyển cảnh, font) → AI ghi lại thành skill → thử với một clip thô → góp ý 3–4 vòng. Lỗi thường gặp ở các vòng đầu và cách sửa:
- Chữ hiện rồi biến quá nhanh: cho chậm lại; mọi chuyển động phải có ease in-out.
- Chữ nhỏ, bố cục lệch: to lên, cân lại.
- Đồ hoạ đè lên người nói: dời ra; lỗi về vị trí thì gửi **ảnh chụp khung** kèm góp ý (nút 📸 Lưu gói góp ý).
- 10 giây đầu chậm: đây là đoạn quyết định người xem ở lại; dựng nhanh gọn nhất.
Dùng 1 video mẫu để giống đúng style đó; 2–3 video để ra style riêng. Skill: `.claude/skills/hoc-mau/`.

---

## QUY TẮC CỨNG: đối chiếu ghi âm và kịch bản, không đoán ý, hỏi Hào rồi mới dựng (Hào chốt 14/11/2026)
1. **Viết ra text từ ghi âm** (nhận dạng giọng, `build/transcripts/`) và **đặt cạnh kịch bản** (`KICH-BAN.md`, `NGUON-SO-LIEU.md`) để so sánh trùng khớp. Không đoán ý Hào định nói gì.
2. Mọi **chữ, số, tên, dữ kiện** hiện trên màn hình phải có một trong ba: (a) chính Hào nói trong ghi âm, (b) có trong `NGUON-SO-LIEU.md` với cột "Hào xác nhận" = rồi, (c) Hào duyệt riêng (`meta.da_duyet`). Số tiền, diện tích, pháp lý, chính sách phải có nguồn và ngày.
3. **Không biết, không chắc, thông tin chưa kiểm chứng, lời nói khác kịch bản, còn `[...]`: HỎI HÀO trước, rồi mới dựng bản cuối.** Không tự điền, không tự sửa số cho "hợp lý".
4. Máy làm hộ phần kiểm: `python3 scripts/doi_chieu.py projects/<tên>` → `build/doi-chieu.md`. `dung.py` tự chạy và **dừng (bản cuối)** khi còn mục cần hỏi; Hào đồng ý rồi mới thêm `meta.da_duyet` hoặc chạy `dung.py --da-duyet`. Bản nháp chỉ cảnh báo để còn xem bố cục.
5. Chưa kiểm tự động: tên riêng, pháp lý, ý nghĩa của từ khoá. Claude vẫn đọc báo cáo và hỏi khi nghi ngờ. Thẻ số liệu (`kieu: "so-lieu"`) bắt buộc có `nguon`.

## Bố cục chữ chuyên nghiệp (14/11/2026)
- Chữ to nhất có thể mà vẫn nằm gọn chiều ngang (lề 70px); từ khoá to hơn chữ thường (mặc định ×2); cụm chữ không rớt vào vùng giao diện TikTok (dưới 78% chiều cao) và không lên sát đỉnh (trên 30%). Mã: `lop_chu.bo_cuc_loi`.
- Cảnh chèn đồ hoạ (`cards`, trường `kieu`): `so-lieu` (một số lớn + nhãn + nguồn), `quy-dao` (tâm + 2–6 ý xoay quanh), `checklist` (dấu ✓ cam), `kinh` (thẻ kính một câu nhấn), `danh-sach` (cũ). Mỗi 8–10 giây một cảnh chèn rồi về người nói.

## Thiết kế âm cho chữ theo nhịp nói (14/11/2026)
Đo 3 video mẫu Open Residency: độ ồn −29, −25 và **−14,8 LUFS**: chỉ bản hoàn thiện có lớp nền liên tục (dải trầm–trung) cộng tiếng chạm; hai bản kia gần như chỉ có giọng. Đo tiếng cao tần so với mốc cắt: **không trùng hơn ngẫu nhiên** (9/31 mốc cắt so với 9,3 kỳ vọng), nên **không tách riêng được lớp hiệu ứng âm của video mẫu bằng máy**; phần thiết kế âm của mình dựa theo cách dựng chuyên nghiệp thông thường, không chép âm của người khác. Hào cho mốc giờ cụ thể ("giây X có tiếng gì") thì mình bám sát hơn.
Các lớp âm: xem `MAU.md` của `talking-cam-01`. Mọi âm vào mẫu qua `am_loi` (đổi âm: sửa `mau.json`).

## Tốc độ chuyển động chữ (Hào chốt 14/11/2026)
- Chữ xuất hiện **chậm hơn** để nhìn rõ chuyển động: mọi chuyển động chữ và cảnh chèn dài gấp **1,5 lần** (`meta.cham_chu`, mặc định 1.5).
- **Mọi chuyển động đều có ease in-out** (tăng tốc nhẹ rồi hãm lại), kể cả lúc chữ ra. Không dùng kiểu chạy đều hay dừng gắt. Mã: `lop_chu.em_dan` áp cho mọi chữ, thẻ, tag, cảnh chèn; chỉ thanh tiến độ chạy đều.
- Chữ theo nhịp nói bắt đầu sớm 0,1 giây để rõ hẳn đúng lúc nói; cuối cụm mờ ra êm. Tiếng chạm của từ khoá dời theo (đỉnh chuyển động).

## CẬP NHẬT quy tắc đối chiếu (Hào chốt 16/11/2026, thay một phần mục "QUY TẮC CỨNG" ở trên)
- **Từ nghe sai: Claude được đoán ý cho phù hợp nội dung, chủ đề** (vd. "bàn giao kẻ" → "bàn giao kèm", "chủ tư" → "chủ đầu tư"), ghi vào `meta.sua_tu` và **liệt kê các chỗ đã sửa** trong tin báo cho Hào. Không cần hỏi trước từng chữ.
- **Thông tin Hào đưa đều đã xác thực**: lời Hào nói trong video và tài liệu Hào gửi được dùng thẳng; nguồn ghi "Hào cung cấp, <ngày>".
- **Vẫn phải hỏi Hào** khi: thông tin không do Hào nói hay gửi (Claude tự tìm, tự suy ra số), các nguồn mâu thuẫn nhau, hoặc đoán ý mà có nhiều cách hiểu khác hẳn nhau về nghĩa (giá, pháp lý, chính sách).

## Âm thanh chuyên nghiệp: bộ âm của Hào + cách trộn (Hào nhận xét 16/11/2026: "thiếu tính chuyên nghiệp")
- Dùng **bộ âm của Hào** (Drive KHO-EDIT, 12 âm `hsl_*` trong `thu-vien-am-thanh/`), không dùng âm tổng hợp cho mẫu talking head.
- **Không dày đặc:** pop cụm chữ chỉ cách một cụm, cụm có từ khoá đã có âm riêng thì không thêm pop; mỗi từ khoá: vút trước + vút-chạm + chuông nhẹ.
- **Hiệu ứng nằm dưới giọng:** đo bản demo: giọng −23,8 LUFS, lớp hiệu ứng −29,7 LUFS (thấp hơn ~6 dB). Không để hiệu ứng to ngang giọng.
- **Ducking:** nhạc nền tự nhỏ xuống khi Hào nói (nén theo giọng, đo thử: nhỏ đi 13,5 dB lúc nói), lên lại lúc nghỉ. Mã: `dung.py` (sidechaincompress).
- Âm có đuôi dài (vút-chạm 4–6 giây) cắt còn 1,8 giây, mờ đuôi.
