import json
import re

with open('all_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Extract reference dictionaries
cpu_ref = {}
gpu_ref = {}

for it in items:
    cpu = (it.get('cpu') or '').strip()
    if cpu and it.get('_cpu_s'):
        cpu_ref[cpu.lower()] = (it.get('_cpu_s'), it.get('_fam'))
    
    gpu = (it.get('gpu') or '').strip()
    if gpu and it.get('_gpu_s'):
        gpu_ref[gpu.lower()] = (it.get('_gpu_s'), it.get('_gpu_cls'))

print(f"Total reference items: {len(items)}")
print(f"Unique CPU strings in DB: {len(cpu_ref)}")
print(f"Unique GPU strings in DB: {len(gpu_ref)}")

with open('gearvn_crawled_products.json', 'r', encoding='utf-8') as f:
    crawled = json.load(f)

print(f"\nAnalyzing 57 GearVN crawled laptops:")
unmatched_cpus = []
unmatched_gpus = []

for idx, it in enumerate(crawled, 1):
    name = it.get('name')
    cpu = it.get('cpu') or ''
    gpu = it.get('gpu') or ''
    ram = it.get('ram') or ''
    ssd = it.get('ssd') or ''
    screen = it.get('screen_size') or ''
    res = it.get('resolution') or ''
    hz = it.get('refresh_rate') or ''
    bat = it.get('battery') or ''
    
    # Check CPU
    cpu_clean = cpu.lower().strip()
    # match substring
    matched_cpu = None
    for k, v in cpu_ref.items():
        if k in cpu_clean or cpu_clean in k:
            matched_cpu = v
            break
    
    # Check GPU
    gpu_clean = gpu.lower().strip()
    matched_gpu = None
    for k, v in gpu_ref.items():
        if k in gpu_clean or gpu_clean in k:
            matched_gpu = v
            break

    print(f"#{idx:02d}: {name[:60]}")
    print(f"    CPU: '{cpu[:45]}' -> {matched_cpu}")
    print(f"    GPU: '{gpu[:45]}' -> {matched_gpu}")
    print(f"    RAM: '{ram}' | SSD: '{ssd}' | Screen: '{screen}' | Res: '{res}' | Hz: '{hz}' | Pin: '{bat}'")

