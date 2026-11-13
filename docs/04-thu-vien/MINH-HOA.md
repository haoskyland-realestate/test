# Video giải thích bằng tranh minh hoạ (explainer)

Lập 13/11/2026 từ video mẫu Hào gửi (98 giây, chỉ lưu phân tích, không lưu video). Trạng thái: **phân tích + bộ câu lệnh thử phong cách; chưa code**.

## 1. Video mẫu làm thế nào
- 95 giây tranh minh hoạ chạy theo lời đọc, 3 giây cuối người thật nói lời kêu gọi.
- **Một bối cảnh cho cả video** (góc phòng nền giấy, bóng nắng chéo). Không đổi cảnh, chỉ "lia máy" trong cùng căn phòng, các cảnh mờ chồng sang nhau. Máy dò cắt cảnh gần như không thấy lần cắt nào.
- **Khoảng 20 đồ vật cắt rời dùng đi dùng lại** (túi, loa, kính lúp, cân, la bàn, điện thoại…). Kiểu xuất hiện: bật nảy, vẽ nét dần, trượt vào, nhún.
- **Mỗi ý trừu tượng thành một đồ vật**: "đánh giá" là kính lúp, "trọng số" là cái cân, "lan truyền" là cái loa.
- **2–3 giây một ý hình**, khớp từ khoá trong lời đọc.
- **Chữ 2–4 từ in hoa đậm**: đỏ cho rủi ro hoặc câu gây chú ý, màu chính cho thông tin. Nhãn nhỏ ở góc trên, con số to.
- Âm thanh: lời đọc liền mạch, âm lượng −19,6 LUFS. Bản của mình chuẩn −14 cho TikTok.

## 2. Hướng làm cho Hào Sky Land
**Không** dùng Flow tạo từng cảnh của từng video. Lý do: tốn lượt tạo, phong cách lệch giữa các clip, chữ tiếng Việt hay sai, khó khớp lời đọc.
**Làm một lần bộ tài sản, dùng mãi:**
1. **Bộ bối cảnh** (3–5 ảnh nền dọc 9:16) và **bộ đạo cụ BĐS** (20–30 món) tạo bằng Flow. Tách nền (nút xoá nền của Canva, hoặc Claude tách nền phẳng bằng OpenCV). Lưu vào kho `10_THUONG-HIEU/hao-sky-land/minh-hoa/` (`boi-canh/`, `dao-cu/`), tên theo ý nghĩa: `heo-dat_tiet-kiem_01.png`.
2. **Hệ thống HSL tự làm chuyển động** (lớp chữ HTML đang có): đạo cụ bật nảy hoặc vẽ nét, lia máy, chữ khoá đúng lúc nói (lấy mốc từ phụ đề).
3. **Skill `minh-hoa`** (chưa làm): Claude đọc `KICH-BAN.md`, chia nhịp 2–3 giây, mỗi nhịp chọn một đạo cụ theo ý câu nói và đặt chữ khoá, xuất bảng storyboard để Hào duyệt, rồi dựng.
4. **Mẫu `minh-hoa-01`** trong thư viện mẫu, kết thúc 3–5 giây Hào nói trước máy.
5. Flow tạo clip chỉ dùng cho 1–2 cảnh đặc biệt mỗi video, nếu cần.

**Giọng đọc:** Hào tự thu, hoặc Voice Studio (`GIONG-NOI-AI.md`). Hệ thống nhận file giọng nào cũng được. Phụ đề và mốc chữ lấy từ giọng đó.
**Không chép phong cách hay đồ vật của kênh mẫu.** Bộ của mình dùng bảng màu riêng (mục 3).

## 3. Thử phong cách (bước 1, Hào làm trong Flow)

**Ngân sách Flow Pro (1.000 credit/tháng):** theo trang Google, Veo 3.1 Fast tốn 20 credit mỗi clip, bản Quality 100 credit. Giá tạo ảnh chưa thấy công bố: xem số credit Flow hiện trước khi bấm tạo. Nguồn: [Manage your Google Flow credits](https://support.google.com/flow/answer/16526234).

**Mẹo đồng nhất:**
- Tạo bối cảnh trước.
- Lấy ảnh bối cảnh ưng nhất làm **ảnh tham chiếu (ingredient / reference)** cho mọi đạo cụ sau.
- Câu "khoá phong cách" giữ y nguyên trong mọi câu lệnh.
- Mỗi câu lệnh tạo 2–4 bản rồi chọn một.

**Câu khoá phong cách (chép vào cuối mọi câu lệnh):**
```
Style: flat paper-cutout collage illustration, matte gouache texture with subtle paper grain, soft natural window light from the upper left, gentle long diagonal shadows, calm minimal composition, muted palette of warm off-white, deep forest green, brass gold and soft charcoal, premium real-estate mood. No text, no letters, no numbers, no logos, no people.
```

**Bối cảnh (1 ảnh, dọc 9:16):**
```
Vertical 9:16 illustration of an empty corner of a modern luxury living room: warm off-white walls, a deep green skirting band, a light oak floor, a long low marble counter in the lower third, a tall window casting diagonal sunlight across the wall. The upper half of the frame is calm empty wall space (room for headline text). No furniture in the center. [câu khoá phong cách]
```

**5 đạo cụ thử (mỗi món một ảnh vuông 1:1, nền phẳng để dễ tách):**
```
1. A small model house with a pitched roof and a lit window
2. A single brass house key with a round green key tag
3. A ceramic piggy bank in deep forest green with a gold coin above the slot
4. A brass balance scale with two pans, slightly tilted
5. A brass hourglass with warm sand flowing
Mỗi món thêm: "Single object, centered, isolated on a perfectly flat plain light grey background (#E9E9E9), soft contact shadow under it, 3/4 view, nothing else in the frame." + [câu khoá phong cách]
```

**Gửi Claude:** ảnh bối cảnh và 5 đạo cụ ưng nhất. Claude ghép thử một cảnh 3 giây (bối cảnh, heo đất bật vào, chữ "DÒNG TIỀN" đúng lúc nói) để chốt phong cách, rồi mới làm đủ bộ và code.

## 4. Đạo cụ BĐS dự kiến cho bộ đầy đủ (20–30 món)
nhà, chìa khoá, heo đất, cân, đồng hồ cát, máy tính bỏ túi, lịch (kỳ trả nợ), biểu đồ tăng, biểu đồ giảm, kính lúp, la bàn, ngân hàng, túi tiền, cái ô (phòng rủi ro), bản đồ có ghim, xe hơi, trường học, cây xanh, mặt trời/biển (nghỉ dưỡng), cầu thang (từng bước), dấu hỏi, dấu tích, tấm khiên, hộp quà (chính sách: chỉ khi có nguồn).
**Không vẽ giấy tờ pháp lý giả** (sổ hồng, hợp đồng, con dấu).
