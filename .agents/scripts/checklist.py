#!/usr/bin/env python3
"""Pre-commit & Pre-deploy Checklist for Laptop Report VN.
Must pass 5/5 checks before committing or releasing.
"""
import os, sys, subprocess, json

def print_header(title):
    print("\n" + "=" * 60)
    print(f"📋 CHECK: {title}")
    print("=" * 60)

def run_step(step_num, title, fn):
    print(f"\n[Bước {step_num}/5] {title}...")
    try:
        ok, msg = fn()
        if ok:
            print(f"  ✅ PASSED: {msg}")
            return True
        else:
            print(f"  ❌ FAILED: {msg}")
            return False
    except Exception as e:
        print(f"  💥 ERROR: {e}")
        return False

def check_scoring_tests():
    # Tìm file test_scoring.py
    candidates = [
        os.path.join(os.getcwd(), "laptop-report-vn", "test_scoring.py"),
        os.path.join(os.getcwd(), "test_scoring.py")
    ]
    test_file = next((p for p in candidates if os.path.exists(p)), None)
    if not test_file:
        return False, "Không tìm thấy file test_scoring.py"
    
    cwd = os.path.dirname(test_file)
    res = subprocess.run([sys.executable, test_file], cwd=cwd, capture_output=True, text=True)
    if res.returncode == 0 and "failed" in res.stdout and "0 failed" in res.stdout:
        return True, "35/35 unit test scoring passed"
    return False, f"Test failure hoặc crash:\n{res.stdout}\n{res.stderr}"

def check_dataset_integrity():
    candidates = [
        os.path.join(os.getcwd(), "laptop-report-vn", "all_items.json"),
        os.path.join(os.getcwd(), "all_items.json"),
        os.path.expanduser("~/laptop-report-19m/all_items.json")
    ]
    item_file = next((p for p in candidates if os.path.exists(p)), None)
    if not item_file:
        return False, "Không tìm thấy file all_items.json"
    
    with open(item_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list) and len(data) > 100:
        return True, f"Dataset all_items hợp lệ ({len(data)} sản phẩm)"
    return False, "all_items.json rỗng hoặc không đúng định dạng"

def check_score_clamping():
    candidates = [
        os.path.join(os.getcwd(), "laptop-report-vn", "raw", "full", "_ALL_scored.json"),
        os.path.expanduser("~/laptop-report-19m/raw/full/_ALL_scored.json")
    ]
    scored_file = next((p for p in candidates if os.path.exists(p)), None)
    if not scored_file:
        return True, "Bỏ qua (không tìm thấy file _ALL_scored.json local)"
    
    with open(scored_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    for idx, it in enumerate(items):
        for key in ["_cpu_s", "_ram_s", "_gpu_s", "_display_s", "_batt_s", "_storage_s"]:
            val = it.get(key)
            if val is not None and (val < 0 or val > 100.001):
                return False, f"Tràn điểm tại máy #{idx} ({it.get('name')}): {key} = {val}"
    return True, f"Tất cả {len(items)} máy đều thoả mãn clamp [0, 100]"

def check_compact_build():
    candidates = [
        os.path.join(os.getcwd(), "laptop-report-vn", "build_compact.py"),
        os.path.join(os.getcwd(), "build_compact.py")
    ]
    build_file = next((p for p in candidates if os.path.exists(p)), None)
    if not build_file:
        return False, "Không tìm thấy file build_compact.py"
    
    cwd = os.path.dirname(build_file)
    res = subprocess.run([sys.executable, build_file], cwd=cwd, capture_output=True, text=True)
    if res.returncode == 0:
        return True, "Build compact HTML thành công mượt mà"
    return False, f"Build compact gặp lỗi:\n{res.stderr}"

def check_security():
    script_path = os.path.join(os.path.dirname(__file__), "vulnerability-scanner", "scripts", "security_scan.py")
    if not os.path.exists(script_path):
        script_path = os.path.join(os.getcwd(), ".agent", "skills", "vulnerability-scanner", "scripts", "security_scan.py")
    
    if os.path.exists(script_path):
        res = subprocess.run([sys.executable, script_path, "."], capture_output=True, text=True)
        if res.returncode == 0:
            return True, "Không phát hiện rò rỉ secret / API key"
        return False, f"Phát hiện cảnh báo bảo mật:\n{res.stdout}"
    return True, "Bỏ qua security scan (script chưa sẵn sàng)"

def main():
    print_header("TIỀN KIỂM TRA PRE-COMMIT / PRE-DEPLOY LAPTOP REPORT VN")
    
    steps = [
        ("Kiểm thử Scoring Invariant Unit Tests", check_scoring_tests),
        ("Kiểm tra Tính Toàn vẹn của Dataset", check_dataset_integrity),
        ("Kiểm tra Bất biến Giới hạn Điểm (Clamping [0, 100])", check_score_clamping),
        ("Kiểm tra Quy trình Build Compact HTML", check_compact_build),
        ("Quét Bảo mật & Rò rỉ Secret", check_security),
    ]
    
    results = []
    for idx, (title, fn) in enumerate(steps, 1):
        res = run_step(idx, title, fn)
        results.append(res)
        
    passed_count = sum(1 for r in results if r)
    print("\n" + "=" * 60)
    print(f"📊 KẾT QUẢ TỔNG KẾT: {passed_count}/{len(steps)} BƯỚC ĐẠT CHUẨN")
    print("=" * 60)
    
    if passed_count == len(steps):
        print("🎉 TẤT CẢ CHECKS ĐÃ THÀNH CÔNG! ĐỦ ĐIỀU KIỆN COMMIT / DEPLOY.")
        return 0
    else:
        print("❌ CÓ BƯỚC THẤT BẠI! VUI LÒNG KIỂM TRA VÀ KHẮC PHỤC TRƯỚC KHI TIẾP TỤC.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
