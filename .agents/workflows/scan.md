---
description: Quy trình quét mã nguồn, dữ liệu bất thường và lỗ hổng bảo mật.
---

# 🛡️ Workflow: Security & Integrity Scan

---

## 👥 Agents phụ trách:
- `security-auditor` (Chủ trì)
- `data-reconciler`
- `qa-test-engineer`

---

## Các hạng mục quét:

1. **Quét Rò rỉ Thông tin Bí mật**:
   - Quét tìm API keys, secrets hoặc private credentials trong toàn bộ project.
2. **Quét Bất thường Dữ liệu (Data Anomalies)**:
   - Kiểm tra các sản phẩm có giá $\le 0$ hoặc $> 200.000.000$ VNĐ.
   - Kiểm tra các điểm thành phần $> 100$ hoặc $< 0$.
   - Phát hiện các sản phẩm trùng lặp URL hoặc tên gọi.
3. **Chạy Script Quét Tự Động**:
   ```bash
   python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
   ```
