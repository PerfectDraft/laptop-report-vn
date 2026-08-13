import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

# main laptop category page
html = fetch("https://laptopgame.vn/laptop")
cards = re.findall(r'class="item-title[^"]*">\s*<a[^>]*href="([^"]+)"', html)
print("laptop page cards:", len(cards), "unique:", len(set(cards)))

# api for /laptop collection
try:
    j = json.loads(fetch("https://laptopgame.vn/collections/laptop/products.json?page=1&limit=100"))
    print("laptop API count:", len(j["products"]))
    for p in j["products"]:
        print("  ", p["alias"])
except Exception as e:
    print("laptop API failed:", e)
