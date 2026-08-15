---
name: scoring-engine
description: Kỹ năng chuyên sâu về tính toán điểm chuẩn Benchmark cho CPU, GPU, RAM, Ổ cứng, Màn hình, Pin và Value Factor.
---

# 🧮 Skill: Scoring Engine

Hướng dẫn chi tiết về cấu trúc hàm và cách kiểm thử scoring.

## 1. Các hàm Python cốt lõi trong `build_compact.py`
```python
def raw_scores(rec):
    # RAM: log2 (8=25, 16=50, 32=75, 64=100)
    ram_s = rec.get("_ram_s", 0)
    # Storage: tier (HDD 15, SATA 45, NVMe3 65, NVMe4 85, NVMe5 100) x multiplier, clamped 100
    storage_s = rec.get("_storage_s", 0)
    # Pin: 100Wh = 100
    batt_s = rec.get("_batt_s", 0)
    # Display: PPI + Hz + Panel
    display_s = rec.get("_display_s", 0)
    # GPU: PassMark G3D log (KHÔNG bonus dGPU)
    gpu_eff = rec["_gpu_s"]
    return [rec["_cpu_s"], round(ram_s, 1), round(gpu_eff, 1), round(display_s, 1), round(batt_s, 1), round(storage_s, 1)]
```

## 2. Kiểm thử đồng bộ với JavaScript (Node.js)
Khi sửa đổi cách tính điểm, luôn chạy:
```bash
python test_scoring.py
```
Script sẽ tự động trích xuất code JavaScript trong `build_compact.py` và chạy qua Node.js để đối chiếu với kết quả Python, đảm bảo độ sai lệch $= 0$.
