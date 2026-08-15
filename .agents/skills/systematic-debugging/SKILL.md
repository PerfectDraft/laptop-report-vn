---
name: systematic-debugging
description: Phương pháp điều tra lỗi hệ thống dữ liệu, chấm điểm và giao diện một cách khoa học.
---

# 🔍 Skill: Systematic Debugging

## Các kỹ thuật điều tra lỗi:
1. **Debug Điểm số Lệch (Scoring Mismatch)**:
   - In chi tiết `raw_scores(item)` của sản phẩm.
   - Kiểm tra xem có trường nào bị clamp sai hoặc cộng bonus ngoài ý muốn không.
2. **Debug Lỗi Bóc tách Thông số (Parser Failure)**:
   - Xem nội dung thô trong `details.json` của sản phẩm đó.
   - Viết regex test độc lập để kiểm tra pattern match.
3. **Debug Render DOM / Slider Client-side**:
   - Mở Console trên trình duyệt và kiểm tra xem hàm `computeScore` hoặc `renderCard` có phát sinh exception không.
