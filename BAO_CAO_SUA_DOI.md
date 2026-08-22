# 📋 BÁO CÁO SỬA ĐỔI & TIẾN TRÌNH KỸ THUẬT (BAO_CAO_SUA_DOI.md)

Tài liệu ghi nhận toàn bộ lịch sử chỉnh sửa, lý do kỹ thuật, kết quả kiểm thử và phân bổ trách nhiệm theo chuẩn quản lý tiến trình **Widget_Date**.

---

## 🚀 Phiên bản v2.11 — Khắc Phục Lỗi Nhận Diện Tồn Kho, Phục Hồi 110 Laptop Còn Hàng & Cập Nhật Parser Live (22/08/2026)

**Ngày:** 22/08/2026 • **Agents tham gia:** `orchestrator`, `crawler-specialist`, `data-reconciler`, `frontend-specialist`, `qa-test-engineer`, `devops-specialist` • **Trạng thái:** ✅ Đã hoàn tất, nghiệm thu 100% & Pre-commit 5/5 PASSED

### 1. Vấn đề Phát hiện & Nguyên nhân Kỹ thuật (Issues & Root Causes)
1. **Lỗi Thứ Tự Ưu Tiên Trong Parser Chuỗi Thô (Global Substring Matching Inversion):**
   - *Nguyên nhân:* Trong script xác thực cũ (`verify_stock.py`), điều kiện `if "hết hàng" in html` được kiểm tra trước `if "mua ngay" in html`.
   - Các sàn TMĐT (*CellphoneS, Hacom, LaptopGame, TGDD*) luôn có từ khóa *"hết hàng"* xuất hiện cố định tại Footer (chính sách đổi trả, box sản phẩm tương tự khi hết hàng). Do đó, script quét chuỗi toàn trang đã bắt nhầm từ khóa ở footer và đánh dấu sai thành `✕ Hết hàng` dù nút "MUA NGAY" và "THÊM VÀO GIỎ" vẫn đang hoạt động.
2. **Kho Hàng Đại Lý Vừa Nhập Lô Mới (Restock):**
   - Các dòng máy (*MacBook Neo, Lenovo LOQ, Asus Vivobook, HP 250R*) sau đợt hết hàng đã được shop nhập thêm hàng về kho nhưng dữ liệu cũ chưa được refresh.

### 2. Các Thay đổi Chi tiết Đã Thực Hiện (Detailed Modifications)
- **Tối Ưu & Sửa Triệt Để Bộ Parser Tồn Kho (`verify_stock.py`):**
   - Ưu tiên bóc tách theo thứ tự: JSON-LD `schema.org/InStock` / `OutOfStock` $\rightarrow$ Scoped Selector Nút Mua (`btn-buy`, `button__buy-now`, `btn-mua-ngay`, `MUA NGAY`) $\rightarrow$ Scoped OutOfStock (`btn-hethang`, `tạm hết hàng`).
- **Khôi Phục Trạng Thái Tồn Kho Cho 110 Máy (`_compact_data.json`):**
   - Phục hồi 55 máy từ CellphoneS, 35 máy từ Hacom, 18 máy từ LaptopGame và 2 máy từ TGDD về đúng trạng thái `● Còn hàng` (`k = "CÒN"`).
   - Tỷ lệ máy Còn hàng tăng lên **1.757 máy** (tăng +110 máy), số lượng máy Hết hàng thực tế giảm chuẩn xác về **19 máy**.
- **Đóng gói Compact HTML & Cập nhật In-App Changelog:**
   - Cập nhật Changelog v2.11 vào `build_compact.py`, build lại toàn bộ các artifact: `bao-cao-laptop-phan-khuc.html`, `deploy/index.html`, `index.html`.

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Results)
- ✅ **Unit Tests Scoring**: `python test_scoring.py` $\rightarrow$ **35/35 PASSED**.
- ✅ **Pre-commit Checklist**: `python .agent/scripts/checklist.py` $\rightarrow$ **5/5 PASSED**.
- ✅ **Live PDP Audit**: 100% 129 link sản phẩm được rà soát trực tiếp qua parser mới, bảo đảm tính xác thực cao.

---

## 🚀 Phiên bản v2.10 — Kiểm toán Toàn diện Thông số Màn hình, Sửa Lỗi Điểm 0/100 & Khôi phục 100% Thông số Phần cứng (17/08/2026)

**Ngày:** 17/08/2026 • **Agents tham gia:** `orchestrator`, `data-reconciler`, `scoring-architect`, `frontend-specialist`, `qa-test-engineer`, `devops-specialist` • **Trạng thái:** ✅ Đã hoàn tất, nghiệm thu 100% & Pre-commit 5/5 PASSED

### 1. Vấn đề Phát hiện & Nguyên nhân Kỹ thuật (Issues & Root Causes)
1. **Lỗi Điểm Màn hình 0/100 trong Modal Chi tiết (`showDetail`):**
   - *Nguyên nhân:* 1.602 máy trong dataset có trường `q[3]` lưu tĩnh là `0` do kỳ vọng tính động theo ngành; tuy nhiên hàm JS `showDetail()` lại đọc trực tiếp `sc = r.q[i]`, dẫn đến việc modal hiển thị `0/100` điểm và `0.0` đóng góp dù hàm tổng `computeScore()` vẫn tính điểm.
2. **Chuỗi hiển thị Màn hình bị rút gọn cụt lủn:**
   - *Nguyên nhân:* Modal chỉ in chuỗi thô `15.6" OLED=không` và bỏ qua hoàn toàn trường chi tiết độ phân giải, tần số quét và loại tấm nền.
3. **182 máy bị khuyết thông số Màn hình do lỗi bóc tách từ shop:**
   - *Nguyên nhân:* Selector HTML một số shop chỉ lấy kích thước (`15"`, `16"`) hoặc để trống trong khi tiêu đề chứa đầy đủ thông số FHD, 2K, 3K, 4K, 120Hz, 144Hz, IPS, OLED, Cảm ứng.
4. **Khuyết tên CPU (`r.c`) và GPU (`r.g`) trên 622 máy:**
   - *Nguyên nhân:* Thiếu parser fallback từ tiêu đề máy.

### 2. Các Thay đổi Chi tiết Đã Thực Hiện (Detailed Modifications)
- **Parser Thông Minh Chuẩn Hoá Màn Hình (`reconcile_display_and_specs.py`):**
  - Trích xuất kích thước, độ phân giải (FHD, WUXGA, 2.5K, 3K, 4K), tần số quét (60Hz–360Hz), tấm nền (OLED, Mini-LED, IPS, Cảm ứng) cho 100% 3.271 máy.
  - Chuẩn hoá mảng cấu phần `r.dp = [ppi, hz, panel]` và gán `q[3] = disp_s` chính xác.
- **Fallback CPU & GPU Từ Tiêu Đề:**
  - Nhận diện vi xử lý (Ryzen AI 300, Intel Core Ultra, Gen 13/14, Apple M) và Card rời/onboard (RTX 30/40/50, Arc, Radeon, Iris Xe), xóa bỏ hoàn toàn dấu gạch ngang `—`.
- **Đồng bộ Logic Hiển thị Modal (`showDetail` & `dispScore`):**
  - Đồng bộ điểm màn hình động theo ngành `dScore = dispScore(r, curProf)` trong bảng phân tích chi tiết.
  - Hiển thị đầy đủ mô tả `r.d` (ví dụ: `15.6" Full HD (1920x1080) • 144Hz IPS`).
- **Đóng gói Compact HTML & In-App Changelog:**
  - Cập nhật In-App Changelog v2.10, xuất xưởng các bản HTML độc lập 1.62 MB (`bao-cao-laptop-phan-khuc.html`, `deploy/index.html`, `index.html`).

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Results)
- ✅ **Unit Tests Scoring**: `python test_scoring.py` $\rightarrow$ **35/35 PASSED**.
- ✅ **Pre-commit Checklist**: `python .agent/scripts/checklist.py` $\rightarrow$ **5/5 PASSED**.
- ✅ **Dataset Integrity**: 0 máy có điểm màn hình = 0, 0 máy bị thiếu chuỗi màn hình.
- ✅ **Browser Subagent Test**: Xác minh thành công trên các model phản ánh (`A29T2UA`, `1411VN`) qua video recording `verify_display_fix_1786953106404.webp`.

---

## 🚀 Phiên bản v2.9 — Kiểm toán Toàn diện Link Sản phẩm 13 Shop, Sửa 100% Link Hỏng & Tích hợp Hệ thống Báo Lỗi / Gamification (17/08/2026)

**Ngày:** 17/08/2026 • **Agents tham gia:** `orchestrator`, `crawler-specialist`, `data-reconciler`, `frontend-specialist`, `qa-test-engineer`, `devops-specialist` • **Trạng thái:** ✅ Đã triển khai Production Vercel (`https://laptop-report-vn.vercel.app`) & Nghiệm thu 100%

### 1. Mục tiêu & Phạm vi Thực hiện (Objective & Scope)
1. **Kiểm toán & Sửa lỗi toàn bộ Link Sản phẩm (PDP) trên 13 đại lý:**
   - Quét mã phản hồi HTTP thực tế trên toàn bộ danh mục sản phẩm (13 shop).
   - Xóa bỏ hoàn toàn định dạng URL cũ (`.html` trên GearVN), chuyển đổi 100% sang định dạng Next.js App Router `/products/<slug>` theo sitemap chính hãng.
   - Sửa lỗi các ký tự đặc biệt (dấu ngoặc kép unicode `″`) trên No1Computer dẫn đến lỗi 404, bổ sung cơ chế fallback tìm kiếm thông minh khi sản phẩm hết hàng hoặc đổi link.
2. **Tích hợp Hệ thống Báo cáo Dữ liệu & Đóng góp Ý kiến Người dùng:**
   - Nút báo lỗi nhanh 1-chạm `🚩` trên từng hàng sản phẩm và trong modal chi tiết điểm (pre-filled sẵn 100% thông số).
   - Modal 2 Tab (`#feedback-modal`): Báo lỗi máy/giá sai và Đề xuất tính năng/giao diện UI/UX.
3. **Tích hợp Gamification Phần Thưởng & Hiệu ứng Animation:**
   - Hệ thống tích lũy điểm uy tín (+50 XP) và 4 cấp bậc huy hiệu (*Bug Scout, Spec Inspector, Benchmark Master, Tech Legend*).
   - Hiệu ứng Pháo hoa Canvas Confetti 60 FPS và Thẻ Chứng Nhận Đóng Góp Vàng (Holographic 3D Golden Card).
4. **Kiểm thử Responsive UI/UX Đa Thiết Bị:**
   - Kiểm tra hiển thị pixel-perfect trên Mobile (390x844), Tablet (768x1024) và Laptop (1366x768).

---

## 🚀 Phiên bản v2.8 — Cập nhật Dữ liệu GearVN, Khớp Chuẩn Benchmark Thế Hệ Mới & Mở rộng Dataset (17/08/2026)

**Ngày:** 17/08/2026 • **Agents tham gia:** `orchestrator`, `crawler-specialist`, `data-reconciler`, `scoring-architect`, `qa-test-engineer`, `devops-specialist` • **Trạng thái:** ✅ Đã hoàn tất & nghiệm thu 100%

### 1. Mục tiêu & Phạm vi Thực hiện (Objective & Scope)
1. **Thu thập dữ liệu thực tế từ 2 landing page chiến lược của GearVN:**
   - `https://gearvn.com/pages/laptop-van-phong`
   - `https://gearvn.com/pages/laptop-gaming`
2. **Trích xuất & Khử trùng lặp PDP (Product Detail Page):**
   - Thu thập 57 sản phẩm laptop duy nhất từ Next.js RSC stream và schema JSON-LD.
   - Bóc tách 100% thông số cấu hình chính hãng: CPU, GPU, RAM, Ổ cứng SSD, Màn hình (Kích thước, độ phân giải, Hz, Panel), Dung lượng Pin (Wh), Tình trạng tồn kho (Còn hàng / Hết hàng) và Giá niêm yết/khuyến mãi.
3. **Chuẩn hoá Thông số & Tính điểm Benchmark Chính xác Tuyệt đối (Zero-Guesswork):**
   - Mở rộng hỗ trợ chip thế hệ mới: AMD Ryzen AI 300/400 (`AI 9 465`, `AI 9 365`, `AI 7 350`), Intel Core Ultra 200V Lunar Lake (`Ultra 9 288V`, `Ultra 5 226V`), Intel Core Ultra 9 `275HX` / `386H`, Intel Core Series 1/2 (`Core 7 240H`, `Core 5 210H`, `Core 5 120U`, `Core 3 N350`), NVIDIA GeForce RTX 50 Mobile Series (`5050`, `5060`, `5070`, `5070 Ti`).
   - Khớp công thức chấm điểm đa ngành và hệ số giá trị phân khúc ($VF \in [0.85, 1.15]$).

### 2. Các Thay đổi Chi tiết Đã Thực Hiện (Detailed Modifications)
- **Crawler Chuyên dụng GearVN (`crawl_gearvn_landing.py`):**
  - Giải mã RSC stream Next.js, bóc tách cấu hình sạch từ JSON-LD schema, tự động chống nghẽn rate limit (delay 0.4s - 1.0s).
- **Bộ chuẩn hoá & Chấm điểm (`build_gearvn_scored.py`):**
  - Làm sạch ký tự đặc biệt (®, ™), map chính xác 100% chip CPU/GPU theo PassMark Benchmark thật.
- **Đồng bộ Cơ sở dữ liệu (`sync_gearvn_to_dataset.py`):**
  - Cập nhật 6 sản phẩm và bổ sung 51 sản phẩm mới vào `all_items.json` và `_ALL_scored.json`, nâng quy mô dataset toàn hệ thống lên **3.379 laptop**.
- **Đóng gói Báo cáo Single-File HTML (`build_compact.py`):**
  - Cập nhật In-App Changelog v2.8, xuất xưởng các bản HTML độc lập ~1.73 MB (`bao-cao-laptop-phan-khuc.html`, `deploy/index.html`, `index.html`).

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Results)
- ✅ **Unit Tests Scoring**: `python test_scoring.py` $\rightarrow$ **35/35 PASSED** (100% khớp Node.js runtime).
- ✅ **Pre-commit Checklist**: `python .agent/scripts/checklist.py` $\rightarrow$ **5/5 PASSED**.
- ✅ **Dataset Integrity**: Toàn bộ 3.379 máy đều thỏa mãn giới hạn $[0, 100]$, 0 dữ liệu rác, 0 secret leak.

---

## 🚀 Phiên bản v2.5 — Audit Toàn Diện, Tìm & Fix Triệt Để Bug Dữ Liệu & UI (16/08/2026)

**Ngày:** 16/08/2026 • **Agents tham gia:** `orchestrator`, `data-reconciler`, `scoring-architect`, `frontend-specialist`, `qa-test-engineer`, `security-auditor` • **Trạng thái:** ✅ Đã hoàn tất & nghiệm thu 100%

### 1. Vấn đề Phát hiện qua Deep Audit (Issues & Root Causes)
1. **Thiếu hiển thị Dung lượng SSD/RAM trong chuỗi tóm tắt bảng:** 
   - *Nguyên nhân:* 1.437 máy trong dataset cào ban đầu không có trường `storage` riêng biệt do shop nhúng dung lượng vào tiêu đề. Hàm `spec(r)` trong JS chỉ kiểm tra `r.t` (storage) và `r.r` (RAM), nếu chuỗi rỗng sẽ bỏ qua hiển thị ổ cứng/RAM trong dòng tóm tắt bảng dù mảng cấu hình số `r.i` (`r.i[4]`: SSD GB, `r.i[5]`: RAM GB) vẫn được trích xuất đầy đủ.
2. **Nguy cơ XSS & Lỗi vỡ HTML khi tên máy có ký tự đặc biệt:**
   - *Nguyên nhân:* Tên máy `r.n` và thông số linh kiện từ web shop chứa ký tự ngoặc kép `"` (ví dụ: `15.6"`), dấu `<` / `>` được render trực tiếp vào innerHTML mà chưa qua hàm escape.
3. **Giới hạn thanh trượt trọng số (Sliders max cap = 50%):**
   - *Nguyên nhân:* Input range slider trước đây đặt `max="50"`, ngăn cản người dùng chuyên sâu muốn dồn trọng số lên tới `60% – 100%` cho một tiêu chí duy nhất (ví dụ: chỉ ưu tiên GPU cho render 3D hoặc CPU cho biên dịch code).
4. **Thiếu công cụ Tìm kiếm nhanh (Instant Search Bar) & Xử lý Trạng thái Trống (Empty State):**
   - *Nguyên nhân:* Người dùng phải cuộn qua hàng trăm máy để tìm model mong muốn; khi bật bộ lọc hết hàng mà không có máy nào phù hợp thì bảng bị trống trơn không có thông báo hướng dẫn.
5. **Trải nghiệm phím ESC & An toàn URL:**
   - Cần hỗ trợ phím `Escape` để đóng nhanh các modal đang mở và mã hóa URL `encodeURI(r.u)` khi tạo link sang shop.

### 2. Các Thay đổi Chi tiết Đã Thực Hiện (Detailed Fixes)
- **Tự động Fallback Thông số Kỹ thuật (`spec(r)` & `showDetail(r)`):**
  - Cập nhật hàm `spec(r)` tự động trích xuất dung lượng RAM từ `r.i[5]` và SSD từ `r.i[4]` khi chuỗi văn bản bị thiếu. 100% 3.328 laptop hiển thị đầy đủ RAM và SSD.
- **Tích Hợp Thanh Tìm Kiếm Tức Thì (Instant Real-Time Search Bar):**
  - Bổ sung ô tìm kiếm `.search-box` với icon tìm kiếm và nút xóa nhanh `✕`. Lọc tức thì theo mọi trường: tên máy, CPU, RAM, GPU, SSD, tên shop.
  - Bổ sung Empty State thông minh với gợi ý cụ thể khi không tìm thấy kết quả phù hợp.
- **Mở rộng Thanh trượt Trọng số (Custom Sliders):**
  - Nâng giới hạn tối đa của slider từ `50%` lên `100%`, cho phép người dùng tự do cấu hình trọng số theo nhu cầu cá nhân.
- **Bảo mật XSS & An toàn Render HTML:**
  - Viết hàm chuẩn `escHtml(s)` để escape an toàn toàn bộ tên sản phẩm, thông số linh kiện, nhãn shop và tên ngành nghề trước khi đưa vào DOM.
  - Mã hóa an toàn `encodeURI(r.u)` cho các liên kết PDP cửa hàng.
- **Tiện ích Tương Tác & Trợ năng (Accessibility):**
  - Lắng nghe sự kiện bàn phím `Escape` đóng tức thì cả Modal Chi tiết Điểm (`#modal`) và Modal Nhật ký Cập nhật (`#log-modal`).

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Results)
- ✅ **Unit Tests Scoring**: `python test_scoring.py` $\rightarrow$ **35/35 PASSED** (100% khớp Node.js runtime).
- ✅ **Pre-commit Checklist**: `python .agent/scripts/checklist.py` $\rightarrow$ **5/5 PASSED**.
- ✅ **Browser Subagent Test**:
  - Test tìm kiếm hợp lệ (`MSI`): Lọc tức thì ra đúng 13 máy MSI trong phân khúc.
  - Test nút xóa tìm kiếm `✕`: Reset tức thì về danh sách toàn bộ 332 máy.
  - Test tìm kiếm không tồn tại (`xyznonexistent999`): Hiển thị thông báo Empty State rõ ràng, trực quan.
  - Test Modal Chi tiết: Toàn bộ thông số CPU, RAM, GPU, Màn hình, Pin, SSD hiển thị chuẩn xác 100%.
  - Test phím `Escape`: Đóng modal mượt mà.
  - Test Sliders: Kéo chỉnh tới 100% trơn tru.
  - Video nghiệm thu: `search_and_bugfix_test_1786818936401.webp`.

---

## 🚀 Phiên bản v2.4 — Sửa lỗi UI Mobile & Nút Chi tiết Score (16/08/2026)

**Ngày:** 16/08/2026 • **Agents tham gia:** `orchestrator`, `project-planner`, `frontend-specialist`, `qa-test-engineer`, `devops-specialist` • **Trạng thái:** ✅ Đã hoàn tất & build release

### 1. Vấn đề & Nguyên nhân (Problem & Root Cause)
- **Hiện tượng:** Khi xem trên điện thoại hoặc co nhỏ cửa sổ trình duyệt trên laptop ($\le 768\text{px}$), tất cả các nút `ⓘ` xem chi tiết điểm số trong bảng bị biến mất khỏi ô điểm.
- **Nguyên nhân kỹ thuật:** Class `.info-btn` bị gán trùng cho nút Hướng dẫn Header và từng nút `ⓘ` trong bảng điểm. Rule CSS `@media (max-width: 768px) { .info-btn { position: fixed; right: 14px; bottom: 14px; ... } }` đã biến toàn bộ các nút `ⓘ` trong hàng thành fixed button bay về góc dưới bên phải màn hình.

### 2. Các thay đổi chi tiết (Detailed Modifications)
- **Phân tách Class Name:**
  - Nút Hướng dẫn Header: đổi thành `.guide-btn`, chỉ riêng nút này có hiệu ứng FAB nổi ở góc phải khi cuộn trên mobile.
  - Nút Chi tiết Điểm: đổi thành `.score-detail-btn`, thiết kế badge tròn màu cyan nổi bật (`rgba(34,211,238,0.12)`), viền sáng subtle, cố định ngay cạnh điểm số trên mọi kích thước màn hình.
- **Tối ưu Bảng dữ liệu & DOM:**
  - Hợp nhất thành 1 container bảng dữ liệu duy nhất (`.table-scroll-wrap` + `.report-table`), loại bỏ việc sinh 2 bảng song song `desktop` và `mobile` trong JavaScript `render()`.
  - Hỗ trợ **Quick Tap**: Bấm vào bất kỳ đâu trên dòng sản phẩm để mở ngay modal chi tiết điểm.
  - Thêm `sticky header` cho thead khi cuộn dọc và chỉ dẫn vuốt ngang `swipe-hint` trên mobile.
- **Tối ưu Modal Chi tiết Điểm (`#modal-card`):**
  - Card điểm số 2 tầng: **Điểm Giá Trị** (xếp hạng) và **Điểm Phần Cứng**.
  - Bảng tiêu chí tự động ẩn cột thanh tiến trình trên màn hình hẹp ($\le 520\text{px}$) để giữ độ rõ nét cho các thông số linh kiện.
- **Khắc phục Đường viền Bảng Bị Lồi Lên (Stepped Borders):**
  - *Nguyên nhân:* Thuộc tính `display: flex` áp trực tiếp lên class `.score` của thẻ `<td>` khiến trình duyệt hủy chế độ `display: table-cell`. Ô điểm bị co chiều cao theo nội dung chữ (~24px) thay vì giãn bằng các ô khác (~50px), làm đường kẻ `border-bottom` bị giật lùi/lồi lên so với các ô bên cạnh.
  - *Giải pháp:* Đưa `<td>` về chuẩn `display: table-cell` và bọc nội dung điểm bên trong một thẻ `<span class="score-box">` với `display: inline-flex; align-items: center; gap: 4px; vertical-align: middle;`. Nhờ đó mọi ô trong hàng đều đồng nhất chiều cao, đường viền `border-bottom` phẳng và liền mạch 100%.
- **Tự Động Hóa Số Liệu Động (Dynamic Data Points):**
  - Tự động đếm động số máy (`__TOTAL__`), số shop (`__SHOPS_COUNT__`), danh sách shop (`__SHOP_NAMES__`), số phân khúc (`__SEGS_COUNT__`), số chuyên ngành (`__PROFS_COUNT__`) và ngày cập nhật (`__UPDATED_DATE__`).
  - Bổ sung nhật ký phiên bản v2.4 vào Modal Hướng dẫn (`#pane-updates`).
- **Đồng bộ Build Output:**
  - Cập nhật `build_compact.py` xuất đồng bộ ra cả `~/laptop-report-19m/bao-cao-laptop-phan-khuc.html`, `laptop-report-vn/bao-cao-laptop-phan-khuc.html` và `deploy/index.html`.

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Exit Gate)
- ✅ **Unit Tests Scoring**: `python test_scoring.py` $\rightarrow$ **35/35 passed** (100%).
- ✅ **Dataset Integrity**: 994 máy all_items, 3.353 máy scored hợp lệ.
- ✅ **Score Clamping Invariant**: 100% điểm thành phần $\in [0, 100]$.
- ✅ **Pre-deploy Checklist**: `python .agent/scripts/checklist.py` $\rightarrow$ **5/5 PASSED**.
- ✅ **Browser Subagent Visual Test**: Kiểm thử tự động trên 3 viewports:
  - Mobile (390 x 844 px): Nút `ⓘ` hiển thị đúng vị trí, modal mở mượt mà, FAB hoạt động tốt.
  - Đường viền bảng phẳng và liền mạch 100% trên toàn bộ các cột Giá, Hàng, Điểm, Shop.
  - Số liệu động và log v2.4 hiển thị đầy đủ, chính xác.
  - Video & ảnh chụp nghiệm thu: `table_border_fixed_verification_1786816020102.webp`, `desktop_layout_table_1786816026662.png`.

---

## ⚡ Phiên bản v2.3 — Chuẩn hoá Thang điểm Max & Lọc Desktop (13/08/2026)

**Ngày:** 13/08/2026 • **Agents:** `scoring-architect`, `qa-test-engineer` • **Trạng thái:** Đã deploy

1. **Chuẩn hoá thang điểm theo max thực tế:** CPU/GPU chấm theo đỉnh laptop thật (RTX 5090 = 100), kéo giãn khoảng cách máy cao cấp.
2. **Loại bỏ máy desktop:** Lọc sạch Mac Studio, Mac Pro, iMac, Studio Display khỏi bảng xếp hạng laptop.
3. **Sửa điểm Apple GPU:** MacBook "N-core GPU" chấm đúng theo chip (trước bị 100 tràn).

---

## ⚡ Phiên bản v2.2 — Bỏ Thưởng dGPU & Tách Điểm Giá Trị (13/08/2026)

**Ngày:** 13/08/2026 • **Agents:** `scoring-architect`, `devops-specialist` • **Trạng thái:** Đã deploy

1. **Bỏ thưởng +10 dGPU:** Điểm GPU thuần PassMark G3D, tránh đảo hạng card rời yếu vượt iGPU mạnh.
2. **Apple Silicon Geekbench Metal:** M1 $\rightarrow$ M5 Max quy đổi chuẩn Notebookcheck/Blender.
3. **Tách 2 loại điểm:** Điểm Giá Trị (xếp hạng chính) và Điểm Phần Cứng (trong modal).

---

## ⚡ Phiên bản v2.1 — Chấm Điểm Chuẩn PassMark & Review Claude (12/08/2026)

**Ngày:** 12/08/2026 • **Agents:** `scoring-architect`, `qa-test-engineer` • **Trạng thái:** Đã deploy

1. **Fix storage overflow:** Gộp bonus vào `storage_raw` trước khi clamp 1 lần duy nhất, tránh 2TB NVMe vượt 100.
2. **Viết 35 unit test tự động:** Đưa `test_scoring.py` vào CI/CD pre-commit.
3. **Audit trọng số 6 chuyên ngành:** Đảm bảo $\sum w_i = 1.000$.
