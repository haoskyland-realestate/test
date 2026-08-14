# Vietland — Khung web bất động sản Việt Nam cho người mua nước ngoài

Khung (scaffold) Next.js 14 + TypeScript + Tailwind CSS, phỏng theo bố cục của
một trang bất động sản quốc tế điển hình: Trang chủ có tìm kiếm + bản đồ, trang
Dự án dạng lưới có bộ lọc, trang Giới thiệu có đội ngũ, trang Liên hệ có form +
bản đồ mạng lưới văn phòng, Footer & thanh liên hệ nổi dùng chung toàn site.

> **Toàn bộ tên thương hiệu, số liệu, tên dự án và thành viên đội ngũ trong
> khung này đều là dữ liệu mẫu (hư cấu)** để bạn thấy rõ cấu trúc hoạt động.
> Hãy thay bằng nội dung thật của bạn trước khi đưa vào sử dụng.

## Chạy thử

```bash
npm install
npm run dev
```

Mở http://localhost:3000

Build production:

```bash
npm run build
npm run start
```

## Cấu trúc thư mục

```
app/
  layout.tsx          Layout gốc: nạp font, Navbar, Ticker, Footer, nút liên hệ nổi
  page.tsx             Trang chủ
  projects/page.tsx    Danh sách dự án (lọc/tìm kiếm/sắp xếp phía client)
  projects/[slug]/     Trang chi tiết 1 dự án (route động)
  about/page.tsx       Giới thiệu + đội ngũ
  contact/page.tsx     Liên hệ: form + bản đồ mạng lưới văn phòng
  not-found.tsx        Trang 404 tuỳ chỉnh
  globals.css          Tailwind + biến CSS dùng chung

components/            Toàn bộ UI tách theo component (Navbar, Hero, ProjectCard,
                        SearchWidget, Footer, OfficeNetworkMap, ContactForm...)

data/                  Dữ liệu mẫu: projects.ts, team.ts, offices.ts
```

## Tuỳ biến nhanh

- **Đổi thương hiệu**: sửa tên/logo trong `components/Navbar.tsx` và
  `components/Footer.tsx` (chữ "V" hiện là logo chữ, thay bằng ảnh logo thật
  nếu cần).
- **Đổi bảng màu / font**: sửa `tailwind.config.ts` (mục `colors`,
  `fontFamily`) — hiện đang dùng tông đỏ sơn mài + vàng gold + mực navy, font
  Fraunces (tiêu đề) + IBM Plex Sans/Mono (nội dung), nạp qua thẻ
  `<link>` Google Fonts trong `app/layout.tsx`.
- **Đổi dữ liệu dự án / đội ngũ / văn phòng**: sửa trực tiếp trong
  `data/projects.ts`, `data/team.ts`, `data/offices.ts` — toàn bộ UI đọc từ
  đây nên chỉ cần sửa dữ liệu là các trang tự cập nhật.
- **Ảnh thật**: các "ảnh" dự án và avatar hiện là khối gradient (không dùng ảnh
  thật vì đây chỉ là khung mẫu). Thay bằng `<Image>` của Next.js khi có ảnh
  thật — nhớ khai báo domain ảnh trong `next.config.mjs` nếu ảnh lấy từ nguồn
  ngoài.
- **Bản đồ "dải ruy-băng"**: `components/VietRibbon.tsx` là hoạ tiết SVG cách
  điệu (không phải bản đồ địa lý chính xác) dùng xuyên suốt Hero và Footer để
  tạo điểm nhấn nhận diện — có thể chỉnh path SVG nếu muốn hình dạng khác.

## Ghi chú kỹ thuật

- Toàn bộ import dùng đường dẫn tương đối (không dùng alias `@/...`) để đảm
  bảo build ổn định trên mọi môi trường.
- `tailwindcss` được ghim ở bản `3.x` (không dùng v4) vì cấu hình
  `tailwind.config.ts` hiện viết theo cú pháp v3.
- Đã build thử thành công với `npm run build` (16 trang tĩnh, không lỗi
  TypeScript/ESLint).
