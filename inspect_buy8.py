# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_dell_pro_15_pv15250.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

# 'MUA NGAY' at 90666 and 'đặt hàng' at 90319 — inspect
i = 90319
seg = html[i - 3000:i + 2500]
print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))[:4200])
