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

- **v2.1 (13/08/2026)**: Chấm điểm PassMark chuẩn, điểm RAM/Ổ cứng/Màn hình/Pin theo chuẩn ngành, bổ sung thông số 800+ máy từ PDP, thêm ShopDunk (63 máy Mac), verify tình trạng hàng, Update Log popup

## Dữ liệu

- **Nguồn**: 13 shop VN, giá niêm yết hiện tại, cập nhật 13/08/2026
- **Điểm**: CPU/GPU PassMark log-scale, RAM log2, ổ cứng chuẩn SATA-IO/PCI-SIG/NVMe, màn hình PPI+Hz+panel (RTings/DisplayMate), pin IATA/FAA 100Wh
