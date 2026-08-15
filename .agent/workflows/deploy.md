---
description: Quy trình đóng gói và triển khai bản release lên Vercel Production.
---

# 🚀 Workflow: Build & Deploy

Quy trình chuẩn bị và phát hành bản cập nhật cho Laptop Report VN.

---

## 👥 Agents phụ trách:
- `devops-specialist` (Chủ trì)
- `security-auditor`
- `qa-test-engineer`

---

## Các bước triển khai:

1. **Kiểm thử tiền phát hành (Pre-flight checks)**:
   ```bash
   python .agent/scripts/checklist.py
   ```
   Chỉ tiếp tục nếu kết quả là `5/5 PASSED`.

2. **Build Compact Production Artifact**:
   ```bash
   python build_compact.py
   ```
   - Xác nhận file `deploy/index.html` được cập nhật và kích thước tối ưu (~1.5MB).

3. **Kiểm tra file cấu hình Vercel**:
   - Xác nhận `deploy/vercel.json` định tuyến chính xác.

4. **Triển khai lên Vercel**:
   ```bash
   # Nếu deploy qua CLI:
   npx vercel --prod deploy
   ```
   - Kiểm tra trang live tại: `https://laptop-report-vn.vercel.app`.

5. **Ghi nhật ký phát hành**:
   - Cập nhật phiên bản mới vào `README.md` và `PROGRESS.md`.
