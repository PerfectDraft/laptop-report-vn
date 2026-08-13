# BÁO CÁO SỬA ĐỔI HỆ THỐNG CHẤM ĐIỂM THEO REVIEW (v2)

**Ngày:** 12/08/2026 • **Nguồn:** laptop_scoring_review.pdf + review vòng 2 từ Claude • **Trạng thái:** Đã xử lý + deploy production

---

## ✅ Bổ sung sau review vòng 2 (Claude)

### 1. Fix storage overflow (Nghiêm trọng — tái phát lỗi cũ)
- **Lỗi:** `storage_s = min(100, 40 + GB/20)` rồi cộng bonus NVMe (+8) SAU clamp → 2TB NVMe = 108 (tràn trần)
- **Fix:** gộp bonus vào `storage_raw` TRƯỚC khi clamp 1 lần duy nhất:
  ```python
  storage_raw = 40 + GB/20
  storage_s = min(100, max(0, storage_raw + bonus))  # bonus: NVMe +8 / SATA/HDD −10
  ```
- **Verify:** unit test 2TB NVMe = 100 (không còn 108) ✅ + production max component = 100 ✅

### 2. Unit test MSI Thin 15 (vấn đề 5 — "nhất quán" ≠ "đúng")
- Đã viết `test_scoring.py` — **16/16 pass**:
  - MSI Thin 15: raw_scores = [84, 40, 78, 62.2, 70, 73.6] (CPU/RAM/GPU/Display/Pin/Storage)
  - Boundary: RAM 8/64/128, Pin 0/80/99, Display 4K+240Hz+OLED+17" cap 100, Storage 2TB NVMe/HDD cap 100
- Chạy: `python test_scoring.py` → "16 passed, 0 failed"

### 3. Ghi rõ min() trong doc (RAM & Pin)
- RAM: `ram_s = min(100, 20 + 1.25×GB)` (cán 64GB)
- Pin: `batt_s = min(100, 20 + Wh×1.0)` (cán 80Wh)
- (Trước viết "cán ở X" nhưng công thức literal thiếu min() → dễ lệch code)

### 4. Storage 3 mức (điều chỉnh theo góp ý)
- NVMe/PCIe/Gen4/Gen5: **+8**
- SATA SSD: **0** (trung tính — đã tách khỏi HDD)
- HDD: **−10**

### 5. Hệ số giá trị — ví dụ tính tay
- Công thức: `vf = 1.0 ± dist×0.15`, clamp [0.85, 1.15]
- `dist = |giá − tâm band| / (band hi − band lo)` — chuẩn hoá 0–1
- Ví dụ: máy 19tr trong band 15–20tr → dist = |19−17.5|/5 = 0.3 → vf = 1.0 − 0.3×0.15 = **0.955**

### 6. Audit trọng số
- Đã verify thủ công **6/6 bộ trọng số** (AI, CNTT, ĐH, VP, Game, CAD) — Σ = 1.00 mỗi bộ
- (Claude hỏi — trả lời: đã check đủ 6, không chỉ 1)

---

## 🔥 Đã deploy production
- **`https://laptop-report-vn.vercel.app`** — bản mới nhất (fix storage overflow + test)
- Verify: max component score = 100, 27 máy 2TB clamp đúng

## Còn lại (nhỏ, không chặn production)
- [ ] Dán snippet `display_s` thật vào doc (30s — loại nghi ngờ vấn đề 2)
- [ ] Log CPU unknown để bổ sung family định kỳ

## Lệnh chạy test
```bash
cd ~/laptop-report-19m && env -u PYTHONPATH python test_scoring.py
```
