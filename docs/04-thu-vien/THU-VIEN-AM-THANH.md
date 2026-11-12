# Thư viện hiệu ứng âm

Tự sinh: `python3 scripts/am_thanh.py --md > ../docs/04-thu-vien/THU-VIEN-AM-THANH.md` (trong `video-studio`).
File: `video-studio/thu-vien-am-thanh/hieu-ung/<tên>.wav`. Dùng tên ở cột đầu cho hàng `sfx` của `timeline.json`, hoặc chọn trong app (tab Hiệu ứng âm).
Điểm nhấn = giây trong file mà tai nghe là lúc "chạm"; mẫu edit canh điểm này vào đúng lúc hình chuyển/chữ hiện.

## whoosh
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `whoosh_nhanh_01` | Gió vút nhanh 0,45 s | Chuyển cảnh cắt nhanh, chữ lớn bay vào | 0.45s | 0.25s | tổng hợp (scripts/tao_sfx.py) |
| `whoosh_cham_01` | Gió vút chậm 1 s | Chuyển cảnh chậm (hoà tan, trượt), đổi chương | 1.0s | 0.6s | tổng hợp (scripts/tao_sfx.py) |
| `whoosh_zoom_01` | Vút lên cao như lao vào cảnh | Chuyển cảnh phóng mờ (gl-CrossZoom, zoomin) | 0.6s | 0.5s | tổng hợp (scripts/tao_sfx.py) |
| `whoosh_xoay_01` | Vút có rung xoáy | Chuyển cảnh xoay (gl-WhipSpin, gl-Swirl) | 0.6s | 0.38s | tổng hợp (scripts/tao_sfx.py) |
| `whoosh_quat_01` | Quất rất ngắn 0,25 s | Lia máy nhanh, chữ trượt ngang | 0.25s | 0.12s | tổng hợp (scripts/tao_sfx.py) |

## chu
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `chu_swish-pop_01` | Vụt + bụp nhẹ (0,15 s, nhiều tần cao) | Chữ lớn hiện (giống video mẫu: mỗi lần chữ to xuất hiện) | 0.2s | 0.13s | tổng hợp (scripts/tao_sfx.py) |
| `chu_pop_01` | Bụp tròn, ngắn | Chữ nhỏ, nhãn, gạch đầu dòng hiện | 0.09s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `chu_click_01` | Tách rất ngắn | Phụ đề đổi dòng, đánh dấu ✓ | 0.012s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `chu_tick_01` | Tíc gỗ | Đếm số, từng mục danh sách | 0.05s | 0.0s | tổng hợp (scripts/tao_sfx.py) |

## ting
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `ting_don_01` | Ting kim loại 5,2 kHz | Con số chốt (giá, diện tích), từ khóa quan trọng | 0.6s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `ting_kep_01` | Ting hai nhịp | Số liệu nổi bật nhất video | 0.68s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `ting_lap-lanh_01` | Lấp lánh nhiều ting nhỏ | Tiện ích sang trọng, cảnh đẹp, logo | 1.492s | 0.05s | tổng hợp (scripts/tao_sfx.py) |
| `ting_ket_01` | Ding dài vang (3,6 kHz) | Cảnh kết, lời kêu gọi | 2.6s | 0.0s | tổng hợp (scripts/tao_sfx.py) |

## impact
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `impact_tram_01` | Đập trầm ngắn | Hook giây đầu, chữ số lớn đập vào | 0.9s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `impact_boom_01` | Bùm trầm vang dài | Mở đầu mạnh, sau khoảng lặng, cú chuyển lớn | 2.8s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `impact_hit_01` | Đánh gọn | Nhấn từng ý trong danh sách | 0.35s | 0.0s | tổng hợp (scripts/tao_sfx.py) |

## riser
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `riser_1s_01` | Dồn lên 1 giây (kết thúc đột ngột) | Đặt ngay trước chuyển cảnh lớn | 1.0s | 0.99s | tổng hợp (scripts/tao_sfx.py) |
| `riser_2s_01` | Dồn lên 2 giây | Trước tiết lộ quan trọng (giá, tiện ích) | 2.0s | 1.99s | tổng hợp (scripts/tao_sfx.py) |
| `riser_nguoc_01` | Tiếng chũm chọe ngược 1 giây | Dẫn vào cảnh mới, trước chữ lớn | 1.0s | 0.99s | tổng hợp (scripts/tao_sfx.py) |

## anh-sang
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `anh-sang_chay_01` | Gió ấm + lách tách | Chuyển cảnh cháy sáng / light leak (gl-FilmBurn, gl-BurnThrough) | 0.8s | 0.3s | tổng hợp (scripts/tao_sfx.py) |
| `anh-sang_flash_01` | Loé xì ngắn | Chuyển cảnh loé trắng (gl-Overexposure, gl-FlashFade) | 0.35s | 0.08s | tổng hợp (scripts/tao_sfx.py) |

