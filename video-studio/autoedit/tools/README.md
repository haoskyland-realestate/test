# tools/: công cụ và mẫu đã chạy được

- `matte_person.py`: tách người nói thành `person.webm` có alpha (preset A, đầu nhô khỏi khung).
- `preset_A_example/src.html` + `build.py`: dự án HyperFrames mẫu của preset A (1080x1920, 5 cảnh: connect_flow, amenity_grid, note_board, tree_diagram, ảnh gộp 2x2 + nút). `build.py` ghép `src.html` thành `index.html`:
  - `python build.py guides` → có lớp vạch VÙNG AN TOÀN TikTok/Reels (chỉ để xem thử, KHÔNG dùng khi xuất bản chuẩn).
  - `python build.py` → bản sạch để render.
  - Chèn nhạc nền và sound effect (tag `<audio>`) ngay trong `build.py`.
  - Muốn dùng lại: chép sang `work/<ten>/`, sửa đường dẫn trong `build.py`, thay chữ, hình, mốc giây. `src.html` KHÔNG được nằm trong thư mục dự án HyperFrames (lint báo nhiều file gốc), hãy để ngoài thư mục `hf/`.
