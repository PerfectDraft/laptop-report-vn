# -*- coding: utf-8 -*-
import re, json, subprocess, time, os, html as htmlmod

BASE = "https://hoanghamobile.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
RAW = os.path.expanduser("~/laptop-report-19m/raw")

def fetch(url, fn):
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        return open(fn, encoding='utf-8', errors='ignore').read()
    r = subprocess.run(["curl", "-s", "-L", "-A", UA, url], capture_output=True, text=True)
    html = r.stdout
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

def clean(s):
    if not s: return None
    s = htmlmod.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else None

def parse_detail(html):
    cpu = ram = storage = display = gpu = battery = weight = None
    # Spec table: <td>label</td><td>value</td> patterns (various)
    row_pats = [
        r'<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',
        r'<td[^>]*class="[^"]*label[^"]*"[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',
        r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>',
        r'<li[^>]*>\s*<span[^>]*class="[^"]*name[^"]*"[^>]*>(.*?)</span>\s*<span[^>]*>(.*?)</span>',
        r'<div[^>]*class="[^"]*spec-name[^"]*"[^>]*>(.*?)</div>\s*<div[^>]*class="[^"]*spec-value[^"]*"[^>]*>(.*?)</div>',
        r'<b[^>]*>(.*?)</b>\s*:\s*(.*?)<br',
    ]
    rows = []
    for pat in row_pats:
        rows = re.findall(pat, html, re.S | re.I)
        if rows: break
    def map_label(lab):
        lab = re.sub(r'<[^>]+>', '', lab)
        lab = htmlmod.unescape(lab).strip().lower()
        lab = re.sub(r'\s+', ' ', lab)
        return lab
    def map_val(val):
        val = re.sub(r'<[^>]+>', ' ', val)
        val = htmlmod.unescape(val)
        return re.sub(r'\s+', ' ', val).strip()
    for lab, val in rows:
        lab = map_label(lab)
        val = map_val(val)
        if not val: continue
        if 'cpu' in lab or 'vi xử lý' in lab or 'bộ xử lý' in lab:
            cpu = cpu or val
        elif 'ram' in lab:
            ram = ram or val
        elif 'ổ cứng' in lab or 'ssd' in lab or 'hdd' in lab or 'bộ nhớ trong' in lab or 'lưu trữ' in lab:
            storage = storage or val
        elif 'màn hình' in lab or 'display' in lab:
            display = display or val
        elif 'card' in lab or 'gpu' in lab or 'đồ họa' in lab or 'vga' in lab:
            gpu = gpu or val
        elif 'pin' in lab:
            battery = battery or val
        elif 'trọng lượng' in lab or 'khối lượng' in lab or 'weight' in lab:
            weight = weight or val
    return clean(cpu), clean(ram), clean(storage), clean(display), clean(gpu), clean(battery), clean(weight)

def battery_wh(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*wh', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

def weight_kg(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*kg', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

band = json.load(open(os.path.join(RAW, 'hoangha_band.json'), encoding='utf-8'))
print("band size:", len(band))
results = []
for i, it in enumerate(band):
    slug = it['url'].rstrip('/').split('/')[-1]
    fn = os.path.join(RAW, 'detail_' + re.sub(r'\W+', '_', slug) + '.html')
    try:
        html = fetch(it['url'], fn)
    except Exception as e:
        print("ERR fetch", it['url'], e)
        continue
    cpu, ram, storage, display, gpu, battery, weight = parse_detail(html)
    # out of stock on detail page
    note = it.get('note', 'còn hàng')
    if 'outstock' in html or 'chưa có sẵn' in html or 'Hết hàng' in html:
        if 'còn hàng' in note: note = 'hết hàng'
    row = {
        'shop': 'hoanghamobile',
        'name': it['name'],
        'price': it['price'],
        'url': it['url'],
        'cpu': cpu,
        'ram': ram or it.get('ram'),
        'storage': storage or it.get('storage'),
        'display': display,
        'gpu': gpu,
        'battery_wh': battery_wh(battery),
        'weight': weight_kg(weight),
        'note': note,
    }
    results.append(row)
    print(f"{i+1}/{len(band)} {row['price']} {row['name'][:60]} | cpu={row['cpu']} | ram={row['ram']} | disk={row['storage']} | disp={row['display']} | gpu={row['gpu']} | bat={row['battery_wh']} | wt={row['weight']}")
    time.sleep(0.4)

with open(os.path.join(RAW, 'hoangha.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("SAVED", len(results))
