# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
fn = os.path.join(RAW, 'detail_dell_pro_15_pv15250.html')
html = open(fn, encoding='utf-8', errors='ignore').read()

print('len', len(html))
for pat in ['ĐĂNG KÝ NHẬN THÔNG TIN', 'Đăng ký nhận thông tin', 'MUA NGAY', 'Mua ngay', 'CHỌN MUA', 'Chọn mua', 'thêm vào giỏ', 'Thêm vào giỏ', 'Đặt hàng', 'đặt hàng', 'ĐẶT HÀNG', 'btn', 'add-to-cart', 'addCart']:
    idxs = [m.start() for m in re.finditer(pat, html)]
    print(pat, '->', idxs[:8])

# main buy area: find data-BestPrice (first occurrence after 40k)
idxs = [m.start() for m in re.finditer('data-BestPrice', html)]
print('data-BestPrice idxs:', idxs[:6])
if idxs:
    i = idxs[0]
    seg = html[i:i + 8000]
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', seg))
    # find button-ish words
    for kw in ['MUA', 'mua', 'Giỏ', 'giỏ', 'Đặt', 'đặt', 'ĐĂNG KÝ', 'Đăng ký']:
        j = txt.find(kw)
        if j > 0:
            print('KW', kw, ':', txt[max(0,j-150):j+200])
            print('---')
