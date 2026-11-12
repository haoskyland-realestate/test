# MCP cho dự án (kết nối Claude với phần mềm khác)

MCP là cách cho Claude điều khiển phần mềm/dịch vụ khác. Mỗi máy tự bật cái mình cần; **không** bật sẵn trong repo để máy không có phần mềm đó khỏi báo lỗi.

| MCP | Máy | Dùng để | Cài |
|---|---|---|---|
| Google Drive | Mọi nơi (connector của Claude) | Đọc thư mục footage, kịch bản | Bật trong Claude: Settings → Connectors (đã bật ở phiên cloud) |
| Blender MCP | PC Windows | Dựng cảnh 3D bằng lời | Cài Blender + add-on từ github.com/ahujasid/blender-mcp, rồi `claude mcp add blender uvx blender-mcp` (cần `uv`). **Chưa thử** |

Skill của dự án nằm ở `.claude/skills/` (lap-storyboard, dung-video, bao-cao-nghiem-thu): Claude Code tự thấy khi mở repo này, trên PC, Mac hay phiên cloud.
