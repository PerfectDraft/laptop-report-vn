# 🤖 AGENTS.md — Laptop Report VN

Hệ thống quản lý và quy chuẩn vận hành dành cho Đội quân Agent (Multi-Agent Squad) trong dự án **Laptop Report VN**.

---

## 👥 Đội quân Agent & Phân bổ Chuyên môn (Agent Squad)

| Agent | Domain | Nhiệm vụ chính |
|---|---|---|
| 👑 **`orchestrator`** | Meta / Điều phối | Điều phối 2-Phase (Planning $\rightarrow$ Implementation), bắt buộc tối thiểu 3 Agent phối hợp, kiểm soát exit gate. |
| 📋 **`project-planner`** | Planning | Phân tích yêu cầu, thiết kế kiến trúc, lập PLAN.md, roadmap tính năng. |
| 🕷️ **`crawler-specialist`** | Crawling / Scraping | Thu thập dữ liệu từ 13 shop VN (TGDD, FPT, Phong Vũ, CellphoneS, GearVN, Hacom, ShopDunk, LaptopAZ, Laptop88, LaptopWorld, No1, Hoàng Hà, LaptopGame), verify tồn kho PDP. |
| 🧬 **`data-reconciler`** | ETL / Data Sync | Chuẩn hoá tên linh kiện (CPU, GPU, RAM, SSD, Màn hình, Pin), khử trùng lặp dữ liệu, phát hiện thiếu thông số. |
| 🧮 **`scoring-architect`** | Scoring / Benchmark | Duy trì & tối ưu thuật toán chấm điểm (PassMark log-scale, RAM log2, SSD tiers, Display PPI+Hz+Panel, Pin 100Wh, Value Factor). |
| 🎨 **`frontend-specialist`** | UI / UX / Web | Tối ưu HTML/CSS/JS Single-File bundle, Dark mode, thanh trượt trọng số (sliders), responsive di động & desktop. |
| 🧪 **`qa-test-engineer`** | Testing / QA | Quản lý 35+ unit test tự động (`test_scoring.py`), boundary tests, invariant tests qua Node & Python. |
| 🛡️ **`security-auditor`** | Security / Anti-bot | Kiểm tra an toàn crawler, rate limit, kiểm soát mã độc và rò rỉ secret / API keys. |
| 🚀 **`devops-specialist`** | Build / Deploy | Tối ưu nén dữ liệu (~6x), script `build_compact.py`, kiểm tra cấu hình Vercel và triển khai production. |
| 🔍 **`debugger`** | Debugging | Điều tra lỗi dữ liệu cào, lỗi tính điểm, lỗi render DOM hoặc conflict parser. |

---

## 📜 Quy tắc cốt lõi (Auto-load mỗi phiên)
Đọc theo thứ tự ưu tiên:
1. `.agent/rules/GEMINI.md` — Quy tắc kỹ thuật chung & bất biến toán học
2. `.agent/rules/versioning-and-changelog.md` — Quy chuẩn phiên bản & đồng bộ nhật ký lên giao diện Web (In-App Changelog)
3. `.agent/rules/progress-tracking.md` — Quy chuẩn đảm bảo tiến độ & báo cáo sửa đổi 4 lớp (Quad-Layer Sync)
4. `.agent/rules/scoring-contract.md` — Hợp đồng công thức chấm điểm & chuẩn dữ liệu
5. `.agent/rules/autonomous-policy.md` — Quy chế chạy tự động & an toàn
6. `.agent/rules/security-rules.md` — An toàn crawler & bảo vệ bí mật

---

## 🚦 Pre-commit & Pre-deploy Checklist
Trước mỗi commit hoặc deploy, BẮT BUỘC chạy và đảm bảo **5/5 checks PASSED**:
```bash
python .agent/scripts/checklist.py
```
Nội dung kiểm tra bao gồm:
1. ✅ **Scoring Unit Tests**: `python test_scoring.py` $\rightarrow$ 35/35 passed.
2. ✅ **Dataset Integrity**: `all_items.json` & `_ALL_scored.json` tồn tại, cấu trúc chuẩn.
3. ✅ **Score Clamping**: Không có điểm thành phần nào $> 100$ hoặc $< 0$.
4. ✅ **Compact Build & In-App Changelog**: `python build_compact.py` sinh HTML hợp lệ, `UPDATE_LOGS` đồng bộ với docs.
5. ✅ **Security Scan**: Không có hardcoded secret / API key trong mã nguồn.

---

## 💻 Code Style & Ngôn ngữ
- **Giao tiếp**: Tiếng Việt chuẩn mực, rõ ràng, súc tích với người dùng.
- **Code & Comments**: Code bằng Python 3.10+ / ES6+ JavaScript, comment bằng tiếng Anh hoặc tiếng Việt chuẩn.
- **Triết lý Web UI**: Không dùng framework cồng kềnh cho trang report; giữ nguyên kiến trúc Single-File HTML siêu nhẹ, tự đóng gói toàn bộ CSS, JS và Data JSON nén.

---

## 🔄 Quy trình làm việc (Workflow Preferences — Chuẩn Widget_Date)
- **Đồng bộ 4 Lớp (Quad-Layer Sync)** mỗi khi có phiên bản hoặc cải tiến lớn:
  1. Cập nhật `UPDATE_LOGS` trong `build_compact.py` $\rightarrow$ Giao diện Web hiển thị ngay Modal Nhật ký `#log-modal` & Header Version Badge.
  2. Cập nhật [BAO_CAO_SUA_DOI.md](file:///d:/UET/ProjectVibeCode/laptopReport/BAO_CAO_SUA_DOI.md) mỗi khi chỉnh sửa code, UI, data hoặc thuật toán.
  3. Cập nhật [PROGRESS.md](file:///d:/UET/ProjectVibeCode/laptopReport/PROGRESS.md) cuối mỗi phiên làm việc.
  4. Cập nhật [AUTONOMOUS_LOG.md](file:///d:/UET/ProjectVibeCode/laptopReport/AUTONOMOUS_LOG.md) sau mỗi phiên autonomous / orchestration.
- Luôn chạy `python .agent/scripts/checklist.py` trước khi hoàn tất công việc (bắt buộc 5/5 PASSED).
- Không merge code và docs vào chung một commit lộn xộn.

