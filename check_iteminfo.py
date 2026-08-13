import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

html = fetch("https://laptopgame.vn/laptop")
# find one full item-info block to see name/price markup
m = re.search(r'<div class="item-info[^"]*">.*?</div>\s*<div class=\'rte prd_sum\'>.*?</div>', html, re.S)
if m:
    print(m.group(0)[:2000])
