import subprocess, re, json
UA = "Mozilla/5.0 Chrome/120.0"
def fetch(url):
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True)
    return r.stdout

targets = [
    "laptop-asus-vivobook-s-14-oled-s5406sa-pp059ws-ultra-7-258v-32gb-1tb-intel-arc-graphics-14-0inch-3k-oled-win-11-officehs24-xanh",
    "laptop-surface-pro-9-core-i5-1235u-ram-8gb-ssd-128gb-13in-2880-x-1920-120ghz",
    "laptop-surface-pro-9-wifi-core-i7-1255u-ram-16gb-ssd-256gb",
    "laptop-surface-pro-9-wifi-core-i7-1255u-ram-16gb-ssd-512gb",
]
# which collection pages mention them?
for coll in ["danh-muc-surface", "laptop-mong-nhe", "laptop", "samsung", "flash-sale"]:
    html = fetch(f"https://laptopgame.vn/{coll}")
    found = [t for t in targets if t in html]
    print(coll, "->", len(found), found if found else "")
