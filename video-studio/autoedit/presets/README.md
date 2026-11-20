# Thư viện preset
Mỗi preset là một cách trình bày trọn bộ. Người dùng chỉ cần gọi tên: "dùng preset A".
- A `xanh_gradient`: xanh sáng, người nói tách nền, đầu nhô khỏi khung.
- B `cam_kem`: cam đất, hai khung, không tách nền.
- C `neon_toi`: đen neon, đồ họa toàn khung, người nói vòng tròn.
Thêm preset mới: sao chép một file làm khuôn, đổi tên, sửa màu, bố cục, motion và bảng "Kịch bản mẫu 30 giây", rồi thêm một dòng vào bảng ở "Bước 0" trong `CLAUDE.md`.


Token nền dùng chung: mỗi preset khai báo `--orb1` (màu chính) và `--orb2` (màu sáng) cho hai đốm màu mờ ở nền (xem CLAUDE.md mục 4, "NỀN CHUNG"). Đổi màu nền toàn bộ hiệu ứng chỉ cần đổi hai giá trị này.
