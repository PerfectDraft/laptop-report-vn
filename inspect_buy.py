# -*- coding: utf-8 -*-
import re, os, json, html as htmlmod

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# Buy button region: look around the price block on the detail page
# Find 'price' related blocks near top
for pat in ['Mua ngay', 'Chọn mua', 'Đặt mua', 'mua ngay', 'outstock', 'btn-buy', 'btnBuy', 'buy', 'dat-hang', 'out-stock', 'icon-outstock', 'notify']:
    idxs = [m.start() for m in re.finditer(pat, html, re.I)]
    print(pat, '->', idxs[:8])

print()
# Find the main buy box: often <div class="box-buy"> or around price-tags-home
i = html.find('price-tags-home')
print('price-tags-home at', i)
if i > 0:
    seg = html[i:i+4000]
    print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))[:3000])
