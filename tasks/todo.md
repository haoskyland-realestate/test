# Việc cần làm: Master cut kiểu chuyên nghiệp

## T1: Bộ test thật từ Saigon Park
**Mô tả:** Trích từ dự án Saigon Park 3 đoạn ngắn (text từng từ + âm lượng 20 ms, KHÔNG có hình/tiếng):
- (a) "Theo bản … vẽ quy hoạch" (ngập ngừng trong từ),
- (b) "biệt thự đơn lập, song lập" nói 2 lần,
- (c) "2 phân khu chính, phân khu thấp tầng" (không phải lặp).

Lưu thành `video-studio/scripts/test_du_lieu/cat_saigon.json`. Thêm bài test ghi rõ kết quả mong muốn. Ở bước này bài test đánh dấu (a) và (b) là "chưa bắt được": đó là mốc ban đầu.

**Tiêu chí:**
- [ ] File test < 50 KB, không chứa âm thanh/hình
- [ ] `test_master_cut.py` chạy được; ghi rõ (a), (b) chưa bắt được, (c) không báo

**Kiểm:** `python3 scripts/test_master_cut.py`

**Phụ thuộc:** Không · **File:** `scripts/test_master_cut.py`, `scripts/test_du_lieu/cat_saigon.json` · **Cỡ:** S

## T2: Chỗ cắt về đáy âm lượng + làm mềm âm 10 ms
**Mô tả:**
- Trong `doan_noi`, mỗi mốc vào/ra dời về khung 20 ms có âm lượng thấp nhất trong ±150 ms, nhưng không đè vào từ kế bên.
- Trong `giong.py`, mỗi đoạn ghép có `afade` vào/ra 10 ms. Độ dài không đổi.

**Tiêu chí:**
- [ ] Test: mốc cắt rơi vào khung có âm lượng ≤ ngưỡng lặng
- [ ] Đo trên bản ghép: không có bước nhảy biên độ lớn (> 0,2) ở chỗ ghép
- [ ] `kiem_cuoi.py` vẫn đạt (hình khớp tiếng ±0,1 giây)

**Kiểm:**
- `python3 scripts/test_master_cut.py`
- dựng thử `kiem_may.py --dung-thu`

**Phụ thuộc:** T1 · **File:** `scripts/master_cut.py`, `scripts/giong.py`, `scripts/test_master_cut.py` · **Cỡ:** S

## Checkpoint 1
- [ ] `python3 scripts/kiem_may.py --tu-kiem` đạt toàn bộ
- [ ] Không tiếng tách ở chỗ ghép (đo)

## T3: Ngập ngừng trong từ
**Mô tả:**
- Từ nào máy nghe kéo dài > 0,6 giây: đo âm lượng bên trong. Nếu có chuỗi lặng ≥ 0,35 giây thì tách thành "khoảng ngập ngừng", đề xuất cắt, chừa 0,1 giây mỗi bên.
- Thay `lam_on_tu`/`kep_tu` hiện chỉ dời điểm đầu.

**Tiêu chí:**
- [ ] Đoạn (a) của bộ test: bắt được khoảng 0,7–0,84 giây đúng chỗ (±0,1 giây)
- [ ] Từ kéo dài nhưng không có lặng bên trong (nói chậm): không cắt

**Kiểm:** `python3 scripts/test_master_cut.py`

**Phụ thuộc:** T1 · **File:** `scripts/master_cut.py`, test · **Cỡ:** S

## T4: Câu lặp
**Mô tả:**
- Phát hiện lặp bằng `phan_tich_loi.lap` (cụm ≥ 3 từ, liền nhau hoặc cách ≤ 2 từ), giữ lần nói sau, đề xuất bỏ lần đầu. Mốc cắt ở đáy âm lượng (dùng T2).
- `bo_noi_lai` chỉ giữ phần "lặp xa có ngập ngừng" mà `lap` không phủ, hoặc bỏ hẳn nếu test cho thấy trùng.

**Tiêu chí:**
- [ ] Đoạn (b): đề xuất bỏ đúng lần đầu "biệt thự đơn lập, song lập"
- [ ] Đoạn (c): không báo
- [ ] Bài test cũ của `bo_noi_lai` vẫn đạt (hoặc ghi lý do đổi)

**Kiểm:**
- `python3 scripts/test_master_cut.py`
- `python3 scripts/phan_tich_loi.py --tu-kiem`

**Phụ thuộc:** T1, T2 · **File:** `scripts/master_cut.py`, `scripts/phan_tich_loi.py`, test · **Cỡ:** M

## Checkpoint 2
- [ ] Bộ test thật bắt đúng (a), (b); không báo nhầm (c)
- [ ] `kiem_may.py --tu-kiem` đạt

## T5: Ba mức tin cậy + đề xuất + Cổng 1 agent
**Mô tả:**
- Master cut chỉ tự áp lặng thuần.
- Câu lặp, ngập ngừng trong từ, tiếng đệm (tuỳ Hào trả lời câu hỏi 1) ghi vào `build/cat-de-xuat.json` (`id`, loại, giây, câu, mức). Báo cáo `master-cut.md` liệt kê chúng.
- `master_cut.py --ap-dung <id,…|tat-ca>` áp các đề xuất đã duyệt, dùng `cat_doan.cat`.
- Agent Cổng 1 đọc file này thay cho `phan_tich_loi` trong `CAN-HOI.md`.

**Tiêu chí:**
- [ ] Chạy master cut không tự bỏ câu nào; đề xuất có trong file + báo cáo
- [ ] `--ap-dung` cắt đúng và dời chữ/thẻ (qua `cat_doan`); chạy lại không cắt hai lần
- [ ] Agent Cổng 1 hiện đề xuất có số `id`

**Kiểm:**
- `test_master_cut.py`
- `agent.py --tu-kiem`

**Phụ thuộc:** T3, T4 · **File:** `scripts/master_cut.py`, `scripts/agent.py`, `scripts/cat_doan.py`, test · **Cỡ:** M

## T6: Nhận dạng giọng một lần
**Mô tả:**
- Sau khi cắt, ghi text của `voice.wav` (và `.tin.json`) bằng cách dời mốc text từng file gốc qua bản đồ cắt (đoạn chính → giờ video), bỏ từ nằm trong phần bị cắt.
- Agent bỏ bước nhận dạng lần hai nếu text đã có và khớp mã giọng.

**Tiêu chí:**
- [ ] Trên Saigon Park: text dời mốc so với nhận dạng lại ≥ 95% từ trùng, lệch mốc trung vị ≤ 0,15 giây
- [ ] Agent không gọi máy nghe lần hai (đo thời gian)

**Kiểm:**
- `python3 scripts/master_cut.py --tu-kiem` (dời mốc trên dữ liệu giả)
- so sánh trên Saigon Park

**Phụ thuộc:** T5 · **File:** `scripts/master_cut.py`, `scripts/agent.py`, `scripts/phu_de.py` · **Cỡ:** M

## T7: Chạy lại Saigon Park từ file gốc
**Mô tả:** Tạo bản sao dự án (`zz-` …) từ footage gốc, chạy agent tới Cổng 1, so với 2 chỗ Hào đã cắt tay và bản cuối đã duyệt. Viết kết quả vào `build/master-cut.md`.

**Tiêu chí:**
- [ ] 2 chỗ cắt tay xuất hiện (tự động hoặc đề xuất)
- [ ] Không còn lặng > 0,6 giây giữa câu (đo)
- [ ] Bản xem 540 qua `kiem_cuoi.py`

**Kiểm:**
- `agent.py zz-… <footage>`
- `kiem_cuoi.py`

**Phụ thuộc:** T6 · **File:** không sửa code (chỉ chạy, ghi kết quả) · **Cỡ:** S

## Checkpoint 3 (xong)
- [ ] Mọi tiêu chí trên đạt
- [ ] Hào nghe bản xem 540 và duyệt
