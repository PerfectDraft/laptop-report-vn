#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 2: fetch detail pages for pre-filtered candidates, extract price + specs."""
import re, json, subprocess, os, sys, time, html as htmlmod

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BASE = os.path.expanduser("~/laptop-report-19m/raw")

def curl(url, timeout=60):
    r = subprocess.run(["curl", "-s", "-L", "--max-time", str(timeout),
                        "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")

def clean(s):
    s = htmlmod.unescape(s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_highlights(html):
    """The summary <li><strong>label: value</strong></li> list near 'Thông số'."""
    out = []
    for m in re.finditer(r'<li><strong>(.*?)</strong></li>', html, re.S):
        t = clean(m.group(1))
        if ':' in t:
            k, v = t.split(':', 1)
            out.append((k.strip(), v.strip()))
    return out

def find_spec(pairs, highlights, keys, section=None, skip_keys=()):
    kl = [x.lower() for x in keys]
    sk = [x.lower() for x in skip_keys]
    for k, v, s in pairs:
        if section and section.lower() not in (s or '').lower(): continue
        klow = k.lower()
        if any(x in klow for x in sk): continue
        if any(x in klow for x in kl):
            return v
    for k, v in highlights:
        klow = k.lower()
        if any(x in klow for x in sk): continue
        if any(x in klow for x in kl):
            return v
    return None

def parse_spec_table(html):
    """Parse product-specs table -> ordered list of (label, value, section)."""
    m = re.search(r'<section class="product-specs">(.*?)</section>', html, re.S)
    if not m: return []
    rows = re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S)
    pairs, cur_section = [], None
    for r in rows:
        tds = re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)
        if len(tds) == 1:
            cur_section = clean(tds[0])
            continue
        if len(tds) >= 2:
            lab, val = clean(tds[0]), clean(tds[1])
            if lab and val:
                pairs.append((lab, val, cur_section))
    return pairs

def parse_detail(html):
    out = {}
    # --- price: pricing section ---
    pm = re.search(r'<section class="product-pricing">(.*?)</section>', html, re.S)
    sale = online = None
    if pm:
        seg = pm.group(1)
        ms = re.search(r'price-sale.*?itemprop="price">\s*([0-9][0-9.]*)\s*VND', seg, re.S)
        mo = re.search(r'price-online.*?<strong>([0-9][0-9.]*)\s*VND', seg, re.S)
        sale = int(ms.group(1).replace('.', '')) if ms else None
        online = int(mo.group(1).replace('.', '')) if mo else None
    cur = None
    for c in (sale, online):
        if c is not None and (cur is None or c < cur): cur = c
    out['price'] = cur
    out['price_sale'] = sale
    out['price_online'] = online
    # --- availability from JSON-LD ---
    avail = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        def walk(o):
            res = []
            if isinstance(o, dict):
                if 'availability' in o and isinstance(o.get('availability'), str):
                    res.append(o['availability'])
                for v in o.values(): res.extend(walk(v))
            elif isinstance(o, list):
                for v in o: res.extend(walk(v))
            return res
        for a in walk(d):
            if 'OutOfStock' in a: avail = 'out'
            elif 'InStock' in a and avail is None: avail = 'in'
    out['availability'] = avail
    # --- specs ---
    pairs = parse_spec_table(html)
    highs = parse_highlights(html)
    def spec(keys, section=None):
        return find_spec(pairs, highs, keys, section)
    cpu = spec(['tên bộ vi xử lý', 'cpu']) or spec(['bộ vi xử lý', 'vi xử lý', 'processor'])
    ram = spec(['dung lượng'], section='Bộ nhớ trong') or spec(['dung lượng ram', 'bộ nhớ trong', 'ram'])
    storage = spec(['dung lượng'], section='Ổ cứng') or spec(['ổ cứng', 'ssd', 'lưu trữ', 'storage'])
    disp_sec = spec(['màn hình'], section='Hiển thị', skip_keys=('độ phân giải',))
    disp_res = spec(['độ phân giải'], section='Hiển thị')
    gpu = spec(['đồ họa', 'vga', 'gpu', 'card màn hình'], skip_keys=('hdmi', 'usb-c', 'usb type'))
    bat = spec(['pin', 'battery'])
    wt = spec(['trọng lượng', 'cân nặng'])
    if gpu and gpu.lower().startswith(('1 x', '2 x', 'port', 'cổng')):
        gpu = spec(['đồ họa', 'vga', 'gpu', 'card màn hình'], skip_keys=('hdmi', 'usb-c', 'usb type'), section='Đồ Họa')
    # fallback: grab VGA/GPU from highlight list if missing
    if not gpu:
        for k, v in highs:
            kl = k.lower()
            if ('gpu' in kl or 'vga' in kl or 'đồ họa' in kl) and not any(x in kl for x in ('hdmi', 'port')):
                gpu = v
                break
    out['cpu'] = cpu
    out['ram'] = ram
    out['storage'] = storage
    out['display'] = (disp_sec + (' / ' + disp_res if disp_res and disp_res not in disp_sec else '')) if disp_sec else (disp_res or None)
    out['gpu'] = gpu
    out['battery_wh'] = bat
    out['weight'] = wt
    out['_pair_count'] = len(pairs)
    return out

def main():
    listings = json.load(open(os.path.join(BASE, '_listings.json'), encoding='utf-8'))
    # pre-filter: listing price 12.5M - 26M (wide) to catch boundary shifts after discount
    cands = [it for it in listings if it['price'] and 12_500_000 <= it['price'] <= 26_000_000]
    print(f"candidates: {len(cands)}")
    done_file = os.path.join(BASE, '_details.json')
    done = {}
    if os.path.exists(done_file):
        done = {d['url']: d for d in json.load(open(done_file, encoding='utf-8'))}
        print(f"resuming, already done: {len(done)}")
    todo = [c for c in cands if c['url'] not in done]
    for i, c in enumerate(todo):
        url = c['url']
        ok = False
        for attempt in range(3):
            try:
                h = curl(url)
                if not h or 'product-pricing' not in h:
                    raise ValueError('bad response')
                det = parse_detail(h)
                ok = True
                break
            except Exception as e:
                time.sleep(2 + attempt * 2)
        if not ok:
            print(f"[FAIL] {url}")
            continue
        rec = dict(c)
        rec.update({k: v for k, v in det.items() if k != 'price' or v is not None})
        if det['price'] is not None:
            rec['price'] = det['price']
        done[url] = rec
        if (i + 1) % 25 == 0:
            json.dump(list(done.values()), open(done_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f"progress {i+1}/{len(todo)}, done={len(done)}")
        time.sleep(0.25)
    json.dump(list(done.values()), open(done_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"FINAL done={len(done)}")

if __name__ == '__main__':
    main()
