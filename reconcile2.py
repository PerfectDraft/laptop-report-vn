import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

data = json.load(open("raw/full/laptopgame_full.json", encoding="utf-8"))
crawled = set(i["url"] for i in data["items"])
print("file items:", len(data["items"]), "unique urls:", len(crawled))

# API /laptop collection
j = json.loads(fetch("https://laptopgame.vn/collections/laptop/products.json?page=1&limit=100"))
api_urls = set()
for p in j["products"]:
    api_urls.add("https://laptopgame.vn/" + p["alias"])
print("API urls:", len(api_urls))

# normalize by alias tail (strip -1 style suffixes? no - compare exact)
only_api = api_urls - crawled
only_html = crawled - api_urls
print("\nONLY in API (missing from file):", len(only_api))
for u in sorted(only_api):
    print("  ", u.replace("https://laptopgame.vn", ""))
print("\nONLY in HTML file (not in API):", len(only_html))
for u in sorted(only_html):
    print("  ", u.replace("https://laptopgame.vn", ""))
