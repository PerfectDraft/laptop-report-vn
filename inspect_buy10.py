# -*- coding: utf-8 -*-
import re, os

RAW = os.path.expanduser("~/laptop-report-19m/raw")
for fn in ['detail_macbook_neo_256gb.html', 'detail_laptop_acer_aspire_5_a515_58m_79r7_nx_kq8sv_007.html', 'detail_dell_pro_15_pv15250.html', 'detail_laptop_gaming_hp_victus_15_fa1087tx_8c5m4pa_chinh_hang.html', 'detail_asus_vivobook_go_14_e1404fa_eb935w.html']:
    html = open(os.path.join(RAW, fn), encoding='utf-8', errors='ignore').read()
    i_sku = html.find('SKU:')
    i_bp = html.find('data-BestPrice')
    print(fn[:55], '| SKU at', i_sku, '| BestPrice at', i_bp)
    # buybox region: from SKU (or BestPrice) to 'ƯU ĐÃI HOÀNG HÀ'
    start = i_sku if i_sku > 0 else i_bp
    end = html.find('ƯU ĐÃI HOÀNG HÀ', start)
    if end < 0: end = start + 30000
    region = html[start:end]
    has_mua = 'MUA NGAY' in region
    has_reg = ('ĐĂNG KÝ NHẬN THÔNG TIN' in region) or ('Đăng ký nhận thông tin' in region)
    has_tragop = 'TRẢ GÓP' in region
    print('   region len', len(region), '| MUA NGAY:', has_mua, '| ĐĂNG KÝ:', has_reg, '| TRẢ GÓP:', has_tragop)
