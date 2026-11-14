# Thư viện tag chữ

Lập 13/11/2026. Mã: `video-studio/scripts/tag_chu.py`. Trong timeline là khối chữ `kind: "tag"`.
Mỗi tag là **khung bố cục + chuyển động có sẵn**: chỉ điền chữ của Hào. Học bố cục và nhịp từ bộ tag mẫu Hào tải lên Drive (bộ 1, 10 kiểu). Claude dựng lại bằng HTML/GSAP, **không dùng file gốc** (bộ mẫu có thể là gói của người khác).

## 66 tag trong 6 bộ (danh mục tự sinh: `python3 scripts/tag_chu.py --md`)
Bộ 1 do Claude làm riêng từng tag. Bộ 2–6 dùng **2 khung chung**:
- **Chữ chồng dòng** (bộ 3–6): mỗi dòng một kiểu chữ (viết tay, đậm, có chân, chữ hẹp, nhỏ, nhãn, biểu tượng) và màu/phát sáng.
- **Thanh tên kim loại** (bộ 2): 6 hình, màu đỏ/xanh/vàng, có tia sáng quét.

Thêm tag mới chỉ là thêm một dòng cấu hình (`dang_dong(...)` hoặc `dang_thanh(...)` trong `tag_chu.py`).
Ô chữ của tag chồng dòng là `"1"`, `"2"`… theo thứ tự dòng từ trên xuống.
Bộ 7 (file `2448…`) là video quảng cáo của bộ 5, không có tag mới.

### Bộ 1: tag cơ bản
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `thanh-doc` | Nhấn một ưu điểm: chữ đậm + dòng mảnh bên dưới | tren: VỊ TRÍ *VÀNG* · duoi: sát trục chính |
| `chong-tuong-phan` | Đối lập hai ý: A chứ không phải B | a: DÒNG TIỀN · nho: mới là điều · phu: không phải · b: GIÁ BÁN |
| `rai-so-le` | Liệt kê 3–4 điểm ngắn: tiện ích, ưu điểm | 1: Gần trường · 2: gần chợ · 3: đi bộ · 4: ra biển |
| `so-tron` | Một con số nổi bật (phải có nguồn và ngày) | so: 30% · nhan: VỐN TỰ CÓ |
| `gach-chan` | Cảnh báo, sai lầm, điều cần nhớ | cau: Sai lầm khi vay · duoi: lần đầu mua nhà |
| `thanh-ten` | Giới thiệu dự án, người nói, thương hiệu | logo: HSL · ten: VINHOMES CẦN GIỜ · mo_ta: Hào Sky Land · tư vấn dòng tiền |
| `doi-chu` | Một ý, nhiều đáp án: phù hợp an cư → cho thuê → nghỉ dưỡng | tren: Phù hợp · doi: an cư\|cho thuê\|nghỉ dưỡng |
| `ba-tang` | Khẩu hiệu ngắn, cảm xúc: tầng giữa là chữ chính | tren: SỐNG · giua: XANH · duoi: MỖI NGÀY |
| `hop-trang` | Điểm cần kiểm tra, mục quan trọng | hop: Điều cần kiểm tra · nhan: TRƯỚC KHI ĐẶT CỌC |
| `buoc-so` | Các bước, thứ tự, danh sách đánh số | chu: Bước · so: 1 |

### Bộ 2: thanh tên kim loại (ô mau: do / xanh / vang)
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `thanh-lo-dat` | Diện tích, lô đất | tieu_de: Lô đất [...] m² · phu: Vinhomes Hóc Môn · mau: xanh |
| `thanh-gia-thue` | Giá thuê, giá từ (có nguồn) | tieu_de: CĂN HỘ [...] · phu: giá thuê từ [...] triệu/tháng · mau: do |
| `thanh-loai-can` | Tên loại căn | tieu_de: CĂN 2 PHÒNG NGỦ · phu: [...] m² · view nội khu · mau: vang · icon: nha |
| `thanh-so` | Ý số 1, 2, 3 | tieu_de: Tầm nhìn rộng · phu: view toàn cảnh · mau: do · so: 1 |
| `thanh-tien-ich` | Tiện ích | tieu_de: Tiện ích nội khu · phu: hồ bơi · công viên · trường học · mau: xanh · icon: sao |
| `thanh-du-an` | Tên dự án | tieu_de: VINHOMES CẦN GIỜ · phu: dự án đang phân phối · mau: do |
| `thanh-lien-he` | Kêu gọi liên hệ | tieu_de: LIÊN HỆ HÀO · phu: để nhận bảng tính dòng tiền · mau: do · icon: dien-thoai |
| `thanh-ban-tin` | Bản tin, cập nhật có ngày | tieu_de: BẢN TIN BĐS [...] · phu: cập nhật ngày [...] · mau: do |
| `thanh-dich-vu` | Dịch vụ | tieu_de: TƯ VẤN DÒNG TIỀN · phu: miễn phí bảng tính · mau: vang |
| `thanh-vi-tri` | Vị trí, kết nối | tieu_de: Vị trí dự án · phu: cách trung tâm [...] km · mau: do · icon: ghim |
| `thanh-chinh-sach` | Chính sách (phải có nguồn) | tieu_de: CHÍNH SÁCH [...] · phu: nguồn: chủ đầu tư, ngày [...] · mau: do · icon: the |
| `thanh-nguoi-noi` | Tên người nói | tieu_de: LÊ DƯƠNG HÀO · phu: Hào Sky Land · mau: vang · icon: sao |

### Bộ 3: tiêu đề viết tay + đậm + phát sáng
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `td-uu-dai` | Ưu đãi có số (phải có nguồn) | 1: Ưu đãi · 2: [...] triệu |
| `td-buoc-thuc-hien` | Số bước + tiêu đề | 1: 5 · 2: Bước · 3: mua nhà · 4: đúng quy trình |
| `td-de-dang` | Câu ngắn hai màu | 1: dễ dàng · 2: vay vốn |
| `td-so-huu` | Không gian sống | 1: Sở hữu · 2: Không Gian Sống · 3: đẳng cấp |
| `td-can-ho-mau` | Giới thiệu căn mẫu | 1: Căn hộ mẫu · 2: VINHOMES HÓC MÔN · 3: Hào Sky Land |
| `td-uu-dai-vang` | Ưu đãi nổi bật | 1: Ưu đãi · 2: Vàng · 3: [...] / tháng |
| `td-biet-thu` | Loại hình + phong cách | 1: Biệt thự · 2: PHONG CÁCH · 3: hiện đại |
| `td-mot-can` | Số + chữ viết tay | 1: 1 · 2: Căn hộ · 3: đáng sống |
| `td-so-huu-ngay` | Loại căn | 1: Phù hợp · 2: CĂN 2 NGỦ · 3: gia đình trẻ |
| `td-bo-ra` | Số tiền lớn (có nguồn) | 1: Vốn từ · 2: [...] tỷ · 3: cho căn 2 ngủ |
| `td-thang-hoa` | Cảm xúc, khoảnh khắc | 1: Khoảnh khắc · 2: Về Nhà · 3: bình yên |
| `td-luu-giu` | Câu cảm xúc 3 tầng | 1: Lưu giữ · 2: Tổ ấm · 3: cho con · 4: sống xanh mỗi ngày |

### Bộ 4: bất động sản sang trọng
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `bds-song-sang` | Phong cách sống | 1: Đậm chất · 2: SỐNG XANH · 3: trong từng không gian |
| `bds-tam-diem` | Vị trí trung tâm | 1: đầu tư dự án · 2: TÂM ĐIỂM · 3: kết nối khu Tây Bắc |
| `bds-ben-song` | Không gian + biểu tượng tòa nhà | 1: không gian · 2: BÊN DÒNG SÔNG · 3: nhịp sống khác biệt |
| `bds-bieu-tuong` | Danh hiệu + nhãn | 1: Biểu tượng · 2: Sống Xanh · 3: trong lòng thành phố |
| `bds-cham-bien` | Biển, nghỉ dưỡng | 1: một bước · 2: Chạm Biển · 3: Cần Giờ · 4: nghỉ dưỡng |
| `bds-dinh-danh` | Định danh dự án | 1: Định danh · 2: Đô Thị Biển · 3: Vinhomes Cần Giờ |
| `bds-vi-tri` | Vị trí | 1: Vị trí · 2: Kết Nối · 3: [...] phút về trung tâm |
| `bds-view-song` | Loại căn + view | 1: Căn hộ · 2: VIEW SÔNG · 3: thoáng mát |
| `bds-toa-do` | Tọa độ + ghim | 1: Tọa độ · 2: Trục Chính · 3: gần hạ tầng [...] |
| `bds-dai-do-thi` | Tên đại đô thị + nhãn | 1: Đại đô thị · 2: VINHOMES HÓC MÔN |
| `bds-bao-chung` | Cam kết của chủ đầu tư (có nguồn) | 1: Pháp lý · 2: RÕ RÀNG · 3: nguồn: [...] |
| `bds-khong-gian-mo` | Căn hộ + biểu tượng nhà | 1: Căn Hộ · 2: KHÔNG GIAN MỞ · 3: nâng tầm cuộc sống |
| `bds-song-dinh` | Khám phá | 1: Khám phá không gian · 2: SỐNG XANH · 3: VINHOMES · 4: Hóc Môn |
| `bds-oc-dao` | Xanh giữa đô thị | 1: ỐC ĐẢO · 2: XANH · 3: giữa lòng · 4: Đô Thị |
| `bds-dong-tien` | Dòng tiền | 1: Bài toán · 2: DÒNG TIỀN · 3: mỗi tháng · 4: sau khi trừ tiền vay |

### Bộ 5: talking head (chữ hiện từng từ, đặt x 0,3 hoặc 0,7)
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `th-mang-lai` | Lợi ích chính | 1: em mang lại · 2: BẢNG TÍNH |
| `th-hang-c` | Loại căn + nhãn | 1: CĂN 2 NGỦ · 2: vừa túi tiền |
| `th-day-la` | Câu dài 3 nhịp | 1: đây là · 2: căn dành cho · 3: gia đình |
| `th-con-so` | Con số nóng (có nguồn) | 1: lãi vay · 2: [...]% · 3: năm đầu |
| `th-dep-nhat` | So sánh nhất | 1: VIEW · 2: đẹp nhất · 3: toàn dự án |
| `th-chat-luong` | Hai cụm đối | 1: Pháp lý · 2: RÕ RÀNG · 3: không thể bỏ qua |
| `th-tam-tri` | Câu cảm xúc | 1: cho · 2: GIA ĐÌNH BẠN · 3: Tổ ấm |
| `th-chan` | Nỗi đau + giải pháp | 1: Chán · 2: đi thuê nhà? · 3: có nhà riêng |
| `th-an-toan` | Từ khoá an toàn | 1: công nghệ · 2: AN TOÀN · 3: cho cả nhà |
| `th-ben-bi` | Một từ khoá nhấn | 1: độ · 2: BỀN BỈ · 3: theo năm tháng |

### Bộ 6: ưu đãi
| Tên (`tag`) | Dùng cho | Ô chữ mẫu (`o`) |
|---|---|---|
| `ud-glow` | Tiêu đề hai màu | 1: SỐNG XANH · 2: MỖI NGÀY |
| `ud-giam-den` | Nhãn giảm (có nguồn) | 1: chiết khấu đến · 2: [...]% |
| `ud-bieu-tuong` | Danh hiệu + nhãn hồng | 1: Biểu tượng · 2: An Cư · 3: nâng tầm tổ ấm |
| `ud-top` | Top N | 1: 3 · 2: Top · 3: LÝ DO NÊN MUA · 4: Ở THỰC |
| `ud-buoc-cham` | Số bước | 1: 4 · 2: Bước · 3: CHUẨN BỊ VỐN · 4: trước khi xem nhà |
| `ud-phieu` | Phiếu 2 ô: chính sách, quà (có nguồn) | a1: HỖ TRỢ · a2: LÃI [...] · b1: QUÀ TẶNG · b2: [...] |
| `ud-doi-hop` | Phương pháp + đổi chữ trong hộp sáng | tren: Giải pháp · chinh: VAY [...]% · doi: lãi cố định\|ân hạn gốc\|trả góp đều |

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
- Xong 13/11: bộ 2–6 (56 tag) từ 6 file mẫu Hào gửi trong chat; chụp đủ 66 tag, sửa các tag lệch; dựng thử 44 giây 15 tag trên footage thật (`projects/zz-tag-thu2`).
- Chữ mẫu đã đổi sang nội dung BĐS của Hào; số liệu chưa có nguồn để `[...]`. Tên dự án, chủ đầu tư trong bộ mẫu (Vinhomes khác, Imperia, Toyota…) không chép.
- Còn yếu: chữ vàng có chân trên nền cây, trời sáng hơi chìm (nên đặt trên vùng tối hoặc thêm thẻ nền).
