# Thư viện tag chữ

Lập 13/11/2026. Mã: `video-studio/scripts/tag_chu.py`. Trong timeline là khối chữ `kind: "tag"`.
Mỗi tag là **khung bố cục + chuyển động có sẵn**: chỉ điền chữ của Hào. Học bố cục và nhịp từ bộ tag mẫu Hào tải lên Drive (bộ 1, 10 kiểu). Claude dựng lại bằng HTML/GSAP, **không dùng file gốc** (bộ mẫu có thể là gói của người khác).

## 10 tag (bộ 1)
| Tên (`tag`) | Kiểu | Ô chữ (`o`) | Dùng cho | Ví dụ |
|---|---|---|---|---|
| `thanh-doc` | Thanh dọc + 2 tầng chữ | `tren`, `duoi` | Nhấn một ưu điểm | VỊ TRÍ *VÀNG* / sát trục chính |
| `chong-tuong-phan` | Chữ chồng tương phản | `a`, `nho`, `phu`, `b` | A chứ không phải B | DÒNG TIỀN / mới là điều / không phải / GIÁ BÁN |
| `rai-so-le` | Chữ rải so le | `1`…`4` | Liệt kê 3–4 điểm ngắn | Gần trường, gần chợ, đi bộ, ra biển |
| `so-tron` | Số lớn + vòng tròn | `so`, `nhan` | Một con số (có nguồn, ngày) | 30% / VỐN TỰ CÓ |
| `gach-chan` | Câu + gạch chân | `cau`, `duoi` | Cảnh báo, sai lầm | Sai lầm khi vay / lần đầu mua nhà |
| `thanh-ten` | Thanh tên (logo + tên) | `logo`, `ten`, `mo_ta` | Giới thiệu dự án, người nói | HSL / VINHOMES CẦN GIỜ / … |
| `doi-chu` | Đổi chữ cuối | `tren`, `doi` (cách bằng `\|`) | Một ý, nhiều đáp án | Phù hợp / an cư \| cho thuê \| nghỉ dưỡng |
| `ba-tang` | Chữ chồng 3 tầng | `tren`, `giua`, `duoi` | Khẩu hiệu cảm xúc | SỐNG / XANH / MỖI NGÀY |
| `hop-trang` | Hộp trắng + nhãn | `hop`, `nhan` | Điều cần kiểm tra | Điều cần kiểm tra / TRƯỚC KHI ĐẶT CỌC |
| `buoc-so` | Bước + số lớn | `chu`, `so` | Các bước | Bước / 1 |

Mẫu trong timeline:
```json
{"kind": "tag", "tag": "so-tron", "start": 12.4, "dur": 2.5, "o": {"so": "30%", "nhan": "VỐN TỰ CÓ"}, "y": 0.24}
```
- `y`: vị trí dọc 0..1 (mặc định 0,24 = trên mặt người nói, theo `GHI-NHO-NGHIEM-THU.md`).
- `*từ*` để tô màu nhấn. Tag nào cũng có bóng mờ phía sau để đọc được trên nền trời sáng.
- Vào: quét, trượt, mờ thành rõ, vẽ nét. Ra: vệt nhoè ngang (như bộ mẫu). Khung YouTube tự thu nhỏ.
- Tag số liệu (giá, %, ưu đãi): chỉ điền khi có nguồn và ngày; chưa có thì `[...]`.

## Đã làm, chưa làm
- Xong 13/11: 10 tag, tự kiểm (`python3 scripts/tag_chu.py --tu-kiem`), dựng thử 29 giây trên footage thật của Hào (`projects/zz-tag-thu`), đã xem khung hình.
- Chưa: nút "🏷 Tag" trong app (chọn tag, gõ chữ, đặt tại kim), tự chọn tag theo kịch bản (`[buoc] Bước / 1` trong cột chữ của `KICH-BAN.md`), âm "vút/bụp" tự rải theo tag.
- 6 bộ tag mẫu còn lại trên Drive (thư mục "Tài Nguyên ( Update theo tháng )") chưa xem được vì thư mục đã khoá chia sẻ.
