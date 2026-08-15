# 📋 BÁO CÁO SỬA ĐỔI & TIẾN TRÌNH KỸ THUẬT (BAO_CAO_SUA_DOI.md)

Tài liệu ghi nhận toàn bộ lịch sử chỉnh sửa, lý do kỹ thuật, kết quả kiểm thử và phân bổ trách nhiệm theo chuẩn quản lý tiến trình **Widget_Date**.

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
