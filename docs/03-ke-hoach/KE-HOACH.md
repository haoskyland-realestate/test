# Kế hoạch xây bộ khung Cloud Edit Video hoàn chỉnh

Lập ngày 12/11/2026 (thứ Năm). Đây là kế hoạch, chưa phải cam kết: mốc ngày phụ thuộc vào thời gian Hào dành mỗi ngày (xem mục Giả định).

## 0. Cập nhật 12/11/2026 sau khi Hào trả lời
Hào dành được cả ngày (giới hạn là token), tự thu giọng, repo riêng tư, có logo và bộ màu. Video đầu là TikTok khoảng 130 giây từ flycam thô + giọng thu + kịch bản. Vì vậy **cắt ghép tự động trở thành lõi của V1.0**, đồ họa HyperFrames chỉ dùng cho cảnh chữ/số. Mốc V1.0 có thể sớm hơn 20/11 nếu Hào gửi đủ tài liệu trong ngày: xem `../99-luu-tru/QUY-TRINH-CAT-GHEP.md` (đã thay bằng `../02-quy-trinh/QUY-TRINH-MOT-VIDEO.md`). Mốc V1.1 (giọng, phụ đề) gộp vào V1.0 vì Hào đã có giọng.

## 1. Đích đến

Một hệ thống mà Hào chỉ làm 3 việc: **chọn chủ đề, xác minh số liệu, bấm render rồi đăng**. Phần soạn bản nháp, dựng, chuẩn hóa định dạng do Claude và công cụ làm. Chạy được trên GitHub (điện thoại/PC) và sau này trên Windows 11 local.

Định nghĩa "bộ khung hoàn chỉnh" (đủ 8 mảnh):
1. Kho dữ liệu dự án có nguồn và ngày (nguồn sự thật của mọi con số).
2. Spec video giàu hơn (nhiều cảnh, không chỉ 1 hook + 3 ý).
3. Nhận diện Hào Sky Land (màu, font, logo, cảnh kết).
4. Thư viện mẫu cảnh (dùng lại, ghép lại).
5. Âm thanh: giọng đọc, nhạc nền, phụ đề.
6. Kiểm tra chất lượng tự động trước khi đăng.
7. Gói đăng: video, ảnh bìa, tiêu đề, mô tả, hashtag.
8. Hai nơi chạy: GitHub và Windows 11 local, cùng một bộ mã.

## 2. Hiện trạng (đã làm, đã kiểm)

| Mảnh | Trạng thái |
|---|---|
| Render HyperFrames (chữ + GSAP + khối 3D) | Chạy trong sandbox và trên GitHub Actions |
| Remotion, FFmpeg | Chạy trong sandbox |
| Form render trên GitHub | Chạy thành công 1 lần (run #2). Ô chọn mẫu mới ở PR #4, chưa gộp |
| App PWA | Có mã, chưa mở thử trên điện thoại |
| Trang Pages cũ | Đã bấm chạy lại "Deploy site", **chưa kiểm** kết quả |
| Thư viện mẫu | 2 mẫu (PR #4) |
| Manim, Blender MCP, Codespaces, Windows 11 | Chưa thử |
| Âm thanh, phụ đề, nhận diện, kho dữ liệu, kiểm tra tự động, gói đăng | Chưa có |

Khoảng trống lớn nhất so với một video đăng được: **video mẫu hiện không có tiếng, không có phụ đề, không có logo và cảnh kết**.

## 3. Giả định (đổi giả định thì đổi mốc)

- Hào dành khoảng 1 giờ mỗi ngày cho dự án (việc chính là kinh doanh bất động sản, ưu tiên số 1).
- Claude làm phần xây dựng; mỗi lần Hào trả lời chậm thì mốc lùi tương ứng.
- Số liệu thật của Vinhomes Hóc Môn / Cần Giờ do Hào xác minh với chủ đầu tư; Claude không tự điền.
- Chưa ai kiểm tra giấy phép nhạc, ảnh, giọng AI nào. Dùng nguồn nào cũng phải kiểm.

## 4. Các giai đoạn

### Giai đoạn 0: Chốt nền (12–14/11, 3 ngày)
Mục tiêu: không còn việc treo từ phiên trước.

| # | Việc | Ai | Xong khi |
|---|---|---|---|
| 0.1 | Gộp PR #4 | Hào cho phép, Claude làm | Form có ô chọn mẫu |
| 0.2 | Mở địa chỉ Pages, kiểm trang cũ ở gốc và `/app/` | Hào xem, Claude đọc log | Trang cũ hiện đúng |
| 0.3 | Mở app trên điện thoại, thử "thêm vào màn hình chính" | Hào | Cài được hoặc ghi rõ lỗi |
| 0.4 | Chốt: repo công khai hay riêng tư | Hào | Quyết định ghi vào CLAUDE.md |
| 0.5 | Chốt chủ đề video thật đầu tiên | Hào | 1 câu chủ đề |

### Giai đoạn 1: V1.0 — video thật đầu tiên đăng được (15–20/11, 6 ngày)
Mục tiêu: **một video 30–45 giây, 9:16, có số liệu thật có nguồn, có nhận diện, đăng TikTok được**, làm hoàn toàn từ form trên GitHub.

| # | Việc | Ai | Xong khi |
|---|---|---|---|
| 1.1 | Kho dữ liệu dự án (file đơn giản, mỗi dòng: dự án, chỉ số, giá trị, nguồn, ngày cập nhật) | Claude dựng khung, Hào điền | Có ít nhất 5 chỉ số của 1 dự án, đủ nguồn và ngày |
| 1.2 | Nhận diện Hào Sky Land: bảng màu, font, logo (Hào cung cấp), cảnh kết có lời kêu gọi | Hào gửi logo, Claude làm | Cảnh kết xuất hiện trong video |
| 1.3 | Nâng spec: nhiều cảnh (mở đầu, 3 ý, rủi ro, kết) thay vì 1 hook + 3 ý | Claude | Video 30–45 giây, tách cảnh rõ |
| 1.4 | Mẫu "số lớn": 1 con số nổi bật + giải thích ngắn (dòng tiền tháng, lãi vay) | Claude | Dùng được cho góc dòng tiền |
| 1.5 | Kiểm tra spec tự động: còn `[...]`, thiếu nguồn/ngày, chữ quá dài, độ dài video | Claude | Render từ chối khi còn chỗ trống |
| 1.6 | Gói đăng: ảnh bìa, tiêu đề, mô tả, hashtag (bản nháp để Hào sửa) | Claude | Có file kèm video |
| 1.7 | Render thật, xem, sửa chữ, đăng | Hào | Video đã đăng |

Rủi ro chính: số liệu chưa kịp xác minh. Cách xử lý: nếu thiếu số liệu có nguồn, V1.0 chuyển sang chủ đề không cần con số riêng (ví dụ cách đọc bài toán dòng tiền, có rủi ro) thay vì điền số chưa kiểm.

### Giai đoạn 2: V1.1 — có tiếng và phụ đề (21–27/11, 7 ngày)
Mục tiêu: video có giọng đọc, phụ đề tiếng Việt, nhạc nền nhẹ.

| # | Việc | Ai | Xong khi |
|---|---|---|---|
| 2.1 | Chọn giọng: Hào tự thu (tự nhiên, đúng thương hiệu "mộc mạc") hay giọng AI (nhanh hơn, ít cá nhân) | Hào chọn | Quyết định ghi lại |
| 2.2 | Kịch bản lời đọc cho từng cảnh, độ dài khớp cảnh | Claude nháp, Hào sửa | Lời đọc cho video 1 |
| 2.3 | Ghép giọng vào video bằng FFmpeg, căn thời lượng cảnh theo giọng | Claude | Video có tiếng, cảnh khớp lời |
| 2.4 | Phụ đề tự động từ giọng, chỉnh lỗi chính tả tiếng Việt, hiện trong video | Claude, Hào duyệt | Phụ đề đúng chính tả |
| 2.5 | Nhạc nền: chọn nguồn miễn phí rõ giấy phép, hạ âm lượng dưới giọng | Hào chọn nguồn, Claude ghép | Ghi rõ nguồn và giấy phép |
| 2.6 | Render và đăng video thứ 2 có tiếng | Hào | Video đã đăng |

Rủi ro: nhận dạng giọng tiếng Việt có thể sai tên riêng và số; luôn cần Hào đọc lại phụ đề. Giọng AI tiếng Việt chất lượng chưa kiểm.

### Giai đoạn 3: V1.2 — thư viện mẫu và nội dung đều đặn (28/11–10/12, khoảng 2 tuần)
Mục tiêu: ra 2 video mỗi tuần mà không phải thiết kế lại từ đầu.

| # | Việc | Xong khi |
|---|---|---|
| 3.1 | Thêm 3 mẫu cảnh: so sánh 2 phương án, biểu đồ dòng tiền theo năm, câu hỏi khách hay hỏi + trả lời | Thư viện có 5–6 mẫu |
| 3.2 | Cho phép ghép các mẫu thành video bằng spec (mỗi cảnh chọn một mẫu) | Video ghép từ ít nhất 3 mẫu |
| 3.3 | Chèn ảnh/video thật Hào quay (cảnh dự án, Hào nói trước máy), FFmpeg cắt ghép | 1 video có cảnh quay thật |
| 3.4 | Biến thể YouTube 16:9 từ cùng nội dung | 1 video xuất cả 9:16 và 16:9 |
| 3.5 | Kiểm tra kiểu chữ tránh: "cơ hội vàng", "cháy hàng"... cảnh báo khi spec chứa | Render cảnh báo |
| 3.6 | Nhịp tuần theo `../02-quy-trinh/NHIP-TUAN.md`, ghi kết quả mỗi tuần | 4 video đã đăng, có số liệu tương tác |

### Giai đoạn 4: V2 — chạy trên Windows 11 local (11/12–31/12)
Mục tiêu: render nhanh trên máy của Hào, không phụ thuộc GitHub, không giới hạn thời gian chạy.

| # | Việc | Xong khi |
|---|---|---|
| 4.1 | Thử `setup-windows.ps1` và `chay-video.bat` trên Windows 11 thật, sửa lỗi | Render ra MP4 trên máy Hào |
| 4.2 | Tận dụng card đồ họa RTX 5060 khi PC sẵn sàng (render nhanh hơn, 3D mượt hơn) | Đo thời gian render, so với GitHub |
| 4.3 | Thử Manim với biểu đồ dòng tiền (ưu tiên 1 trong các mẫu ở 3.1) | 1 cảnh Manim nhúng được vào video |
| 4.4 | Thử Blender MCP: 1 cảnh 3D (ví dụ mô hình đơn giản), xuất ảnh/video dùng làm nền | 1 cảnh Blender dùng được; nếu không đáng công thì ghi rõ và bỏ |
| 4.5 | Thử Codespaces (nếu vẫn cần) | Chạy được hoặc bỏ khỏi tài liệu |
| 4.6 | App bấm nút gọi render từ điện thoại (cần token GitHub; chỉ làm nếu thao tác form hiện tại còn bất tiện) | Quyết định sau khi dùng form 3–4 tuần |

### Giai đoạn 5: Ổn định và chuẩn bị mùa chững (tháng 1/2027)
- Doanh số hay chững dịp Tết (đầu tháng 2/2027, cần xem lại lịch) và tháng 7 âm lịch: dùng tháng 1 để làm sẵn kho video cho giai đoạn này.
- Thêm kiểm tra tự động khi sửa mã (không gãy render), ghim phiên bản công cụ, dọn tài liệu.
- Xem lại: bài nào kéo tin nhắn đúng nhóm khách mục tiêu, giữ mẫu đó, bỏ mẫu không dùng.

## 5. Bảng mốc tổng

| Mốc | Dự kiến | Bạn có gì |
|---|---|---|
| Chốt nền | 14/11 | PR gộp, trang cũ kiểm xong, chủ đề đã chọn |
| **V1.0** | **20/11** | Video thật đầu tiên đăng được (không tiếng) |
| V1.1 | 27/11 | Có giọng đọc, phụ đề, nhạc nền |
| V1.2 | 10/12 | 5–6 mẫu, ghép cảnh, 9:16 và 16:9, 4 video đã đăng |
| V2 | 31/12 | Chạy được trên Windows 11 local, thử xong Manim và Blender |
| Ổn định | 31/1/2027 | Kho video dự phòng cho Tết |

Nếu Hào dành ít hơn 1 giờ/ngày, kéo dài mỗi giai đoạn tương ứng. Nếu bận hơn, **bỏ giai đoạn 4 trước** (Windows, Manim, Blender), không bỏ giai đoạn 1–2 vì đó là phần tạo khách.

## 6. Việc không làm (để khỏi phân tán)
- Không làm app riêng cho từng hệ điều hành; PWA là đủ.
- Không làm CRM trong dự án này (đã là một mục tiêu riêng).
- Không đầu tư Blender, Manim trước khi V1.0–V1.2 đã ra video đều.
- Không thêm công cụ mới khi chưa dùng hết công cụ đang có.

## 7. Rủi ro và cách xử lý
| Rủi ro | Cách xử lý |
|---|---|
| Hào trì hoãn viết kịch bản / duyệt số liệu | Claude luôn mớm bản nháp trước; mỗi tuần chỉ 1 video bắt buộc |
| Số liệu dự án sai hoặc cũ | Mọi số liệu qua kho dữ liệu có nguồn + ngày; render chặn khi thiếu |
| Giấy phép (Remotion, nhạc, ảnh, giọng AI) | Ghi nguồn và giấy phép từng thứ dùng; Remotion chỉ dự phòng |
| Render trên GitHub lỗi do môi trường | Claude đọc log và sửa; đã gặp 1 lỗi (thiếu FFmpeg) và đã sửa |
| Repo công khai làm lộ nội dung | Quyết định ở 0.4; không bao giờ đưa thông tin khách, thu nhập, khóa vào repo |
| Phụ đề/giọng tiếng Việt sai tên và số | Hào duyệt lại bước 2.4 |
| Mất thời gian hoàn thiện công cụ thay vì đăng video | Mỗi giai đoạn kết thúc bằng một video đã đăng, không chỉ mã |

## 8. Cách đo thành công
- Số video đã đăng mỗi tuần (mục tiêu 1–2).
- Thời gian từ chọn chủ đề đến đăng (mục tiêu dưới 2 giờ sau V1.2).
- Số tin nhắn hoặc cuộc hẹn từ đúng nhóm khách mục tiêu sau mỗi bài.
- Chưa đặt mục tiêu doanh thu vì chưa có dữ liệu cơ sở.

## 9. Việc cần Hào quyết định trước 14/11
1. Mỗi ngày dành được bao nhiêu giờ cho dự án?
2. Giọng đọc: tự thu hay giọng AI?
3. Repo để công khai hay riêng tư?
4. Chủ đề video đầu tiên (một câu), và Hào có sẵn số liệu có nguồn cho dự án đó chưa?
5. Logo Hào Sky Land: có file chưa?
