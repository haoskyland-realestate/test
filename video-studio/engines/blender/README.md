# Blender MCP (chỉ chạy trên máy Windows local)

Blender cần giao diện/GPU nên không chạy trong GitHub Actions. Vai trò: Claude điều khiển Blender để tạo cảnh 3D, xuất **video/ảnh PNG** vào `media/`, các engine khác dùng lại làm cảnh nền hoặc cảnh chèn.

Cài (một lần):
1. Cài Blender, tải `addon.py` từ https://github.com/ahujasid/blender-mcp, bật add-on trong Blender (Edit → Preferences → Add-ons) rồi bấm Connect.
2. `claude mcp add blender uvx blender-mcp` (cần `uv`).
3. Mở Claude Code, nhờ dựng cảnh, xuất vào `video-studio/media/`.

Chưa thử trong repo này (chưa có Blender ở đây).
