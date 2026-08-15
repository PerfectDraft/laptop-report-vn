# 🤖 autonomous-policy.md — Quy chế Chạy Tự động (Autonomous Mode)

Quy định phạm vi hoạt động, nguyên tắc an toàn và điều kiện dừng cho các phiên làm việc tự động không giám sát.

---

## 1. Nguyên tắc An toàn (Safety Guardrails)

1. **Bảo toàn Dữ liệu**:
   - Không được xoá hoặc ghi đè file dataset gốc `_ALL_scored.json` hoặc `details.json` nếu chưa tạo bản backup hoặc chưa kiểm tra tính hợp lệ của dữ liệu mới.
2. **Không Thay đổi Cấu trúc Ngoài Ý muốn**:
   - Các thay đổi về cấu trúc trường trong JSON phải đảm bảo tương thích ngược (Backward Compatibility) với file template HTML hiện hành.
3. **Giới hạn Thử lại (Retry Limit)**:
   - Khi cào dữ liệu gặp lỗi mạng hoặc captcha, tối đa retry 3 lần trước khi đánh dấu `failed` và chuyển sang sản phẩm tiếp theo.

---

## 2. Tiêu chí Dừng (Exit Conditions)

Một phiên làm việc autonomous được coi là hoàn thành khi và chỉ khi:
1. Toàn bộ các task trong kế hoạch đã được thực thi.
2. Script kiểm tra `python .agent/scripts/checklist.py` chạy thành công với kết quả **5/5 PASSED**.
3. File `AUTONOMOUS_LOG.md` và `PROGRESS.md` đã được cập nhật đầy đủ.

---

## 3. Quy trình Xử lý Sự cố (Rollback Protocol)
Nếu phát hiện lỗi trong quá trình chạy tự động (ví dụ: test scoring fail hoặc file HTML build bị lỗi):
1. Dừng ngay lập tức các bước tiếp theo.
2. Revert lại thay đổi gần nhất bằng Git hoặc khôi phục từ backup.
3. Ghi rõ nguyên nhân lỗi vào `AUTONOMOUS_LOG.md`.
