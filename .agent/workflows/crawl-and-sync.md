---
description: Quy trình cào dữ liệu từ 13 shop VN, trích xuất PDP, reconcile thông số và cập nhật điểm.
---

# 🕷️ Workflow: Crawl & Sync Data

Quy trình 4 bước chuẩn để cập nhật cơ sở dữ liệu laptop từ 13 nhà bán lẻ tại Việt Nam.

---

## 👥 Agents phụ trách:
- `crawler-specialist` (Chủ trì Cào)
- `data-reconciler` (Chuẩn hoá & Match)
- `scoring-architect` (Chấm điểm Benchmark)
- `qa-test-engineer` (Kiểm thử)

---

## Các bước thực hiện:

### Bước 1: Thu thập Danh sách Sản phẩm (Listing Stage)
```bash
python scripts/stage1_listings.py
# Hoặc chạy scraper riêng lẻ: python scrape.py
```
- Thu thập URL sản phẩm, tên, giá niêm yết, nhãn hàng.
- Lưu trữ trung gian vào `all_items.json`.

### Bước 2: Trích xuất Chi tiết Cấu hình (PDP Detail Fetching)
```bash
python scripts/stage2_details.py
# Hoặc: python fetch_details.py
```
- Lấy thông số kỹ thuật: CPU, RAM (GB, bus, loại), GPU, Màn hình (kích thước, độ phân giải, Hz, panel), Ổ cứng (NVMe/SATA, GB), Dung lượng Pin (Wh), và Tình trạng hàng (CÒN / HẾT / LIÊN HỆ).
- Lưu vào `details.json`.

### Bước 3: Chuẩn hoá, Khớp Benchmark & Chấm điểm (ETL & Scoring)
```bash
python build_json.py
# Hoặc: python parse2.py
```
- Khớp điểm CPU Mark và GPU G3D Mark từ PassMark cache (`passmark_data.json`).
- Áp dụng công thức tính điểm chuẩn theo `scoring-contract.md`.
- Xuất dữ liệu đã chấm điểm vào file `_ALL_scored.json`.

### Bước 4: Đóng gói Báo cáo & Kiểm thử
```bash
python build_compact.py
python test_scoring.py
```
- Nén dữ liệu và đóng gói ra file HTML hoàn chỉnh `bao-cao-laptop-phan-khuc.html` và `deploy/index.html`.
- Kiểm tra 35 unit test scoring.
