# -*- coding: utf-8 -*-
"""Crawl no1computer.vn laptop category, filter 14-24M VND, fetch details."""
import re, json, os, time, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "vi-VN,vi;q=0.9"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

def parse_price(s):
    if not s:
        return None
    m = re.search(r"([\d.]+)", s.replace(".", "").replace(" ", ""))
    # above replace already removed dots; guard
    m = re.search(r"(\d+)", s.replace(".", "").replace(",", ""))
    return int(m.group(1)) if m else None

def parse_items(html):
    items = []
    # each product item block
    blocks = re.split(r'<div class="item cls ">', html)[1:]
    for b in blocks:
        b = b.split('</div>\n\t\t\t\t\t\t\t</div>')[0] if '</div>' in b else b
        m_url = re.search(r'<a href="(https://no1computer\.vn/[^"]+)"', b)
        m_title = re.search(r"title='([^']*)'", b)
        m_price = re.search(r"([\d.]+)\s*(?:₫|đ)", b)
        status = "het-hang" if "Hết Hàng" in b else ("con-hang" if "Còn Hàng" in b else "")
        if m_url:
            items.append({
                "url": m_url.group(1),
                "title": m_title.group(1).strip() if m_title else "",
                "price": parse_price(m_price.group(1)) if m_price else None,
                "status": status,
            })
    return items

def main():
    os.makedirs(os.path.expanduser("~/laptop-report-19m/raw"), exist_ok=True)
    all_items = []
    seen = set()
    for page in range(1, 51):
        url = "https://no1computer.vn/laptop-pc1.html" if page == 1 else f"https://no1computer.vn/laptop-pc1-page{page}.html"
        try:
            html = fetch(url)
        except Exception as e:
            print(f"page {page} FAIL: {e}")
            continue
        items = parse_items(html)
        new = 0
        for it in items:
            if it["url"] not in seen:
                seen.add(it["url"])
                all_items.append(it)
                new += 1
        print(f"page {page}: {len(items)} items ({new} new)")
        time.sleep(0.4)

    print("TOTAL items:", len(all_items))
    priced = [it for it in all_items if it["price"]]
    print("with price:", len(priced))
    in_band = [it for it in priced if 14_000_000 <= it["price"] <= 24_000_000]
    print("in band 14-24M:", len(in_band))
    with open("all_items.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=1)
    with open("in_band.json", "w", encoding="utf-8") as f:
        json.dump(in_band, f, ensure_ascii=False, indent=1)
    print("saved.")

if __name__ == "__main__":
    main()
