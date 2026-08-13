# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# box-price at 44984 and 50616; data-BestPrice at 46264
i = 46264
print('=== data-BestPrice main at', i)
seg = html[i - 2500:i + 2000]
print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))[:3800])
