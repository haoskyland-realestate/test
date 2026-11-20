# Phân tích 30 video gần nhất của @lamphatlong (lấy ngày 20/11/2026)

Phương pháp: `outlier-post-finder` (mức nền = trung vị 24.650 lượt xem) + `transcript-intelligence` (hook, cấu trúc, CTA). Dữ liệu lấy bằng `yt-dlp` và Whisper, không dùng API ScrapeCreators.

Giới hạn: lời thoại chỉ **90 giây đầu** mỗi video, phiên âm tự động nên có chỗ sai chữ (tên dự án, tên riêng hay sai). 2 video không nhận ra lời (#23 dài 27s, #28). Chưa có dữ liệu giữ chân, bình luận, hay chuyển đổi ra khách. Nhóm hook dưới đây là cách em tự xếp loại, mẫu nhỏ, chỉ để tham khảo.

## TL;DR
- **Hook mở bằng câu hỏi, hiểu lầm hoặc số liệu thị trường** có lượt xem tốt nhất: trung vị **36.650** (6 video). Mở bằng **giới thiệu sản phẩm/tiện ích** thấp nhất: trung vị **10.200** (9 video). Mở bằng **con số tiền/chính sách thanh toán**: trung vị 26.400 nhưng chênh lệch rất lớn (15.300 đến 148.500).
- Video cao nhất (148.500, gấp 6 lần mức nền) kết hợp con số tiền với tương phản "rất ít khi được nghe". Chỉ có một video như vậy nên chưa thể coi là quy luật.
- Chuỗi "TT Genesis" (3 tập) thấp nhất kênh (3.000–5.700). Chuỗi "VinHolm Saigon Park" thì khá (37.300 và 45.900). Nên vấn đề nhiều khả năng nằm ở hook và đề tài, không ở chuyện làm nhiều tập.
- Video dài 2–4 phút vẫn có lượt xem cao; video ngắn nhất có lời (87s, #9) chỉ 17.200.

## Video nổ (từ 2 lần mức nền)
| # | Xem | Gấp | Hook (nguyên văn, có thể sai chữ nhẹ) | Link |
|---|---|---|---|---|
| 19 | 148.500 | 6,0x | "Thanh toán 10 triệu trên 1 tháng để sở hữu một căn hộ là quá bình thường… Nhưng thanh toán chỉ từ 10 triệu trên 1 tháng để sở hữu một căn hộ cao cấp, ven sông và có bến du thuyền thì thực sự rất ít khi được nghe." | [link](https://www.tiktok.com/@lamphatlong/video/7677426643627019528) |
| 24 | 105.200 | 4,3x | "Mọi người có để ý một thực trạng rất phổ biến hiện nay: có nhiều căn shop house đơn lẻ nằm trên mặt tiền đường lớn, giá trị không nhỏ nhưng bên trong thì rất vắng khách…" | [link](https://www.tiktok.com/@lamphatlong/video/7667091824150088980) |
| 8 | 94.500 | 3,8x | "Thành phố Hồ Chí Minh có tới 9 triệu dân trên 2.095 km², mật độ khoảng 4.300 người/km²…" rồi dẫn tới câu hỏi "người mua sẽ di chuyển đi đâu?" và "hiệu ứng vết dầu loang" | [link](https://www.tiktok.com/@lamphatlong/video/7698316816195620104) |
| 1 | 69.100 | 2,8x | "Tại sao dòng tiền từ Biên Hòa, Đồng Nai, Vũng Tàu cho đến Cần Thơ lại đang được đổ về Cần Giờ?" | [link](https://www.tiktok.com/@lamphatlong/video/7707646473688714516) |

## Các mẫu lặp lại
| Mẫu | Bằng chứng | Ví dụ |
|---|---|---|
| Câu hỏi "tại sao…?" hoặc nêu hiểu lầm rồi giải thích | #1 (69.100), #21 hiểu lầm Nghị quyết 21 (32.800), #3 so sánh vàng/tiết kiệm/chứng khoán (33.700) | #1, #21 |
| Mở bằng số liệu thị trường rồi dẫn tới một câu hỏi | #8 (94.500), #7 (39.600) | #8 |
| Nêu một thực trạng người xem tự thấy được | #24 shop house vắng khách (105.200) | #24 |
| Con số thanh toán/tiền ở dòng đầu | #19 (148.500), #17 18 triệu/tháng (26.400), #26 "từ 4x triệu/m²" (32.000), #9 (17.200), #18 (15.300) | #19 |
| "Tự chê dự án" (3 điểm chưa hợp) | #6 (28.400), quanh mức nền | #6 |
| Mở bằng tên dự án và liệt kê tiện ích | #12, #14, #15, #25, #27, #5, #10, #16, #30: thấp hơn mức nền ở 7/9 video | #14 (2.978) |
| Mở bằng câu chuyện cảm xúc / không liên quan sản phẩm | #20 tháng 7 âm lịch (18.500), #27 (6.357) | #27 |

## Cấu trúc thường gặp (từ 90 giây đầu)
Hook (1–2 câu) → nêu vấn đề/số liệu → "mời mọi người cùng Long xem hết video" → 3 ý được đánh số ("thứ nhất, thứ hai, thứ ba") → tên dự án và chi tiết. Câu "xem hết video này nhé" xuất hiện ở #16, #21, #22, #26.

## Điều rút ra cho video của Hào
- Kiểu hook "tại sao dòng tiền đang đổ về…" hợp với góc dòng tiền của Hào. Dữ kiện (tuyến metro, ngày duyệt, mốc thông xe) phải có nguồn và ngày cập nhật mới dùng, vì kênh này nói các mốc rất cụ thể mà em không kiểm chứng.
- Hook số tiền như "chỉ từ 10 triệu/tháng" dễ gây hiểu nhầm về áp lực tài chính. Nếu dùng, phải nêu điều kiện (thời gian, vay hay không) và nguồn.
- #9 dùng "chỉ áp dụng cho 100 khách đầu tiên". Hào không nên bắt chước kiểu khan hiếm này khi chưa có căn cứ.
- #24 là dự án ở Hà Nội. Với Hào, nên học cách mở bằng một thực trạng ai cũng thấy, không học nội dung.

## Kho hook (dùng để học cấu trúc, không chép nguyên văn)
Khuôn mẫu, phần trong ngoặc vuông Hào tự điền khi đã có nguồn:
- "Tại sao dòng tiền từ [khu vực A], [khu vực B] lại đang đổ về [dự án/khu vực]?"
- "[Số tiền/tháng] để sở hữu [loại căn] ở [vị trí] là chuyện bình thường. Nhưng kèm [điểm khác biệt] thì ít khi nghe."
- "Nhiều người nghĩ [lầm tưởng]. Thực ra [sự thật có nguồn]."
- "Mọi người có để ý [thực trạng ai cũng thấy] không?"
- "[Số liệu thị trường có nguồn]. Vậy người mua sẽ đi đâu?"

## Ý tưởng chuyển thể (chỉ là bản nháp ý, chưa phải kịch bản)
- Video 60–90s: một "tại sao dòng tiền…" cho Vinhomes Hóc Môn hoặc Cần Giờ, có nguồn và ngày cho từng mốc hạ tầng.
- Video "hiểu lầm vs sự thật" về một chính sách pháp lý (kiểu #21), cần văn bản gốc làm nguồn.
- Video so sánh dòng tiền hàng tháng sau khi trừ tiền vay, theo khuôn #18 nhưng nêu cả rủi ro lãi suất.

Chưa làm: lời thoại đầy đủ (chỉ có 90 giây đầu), CTA cuối video (đa số video chưa nghe tới đoạn cuối), phân tích bình luận.
