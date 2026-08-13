#!/usr/bin/env python3
"""Build multi-segment laptop report (7 price bands x 6 majors) with stock status."""
import json, os, re

BASE = os.path.expanduser("~/laptop-report-19m/raw/full")
data = json.load(open(os.path.join(BASE, "_ALL_scored.json"), encoding="utf-8"))
profiles = data["profiles"]; items = data["items"]

SEGMENTS = [
    {"id": "d10", "label": "Dưới 10tr", "emoji": "💸", "lo": 0, "hi": 10_000_000, "note": "Laptop cơ bản, sinh viên phổ thông, văn phòng nhẹ"},
    {"id": "s10", "label": "10 – 15tr", "emoji": "📘", "lo": 10_000_000, "hi": 15_000_000, "note": "Sinh viên chính phẩm — i3/Core 3/R5, 8-16GB"},
    {"id": "s15", "label": "15 – 20tr", "emoji": "🎯", "lo": 15_000_000, "hi": 20_000_000, "note": "Điểm cân bằng — i5/Core 5/R5, 16GB, có OLED/2K"},
    {"id": "s20", "label": "20 – 25tr", "emoji": "🚀", "lo": 20_000_000, "hi": 25_000_000, "note": "Ultra 5/Ryzen AI 5, dGPU entry, màn đẹp"},
    {"id": "s25", "label": "25 – 30tr", "emoji": "⚡", "lo": 25_000_000, "hi": 30_000_000, "note": "Ultra 7/Ryzen AI 7, RTX 4050/5050"},
    {"id": "s30", "label": "30 – 40tr", "emoji": "💎", "lo": 30_000_000, "hi": 40_000_000, "note": "Hiệu năng cao — RTX 4060/5060, OLED 2K"},
    {"id": "s40", "label": "Trên 40tr", "emoji": "👑", "lo": 40_000_000, "hi": 10**12, "note": "Cao cấp — RTX 5070+, Ultra 9, MacBook Pro"},
]

SHOP_LABEL = {
    "tgdd": "TGDD", "fpt": "FPT", "phongvu": "PhongVũ", "hacom": "Hacom",
    "no1computer": "No1", "cellphones": "CellphoneS", "laptopworld": "LaptopWorld",
    "laptopaz": "LaptopAZ", "laptop88": "Laptop88", "laptopgame": "LaptopGame",
    "hoangha": "Hoàng Hà", "gearvn": "GearVN",
}

def fmt_price(p):
    return f"{p//1_000_000}.{(p%1_000_000)//100_000}tr"

def stock_badge(stock):
    if stock == "CÒN": return '<span class="badge badge-green">● Còn hàng</span>'
    if stock == "HẾT": return '<span class="badge badge-red">✕ Hết hàng</span>'
    if stock == "LIÊN HỆ": return '<span class="badge badge-gold">✆ Liên hệ</span>'
    return '<span class="badge badge-gray">? Kiểm tra</span>'

def spec_str(r):
    parts = []
    if r.get("cpu"): parts.append(f"CPU: {r['cpu'][:45]}")
    if r.get("ram"): parts.append(f"RAM: {r['ram'][:25]}")
    if r.get("storage"): parts.append(f"SSD: {r['storage'][:25]}")
    if r.get("display"): parts.append(f"Màn: {r['display'][:35]}")
    if r.get("gpu"): parts.append(f"GPU: {r['gpu'][:25]}")
    return " • ".join(parts)

# value factor cho band center
def value_factor(price, lo, hi):
    center = (lo + hi) / 2 if hi < 10**12 else lo * 1.15
    dist = abs(price - center) / max(1, (hi - lo))
    return max(0.80, 1.0 - dist * 0.2)

# ─── Raw component scores (weight-independent, dùng cho custom weights) ───
def raw_scores(rec):
    ram_s = min(100, 30 + rec["_ram_gb"] * 5) if rec["_ram_gb"] >= 8 else 20
    storage_s = min(100, 40 + rec["_storage"] / 20)
    batt_s = min(100, rec["_bat"] * 2)
    display_s = min(100, rec["_res_s"] * 0.5 + rec["_ref_s"] * 0.25 + (20 if rec["_oled"] else 0) + min(10, max(0, rec["_size"] - 13) * 2))
    gpu_eff = min(100, rec["_gpu_s"] * 0.85 + (10 if rec["_gpu_cls"] == "dgpu" else 0))
    return {
        "cpu": rec["_cpu_s"], "ram": ram_s, "gpu": gpu_eff, "npu": rec["_npu"],
        "display": display_s, "battery": batt_s, "storage": storage_s,
    }
for r in items:
    r["_sv"] = {}
    for seg in SEGMENTS:
        vf = value_factor(r["price"], seg["lo"], seg["hi"])
        r["_sv"][seg["id"]] = {k: round(v * vf, 1) for k, v in r["_scores"].items()}

# HTML
prof_list = list(profiles.keys())
rows_by_cell = {}
for seg in SEGMENTS:
    for prof in prof_list:
        in_band = [x for x in items if seg["lo"] <= x["price"] < seg["hi"]]
        top = sorted(in_band, key=lambda x: -x["_sv"][seg["id"]][prof])[:10]
        rows_by_cell[(seg["id"], prof)] = top

# counts per segment
seg_counts = {seg["id"]: sum(1 for x in items if seg["lo"] <= x["price"] < seg["hi"]) for seg in SEGMENTS}

# Generate table rows HTML per cell
def cell_table(seg_id, prof):
    rows = rows_by_cell[(seg_id, prof)]
    if not rows:
        return '<tr><td colspan="5" style="text-align:center;color:var(--muted)">Không có máy trong phân khúc này</td></tr>'
    trs = []
    for i, r in enumerate(rows):
        stock = r.get("stock", "?")
        oos_class = ' class="oos-row"' if stock == "HẾT" else ""
        trs.append(f"""<tr{oos_class}>
<td class="rank {'rank-1' if i==0 else ''}">{i+1}</td>
<td><div class="name">{r['name'][:80]}</div><div class="spec">{spec_str(r)}</div></td>
<td class="price">{fmt_price(r['price'])}</td>
<td>{stock_badge(stock)}</td>
<td class="score">{r['_sv'][seg_id][prof]:.1f}</td>
<td><span class="shop">{SHOP_LABEL.get(r['shop'], r['shop'])}</span><br><a href="{r['url']}" target="_blank">Xem</a></td>
</tr>""")
    return "\n".join(trs)

# Build HTML
html_head = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Laptop theo phân khúc giá & chuyên ngành (08/2026)</title>
<style>
:root{--bg:#0f1420;--card:#1a2233;--card2:#202a3f;--border:#2c3a55;--text:#e8eef7;--muted:#93a3bc;--accent:#4f8cff;--accent2:#22d3ee;--gold:#fbbf24;--green:#34d399;--red:#f87171}
*{margin:0;padding:0;box-sizing:border-box}
::-webkit-scrollbar{width:10px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:5px}
html{scrollbar-color:var(--border) var(--bg)}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;padding:24px}
h1{font-size:1.6rem;margin-bottom:4px}
.sub{color:var(--muted);font-size:.9rem;margin-bottom:20px}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.72rem;font-weight:600;white-space:nowrap}
.badge-green{background:rgba(52,211,153,.12);color:var(--green)}
.badge-red{background:rgba(248,113,113,.12);color:var(--red)}
.badge-gold{background:rgba(251,191,36,.12);color:var(--gold)}
.badge-gray{background:rgba(147,163,188,.15);color:var(--muted)}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-bottom:20px}
.hero-card{background:linear-gradient(135deg,var(--card),var(--card2));border:1px solid var(--border);border-radius:12px;padding:14px}
.hero-card .label{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.hero-card .big{font-size:1.15rem;font-weight:700;color:var(--accent2)}
.hero-card .sub2{font-size:.78rem;color:var(--muted);margin-top:4px}
.controls{margin:16px 0}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
.row-label{font-size:.8rem;color:var(--muted);width:110px}
.chip{padding:6px 14px;border-radius:20px;background:var(--card);border:1px solid var(--border);cursor:pointer;font-size:.82rem;transition:.2s;white-space:nowrap}
.chip:hover{background:var(--card2)}
.chip.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.chip .cnt{font-size:.68rem;opacity:.75}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;font-size:.83rem}
th{background:var(--card2);padding:9px 10px;text-align:left;font-weight:600;color:var(--muted);text-transform:uppercase;font-size:.7rem;letter-spacing:.4px}
td{padding:9px 10px;border-top:1px solid var(--border);vertical-align:top}
tr:hover td{background:rgba(79,140,255,.05)}
tr.oos-row td{opacity:.55}
.price{color:var(--green);font-weight:700;white-space:nowrap}
.rank{font-size:1.05rem;font-weight:800;color:var(--accent2)}
.rank-1{color:var(--gold)}
.shop{font-size:.72rem;color:var(--muted)}
.name{font-weight:600;line-height:1.35}
.spec{font-size:.75rem;color:var(--muted);margin-top:3px;line-height:1.45}
.score{font-weight:700;color:var(--accent2);white-space:nowrap}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.section{margin:24px 0 10px;font-size:1.05rem;font-weight:700;border-left:4px solid var(--accent);padding-left:12px}
.footer{margin-top:28px;padding-top:16px;border-top:1px solid var(--border);color:var(--muted);font-size:.78rem;line-height:1.7}
.watch{margin:20px 0}
.watch-table td{font-size:.8rem}
.info-btn{cursor:pointer;color:var(--accent2);font-size:.85rem;margin-left:4px;border:none;background:none}
.info-btn:hover{color:var(--accent)}
#modal{display:none;position:fixed;inset:0;background:rgba(5,8,15,.75);z-index:100;align-items:center;justify-content:center;padding:20px}
#modal-card{background:var(--card);border:1px solid var(--border);border-radius:14px;max-width:760px;width:100%;max-height:85vh;overflow:auto;padding:20px}
#modal-close{float:right;cursor:pointer;color:var(--muted);font-size:1.3rem;border:none;background:none}
#modal-close:hover{color:var(--text)}
.custom-panel{margin:14px 0;background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.cp-head{padding:12px 16px;cursor:pointer;font-weight:600;display:flex;justify-content:space-between;align-items:center;font-size:.92rem}
.cp-head:hover{background:var(--card2)}
.cp-body{padding:14px 16px;border-top:1px solid var(--border);display:none}
.cp-body.open{display:block}
.cp-presets{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:12px}
.cp-btn{padding:5px 12px;border-radius:14px;background:var(--card2);border:1px solid var(--border);color:var(--text);cursor:pointer;font-size:.75rem;transition:.2s}
.cp-btn:hover{border-color:var(--accent)}
.cp-sliders{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px 20px;margin-bottom:12px}
.cp-slider{display:flex;align-items:center;gap:8px}
.cp-slider label{font-size:.78rem;min-width:70px;color:var(--muted)}
.cp-slider input[type=range]{flex:1;accent-color:var(--accent)}
.cp-slider .val{font-size:.78rem;min-width:38px;text-align:right;color:var(--accent2);font-weight:700}
.cp-total{font-size:.8rem;color:var(--muted);margin-bottom:10px}
.cp-apply{padding:8px 18px;border-radius:8px;background:var(--accent);border:none;color:#fff;font-weight:600;cursor:pointer;font-size:.85rem}
.cp-apply:hover{filter:brightness(1.15)}
.table-scroll{max-height:78vh;overflow-y:auto;overflow-x:hidden;border-radius:0 0 12px 12px;border:1px solid var(--border);border-top:none}
.table-scroll table{border-radius:0;border-collapse:separate;border-spacing:0;min-width:720px}
.table-wrap{position:relative}
.head-table{width:100%;border-collapse:separate;border-spacing:0;background:var(--card2);border-radius:12px 12px 0 0;border:1px solid var(--border);border-bottom:none;position:relative;z-index:10}
.head-table th{background:var(--card2);padding:9px 10px;text-align:left;font-weight:600;color:var(--muted);text-transform:uppercase;font-size:.7rem;letter-spacing:.4px;border-bottom:1px solid var(--border)}
.table-scroll td{border-bottom:1px solid var(--border)}
.table-scroll tbody tr:last-child td{border-bottom:none}
.col-rank{width:40px}
.col-price{width:90px}
.col-stock{width:110px}
.col-score{width:90px}
.col-shop{width:80px}
</style>
</head>
<body>

<div id="modal" onclick="if(event.target===this)closeModal()">
  <div id="modal-card">
    <button id="modal-close" onclick="closeModal()">✕</button>
    <div id="modal-body"></div>
  </div>
</div>
"""

# Stats
total = len(items)
shops_n = len(set(x["shop"] for x in items))

html_mid = f"""
<h1>💻 Laptop VN — 7 phân khúc giá × 6 chuyên ngành</h1>
<div class="sub">Khảo sát {shops_n} shop (TGDD, FPT, PhongVũ, Hacom, No1, CellphoneS, LaptopWorld, LaptopAZ, Laptop88, LaptopGame, Hoàng Hà, GearVN) • {total} máy mới • Cập nhật 12/08/2026 • <b style="color:var(--gold)">Giá + tình trạng hàng đã verify PDP</b></div>

<div class="hero">
<div class="hero-card"><div class="label">Tổng máy khảo sát</div><div class="big">{total}</div><div class="sub2">máy mới, đã lọc cũ/likenew</div></div>
<div class="hero-card"><div class="label">Số shop</div><div class="big">{shops_n}</div><div class="sub2">giá niêm yết hiện tại</div></div>
<div class="hero-card"><div class="label">Phân khúc giá</div><div class="big">7</div><div class="sub2">từ dưới 10tr đến 40tr+</div></div>
<div class="hero-card"><div class="label">Chuyên ngành</div><div class="big">6</div><div class="sub2">AI, CNTT, ĐH, VP, Game, CAD</div></div>
</div>

<div class="controls">
<div class="row"><div class="row-label">💰 Phân khúc:</div>"""

for seg in SEGMENTS:
    html_mid += f'<div class="chip" data-seg="{seg["id"]}" onclick="selectSeg(this)">{seg["emoji"]} {seg["label"]} <span class="cnt">({seg_counts[seg["id"]]})</span></div>'

html_mid += """</div>
<div class="row"><div class="row-label">🎓 Chuyên ngành:</div>"""

for prof in prof_list:
    html_mid += f'<div class="chip" data-prof="{prof}" onclick="selectProf(this)">{prof}</div>'

html_mid += """</div>
</div>

<div class="row" style="margin-top:8px">
  <button id="oos-toggle" class="chip" onclick="toggleOOS()" style="border-color:var(--accent2)">🙈 Ẩn máy hết hàng (vẫn xếp điểm khi bật lại)</button>
</div>

<div class="custom-panel" id="custom-panel">
  <div class="cp-head" onclick="togglePanel()">
    <span>🎛️ Tự chỉnh trọng số <span style="font-size:.7rem;color:var(--muted)">(bấm để mở/đóng)</span></span>
    <span id="cp-arrow">▾</span>
  </div>
  <div class="cp-body" id="cp-body">
    <div class="cp-presets">
      <span style="color:var(--muted);font-size:.75rem">Preset:</span>
      <button class="cp-btn" onclick="useProfile('AI / Data Science')">🤖 AI/Data</button>
      <button class="cp-btn" onclick="useProfile('Lập trình / CNTT')">💻 Lập trình</button>
      <button class="cp-btn" onclick="useProfile('Đồ họa / Thiết kế')">🎨 Đồ họa</button>
      <button class="cp-btn" onclick="useProfile('Kinh tế / Văn phòng')">💼 Văn phòng</button>
      <button class="cp-btn" onclick="useProfile('Game / Đa phương tiện')">🎮 Game</button>
      <button class="cp-btn" onclick="useProfile('Cơ khí / Kỹ thuật (CAD)')">📐 CAD</button>
      <button class="cp-btn" onclick="resetCustom()">↺ Mặc định</button>
    </div>
    <div class="cp-sliders" id="cp-sliders"></div>
    <div class="cp-total">Tổng trọng số: <b id="cp-total-val">100%</b> <span id="cp-total-warn" style="color:var(--red);display:none">(phải = 100%)</span></div>
    <button class="cp-apply" onclick="applyCustom()">Áp dụng & Xếp hạng lại</button>
  </div>
</div>

<div id="table-container"></div>

<div class="section">⏳ Hết hàng nhưng đáng chờ (top theo điểm số)</div>
<div class="watch"><table class="watch-table"><tr><th>#</th><th>Sản phẩm</th><th>Giá</th><th>Shop</th><th>Ghi chú</th></tr>"""

# Watch list: máy HẾT (hoặc LIÊN HỆ) top score trung bình
oos_items = [x for x in items if x.get("stock") in ("HẾT", "LIÊN HỆ")]
oos_sorted = sorted(oos_items, key=lambda x: -max(x["_scores"].values()))[:12]
for i, r in enumerate(oos_sorted, 1):
    note = "Liên hệ để mua (không mua online trực tiếp)" if r.get("stock") == "LIÊN HỆ" else "Hết hàng — có thể đáng chờ nếu cấu hình hiếm"
    html_mid += f"""<tr>
<td class="rank">{i}</td>
<td><div class="name">{r['name'][:70]}</div><div class="spec">{spec_str(r)}</div></td>
<td class="price">{fmt_price(r['price'])}</td>
<td><span class="shop">{SHOP_LABEL.get(r['shop'], r['shop'])}</span></td>
<td>{stock_badge(r.get('stock','?'))} <span style="font-size:.72rem;color:var(--muted)">{note}</span></td>
</tr>"""

html_mid += """</table></div>

<div class="section">📌 Ghi chú</div>
<div class="footer">
• Giá = giá bán hiện tại từ PDP (đã loại giá trả góp hàng tháng — cảnh giác card FPT/TGDD).<br>
• <b>Stock chỉ verify cho top candidates mỗi phân khúc</b> (~50 máy). Máy chưa verify hiển thị "? Kiểm tra" — nên xác nhận trên trang shop trước khi mua.<br>
• LaptopAZ nhiều máy hiện "Liên hệ" thay vì Mua ngay — kiểm tra trực tiếp.<br>
• Hàng cũ / like new / refurb / outlet đã loại. TrungTran không công khai giá nên không có.<br>
• Điểm = chấm theo trọng số từng chuyên ngành, điều chỉnh theo giá trị trong phân khúc.
</div>

<script>
const DATA = __DATA__;
const PROFILES = __PROFILES__;
let curSeg = 's15', curProf = 'AI / Data Science';

function fmtPrice(p){return (p/1e6).toFixed(1).replace('.',',')+'tr';}
function badge(st){if(st==='CÒN')return '<span class="badge badge-green">● Còn hàng</span>';if(st==='HẾT')return '<span class="badge badge-red">✕ Hết hàng</span>';if(st==='LIÊN HỆ')return '<span class="badge badge-gold">✆ Liên hệ</span>';return '<span class="badge badge-gray">? Kiểm tra</span>';}
function spec(r){const p=[];if(r.cpu)p.push('CPU: '+r.cpu.slice(0,45));if(r.ram)p.push('RAM: '+r.ram.slice(0,22));if(r.storage)p.push('SSD: '+r.storage.slice(0,22));if(r.display)p.push('Màn: '+r.display.slice(0,32));if(r.gpu)p.push('GPU: '+r.gpu.slice(0,22));return p.join(' • ');}
function showDetail(r){
  const det = r.detail || {};
  const w = currentWeights();
  const keys = [['cpu','CPU'],['ram','RAM'],['gpu','GPU'],['npu','NPU/AI'],['display','Màn hình'],['battery','Pin'],['storage','Ổ cứng']];
  let rows = keys.map(([k,label])=>{
    const sc = r.raw[k]||0, wt = w[k]||0;
    const pct = (sc*wt).toFixed(1);
    const bar = Math.round(sc);
    const d = det[label] || det[k] || '';
    return `<tr><td style="white-space:nowrap">${label}</td><td style="text-align:center">${Math.round(wt*100)}%</td><td style="text-align:center">${sc.toFixed(0)}/100</td><td style="text-align:center;color:var(--accent2);font-weight:700">${pct}</td><td><div style="background:var(--card2);border-radius:4px;height:8px;width:100%"><div style="background:linear-gradient(90deg,var(--accent),var(--accent2));height:8px;border-radius:4px;width:${bar}%"></div></div></td><td style="font-size:.72rem;color:var(--muted)">${d}</td></tr>`;
  }).join('');
  const score = computeScore(r, w);
  document.getElementById('modal-body').innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:12px">
      <div>
        <div style="font-weight:700;font-size:1rem;line-height:1.4">${r.name}</div>
        <div style="color:var(--muted);font-size:.8rem;margin-top:4px">${fmtPrice(r.price)} • ${r.shopLabel} • ${badge(r.stock)}</div>
      </div>
      <div style="text-align:center;min-width:80px"><div style="font-size:1.6rem;font-weight:800;color:var(--accent2)">${score.toFixed(1)}</div><div style="font-size:.65rem;color:var(--muted)">ĐIỂM</div></div>
    </div>
    <div style="color:var(--muted);font-size:.78rem;margin-bottom:10px">Ngành <b style="color:var(--accent2)">${curProf}</b> — điểm mỗi tiêu chí = điểm tiêu chí × trọng số × hệ số giá trị phân khúc. Tổng = ${score.toFixed(1)}</div>
    <table style="width:100%;font-size:.8rem"><tr><th>Tiêu chí</th><th style="text-align:center">Trọng số</th><th style="text-align:center">Điểm</th><th style="text-align:center">Đóng góp</th><th style="width:30%"></th><th>Chi tiết</th></tr>${rows}</table>`;
  document.getElementById('modal').style.display = 'flex';
}
function closeModal(){document.getElementById('modal').style.display='none';}
let customWeights = null; // null = dùng profile
let hideOOS = false; // ẩn máy hết hàng
function toggleOOS(){
  hideOOS = !hideOOS;
  document.getElementById('oos-toggle').classList.toggle('active', hideOOS);
  render();
}
function currentWeights(){
  if (customWeights) return customWeights;
  return PROFILES[curProf].w;
}
function computeScore(r, w){
  let total = 0;
  for (const k of ['cpu','ram','gpu','npu','display','battery','storage']) total += (r.raw[k]||0) * (w[k]||0);
  return total;
}
function valueFactorFor(price, seg){
  const center = (seg.lo + seg.hi) / 2;
  const dist = Math.abs(price - center) / Math.max(1, (seg.hi - seg.lo));
  return Math.max(0.80, 1.0 - dist * 0.2);
}
function selectSeg(el){curSeg=el.dataset.seg;document.querySelectorAll('.chip[data-seg]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function selectProf(el){curProf=el.dataset.prof;customWeights=null;document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function render(){
  const seg = DATA.segments.find(s=>s.id===curSeg);
  const w = currentWeights();
  let inBand = DATA.items.filter(x=>x.price>=seg.lo&&x.price<seg.hi);
  if (hideOOS) inBand = inBand.filter(x=>x.stock!=='HẾT');
  const scored = inBand.map(r=>({r, s: computeScore(r,w) * valueFactorFor(r.price, seg)}));
  scored.sort((a,b)=>b.s-a.s);
  let rows = scored.map((item,i)=>{
    const r = item.r;
    const oos = r.stock==='HẾT'?' class="oos-row"':'';
    return `<tr${oos}><td class="rank ${i===0?'rank-1':''} col-rank">${i+1}</td><td><div class="name">${r.name.slice(0,85)}</div><div class="spec">${spec(r)}</div></td><td class="price col-price">${fmtPrice(r.price)}</td><td class="col-stock">${badge(r.stock)}</td><td class="score col-score">${item.s.toFixed(1)} <span class="info-btn" onclick="showDetail(DATA.items[${DATA.items.indexOf(r)}])" title="Xem giải thích điểm">ⓘ</span></td><td class="col-shop"><span class="shop">${r.shopLabel}</span><br><a href="${r.url}" target="_blank">Xem</a></td></tr>`;
  }).join('');
  const mode = customWeights ? '🎛️ trọng số tự chỉnh' : `ngành <b style="color:var(--accent2)">${curProf}</b>`;
  const oosInfo = hideOOS ? ` (đã ẩn máy hết hàng)` : '';
  document.getElementById('table-container').innerHTML = `<div style="margin-bottom:10px;color:var(--muted);font-size:.85rem">Phân khúc <b style="color:var(--accent2)">${seg.emoji} ${seg.label}</b> — <b style="color:var(--accent2)">${scored.length}</b> máy • ${mode}${oosInfo} • <span style="color:var(--muted)">bấm ⓘ xem giải thích • cuộn trong bảng để xem hết</span></div><div class="table-wrap"><table class="head-table"><thead><tr><th class="col-rank">#</th><th>Sản phẩm</th><th class="col-price">Giá</th><th class="col-stock">Hàng</th><th class="col-score">Điểm</th><th class="col-shop">Shop</th></tr></thead></table><div class="table-scroll"><table><tbody>${rows}</tbody></table></div></div>`;
}
// ─── Custom weights panel ───
const CRITERIA = [['cpu','CPU'],['ram','RAM'],['gpu','GPU'],['npu','NPU/AI'],['display','Màn hình'],['battery','Pin'],['storage','Ổ cứng']];
function togglePanel(){
  const body = document.getElementById('cp-body');
  body.classList.toggle('open');
  document.getElementById('cp-arrow').innerText = body.classList.contains('open') ? '▴' : '▾';
  if (body.classList.contains('open') && !document.getElementById('cp-sliders').children.length) buildSliders();
}
function buildSliders(){
  const w = customWeights || PROFILES[curProf].w;
  document.getElementById('cp-sliders').innerHTML = CRITERIA.map(([k,label])=>
    `<div class="cp-slider"><label>${label}</label><input type="range" min="0" max="50" step="1" value="${Math.round(w[k]*100)}" data-key="${k}" oninput="this.parentElement.querySelector('.val').innerText=this.value+'%';updateTotal()"><span class="val">${Math.round(w[k]*100)}%</span></div>`
  ).join('');
  updateTotal();
}
function updateTotal(){
  const total = Array.from(document.querySelectorAll('#cp-sliders input')).reduce((s,i)=>s+parseInt(i.value),0);
  document.getElementById('cp-total-val').innerText = total + '%';
  document.getElementById('cp-total-warn').style.display = total === 100 ? 'none' : 'inline';
}
function useProfile(p){
  curProf = p;
  document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));
  const chip = document.querySelector(`.chip[data-prof="${p}"]`);
  if (chip) chip.classList.add('active');
  customWeights = null;
  buildSliders();
  render();
}
function resetCustom(){
  useProfile(curProf);
}
function applyCustom(){
  const w = {};
  let total = 0;
  Array.from(document.querySelectorAll('#cp-sliders input')).forEach(i=>{
    w[i.dataset.key] = parseInt(i.value)/100; total += parseInt(i.value);
  });
  if (total !== 100) { alert('Tổng trọng số phải bằng 100%! Hiện tại: ' + total + '%'); return; }
  customWeights = w;
  render();
}
// init active chips
document.querySelectorAll('.chip[data-seg]')[3].classList.add('active');
document.querySelectorAll('.chip[data-prof]')[0].classList.add('active');
render();
</script>
</body></html>"""

# Serialize data for JS
seg_js = [{"id": s["id"], "label": s["label"], "emoji": s["emoji"], "lo": s["lo"], "hi": s["hi"]} for s in SEGMENTS]
items_js = []
for r in items:
    items_js.append({
        "name": r["name"], "price": r["price"], "shop": r["shop"],
        "shopLabel": SHOP_LABEL.get(r["shop"], r["shop"]), "url": r["url"],
        "cpu": r.get("cpu",""), "ram": r.get("ram",""), "storage": r.get("storage",""),
        "display": r.get("display",""), "gpu": r.get("gpu",""), "stock": r.get("stock","?"),
        "sv": r["_sv"], "raw": raw_scores(r),
        # detail cho modal
        "detail": {
            "cpu": r.get("cpu","") or r.get("_fam",""), "ram": f"{r.get('_ram_gb',0)}GB",
            "gpu": r.get("gpu","") or r.get("_gpu_cls",""), "npu": "AI accelerator" if r.get("_npu") else "Không có",
            "display": f"{r.get('_size','')}\" OLED={r.get('_oled',False)}", "battery": f"{r.get('_bat',0):.0f}Wh",
            "storage": r.get("storage","") or f"{r.get('_storage',0)}GB",
        },
    })

html = html_head + html_mid
html = html.replace("__DATA__", json.dumps({"segments": seg_js, "items": items_js}, ensure_ascii=False))
html = html.replace("__PROFILES__", json.dumps(profiles, ensure_ascii=False))

out = os.path.expanduser("~/laptop-report-19m/bao-cao-laptop-phan-khuc.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("saved:", out, os.path.getsize(out), "bytes")
