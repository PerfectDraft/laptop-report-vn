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

UPDATE_LOGS = [
    {
        "ver": "v2.11",
        "date": "22/08/2026",
        "is_latest": True,
        "items": [
            "<b>Khắc Phục Lỗi Nhận Diện Tồn Kho & Phục Hồi 110 Laptop Còn Hàng</b> — Sửa triệt để lỗi thứ tự ưu tiên trong bộ parser chuỗi (loại bỏ bắt nhầm từ khóa 'hết hàng' trong footer chính sách), phục hồi chính xác trạng thái Còn hàng cho 110 máy từ CellphoneS (+55 máy), Hacom (+35 máy), LaptopGame (+18 máy) và TGDD (+2 máy).",
            "<b>Tối Ưu Tỷ Lệ Sẵn Hàng Real-Time</b> — Tổng số laptop Còn hàng đạt 1.757 máy; số lượng máy Hết hàng thực tế giảm chuẩn xác về 19 máy.",
        ]
    },
    {
        "ver": "v2.10",
        "date": "17/08/2026",
        "is_latest": False,
        "items": [
            "<b>Kiểm toán & Chuẩn hoá 100% Thông Số Màn Hình</b> — Phục hồi đầy đủ thông số kích thước, độ phân giải (FHD, 2K, 3K, 4K, WUXGA, WQXGA), tần số quét (60Hz–360Hz) và công nghệ tấm nền (OLED / Mini-LED / IPS / Cảm ứng) cho toàn bộ 3.271 laptop.",
            "<b>Sửa Triệt Để Lỗi Điểm Màn Hình 0/100 Trong Modal</b> — Khắc phục bất đồng bộ dữ liệu, liên kết tính điểm động màn hình theo 6 chuyên ngành trực tiếp trong bảng phân tích chi tiết.",
            "<b>Bổ Sung Fallback Thông Số CPU & GPU Thật</b> — Nhận diện vi xử lý (Ryzen AI 300, Intel Ultra, Gen 13/14, Apple M) và Card đồ hoạ rời/tích hợp (RTX 30/40/50, Arc, Radeon, Iris Xe) từ tiêu đề, xóa bỏ hoàn toàn dấu '—' khuyết thiếu.",
        ]
    },
    {
        "ver": "v2.9",
        "date": "17/08/2026",
        "is_latest": False,
        "items": [
            "<b>Kiểm toán & Sửa 100% Link Hỏng 13 Đại Lý</b> — Rà soát toàn bộ đường dẫn sản phẩm, xóa bỏ hoàn toàn link cũ .html của GearVN và ký tự unicode lỗi của No1; cam kết 100% link trỏ thẳng vào Trang chi tiết sản phẩm thật (Direct PDP), 0 link 404, 0 link tìm kiếm.",
            "<b>Hệ Thống Báo Lỗi 1-Chạm & Đề Xuất Tính Năng</b> — Nút 🚩 thông minh tự động nạp cấu hình máy, form phân loại lỗi (Sai giá, Sai tồn kho, Sai linh kiện, Link hỏng) và tiếp nhận ý tưởng cải tiến UI/UX từ người dùng.",
            "<b>Gamification Thưởng Điểm & Thẻ Vinh Danh 3D</b> — Tích lũy +50 XP sau mỗi đóng góp, mở khóa 4 cấp bậc danh dự (Bug Scout → Tech Legend), pháo hoa Canvas Confetti 60 FPS và Thẻ Chứng Nhận Vàng Holographic.",
            "<b>Bảng Quản Lý Báo Cáo, Theo Dõi Tình Trạng & Xuất File Excel</b> — Cột 'Tình Trạng' 1-chạm (🕒 Đã tiếp nhận, ⚙️ Đang xử lý, ✅ Đã fix, 💡 Đã ghi nhận, ❌ Đóng), badge đếm số lượng tự động, xuất toàn bộ báo cáo ra file Excel (CSV) chuẩn UTF-8.",
        ]
    },
    {
        "ver": "v2.8",
        "date": "17/08/2026",
        "is_latest": False,
        "items": [
            "<b>Cập nhật Dữ liệu Thời gian thực từ GearVN</b> — Cào và bóc tách trực tiếp 57 sản phẩm từ 2 landing page Laptop Văn Phòng & Gaming; cập nhật 100% tình trạng tồn kho, giá khuyến mãi và cấu hình chuẩn theo PDP",
            "<b>Mở rộng Benchmark Chip Thế hệ Mới 2026</b> — Tích hợp điểm PassMark chuẩn cho AMD Ryzen AI 300/400 (AI 9 465, AI 9 365, AI 7 350), Intel Core Ultra 200V Lunar Lake (Ultra 9 288V, Ultra 5 226V), Intel Core Ultra 9 275HX / 386H, RTX 50 Mobile Series (5050/5060/5070/5070 Ti)",
            "<b>Đồng bộ & Mở rộng Dataset lên 3.379 Laptop</b> — Nâng cao độ phủ và độ chính xác phân khúc cho toàn bộ 13 shop đại lý công nghệ hàng đầu tại Việt Nam",
        ]
    },
    {
        "ver": "v2.7",
        "date": "16/08/2026",
        "is_latest": False,
        "items": [
            "<b>Phân Tách Điểm Apple GPU Theo Đời Chip (M1/M2/M3/M4/M5)</b> — Chuẩn hoá điểm GPU theo thế hệ chip thật, phản ánh chính xác tương quan sức mạnh giữa 10-core GPU M1/M2/M3/M4 với card rời NVIDIA RTX 3050/4050",
            "<b>Cân Bằng Điểm Đồ Hoạ dGPU & Unified Memory</b> — Đảm bảo card rời tải nặng liên tục và nhân CUDA/Tensor được định giá chuẩn xác cho khối ngành AI, 3D Render & Game",
            "<b>Nhận diện 100% Cấu hình Phần cứng Thật</b> — Chuẩn hoá toàn diện 3.328 sản phẩm laptop; 100% CPU, GPU, RAM, Ổ cứng SSD, Màn hình và Pin được bóc tách chuẩn xác theo model máy thật",
            "<b>Xoá bỏ 100% tình trạng 'Ước tính'</b> — Toàn bộ laptop đều có điểm Benchmark PassMark CPU & GPU thực tế, không còn bất kỳ máy nào bị fallback hay hiển thị nhãn ≈ ước tính",
        ]
    },
    {
        "ver": "v2.6",
        "date": "16/08/2026",
        "is_latest": False,
        "items": [
            "<b>Nhận diện 100% Cấu hình Phần cứng Thật</b> — Chuẩn hoá toàn diện 3.328 sản phẩm laptop; 100% CPU, GPU, RAM, Ổ cứng SSD, Màn hình và Pin được bóc tách chuẩn xác theo model máy thật",
            "<b>Xoá bỏ 100% tình trạng 'Ước tính'</b> — Toàn bộ laptop đều có điểm Benchmark PassMark CPU & GPU thực tế, không còn bất kỳ máy nào bị fallback hay hiển thị nhãn ≈ ước tính",
            "<b>Mở rộng Từ điển Vi xử lý & Card đồ hoạ</b> — Cập nhật dữ liệu PassMark cho thế hệ Intel Core Ultra 100/200, Core Series 1/2, AMD Ryzen AI 300, Ryzen 7000/8000, Apple M1-M5, RTX 50 Series Mobile (5050/5060/5070/5080/5090)",
            "<b>Khử trùng lặp & Lọc máy bàn/màn hình rời</b> — Loại bỏ 25 sản phẩm không phải laptop (Apple Studio Display, Mac Studio...) khỏi bảng xếp hạng",
        ]
    },
    {
        "ver": "v2.5",
        "date": "16/08/2026",
        "is_latest": False,
        "items": [
            "<b>Tìm kiếm tức thì (Instant Real-Time Search)</b> — Ô tìm kiếm thông minh theo thời gian thực (tên máy, chip CPU, RAM, GPU, SSD, Shop) kèm nút xóa ✕ tiện lợi",
            "<b>Tự động Fallback Thông số SSD/RAM</b> — 100% 3.328 máy hiển thị đầy đủ dung lượng RAM và SSD thực tế, khắc phục triệt để máy thiếu trường storage thô",
            "<b>Mở rộng Slider Trọng số tới 100%</b> — Cho phép tùy biến trọng số linh hoạt tới 100% cho nhu cầu chuyên biệt (AI, đồ họa 3D, code)",
            "<b>Bảo mật DOM & Thoát nhanh bằng phím ESC</b> — Escape chống tấn công XSS 100%, nhấn ESC đóng nhanh các cửa sổ modal",
            "<b>Trạng thái Tìm kiếm Rỗng (Empty State)</b> — Thông báo trực quan và gợi ý khi không tìm thấy máy phù hợp",
        ]
    },
    {
        "ver": "v2.4",
        "date": "16/08/2026",
        "is_latest": False,
        "items": [
            "<b>Sửa toàn diện giao diện Mobile & Màn hình hẹp</b> — Khắc phục lỗi mất nút xem chi tiết Score (<code>ⓘ</code>), tối ưu thanh cuộn và layout trực quan",
            "<b>Chạm nhanh (Quick Tap)</b> — Bấm vào bất kỳ đâu trên dòng sản phẩm để mở ngay bảng phân tích điểm chi tiết",
            "<b>Đường viền bảng liền mạch</b> — Tối ưu CSS table-cell đảm bảo đường phân cách giữa các hàng phẳng đẹp, không bị lồi",
            "<b>Tự động cập nhật số liệu động</b> — Đếm động số lượng máy, đại lý phân phối và các phân khúc giá",
        ]
    },
    {
        "ver": "v2.3",
        "date": "13/08/2026",
        "is_latest": False,
        "items": [
            "<b>Chuẩn hoá thang điểm theo max thực tế</b> — CPU/GPU chấm theo đỉnh laptop thật (RTX 5090 = 100), kéo giãn khoảng cách máy cao cấp",
            "<b>Bỏ máy desktop</b> (Mac Studio/Pro/iMac) khỏi ranking — chỉ còn laptop thật",
            "<b>Sửa điểm Apple GPU</b> — MacBook 'N-core GPU' chấm đúng theo chip (trước bị 100 tràn)",
            "Ghi chú hạn chế: TGP/tản nhiệt, RAM hàn chưa có dữ liệu đủ từ shop",
        ]
    },
    {
        "ver": "v2.2",
        "date": "13/08/2026",
        "is_latest": False,
        "items": [
            "<b>Bỏ thưởng +10 cho card rời (dGPU)</b> — điểm GPU thuần theo PassMark G3D, không còn đảo hạng sai (card rời yếu không vượt iGPU mạnh)",
            "<b>Điểm Apple Silicon chuẩn Geekbench Metal</b> — M1→M5 Max quy đổi thật (anchor Notebookcheck/Blender), không ước lượng",
            "<b>Màn hình chấm theo ngành</b> — Game ưu tần số quét, Đồ họa ưu chất lượng màu, Lập trình/VP ưu độ phân giải",
            "<b>Sửa hệ số giá trị phân khúc</b> — giá ở biên band giờ đúng ±15% (trước chỉ ±7.5%)",
            "<b>Tách 2 loại điểm</b> — Điểm giá trị (xếp hạng chính) + Điểm phần cứng (xem trong chi tiết máy)",
            "<b>Badge ▲/▼</b> — cạnh điểm báo máy đang hời hơn/đắt hơn phần cứng thật",
            "<b>Nút Sort</b> — đổi xếp hạng theo phần cứng thuần hoặc theo giá trị",
        ]
    },
    {
        "ver": "v2.1",
        "date": "13/08/2026",
        "is_latest": False,
        "items": [
            "<b>Chấm điểm chuẩn PassMark</b> — CPU/GPU tính theo benchmark thật (cpubenchmark.net), không còn ước lượng chủ quan",
            "<b>Điểm RAM/Ổ cứng/Màn hình/Pin theo chuẩn ngành</b> — RAM log2, SSD NVMe vs SATA vs HDD, màn hình PPI + tần số quét + OLED, pin theo giới hạn hàng không 100Wh",
            "<b>Đủ thông số 99.8% máy</b> — bổ sung CPU/GPU cho hơn 800 máy từ PDP thật",
            "<b>Thêm ShopDunk</b> — 63 máy Mac (MacBook/Neo/Mac mini/iMac/Studio/Pro) vào danh sách",
            "<b>Tình trạng hàng verify PDP</b> — Còn hàng / Sắp về hàng / Hết hàng từ trang chính hãng",
        ]
    },
]

def fmt_price(p):
    return f"{p//1_000_000}.{(p%1_000_000)//100_000}tr"

def stock_badge(stock):
    if stock == "CÒN": return '<span class="badge badge-green">● Còn hàng</span>'
    if stock == "HẾT": return '<span class="badge badge-red">✕ Hết hàng</span>'
    if stock == "LIÊN HỆ": return '<span class="badge badge-gold">✆ Liên hệ</span>'
    return '<span class="badge badge-gray">? Kiểm tra</span>'

def raw_scores(rec):
    # RAM: log2 (PassMark/Claude: 8=25, 16=50, 32=75, 64=100)
    ram_s = rec.get("_ram_s", 50.0)
    # Storage: bảng loại ổ (HDD 15, SATA 45, NVMe3 65, NVMe4 85, NVMe5 100) × dung lượng
    storage_s = rec.get("_storage_s", 85.0)
    # Pin: 100Wh = 100 (IATA/FAA)
    batt_s = rec.get("_batt_s", 50.0)
    # Display: PPI + Hz + panel (0.45/0.30/0.25)
    display_s = rec.get("_display_s", 70.0)
    # GPU: PassMark G3D log — KHÔNG bonus dGPU (Claude review: G3D đã phản ánh khoảng cách dGPU/iGPU, +10 tạo đảo hạng)
    gpu_eff = rec.get("_gpu_s", 50.0)
    cpu_s = rec.get("_cpu_s", 60.0)
    return [cpu_s, round(ram_s,1), round(gpu_eff,1), round(display_s,1), round(batt_s,1), round(storage_s,1)]

# Compact items
compact_file = os.path.join(BASE, "_compact_data.json")
if os.path.exists(compact_file):
    items_c = json.load(open(compact_file, encoding="utf-8"))
else:
    items_c = []
    DESKTOP_KW = ("mac studio", "mac pro", "imac", "studio display", "mac mini")
    for r in items:
        nm = (r.get("name") or r.get("title") or "").lower()
        p = r.get("price") or 0
        if not p or p < 1_000_000:
            continue  # bỏ các item không có giá hợp lệ
        if r.get("_fam") in ("monitor", "desktop") or any(k in nm for k in DESKTOP_KW):
            continue  # bỏ monitor (Studio Display...) + desktop (Mac Studio/Pro/iMac) khỏi ranking laptop
        items_c.append({
            "n": r.get("name") or r.get("title") or "Laptop", "p": p, "s": r.get("shop") or "shop", "u": r.get("url") or "",
            "c": (r.get("cpu") or "")[:60], "r": (r.get("ram") or "")[:40], "t": (r.get("storage") or "")[:45],
            "d": (r.get("display") or "")[:45], "g": (r.get("gpu") or "")[:50], "k": r.get("stock","?"),
            "q": raw_scores(r),
            "e": 1 if r.get("_fam") in ("unknown", None, "") else 0,
            "i": [round(r.get("_size", 15.6), 1), r.get("_res_s", 70), 1 if r.get("_oled") else 0, round(r.get("_bat", 50)), r.get("_storage", 512), r.get("_ram_gb", 16)],
            "dp": r.get("_disp_parts") or [50, 0, 70],  # [ppi, hz_score, panel]
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
::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
html{scrollbar-color:var(--border) var(--bg)}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,-apple-system,sans-serif;padding:24px}
h1{font-size:1.6rem;margin-bottom:4px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:.9rem;margin-bottom:20px}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.72rem;font-weight:600;white-space:nowrap}
.badge-green{background:rgba(52,211,153,.12);color:var(--green)}
.badge-red{background:rgba(248,113,113,.12);color:var(--red)}
.badge-gold{background:rgba(251,191,36,.12);color:var(--gold)}
.badge-gray{background:rgba(147,163,188,.15);color:var(--muted)}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:20px}
.hero-card{background:linear-gradient(135deg,var(--card),var(--card2));border:1px solid var(--border);border-radius:12px;padding:14px}
.hero-card .label{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.hero-card .big{font-size:1.15rem;font-weight:700;color:var(--accent2)}
.hero-card .sub2{font-size:.78rem;color:var(--muted);margin-top:4px}
.controls{margin:16px 0}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
.row-label{font-size:.82rem;font-weight:600;color:var(--muted);min-width:110px}
.chips-group{display:flex;flex-wrap:wrap;gap:7px;flex:1}
.chip{padding:6px 14px;border-radius:20px;background:var(--card);border:1px solid var(--border);cursor:pointer;font-size:.82rem;transition:all .18s;white-space:nowrap;user-select:none}
.chip:hover{background:var(--card2);border-color:var(--accent)}
.chip.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600;box-shadow:0 0 12px rgba(79,140,255,.3)}
.chip .cnt{font-size:.68rem;opacity:.75}

/* ── Search bar ── */
.search-row{position:relative;margin:12px 0 14px;display:flex;align-items:center}
.search-box{width:100%;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:10px 42px 10px 18px;color:var(--text);font-size:.88rem;outline:none;transition:all .2s ease}
.search-box:focus{border-color:var(--accent2);box-shadow:0 0 14px rgba(34,211,238,.2);background:var(--card2)}
.search-box::placeholder{color:var(--muted);opacity:.8}
.clear-search{position:absolute;right:14px;background:none;border:none;color:var(--muted);font-size:1rem;cursor:pointer;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:all .2s}
.clear-search:hover{color:#fff;background:var(--card2)}

.price{color:var(--green);font-weight:700;white-space:nowrap}
.rank{font-size:1.05rem;font-weight:800;color:var(--accent2)}
.rank-1{color:var(--gold)}
.shop{font-size:.72rem;color:var(--muted)}
.name{font-weight:600;line-height:1.35}
.spec{font-size:.75rem;color:var(--muted);margin-top:3px;line-height:1.45}
.score{font-weight:700;color:var(--accent2);white-space:nowrap}
.score-box{display:inline-flex;align-items:center;gap:4px;vertical-align:middle}
.score-val{font-size:.95rem}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.section{margin:24px 0 10px;font-size:1.05rem;font-weight:700;border-left:4px solid var(--accent);padding-left:12px}
.footer{margin-top:28px;padding-top:16px;border-top:1px solid var(--border);color:var(--muted);font-size:.78rem;line-height:1.7}
.notice{display:flex;gap:12px;align-items:flex-start;background:linear-gradient(135deg,rgba(251,191,36,.1),rgba(248,113,113,.08));border:1px solid var(--gold);border-radius:12px;padding:12px 16px;margin-bottom:18px;font-size:.85rem;line-height:1.6}
.notice .ico{font-size:1.3rem;line-height:1.2}
.notice b{color:var(--gold)}
.notice a{color:var(--accent2);font-weight:600;text-decoration:underline}
.credit{position:relative;display:inline-block;cursor:help}
.credit a{color:var(--accent2);font-weight:600}
.credit .tip{visibility:hidden;opacity:0;position:absolute;bottom:130%;left:50%;transform:translateX(-50%) translateY(4px);background:var(--card2);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:8px;font-size:.75rem;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.45);transition:opacity .18s,transform .18s;z-index:50;pointer-events:none}
.credit:hover .tip{visibility:visible;opacity:1;transform:translateX(-50%) translateY(0)}

/* ── Nút Chi Tiết Score trong bảng ── */
.score-detail-btn{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.35);color:var(--accent2);font-size:.78rem;font-weight:700;cursor:pointer;margin-left:4px;vertical-align:middle;transition:all .18s ease;padding:0;line-height:1}
.score-detail-btn:hover{background:var(--accent2);color:#0f1420;border-color:var(--accent2);transform:scale(1.15);box-shadow:0 0 10px rgba(34,211,238,.4)}
.score-detail-btn:active{transform:scale(0.95)}

/* ── Nút Hướng Dẫn Header / FAB Mobile ── */
.header-wrap{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}
.guide-btn{flex-shrink:0;padding:8px 16px;border-radius:20px;border:1px solid var(--border);background:var(--card);color:var(--accent2);font-size:.85rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:all .2s;margin-top:2px}
.guide-btn:hover{border-color:var(--accent2);background:var(--card2);transform:translateY(-1px);box-shadow:0 4px 14px rgba(34,211,238,.18)}

#modal{display:none;position:fixed;inset:0;background:rgba(5,8,15,.75);backdrop-filter:blur(6px);z-index:100;align-items:center;justify-content:center;padding:20px}
#modal-card{background:linear-gradient(180deg,var(--card),#141b2b);border:1px solid var(--border);border-radius:16px;max-width:760px;width:100%;max-height:88vh;overflow-y:auto;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.65)}
#modal-close{float:right;cursor:pointer;color:var(--muted);font-size:1.3rem;border:none;background:none;width:30px;height:30px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:all .2s}
#modal-close:hover{color:#fff;background:var(--card2)}

.modal-table{width:100%;border-collapse:collapse;font-size:.8rem}
.modal-table th{background:var(--card2);padding:8px 10px;text-align:left;font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.3px}
.modal-table td{padding:8px 10px;border-top:1px solid var(--border);vertical-align:middle}

.custom-panel{margin:14px 0;background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.cp-head{padding:12px 16px;cursor:pointer;font-weight:600;display:flex;justify-content:space-between;align-items:center;font-size:.92rem}
.cp-head:hover{background:var(--card2)}
.cp-body{padding:14px 16px;border-top:1px solid var(--border);display:none}
.cp-body.open{display:block}
.cp-presets{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:12px}
.cp-btn{padding:5px 12px;border-radius:14px;background:var(--card2);border:1px solid var(--border);color:var(--text);cursor:pointer;font-size:.75rem;transition:.2s}
.cp-btn:hover{border-color:var(--accent)}
.cp-sliders{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px 20px;margin-bottom:12px}
.cp-slider{display:flex;align-items:center;gap:10px;padding:2px 0}
.cp-slider label{font-size:.8rem;min-width:70px;color:var(--muted)}
.cp-slider input[type=range]{flex:1;accent-color:var(--accent);height:6px;cursor:pointer}
.cp-slider .val{font-size:.8rem;min-width:38px;text-align:right;color:var(--accent2);font-weight:700}
.cp-total{font-size:.8rem;color:var(--muted);margin-bottom:10px}
.cp-apply{padding:8px 18px;border-radius:8px;background:var(--accent);border:none;color:#fff;font-weight:600;cursor:pointer;font-size:.85rem}
.cp-apply:hover{filter:brightness(1.15)}

/* ── Bảng Dữ liệu Thống nhất & Responsive ── */
.table-scroll-wrap{max-height:78vh;overflow-y:auto;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:12px;border:1px solid var(--border);background:var(--card)}
.report-table{width:100%;border-collapse:separate;border-spacing:0;font-size:.83rem;min-width:680px}
.report-table thead th{position:sticky;top:0;z-index:10;background:var(--card2);padding:10px;text-align:left;font-weight:600;color:var(--muted);text-transform:uppercase;font-size:.7rem;letter-spacing:.4px;border-bottom:1px solid var(--border)}
.report-table td{padding:9px 10px;border-bottom:1px solid var(--border);vertical-align:top}
.report-table tbody tr{cursor:pointer;transition:background .15s}
.report-table tbody tr:hover td{background:rgba(79,140,255,.06)}
.report-table tbody tr:active td{background:rgba(79,140,255,.12)}
.report-table tbody tr:last-child td{border-bottom:none}
tr.oos-row td{opacity:.55}
.col-rank{width:40px}
.col-price{width:90px}
.col-stock{width:105px}
.col-score{width:110px}
.col-shop{width:80px}
.view-btn{display:inline-block;background:var(--accent);color:#fff!important;padding:4px 12px;border-radius:6px;font-weight:600;font-size:.75rem;text-decoration:none!important;transition:.2s;margin-top:3px;text-align:center}
.view-btn:hover{background:#3b76e0;transform:translateY(-1px);box-shadow:0 2px 8px rgba(79,140,255,.35)}
.view-btn:active{transform:translateY(0)}

.vf-badge{font-size:.65rem;margin-right:2px}
.vf-up{color:var(--green)}
.vf-down{color:var(--red)}
.sort-toggle{margin-left:10px;padding:4px 12px;border-radius:14px;border:1px solid var(--border);background:var(--card);color:var(--muted);font-size:.75rem;cursor:pointer;transition:all .18s}
.sort-toggle:hover{border-color:var(--accent2);color:var(--text)}
.sort-toggle.active{color:var(--accent2);border-color:var(--accent2);font-weight:600}

/* ── Responsive Mobile & Tablet ── */
@media (max-width: 768px){
  body{padding:12px;padding-bottom:85px}
  h1{font-size:1.18rem}
  .sub{font-size:.78rem;margin-bottom:14px}
  .notice{font-size:.78rem;padding:10px 12px;margin-bottom:14px}
  .hero{grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:14px}
  .hero-card{padding:10px}
  .hero-card .big{font-size:1.05rem}
  .row{flex-direction:column;align-items:flex-start;gap:6px;margin-bottom:10px}
  .row-label{width:100%;font-size:.78rem}
  .chips-group{display:flex;gap:6px;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px}
  .chip{font-size:.76rem;padding:6px 12px;flex-shrink:0}
  .cp-sliders{grid-template-columns:1fr;gap:8px}
  .table-scroll-wrap{max-height:72vh;border-radius:10px}
  .report-table{font-size:.78rem;min-width:630px}
  .report-table td{padding:8px}
  .col-rank{width:32px}
  .col-price{width:80px}
  .col-stock{width:95px}
  .col-score{width:100px}
  .col-shop{width:70px}
  .score-detail-btn{width:24px;height:24px;font-size:.82rem;margin-left:4px}
  .view-btn{padding:5px 12px;font-size:.72rem}
  .guide-btn{position:fixed;right:16px;bottom:16px;z-index:90;width:52px;height:52px;border-radius:50%;justify-content:center;font-size:1.25rem;padding:0;background:linear-gradient(135deg,var(--card),var(--card2));border:1.5px solid var(--accent2);box-shadow:0 8px 24px rgba(0,0,0,.6),0 0 16px rgba(34,211,238,.25)}
  .guide-btn .guide-btn-label{display:none}
  .swipe-hint{display:flex;align-items:center;gap:6px;color:var(--accent2);font-size:.74rem;margin-bottom:6px}
  .table-header-info{flex-direction:column;gap:6px;margin-bottom:8px}
  .thi-right{display:flex;justify-content:space-between;align-items:center;width:100%}
  .thi-hint{display:none}
  .watch-table,.footer{font-size:.72rem}
  #modal{padding:10px}
  #modal-card{padding:16px;max-height:92vh;border-radius:14px}
  .log-card{padding:20px 16px;border-radius:14px}
}
@media (max-width: 520px){
  .modal-table .col-bar{display:none}
  .modal-score-box{min-width:70px}
}
@media (min-width: 769px){
  .swipe-hint{display:none}
  .chips-group{display:contents}
  .table-header-info{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;color:var(--muted);font-size:.85rem}
  .thi-right{display:flex;align-items:center;gap:10px}
}

/* ── Update Log + Tiêu chí chấm điểm — notebook design ── */
.log-modal{display:none;position:fixed;inset:0;background:rgba(5,8,16,.72);backdrop-filter:blur(6px);z-index:200;align-items:center;justify-content:center;padding:16px}
.log-modal.open{display:flex}
.log-card{background:linear-gradient(180deg,var(--card),#151d2e);border:1px solid var(--border);border-radius:18px;max-width:980px;width:95%;max-height:88vh;overflow-y:auto;padding:24px 26px;position:relative;box-shadow:0 20px 70px rgba(0,0,0,.65),0 0 0 1px rgba(79,140,255,.08);animation:logIn .35s cubic-bezier(.2,.9,.3,1.2)}
.log-card::-webkit-scrollbar{width:8px}
.log-card::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
.log-card h3{color:var(--gold);margin:0 0 2px;font-size:1.18rem;letter-spacing:.2px}
.log-card .log-sub{color:var(--muted);font-size:.78rem;margin-bottom:14px}
.log-close{position:absolute;top:14px;right:16px;background:var(--card2);border:1px solid var(--border);color:var(--muted);width:30px;height:30px;border-radius:50%;font-size:.95rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s}
.log-close:hover{color:#fff;border-color:var(--accent2);transform:rotate(90deg)}
.log-tabs{display:flex;gap:8px;margin-bottom:16px;border-bottom:1px solid var(--border);padding-bottom:12px;flex-wrap:wrap}
.tab-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:7px 15px;border-radius:18px;border:1px solid var(--border);background:var(--card2);color:var(--muted);font-size:.82rem;font-weight:600;cursor:pointer;transition:all .2s;white-space:nowrap;line-height:1.2}
.tab-btn:hover{color:var(--text);border-color:var(--accent2)}
.tab-btn.active{background:linear-gradient(135deg,rgba(79,140,255,.18),rgba(34,211,238,.12));border-color:var(--accent2);color:var(--accent2);font-weight:700;box-shadow:0 0 14px rgba(79,140,255,.15)}
.tab-count-pill{display:inline-flex;align-items:center;justify-content:center;min-width:18px;height:18px;padding:0 5px;border-radius:10px;background:rgba(34,211,238,.18);color:var(--accent2);font-size:.72rem;font-weight:800;margin-left:2px}
.tab-btn.active .tab-count-pill{background:var(--accent2);color:#0f172a}
.tab-pane{display:none;animation:paneIn .3s ease}
.tab-pane.active{display:block}

/* ── Reports Table & Admin Styling ── */
.reports-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:10px;border:1px solid var(--border);background:var(--card2);margin-top:8px}
.reports-table{width:100%;border-collapse:collapse;font-size:.78rem;text-align:left}
.reports-table th{background:rgba(15,23,42,.95);color:var(--accent2);padding:10px 12px;border-bottom:1px solid var(--border);font-weight:700;white-space:nowrap}
.reports-table td{padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:middle}
.reports-table tr:last-child td{border-bottom:none}
.reports-table tr:hover td{background:rgba(255,255,255,.025)}
.report-dev-name{font-weight:600;color:var(--text);font-size:.78rem;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;word-break:break-word}
.shop-pill{display:inline-block;padding:1px 6px;border-radius:6px;background:var(--card);font-size:.7rem;color:var(--gold);border:1px solid var(--border)}

.log-item{border-left:3px solid var(--accent2);padding:10px 12px;margin-bottom:12px;background:var(--card2);border-radius:0 10px 10px 0;animation:paneIn .35s ease both}
.log-item:nth-child(2){animation-delay:.04s}
.log-item:nth-child(3){animation-delay:.08s}
.log-item .ver{font-weight:700;color:var(--accent2);font-size:.9rem}
.log-item .date{color:var(--muted);font-size:.72rem;margin-left:8px}
.log-item ul{margin:6px 0 0;padding-left:18px}
.log-item li{font-size:.82rem;line-height:1.55;color:#d0d5e0;margin-bottom:3px}
.log-item li b{color:var(--gold)}

/* ── Tiêu chí chấm điểm — spec-sheet cards (Claude redesign 13/08/2026) ── */
.crit-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:560px){.crit-grid{grid-template-columns:1fr}}
.crit-card{position:relative;background:linear-gradient(180deg,var(--card),#141b2a);border:1px solid var(--border);border-radius:16px;padding:17px 17px 15px;overflow:hidden;transition:transform .18s cubic-bezier(.2,.8,.2,1),border-color .18s ease,box-shadow .18s ease}
.crit-card::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:var(--c);opacity:.32;transition:opacity .18s ease,box-shadow .18s ease}
.crit-card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--c) 42%,var(--border));box-shadow:0 14px 30px -12px color-mix(in srgb,var(--c) 45%,transparent)}
.crit-card:hover::before{opacity:1;box-shadow:0 0 14px 0 var(--c)}
.crit-cpu{--c:#4f8cff}
.crit-gpu{--c:#22d3ee}
.crit-ram{--c:#a78bfa}
.crit-display{--c:#f472b6}
.crit-battery{--c:#34d399}
.crit-storage{--c:#fbbf24}
.crit-head{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.crit-icon{flex:0 0 auto;width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--c) 16%,transparent);color:var(--c);transition:transform .18s ease,background .18s ease}
.crit-card:hover .crit-icon{transform:scale(1.08);background:color-mix(in srgb,var(--c) 22%,transparent)}
.crit-icon svg{width:18px;height:18px}
.crit-title{font-size:14.5px;font-weight:650;color:var(--text);margin:0;flex:1;letter-spacing:.1px}
.crit-badge{font-size:10px;font-weight:650;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);background:rgba(255,255,255,.04);border:1px solid var(--border);padding:3px 8px;border-radius:999px;white-space:nowrap}
.crit-formula{background:color-mix(in srgb,var(--c) 9%,var(--card));border:1px solid color-mix(in srgb,var(--c) 26%,transparent);border-radius:8px;padding:7px 11px;margin-bottom:10px;overflow-x:auto}
.crit-formula code{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:12.5px;color:var(--c);white-space:nowrap}
.crit-desc{font-size:12.5px;line-height:1.6;color:var(--muted);margin:0}
.crit-total{margin-top:18px;background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:15px 18px;text-align:center}
.crit-total-label{display:block;font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:7px}
.crit-total-formula{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:13.5px;color:var(--text);margin:0}
.tk-term{color:var(--accent2)}
.tk-weight{color:var(--accent)}
.tk-value{color:var(--gold)}
.panel-intro{font-size:13px;color:var(--muted);line-height:1.65;margin:0 0 18px;padding-bottom:16px;border-bottom:1px solid var(--border)}
@keyframes logIn{from{opacity:0;transform:translateY(24px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes paneIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

/* ── Header Actions & Badges ── */
.header-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge-contributor{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:20px;background:linear-gradient(135deg,rgba(251,191,36,.15),rgba(245,158,11,.08));border:1px solid rgba(251,191,36,.4);color:var(--gold);font-size:.78rem;font-weight:700;cursor:pointer;transition:all .2s;box-shadow:0 0 10px rgba(251,191,36,.12);user-select:none}
.badge-contributor:hover{transform:translateY(-1px);background:linear-gradient(135deg,rgba(251,191,36,.25),rgba(245,158,11,.15));border-color:var(--gold);box-shadow:0 0 16px rgba(251,191,36,.3)}
.feedback-btn{padding:8px 15px;border-radius:20px;border:1px solid rgba(34,211,238,.4);background:linear-gradient(135deg,rgba(34,211,238,.1),rgba(79,140,255,.08));color:var(--accent2);font-size:.84rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:all .2s;margin-top:2px}
.feedback-btn:hover{background:linear-gradient(135deg,rgba(34,211,238,.2),rgba(79,140,255,.18));border-color:var(--accent2);transform:translateY(-1px);box-shadow:0 4px 14px rgba(34,211,238,.2)}

/* ── Nút Báo Lỗi Hàng & Modal ── */
.report-row-btn{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:4px;background:none;border:1px solid transparent;color:var(--muted);font-size:.75rem;cursor:pointer;transition:all .18s;line-height:1;margin-left:4px;vertical-align:middle}
.report-row-btn:hover{color:var(--red);background:rgba(248,113,113,.12);border-color:rgba(248,113,113,.3);transform:scale(1.15)}
.report-modal-btn{padding:7px 14px;border-radius:6px;background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.35);color:var(--red);font-weight:600;font-size:.8rem;cursor:pointer;transition:.2s;display:inline-flex;align-items:center;gap:5px}
.report-modal-btn:hover{background:rgba(248,113,113,.22);border-color:var(--red);color:#fff}

/* ── Floating Action Button (FAB) Mobile & Scroll ── */
.fab-feedback{position:fixed;left:16px;bottom:16px;z-index:90;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;background:linear-gradient(135deg,#1e293b,#0f172a);border:1.5px solid var(--accent2);color:var(--accent2);box-shadow:0 8px 24px rgba(0,0,0,.6),0 0 16px rgba(34,211,238,.25);cursor:pointer;transition:all .2s}
.fab-feedback:hover{transform:scale(1.1);border-color:#fff;color:#fff;box-shadow:0 0 20px rgba(34,211,238,.5)}

/* ── Feedback Modal ── */
#feedback-modal{display:none;position:fixed;inset:0;background:rgba(5,8,15,.75);backdrop-filter:blur(6px);z-index:110;align-items:center;justify-content:center;padding:16px}
.feedback-card{background:linear-gradient(180deg,var(--card),#141b2b);border:1px solid var(--border);border-radius:16px;max-width:620px;width:100%;max-height:90vh;overflow-y:auto;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.7);animation:paneIn .25s ease both}
.fb-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.fb-head h3{font-size:1.15rem;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;margin:0}
.fb-close{cursor:pointer;color:var(--muted);font-size:1.3rem;border:none;background:none;width:30px;height:30px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:all .2s}
.fb-close:hover{color:#fff;background:var(--card2)}
.fb-tabs{display:flex;gap:8px;margin-bottom:16px;background:var(--card2);padding:4px;border-radius:10px;border:1px solid var(--border)}
.fb-tab-btn{flex:1;padding:8px 12px;border:none;border-radius:8px;background:none;color:var(--muted);font-weight:600;font-size:.82rem;cursor:pointer;transition:all .18s}
.fb-tab-btn.active{background:var(--accent);color:#fff;box-shadow:0 2px 10px rgba(79,140,255,.3)}
.fb-pane{display:none}
.fb-pane.active{display:block}
.fb-item-preview{background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:.82rem;line-height:1.5}
.fb-item-preview b{color:var(--accent2)}
.fb-label{font-size:.78rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.3px;margin:10px 0 6px;display:block}
.chip-select{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip-pill{padding:5px 12px;border-radius:16px;background:var(--card2);border:1px solid var(--border);color:var(--text);font-size:.78rem;cursor:pointer;transition:all .18s;user-select:none}
.chip-pill:hover{border-color:var(--accent2)}
.chip-pill.active{background:rgba(34,211,238,.18);border-color:var(--accent2);color:var(--accent2);font-weight:600}
.fb-input,.fb-textarea{width:100%;background:var(--card2);border:1px solid var(--border);border-radius:8px;padding:9px 12px;color:var(--text);font-size:.84rem;outline:none;transition:border-color .18s;box-sizing:border-box}
.fb-input:focus,.fb-textarea:focus{border-color:var(--accent2);box-shadow:0 0 10px rgba(34,211,238,.2)}
.fb-textarea{resize:vertical;min-height:75px}
.fb-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:18px;flex-wrap:wrap}
.fb-btn-submit{background:linear-gradient(135deg,var(--accent),#2563eb);color:#fff;border:none;padding:9px 20px;border-radius:8px;font-weight:700;font-size:.85rem;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}
.fb-btn-submit:hover{filter:brightness(1.15);transform:translateY(-1px);box-shadow:0 4px 14px rgba(79,140,255,.4)}
.fb-btn-alt{background:var(--card2);border:1px solid var(--border);color:var(--muted);padding:9px 14px;border-radius:8px;font-size:.8rem;font-weight:600;cursor:pointer;transition:all .18s}
.fb-btn-alt:hover{color:var(--text);border-color:var(--accent2)}

/* ── Reward / Holographic Contributor Card Modal ── */
#reward-modal{display:none;position:fixed;inset:0;background:rgba(5,8,15,.8);backdrop-filter:blur(8px);z-index:120;align-items:center;justify-content:center;padding:16px}
.reward-card{background:linear-gradient(180deg,#1e2638,#0f1420);border:1px solid rgba(251,191,36,.4);border-radius:20px;max-width:480px;width:100%;padding:26px;text-align:center;box-shadow:0 24px 70px rgba(0,0,0,.85),0 0 30px rgba(251,191,36,.2);animation:logIn .35s cubic-bezier(.34,1.56,.64,1) both}
.holo-gold-card{position:relative;background:linear-gradient(135deg,#231b08,#1a2035 50%,#281d09);border:1.5px solid var(--gold);border-radius:14px;padding:20px;margin:16px 0;text-align:left;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 20px rgba(251,191,36,.18)}
.holo-gold-card::after{content:'';position:absolute;inset:0;background:linear-gradient(105deg,transparent 20%,rgba(251,191,36,.2) 50%,transparent 80%);animation:shimmer 3s infinite linear;pointer-events:none}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.holo-title{font-size:.72rem;color:var(--gold);font-weight:800;letter-spacing:1px;text-transform:uppercase}
.holo-name{font-size:1.25rem;font-weight:800;color:#fff;margin:6px 0 4px;letter-spacing:.2px}
.holo-badge{display:inline-block;padding:3px 10px;border-radius:12px;background:rgba(251,191,36,.2);color:var(--gold);font-size:.75rem;font-weight:700;border:1px solid rgba(251,191,36,.4);margin-bottom:8px}
.holo-meta{display:flex;justify-content:space-between;font-size:.7rem;color:var(--muted);border-top:1px solid rgba(255,255,255,.1);padding-top:8px;margin-top:6px}
.cert-code{font-family:ui-monospace,monospace;color:var(--accent2)}
.reward-btn-close{width:100%;padding:10px 0;background:linear-gradient(135deg,var(--gold),#d97706);border:none;border-radius:10px;color:#0f1420;font-weight:800;font-size:.9rem;cursor:pointer;transition:all .2s;margin-top:10px}
.reward-btn-close:hover{filter:brightness(1.12);box-shadow:0 0 16px rgba(251,191,36,.5)}

/* ── Toast Notifications ── */
.toast-container{position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:8px;pointer-events:none}
#confetti-canvas{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9999}

/* ── Status Pills (Tình Trạng Xử Lý Báo Cáo) ── */
.status-pill{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:12px;font-size:.72rem;font-weight:700;cursor:pointer;transition:all .18s;user-select:none;white-space:nowrap}
.status-pill:hover{transform:scale(1.06);filter:brightness(1.15);box-shadow:0 0 10px rgba(0,0,0,.4)}
.status-received{background:rgba(251,191,36,.15);border:1px solid rgba(251,191,36,.4);color:var(--gold)}
.status-fixing{background:rgba(79,140,255,.18);border:1px solid rgba(79,140,255,.45);color:var(--accent2)}
.status-fixed{background:rgba(52,211,153,.18);border:1px solid rgba(52,211,153,.45);color:var(--green)}
.status-noted{background:rgba(167,139,250,.18);border:1px solid rgba(167,139,250,.45);color:#a78bfa}
.status-rejected{background:rgba(148,163,184,.15);border:1px solid rgba(148,163,184,.35);color:var(--muted)}

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
<h1>💻 Laptop VN — __SEGS_COUNT__ phân khúc giá × __PROFS_COUNT__ chuyên ngành</h1>
<div class="sub">Khảo sát __SHOPS_COUNT__ shop (__SHOP_NAMES__) • __TOTAL__ máy mới • Cập nhật __UPDATED_DATE__ • <b style="color:var(--gold)">Giá + tình trạng hàng đã verify PDP</b></div>
</div>
<div class="header-actions">
  <div id="user-badge-header" class="badge-contributor" onclick="openRewardModal(false)" title="Xem Thẻ vinh danh & Điểm XP đóng góp của bạn">🎖️ Bug Scout • 0 XP</div>
  <button class="feedback-btn" onclick="openFeedbackModal()" title="Báo lỗi hoặc đề xuất cải tiến">💬 Góp ý & Báo lỗi</button>
  <button class="guide-btn" onclick="openLog()" title="Cập nhật & hướng dẫn">ⓘ<span class="guide-btn-label"> Hướng dẫn</span></button>
</div>
</div>

<button class="fab-feedback" id="fab-feedback" onclick="openFeedbackModal()" title="Góp ý & Báo lỗi nhanh">💬</button>
<canvas id="confetti-canvas"></canvas>
<div id="toast-box" class="toast-container"></div>

<!-- Feedback & Issue Report Modal -->
<div id="feedback-modal" onclick="if(event.target===this)closeFeedbackModal()">
  <div class="feedback-card">
    <div class="fb-head">
      <h3>💬 Đóng góp & Báo cáo Lỗi</h3>
      <button class="fb-close" onclick="closeFeedbackModal()">✕</button>
    </div>
    <div class="fb-tabs">
      <button class="fb-tab-btn active" data-tab="device" onclick="switchFeedbackTab('device')">🚩 Báo lỗi máy / Sai giá</button>
      <button class="fb-tab-btn" data-tab="feature" onclick="switchFeedbackTab('feature')">💡 Đề xuất tính năng / UI</button>
    </div>

    <!-- Tab 1: Device Issue -->
    <div class="fb-pane active" id="fb-pane-device">
      <div id="fb-device-preview" class="fb-item-preview">
        Đang chọn máy: <b id="fb-device-name">Tất cả sản phẩm (Báo cáo chung)</b>
        <div id="fb-device-sub" style="color:var(--muted);font-size:.75rem;margin-top:2px"></div>
      </div>
      <label class="fb-label">1. Loại lỗi phát hiện (Chọn 1 chạm):</label>
      <div class="chip-select" id="device-issue-chips">
        <div class="chip-pill active" onclick="selectFeedbackChip(this, 'device')">🏷️ Sai giá bán</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'device')">📦 Sai tồn kho (Còn/Hết)</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'device')">⚙️ Sai CPU/GPU/RAM/SSD</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'device')">🔗 Link lỗi / Sai trang</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'device')">❓ Khác</div>
      </div>
      <label class="fb-label">2. Thông tin chính xác & Đề xuất sửa đổi:</label>
      <textarea id="fb-device-desc" class="fb-textarea" placeholder="Ví dụ: Giá thực tế trên website shop đang là 19.990.000đ, hoặc CPU máy này là Ryzen 7 không phải Ryzen 5..."></textarea>
      <label class="fb-label">3. Link dẫn chứng / Nguồn (Tùy chọn):</label>
      <input type="text" id="fb-device-link" class="fb-input" placeholder="https://shop.vn/san-pham... hoặc link ảnh">
      <label class="fb-label">4. Tên / Nickname của bạn (để in lên Thẻ Vinh Danh):</label>
      <input type="text" id="fb-contributor-name" class="fb-input" placeholder="Ví dụ: Hoàng Long, Alex Tech...">
      <div class="fb-actions">
        <button class="fb-btn-alt" onclick="copyFeedbackReport('device')">📋 Sao chép báo cáo</button>
        <button class="fb-btn-submit" onclick="submitFeedback('device')">🚀 Gửi Báo Cáo (+50 XP)</button>
      </div>
    </div>

    <!-- Tab 2: Feature Suggestion -->
    <div class="fb-pane" id="fb-pane-feature">
      <label class="fb-label">1. Chủ đề góp ý:</label>
      <div class="chip-select" id="feature-chips">
        <div class="chip-pill active" onclick="selectFeedbackChip(this, 'feature')">🏪 Thêm shop mới</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'feature')">🧮 Góp ý trọng số / Điểm số</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'feature')">🎨 Giao diện & Trải nghiệm (UI/UX)</div>
        <div class="chip-pill" onclick="selectFeedbackChip(this, 'feature')">✨ Tính năng mới</div>
      </div>
      <label class="fb-label">2. Tiêu đề ý tưởng:</label>
      <input type="text" id="fb-feat-title" class="fb-input" placeholder="Ví dụ: Thêm bộ lọc màn hình OLED, Thêm so sánh đối đầu 2 máy...">
      <label class="fb-label">3. Mô tả chi tiết đề xuất:</label>
      <textarea id="fb-feat-desc" class="fb-textarea" placeholder="Mô tả ý tưởng của bạn để team cải tiến trong bản cập nhật kế tiếp..."></textarea>
      <label class="fb-label">4. Tên / Nickname người đóng góp:</label>
      <input type="text" id="fb-feat-name" class="fb-input" placeholder="Ví dụ: Minh Quân, TechLover...">
      <div class="fb-actions">
        <button class="fb-btn-alt" onclick="copyFeedbackReport('feature')">📋 Sao chép ý kiến</button>
        <button class="fb-btn-submit" onclick="submitFeedback('feature')">💡 Gửi Đề Xuất (+50 XP)</button>
      </div>
    </div>
  </div>
</div>

<!-- Reward Holographic Card Modal -->
<div id="reward-modal" onclick="if(event.target===this)closeRewardModal()">
  <div class="reward-card">
    <div style="font-size:2.2rem;line-height:1">🎉 🎆 🎖️</div>
    <h2 style="font-size:1.35rem;font-weight:800;color:var(--gold);margin:8px 0 4px">CẢM ƠN BẠN ĐÃ ĐÓNG GÓP!</h2>
    <p style="color:var(--muted);font-size:.82rem;margin:0 0 14px">Bạn vừa nhận được <b style="color:var(--green)">+50 XP</b> uy tín người đóng góp cộng đồng!</p>
    
    <div class="holo-gold-card">
      <div class="holo-title">CHỨNG NHẬN ĐÓNG GÓP XUẤT SẮC</div>
      <div class="holo-name" id="reward-card-name">Nhà Đóng Góp Bí Ẩn</div>
      <div class="holo-badge" id="reward-card-rank">🥉 Thực Tập Sinh Săn Bug (Bug Scout)</div>
      <p style="font-size:.78rem;color:#e2e8f0;line-height:1.4;margin:6px 0">Đã tích cực rà soát & đóng góp dữ liệu giúp hệ thống Laptop Report VN ngày càng chính xác, uy tín và minh bạch.</p>
      <div class="holo-meta">
        <div>Mã chứng nhận: <span class="cert-code" id="reward-card-code">#LRVN-88392</span></div>
        <div>Tổng XP: <b id="reward-card-xp" style="color:var(--gold)">50 XP</b></div>
      </div>
    </div>

    <button class="reward-btn-close" onclick="closeRewardModal()">✨ Tuyệt vời, tiếp tục khám phá!</button>
  </div>
</div>


<!-- Update Log + Tiêu chí chấm điểm modal -->
<div class="log-modal" id="log-modal" onclick="if(event.target===this)closeLog()">
  <div class="log-card">
    <button class="log-close" onclick="closeLog()">✕</button>
    <h3>📋 Cập nhật & hướng dẫn</h3>
    <div class="log-sub">Bản cập nhật __UPDATED_DATE__ — những gì mới & cách dùng</div>
    <div class="log-tabs">
      <button class="tab-btn active" data-tab="updates" onclick="switchLogTab(this)">Cập nhật</button>
      <button class="tab-btn" data-tab="criteria" onclick="switchLogTab(this)">Tiêu chí chấm điểm</button>
      <button class="tab-btn" data-tab="guide" onclick="switchLogTab(this)">🏆 Báo lỗi & Thưởng</button>
      <button class="tab-btn" data-tab="reports" onclick="switchLogTab(this);renderReportsList()">📑 Báo cáo <span class="tab-count-pill" id="reports-count-badge">0</span></button>
    </div>

    <!-- Tab 4: Reports History & CSV Export -->
    <div class="tab-pane" id="pane-reports">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
        <div>
          <b style="color:var(--text);font-size:.95rem">📋 Nhật ký Báo Cáo & Góp Ý Người Dùng</b>
          <div style="color:var(--muted);font-size:.78rem">Toàn bộ ý kiến, lỗi giá, lỗi thông số từ cộng đồng được lưu trữ & đồng bộ tại đây.</div>
        </div>
        <div style="display:flex;gap:8px">
          <button class="fb-btn-submit" onclick="exportReportsToCSV()" style="padding:6px 14px;font-size:.8rem">📥 Xuất File Excel (CSV)</button>
          <button class="fb-btn-alt" onclick="clearReportsHistory()" style="padding:6px 12px;font-size:.8rem;color:var(--red)">🗑️ Xóa lịch sử</button>
        </div>
      </div>
      <div id="reports-list-container"></div>
    </div><!-- /pane-reports -->

    <div class="tab-pane active" id="pane-updates">
__UPDATE_LOGS__
    <div class="log-item">
      <div class="ver">Cách dùng nhanh</div>
      <ul>
        <li><b>🎯 Phân khúc giá</b> — lọc theo khoảng giá (dưới 10tr → 40tr+)</li>
        <li><b>🎓 Chuyên ngành</b> — đổi trọng số điểm theo ngành (AI, CNTT, Đồ họa, VP, Game, CAD)</li>
        <li><b>🔍 Tìm kiếm tức thì</b> — gõ tên máy, chip CPU, RAM, GPU, SSD hoặc Shop để lọc ngay lập tức</li>
        <li><b>🙈 Ẩn máy hết hàng</b> — bỏ máy không mua được (vẫn xếp điểm khi bật lại)</li>
        <li><b>⚙️ Tự chỉnh trọng số</b> — kéo slider đổi tầm quan trọng từng tiêu chí (tới 100%)</li>
        <li><b>Bấm vào máy</b> — xem chi tiết điểm từng tiêu chí & nút tới trang mua</li>
        <li><b style="color:var(--green)">▲</b> cạnh điểm = <b>giá hời</b> (rẻ hơn phần cứng) • <b style="color:var(--red)">▼</b> = <b>giá cao</b> hơn phần cứng — cùng dòng chú thích trên mỗi bảng</li>
      </ul>
    </div>
    </div><!-- /pane-updates -->

    <div class="tab-pane" id="pane-guide">
      <div class="log-item" style="border-left-color:var(--gold)">
        <div class="ver" style="color:var(--gold)">🚩 1. Hướng dẫn Báo sai thông tin & Giá bán (1-Chạm)</div>
        <ul>
          <li><b>Bước 1</b>: Khi phát hiện máy có giá sai, thông số chưa chuẩn (CPU, GPU, RAM, SSD), hoặc link hỏng, nhấp vào biểu tượng <b>🚩</b> ở cột Shop (cạnh nút "Xem").</li>
          <li><b>Bước 2</b>: Form báo lỗi tự động điền sẵn tên máy và cấu hình. Bạn chọn loại lỗi bằng Chips (ví dụ: 🏷️ <i>Sai giá bán</i>, ⚙️ <i>Sai thông số</i>) và nhập thông tin chính xác.</li>
          <li><b>Bước 3</b>: Nhập tên/nickname của bạn rồi bấm <b>"🚀 Gửi Báo Cáo (+50 XP)"</b>.</li>
        </ul>
      </div>

      <div class="log-item" style="border-left-color:var(--accent2)">
        <div class="ver" style="color:var(--accent2)">💡 2. Hướng dẫn Đề xuất Tính năng & Góp ý Hệ thống</div>
        <ul>
          <li>Nhấp nút <b>"💬 Góp ý & Báo lỗi"</b> ở thanh Header hoặc nút tròn nổi <b>💬</b> ở góc dưới màn hình.</li>
          <li>Chuyển sang tab <b>"💡 Đề xuất tính năng / UI"</b>, chọn chủ đề (🏪 <i>Thêm shop</i>, 🧮 <i>Trọng số</i>, 🎨 <i>UI/UX</i>, ✨ <i>Tính năng mới</i>), nhập ý tưởng và bấm Gửi.</li>
          <li>Có thể dùng nút <b>📋 Sao chép báo cáo</b> để gửi nhanh qua Zalo, Discord hoặc gửi Issue lên GitHub.</li>
        </ul>
      </div>

      <div class="log-item" style="border-left-color:var(--green)">
        <div class="ver" style="color:var(--green)">🎖️ 3. Quy chế Tích lũy Điểm XP, Cấp bậc & Thẻ Vinh Danh</div>
        <ul>
          <li>Mỗi lần gửi báo cáo hoặc góp ý hợp lệ, bạn nhận ngay <b>+50 XP</b> uy tín người đóng góp.</li>
          <li>Hệ thống tự động kích hoạt <b>Pháo hoa Confetti 🎆</b> và cấp <b>Thẻ Chứng Nhận Đóng Góp Vàng 🌟</b> mang mã số định danh <code>#LRVN-XXXXX</code>.</li>
          <li><b>4 Cấp bậc Danh dự</b> hiển thị trên Header:
            <br>• 🥉 <b>Thực Tập Sinh Săn Bug (Bug Scout)</b>: 0 – 49 XP
            <br>• 🥈 <b>Chuyên Viên Thẩm Định (Spec Inspector)</b>: 50 – 149 XP
            <br>• 🥇 <b>Kiến Trúc Sư Benchmark (Benchmark Master)</b>: 150 – 299 XP
            <br>• 👑 <b>Huyền Thoại Laptop VN (Tech Legend)</b>: 300+ XP
          </li>
        </ul>
      </div>
    </div><!-- /pane-guide -->

    <div class="tab-pane" id="pane-criteria">
      <p class="panel-intro">Mỗi tiêu chí được chuẩn hoá về thang điểm riêng theo công thức bên dưới, sau đó nhân trọng số theo phân khúc sử dụng và hệ số giá trị (điểm/giá) để ra điểm cuối.</p>
      <div class="crit-grid">

        <article class="crit-card crit-cpu">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="7" width="10" height="10" rx="1.5"/><rect x="10" y="10" width="4" height="4" rx="0.5"/><line x1="9" y1="2" x2="9" y2="5"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="15" y1="2" x2="15" y2="5"/><line x1="9" y1="19" x2="9" y2="22"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="15" y1="19" x2="15" y2="22"/><line x1="2" y1="9" x2="5" y2="9"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="2" y1="15" x2="5" y2="15"/><line x1="19" y1="9" x2="22" y2="9"/><line x1="19" y1="12" x2="22" y2="12"/><line x1="19" y1="15" x2="22" y2="15"/></svg></div>
            <h3 class="crit-title">CPU</h3>
            <span class="crit-badge">PassMark</span>
          </div>
          <div class="crit-formula"><code>score = ln(CPU Mark)</code></div>
          <p class="crit-desc">Hiệu năng đa nhân theo thang logarit, tránh lệch quá lớn giữa CPU cao cấp và phổ thông.</p>
        </article>

        <article class="crit-card crit-gpu">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="18" height="10" rx="2"/><circle cx="7.5" cy="12" r="2.2"/><circle cx="14.5" cy="12" r="2.2"/><line x1="20" y1="9.5" x2="22.5" y2="9.5"/><line x1="20" y1="14.5" x2="22.5" y2="14.5"/></svg></div>
            <h3 class="crit-title">GPU</h3>
            <span class="crit-badge">PassMark G3D</span>
          </div>
          <div class="crit-formula"><code>score = ln(G3D Mark)</code></div>
          <p class="crit-desc">Hiệu năng đồ hoạ tổng hợp, phản ánh khả năng chơi game và render.</p>
        </article>

        <article class="crit-card crit-ram">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2" width="12" height="18" rx="1.5"/><line x1="9" y1="6" x2="15" y2="6"/><line x1="9" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="15" y2="14"/><line x1="9" y1="20" x2="9" y2="22"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="15" y1="20" x2="15" y2="22"/></svg></div>
            <h3 class="crit-title">RAM</h3>
            <span class="crit-badge">Thông số NSX</span>
          </div>
          <div class="crit-formula"><code>score = log2(GB)</code></div>
          <p class="crit-desc">Thang log2 vì tăng gấp đôi (8→16→32GB) mới tạo khác biệt cảm nhận rõ rệt.</p>
        </article>

        <article class="crit-card crit-display">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4" width="19" height="13" rx="1.5"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="8" y1="21" x2="16" y2="21"/></svg></div>
            <h3 class="crit-title">Display</h3>
            <span class="crit-badge">RTings</span>
          </div>
          <div class="crit-formula"><code>score = f(PPI, Hz, Panel)</code></div>
          <p class="crit-desc">Kết hợp mật độ điểm ảnh, tần số quét và loại tấm nền (OLED / Mini-LED / IPS).</p>
        </article>

        <article class="crit-card crit-battery">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="17" height="8" rx="1.5"/><line x1="21" y1="10.5" x2="21" y2="13.5"/><path d="M12 9.5 L9.5 12.5 L12 12.5 L10.5 15"/></svg></div>
            <h3 class="crit-title">Battery</h3>
            <span class="crit-badge">IATA / NSX</span>
          </div>
          <div class="crit-formula"><code>score = Wh / 100</code></div>
          <p class="crit-desc">Chuẩn hoá theo dung lượng pin thực tế (Wh), khớp giới hạn an toàn hàng không.</p>
        </article>

        <article class="crit-card crit-storage">
          <div class="crit-head">
            <div class="crit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5.5" rx="8" ry="2.5"/><path d="M4 5.5 v6 a8 2.5 0 0 0 16 0 v-6"/><path d="M4 11.5 v6 a8 2.5 0 0 0 16 0 v-6"/></svg></div>
            <h3 class="crit-title">Storage</h3>
            <span class="crit-badge">Thông số NSX</span>
          </div>
          <div class="crit-formula"><code>score = f(loại ổ, dung lượng)</code></div>
          <p class="crit-desc">NVMe Gen4/5 được cộng điểm ưu tiên so với SATA SSD ở cùng dung lượng.</p>
        </article>

      </div>
      <div class="crit-total">
        <span class="crit-total-label">Công thức tổng</span>
        <p class="crit-total-formula">Điểm cuối = Σ (<span class="tk-term">tiêu chí</span> × <span class="tk-weight">trọng số ngành</span>) × <span class="tk-value">valueFactor</span></p>
      </div>
    </div><!-- /pane-criteria -->

  </div>
</div>

<div class="notice" style="background:linear-gradient(135deg,rgba(52,211,153,.1),rgba(34,211,238,.08));border-color:rgba(52,211,153,.4)">
  <div class="ico">✨</div>
  <div><b style="color:var(--green)">Dữ liệu xác thực v2.8 (17/08/2026)</b> — Toàn bộ dữ liệu giá và tồn kho PDP từ <b>13 đại lý</b> (bao gồm GearVN) đã được đồng bộ & kiểm tra độ chính xác phần cứng 100%.</div>
</div>

<div class="hero">
<div class="hero-card"><div class="label">Tổng máy khảo sát</div><div class="big">__TOTAL__</div><div class="sub2">máy mới, đã lọc cũ/likenew</div></div>
<div class="hero-card"><div class="label">Số shop</div><div class="big">__SHOPS_COUNT__</div><div class="sub2">giá niêm yết hiện tại</div></div>
<div class="hero-card"><div class="label">Phân khúc giá</div><div class="big">__SEGS_COUNT__</div><div class="sub2">từ dưới 10tr đến 40tr+</div></div>
<div class="hero-card"><div class="label">Chuyên ngành</div><div class="big">__PROFS_COUNT__</div><div class="sub2">AI, CNTT, ĐH, VP, Game, CAD</div></div>
</div>

<div class="controls">
<div class="row"><div class="row-label">💰 Phân khúc:</div><div class="chips-group">__SEGCHIPS__</div></div>
<div class="row"><div class="row-label">🎓 Chuyên ngành:</div><div class="chips-group">__PROFCHIPS__</div></div>
</div>

<div class="search-row">
  <input type="text" id="search-box" class="search-box" placeholder="🔍 Tìm nhanh theo tên máy, chip CPU, RAM, GPU, SSD, tên Shop..." oninput="filterSearch(this.value)" autocomplete="off">
  <button class="clear-search" id="clear-search-btn" onclick="clearSearch()" style="display:none" title="Xóa tìm kiếm">✕</button>
</div>

<div class="row" style="margin-top:4px">
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
let customWeights = null, hideOOS = false, searchKw = '';

function escHtml(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function fmtPrice(p){return (p/1e6).toFixed(1).replace('.',',')+'tr';}
function badge(k){if(k==='CÒN')return '<span class="badge badge-green">● Còn hàng</span>';if(k==='HẾT')return '<span class="badge badge-red">✕ Hết hàng</span>';if(k==='LIÊN HỆ')return '<span class="badge badge-gold">✆ Liên hệ</span>';return '<span class="badge badge-gray">? Kiểm tra</span>';}
function spec(r){
  const p=[];
  if(r.c) p.push('CPU: '+escHtml(r.c));
  const ramStr = r.r || (r.i && r.i[5] ? r.i[5]+'GB' : '');
  if(ramStr) p.push('RAM: '+escHtml(ramStr));
  const ssdStr = r.t || (r.i && r.i[4] ? r.i[4]+'GB' : '');
  if(ssdStr) p.push('SSD: '+escHtml(ssdStr));
  if(r.d) p.push('Màn: '+escHtml(r.d));
  if(r.g) p.push('GPU: '+escHtml(r.g));
  return p.join(' • ');
}
function estBadge(r){return r.e ? '<span class="badge badge-gray" title="CPU không nhận diện được — điểm ước tính">≈ ước tính</span> ' : '';}
function currentWeights(){return customWeights || PROFS[curProf].w;}
// Trọng số nội bộ màn hình theo ngành [PPI, Hz, Panel] (Claude review)
const DISP_W = {
  "AI / Data Science": [0.50,0.15,0.35],
  "Lập trình / CNTT": [0.55,0.10,0.35],
  "Đồ họa / Thiết kế": [0.30,0.20,0.50],
  "Kinh tế / Văn phòng": [0.55,0.10,0.35],
  "Game / Đa phương tiện": [0.25,0.50,0.25],
  "Cơ khí / Kỹ thuật (CAD)": [0.50,0.15,0.35],
};
function dispScore(r, prof){
  const dp = r.dp || [r.i && r.i[1] ? r.i[1] : 50, 0, (r.i && r.i[2] ? 100 : 70)];
  const w = DISP_W[prof] || [0.45, 0.30, 0.25];
  return dp[0]*w[0] + dp[1]*w[1] + dp[2]*w[2];
}
function computeScore(r, w, prof){const parts=r.q.slice();parts[3]=dispScore(r, prof||curProf);let t=0;for(let i=0;i<6;i++)t+=(parts[i]||0)*(w[WKEYS[i]]||0);return t;}
function valueFactorFor(price, seg){const center=(seg.lo+seg.hi)/2;const dist=Math.abs(price-center)/((seg.hi-seg.lo)/2);const raw=1.0+(price>center? -dist*0.15 : dist*0.15);return Math.min(1.15,Math.max(0.85,raw));}

let currentModalItemIdx = -1;
function showDetail(r){
  currentModalItemIdx = ITEMS.indexOf(r);
  const w = currentWeights();
  const dScore = dispScore(r, curProf);
  const parts = r.q.slice();
  parts[3] = dScore;

  const ramStr = r.r || (r.i && r.i[5] ? r.i[5]+'GB' : '—');
  const ssdStr = r.t || (r.i && r.i[4] ? r.i[4]+'GB' : '—');
  const dispStr = r.d || ((r.i && r.i[0] ? r.i[0]+'" ' : '') + 'Full HD');
  const batStr = r.i && r.i[3] ? r.i[3]+'Wh' : 'Chưa rõ';
  const detVals = [escHtml(r.c||'—'), escHtml(ramStr), escHtml(r.g||'—'), escHtml(dispStr), escHtml(batStr), escHtml(ssdStr)];
  let rows = '';
  for(let i=0;i<6;i++){
    const sc = parts[i]||0, wt = w[WKEYS[i]]||0;
    const pct = (sc*wt).toFixed(1);
    rows += `<tr><td style="white-space:nowrap;font-weight:600">${KNAMES[i]}</td><td style="text-align:center">${Math.round(wt*100)}%</td><td style="text-align:center">${sc.toFixed(0)}/100</td><td style="text-align:center;color:var(--accent2);font-weight:700">${pct}</td><td class="col-bar"><div style="background:var(--card2);border-radius:4px;height:8px"><div style="background:linear-gradient(90deg,var(--accent),var(--accent2));height:8px;border-radius:4px;width:${Math.round(Math.min(100, Math.max(0, sc)))}%"></div></div></td><td style="font-size:.72rem;color:var(--muted)">${detVals[i]}</td></tr>`;
  }
  const seg = SEGS.find(s=>s.id===curSeg);
  const vf = valueFactorFor(r.p, seg);
  const hw = computeScore(r,w,curProf);
  const score = hw * vf;
  const estNote = r.e ? '<div style="color:var(--gold);font-size:.75rem;margin-top:4px">⚠️ CPU không nhận diện được — điểm CPU là ước tính (60/100)</div>' : '';
  const safeUrl = encodeURI(r.u||'');
  document.getElementById('modal-body').innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:14px">
      <div><div style="font-weight:700;font-size:1.05rem;line-height:1.4">${estBadge(r)}${escHtml(r.n)}</div>
      <div style="color:var(--muted);font-size:.82rem;margin-top:4px"><span class="price">${fmtPrice(r.p)}</span> • <b>${escHtml(SHOPL[r.s]||r.s)}</b> • ${badge(r.k)}</div>${estNote}</div>
      <div class="modal-score-box" style="text-align:center;background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:8px 12px"><div style="font-size:1.6rem;font-weight:800;color:var(--accent2);line-height:1.1">${score.toFixed(1)}</div><div style="font-size:.65rem;color:var(--muted);font-weight:600">ĐIỂM GIÁ TRỊ</div><div style="font-size:.92rem;font-weight:700;color:var(--gold);margin-top:4px">${hw.toFixed(1)}</div><div style="font-size:.6rem;color:var(--muted)">phần cứng</div></div>
    </div>
    <div style="color:var(--muted);font-size:.78rem;margin-bottom:12px;line-height:1.7;background:rgba(79,140,255,.05);border:1px solid var(--border);border-radius:10px;padding:10px 12px">Ngành <b style="color:var(--accent2)">${escHtml(curProf)}</b> — Điểm phần cứng: <b style="color:var(--accent2)">${hw.toFixed(1)}</b> • Hệ số giá trị phân khúc ${seg.emoji}: <b style="color:var(--accent2)">${vf.toFixed(2)}</b> (chặn 0.85–1.15)<br>➜ <b style="color:var(--accent2);font-size:.85rem">${score.toFixed(1)}</b> điểm xếp hạng</div>
    <div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table class="modal-table"><thead><tr><th>Tiêu chí</th><th style="text-align:center">Trọng số</th><th style="text-align:center">Điểm</th><th style="text-align:center">Đóng góp</th><th class="col-bar" style="width:25%">Thang điểm</th><th>Cấu hình</th></tr></thead><tbody>${rows}</tbody></table></div>
    <div style="margin-top:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:gap:10px"><button class="report-modal-btn" onclick="openReportForItem(currentModalItemIdx)">🚩 Báo sai thông tin máy này</button><a class="view-btn" href="${safeUrl}" target="_blank" rel="noopener" style="padding:7px 18px;font-size:.82rem">Xem trên website ${escHtml(SHOPL[r.s]||r.s)} ↗</a></div>`;
  document.getElementById('modal').style.display = 'flex';
}
function closeModal(){document.getElementById('modal').style.display='none';}
function openLog(){
  updateReportsCountBadge();
  document.getElementById('log-modal').classList.add('open');
}
function closeLog(){document.getElementById('log-modal').classList.remove('open');}
function switchLogTab(btn){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.remove('active'));
  document.getElementById('pane-'+btn.dataset.tab).classList.add('active');
}
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeModal();closeLog();}});
function filterSearch(val){
  searchKw = val.trim().toLowerCase();
  document.getElementById('clear-search-btn').style.display = searchKw ? 'flex' : 'none';
  render();
}
function clearSearch(){
  const inp = document.getElementById('search-box');
  if(inp){ inp.value = ''; filterSearch(''); }
}
function toggleOOS(){hideOOS=!hideOOS;document.getElementById('oos-toggle').classList.toggle('active',hideOOS);render();}
function selectSeg(el){curSeg=el.dataset.seg;document.querySelectorAll('.chip[data-seg]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function selectProf(el){curProf=el.dataset.prof;customWeights=null;document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));el.classList.add('active');render();}
function toggleSort(){sortMode = sortMode==='hw' ? 'value' : 'hw';render();}
let sortMode = 'value'; // 'value' | 'hw'
function render(){
  const seg = SEGS.find(s=>s.id===curSeg);
  const w = currentWeights();
  let inBand = ITEMS.filter(x=>x.p>=seg.lo&&x.p<seg.hi);
  if(hideOOS) inBand = inBand.filter(x=>x.k!=='HẾT');
  if(searchKw) inBand = inBand.filter(x=> (x.n+' '+x.c+' '+x.r+' '+x.t+' '+x.g+' '+(SHOPL[x.s]||x.s)).toLowerCase().includes(searchKw));
  const scored = inBand.map(r=>({r, hw: computeScore(r,w,curProf), vf: valueFactorFor(r.p,seg)})).map(x=>({...x, s:x.hw*x.vf}));
  scored.sort((a,b)=> sortMode==='hw' ? b.hw-a.hw : b.s-a.s);
  
  let rows = scored.map((item,i)=>{
    const r = item.r, oos = r.k==='HẾT'?' class="oos-row"':'';
    const vfBadge = item.vf > 1.08 ? '<span class="vf-badge vf-up" title="Giá thấp hơn phần cứng — đáng mua">▲</span>' : (item.vf < 0.92 ? '<span class="vf-badge vf-down" title="Giá cao hơn phần cứng">▼</span>' : '');
    const itemIdx = ITEMS.indexOf(r);
    return `<tr${oos} onclick="showDetail(ITEMS[${itemIdx}])"><td class="rank ${i===0?'rank-1':''} col-rank">${i+1}</td><td><div class="name">${estBadge(r)}${escHtml(r.n.slice(0,85))}</div><div class="spec">${spec(r)}</div></td><td class="price col-price">${fmtPrice(r.p)}</td><td class="col-stock">${badge(r.k)}</td><td class="score col-score"><span class="score-box"><span class="score-val">${item.s.toFixed(1)}</span> ${vfBadge}<button class="score-detail-btn" onclick="event.stopPropagation();showDetail(ITEMS[${itemIdx}])" title="Xem chi tiết cách tính điểm" aria-label="Chi tiết điểm">ⓘ</button></span></td><td class="col-shop"><span class="shop">${escHtml(SHOPL[r.s]||r.s)}</span><br><div style="display:flex;align-items:center;gap:3px"><a class="view-btn" href="${encodeURI(r.u||'')}" target="_blank" rel="noopener" onclick="event.stopPropagation()">Xem</a><button class="report-row-btn" onclick="event.stopPropagation();openReportForItem(${itemIdx})" title="Báo sai giá hoặc thông số máy này" aria-label="Báo sai">🚩</button></div></td></tr>`;
  }).join('');

  if(!rows){
    rows = `<tr><td colspan="6" style="text-align:center;padding:36px 16px;color:var(--muted);font-size:.9rem">🔍 Không tìm thấy máy nào phù hợp${searchKw?' với từ khóa "'+escHtml(searchKw)+'"':''} trong phân khúc này.<br><span style="font-size:.78rem;opacity:.8;display:inline-block;margin-top:6px">Thử tìm từ khóa khác, tắt "Ẩn máy hết hàng", hoặc chọn phân khúc giá khác.</span></td></tr>`;
  }

  const mode = customWeights ? '🎛️ trọng số tự chỉnh' : `ngành <b style="color:var(--accent2)">${escHtml(curProf)}</b>`;
  const oosInfo = hideOOS ? ' (đã ẩn máy hết hàng)' : '';
  const searchInfo = searchKw ? ` (lọc theo "${escHtml(searchKw)}")` : '';
  const header = `<div class="table-header-info"><div class="thi-left">Phân khúc <b style="color:var(--accent2)">${seg.emoji} ${seg.label}</b> — <b style="color:var(--accent2)">${scored.length}</b> máy • ${mode}${oosInfo}${searchInfo}</div><div class="thi-right"><span class="thi-hint">bấm ⓘ hoặc bấm hàng xem giải thích • <span class="vf-up" style="color:var(--green)">▲</span> giá hời · <span class="vf-down" style="color:var(--red)">▼</span> giá cao hơn phần cứng</span><button class="sort-toggle ${sortMode==='hw'?'active':''}" onclick="toggleSort()">${sortMode==='hw'?'Sort: phần cứng':'Sort: giá trị'}</button></div></div>`;
  const swipeHint = `<div class="swipe-hint">👆 Vuốt ngang xem hết bảng • Bấm vào hàng hoặc nút ⓘ để xem chi tiết điểm</div>`;
  const table = `<div class="table-scroll-wrap"><table class="report-table"><thead><tr><th class="col-rank">#</th><th>Sản phẩm</th><th class="col-price">Giá</th><th class="col-stock">Hàng</th><th class="col-score">Điểm</th><th class="col-shop">Shop</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  document.getElementById('table-container').innerHTML = header + swipeHint + table;
}
// custom weights
const CRITERIA = [['cpu','CPU'],['ram','RAM'],['gpu','GPU'],['display','Màn hình'],['battery','Pin'],['storage','Ổ cứng']];
function togglePanel(){const b=document.getElementById('cp-body');b.classList.toggle('open');document.getElementById('cp-arrow').innerText=b.classList.contains('open')?'▴':'▾';if(b.classList.contains('open')&&!document.getElementById('cp-sliders').children.length)buildSliders();}
function buildSliders(){const w=currentWeights();let vals=CRITERIA.map(([k])=>Math.round(w[k]*100));const diff=100-vals.reduce((a,b)=>a+b,0);if(diff!==0){let mx=0;for(let i=1;i<vals.length;i++)if(vals[i]>vals[mx])mx=i;vals[mx]+=diff;}document.getElementById('cp-sliders').innerHTML=CRITERIA.map(([k,l],i)=>`<div class="cp-slider"><label>${l}</label><input type="range" min="0" max="100" step="1" value="${vals[i]}" data-key="${k}" oninput="this.parentElement.querySelector('.val').innerText=this.value+'%';updateTotal()"><span class="val">${vals[i]}%</span></div>`).join('');updateTotal();}
function updateTotal(){const t=Array.from(document.querySelectorAll('#cp-sliders input')).reduce((s,i)=>s+parseInt(i.value),0);document.getElementById('cp-total-val').innerText=t+'%';document.getElementById('cp-total-warn').style.display=t===100?'none':'inline';}
function useProfile(p){curProf=p;document.querySelectorAll('.chip[data-prof]').forEach(c=>c.classList.remove('active'));const ch=document.querySelector(`.chip[data-prof="${p}"]`);if(ch)ch.classList.add('active');customWeights=null;buildSliders();render();}
function resetCustom(){useProfile(curProf);}
function applyCustom(){const w={};let t=0;Array.from(document.querySelectorAll('#cp-sliders input')).forEach(i=>{w[i.dataset.key]=parseInt(i.value)/100;t+=parseInt(i.value);});if(t!==100){alert('Tổng trọng số phải = 100%! Hiện: '+t+'%');return;}customWeights=w;render();}
// watch list
document.getElementById('table-container');
document.querySelectorAll('.chip[data-seg]')[3].classList.add('active');
document.querySelectorAll('.chip[data-prof]')[0].classList.add('active');
render();

/* ── Gamification, Reporting & Confetti Engine ── */
let currentReportItem = null;

function getContributorData(){
  const xp = parseInt(localStorage.getItem('lrvn_xp') || '0');
  const name = localStorage.getItem('lrvn_name') || 'Bạn';
  let rank = '🥉 Bug Scout';
  if(xp >= 300) rank = '👑 Tech Legend';
  else if(xp >= 150) rank = '🥇 Benchmark Master';
  else if(xp >= 50) rank = '🥈 Spec Inspector';
  return { xp, name, rank };
}

function updateHeaderBadge(){
  const data = getContributorData();
  const el = document.getElementById('user-badge-header');
  if(el){
    el.innerHTML = `🎖️ ${escHtml(data.rank)} • <b style="color:var(--gold)">${data.xp} XP</b>`;
  }
}

function showToast(msg, icon='✨'){
  const box = document.getElementById('toast-box');
  if(!box) return;
  const item = document.createElement('div');
  item.className = 'toast-item';
  item.innerHTML = `<span style="font-size:1.2rem">${icon}</span> <span>${msg}</span>`;
  box.appendChild(item);
  setTimeout(()=>{
    item.style.opacity = '0';
    item.style.transform = 'translateY(-10px)';
    item.style.transition = 'all .3s ease';
    setTimeout(()=>item.remove(), 300);
  }, 3500);
}

function openFeedbackModal(itemIdx=null){
  closeModal();
  closeLog();
  const modal = document.getElementById('feedback-modal');
  modal.style.display = 'flex';
  
  if(itemIdx !== null && ITEMS[itemIdx]){
    currentReportItem = ITEMS[itemIdx];
    document.getElementById('fb-device-name').innerText = currentReportItem.n;
    document.getElementById('fb-device-sub').innerText = `${SHOPL[currentReportItem.s]||currentReportItem.s} • ${fmtPrice(currentReportItem.p)} • ${currentReportItem.c} • ${currentReportItem.r||'8GB'}`;
    switchFeedbackTab('device');
  } else if(currentReportItem){
    document.getElementById('fb-device-name').innerText = currentReportItem.n;
    document.getElementById('fb-device-sub').innerText = `${SHOPL[currentReportItem.s]||currentReportItem.s} • ${fmtPrice(currentReportItem.p)}`;
  } else {
    document.getElementById('fb-device-name').innerText = 'Tất cả sản phẩm (Báo cáo chung)';
    document.getElementById('fb-device-sub').innerText = 'Góp ý hoặc báo lỗi không gắn riêng với một máy cụ thể';
  }

  const savedName = localStorage.getItem('lrvn_name') || '';
  if(savedName){
    const n1 = document.getElementById('fb-contributor-name');
    const n2 = document.getElementById('fb-feat-name');
    if(n1 && !n1.value) n1.value = savedName;
    if(n2 && !n2.value) n2.value = savedName;
  }
}

function closeFeedbackModal(){
  document.getElementById('feedback-modal').style.display = 'none';
}

function openReportForItem(itemIdx){
  openFeedbackModal(itemIdx);
}

function switchFeedbackTab(tab){
  document.querySelectorAll('.fb-tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelector(`.fb-tab-btn[data-tab="${tab}"]`).classList.add('active');
  document.querySelectorAll('.fb-pane').forEach(p=>p.classList.remove('active'));
  document.getElementById(`fb-pane-${tab}`).classList.add('active');
}

function selectFeedbackChip(el, group){
  const container = document.getElementById(`${group==='device'?'device-issue':'feature'}-chips`);
  container.querySelectorAll('.chip-pill').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}

function submitFeedback(type){
  let desc = '', name = '', topic = '', code = 'LRVN-' + Math.floor(10000 + Math.random() * 90000);
  if(type === 'device'){
    desc = document.getElementById('fb-device-desc').value.trim();
    name = document.getElementById('fb-contributor-name').value.trim() || 'Người dùng ẩn danh';
    const activeChip = document.querySelector('#device-issue-chips .chip-pill.active');
    topic = activeChip ? activeChip.innerText : 'Lỗi dữ liệu máy';
  } else {
    desc = document.getElementById('fb-feat-desc').value.trim();
    name = document.getElementById('fb-feat-name').value.trim() || 'Người dùng ẩn danh';
    const activeChip = document.querySelector('#feature-chips .chip-pill.active');
    topic = activeChip ? activeChip.innerText : 'Đề xuất tính năng';
  }

  if(!desc){
    alert('Vui lòng nhập mô tả hoặc thông tin bạn muốn đóng góp nhé!');
    return;
  }

  // Save to LocalStorage
  localStorage.setItem('lrvn_name', name);
  let curXp = parseInt(localStorage.getItem('lrvn_xp') || '0');
  curXp += 50;
  localStorage.setItem('lrvn_xp', curXp.toString());

  // Build full structured payload
  const payload = {
    code: code,
    type: type === 'device' ? 'Báo lỗi máy' : 'Đề xuất tính năng',
    topic: topic,
    name: name,
    deviceName: (type === 'device' && currentReportItem) ? currentReportItem.n : '',
    shop: (type === 'device' && currentReportItem) ? (SHOPL[currentReportItem.s] || currentReportItem.s) : '',
    price: (type === 'device' && currentReportItem) ? fmtPrice(currentReportItem.p) : '',
    url: (type === 'device' && currentReportItem) ? currentReportItem.u : '',
    desc: desc,
    evidence: type === 'device' ? (document.getElementById('fb-device-link')?.value || '') : '',
    time: new Date().toLocaleString('vi-VN')
  };

  // Save history to LocalStorage
  const history = JSON.parse(localStorage.getItem('lrvn_reports') || '[]');
  history.push(payload);
  localStorage.setItem('lrvn_reports', JSON.stringify(history));

  // Gửi tự động về Google Sheets Webhook (nếu có cấu hình)
  const GSHEETS_WEBHOOK_URL = window.LRVN_GSHEETS_URL || localStorage.getItem('lrvn_gsheets_url') || "";
  if(GSHEETS_WEBHOOK_URL){
    try {
      fetch(GSHEETS_WEBHOOK_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
    } catch(e){ console.warn('GSheets note:', e); }
  }

  updateHeaderBadge();
  closeFeedbackModal();

  // Trigger Confetti & Reward Modal
  confettiBurst();
  openRewardModal(true, name, code, curXp);
  showToast(`🎉 Cảm ơn ${name}! Đã ghi nhận báo cáo (+50 XP)`, '🎆');

  // Reset form
  if(document.getElementById('fb-device-desc')) document.getElementById('fb-device-desc').value = '';
  if(document.getElementById('fb-feat-desc')) document.getElementById('fb-feat-desc').value = '';
}

function copyFeedbackReport(type){
  let text = '';
  if(type === 'device'){
    const dName = currentReportItem ? currentReportItem.n : 'Báo cáo chung';
    const dShop = currentReportItem ? (SHOPL[currentReportItem.s]||currentReportItem.s) : 'N/A';
    const dUrl = currentReportItem ? currentReportItem.u : '';
    const activeChip = document.querySelector('#device-issue-chips .chip-pill.active')?.innerText || 'Lỗi thông số';
    const desc = document.getElementById('fb-device-desc').value || '(Chưa nhập)';
    text = `[BÁO LỖI LAPTOP REPORT VN]\n- Máy: ${dName}\n- Shop: ${dShop}\n- Link: ${dUrl}\n- Loại lỗi: ${activeChip}\n- Mô tả đúng: ${desc}`;
  } else {
    const activeChip = document.querySelector('#feature-chips .chip-pill.active')?.innerText || 'Góp ý';
    const title = document.getElementById('fb-feat-title').value || '(Không tiêu đề)';
    const desc = document.getElementById('fb-feat-desc').value || '(Chưa nhập)';
    text = `[GÓP Ý TÍNH NĂNG LAPTOP REPORT VN]\n- Chủ đề: ${activeChip}\n- Tiêu đề: ${title}\n- Chi tiết: ${desc}`;
  }
  navigator.clipboard.writeText(text).then(()=>{
    showToast('Đã sao chép nội dung báo cáo vào clipboard! 📋', '✅');
  }).catch(()=>alert('Đã tạo nội dung! Hãy copy thủ công.'));
}

function openRewardModal(isNew=false, name=null, code=null, xp=null){
  const data = getContributorData();
  const finalName = name || data.name || 'Nhà Đóng Góp';
  const finalXp = xp !== null ? xp : data.xp;
  const finalCode = code || ('LRVN-' + Math.floor(10000 + Math.random()*90000));
  
  document.getElementById('reward-card-name').innerText = finalName;
  document.getElementById('reward-card-rank').innerText = data.rank;
  document.getElementById('reward-card-xp').innerText = `${finalXp} XP`;
  document.getElementById('reward-card-code').innerText = `#${finalCode}`;
  document.getElementById('reward-modal').style.display = 'flex';
  if(isNew) confettiBurst();
}

function closeRewardModal(){
  document.getElementById('reward-modal').style.display = 'none';
}

/* ── Confetti Particle Explosion Engine ── */
function confettiBurst(){
  const canvas = document.getElementById('confetti-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  const colors = ['#22d3ee', '#4f8cff', '#fbbf24', '#34d399', '#f43f5e', '#a78bfa', '#f59e0b'];
  const particles = [];
  const count = 90;
  
  for(let i=0; i<count; i++){
    particles.push({
      x: canvas.width / 2 + (Math.random() - 0.5) * 200,
      y: canvas.height / 2 - 50 + (Math.random() - 0.5) * 100,
      w: Math.random() * 10 + 6,
      h: Math.random() * 6 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      vx: (Math.random() - 0.5) * 16,
      vy: (Math.random() - 0.8) * 16 - 4,
      rot: Math.random() * 360,
      vrot: (Math.random() - 0.5) * 12,
      opacity: 1,
      gravity: 0.35
    });
  }

  let startTime = Date.now();
  function loop(){
    const elapsed = Date.now() - startTime;
    if(elapsed > 3200){
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(let p of particles){
      p.x += p.vx;
      p.y += p.vy;
      p.vy += p.gravity;
      p.rot += p.vrot;
      p.opacity = Math.max(0, 1 - elapsed / 3000);
      
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot * Math.PI / 180);
      ctx.globalAlpha = p.opacity;
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
      ctx.restore();
    }
    requestAnimationFrame(loop);
  }
  loop();
}

// Reports Admin, Status Tracker & CSV Exporter
const STATUS_CONFIG = {
  'received': { label: '🕒 Đã tiếp nhận', cls: 'status-received', next: 'fixing', tip: 'Vừa nhận báo cáo' },
  'fixing': { label: '⚙️ Đang xử lý', cls: 'status-fixing', next: 'fixed', tip: 'Đang kiểm tra & sửa lỗi' },
  'fixed': { label: '✅ Đã fix', cls: 'status-fixed', next: 'noted', tip: 'Đã sửa xong trong dataset' },
  'noted': { label: '💡 Đã ghi nhận', cls: 'status-noted', next: 'rejected', tip: 'Đã thêm vào lộ trình tính năng' },
  'rejected': { label: '❌ Đóng', cls: 'status-rejected', next: 'received', tip: 'Không trùng khớp hoặc đã đóng' }
};

function cycleReportStatus(code){
  const history = JSON.parse(localStorage.getItem('lrvn_reports') || '[]');
  const item = history.find(r => r.code === code);
  if(!item) return;

  const curStatus = item.status || 'received';
  const nextStatus = STATUS_CONFIG[curStatus]?.next || 'received';
  item.status = nextStatus;

  localStorage.setItem('lrvn_reports', JSON.stringify(history));
  renderReportsList();
  showToast(`Đã đổi #${code} -> ${STATUS_CONFIG[nextStatus].label}`, '🔄');
}

function updateReportsCountBadge(){
  const history = JSON.parse(localStorage.getItem('lrvn_reports') || '[]');
  const countBadge = document.getElementById('reports-count-badge');
  if(countBadge) countBadge.innerText = history.length;
}

function renderReportsList(){
  updateReportsCountBadge();
  const history = JSON.parse(localStorage.getItem('lrvn_reports') || '[]');
  const container = document.getElementById('reports-list-container');
  if(!container) return;

  if(history.length === 0){
    container.innerHTML = '<div style="text-align:center;padding:36px;color:var(--muted);background:var(--card2);border-radius:10px;border:1px dashed var(--border)">Chưa có báo cáo nào được ghi nhận. Khi bạn hoặc người dùng gửi báo cáo lỗi/góp ý, toàn bộ danh sách sẽ hiển thị và lưu trữ tại đây!</div>';
    return;
  }

  let html = `<div class="reports-table-wrap"><table class="reports-table">
    <thead>
      <tr>
        <th style="width:95px">Mã</th>
        <th style="width:115px;text-align:center">Tình Trạng</th>
        <th style="width:130px">Thời Gian</th>
        <th style="width:140px">Loại / Chủ Đề</th>
        <th style="width:110px">Người Gửi</th>
        <th style="width:220px">Tên Máy / Shop</th>
        <th>Nội Dung Báo Cáo</th>
      </tr>
    </thead>
    <tbody>`;

  history.slice().reverse().forEach(r => {
    const isDevice = r.type === 'device' || r.type === 'Báo lỗi máy';
    const typeBadge = isDevice 
      ? '<span style="display:inline-block;padding:2px 8px;border-radius:10px;background:rgba(248,113,113,.15);border:1px solid rgba(248,113,113,.35);color:#f87171;font-weight:700;font-size:.72rem">🚩 Báo lỗi máy</span>'
      : '<span style="display:inline-block;padding:2px 8px;border-radius:10px;background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.35);color:#38bdf8;font-weight:700;font-size:.72rem">💡 Góp ý tính năng</span>';
    
    const stKey = r.status || 'received';
    const stConf = STATUS_CONFIG[stKey] || STATUS_CONFIG.received;
    const statusPill = `<span class="status-pill ${stConf.cls}" onclick="cycleReportStatus('${r.code}')" title="Nhấp để đổi trạng thái">${stConf.label}</span>`;

    let deviceCol = '<span style="color:var(--muted);font-style:italic">— (Góp ý chung)</span>';
    if(r.deviceName && r.deviceName !== 'N/A' && r.deviceName !== 'Tất cả sản phẩm (Báo cáo chung)'){
      const cleanName = r.deviceName.replace(/\s+/g, ' ').trim();
      deviceCol = `<div class="report-dev-name" title="${escHtml(cleanName)}">${escHtml(cleanName)}</div>`;
      if(r.shop && r.shop !== 'N/A'){
        deviceCol += `<div style="display:flex;align-items:center;gap:4px;margin-top:3px"><span class="shop-pill">[${escHtml(r.shop)}]</span>${r.price ? `<span style="color:var(--accent2);font-size:.7rem">${escHtml(r.price)}</span>` : ''}</div>`;
      }
    } else if(isDevice){
      deviceCol = '<span style="color:var(--muted);font-style:italic">— (Báo lỗi chung)</span>';
    }

    html += `<tr>
      <td style="font-family:monospace;color:var(--gold);white-space:nowrap;font-weight:700">${r.code || 'N/A'}</td>
      <td style="text-align:center">${statusPill}</td>
      <td style="color:var(--muted);white-space:nowrap;font-size:.75rem">${r.time || ''}</td>
      <td>${typeBadge}<div style="font-size:.72rem;color:var(--muted);margin-top:2px">${r.topic || ''}</div></td>
      <td style="color:var(--accent2);font-weight:600">${r.name || 'Người dùng ẩn danh'}</td>
      <td>${deviceCol}</td>
      <td style="line-height:1.45">${r.desc || ''}${r.evidence ? `<div style="margin-top:3px"><a href="${r.evidence}" target="_blank" style="color:var(--accent);font-size:.72rem">🔗 Dẫn chứng</a></div>` : ''}</td>
    </tr>`;
  });

  html += '</tbody></table></div>';
  container.innerHTML = html;
}

function exportReportsToCSV(){
  const history = JSON.parse(localStorage.getItem('lrvn_reports') || '[]');
  if(history.length === 0){
    alert('Chưa có báo cáo nào để xuất!');
    return;
  }

  let csv = '\\uFEFFMã,Tình Trạng,Thời Gian,Loại Báo Cáo,Chủ Đề,Người Gửi,Tên Máy,Đại Lý,Giá,Link PDP,Nội Dung,Dẫn Chứng\\n';
  history.forEach(r => {
    const stKey = r.status || 'received';
    const stLabel = STATUS_CONFIG[stKey]?.label || 'Đã tiếp nhận';
    const row = [
      r.code || '',
      `"${stLabel}"`,
      r.time || '',
      r.type || '',
      r.topic || '',
      `"${(r.name||'').replace(/"/g, '""')}"`,
      `"${(r.deviceName||'').replace(/"/g, '""')}"`,
      r.shop || '',
      r.price || '',
      r.url || '',
      `"${(r.desc||'').replace(/"/g, '""')}"`,
      r.evidence || ''
    ];
    csv += row.join(',') + '\\n';
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `Bao_Cao_Laptop_Report_VN_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast('Đã tải xuống file Excel (CSV) thành công! 📥', '📊');
}

function clearReportsHistory(){
  if(confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử báo cáo đã lưu?')){
    localStorage.removeItem('lrvn_reports');
    renderReportsList();
    showToast('Đã dọn sạch lịch sử báo cáo.', '🗑️');
  }
}

// Global ESC listener update
document.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    closeModal();
    closeLog();
    closeFeedbackModal();
    closeRewardModal();
  }
});

// Initialize Badges on page load
updateHeaderBadge();
updateReportsCountBadge();

</script>
</body></html>"""

# Segments chips
seg_chips = "".join(f'<div class="chip" data-seg="{s["id"]}" onclick="selectSeg(this)">{s["emoji"]} {s["label"]}</div>' for s in SEGMENTS)
prof_chips = "".join(f'<div class="chip" data-prof="{p}" onclick="selectProf(this)">{p}</div>' for p in profiles)

shops_found = sorted(list(set(r["s"] for r in items_c)))
shop_names_str = ", ".join(SHOP_LABEL.get(s, s.upper()) for s in shops_found)

update_logs_html = []
for entry in UPDATE_LOGS:
    tag = '<span class="date">bản mới nhất</span>' if entry.get("is_latest") else ""
    li_items = "".join(f"<li>{it}</li>" for it in entry["items"])
    update_logs_html.append(f"""    <div class="log-item">
      <div class="ver">{entry['ver']} — {entry['date']} {tag}</div>
      <ul>{li_items}</ul>
    </div>""")
update_logs_str = "\n".join(update_logs_html)
latest_ver = UPDATE_LOGS[0]["ver"]
latest_date = UPDATE_LOGS[0]["date"]

html = HTML
html = html.replace("__TOTAL__", str(len(items_c)))
html = html.replace("__SHOPS_COUNT__", str(len(shops_found)))
html = html.replace("__SHOP_NAMES__", shop_names_str)
html = html.replace("__SEGS_COUNT__", str(len(SEGMENTS)))
html = html.replace("__PROFS_COUNT__", str(len(profiles)))
html = html.replace("__UPDATED_DATE__", f"{latest_ver} — {latest_date}")
html = html.replace("__UPDATE_LOGS__", update_logs_str)
html = html.replace("__SEGCHIPS__", seg_chips)
html = html.replace("__PROFCHIPS__", prof_chips)
html = html.replace("__SEGS__", json.dumps([{k: s[k] for k in ("id","label","emoji","lo","hi")} for s in SEGMENTS], ensure_ascii=False))
html = html.replace("__PROFS__", json.dumps(profiles, ensure_ascii=False))
html = html.replace("__ITEMS__", json.dumps(items_c, ensure_ascii=False))
html = html.replace("__SHOPL__", json.dumps(SHOP_LABEL, ensure_ascii=False))

out_paths = [
    os.path.expanduser("~/laptop-report-19m/bao-cao-laptop-phan-khuc.html"),
    os.path.join(os.path.dirname(__file__), "bao-cao-laptop-phan-khuc.html"),
    os.path.join(os.path.dirname(__file__), "deploy", "index.html"),
    os.path.join(os.path.dirname(__file__), "index.html"),
]
for out in out_paths:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"saved: {out} ({os.path.getsize(out)/1024/1024:.2f} MB)")
