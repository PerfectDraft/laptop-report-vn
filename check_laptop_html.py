import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

html = fetch("https://laptopgame.vn/laptop")
# check card structure: does it have special-price?
blocks = re.findall(r'class="product-item[^"]*">(.*?)(?=class="product-item|$)', html, re.S)
print("blocks:", len(blocks))
b = blocks[0]
pm = re.search(r'class="special-price[^"]*">\s*([\d.]+)\s*₫', b)
print("first price:", pm.group(1) if pm else None)
print(b[:1200])
