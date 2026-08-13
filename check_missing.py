import subprocess, re
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

# all collection URLs from sitemap
coll = fetch("https://laptopgame.vn/sitemap_collections_1.xml")
colls = re.findall(r"<loc>(.*?)</loc>", coll)
print("collections:", colls)

# all product URLs
prod = fetch("https://laptopgame.vn/sitemap_products_1.xml")
prods = set(re.findall(r"<loc>(.*?)</loc>", prod))
print("total products in sitemap:", len(prods))

# our crawled urls
import json
data = json.load(open("raw/full/laptopgame_full.json", encoding="utf-8"))
crawled = set(i["url"] for i in data["items"])
print("crawled:", len(crawled))
missing = prods - crawled
print("in sitemap not crawled:", len(missing))
for u in sorted(missing):
    print("  MISSING:", u)
