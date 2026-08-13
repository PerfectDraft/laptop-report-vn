import re, subprocess
UA = "Mozilla/5.0 Chrome/120.0"
def get(cat, p):
    url = f"https://laptopgame.vn/{cat}" + (f"?page={p}" if p > 1 else "")
    html = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url], capture_output=True, text=True).stdout
    return re.findall(r'class="item-title[^"]*">\s*<a[^>]*href="([^"]+)"', html)
mn1 = get("laptop-mong-nhe", 1)
mn2 = get("laptop-mong-nhe", 2)
g1 = get("laptop-gaming", 1)
g2 = get("laptop-gaming", 2)
print("mong-nhe p1:", len(mn1), "unique:", len(set(mn1)))
print("mong-nhe p2:", len(mn2), "unique:", len(set(mn2)))
print("gaming p1:", len(g1), "unique:", len(set(g1)))
print("gaming p2:", len(g2), "unique:", len(set(g2)))
s = lambda a, b: len(set(a).intersection(set(b)))
print("mn2 in mn1:", s(mn2, mn1))
print("mn2 in g1:", s(mn2, g1))
print("g2 in g1:", s(g2, g1))
print("mn1 intersect g1:", s(mn1, g1))
allu = set(mn1).union(set(mn2), set(g1), set(g2))
print("TOTAL unique:", len(allu))
