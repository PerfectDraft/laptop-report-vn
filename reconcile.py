import subprocess, json, re, time
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

# API products
api_urls = {}
for coll in ["laptop-mong-nhe", "laptop-gaming"]:
    j = json.loads(fetch(f"https://laptopgame.vn/collections/{coll}/products.json?page=1&limit=100"))
    api_urls[coll] = set("/" + p["alias"] for p in j["products"])
    print(coll, "API count:", len(api_urls[coll]))

# HTML cards
def html_cards(coll):
    html = fetch(f"https://laptopgame.vn/{coll}")
    return re.findall(r'class="item-title[^"]*">\s*<a[^>]*href="([^"]+)"', html)

for coll in ["laptop-mong-nhe", "laptop-gaming"]:
    cards = html_cards(coll)
    uniq = set(cards)
    print(f"\n{coll}: HTML cards={len(cards)} unique={len(uniq)}")
    print("  in HTML not API:", sorted(uniq - api_urls[coll])[:15])
    print("  in API not HTML:", sorted(api_urls[coll] - uniq)[:15])
