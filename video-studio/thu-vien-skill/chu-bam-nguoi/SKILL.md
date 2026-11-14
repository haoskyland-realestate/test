---
name: chu-bam-nguoi
description: Chữ bám theo người nói: đặt chữ ngang ngực/đầu người, di chuyển theo khi người đi. Dùng khi Hào nói "chữ bám theo người", "tracking".
---

# Chu bam nguoi (MỘT PHẦN)

Quan sát từ video mẫu (Open Residency, Hào gửi 14/11/2026; chỉ học cấu trúc và nhịp, không chép nguyên đồ hoạ): Mẫu: chữ nằm sát người nói trong mọi cảnh, đổi chỗ theo từng cảnh; thẻ tên bám bên cạnh.

## Cách làm
1. Tách người từng khung (MODNet qua `scripts/tach_nguoi.py`), tính tâm và đỉnh đầu, làm mượt.
2. Đưa đường đi vào GSAP (keyframe x, y) cho khối chữ.
3. Người ra khỏi khung: chữ về vị trí mặc định.

## Đã có trong repo
`--ngang-nguc` (`loi_nhip.py`, `dung.py: dinh_dau_tai`): đặt chữ ngang ngực theo vị trí đầu TẠI LÚC CỤM BẮT ĐẦU; chữ sau đầu (`sau_dau`).

## Còn thiếu
Bám từng khung hình (đường đi x, y theo thời gian); mặt nạ cho cảnh đông người; tốc độ tách người trên Mac.

## Quy tắc
Đọc `docs/04-thu-vien/GHI-NHO-NGHIEM-THU.md` trước khi dựng. Dữ kiện dự án phải có nguồn và ngày. Chưa chạy thử thì ghi "chưa thử". Hào duyệt trước khi tải tài nguyên mới hoặc tốn chi phí.
