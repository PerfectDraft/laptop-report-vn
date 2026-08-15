---
name: parallel-agents
description: Hướng dẫn kích hoạt và phối hợp đa Agent song song theo chuyên môn trong Laptop Report VN.
---

# 👥 Skill: Parallel Agents Coordination

## Cách phối hợp Agent:
1. **Phân chia Task không giẫm chân lên nhau**:
   - `scoring-architect`: Tập trung vào file logic tính điểm `build_compact.py` (hàm scoring) và `test_scoring.py`.
   - `frontend-specialist`: Tập trung vào CSS/HTML template và client-side JS trong `build_compact.py`.
   - `crawler-specialist`: Tập trung vào crawler trong thư mục `scripts/` và `scrape.py`.
2. **Nguyên tắc Context Passing**:
   - Khi chuyển giao task giữa các Agent, luôn tóm tắt đầy đủ: Yêu cầu gốc, quyết định đã chốt, kết quả của Agent trước đó.
3. **Exit Gate Check**:
   - Luôn chạy script kiểm thử trước khi kết thúc quá trình phối hợp.
