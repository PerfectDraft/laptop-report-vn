# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# The main price block on detail page: look for '<strong>' with price, then nearby buttons
for m in list(re.finditer(r'<strong>\s*[\d.,]+\s*(?:₫|đ|VNĐ)', html))[:5]:
    i = m.start()
    seg = html[max(0, i - 800):i + 2500]
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))
    print('PRICE at', i)
    print(txt[:2200])
    print('====')
