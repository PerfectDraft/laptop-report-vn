import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

# API authoritative list
j = json.loads(fetch("https://laptopgame.vn/collections/laptop/products.json?page=1&limit=100"))
api = set("/" + p["alias"] for p in j["products"])
print("API total:", len(api))

data = json.load(open("raw/full/laptopgame_full.json", encoding="utf-8"))
crawled = set(i["url"] for i in data["items"])
print("crawled in file:", len(crawled))

print("\n== API items MISSING from file ==")
for u in sorted(api - crawled):
    print(" ", u)

print("\n== dropped (used-filter) ==")
USED_KW = ["cũ", "like new", "thanh lý", "99%", "trưng bày", "refurb", "outlet"]
html = fetch("https://laptopgame.vn/laptop")
blocks = re.findall(r'class="product-item position-relative[^"]*">(.*?)(?=class="product-item position-relative|$)', html, re.S)
for m in re.finditer(r'<h3 class="item-title[^"]*">\s*<a[^>]*href="([^"]+)"[^>]*title="([^"]*)"', html, re.S):
    u, t = m.group(1), m.group(2)
    if any(k in t.lower() for k in USED_KW):
        print("  DROPPED:", u)

# price sanity
prices = [i["price"] for i in data["items"] if i["price"]]
print("\nprices: min", min(prices), "max", max(prices), "none:", sum(1 for i in data["items"] if not i["price"]))
