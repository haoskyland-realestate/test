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
| `whoosh_air-woosh_01` | Air woosh 2.32 s | Chuyển cảnh, chữ bay vào | 2.32s | 0.7s | Mixkit 1489 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_cinematic-whoosh-fast-tr_01` | Cinematic whoosh fast transition 1.33 s | Chuyển cảnh, chữ bay vào | 1.33s | 1.06s | Mixkit 1492 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_arrow-whoosh_01` | Arrow whoosh 1.1 s | Chuyển cảnh, chữ bay vào | 1.1s | 0.28s | Mixkit 1491 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_fast-whoosh-transition_01` | Fast whoosh transition 1.76 s | Chuyển cảnh, chữ bay vào | 1.76s | 0.72s | Mixkit 1490 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_explainer-video-pops-who_01` | Explainer video pops whoosh light pop 0.18 s | Chuyển cảnh, chữ bay vào | 0.18s | 0.02s | Mixkit 3005 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_metal-hit-woosh_01` | Metal hit woosh 0.48 s | Chuyển cảnh, chữ bay vào | 0.48s | 0.08s | Mixkit 1485 https://mixkit.co/free-sound-effects/whoosh/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_fast-small-sweep-transit_01` | Fast small sweep transition 0.78 s | Chuyển cảnh | 0.78s | 0.32s | Mixkit 166 https://mixkit.co/free-sound-effects/transition/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_air-zoom-vacuum_01` | Air zoom vacuum 1.27 s | Chuyển cảnh | 1.27s | 0.44s | Mixkit 2608 https://mixkit.co/free-sound-effects/transition/ (Sound Effects Free License, tải 2026-11-14) |
| `whoosh_vacuum-swoosh-transition_01` | Vacuum swoosh transition 2.26 s | Chuyển cảnh | 2.26s | 1.56s | Mixkit 1465 https://mixkit.co/free-sound-effects/transition/ (Sound Effects Free License, tải 2026-11-14) |

## chu
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `chu_swish-pop_01` | Vụt + bụp nhẹ (0,15 s, nhiều tần cao) | Chữ lớn hiện (giống video mẫu: mỗi lần chữ to xuất hiện) | 0.2s | 0.13s | tổng hợp (scripts/tao_sfx.py) |
| `chu_pop_01` | Bụp tròn, ngắn | Chữ nhỏ, nhãn, gạch đầu dòng hiện | 0.09s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `chu_click_01` | Tách rất ngắn | Phụ đề đổi dòng, đánh dấu ✓ | 0.012s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `chu_tick_01` | Tíc gỗ | Đếm số, từng mục danh sách | 0.05s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `chu_camera-shutter-click_01` | Camera shutter click 0.35 s | Chữ hiện, nút bấm | 0.35s | 0.18s | Mixkit 1133 https://mixkit.co/free-sound-effects/click/ (Sound Effects Free License, tải 2026-11-14) |
| `chu_fast-double-click-on-mou_01` | Fast double click on mouse 0.47 s | Chữ hiện, nút bấm | 0.47s | 0.1s | Mixkit 275 https://mixkit.co/free-sound-effects/click/ (Sound Effects Free License, tải 2026-11-14) |
| `chu_select-click_01` | Select click 1.1 s | Chữ hiện, nút bấm | 1.1s | 0.06s | Mixkit 1109 https://mixkit.co/free-sound-effects/click/ (Sound Effects Free License, tải 2026-11-14) |
| `chu_long-pop_01` | Long pop 0.48 s | Chữ nảy lên, thẻ xuất hiện | 0.48s | 0.02s | Mixkit 2358 https://mixkit.co/free-sound-effects/pop/ (Sound Effects Free License, tải 2026-11-14) |
| `chu_hard-pop-click_01` | Hard pop click 1.17 s | Chữ nảy lên, thẻ xuất hiện | 1.17s | 0.04s | Mixkit 2364 https://mixkit.co/free-sound-effects/pop/ (Sound Effects Free License, tải 2026-11-14) |
| `chu_bubble-pop-up-alert-noti_01` | Bubble pop up alert notification 0.38 s | Chữ nảy lên, thẻ xuất hiện | 0.38s | 0.04s | Mixkit 2357 https://mixkit.co/free-sound-effects/pop/ (Sound Effects Free License, tải 2026-11-14) |

## ting
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `ting_don_01` | Ting kim loại 5,2 kHz | Con số chốt (giá, diện tích), từ khóa quan trọng | 0.6s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `ting_kep_01` | Ting hai nhịp | Số liệu nổi bật nhất video | 0.68s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `ting_lap-lanh_01` | Lấp lánh nhiều ting nhỏ | Tiện ích sang trọng, cảnh đẹp, logo | 1.492s | 0.05s | tổng hợp (scripts/tao_sfx.py) |
| `ting_ket_01` | Ding dài vang (3,6 kHz) | Cảnh kết, lời kêu gọi | 2.6s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `ting_correct-answer-tone_01` | Correct answer tone 1.96 s | Số liệu, thông báo, thẻ | 1.96s | 0.02s | Mixkit 2870 https://mixkit.co/free-sound-effects/notification/ (Sound Effects Free License, tải 2026-11-14) |
| `ting_software-interface-start_01` | Software interface start 2.35 s | Số liệu, thông báo, thẻ | 2.35s | 0.12s | Mixkit 2574 https://mixkit.co/free-sound-effects/notification/ (Sound Effects Free License, tải 2026-11-14) |
| `ting_sci-fi-click_01` | Sci fi click 0.7 s | Số liệu, thông báo, thẻ | 0.7s | 0.14s | Mixkit 900 https://mixkit.co/free-sound-effects/notification/ (Sound Effects Free License, tải 2026-11-14) |

## impact
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `impact_tram_01` | Đập trầm ngắn | Hook giây đầu, chữ số lớn đập vào | 0.9s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `impact_boom_01` | Bùm trầm vang dài | Mở đầu mạnh, sau khoảng lặng, cú chuyển lớn | 2.8s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `impact_hit_01` | Đánh gọn | Nhấn từng ý trong danh sách | 0.35s | 0.0s | tổng hợp (scripts/tao_sfx.py) |
| `impact_wood-hard-hit_01` | Wood hard hit 0.42 s | Chữ lớn chạm, nhấn ý | 0.42s | 0.06s | Mixkit 2182 https://mixkit.co/free-sound-effects/impact/ (Sound Effects Free License, tải 2026-11-14) |
| `impact_metal-hammer-hit_01` | Metal hammer hit 0.77 s | Chữ lớn chạm, nhấn ý | 0.77s | 0.12s | Mixkit 833 https://mixkit.co/free-sound-effects/impact/ (Sound Effects Free License, tải 2026-11-14) |
| `impact_impact-of-a-blow_01` | Impact of a blow 0.59 s | Chữ lớn chạm, nhấn ý | 0.59s | 0.18s | Mixkit 2150 https://mixkit.co/free-sound-effects/impact/ (Sound Effects Free License, tải 2026-11-14) |

## riser
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `riser_1s_01` | Dồn lên 1 giây (kết thúc đột ngột) | Đặt ngay trước chuyển cảnh lớn | 1.0s | 0.99s | tổng hợp (scripts/tao_sfx.py) |
| `riser_2s_01` | Dồn lên 2 giây | Trước tiết lộ quan trọng (giá, tiện ích) | 2.0s | 1.99s | tổng hợp (scripts/tao_sfx.py) |
| `riser_nguoc_01` | Tiếng chũm chọe ngược 1 giây | Dẫn vào cảnh mới, trước chữ lớn | 1.0s | 0.99s | tổng hợp (scripts/tao_sfx.py) |
| `riser_cinematic-trailer-riser_01` | Cinematic trailer riser 2.58 s | Tăng dần trước chuyển cảnh mạnh | 2.58s | 2.52s | Mixkit 790 https://mixkit.co/free-sound-effects/riser/ (Sound Effects Free License, tải 2026-11-14) |

## anh-sang
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `anh-sang_chay_01` | Gió ấm + lách tách | Chuyển cảnh cháy sáng / light leak (gl-FilmBurn, gl-BurnThrough) | 0.8s | 0.3s | tổng hợp (scripts/tao_sfx.py) |
| `anh-sang_flash_01` | Loé xì ngắn | Chuyển cảnh loé trắng (gl-Overexposure, gl-FlashFade) | 0.35s | 0.08s | tổng hợp (scripts/tao_sfx.py) |

## glitch
| Tên | Âm | Dùng khi | Dài | Điểm nhấn | Nguồn |
|---|---|---|---|---|---|
| `glitch_small-electric-glitch_01` | Small electric glitch 1.02 s | Chữ giải mã, nhiễu hình | 1.02s | 0.0s | Mixkit 2595 https://mixkit.co/free-sound-effects/glitch/ (Sound Effects Free License, tải 2026-11-14) |
| `glitch_glitch-static_01` | Glitch static 1.4 s | Chữ giải mã, nhiễu hình | 1.4s | 0.14s | Mixkit 1457 https://mixkit.co/free-sound-effects/glitch/ (Sound Effects Free License, tải 2026-11-14) |
| `glitch_glitch-roar_01` | Glitch roar 1.08 s | Chữ giải mã, nhiễu hình | 1.08s | 0.06s | Mixkit 1033 https://mixkit.co/free-sound-effects/glitch/ (Sound Effects Free License, tải 2026-11-14) |

