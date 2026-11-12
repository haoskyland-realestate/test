# Thư viện hiệu ứng v1

Tự sinh từ `video-studio/scripts/effects.py`. Dùng tên ở cột đầu trong `timeline.json`.

## Phong cách (`meta.style`)
| Tên | Mô tả |
|---|---|
| `hien-dai` | Hiện đại: chữ đậm không chân, vàng nhấn, nhịp nhanh (giống video test đã duyệt) |
| `sang-trong` | Sang trọng: navy + vàng champagne, tiêu đề chữ có chân, chuyển động chậm, màu ấm có viền tối |
| `toi-gian` | Tối giản: đen trắng, một màu nhấn nhạt, chữ mảnh, hiện mờ dần, màu nhạt |

## Chỉnh màu (`look` của từng cảnh, mặc định theo phong cách)
| Tên | Mô tả |
|---|---|
| `trung-tinh` | Trung tính, tăng nhẹ tương phản và độ rực |
| `am-sang` | Ấm sang: ấm nhẹ, bớt rực, viền tối, hạt phim nhẹ |
| `mat-hien-dai` | Mát hiện đại: xanh nhẹ, tương phản cao |
| `nhat-toi-gian` | Nhạt tối giản: sáng, ít màu, ít tương phản |

## Chuyển cảnh (`transitions[].type`, đổi độ dài bằng `dur`)
| Tên | Mặc định | Mô tả |
|---|---|---|
| `cut` | 0.0s | Cắt thẳng (mặc định, dùng nhiều nhất) |
| `cube-h` | 0.8s | Khối 3D xoay ngang: sang chương mới |
| `cube-v` | 0.8s | Khối 3D xoay dọc: sang chương mới |
| `flip` | 0.8s | Lật thẻ 3D: đổi phương án, so sánh |
| `fade` | 0.5s | Hòa tan: đổi thời gian, cảm xúc chậm |
| `dip` | 0.6s | Tối dần rồi sáng: mở/kết chương |
| `zoom` | 0.5s | Phóng xuyên: từ xa vào gần, ngoài vào trong |
| `slide` | 0.4s | Trượt ngang: danh sách, từng mục |
| `wipe` | 0.5s | Quét ngang: tối giản |
| `circle` | 0.6s | Mở vòng tròn: tiết lộ, nhấn mạnh |

## Hiệu ứng chữ (`texts[].anim`, mặc định theo phong cách)
| Tên | Mô tả |
|---|---|
| `rise` | Từng từ trượt lên, mờ → rõ |
| `mask` | Từng dòng trồi lên từ sau mép (sang trọng) |
| `blur` | Từng từ hiện từ mờ nhòe, không di chuyển (tối giản) |
| `pop` | Từng dòng phóng nhẹ 118% → 100% (hook) |
| `track` | Chữ giãn rộng rồi thu về (tiêu đề sang trọng) |
| `type` | Gõ từng ký tự (phân tích, tin nhanh) |

## Khối chữ (`texts[].kind`)
| Tên | Trường bắt buộc | Mô tả |
|---|---|---|
| `hook` | tag, lines | Mở đầu: thẻ nhãn + câu lớn |
| `section` | num, title, lines | Mục số viền + tiêu đề có thanh nhấn |
| `line` | lines | Một hai dòng chữ lớn |
| `outro` | lines | Cảnh kết thương hiệu (có thể thêm 'note') |
| `lower` | title | Thanh tiêu đề dưới màn hình (thêm 'sub' cho dòng phụ) |
| `quote` | lines | Câu trích lớn có dấu ngoặc (thêm 'by' cho người nói) |
| `source` | text | Thẻ nguồn nhỏ, bắt buộc khi có số liệu: 'Nguồn: …, cập nhật …' |
| `checklist` | items | Danh sách kiểm, từng mục hiện dần có dấu ✓ (thêm 'title') |
| `stat` | value, label | Số lớn chạy từ 0 (thêm 'prefix', 'suffix', 'decimals') |
