import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

data = json.load(open("raw/full/laptopgame_full.json", encoding="utf-8"))
crawled = set(i["url"] for i in data["items"])

# sitemap product urls
prod = fetch("https://laptopgame.vn/sitemap_products_1.xml")
prods = set(re.findall(r"<loc>(.*?)</loc>", prod))

# laptop-ish = not accessories (gravastar/chuot/ban-phim/loa/tai-nghe/tui/hub/cap/bo/ke/hop/but)
accessory = re.compile(r"(gravastar|chuot|ban-phim|loa|tai-nghe|tui|hub|cong|cap|bo-thu|bo-hub|ke-tay|hop-|but-cam|test|ban-di|surface-accessory)", re.I)
laptop_urls = [u for u in prods if u != "https://laptopgame.vn/" and not accessory.search(u) and u != "https://laptopgame.vn/test"]
print("sitemap laptop-ish urls:", len(laptop_urls))
missing = [u for u in laptop_urls if u not in crawled]
print("MISSING from file:", len(missing))
for u in sorted(missing):
    print("  ", u)
