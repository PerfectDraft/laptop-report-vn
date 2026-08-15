---
name: testing-patterns
description: Các mẫu kiểm thử nâng cao cho thuật toán chấm điểm và dữ liệu laptop.
---

# 🧪 Skill: Testing Patterns

## Các mẫu kiểm thử quan trọng:
1. **Invariant Tests**:
   - Kiểm tra xem điểm số có thoả mãn các tính chất toán học không (luôn trong đoạn $[0, 100]$, tổng trọng số $= 1.0$).
2. **Boundary Value Testing**:
   - Kiểm tra các giá trị biên: RAM 0GB, 8GB, 64GB, 128GB; Pin 0Wh, 100Wh; Dung lượng SSD 128GB, 2TB, 4TB.
3. **Cross-runtime Consistency**:
   - Thực thi cùng một dữ liệu đầu vào qua hàm Python và hàm JS trong Node.js để kiểm tra tính nhất quán 100%.
