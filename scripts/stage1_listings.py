#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage 1: crawl all /laptop listing pages, collect product cards (name, url, listing price)."""
import re, json, subprocess, sys, os, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT = os.path.expanduser("~/laptop-report-19m/raw/_listings.json")

def curl(url, timeout=60):
    r = subprocess.run(["curl", "-s", "-L", "--max-time", str(timeout),
                        "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", errors="replace")

def parse_items(html):
    out = []
    for m in re.finditer(r'<li class="product-item">(.*?)</li>', html, re.S):
        block = m.group(1)
        hm = re.search(r'<h3>\s*<a href="([^"]+)">(.*?)</a>\s*</h3>', block, re.S)
        pm = re.search(r'<p class="price">\s*([0-9][0-9.]*)\s*VND', block)
        if not hm: continue
        name = re.sub(r'<[^>]+>', '', hm.group(2)).strip()
        name = re.sub(r'\s+', ' ', name)
        price = int(pm.group(1).replace('.', '')) if pm else None
        # old-price presence (gạch ngang) inside card?
        oldm = re.search(r'<del>([0-9][0-9.]*)\s*VND</del>', block)
        out.append({"name": name, "url": hm.group(1).strip(), "price": price,
                    "old_price": int(oldm.group(1).replace('.', '')) if oldm else None})
    return out

def main():
    # page 1 already downloaded
    html1 = open("/tmp/hacom_laptop.html", encoding="utf-8", errors="replace").read()
    all_items = parse_items(html1)
    print("page 1:", len(all_items), "items")
    # find max page from pagination links
    pages = set(int(p) for p in re.findall(r'/laptop\?page=(\d+)', html1))
    maxp = max(pages) if pages else 1
    print("max page:", maxp)
    for p in range(2, maxp + 1):
        url = f"https://hacom.vn/laptop?page={p}"
        for attempt in range(3):
            try:
                html = curl(url)
                if not html or "product-item" not in html:
                    raise ValueError("empty/blocked")
                items = parse_items(html)
                print(f"page {p}: {len(items)} items")
                all_items.extend(items)
                break
            except Exception as e:
                print(f"page {p} attempt {attempt} failed: {e}; retrying...")
                time.sleep(3)
        else:
            print(f"page {p} FAILED after retries")
        time.sleep(0.3)
    # dedupe by url
    seen, uniq = set(), []
    for it in all_items:
        if it["url"] not in seen:
            seen.add(it["url"]); uniq.append(it)
    print("total unique:", len(uniq))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(uniq, f, ensure_ascii=False, indent=1)
    # stats
    priced = [it for it in uniq if it["price"]]
    inband = [it for it in priced if 14_000_000 <= it["price"] <= 24_000_000]
    print("priced:", len(priced), "| in band (14-24M by listing price):", len(inband))
    print("saved ->", OUT)

if __name__ == "__main__":
    main()
