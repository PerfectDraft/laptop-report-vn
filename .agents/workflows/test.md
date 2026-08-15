---
description: Quy trình kiểm thử toàn diện tính đúng đắn của dữ liệu và thuật toán chấm điểm.
---

# 🧪 Workflow: Testing & QA

Quy trình xác thực chất lượng và tính bất biến của thuật toán chấm điểm.

---

## 👥 Agents phụ trách:
- `qa-test-engineer` (Chủ trì)
- `scoring-architect`
- `debugger`

---

## Các bài test chuẩn:

1. **Chạy Unit Test Scoring**:
   ```bash
   python test_scoring.py
   ```
   - Xác thực 35 test case covering:
     - Case thực tế (MSI Thin 15 AI profile, base score, value factor, final score).
     - Case cận biên: RAM 8GB, 64GB, 128GB cap 100; Pin 0Wh, 80Wh, 99Wh; Màn hình 4K 240Hz OLED.
     - Storage tiers: NVMe vs SATA SSD vs HDD.
     - Invariant iGPU/dGPU: Card rời không nhận flat bonus làm đảo hạng.
     - Value Factor luôn nằm trong $[0.85, 1.15]$.

2. **Chạy Pre-commit Checklist**:
   ```bash
   python .agent/scripts/checklist.py
   ```

3. **Kiểm tra Toàn vẹn Dữ liệu**:
   ```bash
   python verify_final.py
   ```
