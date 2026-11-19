# Kế hoạch: Làm lại master cut theo cách người dựng phim chuyên nghiệp

## Tổng quan
`video-studio/scripts/master_cut.py` đang tự cắt khoảng lặng, tiếng đệm và lần nói vấp, rồi **áp luôn** vào timeline.
Video Saigon Park (17–18/11) lộ 4 điểm yếu thật:
1. **Không bắt được ngập ngừng nằm trong một từ.** "Theo bản … vẽ quy hoạch": lặng 0,84 giây nhưng máy nghe kéo dài chữ "vẽ" thành 1,66 giây, nên lặng nằm "trong từ" và master cut không cắt. Phải cắt tay.
2. **Không bắt được câu lặp.** "biệt thự đơn lập, song lập" nói 2 lần liền. `bo_noi_lai` đòi lặng ≥ 0,4 giây trước lần sau, mà ở đây không đủ. `phan_tich_loi.lap` thì bắt được.
3. **Chỗ cắt đặt theo mốc của máy nghe**, mà mốc này lệch ±0,1–0,3 giây (đã đo). Hai đoạn ghép thẳng, không làm mềm, nên có thể nghe tiếng "tách".
4. **Áp luôn, không hỏi.** Bỏ câu "vấp" là quyết định biên tập, trái với nguyên tắc agent "không đoán". Thêm nữa, giọng bị nhận dạng 2 lần (master cut 1 lần trên file gốc, agent 1 lần trên `voice.wav`): tốn thời gian, và hai bản có thể lệch nhau.

Mục tiêu: chỗ cắt **nghe không ra** (đúng khoảng lặng, có làm mềm âm), bắt được ngập ngừng và câu lặp, và tách rõ chỗ **tự cắt** (lặng thuần) với chỗ **đề xuất** (bỏ câu, bỏ từ) để Hào duyệt ở Cổng 1 của agent.

## Quyết định thiết kế
- **Đo âm lượng là chuẩn, mốc máy nghe chỉ là gợi ý.** Mọi chỗ cắt dịch về chỗ âm lượng thấp nhất trong ±150 ms quanh mốc. Dùng lại `nang_luong`/`nguong` có sẵn.
- **Mỗi chỗ ghép có làm mềm âm 10 ms** (`afade` in/out) trong `giong.py`, cho cả `dung.py` và agent. Đây là chuẩn nghề, tránh tiếng tách.
- **Ba mức tin cậy:**
  - *Tự cắt*: lặng thuần đo bằng âm lượng.
  - *Đề xuất*: câu lặp ≥ 3 từ, ngập ngừng trong từ, tiếng đệm.
  - *Chỉ báo*: lặp 1–2 từ, nói nhanh/chậm.
  - Đề xuất ghi vào `build/cat-de-xuat.json`, chỉ áp khi Hào duyệt.
- **Một nguồn phát hiện lặp:** dùng `phan_tich_loi.lap` (đã kiểm trên Saigon Park), bỏ bản trùng trong `bo_noi_lai`.
- **Nhận dạng giọng một lần:** sau khi cắt, text của `voice.wav` lấy bằng cách dời mốc từ text file gốc qua bản đồ cắt, không chạy máy nghe lần hai. Giữ cả độ tin cậy từng từ.
- **Kiểm bằng dữ liệu thật:** trích một đoạn ngắn (từ + âm lượng, không có hình) của 2 lỗi Saigon Park làm bộ test cố định.

## Đồ thị phụ thuộc
```
T1 bộ test thật (Saigon Park)
 ├─ T2 chỗ cắt về đáy âm lượng + làm mềm 10 ms
 ├─ T3 ngập ngừng trong từ
 └─ T4 câu lặp (dùng phan_tich_loi.lap)
        └─ T5 ba mức tin cậy + cat-de-xuat.json + --ap-dung + Cổng 1 agent
               └─ T6 nhận dạng giọng một lần (dời mốc qua bản đồ cắt)
                      └─ T7 chạy lại Saigon Park từ file gốc, so với bản cắt tay
```

## Danh sách việc
Chi tiết, tiêu chí nghiệm thu và cách kiểm: `tasks/todo.md`.

### Đợt 1: Nền tảng và độ chính xác chỗ cắt
- [ ] T1: Bộ test thật từ Saigon Park
- [ ] T2: Chỗ cắt về đáy âm lượng + làm mềm âm 10 ms

### Checkpoint 1
- [ ] Mọi bài tự kiểm đạt (`kiem_may.py --tu-kiem`); không còn tiếng tách ở chỗ ghép (đo)

### Đợt 2: Bắt lỗi nói
- [ ] T3: Ngập ngừng trong từ
- [ ] T4: Câu lặp

### Checkpoint 2
- [ ] Bộ test thật: bắt đúng cả 2 lỗi Saigon Park, không báo nhầm "2 phân khu chính, phân khu thấp tầng"

### Đợt 3: Quy trình duyệt và hiệu năng
- [ ] T5: Ba mức tin cậy + đề xuất + Cổng 1 agent
- [ ] T6: Nhận dạng giọng một lần
- [ ] T7: Chạy lại Saigon Park từ file gốc

### Checkpoint 3 (xong)
- [ ] Saigon Park chạy lại từ file gốc: ra đúng 2 chỗ Hào đã cắt tay (tự động hoặc đề xuất), không còn chỗ lặng > 0,6 giây giữa câu
- [ ] Hào nghe bản xem 540 và duyệt

## Rủi ro
| Rủi ro | Mức | Cách giảm |
|---|---|---|
| Cắt nhầm chỗ lặp có chủ ý ("rất rất", nhấn mạnh) | Cao | Lặp chỉ là *đề xuất*, Hào duyệt; lặp 1–2 từ chỉ báo |
| Dời chỗ cắt về đáy âm lượng làm lệch hình (khẩu hình) | Trung bình | Chỉ dời trong ±150 ms; hình và tiếng cắt cùng mốc |
| Dời mốc text qua bản đồ cắt sai khi cắt trúng giữa từ | Trung bình | Từ nằm trong đoạn bị cắt thì bỏ; T6 có test so với nhận dạng lại |
| Đổi `giong.py` làm lệch mốc các dự án cũ | Thấp | Làm mềm không đổi độ dài; `kiem_cuoi.py` kiểm hình khớp tiếng |
| Ngưỡng chỉnh trên ít giọng (Hùng, Gladia) | Trung bình | Ghi ngưỡng trong code; ghi "mới kiểm trên 2 giọng" |

## Câu hỏi cần Hào trả lời
1. **Tiếng đệm** "ờ, à, ừm": tự cắt luôn (như hiện nay), hay đưa vào đề xuất?
2. **Nhịp nghỉ**: giữ như hiện nay (giữa câu ~0,22 giây, cuối câu ~0,38 giây), hay Hào muốn chậm/nhanh hơn?
3. **Video cũ**: có cần chạy lại master cut cho các video cũ (Gladia), hay chỉ áp cho video mới?
