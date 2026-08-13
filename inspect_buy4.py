# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# Find main product block: typically has id="product-info" or class="info" near top with price
for pat in ['data-BestPrice', 'data-bestprice', 'box-info', 'product-info', 'info-product', 'id="info', 'price-main', 'product-price', 'box-price', 'main-price', 'detail-price', 'cau-hinh', 'btn-mua', 'btnBuyNow', 'btn-mua-ngay', 'chot-don', 'dat-hang-ngay']:
    idxs = [m.start() for m in re.finditer(pat, html, re.I)]
    print(pat, '->', idxs[:10])

# Show area 30-50k (between header and related products) — find where the main content starts
i = html.find('CAM KẾT SẢN PHẨM')
print('CAM KẾT at', i)
# find 'GIÁ CUỐI' first occurrence
j = html.find('GIÁ CUỐI')
print('GIÁ CUỐI at', j)
if j > 0:
    seg = html[max(0, j - 3000):j + 3000]
    print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))[:3500])
