# Chỉnh màu: luật và cách hệ thống làm

Lập 13/11/2026. Công cụ: `video-studio/scripts/chinh_mau.py`. Quy trình cho Claude: skill `.claude/skills/chinh-mau/SKILL.md`.
Miễn phí, tự xây: chỉ dùng numpy, OpenCV, ffmpeg (đã có). Học cách làm (không chép mã) từ hai repo giấy phép MIT: [agentic-color-grader](https://github.com/perbhat/agentic-color-grader) (quy trình cảnh chuẩn, ngưỡng kiểm) và [Colourway](https://github.com/Gadfly-Yang/Colourway) (đọc "chữ ký màu" của video mẫu).

## 1. Hệ thống làm gì (5 bước)
| Bước | Máy làm | Ra |
|---|---|---|
| 1. Đo | Mỗi cảnh lấy 3 khung: độ sáng (giữa, tối, sáng), % cháy và % thiếu sáng, **ám màu đo trên vùng trắng/xám**, độ rực, **màu da** (tự tìm mặt người) | bảng số trong `MAU-SAC.md` |
| 2. Sửa lỗi | Cân trắng (đưa vùng trắng/xám về trung tính 90%), kéo sáng tối về vùng đẹp, nén mềm vùng cháy. Chỉnh trên độ sáng chung nên **không làm da rực thêm** | thông số từng cảnh |
| 3. Đồng nhất | Chọn **cảnh chuẩn** (có người, ít cháy, sáng vừa; hoặc Hào chỉ định), kéo độ sáng các cảnh khác về gần cảnh chuẩn (mức `--do-manh`, mặc định 70%) | |
| 4. Phong cách | Phủ tông chung: tint vùng tối/vùng sáng, tương phản chữ S, độ rực. Từ bảng có sẵn hoặc **đọc từ video/ảnh mẫu** | |
| 5. Giữ da, giữ trắng, kiểm | Màu thuộc dải da lấy lại 90% màu đã sửa lỗi, không rực hơn quá 3%. Trắng sáng không bị nhuộm quá 1,5 đơn vị. Đo lại, báo cảnh lệch | `mau/cNN.cube`, `mau/truoc-sau.jpg` |

Mỗi cảnh ra một **LUT 33³** (`projects/<tên>/mau/cNN.cube`). Timeline ghi `"look": "lut:mau/cNN.cube"`. App hiện tên "Màu đạo diễn"; muốn đổi thì chọn lại màu khác trong ô Chỉnh màu của đoạn đó. Thông số sửa tay ở `mau/ke-hoach.json`, chạy lại với `--tu-file`. LUT dùng được cả trong Premiere, DaVinci, CapCut.

## 2. Số chuẩn (để kiểm, không đoán bằng mắt)
| Chỉ số | Chuẩn | Ghi chú |
|---|---|---|
| Da người (độ rực HSV, vùng giữa mặt) | **35–50%** | trên 55% là cam. Video Gladia cũ bị 51–74% |
| Da người (sắc độ HSV) | 12–24° | thấp hơn: hồng/đỏ; cao hơn: vàng |
| Vùng trắng/xám (Lab a, b) | lệch cảnh chuẩn ≤ ±3 | nhà mẫu cao cấp cố ý ấm nhẹ: b khoảng +2 |
| Độ sáng giữa giữa các cảnh | lệch ≤ 0,08 | cảnh khác hẳn ánh sáng (trong/ngoài) được lệch, ghi lý do |
| Cháy sáng | < 2% điểm ảnh | quá thì footage hỏng vùng sáng, chỉ nén mềm được |
| Nội thất trắng (high-key) | độ sáng giữa tới 0,75 | **không kéo tối** nội thất trắng chỉ để "đúng chuẩn" |

## 3. Phong cách có sẵn (`--phong-cach`)
| Tên | Dùng cho | Cảm giác |
|---|---|---|
| `sang-trong` (mặc định) | Nhà mẫu, biệt thự cao cấp | Trắng sạch hơi ấm, đen sâu vừa, ít rực, vật liệu thật |
| `am-ap` | Gia đình, nắng chiều, nghỉ dưỡng | Vùng sáng vàng ấm, vùng tối trung tính |
| `hien-dai-mat` | Căn hộ, văn phòng, cao tầng | Vùng tối hơi xanh, trắng trung tính, tương phản rõ |
| `dien-anh` | Video thương hiệu, phóng sự | Vùng tối xanh ngọc, vùng sáng ấm, vẫn giữ da |
| `tu-nhien` | Video cần đúng màu thật (pháp lý, tiến độ) | Chỉ sửa lỗi và đồng nhất, không phủ màu |

**Lấy màu từ video mẫu (`--mau`):** máy đọc chữ ký màu của mẫu (độ sáng giữa, tint vùng tối/giữa/sáng, độ rực), rồi áp vào footage theo `--do-manh`. Da và trắng vẫn được giữ. Đã thử với một ảnh mẫu tông cam đậm: cảnh nhận tông ấm, độ rực chung tăng gấp đôi, da chỉ từ 38% lên 40%.

## 4. Lệnh
```
python3 scripts/chinh_mau.py projects/<tên>                                   # đo + kế hoạch + ảnh trước/sau
python3 scripts/chinh_mau.py projects/<tên> --phong-cach am-ap --chuan 3
python3 scripts/chinh_mau.py projects/<tên> --mau projects/<tên>/build/raw/mau.mp4 --do-manh 0.6
python3 scripts/chinh_mau.py projects/<tên> --tu-file                         # chạy lại sau khi sửa mau/ke-hoach.json
python3 scripts/chinh_mau.py projects/<tên> --ap                              # Hào duyệt: ghi LUT vào timeline
python3 scripts/chinh_mau.py --tu-kiem                                        # tự kiểm
```

## 5. Đã thử (13/11/2026)
- Tự kiểm: ảnh ám vàng tối → hết ám, sáng lên; da không rực quá 5% với phong cách thật; trắng giữ trắng; LUT đúng định dạng.
- Video Gladia (11 cảnh, nội thất trắng): da giữ 38→38%, 46→45%. Độ sáng các cảnh đồng đều 0,67–0,71. Nội thất trắng không bị kéo tối.
- 5 clip ngoài trời của Hào (lẫn quay dọc và ngang): sửa một cảnh ám xanh; kiểm đạt.
- LUT qua ffmpeg so với công thức: lệch trung bình 0,5/255 (mắt không thấy).
- Dựng thật 18 giây có LUT: cảnh sau LUT đúng như kế hoạch.

## 6. Giới hạn và việc sau
- **Dải tối dưới chữ (scrim):** phong cách `hien-dai` phủ dải đen 62% dưới khung **suốt video, kể cả khi không có chữ**, làm video tối hẳn (đo: 0,64 → 0,40). Không phải lỗi màu, nhưng làm hỏng công chỉnh màu. Nên chỉ hiện dải tối khi có chữ hoặc phụ đề (chờ Hào quyết, vì đổi giao diện các mẫu đã duyệt).
- Màu chỉnh theo từng cảnh, không theo từng khung: cảnh có ánh sáng đổi giữa chừng (đi từ trong ra ngoài) nên tách cảnh trước.
- Chưa có: chỉnh màu riêng một vùng (bầu trời, cây), hiệu ứng loé sáng và hạt phim (để sau, LUT không chứa được), xem trước LUT trực tiếp trong khung xem của app (hiện thấy khi Dựng nháp).
- Footage DJI/iPhone HDR được chuyển tông trước khi đo, giống bộ dựng.
