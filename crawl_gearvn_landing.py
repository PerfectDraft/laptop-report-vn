#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawl data từ 2 landing page của GearVN:
1. https://gearvn.com/pages/laptop-van-phong
2. https://gearvn.com/pages/laptop-gaming

Trích xuất danh sách sản phẩm, fetch chi tiết từng PDP (Product Detail Page),
chuẩn hoá thông số kỹ thuật (CPU, RAM, GPU, Màn hình, Pin, Ổ cứng, Tồn kho, Giá).
"""

import urllib.request
import ssl
import re
import json
import time
import os
import csv
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
}

PAGES = [
    {
        "name": "Laptop Văn Phòng",
        "url": "https://gearvn.com/pages/laptop-van-phong"
    },
    {
        "name": "Laptop Gaming",
        "url": "https://gearvn.com/pages/laptop-gaming"
    }
]

def fetch_url(url, retries=3, delay=1.0):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
                if resp.status == 200:
                    return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            # print(f"⚠️ Lỗi fetch {url} (lần {attempt+1}/{retries}): {e}")
            time.sleep(delay * (attempt + 1))
    return None

def extract_landing_products(html, category_name, landing_url):
    """Trích xuất thông tin sản phẩm từ HTML & RSC stream của landing page."""
    pushes = re.findall(r'self\.__next_f\.push\(\[(\d+),\s*"((?:[^"\\]|\\.)*)"\]\)', html)
    full_rsc = ""
    for code, p in pushes:
        try:
            full_rsc += p.encode('utf-8').decode('unicode_escape')
        except:
            full_rsc += p

    # Hỗ trợ chuỗi có chứa ký tự escape như \" trong tên sản phẩm
    matches = re.finditer(r'\{[^{}]*?"id":\s*"(\d+)"[^{}]*?"inStock":\s*(true|false)[^{}]*?"name":\s*"((?:[^"\\]|\\.)*)"[^{}]*?"originalPrice":\s*(\d+)[^{}]*?"price":\s*(\d+)[^{}]*?"slug":\s*"([^"]+)"[^{}]*?\}', full_rsc)
    
    products = {}
    for m in matches:
        slug = m.group(6)
        raw_name = m.group(3).encode('utf-8').decode('unicode_escape')
        products[slug] = {
            "id": m.group(1),
            "in_stock": m.group(2) == "true",
            "name": raw_name,
            "original_price": int(m.group(4)),
            "price": int(m.group(5)),
            "slug": slug,
            "url": f"https://gearvn.com/products/{slug}",
            "landing_category": category_name,
            "landing_url": landing_url
        }

    # Quét thêm các link /products/ nếu có trong HTML thuần
    all_slugs = re.findall(r'href=["\']/products/([^"\'\?#]+)["\']', html)
    for s in all_slugs:
        if s not in products:
            products[s] = {
                "id": None,
                "in_stock": None,
                "name": None,
                "original_price": None,
                "price": None,
                "slug": s,
                "url": f"https://gearvn.com/products/{s}",
                "landing_category": category_name,
                "landing_url": landing_url
            }

    return products

def parse_pdp_details(pdp_html, base_info):
    """Bóc tách đầy đủ cấu hình kỹ thuật từ PDP (JSON-LD + HTML fallback)."""
    item = dict(base_info)
    item["crawled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item["shop"] = "GearVN"
    
    # Defaults
    item.setdefault("brand", None)
    item.setdefault("sku", None)
    item.setdefault("cpu", None)
    item.setdefault("ram", None)
    item.setdefault("ssd", None)
    item.setdefault("gpu", None)
    item.setdefault("screen_size", None)
    item.setdefault("resolution", None)
    item.setdefault("refresh_rate", None)
    item.setdefault("battery", None)
    item.setdefault("images", [])

    # 1. Trích xuất qua JSON-LD
    json_lds = re.findall(r'<script type="application/ld\+json">([^<]+)</script>', pdp_html)
    for j_str in json_lds:
        try:
            data = json.loads(j_str)
            if data.get('@type') == 'Product':
                if data.get("name"):
                    item["name"] = data.get("name")
                if not item.get("brand") and data.get("brand"):
                    item["brand"] = data["brand"].get("name") if isinstance(data["brand"], dict) else data["brand"]
                if not item.get("sku"):
                    item["sku"] = data.get("sku")
                if data.get("image"):
                    item["images"] = data["image"] if isinstance(data["image"], list) else [data["image"]]
                
                offers = data.get("offers", {})
                if isinstance(offers, dict):
                    if item.get("price") is None and offers.get("price"):
                        item["price"] = int(offers["price"])
                    if offers.get("availability"):
                        item["in_stock"] = "InStock" in offers["availability"]
                        item["status"] = "Còn hàng" if item["in_stock"] else "Hết hàng"
                    
                    price_spec = offers.get("priceSpecification", {})
                    if isinstance(price_spec, dict) and price_spec.get("price"):
                        item["original_price"] = int(price_spec["price"])

                # additionalProperty
                for prop in data.get("additionalProperty", []):
                    p_name = prop.get("name", "").strip()
                    p_val = prop.get("value", "").strip()
                    if not p_name or not p_val:
                        continue
                    
                    p_name_lower = p_name.lower()
                    if "cpu" in p_name_lower:
                        item["cpu"] = p_val
                    elif "ram" in p_name_lower:
                        item["ram"] = p_val
                    elif "ssd" in p_name_lower or "ổ cứng" in p_name_lower:
                        item["ssd"] = p_val
                    elif "card" in p_name_lower or "đồ họa" in p_name_lower or "vga" in p_name_lower or "gpu" in p_name_lower:
                        item["gpu"] = p_val
                    elif "kích thước màn hình" in p_name_lower or "màn hình" in p_name_lower:
                        item["screen_size"] = p_val
                    elif "độ phân giải" in p_name_lower:
                        item["resolution"] = p_val
                    elif "tần số quét" in p_name_lower:
                        item["refresh_rate"] = p_val
                    elif "pin" in p_name_lower:
                        item["battery"] = p_val
        except Exception:
            pass

    # Status fallback
    if "status" not in item:
        item["status"] = "Còn hàng" if item.get("in_stock") is True else ("Hết hàng" if item.get("in_stock") is False else "Liên hệ")

    # 2. Fallback từ tiêu đề / HTML nếu thiếu cấu hình
    name = item.get("name") or ""
    
    # Fallback CPU from title
    if not item.get("cpu"):
        m_cpu = re.search(r'\b(Core\s+i\d-\w+|Core\s+Ultra\s+\d-\w+|Core\s+\d-\w+|Ryzen\s+\d\s+\w+|i[3579]-\w+|R[3579]-\w+|Apple\s+M\d\w*)', name, re.I)
        if m_cpu:
            item["cpu"] = m_cpu.group(1)

    # Fallback RAM from title
    if not item.get("ram"):
        m_ram = re.search(r'(\d+)\s*GB\b(?!\s*SSD|\s*VRAM)', name, re.I)
        if m_ram:
            item["ram"] = f"{m_ram.group(1)} GB"

    # Fallback SSD from title
    if not item.get("ssd"):
        m_ssd = re.search(r'(\d+(?:GB|TB))\s*(?:SSD|NVMe)?', name, re.I)
        if m_ssd:
            item["ssd"] = m_ssd.group(1)

    # Fallback GPU from title
    if not item.get("gpu"):
        m_gpu = re.search(r'\b(RTX\s*\d{4}(?:\s*Ti)?|GTX\s*\d{4}(?:\s*Ti)?|Intel\s+Iris\s+Xe|Intel\s+UHD|Radeon\s+\w+|Intel\s+Arc\s+\w+)', name, re.I)
        if m_gpu:
            item["gpu"] = m_gpu.group(1)

    # Fallback Screen from title
    if not item.get("screen_size"):
        m_scr = re.search(r'(\d{2}(?:\.\d)?)\s*(?:inch|[\"”])', name, re.I)
        if m_scr:
            item["screen_size"] = f"{m_scr.group(1)} inch"

    return item

def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU CÀO DỮ LIỆU TỪ 2 TRANG LANDING GEARVN")
    print("=" * 70)

    all_landing_products = {}

    for page_cfg in PAGES:
        p_name = page_cfg["name"]
        p_url = page_cfg["url"]
        print(f"\n📥 Đang tải trang danh mục: {p_name} ({p_url})...")
        html = fetch_url(p_url)
        if not html:
            print(f"❌ Không thể tải {p_url}")
            continue

        prods = extract_landing_products(html, p_name, p_url)
        print(f"✅ Tìm thấy {len(prods)} sản phẩm trong '{p_name}'")
        
        for slug, info in prods.items():
            if slug not in all_landing_products:
                all_landing_products[slug] = info
            else:
                # Ghép danh mục nếu xuất hiện ở cả 2 trang
                cur_cat = all_landing_products[slug]["landing_category"]
                if p_name not in cur_cat:
                    all_landing_products[slug]["landing_category"] = f"{cur_cat}, {p_name}"

    total_items = len(all_landing_products)
    print(f"\n📊 TỔNG CỘNG: {total_items} sản phẩm laptop duy nhất cần crawl chi tiết PDP.\n")

    # Fetch PDP cho từng sản phẩm
    detailed_products = []
    for idx, (slug, base_info) in enumerate(all_landing_products.items(), 1):
        url = base_info["url"]
        print(f"[{idx:02d}/{total_items:02d}] 🌐 Fetching PDP: {slug[:45]}...", end="", flush=True)
        pdp_html = fetch_url(url)
        if pdp_html:
            item_detail = parse_pdp_details(pdp_html, base_info)
            detailed_products.append(item_detail)
            price_str = f"{item_detail.get('price'):,}đ" if item_detail.get('price') else "N/A"
            status_str = "Còn hàng" if item_detail.get('in_stock') else "Hết hàng"
            print(f" OK | {price_str:>12} | {status_str}")
        else:
            print(" ❌ THẤT BẠI")
            detailed_products.append(base_info)
        
        # Delay lịch sự giữa các request
        time.sleep(0.4)

    # Lưu kết quả JSON
    out_json = "gearvn_crawled_products.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(detailed_products, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Đã lưu file JSON: '{out_json}' ({len(detailed_products)} máy)")

    # Lưu kết quả CSV
    out_csv = "gearvn_crawled_products.csv"
    csv_fields = [
        "name", "price", "original_price", "status", "landing_category",
        "cpu", "ram", "ssd", "gpu", "screen_size", "resolution", "refresh_rate", "battery",
        "brand", "sku", "url"
    ]
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction='ignore')
        writer.writeheader()
        for it in detailed_products:
            writer.writerow(it)
    print(f"💾 Đã lưu file CSV: '{out_csv}'")

    # In báo cáo tổng hợp
    in_stock_count = sum(1 for x in detailed_products if x.get("in_stock"))
    out_stock_count = total_items - in_stock_count
    prices = [x["price"] for x in detailed_products if x.get("price")]
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    avg_price = sum(prices) // len(prices) if prices else 0

    print("\n" + "=" * 70)
    print("📈 TỔNG KẾT KẾT QUẢ CÀO DỮ LIỆU GEARVN:")
    print(f" • Tổng số laptop: {total_items}")
    print(f" • Còn hàng: {in_stock_count} ({in_stock_count*100/total_items:.1f}%) | Hết hàng/Liên hệ: {out_stock_count}")
    print(f" • Khoảng giá: {min_price:,} đ - {max_price:,} đ (Trung bình: {avg_price:,} đ)")
    print("=" * 70)

if __name__ == "__main__":
    main()
