# Bảng master dựng

Sinh tự động từ `video-studio/cau-hinh/master.json` bằng `python scripts/bang_master.py --md`. Đừng sửa tay file này.

- **Chỉnh:** app studio → ⚙ Bảng master (Lưu chung hoặc riêng dự án), hoặc bản xem artifact → "Sao chép thay đổi" → dán cho Claude, hoặc nói thẳng "chỉnh X thành Y".
- **Thứ tự ưu tiên:** ghi đè riêng dự án (`timeline.json` → `meta.cau_hinh`) > bảng chung (`mac_dinh`).
- **Kiểm:** giá trị ngoài khoảng hoặc id gõ nhầm bị chặn (`timeline.check`, máy chủ app, `cau_hinh.py --tu-kiem`).

## Cắt & nhịp nghỉ (`cat`)

Master cut tự cắt khoảng lặng, tiếng đệm, lần nói vấp. Nhịp nghỉ quyết định video nghe dồn dập hay thong thả.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Lặng dài hơn thì cắt | `cat.lang_cat` | 0.3 | 0.3 | 0.1–1.5 giây | master_cut.py | Khoảng lặng giữa hai từ dài hơn mức này (và đo âm lượng thấy im thật) thì cắt bỏ. Tăng: giữ nhiều chỗ nghỉ, nghe chậm, tự nhiên. Giảm: dồn dập kiểu TikTok nhưng dễ mất hơi thở. Người dựng chuyên nghiệp thường 0,25–0,4s. |
| Chừa trước khi nói | `cat.chua_truoc` | 0.08 | 0.08 | 0.0–0.4 giây | master_cut.py | Giữ lại một chút trước tiếng đầu tiên của mỗi mẩu để không mất phụ âm đầu. Dưới 0,05s dễ nghe cụt chữ. |
| Chừa sau lời (giữa câu) | `cat.chua_sau` | 0.14 | 0.14 | 0.0–0.6 giây | master_cut.py | Giữ lại sau tiếng cuối của mẩu khi câu chưa hết. Quá ngắn nghe hụt hơi, quá dài nghe lề mề. |
| Chừa sau cuối câu | `cat.chua_cuoi_cau` | 0.3 | 0.3 | 0.0–1.0 giây | master_cut.py | Nhịp nghỉ sau dấu chấm/hỏi. Đây là chỗ người xem 'thở'; 0,3–0,45s là chuẩn cho talking head. |
| Mẩu ngắn hơn thì bỏ | `cat.manh_ngan` | 0.35 | 0.35 | 0.1–1.5 giây | master_cut.py | Mẩu còn lại ngắn hơn mức này (và không có chữ) thì bỏ, tránh hình chớp nháy. |
| Tiếng đệm tự cắt | `cat.tieng_dem` | ờ, ơ, à, ừ, ừm, ừa, hmm, um, uh, ầy | ờ, ơ, à, ừ, ừm, ừa, hmm, um, uh, ầy |  | master_cut.py | Từ đứng riêng được coi là tiếng đệm và cắt bỏ khi master cut. |
| Ngưỡng tiếng nói: trên nền ồn | `cat.nen_cong_db` | 10 | 10 | 3–25 dB | master_cut.py | Ngưỡng coi là có tiếng = mức nền ồn + số dB này. Phòng ồn thì tăng để không coi tiếng ồn là lời nói. |
| Ngưỡng tiếng nói: dưới mức to | `cat.to_tru_db` | 6 | 6 | 2–20 dB | master_cut.py | Ngưỡng không cao quá mức to (90%) trừ số dB này. Giọng nhỏ, đều thì tăng. |
| Từ kéo dài bất thường | `cat.tu_keo_dai` | 0.6 | 0.6 | 0.3–2.0 giây | master_cut.py | Máy nghe hay kéo dài từ đứng sau chỗ ngập ngừng; từ dài hơn mức này thì đo lại điểm bắt đầu bằng âm lượng. |
| Lần nói lại: tìm trong | `cat.lap_cach_giay` | 15 | 15 | 3–60 giây | master_cut.py | Tìm lần nói vấp (cụm ≥ 3 từ nói lại) trong khoảng này trước lần nói sau. |
| Lần nói lại: phải có ngập ngừng | `cat.lap_lang_toi_thieu` | 0.4 | 0.4 | 0.1–2.0 giây | master_cut.py | Chỉ coi là nói lại (bỏ lần đầu) khi trước lần sau có ngập ngừng ít nhất chừng này; nói liền mạch là cố ý. |

## Phân tích lời nói (`phan_tich`)

Bảng phân tích trong storyboard và câu hỏi Cổng 1 của agent: chỉ báo/đề xuất, không tự cắt.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Ngập ngừng giữa câu | `phan_tich.ngap_ngung` | 0.6 | 0.6 | 0.2–2.0 giây | phan_tich_loi.py | Lặng giữa câu (từ trước không có dấu câu) dài hơn mức này thì báo 'nói vấp'. |
| Lặng coi như hết câu | `phan_tich.het_cau` | 0.7 | 0.7 | 0.3–3.0 giây | phan_tich_loi.py | Lặng dài hơn mức này thì coi như sang câu mới (để đo tốc độ nói từng câu). |
| Tiếng đệm cần báo | `phan_tich.tieng_dem` | ờ, ừ, ừm, ơ, à, hmm, ừa, ờm, ê | ờ, ừ, ừm, ơ, à, hmm, ừa, ờm, ê |  | phan_tich_loi.py | Từ đứng riêng được báo là tiếng đệm trong bảng phân tích. |
| Câu lặp: cho cách tối đa | `phan_tich.lap_cach` | 2 | 2 | 0–6 từ | phan_tich_loi.py | Cụm ≥ 3 từ nói lại, cho phép chen giữa tối đa chừng này từ (cụm ngắn hơn phải liền nhau). |
| Nói nhanh khi gấp | `phan_tich.nhanh` | 1.3 | 1.3 | 1.05–2.0 lần | phan_tich_loi.py | Câu nói nhanh hơn nhịp riêng của người nói chừng này lần thì báo 'nói nhanh'. |
| Nói chậm khi dưới | `phan_tich.cham` | 0.7 | 0.7 | 0.3–0.95 lần | phan_tich_loi.py | Câu chậm hơn nhịp riêng xuống dưới chừng này lần thì báo 'nói chậm'. |
| Cảnh ngắn hơn thì báo | `phan_tich.canh_ngan` | 1.0 | 1.0 | 0.2–3.0 giây | phan_tich_loi.py | Cảnh nhìn thấy ngắn hơn mức này bị báo 'như chớp'. |
| Cảnh dài hơn thì báo | `phan_tich.canh_dai` | 7 | 7 | 3–30 giây | phan_tich_loi.py | Cảnh dài hơn mức này bị báo 'nên chèn cảnh trám/zoom/chữ' (người xem dễ lướt). |

## Zoom (`zoom`)

Phóng nhẹ xen kẽ ở chỗ cắt nhảy và mẩu nói dài để hình không đứng yên.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Mức phóng xen kẽ | `zoom.phong` | 1.05 | 1.05 | 1.0–1.15 lần | master_cut.py | Cỡ khung khi phóng (1,05 = 105%). Hào chốt tối đa 104–106%; lớn hơn dễ vỡ hình 1080 và lộ giật. |
| Đổi cỡ khung mỗi | `zoom.nhip` | 4.0 | 4.0 | 2.0–10.0 giây | master_cut.py | Mẩu nói dài thì đổi cỡ khung khoảng mỗi chừng này giây, ở chỗ ngắt giữa hai từ. |

## Nhận dạng giọng (`giong`)

Máy nghe (Whisper) viết lời từ giọng nói, có mốc từng từ.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Mô hình | `giong.mo_hinh` | large-v3-turbo | large-v3-turbo | large-v3-turbo/large-v3/medium/small | phu_de.py | large-v3-turbo: chính xác, nhanh vừa (PC có card thì nhanh). small/medium: nhanh hơn nhưng nghe sai nhiều tên riêng. Biến môi trường WHISPER_MODEL nếu đặt thì thắng. |
| Độ kỹ khi nghe (beam) | `giong.beam` | 5 | 5 | 1–10 | phu_de.py | Số hướng thử khi đoán chữ. Cao hơn: kỹ hơn, chậm hơn. |
| Bỏ qua đoạn không tiếng | `giong.vad` | bật | bật |  | phu_de.py | Lọc khoảng lặng trước khi nghe, giảm câu bịa ở đoạn im. |
| Hỏi Hào khi độ tin cậy dưới | `giong.nguong_tin` | 0.6 | 0.6 | 0.3–0.95 | agent.py | Từ máy nghe với độ tin cậy dưới mức này thì agent hỏi Hào ở Cổng 1. |

## Phụ đề (`phude`)

Phụ đề dòng (kiểu cũ) tự sinh từ giọng.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Tối đa từ mỗi dòng | `phude.tu_toi_da` | 7 | 7 | 3–14 từ | phu_de.py |  |
| Tối đa giây mỗi dòng | `phude.giay_toi_da` | 2.8 | 2.8 | 1.0–6.0 giây | phu_de.py |  |
| Ngừng nói thì xuống dòng | `phude.nghi` | 0.45 | 0.45 | 0.15–1.5 giây | phu_de.py |  |

## Chữ theo nhịp nói (`loi`)

Từng từ hiện đúng lúc nói, gom thành cụm ngang ngực người nói. Mẫu edit có thể ghi đè cỡ/màu.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Nghỉ thì sang cụm mới | `loi.nghi_cum` | 0.4 | 0.4 | 0.15–1.5 giây | loi_nhip.py | Nghỉ giữa hai từ dài hơn mức này thì bắt đầu cụm chữ mới. |
| Tối đa từ mỗi cụm | `loi.tu_toi_da` | 5 | 5 | 2–8 từ | loi_nhip.py | Cụm dài hơn khó đọc trên điện thoại; 3–5 là chuẩn. |
| Cỡ chữ (mặc định) | `loi.co` | 62 | 62 | 36–96 px | lop_chu.py | Cỡ chữ thường trên khung 1080; tự thu nhỏ cho vừa vùng an toàn. Mẫu edit có thể đặt riêng. |
| Từ khoá to hơn | `loi.co_khoa` | 1.9 | 1.9 | 1.0–3.0 lần | lop_chu.py | Từ khoá to gấp chừng này lần chữ thường (tự thu cho vừa). |
| Hiện sớm | `loi.som` | 0.6 | 0.6 | 0.0–1.0 | lop_chu.py | Chữ bắt đầu chuyển động sớm chừng này phần thời lượng chuyển động, để rõ đúng lúc vừa nói (Hào: chữ hiện chậm). |
| Độ chậm chuyển động chữ | `loi.cham_chu` | 1.5 | 1.5 | 0.6–2.5 lần | lop_chu.py | Nhân thời lượng mọi chuyển động chữ/thẻ (ease in-out). Mẫu edit có thể đặt riêng (meta.cham_chu). |
| Chữ không cao hơn | `loi.vung_tren` | 0.3 | 0.3 | 0.15–0.6 | lop_chu.py | Mép trên cụm chữ không cao hơn chừng này chiều cao khung. |

## Chữ lớn & thẻ (`the`)

Thời lượng chữ lớn (hook, tiêu đề) và cảnh chèn thẻ do bản dựng đặt.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Chữ lớn hiện tối thiểu | `the.chu_lon_min` | 1.8 | 1.8 | 0.8–5.0 giây | ban_dung.py |  |
| Chữ lớn còn lại sau lời | `the.chu_lon_them` | 0.8 | 0.8 | 0.0–3.0 giây | ban_dung.py | Giữ thêm sau khi nói xong cụm chữ lớn, để kịp đọc. |
| Thẻ số liệu tối thiểu | `the.so_lieu_min` | 2.0 | 2.0 | 1.0–6.0 giây | ban_dung.py |  |
| Thẻ số liệu còn lại sau lời | `the.so_lieu_them` | 0.6 | 0.6 | 0.0–3.0 giây | ban_dung.py |  |
| Thẻ danh sách/sơ đồ tối thiểu | `the.the_min` | 3.0 | 3.0 | 1.5–8.0 giây | ban_dung.py |  |
| Thẻ danh sách/sơ đồ còn lại sau lời | `the.the_them` | 0.6 | 0.6 | 0.0–3.0 giây | ban_dung.py |  |

## Âm thanh (`am`)

Độ to chuẩn mạng xã hội, nhạc nền tự nhỏ khi nói, làm sạch giọng.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Độ to chuẩn (LUFS) | `am.lufs` | -14 | -14 | -23–-9 LUFS | dung.py | TikTok/YouTube/Instagram chuẩn −14. Thấp hơn (−16) mềm hơn; cao hơn dễ bị nền tảng hạ xuống. |
| Đỉnh tối đa | `am.dinh` | -1.5 | -1.5 | -6–-0.5 dBTP | dung.py | Không cho đỉnh vượt mức này để không vỡ tiếng trên điện thoại. |
| Độ chênh to/nhỏ (LRA) | `am.lra` | 11 | 11 | 5–20 LU | dung.py | Nhỏ: giọng đều đều; lớn: giữ biểu cảm. |
| Nhạc nền khi có giọng | `am.nhac_co_giong` | 0.35 | 0.35 | 0.05–1.0 lần | dung.py | Âm lượng nhạc nền (so với gốc) khi video có giọng nói, trước khi tự nhỏ thêm lúc đang nói. |
| Nhạc tự nhỏ: ngưỡng giọng | `am.duck_nguong` | 0.02 | 0.02 | 0.005–0.2 | dung.py | Giọng to hơn mức này thì nhạc bắt đầu nhỏ xuống. |
| Nhạc tự nhỏ: mức nén | `am.duck_ti_le` | 8 | 8 | 1–20 :1 | dung.py | Càng cao nhạc càng nhỏ khi nói. |
| Nhạc tự nhỏ: tốc độ vào | `am.duck_vao` | 15 | 15 | 1–200 ms | dung.py |  |
| Nhạc tự nhỏ: tốc độ trả lại | `am.duck_nha` | 400 | 400 | 50–2000 ms | dung.py | Ngắn: nhạc bật lại nhanh giữa các câu (dễ 'phập phồng'); dài: êm hơn. |
| Làm sạch giọng: cắt ù dưới | `am.sach_cat_tram` | 80 | 80 | 40–200 Hz | dung.py | Bỏ tiếng ù, gió dưới tần số này. |
| Làm sạch giọng: mức khử ồn | `am.sach_khu_on` | -25 | -25 | -50–-10 dB | dung.py | Mức nền ồn cần khử (càng gần 0 khử càng mạnh, dễ méo giọng). |
| Làm sạch giọng: nén | `am.sach_nen` | 2.5 | 2.5 | 1–8 :1 | dung.py | Nén cho giọng đều. |
| Làm sạch giọng: vùng rõ chữ | `am.sach_nang_hz` | 3500 | 3500 | 1500–6000 Hz | dung.py |  |
| Làm sạch giọng: nâng vùng rõ chữ | `am.sach_nang_db` | 2 | 2 | 0–6 dB | dung.py |  |

## Hình & xuất (`hinh`)

Chất lượng và tốc độ dựng.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Khung/giây | `hinh.fps` | 30 | 30 | 24–60 | dung.py |  |
| Chất lượng cắt cảnh bản cuối (CRF) | `hinh.crf_cuoi` | 18 | 18 | 12–28 | dung.py | Càng nhỏ càng nét, file càng to. 16–20 là mức xuất bản. |
| Chất lượng bản nháp/xem (CRF) | `hinh.crf_nhap` | 28 | 28 | 20–36 | dung.py |  |
| Chất lượng ghép cuối (CRF) | `hinh.crf_ghep` | 19 | 19 | 12–28 | dung.py |  |
| Chất lượng bản nhẹ 540p (CRF) | `hinh.nhe_crf` | 23 | 23 | 18–32 | ban_nhe.py | Bản nhẹ dùng để phân tích và bản xem. |
| Phân tích: khung/giây | `hinh.phan_tich_fps` | 5 | 5 | 1–15 | phan_tich_hinh.py | Chấm điểm hình bao nhiêu khung mỗi giây. |
| Tự cân màu từng cảnh | `hinh.tu_can_mau` | bật | bật |  | dung.py | Tắt nếu muốn giữ màu gốc (cảnh dùng LUT chỉnh màu luôn bỏ qua tự cân). |

## Vùng an toàn (`vung`)

Giao diện TikTok/Reels/Shorts che các mép; chữ, thẻ phải nằm trong (chuẩn AutoEdit).

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Chừa trên | `vung.tren` | 0.15 | 0.15 | 0.05–0.3 chiều cao | kiem_vung.py |  |
| Mép dưới chữ không thấp hơn | `vung.duoi` | 0.75 | 0.75 | 0.6–0.9 chiều cao | kiem_vung.py | 0,75 = chừa 25% dưới cho chú thích và nút của TikTok. |
| Chừa hai bên | `vung.ben` | 0.1 | 0.1 | 0.03–0.2 chiều ngang | kiem_vung.py | Nút thả tim/bình luận nằm ở mép phải. |

## Kiểm bản cuối (`kiem`)

Ngưỡng để kiem_cuoi.py báo lỗi trước khi giao video.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Lệch độ to cho phép | `kiem.lufs_lech` | 1.0 | 1.0 | 0.3–3.0 LU | kiem_cuoi.py |  |
| Lệch hình–tiếng cho phép | `kiem.hinh_tieng` | 0.1 | 0.1 | 0.02–0.5 giây | kiem_cuoi.py |  |
| Lệch độ dài cho phép | `kiem.do_dai` | 0.15 | 0.15 | 0.03–1.0 giây | kiem_cuoi.py |  |

## Agent (`agent`)

Lựa chọn mặc định khi chạy agent.py.

| Thông số | Id | Hiện tại | Gốc | Khoảng | Dùng ở | Giải thích |
|---|---|---|---|---|---|---|
| Preset AutoEdit mặc định | `agent.preset` | A | A | A/B/C | agent.py | A xanh gradient · B cam kem · C neon tối (hiện quyết định ảnh mẫu trang chọn hiệu ứng). |
| Mẫu edit mặc định | `agent.mau` | talking-luxury-01 | talking-luxury-01 |  | agent.py | Thư mục trong thu-vien-mau/ (id mẫu). |

