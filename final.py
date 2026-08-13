# -*- coding: utf-8 -*-
import re, json, os, html as htmlmod

RAW = os.path.expanduser("~/laptop-report-19m/raw")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def clean(s):
    if not s: return None
    s = htmlmod.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else None

def extract_pairs(html):
    pairs = {}
    def add(lab, val):
        lab = clean(lab); val = clean(val)
        if not lab or not val: return
        key = lab.lower()
        if key not in pairs:
            pairs[key] = val
        else:
            if len(val) > len(pairs[key]) and pairs[key] in val:
                pairs[key] = val
    for t in re.findall(r'<table[^>]*>(.*?)</table>', html, re.S):
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            c = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)
            if len(c) >= 2:
                lab = re.sub(r'<[^>]+>', '', c[0]); lab = re.sub(r'\s+', ' ', lab).strip()
                val = re.sub(r'<[^>]+>', ' ', c[1]); val = re.sub(r'\s+', ' ', val).strip()
                if lab and val and lab.lower() not in ('thông số', 'chi tiết', 'thông số kỹ thuật'):
                    add(lab, val)
    for li in re.findall(r'<li[^>]*>(.*?)</li>', html, re.S):
        text = re.sub(r'<[^>]+>', '|', li)
        parts = [p.strip() for p in text.split('|') if p.strip()]
        if len(parts) >= 2 and len(parts[0]) < 60:
            add(parts[0], ' '.join(parts[1:]))
    return pairs

def parse_detail(html):
    pairs = extract_pairs(html)
    def get(*keys):
        for k in keys:
            if k in pairs: return pairs[k]
        return None
    chip = get('chip')
    cn_cpu = get('công nghệ cpu', 'bộ xử lý', 'vi xử lý')
    sh_cpu = get('số hiệu cpu', 'số hiệu chip')
    if chip and any(x in chip.lower() for x in ('apple', 'a1', 'a2', 'm1', 'm2', 'm3', 'm4', 'm5', 'a18')):
        cpu = chip
    elif cn_cpu or sh_cpu:
        cpu = ' '.join(b for b in [cn_cpu, sh_cpu] if b)
    else:
        cpu = chip
    ram = get('ram', 'bộ nhớ', 'dung lượng ram', 'dung lượng ram, ổ cứng')
    storage = get('ổ cứng', 'dung lượng lưu trữ', 'ổ cứng mặc định', 'ổ cứng, ram', 'bộ nhớ trong', 'dung lượng ổ cứng', 'ssd', 'ổ cứng, ram, ổ cứng')
    size = get('kích thước màn hình', 'kích thước màn hình, tấm nền')
    res = get('độ phân giải', 'độ phân giải màn hình', 'chuẩn màn hình')
    tech = get('công nghệ màn hình', 'tấm nền')
    disp_parts = [p for p in [size, res, tech] if p]
    display = '; '.join(disp_parts) if disp_parts else None
    if display and display.strip() == '1': display = None
    gpu = get('chip đồ hoạ', 'chip đồ họa', 'card đồ họa', 'kiểu card đồ họa', 'gpu', 'card màn hình', 'đồ họa', 'card đồ họa, âm thanh')
    battery = get('pin', 'dung lượng pin', 'thời lượng pin', 'pin và sạc')
    weight = get('trọng lượng', 'khối lượng')
    cap = lambda s, n: (s[:n] + '…') if s and len(s) > n else s
    return clean(cap(cpu, 400)), clean(cap(ram, 200)), clean(cap(storage, 200)), clean(cap(display, 300)), clean(cap(gpu, 200)), clean(battery), clean(weight)

def battery_wh(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*wh', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

def weight_kg(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*kg', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

band = json.load(open(os.path.join(RAW, 'hoangha_band.json'), encoding='utf-8'))
# slug -> detail file
detail_files = {fn: open(os.path.join(RAW, fn), encoding='utf-8', errors='ignore').read()
                for fn in os.listdir(RAW) if fn.startswith('detail_') and fn.endswith('.html') and fn not in ('detail_probe.html', 'detail_sample.html')}

def slug_of(url):
    return re.sub(r'\W+', '_', url.rstrip('/').split('/')[-1])

results = []
for it in band:
    slug = slug_of(it['url'])
    fn = 'detail_' + slug + '.html'
    html = detail_files.get(fn, '')
    cpu, ram, storage, display, gpu, battery, weight = parse_detail(html) if html else (None,)*7
    note = it.get('note', 'còn hàng')
    # out of stock detection on detail page
    low = html.lower()
    if not html:
        note = 'hết hàng'
    elif ('chưa có sẵn' in low or 'hết hàng' in low or 'outstock' in low or 'tạm hết' in low):
        note = 'hết hàng'
    # fill from product title if spec missing
    name = it['name']
    if not cpu:
        m = re.search(r'\((.*?)\)', name)
        if m:
            seg = m.group(1)
            m2 = re.search(r'(Intel[^/]*|AMD[^/]*|Ryzen[^/]*|Core[^/]*|Apple[^/]*)', seg)
            if m2: cpu = m2.group(1).strip()
            m3 = re.search(r'(\d+GB[^/]*)', seg)
            if m3 and not ram: ram = m3.group(1).strip()
            m4 = re.search(r'(\d+GB\s*(?:SSD|HDD|NVMe)[^/]*)', seg)
            if m4 and not storage: storage = m4.group(1).strip()
    row = {
        'shop': 'hoanghamobile',
        'name': name,
        'price': it['price'],
        'url': it['url'],
        'cpu': cpu,
        'ram': ram,
        'storage': storage,
        'display': display,
        'gpu': gpu,
        'battery_wh': battery_wh(battery),
        'weight': weight_kg(weight),
        'note': note,
    }
    results.append(row)

with open(os.path.join(RAW, 'hoangha.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("SAVED", len(results))

# Verify: 5 closest to 19m
sorted_by_dist = sorted(results, key=lambda r: abs(r['price'] - 19_000_000))
print("\n5 máy gần 19tr nhất:")
for r in sorted_by_dist[:5]:
    print(f"- {r['price']:,}đ | {r['name']} | {r['cpu']} | {r['ram']} | {r['storage']} | {r['display']} | {r['gpu']} | pin={r['battery_wh']}Wh | {r['weight']}kg | {r['note']}")
# stats
h = [r for r in results if r['note'] == 'hết hàng']
print("\nTổng:", len(results), "| hết hàng:", len(h), "| còn hàng:", len(results)-len(h))
