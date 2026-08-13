# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html')
html = open(fn, encoding='utf-8', errors='ignore').read()
start = 45373
end = html.find('ƯU ĐÃI HOÀNG HÀ', start)
region = html[start:end + 500]
print(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', region))[:4000])
