# Cloud Edit Video (bộ khung)

Spec JSON (`videos/*.json`) → engine dựng → FFmpeg chuẩn hóa → MP4 đăng TikTok (9:16) hoặc YouTube (16:9).

| Repo | Vai trò trong bộ khung | Trạng thái kiểm thử |
|------|------------------------|---------------------|
| HyperFrames | Engine chính: HTML → MP4 | Đã render thử OK (Linux) |
| GSAP | Animation chữ trong HyperFrames | Đã render thử OK |
| three.js | Khối 3D trong HyperFrames | Đã render thử OK (WebGL phần mềm) |
| Remotion | Engine thứ hai: React → MP4 | Đã render thử OK (cần Chromium) |
| FFmpeg | Bước cuối `scripts/render.sh` | Đã chạy OK |
| Manim | Biểu đồ/số liệu động `engines/manim` | **Chưa chạy thử** (chưa cài được manim ở đây) |
| Blender MCP | Cảnh 3D, chỉ chạy local Windows | **Chưa thử**, xem `engines/blender/README.md` |

## Chạy
```bash
cd video-studio && npm install
./scripts/render.sh videos/demo.json hyperframes   # hoặc remotion, manim
# Remotion cần Chromium: BROWSER=/đường/dẫn/chromium ./scripts/render.sh videos/demo.json remotion
```
Trên GitHub: Actions → "Render video" → Run workflow (workflow này **chưa chạy thử trên GitHub**).

## App cài được (PC + điện thoại)
`app/` là PWA: tạo spec JSON. Cần host HTTPS (ví dụ GitHub Pages) mới cài được; chưa bật.
Spec mẫu `videos/demo.json` chứa chỗ trống `[...]`, thay số liệu thật có nguồn và ngày trước khi đăng.
