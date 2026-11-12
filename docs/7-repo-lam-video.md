# 7 repo GitHub làm video (nguồn: video TikTok "Kỹ Sư 4.0")

Ngày tổng hợp: 12/11/2026. Mô tả dưới đây là tóm tắt chung. Số sao, phiên bản và giấy phép cần kiểm tra lại trên GitHub trước khi dùng thật.

| # | Repo | Làm được gì | Ngôn ngữ / cách dùng | Hợp với Hào Sky Land ở đâu |
|---|------|-------------|----------------------|----------------------------|
| 1 | [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen) | Viết HTML/CSS + animation, xuất ra MP4. Render từng khung hình bằng Chrome không giao diện và FFmpeg, nên cùng đầu vào cho ra cùng video. Có sẵn skill cho AI agent. Apache-2.0. | Node.js 22+, FFmpeg. `npx hyperframes init my-video` | Video giới thiệu dự án, số liệu dòng tiền: Claude viết HTML, ra MP4. |
| 2 | [Remotion](https://github.com/remotion-dev/remotion) | Làm video bằng React: mỗi khung là một component. Có Studio xem trước và render ra MP4. | React, Node.js | Mẫu video lặp lại (tin dự án, bảng giá, chính sách) chỉ cần đổi dữ liệu. Giấy phép có điều kiện với công ty lớn, cần đọc kỹ nếu bán dịch vụ. |
| 3 | [three.js](https://github.com/mrdoob/three.js) | Dựng đồ họa 3D trên trình duyệt (WebGL). | JavaScript | Mô hình 3D mặt bằng, phối cảnh đơn giản, chuyển cảnh. |
| 4 | [GSAP](https://github.com/greensock/GSAP) | Thư viện animation: chuyển động chữ, số, hình mượt, điều khiển theo timeline. | JavaScript | Hiệu ứng chữ/số cho video, dùng chung với HyperFrames hoặc Remotion. |
| 5 | [Manim](https://github.com/3b1b/manim) | Dựng animation toán học và biểu đồ (của 3Blue1Brown). Có bản cộng đồng: [ManimCommunity/manim](https://github.com/ManimCommunity/manim). | Python | Minh họa dòng tiền, lãi vay, so sánh kịch bản bằng biểu đồ động. |
| 6 | [Blender MCP](https://github.com/ahujasid/blender-mcp) | Cầu nối để Claude điều khiển Blender (dựng 3D, cảnh, vật liệu) bằng lời. Add-on Blender chạy socket, MCP server nối với Claude. | Python, Blender, `claude mcp add blender uvx blender-mcp` | Cảnh 3D, quay camera quanh mô hình. Cần cài Blender, máy mạnh sẽ tốt hơn (kế hoạch PC RTX 5060). |
| 7 | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Công cụ dòng lệnh cắt, ghép, đổi định dạng, nén, thêm âm thanh. Nền cho hầu hết công cụ làm video. | Dòng lệnh | Hậu kỳ: nén video đăng Facebook/TikTok, đổi tỉ lệ 9:16, ghép phụ đề. |

## Ghi chú
- Chưa có số liệu thật về mức độ phù hợp với quy trình của Hào. Bảng "hợp ở đâu" là gợi ý, chưa thử nghiệm.
- FFmpeg trên GitHub là bản sao (mirror), nguồn chính thức ở ffmpeg.org (chưa kiểm chứng lại hôm nay).
- Chưa tải mã nguồn 7 repo về vì Blender, FFmpeg và three.js rất nặng. Cài bằng npm/pip khi cần.
