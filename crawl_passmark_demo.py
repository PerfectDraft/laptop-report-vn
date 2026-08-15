#!/usr/bin/env python3
"""
crawl_passmark_demo.py - Script crawl rating PassMark cho CPU, so sánh và cập nhật passmark_data.json nếu lệch >15%.
"""

import json
import os
import re
import sys
import urllib.parse
from datetime import datetime
import requests

DATA_FILE = "passmark_data.json"
TARGET_CPU = "Intel Core Ultra 5 225H"
THRESHOLD_PCT = 15.0

# Dữ liệu khởi tạo mặc định nếu passmark_data.json chưa tồn tại
# Giả lập baseline cũ cho 225H là 23,500 để demo trường hợp lệch >15% khi score thực tế xấp xỉ 28,133 (+19.7%)
DEFAULT_PASSMARK_MAP = {
    "Intel Core Ultra 5 225H": {
        "passmark_score": 23500,
        "single_thread": 3600,
        "last_updated": "2025-01-01 00:00:00",
        "note": "Baseline cũ"
    },
    "Intel Core Ultra 7 155H": {
        "passmark_score": 24800,
        "single_thread": 3800,
        "last_updated": "2025-01-01 00:00:00",
        "note": "Baseline cũ"
    },
    "AMD Ryzen 7 8845HS": {
        "passmark_score": 28900,
        "single_thread": 3950,
        "last_updated": "2025-01-01 00:00:00",
        "note": "Baseline cũ"
    }
}


def crawl_passmark_rating(cpu_name: str) -> dict:
    """Crawl rating PassMark (Multithread score & Single Thread rating) từ cpubenchmark.net"""
    encoded_name = urllib.parse.quote_plus(cpu_name)
    url = f"https://www.cpubenchmark.net/cpu.php?cpu={encoded_name}"
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"🌐 Đang kết nối tới PassMark cho '{cpu_name}'...")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ Lỗi HTTP {response.status_code} khi tải trang.")
            return None

        html = response.text
        
        # Tìm khu vực 'Average CPU Mark'
        idx = html.find("Average CPU Mark")
        if idx == -1:
            print("❌ Không tìm thấy chuỗi 'Average CPU Mark' trên trang PassMark.")
            return None

        section = html[idx:idx + 1200]
        
        # Match các khối <div style="...font-size: 44px...;">VALUE</div>
        scores = re.findall(r'<div[^>]*font-size:\s*(\d+)px[^>]*>\s*([\d,]+)\s*</div>', section)
        
        if not scores or len(scores) < 1:
            print("❌ Không tìm thấy điểm số trong HTML.")
            return None

        # multithread (CPU Mark) là điểm đầu tiên, single thread là điểm thứ 2 (nếu có)
        multi_score_str = scores[0][1].replace(",", "")
        multithread_score = int(multi_score_str)

        single_thread_score = None
        if len(scores) >= 2:
            single_score_str = scores[1][1].replace(",", "")
            single_thread_score = int(single_score_str)

        return {
            "passmark_score": multithread_score,
            "single_thread": single_thread_score,
            "crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url
        }

    except Exception as e:
        print(f"❌ Lỗi ngoại lệ khi crawl PassMark: {e}")
        return None


def load_passmark_data(filepath: str) -> dict:
    """Tải file json hiện tại, hoặc tạo mới từ DEFAULT_PASSMARK_MAP nếu chưa có."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"📂 Đã tải thành công '{filepath}' ({len(data)} chip CPUs).")
                return data
        except Exception as e:
            print(f"⚠️ Không đọc được '{filepath}': {e}. Khởi tạo map mới.")
            return dict(DEFAULT_PASSMARK_MAP)
    else:
        print(f"📄 Khởi tạo file mới '{filepath}' từ dữ liệu baseline mặc định.")
        return dict(DEFAULT_PASSMARK_MAP)


def save_passmark_data(filepath: str, data: dict):
    """Ghi dữ liệu map vào file json."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu thành công dữ liệu cập nhật vào '{filepath}'.")


def main():
    print("=" * 65)
    print(f"🚀 PASSMARK CRAWLER & COMPARISON DEMO")
    print(f"🎯 Chip cần kiểm tra : {TARGET_CPU}")
    print(f"⚡ Ngưỡng lệch cập nhật: > {THRESHOLD_PCT}%")
    print("=" * 65)

    # Step 1: Crawl PassMark mới nhất
    crawled_info = crawl_passmark_rating(TARGET_CPU)
    if not crawled_info:
        print("❌ Hủy bỏ quy trình do không crawl được dữ liệu PassMark.")
        sys.exit(1)

    new_score = crawled_info["passmark_score"]
    single_thread = crawled_info["single_thread"]
    print(f"\n✅ Crawl thành công cho {TARGET_CPU}:")
    print(f"   • PassMark CPU Mark (Multithread): {new_score:,}")
    print(f"   • Single Thread Rating           : {single_thread:,}" if single_thread else "   • Single Thread Rating: N/A")

    # Step 2: Load map hiện tại
    print("\n🔍 Đang đọc map dữ liệu hiện tại...")
    passmark_map = load_passmark_data(DATA_FILE)

    current_entry = passmark_map.get(TARGET_CPU)

    # Step 3: So sánh dữ liệu
    print("\n📊 ĐÁNH GIÁ SO SÁNH:")
    if current_entry is None:
        print(f"   • Chip '{TARGET_CPU}' CHƯA CÓ trong map hiện tại.")
        is_missing = True
        old_score = 0
        diff_pct = 100.0
    else:
        is_missing = False
        old_score = current_entry.get("passmark_score", 0)
        if old_score > 0:
            diff_pct = abs(new_score - old_score) / old_score * 100.0
        else:
            diff_pct = 100.0

        print(f"   • Score trong map hiện tại : {old_score:,}")
        print(f"   • Score mới crawl từ web   : {new_score:,}")
        print(f"   • Độ lệch tuyệt đối        : {abs(new_score - old_score):,}")
        print(f"   • Tỷ lệ lệch (Percentage)  : {diff_pct:.2f}%")

    # Step 4: Cập nhật passmark_data.json nếu lệch > 15% (hoặc chưa có chip)
    if is_missing or diff_pct > THRESHOLD_PCT:
        reason = "Chưa có trong map" if is_missing else f"Lệch {diff_pct:.2f}% (vượt ngưỡng {THRESHOLD_PCT}%)"
        print(f"\n⚠️ KẾT LUẬN: CẦN CẬP NHẬT `passmark_data.json` ({reason})")

        passmark_map[TARGET_CPU] = {
            "passmark_score": new_score,
            "single_thread": single_thread,
            "previous_score": old_score if not is_missing else None,
            "diff_percentage": round(diff_pct, 2),
            "last_updated": crawled_info["crawled_at"],
            "url": crawled_info["url"],
            "note": f"Tự động cập nhật do lệch {diff_pct:.1f}% vs baseline cũ"
        }

        save_passmark_data(DATA_FILE, passmark_map)
    else:
        print(f"\n✅ KẾT LUẬN: ĐỘ LỆCH {diff_pct:.2f}% <= {THRESHOLD_PCT}%. KHÔNG CẦN CẬP NHẬT `passmark_data.json`.")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
