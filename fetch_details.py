# -*- coding: utf-8 -*-
"""Fetch detail pages for all no1computer items, parse price + specs, save cache."""
import re, json, os, time, hashlib, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
BASE = os.path.expanduser("~/laptop-report-19m")
CACHE = os.path.join(BASE, "detail_cache")

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "vi-VN,vi;q=0.9"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

# canonical spec keys with ordered label matching (longest label first)
LABEL_ORDER = [
    ("cpu", ["cpu"]),
    ("gpu", ["card màn hình", "card man hinh", "card đồ họa", "card do hoa", "vga"]),
    ("display", ["độ phân giải", "do phan giai", "màn hình", "man hinh", "screen"]),
    ("ram", ["ram"]),
    ("storage", ["ổ cứng", "o cung", "ssd", "hdd"]),
    ("battery", ["pin", "dung lượng pin", "dung luong pin"]),
    ("weight", ["trọng lượng", "trong luong", "khối lượng", "khoi luong"]),
]

def parse_detail(html):
    d = {}
    m = re.search(r'class=[\'"]price_current bk-product-price[\'"]\s+id=[\'"]price[\'"]\s+content=[\'"](\d+)[\'"]', html)
    if m:
        d["price"] = int(m.group(1))
    else:
        m2 = re.search(r'price_current[^>]*>\s*([\d.]+)\s*(?:₫|đ)', html)
        d["price"] = int(m2.group(1).replace(".", "")) if m2 else 0
    m3 = re.search(r'price_old[^>]*>\s*([\d.]+)\s*(?:₫|đ)', html)
    d["price_old"] = int(m3.group(1).replace(".", "")) if m3 else None
    low = html.lower()
    if "ngừng kinh doanh" in low or "ngung kinh doanh" in low or "ngừng bán" in low:
        d["status"] = "ngung-kinh-doanh"
    elif "hết hàng" in low or "het hang" in low:
        d["status"] = "het-hang"
    elif "còn hàng" in low or "con hang" in low:
        d["status"] = "con-hang"
    else:
        d["status"] = "unknown"
    specs = {}
    i = html.find("Thông số kỹ thuật")
    if i < 0:
        i = html.find("Thông Số Kỹ Thuật")
    if i > 0:
        seg = html[i:i+20000]
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', seg, re.S)
        texts = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        texts = [t for t in texts if t]
        # build label->value pairs: a label is a short cell followed by a long value cell
        for j in range(len(texts) - 1):
            key = texts[j].strip().lower()
            val = texts[j + 1].strip()
            if not key or not val or len(key) > 40:
                continue
            for canon, alts in LABEL_ORDER:
                if key == alts[0] or key in alts or any(key == a.lower() for a in alts):
                    if canon not in specs and val.lower() != key and len(val) < 300:
                        specs[canon] = val
                    break
    d["specs"] = specs
    return d

def main():
    os.makedirs(CACHE, exist_ok=True)
    items = json.load(open(os.path.join(BASE, "all_items.json"), encoding="utf-8"))
    out = []
    done = 0
    fails = []
    for it in items:
        h = hashlib.md5(it["url"].encode()).hexdigest()[:12]
        cf = os.path.join(CACHE, h + ".json")
        if os.path.exists(cf):
            rec = json.load(open(cf, encoding="utf-8"))
        else:
            try:
                html = fetch(it["url"])
            except Exception as e:
                fails.append((it["url"], str(e)))
                continue
            rec = parse_detail(html)
            rec["url"] = it["url"]
            json.dump(rec, open(cf, "w", encoding="utf-8"), ensure_ascii=False)
            time.sleep(0.3)
        rec["listing_price"] = it["price"]
        rec["title"] = it["title"]
        rec["listing_status"] = it["status"]
        out.append(rec)
        done += 1
        if done % 50 == 0:
            print(f"{done}/{len(items)}", flush=True)
    json.dump(out, open(os.path.join(BASE, "details.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("DONE", len(out), "fails:", len(fails))
    for f in fails[:10]:
        print("FAIL:", f)

if __name__ == "__main__":
    main()
