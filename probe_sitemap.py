import subprocess, re
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

sitemap = fetch("https://laptopgame.vn/sitemap.xml")
print("sitemap head:", sitemap[:300])
smaps = re.findall(r"<loc>(.*?)</loc>", sitemap)
print("child sitemaps:", smaps)
for sm in smaps:
    if "product" in sm.lower() or "collection" in sm.lower():
        content = fetch(sm)
        locs = re.findall(r"<loc>(.*?)</loc>", content)
        print(sm, "->", len(locs), "urls")
        laps = [u for u in locs if "/laptop-" in u]
        print("  laptop urls:", len(laps), laps[:5])
