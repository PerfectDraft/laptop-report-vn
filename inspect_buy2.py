# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# 'Chọn mua' at 42720 and 'out-stock' at 22220 — inspect both
for name, i in [('Chọn mua', 42720), ('out-stock', 22220), ('dat-hang', 19841), ('Mua ngay header', 755)]:
    print('=' * 20, name, i)
    seg = html[max(0, i - 1500):i + 1200]
    print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))[:2400])
    print()
