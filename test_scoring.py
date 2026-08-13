#!/usr/bin/env python3
"""Unit test scoring v2 — theo review Claude:
1. Gọi ĐÚNG code production: raw_scores (Python) + computeScore/valueFactorFor (JS thật trích từ build_compact.py, chạy qua Node) — không tự viết lại công thức.
2. Test SATA SSD (tier 0 mới thêm, chưa từng có test).
3. Test invariant iGPU: bonus +10 CHỈ áp cho dGPU, iGPU không được cộng.
"""
import json, os, subprocess, sys, tempfile

BASE = os.path.expanduser("~/laptop-report-19m")
src = open(os.path.join(BASE, "build_compact.py"), encoding="utf-8").read()

# ── 1a. raw_scores thật từ Python ──
cut = src.split('HTML = """')[0]
ns = {}
exec(cut, ns)
raw_scores = ns["raw_scores"]

# ── 1b. computeScore + valueFactorFor: trích NGUYÊN VĂN 2 hàm JS thật từ source ──
def extract_js_line(key):
    i = src.index(key)
    j = src.index("\n", i)
    return src[i:j]

FUNCS = "\n".join(extract_js_line(k) for k in ("const WKEYS =", "function computeScore", "function valueFactorFor"))

# Lấy PROFS + SEGMENTS thật từ data build
data = json.load(open(os.path.join(BASE, "raw/full/_ALL_scored.json"), encoding="utf-8"))
PROFS = data["profiles"]          # {"AI / Data Science": {"w": {...}}, ...}
WKEYS = ["cpu", "ram", "gpu", "display", "battery", "storage"]

def _dummy(**over):
    base = {"_cpu_s": 60, "_ram_gb": 16, "_ram_s": 50.0, "_gpu_s": 50, "_gpu_cls": "igpu",
            "_res_s": 50, "_ref_s": 0, "_oled": False, "_size": 15.6,
            "_bat": 50, "_batt_s": 50.0, "_storage": 512, "storage": "SSD 512GB",
            "_storage_s": 65.0, "_display_s": 50.0, "_hz": 60}
    base.update(over)
    return base

def node_score(q, w, price, seg):
    """Chạy đúng 2 hàm JS thật qua Node với dữ liệu thật."""
    wj = json.dumps(w)
    qj = json.dumps(q)
    code = f"""
{FUNCS}
const r = {{q: {qj}}}; const w = {wj};
const seg = {{lo: {seg['lo']}, hi: {seg['hi']}}};
const base = computeScore(r, w);
const vf = valueFactorFor({price}, seg);
console.log(JSON.stringify({{base, vf, final: base * vf}}));
"""
    r = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        print("  NODE FAIL:", r.stderr[:300]); return None
    return json.loads(r.stdout.strip().splitlines()[-1])

passed = failed = 0
def check(name, got, want, tol=0.01):
    global passed, failed
    ok = abs(got - want) < tol
    passed += ok; failed += (not ok)
    print(f"  {'OK' if ok else 'FAIL'} {name}: got={got} want={want}")

print("=== UNIT TEST SCORING v2 (gọi code thật qua Node) ===")

# ── Test MSI Thin 15 (vấn đề 5) ──
print("\n[MSI Thin 15 B13UC - AI profile]")
msi = _dummy(_cpu_s=84, _gpu_s=72, _gpu_cls="dgpu", _res_s=70, _ref_s=88,
             storage="SSD 512GB NVMe PCIe Gen4", _storage_s=85.0, _display_s=55.0, _batt_s=50.0)
q = raw_scores(msi)
cpu, ram, gpu, disp, batt, stor = q
print(f"  raw_scores = {q}")
check("CPU", cpu, 84)
check("RAM (log2 16GB)", ram, 50.0)
check("GPU dGPU (min(100,72+10))", gpu, 82.0)
check("Display", disp, 55.0)
check("Pin (50Wh)", batt, 50.0)
check("Storage 512 NVMe4 (85x1.0)", stor, 85.0)

# Tổng cuối: dùng computeScore THẬT qua Node (không hardcode công thức)
w_ai = PROFS["AI / Data Science"]["w"]
seg15 = {"lo": 15_000_000, "hi": 20_000_000}
r = node_score(q, w_ai, 19_000_000, seg15)
check("computeScore THẬT (Node) total AI", r["base"], 71.37)
check("valueFactorFor THẬT (Node) dist 0.3", r["vf"], 0.955)
check("Final = computeScore x vf (code thật)", r["final"], 68.15)
print(f"  Node trả về: base={r['base']:.2f} vf={r['vf']:.3f} final={r['final']:.2f}")

# ── Boundary cases (giữ nguyên từ v1) ──
print("\n[Boundary cases]")
check("RAM 8GB min", raw_scores(_dummy(_ram_gb=8, _ram_s=25.0))[1], 25)
check("RAM 64GB cap", raw_scores(_dummy(_ram_gb=64, _ram_s=100.0))[1], 100)
check("RAM 128GB cap", raw_scores(_dummy(_ram_gb=128, _ram_s=100.0))[1], 100)
check("Pin 0Wh", raw_scores(_dummy(_bat=0, _batt_s=0.0))[4], 0)
check("Pin 80Wh", raw_scores(_dummy(_bat=80, _batt_s=80.0))[4], 80)
check("Pin 99Wh", raw_scores(_dummy(_bat=99, _batt_s=99.0))[4], 99)
check("Storage 2TB NVMe cap", raw_scores(_dummy(_storage=2000, storage="2TB NVMe", _storage_s=100.0))[5], 100)
check("Storage 2TB HDD cap", raw_scores(_dummy(_storage=2000, storage="2TB HDD", _storage_s=100.0))[5], 100)
check("Storage 256GB HDD", raw_scores(_dummy(_storage=256, storage="HDD 256GB", _storage_s=13.5))[5], 13.5)
check("Display 4K+240Hz+OLED+17in cap", raw_scores(_dummy(_res_s=100, _ref_s=100, _oled=True, _size=17, _display_s=100.0))[3], 100)

# ── 2. SATA SSD (tier 0 mới thêm — chưa từng có test) ──
print("\n[SATA SSD tier 0 — coverage mới]")
check("Storage 512GB SATA SSD (45x1.0)", raw_scores(_dummy(_storage=512, storage="SATA SSD 512GB", _storage_s=45.0))[5], 45.0)
check("Storage 1TB SATA SSD (45x1.08)", raw_scores(_dummy(_storage=1000, storage="SATA SSD 1TB", _storage_s=48.6))[5], 48.6)
# SATA ≠ NVMe: cùng 512GB, NVMe phải hơn SATA đúng 20đ
nv = raw_scores(_dummy(_storage=512, storage="NVMe 512GB", _storage_s=65.0))[5]
sa = raw_scores(_dummy(_storage=512, storage="SATA SSD 512GB", _storage_s=45.0))[5]
check("NVMe - SATA = +20 đúng", round(nv - sa, 1), 20.0)
# SATA false-positive: mô tả khe cắm có chữ "sata" nhưng ổ chính NVMe → vẫn NVMe3
fp = raw_scores(_dummy(_storage=512, storage="512GB PCIe 4.0 NVMe M.2 SSD (2 Khe cắm M.2 hỗ trợ SATA hoặc NVMe)", _storage_s=85.0))[5]
check("NVMe khe 'hỗ trợ SATA' KHÔNG bị trừ -> 85", fp, 85.0)
# Hybrid "SSD + HDD": ổ chính SSD → không trừ HDD (fix Perplexity review)
hyb = raw_scores(_dummy(_storage=128, storage="SSD 128GB + HDD 500GB", _storage_s=48.75))[5]
check("Hybrid SSD 128 + HDD 500 (ổ chính SSD) -> 48.8", hyb, 48.8)
# HDD đơn thuần vẫn thấp
hdd1 = raw_scores(_dummy(_storage=500, storage="HDD 500GB", _storage_s=16.2))[5]
check("HDD 500GB đơn thuần -> 16.2", hdd1, 16.2)

# ── 3. iGPU invariant: bonus +10 CHỈ cho dGPU ──
print("\n[iGPU invariant — bonus chỉ cho dGPU]")
ig = raw_scores(_dummy(_gpu_s=90, _gpu_cls="igpu"))[2]
dg = raw_scores(_dummy(_gpu_s=90, _gpu_cls="dgpu"))[2]
check("iGPU 90 KHÔNG bonus -> 90", ig, 90.0)      # case phân biệt được (không bị clamp che)
check("dGPU 90 +10 -> 100", dg, 100.0)
check("iGPU 95+ vẫn không vượt 100", raw_scores(_dummy(_gpu_s=99, _gpu_cls="igpu"))[2], 99.0)
check("iGPU 100 không thành 110->100 (invariant)", raw_scores(_dummy(_gpu_s=100, _gpu_cls="igpu"))[2], 100.0)

# ── 4. Invariant vf + weights (theo đề xuất Perplexity review mục c) ──
print("\n[vf + weights invariants]")
SEGS = [
    {"lo": 0, "hi": 10_000_000}, {"lo": 10_000_000, "hi": 15_000_000},
    {"lo": 15_000_000, "hi": 20_000_000}, {"lo": 20_000_000, "hi": 25_000_000},
    {"lo": 25_000_000, "hi": 30_000_000}, {"lo": 30_000_000, "hi": 40_000_000},
    {"lo": 40_000_000, "hi": 10**12},
]
# (a) vf luôn trong [0.85, 1.15] với mọi giá hợp lệ trong mọi band
ok_vf = True
for seg in SEGS:
    for price in [seg["lo"] + 1, (seg["lo"] + seg["hi"]) // 2, seg["hi"] - 1]:
        r = node_score([50]*6, {"cpu": .2, "ram": .2, "gpu": .2, "display": .2, "battery": .1, "storage": .1}, price, seg)
        if not (0.85 - 1e-9 <= r["vf"] <= 1.15 + 1e-9): ok_vf = False
check("vf luôn trong [0.85, 1.15] mọi band", ok_vf, True)
# (b) weights mỗi ngành sum = 1
ok_sum = all(abs(sum(p["w"].values()) - 1.0) < 1e-9 for p in PROFS.values())
check("Tổng weights mỗi ngành = 1 (6/6 ngành)", ok_sum, True)
# (c) GPU weight > 0 cho AI/Đồ họa/Game; CPU > 0 mọi ngành
for pname in ["AI / Data Science", "Đồ họa / Thiết kế", "Game / Đa phương tiện"]:
    ok_sum = ok_sum and PROFS[pname]["w"].get("gpu", 0) > 0
check("GPU weight > 0 cho AI/Đồ họa/Game", ok_sum, True)
ok_cpu = all(PROFS[p]["w"].get("cpu", 0) > 0 for p in PROFS)
check("CPU weight > 0 cho mọi ngành", ok_cpu, True)
# (d) giá ngoài mọi band (0 và 1e15) không crash, vf vẫn trong khoảng
r_lo = node_score([50]*6, {"cpu": .2, "ram": .2, "gpu": .2, "display": .2, "battery": .1, "storage": .1}, 0, SEGS[0])
r_hi = node_score([50]*6, {"cpu": .2, "ram": .2, "gpu": .2, "display": .2, "battery": .1, "storage": .1}, 10**15, SEGS[-1])
check("Giá 0 không crash, vf hợp lệ", r_lo is not None and 0.85 <= r_lo["vf"] <= 1.15, True)
check("Giá 1e15 không crash, vf hợp lệ", r_hi is not None and 0.85 <= r_hi["vf"] <= 1.15, True)

print(f"\nKết quả: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
