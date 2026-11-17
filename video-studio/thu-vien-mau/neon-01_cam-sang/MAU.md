# Neon cam ánh sáng (`neon-01`)

Loại: **talking head** · Nhãn: VIDEO TALKING HEAD · Ngành: Bất động sản · Lập 13/11/2026.
Mẫu tự thiết kế cho Hào Sky Land (học thể loại phổ biến, không sao chép mẫu của ai). Nguyên tắc chung: `docs/04-thu-vien/CONG-THUC-VIRAL.md`.

Chữ cam phát sáng gõ dần theo lời, số nổi cam, thẻ tối viền neon; khung gần – khung xa xen kẽ mỗi ý; quét sáng và loé khi đổi chương.

**Hợp cho:** Hook mạnh, cảnh đêm, căn hộ cao tầng, phân tích có số liệu nổi bật

## Công thức
- **Chữ:** cam phát sáng, **gõ dần từng ký tự** (kèm tiếng tíc) → người xem đọc theo nhịp gõ, giữ mắt trên màn hình.
- **Khung gần – xa xen kẽ:** zoom 12% cách một chữ một lần → như có hai góc máy dù chỉ quay một máy.
- **Chuyển cảnh:** quét sáng (LightWipe) và loé trắng (Overexposure) ở chỗ đổi chương, kèm vút/loé.
- **Thẻ minh hoạ:** nền tối viền neon cam.
- **Hook:** tiếng bùm trầm ở giây đầu + chữ số lớn.

## Khi nào hợp
- Một con số "đinh" (giá, lãi suất, khoảng cách) cần nổi bật.
- Cảnh đêm, căn hộ cao tầng, ánh đèn.
- Không hợp: cảnh ban ngày quá sáng (chữ cam kém nổi) → đổi `talking-head-01`.

## Khung 40 giây mẫu
| Giây | Chữ |
|---|---|
| 0–3 | Lãi suất sau ưu đãi / *THẢ NỔI* |
| 3–12 | ưu đãi / *[...] NĂM* / rồi sao? |
| 12–25 | kịch bản / *[...]%* / trả thêm [...] mỗi tháng |
| 25–35 | cách tính / *2 KỊCH BẢN* |
| 35–40 | nhắn / *LÃI SUẤT* |

## Mẫu làm gì khi áp
Phong cách `neon-cam` · chuyển cảnh theo chu kỳ `cut, gl-LightWipe, cut, cut, gl-Overexposure` · hiệu ứng âm tự rải theo chữ và chuyển cảnh (`mau.json`) · zoom 12% khi chữ lớn hiện (xen kẽ) · chưa có nhạc (chờ kho nhạc).

Cách dùng: app → **✦ Thư viện mẫu** → chọn mẫu → Áp mẫu. Viết cột "Chữ trên màn hình" trong `KICH-BAN.md` theo bảng trên rồi bấm **📝 Đặt chữ theo kịch bản**.

**Đã thử:** dựng video giả 10 giây (nền chuyển màu, không footage) để xem chữ, thẻ so sánh, thẻ minh hoạ. **Chưa dựng với footage của Hào**; chưa đo hiệu quả thật trên TikTok.
