---
description: Quy trình điều tra và khoanh vùng sửa lỗi có hệ thống cho Laptop Report.
---

# 🔍 Workflow: Systematic Debugging

Quy trình 4 bước điều tra và khắc phục lỗi hệ thống dữ liệu, thuật toán hoặc hiển thị.

---

## 👥 Agents phụ trách:
- `debugger` (Chủ trì)
- `data-reconciler`
- `scoring-architect`

---

## Các bước xử lý:

1. **Tái hiện Lỗi (Reproduce)**:
   - Trích xuất cấu hình cụ thể hoặc sản phẩm gây ra lỗi (ví dụ: máy 2TB bị tràn điểm 108đ, máy thiếu thông số RAM).
2. **Khoanh vùng Nguyên nhân Gốc (Root Cause Analysis)**:
   - Kiểm tra mã nguồn tương ứng: `parse2.py` (lỗi bóc tách), `build_compact.py` (lỗi tính toán/render), hoặc `test_scoring.py` (lỗi kiểm thử).
3. **Viết Test Trước khi Sửa (Test-Driven Fix)**:
   - Viết một unit test case trong `test_scoring.py` tái hiện đúng lỗi đó (test phải fail trước khi sửa).
4. **Áp dụng Bản vá & Xác nhận**:
   - Sửa code, chạy lại `test_scoring.py` đến khi test pass.
   - Chạy `python .agent/scripts/checklist.py` đảm bảo không gây ra hiệu ứng phụ (regression).
