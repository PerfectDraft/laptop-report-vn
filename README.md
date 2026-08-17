# 💻 Laptop VN — Báo cáo so sánh theo phân khúc giá & chuyên ngành

Báo cáo so sánh **3.364 laptop mới** từ **13 shop VN** (TGDD, FPT, PhongVũ, Hacom, No1, CellphoneS, LaptopWorld, LaptopAZ, Laptop88, LaptopGame, Hoàng Hà, GearVN, ShopDunk), xếp hạng theo 7 phân khúc giá × 6 chuyên ngành.

**Live: https://laptop-report-vn.vercel.app**

## Tính năng

- 🔍 **3.364 máy** — thông số đầy đủ CPU/RAM/SSD/Màn hình/GPU/Pin (coverage ~99.8%)
- 🎯 **7 phân khúc giá** — dưới 10tr → 40tr+
- 🎓 **6 chuyên ngành** — AI/Data Science, Lập trình/CNTT, Đồ họa/Thiết kế, Kinh tế/Văn phòng, Game/Đa phương tiện, Cơ khí/CAD
- 🏆 **Điểm chuẩn PassMark** — CPU/GPU theo benchmark thật (cpubenchmark.net), không ước lượng chủ quan
- 📊 **Điểm tiêu chí chuẩn ngành** — RAM log2, SSD NVMe/SATA/HDD, màn hình PPI + tần số quét + OLED, pin theo giới hạn hàng không 100Wh
- 📦 **Tình trạng hàng verify PDP** — Còn hàng / Sắp về hàng / Hết hàng từ trang chính hãng
- 🎛️ **Tự chỉnh trọng số** — kéo slider đổi tầm quan trọng từng tiêu chí, áp dụng & xếp hạng lại
- 🙈 **Ẩn máy hết hàng** — bỏ máy không mua được (vẫn xếp điểm khi bật lại)
- 📋 **Update Log** — bấm ⓘ góc phải header xem lịch sử cập nhật & hướng dẫn

## Cách chạy

```bash
# Build report (đọc raw/full/_ALL_scored.json)
python build_compact.py
# -> tạo bao-cao-laptop-phan-khuc.html

# Test scoring (35 tests)
python test_scoring.py
```

## Cấu trúc

```
build_compact.py          # Build report HTML (scoring + render)
test_scoring.py           # Unit test scoring (gọi code thật qua Node)
deploy/index.html         # Bản deploy lên Vercel
bao-cao-laptop-phan-khuc.html  # Report build local
raw/full/_ALL_scored.json # Dataset 3371 máy đã chấm điểm (local, không push)
```

## Cập nhật

- **v2.10 (17/08/2026)**: Kiểm toán 100% thông số màn hình (Size, Resolution, Hz, Panel, Touch), sửa triệt để lỗi điểm màn hình 0/100 trong Modal chi tiết, phục hồi nhận diện vi xử lý và card đồ họa từ tiêu đề sản phẩm.
- **v2.9 (17/08/2026)**: Sửa 100% link hỏng 13 shop sang Direct PDP, tích hợp hệ thống báo lỗi nhanh 🚩, Gamification +50 XP, Thẻ vinh danh 3D & Bảng quản lý báo cáo xuất file Excel CSV.
- **v2.8 (17/08/2026)**: Cào dữ liệu GearVN landing page, tích hợp PassMark AMD Ryzen AI 300, Intel Ultra 200V, RTX 50 Mobile Series, mở rộng dataset lên 3.379 máy.
- **v2.5 (16/08/2026)**: Tìm kiếm tức thì Real-time Search, mở rộng Slider 100%, XSS escaping, sửa fallback RAM/SSD.

## Dữ liệu

- **Nguồn**: 13 shop VN (TGDD, FPT, Phong Vũ, Hacom, No1, CellphoneS, LaptopWorld, LaptopAZ, Laptop88, LaptopGame, Hoàng Hà, GearVN, ShopDunk), giá niêm yết hiện tại, cập nhật 17/08/2026
- **Điểm**: CPU/GPU PassMark log-scale, RAM log2, ổ cứng chuẩn SATA-IO/PCI-SIG/NVMe, màn hình PPI+Hz+panel (RTings/DisplayMate), pin IATA/FAA 100Wh

