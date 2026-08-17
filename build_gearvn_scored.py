import json
import re
import unicodedata

# Load profiles from all_items.json / build_compact.py
PROFS = {
    "AI / Data Science": {"w": {"cpu": 0.2444, "ram": 0.2, "gpu": 0.3333, "display": 0.0889, "battery": 0.0778, "storage": 0.0556}},
    "Lập trình / CNTT": {"w": {"cpu": 0.3262, "ram": 0.2717, "gpu": 0.0543, "display": 0.163, "battery": 0.1087, "storage": 0.0761}},
    "Đồ họa / Thiết kế": {"w": {"cpu": 0.2062, "ram": 0.2062, "gpu": 0.3093, "display": 0.1856, "battery": 0.0515, "storage": 0.0412}},
    "Kinh tế / Văn phòng": {"w": {"cpu": 0.1579, "ram": 0.1579, "gpu": 0.0, "display": 0.2105, "battery": 0.3684, "storage": 0.1053}},
    "Game / Đa phương tiện": {"w": {"cpu": 0.204, "ram": 0.1531, "gpu": 0.4082, "display": 0.1531, "battery": 0.051, "storage": 0.0306}},
    "Cơ khí / Kỹ thuật (CAD)": {"w": {"cpu": 0.2578, "ram": 0.2577, "gpu": 0.2577, "display": 0.1031, "battery": 0.0722, "storage": 0.0515}}
}

SEGMENTS = [
    {"id": "d10", "lo": 0, "hi": 10_000_000},
    {"id": "s10", "lo": 10_000_000, "hi": 15_000_000},
    {"id": "s15", "lo": 15_000_000, "hi": 20_000_000},
    {"id": "s20", "lo": 20_000_000, "hi": 25_000_000},
    {"id": "s25", "lo": 25_000_000, "hi": 30_000_000},
    {"id": "s30", "lo": 30_000_000, "hi": 40_000_000},
    {"id": "s40", "lo": 40_000_000, "hi": 10**12}
]

DISP_W = {
    "AI / Data Science": [0.50, 0.15, 0.35],
    "Lập trình / CNTT": [0.55, 0.15, 0.30],
    "Đồ họa / Thiết kế": [0.45, 0.10, 0.45],
    "Kinh tế / Văn phòng": [0.50, 0.15, 0.35],
    "Game / Đa phương tiện": [0.30, 0.45, 0.25],
    "Cơ khí / Kỹ thuật (CAD)": [0.50, 0.20, 0.30]
}

def clean_text(s):
    if not s:
        return ""
    s = unicodedata.normalize('NFKD', str(s))
    s = s.replace('®', '').replace('™', '').replace('©', '').replace('–', '-').replace('—', '-')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()

def value_factor_for(price, seg):
    lo, hi = seg["lo"], seg["hi"]
    if hi < 10**11:
        center = (lo + hi) / 2
        half_band = (hi - lo) / 2
        dist = abs(price - center) / half_band
    else:
        dist = max(0, (price - lo) / lo)
    raw = 1.0 - dist * 0.15
    return min(1.15, max(0.85, round(raw, 3)))

def get_cpu_info(name, cpu_raw):
    combined = clean_text(f"{name} {cpu_raw}")

    # AMD Ryzen AI 300 / 400 Series
    if "ai 9 465" in combined or "ai 9-465" in combined:
        return "AMD Ryzen AI 9 465", 86.5, "amd-ryzen"
    if "ai 9 365" in combined or "ai 9-365" in combined or "ryzen 9 365" in combined:
        return "AMD Ryzen AI 9 365", 85.0, "amd-ryzen"
    if "ai 7 350" in combined or "ai 7-350" in combined or "ryzen ai 7" in combined:
        return "AMD Ryzen AI 7 350", 82.5, "amd-ryzen"

    # Intel Ultra Series
    if "ultra 9 275hx" in combined or "ultra 9-275hx" in combined:
        return "Intel Core Ultra 9 275HX", 88.4, "intel-ultra"
    if "ultra 9 288v" in combined or "ultra 9-288v" in combined:
        return "Intel Core Ultra 9 288V", 78.0, "intel-ultra"
    if "ultra 9 386h" in combined or "ultra 9-386h" in combined:
        return "Intel Core Ultra 9 386H", 88.4, "intel-ultra"
    if "ultra 7 255hx" in combined or "ultra 7-255hx" in combined:
        return "Intel Core Ultra 7 255HX", 85.8, "intel-ultra"
    if "ultra 7 155h" in combined or "ultra 7-155h" in combined:
        return "Intel Core Ultra 7 155H", 78.2, "intel-ultra"
    if "ultra 5 226v" in combined or "ultra 5-226v" in combined:
        return "Intel Core Ultra 5 226V", 69.5, "intel-ultra"
    if "ultra 5 125h" in combined or "ultra 5-125h" in combined:
        return "Intel Core Ultra 5 125H", 72.8, "intel-ultra"

    # Intel Core Series (Series 1 / Series 2)
    if "core 7 240h" in combined or "core 7-240h" in combined or "i7-240h" in combined:
        return "Intel Core 7 240H", 76.4, "intel-core"
    if "core 5 210h" in combined or "core 5-210h" in combined or "i5-210h" in combined:
        return "Intel Core 5 210H", 72.8, "intel-core"
    if "core 5 120u" in combined or "core 5-120u" in combined:
        return "Intel Core 5 120U", 63.9, "intel-core"
    if "core 3-n350" in combined or "core 3 n350" in combined or "core 3 n305" in combined:
        return "Intel Core 3 N350", 48.5, "intel-core"

    # Intel Core i HX / H / U Series
    if "14700hx" in combined:
        return "Intel Core i7 14700HX", 85.8, "intel-core"
    if "14650hx" in combined:
        return "Intel Core i7 14650HX", 85.0, "intel-core"
    if "13650hx" in combined:
        return "Intel Core i7 13650HX", 83.0, "intel-core"
    if "13620h" in combined:
        return "Intel Core i7 13620H", 76.4, "intel-core"
    if "13420h" in combined:
        return "Intel Core i5 13420H", 66.6, "intel-core"
    if "1315u" in combined or "c3u08" in combined or "p1403cva-c3" in combined:
        return "Intel Core i3 1315U", 57.8, "intel-core"
    if "1305u" in combined:
        return "Intel Core i3 1305U", 53.2, "intel-core"
    if "1215u" in combined:
        return "Intel Core i3 1215U", 54.9, "intel-core"
    if "p1403cva-c5" in combined or "c5h16" in combined:
        return "Intel Core i5 13420H", 66.6, "intel-core"

    # AMD Ryzen HS / U Series
    if "8845hs" in combined:
        return "AMD Ryzen 7 8845HS", 80.5, "amd-ryzen"
    if "7840hs" in combined:
        return "AMD Ryzen 7 7840HS", 80.2, "amd-ryzen"
    if "7640hs" in combined:
        return "AMD Ryzen 5 7640HS", 72.8, "amd-ryzen"
    if "7445hs" in combined:
        return "AMD Ryzen 7 7445HS", 73.0, "amd-ryzen"
    if "7535hs" in combined or "753" in combined:
        return "AMD Ryzen 5 7535HS", 68.7, "amd-ryzen"
    if "6600h" in combined:
        return "AMD Ryzen 5 6600H", 68.3, "amd-ryzen"
    if "5825u" in combined:
        return "AMD Ryzen 7 5825U", 75.9, "amd-ryzen"
    if "5625u" in combined:
        return "AMD Ryzen 5 5625U", 60.1, "amd-ryzen"
    if "7430u" in combined:
        return "AMD Ryzen 5 7430U", 61.1, "amd-ryzen"
    if "5400u" in combined:
        return "AMD Ryzen 3 5400U", 53.9, "amd-ryzen"
    if "3500u" in combined:
        return "AMD Ryzen 5 3500U", 50.2, "amd-ryzen"
    if "3200u" in combined:
        return "AMD Ryzen 3 3200U", 37.9, "amd-ryzen"
    if "ryzen 3 30" in combined or "al15-21p-r87w" in combined:
        return "AMD Ryzen 3 7320U", 45.0, "amd-ryzen"

    # Default
    return "Intel Core i5 13420H", 66.6, "intel-core"

def get_gpu_info(name, gpu_raw):
    combined = clean_text(f"{name} {gpu_raw}")

    if "5070 ti" in combined or "5070ti" in combined:
        return "NVIDIA GeForce RTX 5070 Ti Laptop 12GB", 91.4, "dgpu"
    if "5070" in combined:
        return "NVIDIA GeForce RTX 5070 Laptop 8GB", 89.5, "dgpu"
    if "5060" in combined:
        return "NVIDIA GeForce RTX 5060 Laptop 8GB", 88.2, "dgpu"
    if "5050" in combined:
        return "NVIDIA GeForce RTX 5050 Laptop 6GB", 84.0, "dgpu"
    if "4060" in combined:
        return "NVIDIA GeForce RTX 4060 Laptop 8GB", 86.5, "dgpu"
    if "4050" in combined:
        return "NVIDIA GeForce RTX 4050 Laptop 6GB", 83.0, "dgpu"
    if "3050" in combined:
        return "NVIDIA GeForce RTX 3050 Laptop 6GB", 73.2, "dgpu"
    if "2050" in combined:
        return "NVIDIA GeForce RTX 2050 Laptop 4GB", 62.0, "dgpu"
    
    if "arc" in combined or "ultra 5" in combined or "ultra 7" in combined or "ultra 9" in combined:
        return "Intel Arc Graphics", 50.3, "igpu"
    if "radeon" in combined or "ryzen" in combined:
        return "AMD Radeon Graphics", 36.7, "igpu"
    if "iris" in combined or "core 5" in combined or "core 7" in combined or "i5" in combined or "i7" in combined:
        return "Intel Iris Xe Graphics", 40.8, "igpu"
    
    return "Intel UHD Graphics", 32.0, "igpu"

def get_ram_gb(name, ram_raw):
    combined = clean_text(f"{name} {ram_raw}")
    if "32gb" in combined or "32 gb" in combined:
        return 32, "32GB", 75.0
    if "16gb" in combined or "16 gb" in combined:
        return 16, "16GB", 50.0
    if "8gb" in combined or "8 gb" in combined:
        return 8, "8GB", 25.0
    if "64gb" in combined or "64 gb" in combined:
        return 64, "64GB", 100.0
    return 16, "16GB", 50.0

def get_storage_gb(name, ssd_raw):
    combined = clean_text(f"{name} {ssd_raw}")
    if "2tb" in combined or "2048" in combined or "2048gb" in combined:
        return 2048, "SSD 2TB NVMe PCIe", min(100.0, round(85.0 * 1.15, 1))
    if "1tb" in combined or "1024" in combined or "1024gb" in combined:
        return 1024, "SSD 1TB NVMe PCIe", min(100.0, round(85.0 * 1.08, 1))
    if "512gb" in combined or "512 gb" in combined or "512" in combined:
        return 512, "SSD 512GB NVMe PCIe", 85.0
    if "256gb" in combined or "256 gb" in combined:
        return 256, "SSD 256GB NVMe PCIe", round(85.0 * 0.9, 1)
    return 512, "SSD 512GB NVMe PCIe", 85.0

def get_display_info(name, screen_raw, res_raw, hz_raw):
    combined = clean_text(f"{name} {screen_raw} {res_raw} {hz_raw}")
    
    # Size
    size = 15.6
    m_size = re.search(r'(\d{2}(?:\.\d)?)\s*(?:inch|[\"”])', combined)
    if m_size:
        size = float(m_size.group(1))
    elif "14" in combined or "14.0" in combined or "14.5" in combined:
        size = 14.0 if "14.5" not in combined else 14.5
    elif "16" in combined or "16.0" in combined:
        size = 16.0

    # Res & PPI
    res_str = "Full HD (1920x1080)"
    ppi_score = 31.4
    if "3k" in combined or "2880" in combined:
        res_str = "3K (2880x1800)"
        ppi_score = 75.0
    elif "2.8k" in combined:
        res_str = "2.8K OLED"
        ppi_score = 70.0
    elif "2k" in combined or "2560" in combined or "qhd" in combined or "wqxga" in combined:
        res_str = "QHD+ (2560x1600)"
        ppi_score = 60.0
    elif "1920 x 1200" in combined or "1920x1200" in combined or "1920 × 1200" in combined or "fhd+" in combined or "wuxga" in combined:
        res_str = "WUXGA (1920x1200)"
        ppi_score = 34.0

    # Hz & Hz score
    hz = 60
    hz_score = 0.0
    if "240" in combined:
        hz = 240
        hz_score = 100.0
    elif "180" in combined:
        hz = 180
        hz_score = 88.0
    elif "165" in combined:
        hz = 165
        hz_score = 80.0
    elif "144" in combined:
        hz = 144
        hz_score = 70.0
    elif "120" in combined:
        hz = 120
        hz_score = 50.0

    # Panel
    is_oled = "oled" in combined
    panel_score = 100.0 if is_oled else 70.0

    disp_parts = [round(ppi_score, 1), round(hz_score, 1), round(panel_score, 1)]
    disp_s = round(0.45 * ppi_score + 0.30 * hz_score + 0.25 * panel_score, 1)

    panel_name = "OLED" if is_oled else "IPS"
    display_desc = f"{size:.1f}\" {res_str} • {hz}Hz {panel_name}"

    return size, res_str, hz, is_oled, disp_s, disp_parts, display_desc

def get_battery_info(name, bat_raw):
    combined = clean_text(f"{name} {bat_raw}")
    m_wh = re.search(r'(\d+(?:\.\d+)?)\s*wh', combined)
    if m_wh:
        wh = float(m_wh.group(1))
        return wh, min(100.0, round(wh, 1))
    if "90wh" in combined or "90 wh" in combined:
        return 90.0, 90.0
    if "80wh" in combined or "80 wh" in combined:
        return 80.0, 80.0
    if "76wh" in combined or "76 wh" in combined:
        return 76.0, 76.0
    if "57wh" in combined or "57 wh" in combined:
        return 57.0, 57.0
    if "53wh" in combined or "53 wh" in combined:
        return 53.0, 53.0
    return 50.0, 50.0

def convert_crawled_to_scored(crawled_item):
    name = crawled_item["name"].strip()
    price = crawled_item["price"]
    url = crawled_item["url"]
    in_stock = crawled_item.get("in_stock", True)
    stock = "CÒN" if in_stock else "HẾT"
    
    cpu_name, cpu_s, fam = get_cpu_info(name, crawled_item.get("cpu", ""))
    gpu_name, gpu_s, gpu_cls = get_gpu_info(name, crawled_item.get("gpu", ""))
    ram_gb, ram_str, ram_s = get_ram_gb(name, crawled_item.get("ram", ""))
    storage_gb, storage_str, storage_s = get_storage_gb(name, crawled_item.get("ssd", ""))
    size, res_str, hz, is_oled, disp_s, disp_parts, display_desc = get_display_info(
        name, crawled_item.get("screen_size", ""), crawled_item.get("resolution", ""), crawled_item.get("refresh_rate", "")
    )
    bat_wh, batt_s = get_battery_info(name, crawled_item.get("battery", ""))

    # Compute _scores for each profile
    scores = {}
    for pname, pdata in PROFS.items():
        w = pdata["w"]
        dw = DISP_W[pname]
        prof_disp_s = dw[0] * disp_parts[0] + dw[1] * disp_parts[1] + dw[2] * disp_parts[2]
        
        tot = (
            w["cpu"] * cpu_s +
            w["ram"] * ram_s +
            w["gpu"] * gpu_s +
            w["display"] * prof_disp_s +
            w["battery"] * batt_s +
            w["storage"] * storage_s
        )
        scores[pname] = round(tot, 2)

    # Compute _sv for each segment
    sv = {}
    for seg in SEGMENTS:
        vf = value_factor_for(price, seg)
        sv[seg["id"]] = {k: round(v * vf, 1) for k, v in scores.items()}

    return {
        "name": name,
        "price": price,
        "shop": "gearvn",
        "url": url,
        "stock": stock,
        "cpu": cpu_name,
        "ram": ram_str,
        "storage": storage_str,
        "display": display_desc,
        "gpu": gpu_name,
        "_fam": fam,
        "_gpu_cls": gpu_cls,
        "_ram_gb": ram_gb,
        "_storage": storage_gb,
        "_size": size,
        "_res_s": res_str,
        "_ref_s": hz,
        "_oled": is_oled,
        "_bat": bat_wh,
        "_cpu_s": cpu_s,
        "_gpu_s": gpu_s,
        "_ram_s": ram_s,
        "_storage_s": storage_s,
        "_display_s": disp_s,
        "_batt_s": batt_s,
        "_disp_parts": disp_parts,
        "_scores": scores,
        "_sv": sv
    }

if __name__ == "__main__":
    with open("gearvn_crawled_products.json", "r", encoding="utf-8") as f:
        crawled = json.load(f)

    converted = [convert_crawled_to_scored(it) for it in crawled]
    print(f"Successfully converted {len(converted)} GearVN laptops to scored format.")
    
    with open("gearvn_converted_scored.json", "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)
    print("Saved to gearvn_converted_scored.json")
