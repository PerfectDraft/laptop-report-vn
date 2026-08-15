# Vận hành chất lượng dữ liệu

## Trạng thái bản ghi

- `verified`: kiểm tra trực tiếp PDP; ghi `checkedAt`.
- `needs_review`: một hay nhiều trường thiếu, mâu thuẫn hoặc parser thiếu tin cậy.
- `stale`: quá 7 ngày với giá/tồn kho hoặc quá 30 ngày với cấu hình.
- `broken_link`: HTTP lỗi, redirect sai danh mục hoặc không còn đúng SKU.
- `out_of_stock`: PDP xác nhận hết hàng.

## Quy trình hằng ngày

1. Chạy workflow **Catalog quality audit**.
2. Ưu tiên xử lý `broken_link`, `invalid_price`, `missing_field`.
3. Đối chiếu SKU và thông số với trang PDP trước khi sửa.
4. Lưu nguồn, thời điểm kiểm tra và thay đổi thực hiện.
5. Đóng phản hồi người dùng bằng liên kết đến commit hoặc dữ liệu đã chỉnh.

## Tiêu chí mobile

- Kiểm tra 320, 375, 390, 768, 1024 và 1440 CSS px.
- Control có vùng chạm tối thiểu 44x44 px.
- Nội dung quan trọng không chỉ phân biệt bằng màu.
- Không để FAB che CTA hoặc hàng cuối.
- Ưu tiên card view khi bảng phải cuộn ngang.
