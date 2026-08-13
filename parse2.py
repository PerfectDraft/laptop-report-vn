# -*- coding: utf-8 -*-
import re, json, os, html as htmlmod

RAW = os.path.expanduser("~/laptop-report-19m/raw")

def clean(s):
    if not s: return None
    s = htmlmod.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else None

def extract_pairs(html):
    """Collect label->value pairs from spec tables and li items. Return ordered dict."""
    pairs = {}
    def add(lab, val):
        lab = clean(lab)
        val = clean(val)
        if not lab or not val: return
        key = lab.lower()
        if key not in pairs:
            pairs[key] = val
        else:
            # append short missing info (e.g. 'Trọng lượng' repeated)
            if len(val) > len(pairs[key]) and pairs[key] in val:
                pairs[key] = val
    # tables
    for t in re.findall(r'<table[^>]*>(.*?)</table>', html, re.S):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S)
        for r in rows:
            c = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)
            if len(c) >= 2:
                lab = re.sub(r'<[^>]+>', '', c[0])
                lab = re.sub(r'\s+', ' ', lab).strip()
                val = re.sub(r'<[^>]+>', ' ', c[1])
                val = re.sub(r'\s+', ' ', val).strip()
                if lab and val and lab.lower() not in ('thông số', 'chi tiết', 'thông số kỹ thuật'):
                    add(lab, val)
    # li-based spec lists: <li><span?>label</span>...<span>value</span></li> or label|value text
    for li in re.findall(r'<li[^>]*>(.*?)</li>', html, re.S):
        # split into two text parts
        text = re.sub(r'<[^>]+>', '|', li)
        parts = [p.strip() for p in text.split('|') if p.strip()]
        if len(parts) >= 2:
            lab, val = parts[0], parts[1]
            # heuristic: label short, value may span multiple parts -> join rest
            if len(lab) < 60:
                add(lab, ' '.join(parts[1:]))
    return pairs

def find_spec_table(html):
    """Find the primary spec table (the one with header Thông số / Chi tiết or most rows)."""
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.S)
    best = None
    for t in tables:
        txt = re.sub(r'<[^>]+>', ' ', t)
        if 'thông số' in txt.lower() or 'chi tiết' in txt.lower():
            return t
        n = t.count('<tr')
        if best is None or n > best[0]:
            best = (n, t)
    return best[1] if best else None

def parse_detail(html):
    pairs = extract_pairs(html)
    def get(*keys):
        for k in keys:
            if k in pairs:
                return pairs[k]
        return None

    # CPU: prefer Chip (Apple) or combine Công nghệ CPU + Số hiệu CPU
    chip = get('chip')
    cn_cpu = get('công nghệ cpu', 'bộ xử lý', 'vi xử lý')
    sh_cpu = get('số hiệu cpu', 'số hiệu chip')
    if chip and ('apple' in chip.lower() or 'a1' in chip.lower() or 'm1' in chip.lower() or 'm2' in chip.lower() or 'm3' in chip.lower() or 'm4' in chip.lower() or 'm5' in chip.lower()):
        cpu = chip
    elif cn_cpu or sh_cpu:
        bits = [b for b in [cn_cpu, sh_cpu] if b]
        cpu = ' '.join(bits)
    else:
        cpu = chip
    if cpu and len(cpu) > 400:
        cpu = cpu[:400]

    # RAM
    ram = get('ram', 'bộ nhớ', 'dung lượng ram', 'dung lượng ram, ổ cứng')
    if ram and len(ram) > 200: ram = ram[:200]

    # Storage
    storage = get('ổ cứng', 'dung lượng lưu trữ', 'ổ cứng mặc định', 'ổ cứng, ram', 'bộ nhớ trong', 'dung lượng ổ cứng', 'ssd')
    if storage and len(storage) > 200: storage = storage[:200]

    # Display: combine size + resolution + panel
    size = get('kích thước màn hình', 'kích thước màn hình, tấm nền')
    res = get('độ phân giải', 'độ phân giải màn hình', 'chuẩn màn hình')
    tech = get('công nghệ màn hình', 'tấm nền')
    disp_parts = [p for p in [size, res, tech] if p]
    display = '; '.join(disp_parts) if disp_parts else None
    # drop pure numbers like "1" (Số lượng màn hình leak) — handled by keys above
    if display and display.strip() == '1': display = None

    # GPU
    gpu = get('chip đồ hoạ', 'chip đồ họa', 'card đồ họa', 'kiểu card đồ họa', 'gpu', 'card màn hình', 'đồ họa')
    if gpu and len(gpu) > 200: gpu = gpu[:200]

    # Battery
    battery = get('pin', 'dung lượng pin', 'thời lượng pin', 'pin và sạc')
    # Weight
    weight = get('trọng lượng', 'khối lượng')
    return clean(cpu), clean(ram), clean(storage), clean(display), clean(gpu), clean(battery), clean(weight)

def battery_wh(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*wh', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

def weight_kg(s):
    if not s: return None
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*kg', s, re.I)
    return float(m.group(1).replace(',', '.')) if m else None

results = []
for fn in sorted(os.listdir(RAW)):
    if not fn.startswith('detail_') or fn.endswith('.html') is False:
        continue
    if fn in ('detail_probe.html', 'detail_sample.html'):
        continue
    html = open(os.path.join(RAW, fn), encoding='utf-8', errors='ignore').read()
    cpu, ram, storage, display, gpu, battery, weight = parse_detail(html)
    print(f"{fn[:55]:57s} | {str(cpu)[:45]:47s} | {str(ram)[:20]:22s} | {str(storage)[:22]:24s} | {str(display)[:40]}")
