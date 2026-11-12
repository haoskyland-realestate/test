# Hệ thống làm việc AI tự động: vai trò từng nơi

File này nói **máy nào** làm gì. **AI nào** làm việc gì: `AI-NAO-VIEC-NAO.md`. Thư mục footage trên PC: `THU-MUC-VA-DAT-TEN.md`.

Theo Hào (12/11/2026). Ưu tiên miễn phí.

```
Điện thoại ──giao việc──▶ Claude (app / phiên cloud) ──mã──▶ GitHub (nguồn chính)
                                                          │
            Anti (xây phần mềm) ◀──kéo/đẩy mã──────────────┤
                                                          ▼
PC Windows 11 mạnh: tải footage, dựng video ──out/ + báo cáo──▶ Google Drive
                                                          │
Mac: đọc báo cáo, xem video, nghiệm thu ◀─────────────────┘
```

| Nơi | Vai trò | Ghi chú |
|---|---|---|
| **Anti** | Xây, sửa phần mềm | Mình hiểu là Google Antigravity, **cần Hào xác nhận**. Mở chính repo này; đọc `CLAUDE.md` và `docs/` để theo cùng quy tắc |
| **GitHub** | Nguồn chính của mã + bản v1 chạy tạm | Mọi nơi kéo/đẩy mã qua đây. Footage và video **không** để trên GitHub (quá nặng) |
| **PC Windows 11** | Máy làm việc nặng: tải footage, dựng, Blender | Chạy Claude Code tại thư mục repo (`claude remote-control` để giao việc từ điện thoại). Cài một lần: `video-studio/setup-windows.ps1` (**chưa thử**) |
| **Mac** | Đọc báo cáo, xem kết quả, nghiệm thu | Không cần cài công cụ dựng. Mở video + `*-baocao.md` từ Google Drive |
| **Điện thoại** | Giao việc, duyệt storyboard, xem nhanh | App Claude: phiên cloud hoặc phiên Remote Control của PC |
| **App desktop (Claude Desktop / Claude Code)** | Dùng skill | Skill của dự án ở `.claude/skills/`, MCP ở `docs/01-he-thong/MCP-VA-SKILL.md` |

## Luồng một video
1. Điện thoại: "Lập storyboard từ thư mục Drive <link>" → skill `lap-storyboard` → Hào duyệt.
2. PC: "Dựng video <tên>" → skill `dung-video` → `out/<tên>.mp4`.
3. PC: skill `bao-cao-nghiem-thu` → `out/<tên>-baocao.md` + ảnh khung hình.
4. Đưa `out/` sang Google Drive (thư mục đồng bộ của Google Drive cho máy tính trên PC) → Mac/điện thoại xem và nghiệm thu.
5. Hào đăng (Claude không đăng).

## Chi phí và giới hạn miễn phí (cần kiểm lại theo gói hiện tại)
- **GitHub Actions** (render trên GitHub): repo riêng tư có giới hạn số phút miễn phí mỗi tháng; video 90 giây mất khoảng 10–20 phút. Dựng chính nên chạy trên PC.
- **GitHub Pages** (app chạy tạm cho điện thoại): với repo riêng tư thường cần gói trả phí. Nếu không muốn trả: để repo công khai, hoặc dùng dịch vụ host tĩnh miễn phí khác. **Chưa kiểm** gói GitHub của Hào.
- **Google Drive**: 15 GB miễn phí, đủ cho video thành phẩm, không đủ cho kho footage 4K lâu dài.
- Claude, Anti: dùng theo gói hiện có.

## Máy (Hào xác nhận)
- PC: i5 "14800KF" (cần xem lại tên chip), RTX 5050, RAM 64 GB: đủ dựng 4K; sau này có thể dùng mã hóa video bằng card (NVENC) cho nhanh.
- Mac M1 8 GB: chỉ xem, đọc báo cáo. 8 GB RAM không hợp dựng 4K.
- Anti = Google Antigravity, chạy Claude Code bên trong nên dùng được skill `.claude/skills/`.
- Repo nội bộ: GitHub Pages cho repo riêng tư thường cần gói trả phí, nên app trên điện thoại sẽ chạy từ PC (cùng wifi) hoặc qua form GitHub Actions trên app GitHub.

## Chưa kiểm
- Chưa thử gì trên PC Windows và Mac.
- Chưa thử skill trong Anti (trong phiên Claude Code cloud thì skill đã được nhận).
