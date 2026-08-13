# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
for fn in ['detail_macbook_neo_256gb.html', 'detail_laptop_asus_vivobook_14_m1405naq_ly010w.html']:
    html = open(os.path.join(RAW, fn), encoding='utf-8', errors='ignore').read()
    print('=' * 25, fn)
    for pat in ['MUA NGAY', 'Mua ngay', 'ĐĂNG KÝ NHẬN THÔNG TIN', 'Đăng ký nhận thông tin', 'TRẢ GÓP 0%', 'đặt hàng', 'Đặt hàng', 'Chọn mua', 'CHỌN MUA']:
        idxs = [m.start() for m in re.finditer(pat, html)]
        print(' ', pat, '->', idxs[:6])
