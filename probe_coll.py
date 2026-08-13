import subprocess, json, time
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout
for coll in ["laptop-mong-nhe", "laptop-gaming", "laptop-gia-re"]:
    total = 0
    for page in range(1, 30):
        url = f"https://laptopgame.vn/collections/{coll}/products.json?page={page}&limit=100"
        out = fetch(url)
        try:
            j = json.loads(out)
        except Exception:
            print(coll, "page", page, "bad json")
            break
        prods = j.get("products", [])
        if not prods:
            print(f"{coll}: total pages={page-1} products={total}")
            break
        total += len(prods)
        print(f"{coll} page {page}: {len(prods)} (cum {total})")
        time.sleep(0.4)
