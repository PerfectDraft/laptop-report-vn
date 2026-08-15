---
name: compact-builder
description: Kỹ năng nén dữ liệu ~6x và đóng gói Single-File HTML tối ưu dung lượng cho Laptop Report VN.
---

# 📦 Skill: Compact Builder

## 1. Cơ chế Nén Trường Dữ liệu (~6x)
Thay vì nhúng cả JSON đầy đủ tên trường dài vào HTML, các trường được rút gọn thành 1 ký tự:
- `n`: Tên máy (`name`)
- `p`: Giá niêm yết (`price`)
- `s`: Mã shop (`shop`)
- `u`: Đường dẫn sản phẩm (`url`)
- `c`: Thông tin CPU rút gọn
- `r`: Thông tin RAM
- `t`: Thông tin Ổ cứng (`storage`)
- `d`: Thông tin Màn hình (`display`)
- `g`: Thông tin GPU
- `k`: Trạng thái kho hàng (`stock`: `CÒN`, `HẾT`, `LIÊN HỆ`)
- `q`: Điểm thô `[cpu, ram, gpu, display, pin, storage]`
- `i`: Các thuộc tính số học `[size, res_s, oled, bat, storage_gb, ram_gb]`
- `dp`: Điểm thành phần màn hình `[ppi, hz_score, panel]`

## 2. Đóng gói HTML
Chạy `python build_compact.py` để inject thẳng mảng `ITEMS` và `PROFILES` vào script tag trong HTML template.
