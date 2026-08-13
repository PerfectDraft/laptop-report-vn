#!/usr/bin/env python3
"""Crawl laptopgame.vn full laptop catalog -> raw/full/laptopgame_full.json
Sources: /laptop (full catalog), /laptop-mong-nhe, /laptop-gaming (subcats).
Cards are server-rendered; specs come from the prd_sum block (fallback: name).
"""
import re, json, time, sys, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BASE = "https://laptopgame.vn"
PAGES = ["/laptop", "/laptop-mong-nhe", "/laptop-gaming"]

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1:
                print(f"FAIL {url}: {e}", file=sys.stderr)
                return None
            time.sleep(2 * (i + 1))

def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()

def parse_cards(html):
    cards = []
    for m in re.finditer(r'class="product-item position-relative[^"]*">(.*?)(?=class="product-item position-relative|class="category-products|class="m_product|$)', html, re.S):
        b = m.group(1)
        tm = re.search(r'<h3 class="item-title[^"]*">\s*<a[^>]*href="([^"]+)"[^>]*title="([^"]*)"', b, re.S)
        if not tm:
            continue
        url, title = tm.group(1), clean(tm.group(2))
        pm = re.search(r'class="special-price[^"]*">\s*([\d.]+)\s*₫?', b)
        price = int(pm.group(1).replace(".", "")) if pm else None
        sm = re.search(r"<div class='rte prd_sum'>(.*?)</div>", b, re.S)
        summary = clean(re.sub(r"<[^>]+>", " ", sm.group(1))) if sm else None
        cards.append({"name": title, "price": price, "url": BASE + url if url.startswith("/") else url, "summary": summary})
    return cards

USED_KW = ["cũ", "like new", "thanh lý", "99%", "trưng bày", "refurb", "outlet"]

def parse_specs(name, summary):
    src = summary or name
    cpu = ram = storage = display = gpu = None
    # CPU from prd_sum labels or name
    m = re.search(r"CPU:\s*([^|<]{3,40})", src, re.I)
    if not m:
        m = re.search(r"(Core (?:Ultra )?i[3-9][0-9A-Za-z-]*|Core [5-9] \d{3}|Ryzen(?: AI)? [\w\s-]{2,20}|Ultra [5-9] \d{3}|Celeron[^|,(]*|Pentium[^|,(]*)", src, re.I)
    if m: cpu = clean(m.group(1).strip("|"))
    # RAM
    m = re.search(r"Ram:\s*([^|<]{3,20})", src, re.I)
    if not m:
        m = re.search(r"(\d+\s*GB(?:\s*DDR[45])?)", src, re.I)
    if m: ram = clean(m.group(1))
    # Storage
    m = re.search(r"(?:Ổ cứng|Ổ Cứng):\s*([^|<]{3,20})", src)
    if not m:
        m = re.search(r"(\d+\s*(?:GB|TB)\s*(?:SSD|HDD|NVMe)?)", src, re.I)
    if m: storage = clean(m.group(1))
    # Display
    m = re.search(r"M\.Hình:\s*([^|<]{3,25})", src)
    if not m:
        m = re.search(r"(\d{2}(?:\.\d)?\s*(?:inch|in)\s*[^|,(]*)", src, re.I)
    if m: display = clean(m.group(1).strip("|"))
    # GPU
    m = re.search(r"Card:\s*([^|<]{3,30})", src, re.I)
    if not m:
        for g in ["RTX", "GTX", "Arc", "Radeon", "Intel Graphics", "GeForce", "Graphics"]:
            mm = re.search(rf"({g}[\w\s.-]{{0,25}}?)(?=\||$|,|\()", src, re.I)
            if mm:
                gpu = clean(mm.group(1).strip("|"))
                if gpu: break
    else:
        gpu = clean(m.group(1))
    return {"cpu": cpu, "ram": ram, "storage": storage, "display": display, "gpu": gpu}

def main():
    all_items, seen = {}, []
    for page in PAGES:
        html = fetch(BASE + page)
        if not html:
            continue
        cards = parse_cards(html)
        print(f"{page}: {len(cards)} cards")
        for c in cards:
            if c["url"] not in seen:
                seen.append(c["url"])
                all_items[c["url"]] = c
        time.sleep(0.5)
    items = list(all_items.values())
    print(f"TOTAL unique: {len(items)}")

    keep = []
    for c in items:
        if any(k in c["name"].lower() for k in USED_KW):
            continue
        specs = parse_specs(c["name"], c.get("summary"))
        c.update(specs)
        keep.append(c)
    print(f"After used-filter: {len(keep)}")

    out = {"source": "laptopgame.vn", "crawled_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "items": keep}
    with open("raw/full/laptopgame_full.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("WROTE raw/full/laptopgame_full.json with", len(keep), "items")

if __name__ == "__main__":
    main()
