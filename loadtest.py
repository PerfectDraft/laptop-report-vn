#!/usr/bin/env python3
"""Simple load test: N requests, C concurrent, report latency + errors."""
import json, os, sys, time, urllib.request, threading, queue
from collections import Counter

URL = sys.argv[1] if len(sys.argv) > 1 else "https://laptop-report-vn.vercel.app"
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 200
CONC = int(sys.argv[3]) if len(sys.argv) > 3 else 20

latencies = []
errors = []
statuses = Counter()
lock = threading.Lock()

def worker():
    while True:
        try: _ = q.get_nowait()
        except queue.Empty: return
        t0 = time.time()
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "loadtest/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
                statuses[r.status] += 1
                lat = (time.time() - t0) * 1000
        except Exception as e:
            lat = (time.time() - t0) * 1000
            errors.append(str(e)[:80])
        with lock:
            latencies.append(lat)
        q.task_done()

q = queue.Queue()
for _ in range(TOTAL): q.put(1)
threads = [threading.Thread(target=worker) for _ in range(CONC)]
t_start = time.time()
for t in threads: t.start()
for t in threads: t.join()
elapsed = time.time() - t_start

latencies.sort()
n = len(latencies)
p50 = latencies[n//2] if n else 0
p95 = latencies[int(n*0.95)] if n else 0
p99 = latencies[int(n*0.99)] if n else 0
avg = sum(latencies)/n if n else 0
rps = n / elapsed if elapsed else 0

print(f"=== LOAD TEST {URL} ===")
print(f"Requests: {n}/{TOTAL} | Concurrency: {CONC} | Thời gian: {elapsed:.1f}s | RPS: {rps:.1f}")
print(f"Status: {dict(statuses)}")
print(f"Errors: {len(errors)}")
if errors: print("  sample:", errors[:3])
print(f"\nLatency: avg={avg:.0f}ms | p50={p50:.0f}ms | p95={p95:.0f}ms | p99={p99:.0f}ms | max={latencies[-1]:.0f}ms" if n else "No data")
