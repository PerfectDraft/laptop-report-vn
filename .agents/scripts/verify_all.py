#!/usr/bin/env python3
"""Verify All Pipeline & Integrity for Laptop Report VN."""
import os, sys, subprocess

def main():
    print("🚀 Bắt đầu tổng kiểm tra toàn diện Laptop Report VN...")
    
    # 1. Chạy checklist
    chk = os.path.join(os.path.dirname(__file__), "checklist.py")
    res = subprocess.run([sys.executable, chk])
    if res.returncode != 0:
        print("❌ Kiểm tra checklist thất bại!")
        return 1
    
    print("\n✅ Toàn bộ hệ thống Laptop Report VN đang ở trạng thái hoàn hảo!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
