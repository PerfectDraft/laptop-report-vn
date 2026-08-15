# 📋 BÁO CÁO SỬA ĐỔI & TIẾN TRÌNH KỸ THUẬT (BAO_CAO_SUA_DOI.md)

Tài liệu ghi nhận toàn bộ lịch sử chỉnh sửa, lý do kỹ thuật, kết quả kiểm thử và phân bổ trách nhiệm theo chuẩn quản lý tiến trình **Widget_Date**.

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
