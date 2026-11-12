# Thư viện chuyên nghiệp (repo GitHub đã kiểm chứng)

Lập 12/11/2026. Mục đích: bộ dựng Claude Edit Video dựa trên công cụ mà giới dựng phim thật sự dùng, thay vì vá riêng từng video.

**Cách kiểm chứng:** mỗi repo được tải thẳng từ GitHub và đọc file LICENSE gốc (không dựa trang tổng hợp). Tất cả đều cho phép dùng thương mại.
**Vị trí:** `video-studio/thu-vien-chuyen-nghiep/<tên>` (git submodule, cố định phiên bản). Trên PC tải về: `git submodule update --init --depth 1`.

## Quy trình dựng chuẩn nghề (thứ tự làm của một biên tập viên)

| Bước | Việc | Công cụ trong dự án | Repo hỗ trợ |
|---|---|---|---|
| 1. Nạp & chuẩn hoá | Nhận footage, chuyển tông HDR → SDR, tạo bản nhẹ để xem | `scripts/mau.py` (HLG/PQ → BT.709, hable), proxy 540p | colour |
| 2. Chia cảnh | Tìm điểm cắt trong clip dài (flycam, đi bộ) | — | **PySceneDetect** |
| 3. Dựng thô | Sắp cảnh theo kịch bản | app timeline, `lap-storyboard` | — |
| 4. Dựng tinh (master cut) | Cắt khoảng lặng, nói vấp, chọn khúc đẹp, nhịp | `scripts/master_cut.py` | **auto-editor** (đối chiếu cách cắt) |
| 5. Chỉnh màu | Cân màu từng cảnh → áp filter (look) | `mau.py` + 9 filter trong `effects.py` | **colour** (khoa học màu, tạo LUT) |
| 6. Âm thanh | Lọc ồn giọng, cân âm lượng −14 LUFS | `loudnorm` trong `dung.py` | **DeepFilterNet** (lọc ồn), **ffmpeg-normalize** |
| 7. Đồ hoạ & chữ | Chữ động, phụ đề, minh hoạ, chuyển cảnh | HyperFrames + GSAP, `effects.py` | **gl-transitions**, **motion-canvas** |
| 8. Nâng chất | Làm chậm mượt flycam, tăng nét | — | **Practical-RIFE**, **Real-ESRGAN** (cần card RTX) |
| 9. Trao đổi | Mở timeline trong Premiere / DaVinci để chỉnh tinh | — | **OpenTimelineIO** |
| 10. Xuất & kiểm | MP4 9:16, báo cáo nghiệm thu | `dung.py`, skill `bao-cao-nghiem-thu` | — |

## Danh mục repo

| Repo | Giấy phép (đọc từ file gốc) | Cập nhật gần nhất | Giải quyết việc gì | Trạng thái trong dự án |
|---|---|---|---|---|
| [AcademySoftwareFoundation/OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Apache-2.0 | 10/11/2026 | Định dạng timeline chuẩn ngành (Pixar khởi xướng, Academy Software Foundation quản lý); đọc/ghi timeline cho Premiere, DaVinci, Final Cut | Đã thêm. Kế hoạch: nút “Xuất sang Premiere/DaVinci” |
| [gl-transitions/gl-transitions](https://github.com/gl-transitions/gl-transitions) | MIT | 09/11/2026 | 214 chuyển cảnh GLSL (lật sách, phóng chéo, rung máy, mở mống mắt…) | Đã thêm. Kế hoạch: đưa vào thư viện chuyển cảnh (dựng bằng WebGL trong HyperFrames) |
| [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | BSD-3-Clause | 09/11/2026 | Tự tìm điểm chuyển cảnh trong clip dài | Đã thêm. Kế hoạch: chia flycam dài thành cảnh trước khi master cut |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | Public domain (Unlicense) | 12/11/2026 | Tự cắt theo âm lượng/chuyển động; xuất sang Premiere/Resolve | Đã thêm. Dùng để đối chiếu, master cut của dự án đã làm phần này |
| [slhck/ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) | MIT | 09/11/2026 | Chuẩn âm lượng EBU R128 | Đã áp dụng thuật toán (bộ lọc `loudnorm` của FFmpeg, cùng cách ffmpeg-normalize làm) ở −14 LUFS |
| [Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | MIT hoặc Apache-2.0 | 06/11/2026 | Lọc ồn giọng nói (gió, xe, tiếng vang) theo thời gian thực | Đã thêm. Kế hoạch: bước “làm sạch giọng” trước khi dựng |
| [hzwer/Practical-RIFE](https://github.com/hzwer/Practical-RIFE) | MIT | 27/08/2026 | Nội suy khung hình: làm chậm mượt (slow-motion) flycam | Đã thêm. Cần card NVIDIA (PC RTX) |
| [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | BSD-3-Clause | 03/04/2024 (ổn định) | Tăng độ nét / phóng to ảnh, video | Đã thêm. Ít cần vì footage đã 4K; dùng cho ảnh phối cảnh nhỏ |
| [colour-science/colour](https://github.com/colour-science/colour) | BSD-3-Clause | 08/11/2026 | Khoa học màu: không gian màu, chuyển đổi, tạo/đọc LUT | Đã thêm. Kế hoạch: xuất filter thành file LUT `.cube` dùng được cả trong CapCut/Premiere |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | 02/07/2026 | Đồ hoạ chuyển động bằng mã (biểu đồ, sơ đồ động) | Đã thêm. Dự phòng cho minh hoạ phức tạp |

Đã có sẵn trước đó (không thêm lại): HyperFrames, Remotion, GSAP, three.js, Manim, Blender MCP, FFmpeg (xem `docs/7-repo-lam-video.md`).

## Đã áp dụng ngay trong lần này
- **Chuyển tông HDR** (footage DJI/iPhone là HLG BT.2020): nguyên nhân video bị nhạt. Áp cho video xuất, xem trước, ảnh cảnh, chấm điểm.
- **Tự cân màu từng cảnh** + **9 filter** (`tu-nhien`, `tuoi-dam`, `trong-treo`, `am-sang`, `dien-anh`, `nang-chieu`, `mat-hien-dai`, `nhat-toi-gian`, `den-trang`).
- **Âm lượng −14 LUFS** (trước đó khoảng −24 LUFS, nhỏ hơn video khác ~10 dB).
- **Phụ đề**: số điện thoại, giá, diện tích, tên riêng hiện liền một khối, tô nổi; chữ to chữ nhỏ có nền.

## Chưa làm / cần lưu ý
- Chưa tìm được bộ LUT phim (film emulation) trên GitHub có giấy phép rõ ràng để đưa vào; bộ filter hiện tại tự viết. Có thể tạo LUT từ filter bằng `colour`.
- Các repo AI (DeepFilterNet, RIFE, Real-ESRGAN) cần tải mô hình và nên chạy trên PC có card RTX; chưa thử.
- Submodule chỉ là liên kết: nội dung repo không nằm trong lịch sử của repo này.
