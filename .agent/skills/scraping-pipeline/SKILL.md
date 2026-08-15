---
name: scraping-pipeline
description: Kỹ năng cào dữ liệu từ 13 hệ thống bán lẻ laptop tại Việt Nam, xử lý DOM, bypass anti-bot và bóc tách thông số kỹ thuật.
---

# 🕷️ Skill: Scraping Pipeline

## 1. Danh sách 13 Đại lý & Cơ chế lấy dữ liệu
- **Thế Giới Di Động (TGDD)** & **Điện Máy Xanh**: API pagination JSON / HTML SSR.
- **FPT Shop**: GraphQL API / Search API.
- **Phong Vũ**: Algolia Search / Category API.
- **CellphoneS**: Category API (`/api/v2/category/laptop`).
- **GearVN**: Shopify Product JSON endpoint (`/products.json`).
- **Hacom**: Custom PHP HTML / Category grid.
- **ShopDunk**: Shopify API cho MacBook / Apple Silicon.
- **LaptopAZ**, **Laptop88**, **No1 Computer**, **LaptopWorld**, **LaptopGame**, **Hoàng Hà Mobile**: Custom HTML DOM parsing.

## 2. Best Practices
- Luôn gửi kèm `User-Agent` chuẩn của desktop Chrome.
- Quản lý cache tạm vào thư mục `detail_cache/` để tránh tải lại những trang đã cào trong ngày.
- Bóc tách cấu hình bằng regular expressions an toàn, có fallback khi không tìm thấy.
