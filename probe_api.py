import subprocess, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout
# Sapo platform JSON endpoints
tests = [
    "https://laptopgame.vn/collections/laptop-mong-nhe/products.json?page=1&limit=100",
    "https://laptopgame.vn/laptop-mong-nhe/products.json?limit=100",
    "https://laptopgame.vn/sitemap.xml",
]
for t in tests:
    out = fetch(t)
    print("=== ", t)
    print("len:", len(out), "head:", out[:200].replace("\n", " "))
    try:
        j = json.loads(out)
        print("JSON ok, keys:", list(j.keys())[:5], "count:", len(j.get("products", [])))
    except Exception as e:
        print("not json:", str(e)[:80])
