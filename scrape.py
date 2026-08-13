# -*- coding: utf-8 -*-
import re, json, subprocess, sys, time, os, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
BASE = "https://hoanghamobile.com"
os.makedirs(os.path.expanduser("~/laptop-report-19m/raw"), exist_ok=True)

def fetch(url, fn):
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        return open(fn, encoding='utf-8', errors='ignore').read()
    r = subprocess.run(["curl", "-s", "-L", "-A", UA, url], capture_output=True, text=True)
    html = r.stdout
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

def parse_price(txt):
    if not txt: return None
    txt = txt.replace('\u20ab', '').replace('₫', '').replace('đ', '').strip()
    txt = txt.replace('.', '').replace(',', '')
    m = re.search(r'\d+', txt)
    return int(m.group()) if m else None

def get_items(html):
    out = []
    # split by item blocks
    blocks = re.split(r'<div class="pj16-item"', html)
    for b in blocks[1:]:
        m_name = re.search(r'<h3>\s*<a[^>]*title="([^"]+)"[^>]*href="([^"]+)"', b, re.S)
        if not m_name:
            m_name = re.search(r'<a[^>]*title="([^"]+)"[^>]*href="([^"]+)"[^>]*class="text-limit"', b, re.S)
        name = m_name.group(1).strip() if m_name else None
        url = BASE + m_name.group(2) if m_name else None
        # price: first <strong> in price div
        m_price = re.search(r'<div class="price">\s*<strong>([^<]+)</strong>', b, re.S)
        price = parse_price(m_price.group(1)) if m_price else None
        if not price:
            m_price2 = re.search(r'<strong>([\d.,]+)\s*[₫đ]</strong>', b)
            price = parse_price(m_price2.group(1)) if m_price2 else None
        # out of stock
        outstock = ('outstock' in b) or ('chưa có sẵn' in b) or ('Hết hàng' in b) or ('hết hàng' in b)
        note = 'hết hàng' if outstock else 'còn hàng'
        # specs on card
        ram = storage = None
        for li in re.finditer(r'<li class="spec-item">.*?title="([^"]+)".*?<span>\s*([^<]+?)\s*</span>', b, re.S):
            label, val = li.group(1), li.group(2).strip()
            if label == 'RAM': ram = val
            elif 'Ổ cứng' in label: storage = val
        out.append({'name': name, 'price': price, 'url': url, 'ram': ram, 'storage': storage, 'note': note, 'block': b})
    return out

def fetch_detail(url):
    fn = os.path.expanduser("~/laptop-report-19m/raw/detail_" + re.sub(r'\W+', '_', url.rstrip('/').split('/')[-1]) + ".html")
    html = fetch(url, fn)
    return html

def parse_detail(html):
    cpu = ram = storage = display = gpu = battery = weight = None
    # try spec table rows: <td>label</td><td>value</td> or dt/dd
    text = re.sub(r'<[^>]+>', '|', html)
    text = re.sub(r'\|+', '|', text)
    # simpler: search label->value pairs in table
    rows = re.findall(r'<tr[^>]*>.*?<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', html, re.S)
    if not rows:
        rows = re.findall(r'<td[^>]*>\s*<b[^>]*>([^<]+)</b>\s*</td>\s*<td[^>]*>([^<]+)</td>', html, re.S)
    for lab, val in rows:
        lab = re.sub(r'<[^>]+>', '', lab).strip().lower()
        val = re.sub(r'<[^>]+>', ' ', val).strip()
        val = re.sub(r'\s+', ' ', val)
        if 'cpu' in lab or 'vi xử lý' in lab: cpu = val
        elif 'ram' in lab and not ram: ram = val
        elif 'ổ cứng' in lab or 'ssd' in lab or 'hdd' in lab: storage = val
        elif 'màn hình' in lab or 'display' in lab: display = val
        elif 'card' in lab or 'gpu' in lab or 'đồ họa' in lab: gpu = val
        elif 'pin' in lab: battery = val
        elif 'trọng lượng' in lab or 'khối lượng' in lab: weight = val
    if not cpu:
        # fallback: definition lists
        for lab, val in re.findall(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>', html, re.S):
            lab = re.sub(r'<[^>]+>', '', lab).strip().lower()
            val = re.sub(r'<[^>]+>', ' ', re.sub(r'<[^>]+>', '', val)).strip()
            if 'cpu' in lab: cpu = val
            elif 'ram' in lab: ram = val
            elif 'ổ cứng' in lab or 'ssd' in lab: storage = val
            elif 'màn hình' in lab: display = val
            elif 'card' in lab or 'đồ họa' in lab: gpu = val
            elif 'pin' in lab: battery = val
            elif 'trọng lượng' in lab: weight = val
    def clean(s):
        return re.sub(r'\s+', ' ', s).strip() if s else None
    return clean(cpu), clean(ram), clean(storage), clean(display), clean(gpu), clean(battery), clean(weight)

def battery_wh(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*Wh', s, re.I)
    if m: return float(m.group(1).replace(',', '.'))
    # maybe watt-hour in like "52.6WHr" or "52Wh"
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*wh', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

def weight_kg(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*kg', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

def main():
    all_items = {}
    # discover pages
    p1 = fetch(BASE + "/laptop", os.path.expanduser("~/laptop-report-19m/p1.html"))
    # find max page
    pages = {1}
    for m in re.finditer(r'/laptop\?p=(\d+)', p1):
        pages.add(int(m.group(1)))
    for m in re.finditer(r'page-link[^>]*href="[^"]*p=(\d+)"', p1):
        pages.add(int(m.group(1)))
    # also try increasing pages until empty
    maxp = max(pages) if pages else 1
    # probe more pages beyond links
    for p in range(2, 30):
        fn = os.path.expanduser(f"~/laptop-report-19m/p{p}.html")
        html = fetch(BASE + f"/laptop?p={p}", fn)
        cnt = html.count('pj16-item')
        if cnt == 0:
            maxp = p - 1
            break
        maxp = p
    print("pages:", maxp)
    for p in range(1, maxp + 1):
        fn = os.path.expanduser(f"~/laptop-report-19m/p{p}.html")
        html = open(fn, encoding='utf-8', errors='ignore').read()
        for it in get_items(html):
            if it['name'] and it['price']:
                all_items[it['url']] = it
        time.sleep(0.3)
    print("total items:", len(all_items))
    band = [it for it in all_items.values() if it['price'] and 14_000_000 <= it['price'] <= 24_000_000]
    print("in band 14-24M:", len(band))
    for it in band:
        print("  ", it['price'], it['name'])
    # save band list
    with open(os.path.expanduser("~/laptop-report-19m/raw/hoangha_band.json"), 'w', encoding='utf-8') as f:
        json.dump([{k: v for k, v in it.items() if k != 'block'} for it in band], f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
