# -*- coding: utf-8 -*-
"""Build final no1computer.json from detail cache."""
import re, json, os, hashlib

BASE = os.path.expanduser("~/laptop-report-19m")
CACHE = os.path.join(BASE, "detail_cache")

items = json.load(open(os.path.join(BASE, "all_items.json"), encoding="utf-8"))

NOT_NEW = re.compile(r"cũ|like\s*new|refurbished|second|máy\s*cũ|máy\s*thanh\s*lý|thanh\s*lý", re.I)

def battery_wh(s):
    if not s:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:wh|watt\s*giờ|watt-giờ)", s, re.I)
    if m:
        return float(m.group(1))
    m2 = re.search(r"(\d+(?:\.\d+)?)\s*(?:mah|mAh)", s)
    if m2:
        return round(float(m2.group(1)) * 3.7 / 1000, 1)
    return None

def clean_price(p):
    try:
        return int(p)
    except Exception:
        return None

rows = []
for it in items:
    h = hashlib.md5(it["url"].encode()).hexdigest()[:12]
    cf = os.path.join(CACHE, h + ".json")
    if not os.path.exists(cf):
        continue
    d = json.load(open(cf, encoding="utf-8"))
    price = clean_price(d.get("price")) or clean_price(d.get("listing_price"))
    title = d.get("title") or it.get("title") or ""
    if NOT_NEW.search(title):
        continue
    if not price or not (14_000_000 <= price <= 24_000_000):
        continue
    specs = d.get("specs", {})
    status = d.get("status", "")
    note = ""
    if status == "ngung-kinh-doanh":
        note = "ngừng kinh doanh"
    elif status == "het-hang":
        note = "hết hàng"
    rows.append({
        "shop": "no1computer.vn",
        "name": title.strip(),
        "price": price,
        "url": it["url"],
        "cpu": specs.get("cpu", ""),
        "ram": specs.get("ram", ""),
        "storage": specs.get("storage", ""),
        "display": specs.get("display", ""),
        "gpu": specs.get("gpu", ""),
        "battery_wh": battery_wh(specs.get("battery", "")),
        "weight": specs.get("weight", ""),
        "note": note,
    })

rows.sort(key=lambda r: r["price"])
out_path = os.path.join(BASE, "raw", "no1computer.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

print("IN BAND:", len(rows))
print("with status note:", sum(1 for r in rows if r["note"]))
# 5 closest to 19M
near = sorted(rows, key=lambda r: abs(r["price"] - 19_000_000))[:5]
for r in near:
    print(f"- {r['price']:,} | {r['name'][:70]} | {r['cpu'][:40]} | {r['ram']} | {r['storage']} | {r['display'][:45]} | {r['gpu'][:30]} | {r['weight']} | {r['note']}")
