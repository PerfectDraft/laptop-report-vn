#!/usr/bin/env python3
"""Build compact laptop report (7 price bands x 6 majors) — data compressed ~6x."""
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

def raw_scores(rec):
    # RAM: log2 (PassMark/Claude: 8=25, 16=50, 32=75, 64=100)
    ram_s = rec.get("_ram_s", 0)
    # Storage: bảng loại ổ (HDD 15, SATA 45, NVMe3 65, NVMe4 85, NVMe5 100) × dung lượng
    storage_s = rec.get("_storage_s", 0)
    # Pin: 100Wh = 100 (IATA/FAA)
    batt_s = rec.get("_batt_s", 0)
    # Display: PPI + Hz + panel (0.45/0.30/0.25)
    display_s = rec.get("_display_s", 0)
    # GPU: PassMark G3D log + bonus dGPU
    gpu_eff = min(100, rec["_gpu_s"] + (10 if rec["_gpu_cls"] == "dgpu" else 0))
    return [rec["_cpu_s"], round(ram_s,1), round(gpu_eff,1), round(display_s,1), round(batt_s,1), round(storage_s,1)]

# Compact items
items_c = []
for r in items:
    if r.get("_fam") == "monitor":
        continue  # bỏ monitor (Studio Display...) khỏi ranking laptop
    items_c.append({
        "n": r["name"], "p": r["price"], "s": r["shop"], "u": r["url"],
        "c": (r.get("cpu") or "")[:45], "r": (r.get("ram") or "")[:22], "t": (r.get("storage") or "")[:22],
        "d": (r.get("display") or "")[:35], "g": (r.get("gpu") or "")[:25], "k": r.get("stock","?"),
        "q": raw_scores(r),
        "e": 1 if r.get("_fam") in ("unknown", None, "") else 0,
        "i": [round(r["_size"],1), r["_res_s"], 1 if r["_oled"] else 0, round(r["_bat"]), r["_storage"], r["_ram_gb"]],
    })

# HTML (dùng chung template cũ nhưng JS đọc compact)
HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Laptop theo phân khúc giá & chuyên ngành (08/2026)</title>
<style>
:root{--bg:#0f1420;--card:#1a2233;--card2:#202a3f;--border:#2c3a55;--text:#e8eef7;--muted:#93a3bc;--accent:#4f8cff;--accent2:#22d3ee;--gold:#fbbf24;--green:#34d399;--red:#f87171}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
img,svg,video,canvas{max-width:100%;height:auto;display:block}
button,input,select,textarea{font:inherit;color:inherit}
body{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;line-height:1.5;overflow-x:hidden}
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
table{width:100%;border-collapse:collapse;background:var(--card);font-size:.83rem}
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
.notice{display:flex;gap:12px;align-items:flex-start;background:linear-gradient(135deg,rgba(251,191,36,.1),rgba(248,113,113,.08));border:1px solid var(--gold);border-radius:12px;padding:12px 16px;margin-bottom:18px;font-size:.85rem;line-height:1.6}
.notice .ico{font-size:1.3rem;line-height:1.2}
.notice b{color:var(--gold)}
.notice a{color:var(--accent2);font-weight:600;text-decoration:underline}
@media (max-width:768px){.notice{font-size:.78rem;padding:10px 12px}}
.credit{position:relative;display:inline-block;cursor:help}
.credit a{color:var(--accent2);font-weight:600}
.credit .tip{visibility:hidden;opacity:0;position:absolute;bottom:130%;left:50%;transform:translateX(-50%) translateY(4px);background:var(--card2);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:8px;font-size:.75rem;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.45);transition:opacity .18s,transform .18s;z-index:50;pointer-events:none}
.credit:hover .tip{visibility:visible;opacity:1;transform:translateX(-50%) translateY(0)}
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
.view-btn{display:inline-block;background:var(--accent);color:#fff!important;padding:4px 12px;border-radius:6px;font-weight:600;font-size:.75rem;text-decoration:none!important;transition:.2s;margin-top:3px}
.view-btn:hover{background:#3b76e0;transform:translateY(-1px);box-shadow:0 2px 8px rgba(79,140,255,.35)}
.view-btn:active{transform:translateY(0)}
/* ── Responsive: mobile → bảng vuốt ngang ── */
@media (max-width: 768px){
  body{padding:12px}
  h1{font-size:1.15rem}
  .sub{font-size:.78rem}
  .hero{grid-template-columns:repeat(2,1fr);gap:8px}
  .hero-card{padding:10px}
  .hero-card .big{font-size:1rem}
  .row-label{width:100%}
  .chip{font-size:.75rem;padding:5px 10px}
  .cp-sliders{grid-template-columns:1fr}
  /* bảng giữ nguyên, vuốt ngang trong container */
  .table-wrap{display:none}
  .mobile-scroll{display:block;max-height:75vh;overflow:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--border);border-radius:12px;width:100%}
  .mobile-table{min-width:720px;border-collapse:separate;border-spacing:0;width:100%}
  .mobile-table thead{position:sticky;top:0;z-index:5;display:table-header-group}
  .mobile-table thead th{background:var(--card2);padding:9px 10px;text-align:left;font-weight:600;color:var(--muted);text-transform:uppercase;font-size:.7rem;letter-spacing:.4px;border-bottom:1px solid var(--border)}
  .mobile-table td{border-bottom:1px solid var(--border)}
  .mobile-cards{display:none}
  .watch-table,.footer{font-size:.72rem}
  .swipe-hint{display:flex;align-items:center;gap:6px;color:var(--accent2);font-size:.75rem;margin-bottom:6px}
}
@media (min-width: 769px){
  .mobile-cards{display:none}
  .mobile-scroll{display:none}
  .swipe-hint{display:none}
}
.header-wrap{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}
.info-btn{flex-shrink:0;width:34px;height:34px;border-radius:50%;border:1px solid var(--border);background:var(--card);color:var(--accent2);font-size:1.05rem;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;margin-top:2px}
.info-btn:hover{border-color:var(--accent2);background:var(--card2);transform:scale(1.08)}
.log-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:200;align-items:center;justify-content:center;padding:16px}
.log-modal.open{display:flex}
.log-card{background:var(--card);border:1px solid var(--border);border-radius:14px;max-width:560px;width:100%;max-height:80vh;overflow-y:auto;padding:22px;position:relative;box-shadow:0 12px 40px rgba(0,0,0,.5)}
.log-card h3{color:var(--gold);margin:0 0 4px;font-size:1.05rem}
.log-card .log-sub{color:var(--muted);font-size:.78rem;margin-bottom:14px}
.log-close{position:absolute;top:12px;right:12px;background:none;border:none;color:var(--muted);font-size:1.2rem;cursor:pointer}
.log-close:hover{color:#fff}
.log-item{border-left:3px solid var(--accent2);padding:10px 12px;margin-bottom:12px;background:var(--card2);border-radius:0 8px 8px 0}
.log-item .ver{font-weight:700;color:var(--accent2);font-size:.9rem}
.log-item .date{color:var(--muted);font-size:.72rem;margin-left:8px}
.log-item ul{margin:6px 0 0;padding-left:18px}
.log-item li{font-size:.82rem;line-height:1.55;color:#d0d5e0;margin-bottom:3px}
.log-item li b{color:var(--gold)}
</style>
</head>
<body>

<div id="modal" onclick="if(event.target===this)closeModal()">
  <div id="modal-card">
    <button id="modal-close" onclick="closeModal()">✕</button>
    <div id="modal-body"></div>
  </div>
</div>

<div class="header-wrap">
<div>
<h1>💻 Laptop VN — 7 phân khúc giá × 6 chuyên ngành</h1>
<div class="sub">Khảo sát 13 shop (TGDD, FPT, PhongVũ, Hacom, No1, CellphoneS, LaptopWorld, LaptopAZ, Laptop88, LaptopGame, Hoàng Hà, GearVN, ShopDunk) • __TOTAL__ máy mới • Cập nhật 13/08/2026 • <b style="color:var(--gold)">Giá + tình trạng hàng đã verify PDP</b></div>
</div>
<button class="info-btn" onclick="openLog()" title="Cập nhật & hướng dẫn">ⓘ</button>
</div>

<!-- Update Log modal -->
<div class="log-modal" id="log-modal" onclick="if(event.target===this)closeLog()">
  <div class="log-card">
    <button class="log-close" onclick="closeLog()">✕</button>
    <h3>📋 Cập nhật & hướng dẫn</h3>
    <div class="log-sub">Bản cập nhật 13/08/2026 — những gì mới & cách dùng</div>

    <div class="log-item">
      <div class="ver">v2.1 — 13/08/2026 <span class="date">bản mới nhất</span></div>
      <ul>
        <li><b>Chấm điểm chuẩn PassMark</b> — CPU/GPU tính theo benchmark thật (cpubenchmark.net), không còn ước lượng chủ quan</li>
        <li><b>Điểm RAM/Ổ cứng/Màn hình/Pin theo chuẩn ngành</b> — RAM log2, SSD NVMe vs SATA vs HDD, màn hình PPI + tần số quét + OLED, pin theo giới hạn hàng không 100Wh</li>
        <li><b>Đủ thông số 99.8% máy</b> — bổ sung CPU/GPU cho hơn 800 máy từ PDP thật</li>
        <li><b>Thêm ShopDunk</b> — 63 máy Mac (MacBook/Neo/Mac mini/iMac/Studio/Pro) vào danh sách</li>
        <li><b>Tình trạng hàng verify PDP</b> — Còn hàng / Sắp về hàng / Hết hàng từ trang chính hãng</li>
      </ul>
    </div>

    <div class="log-item">
      <div class="ver">Cách dùng</div>
      <ul>
        <li><b>🎯 Phân khúc giá</b> — lọc theo khoảng giá (dưới 10tr → 40tr+)</li>
        <li><b>🎓 Chuyên ngành</b> — đổi trọng số điểm theo ngành (AI, CNTT, Đồ họa, VP, Game, CAD)</li>
        <li><b>🙈 Ẩn máy hết hàng</b> — bỏ máy không mua được (vẫn xếp điểm khi bật lại)</li>
        <li><b>⚙️ Tự chỉnh trọng số</b> — kéo slider đổi tầm quan trọng từng tiêu chí</li>
        <li><b>Bấm vào máy</b> — xem chi tiết điểm từng tiêu chí & nút tới trang mua</li>
      </ul>
    </div>
  </div>
</div>

<div class="notice">
  <div class="ico">⚠️</div>
  <div><b>Nguồn từ GearVN đang lỗi</b></div>
</div>

<div class="hero">
<div class="hero-card"><div class="label">Tổng máy khảo sát</div><div class="big">__TOTAL__</div><div class="sub2">máy mới, đã lọc cũ/likenew</div></div>
<div class="hero-card"><div class="label">Số shop</div><div class="big">12</div><div class="sub2">giá niêm yết hiện tại</div></div>
<div class="hero-card"><div class="label">Phân khúc giá</div><div class="big">7</div><div class="sub2">từ dưới 10tr đến 40tr+</div></div>
<div class="hero-card"><div class="label">Chuyên ngành</div><div class="big">6</div><div class="sub2">AI, CNTT, ĐH, VP, Game, CAD</div></div>
</div>

<div class="controls">
<div class="row"><div class="row-label">💰 Phân khúc:</div>__SEGCHIPS__</div>
<div class="row"><div class="row-label">🎓 Chuyên ngành:</div>__PROFCHIPS__</div>
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

<div class="section">📌 Ghi chú</div>
<div class="footer">
• Giá = giá bán hiện tại từ PDP (đã loại giá trả góp hàng tháng).<br>
• Stock đã verify PDP cho band 15-25tr (toàn bộ); các band khác 1 phần — "? Kiểm tra" nghĩa là chưa verify, nên xác nhận trước khi mua.<br>
• Hàng cũ / like new / refurb / outlet đã loại. TrungTran không công khai giá.<br>
• Điểm = chấm theo trọng số từng chuyên ngành × hệ số giá trị phân khúc. Bấm ⓘ xem chi tiết.<br>
• Made with ❤️ by <span class="credit"><a href="https://www.facebook.com/ITlikegame/" target="_blank" rel="noopener">hungfan</a><span class="tip">P/s: Nếu muốn góp ý gì thì ới mình nhé 😘</span></span> - sguet
</div>

<script>
const SEGS = __SEGS__;
const PROFS = __PROFS__;
const ITEMS = __ITEMS__;
const SHOPL = __SHOPL__;
const KNAMES = ['CPU','RAM','GPU','Màn hình','Pin','Ổ cứng'];
const WKEYS = ['cpu','ram','gpu','display','battery','storage'];
let curSeg = 's15', curProf = 'AI / Data Science';
let customWeights = null, hideOOS = false;

function fmtPrice(p){return (p/1e6).toFixed(1).replace('.',',')+'tr';}
function badge(k){if(k==='CÒN')return '<span class="badge badge-green">● Còn hàng</span>';if(k==='HẾT')return '<span class="badge badge-red">✕ Hết hàng</span>';if(k==='LIÊN HỆ')return '<span class="badge badge-gold">✆ Liên hệ</span>';return '<span class="badge badge-gray">? Kiểm tra</span>';}
function spec(r){const p=[];if(r.c)p.push('CPU: '+r.c);if(r.r)p.push('RAM: '+r.r);if(r.t)p.push('SSD: '+r.t);if(r.d)p.push('Màn: '+r.d);if(r.g)p.push('GPU: '+r.g);return p.join(' • ');}
function estBadge(r){return r.e ? '<span class="badge badge-gray" title="CPU không nhận diện được — điểm ước tính">≈ ước tính</span> ' : '';}
function currentWeights(){return customWeights || PROFS[curProf].w;}
function computeScore(r, w){let t=0;for(let i=0;i<6;i++)t+=(r.q[i]||0)*(w[WKEYS[i]]||0);return t;}
function valueFactorFor(price, seg){const center=(seg.lo+seg.hi)/2;const dist=Math.abs(price-center)/Math.max(1,(seg.hi-seg.lo));const raw=1.0+(price>center? -dist*0.15 : dist*0.15);return Math.min(1.15,Math.max(0.85,raw));}

function showDetail(r){
  const w = currentWeights();
  const detVals = [r.c||'—', r.r||r.i[5]+'GB', r.g||'—', r.i[0]+'" OLED='+(r.i[2]?'có':'không'), r.i[3]+'Wh', r.t||r.i[4]+'GB'];
  let rows = '';
  for(let i=0;i<6;i++){
    const sc = r.q[i]||0, wt = w[WKEYS[i]]||0;
    const pct = (sc*wt).toFixed(1);
    rows += `<tr><td style="white-space:nowrap">${KNAMES[i]}</td><td style="text-align:center">${Math.round(wt*100)}%</td><td style="text-align:center">${sc.toFixed(0)}/100</td><td style="text-align:center;color:var(--accent2);font-weight:700">${pct}</td><td><div style="background:var(--card2);border-radius:4px;height:8px"><div style="background:linear-gradient(90deg,var(--accent),var(--accent2));height:8px;border-radius:4px;width:${Math.round(sc)}%"></div></div></td><td style="font-size:.72rem;color:var(--muted)">${detVals[i]}</td></tr>`;
  }
  const seg = SEGS.find(s=>s.id===curSeg);
  const vf = valueFactorFor(r.p, seg);
  const score = computeScore(r,w) * vf;
  const estNote = r.e ? '<div style="color:var(--gold);font-size:.75rem;margin-top:4px">⚠️ CPU không nhận diện được — điểm CPU là ước tính (60/100)</div>' : '';
  document.getElementById('modal-body').innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:12px">
      <div><div style="font-weight:700;font-size:1rem;line-height:1.4">${estBadge(r)}${r.n}</div>
      <div style="color:var(--muted);font-size:.8rem;margin-top:4px">${fmtPrice(r.p)} • ${SHOPL[r.s]||r.s} • ${badge(r.k)}</div>${estNote}</div>
      <div style="text-align:center;min-width:80px"><div style="font-size:1.6rem;font-weight:800;color:var(--accent2)">${score.toFixed(1)}</div><div style="font-size:.65rem;color:var(--muted)">ĐIỂM</div></div>
    </div>
    <div style="color:var(--muted);font-size:.78rem;margin-bottom:10px;line-height:1.7">Ngành <b style="color:var(--accent2)">${curProf}</b> — điểm tiêu chí × trọng số = <b style="color:var(--accent2)">${computeScore(r,w).toFixed(1)}</b><br>Hệ số giá trị phân khúc (độ gần giữa band ${seg.emoji} ${seg.label}): <b style="color:var(--accent2)">${vf.toFixed(2)}</b> — giới hạn 0.85–1.15<br>= <b style="color:var(--accent2)">${score.toFixed(1)}</b> điểm cuối</div>
    <table style="width:100%;font-size:.8rem"><tr><th>Tiêu chí</th><th style="text-align:center">Trọng số</th><th style="text-align:center">Điểm</th><th style="text-align:center">Đóng góp</th><th style="width:30%"></th><th>Chi tiết</th></tr>${rows}</table>`;
  document.getElementById('modal').style.display = 'flex';
}
function closeModal(){document.getElementById('modal').style.display='none';}
function openLog(){document.getElementById('log-modal').classList.add('open');}
function closeLog(){document.getElementById('log-modal').classList.remove('open');}
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeModal();closeLog();}});
function toggleOOS(){hideOOS=!hideOOS;document.getElementById('oos-toggle').classList.toggle('active',hideOOS);render();}
function selectSeg(el){curSeg=el.dataset.seg;document.querySelectorAll('.chip[data-seg]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function selectProf(el){curProf=el.dataset.prof;customWeights=null;document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function render(){
  const seg = SEGS.find(s=>s.id===curSeg);
  const w = currentWeights();
  let inBand = ITEMS.filter(x=>x.p>=seg.lo&&x.p<seg.hi);
  if(hideOOS) inBand = inBand.filter(x=>x.k!=='HẾT');
  const scored = inBand.map(r=>({r, s: computeScore(r,w)*valueFactorFor(r.p,seg)})).sort((a,b)=>b.s-a.s);
  // Desktop table
  let rows = scored.map((item,i)=>{
    const r = item.r, oos = r.k==='HẾT'?' class="oos-row"':'';
    return `<tr${oos}><td class="rank ${i===0?'rank-1':''} col-rank">${i+1}</td><td><div class="name">${estBadge(r)}${r.n.slice(0,85)}</div><div class="spec">${spec(r)}</div></td><td class="price col-price">${fmtPrice(r.p)}</td><td class="col-stock">${badge(r.k)}</td><td class="score col-score">${item.s.toFixed(1)} <span class="info-btn" onclick="showDetail(ITEMS[${ITEMS.indexOf(r)}])" title="Xem giải thích điểm">ⓘ</span></td><td class="col-shop"><span class="shop">${SHOPL[r.s]||r.s}</span><br><a class="view-btn" href="${r.u}" target="_blank" rel="noopener">Xem</a></td></tr>`;
  }).join('');
  // Mobile cards
  const mode = customWeights ? '🎛️ trọng số tự chỉnh' : `ngành <b style="color:var(--accent2)">${curProf}</b>`;
  const oosInfo = hideOOS ? ' (đã ẩn máy hết hàng)' : '';
  const header = `<div style="margin-bottom:10px;color:var(--muted);font-size:.85rem">Phân khúc <b style="color:var(--accent2)">${seg.emoji} ${seg.label}</b> — <b style="color:var(--accent2)">${scored.length}</b> máy • ${mode}${oosInfo} • <span style="color:var(--muted)">bấm ⓘ xem giải thích • cuộn xem hết</span></div>`;
  const desktop = `<div class="table-wrap"><table class="head-table"><thead><tr><th class="col-rank">#</th><th>Sản phẩm</th><th class="col-price">Giá</th><th class="col-stock">Hàng</th><th class="col-score">Điểm</th><th class="col-shop">Shop</th></tr></thead></table><div class="table-scroll"><table><tbody>${rows}</tbody></table></div></div>`;
  // Mobile: 1 bảng duy nhất (thead sticky) trong container vuốt ngang+dọc
  const mobile = `<div class="swipe-hint">👆 Vuốt ngang để xem hết bảng • vuốt dọc xem hết máy</div><div class="mobile-scroll"><table class="mobile-table"><thead><tr><th class="col-rank">#</th><th>Sản phẩm</th><th class="col-price">Giá</th><th class="col-stock">Hàng</th><th class="col-score">Điểm</th><th class="col-shop">Shop</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  document.getElementById('table-container').innerHTML = header + desktop + mobile;
}
// custom weights
const CRITERIA = [['cpu','CPU'],['ram','RAM'],['gpu','GPU'],['display','Màn hình'],['battery','Pin'],['storage','Ổ cứng']];
function togglePanel(){const b=document.getElementById('cp-body');b.classList.toggle('open');document.getElementById('cp-arrow').innerText=b.classList.contains('open')?'▴':'▾';if(b.classList.contains('open')&&!document.getElementById('cp-sliders').children.length)buildSliders();}
function buildSliders(){const w=currentWeights();let vals=CRITERIA.map(([k])=>Math.round(w[k]*100));const diff=100-vals.reduce((a,b)=>a+b,0);if(diff!==0){let mx=0;for(let i=1;i<vals.length;i++)if(vals[i]>vals[mx])mx=i;vals[mx]+=diff;}document.getElementById('cp-sliders').innerHTML=CRITERIA.map(([k,l],i)=>`<div class="cp-slider"><label>${l}</label><input type="range" min="0" max="50" step="1" value="${vals[i]}" data-key="${k}" oninput="this.parentElement.querySelector('.val').innerText=this.value+'%';updateTotal()"><span class="val">${vals[i]}%</span></div>`).join('');updateTotal();}
function updateTotal(){const t=Array.from(document.querySelectorAll('#cp-sliders input')).reduce((s,i)=>s+parseInt(i.value),0);document.getElementById('cp-total-val').innerText=t+'%';document.getElementById('cp-total-warn').style.display=t===100?'none':'inline';}
function useProfile(p){curProf=p;document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));const ch=document.querySelector(`.chip[data-prof="${p}"]`);if(ch)ch.classList.add('active');customWeights=null;buildSliders();render();}
function resetCustom(){useProfile(curProf);}
function applyCustom(){const w={};let t=0;Array.from(document.querySelectorAll('#cp-sliders input')).forEach(i=>{w[i.dataset.key]=parseInt(i.value)/100;t+=parseInt(i.value);});if(t!==100){alert('Tổng trọng số phải = 100%! Hiện: '+t+'%');return;}customWeights=w;render();}
// watch list
document.getElementById('table-container');
document.querySelectorAll('.chip[data-seg]')[3].classList.add('active');
document.querySelectorAll('.chip[data-prof]')[0].classList.add('active');
render();
</script>
</body></html>"""

# Segments chips
seg_chips = "".join(f'<div class="chip" data-seg="{s["id"]}" onclick="selectSeg(this)">{s["emoji"]} {s["label"]}</div>' for s in SEGMENTS)
prof_chips = "".join(f'<div class="chip" data-prof="{p}" onclick="selectProf(this)">{p}</div>' for p in profiles)

html = HTML
html = html.replace("__TOTAL__", str(len(items)))
html = html.replace("__SEGCHIPS__", seg_chips)
html = html.replace("__PROFCHIPS__", prof_chips)
html = html.replace("__SEGS__", json.dumps([{k: s[k] for k in ("id","label","emoji","lo","hi")} for s in SEGMENTS], ensure_ascii=False))
html = html.replace("__PROFS__", json.dumps(profiles, ensure_ascii=False))
html = html.replace("__ITEMS__", json.dumps(items_c, ensure_ascii=False))
html = html.replace("__SHOPL__", json.dumps(SHOP_LABEL, ensure_ascii=False))

out = os.path.expanduser("~/laptop-report-19m/bao-cao-laptop-phan-khuc.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"saved: {os.path.getsize(out)/1024/1024:.2f} MB")
