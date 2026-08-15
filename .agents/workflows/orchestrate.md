---
description: Điều phối đa Agent cho các tác vụ phức tạp trong Laptop Report VN (Tối thiểu 3 Agent phối hợp).
---

# 👑 Multi-Agent Orchestration — Laptop Report VN

Bạn đang ở **CHẾ ĐỘ ĐIỀU PHỐI (ORCHESTRATION MODE)**. Nhiệm vụ: Phối hợp các Agent chuyên biệt để giải quyết bài toán phức tạp một cách toàn diện, không thiên vị, không bỏ sót góc nhìn.

---

## 🔴 YÊU CẦU BẮT BUỘC: TỐI THIỂU 3 AGENT

> ⚠️ **ORCHESTRATION = TỐI THIỂU 3 AGENT KHÁC NHAU**
> 
> Nếu chỉ dùng 1 hoặc 2 agent $\rightarrow$ Đây chỉ là uỷ thác đơn lẻ, KHÔNG PHẢI Orchestration.
> 
> **Tiêu chí nghiệm thu:**
> - Đếm số lượng Agent tham gia.
> - Nếu `agent_count < 3` $\rightarrow$ DỪNG LẠI và triệu tập thêm Agent chuyên ngành phù hợp.

### Ma trận Chọn Agent (Agent Selection Matrix)

| Loại Tác Vụ | Các Agent BẮT BUỘC (Tối thiểu 3) |
|---|---|
| **Thu thập & Cập nhật Shop** | `crawler-specialist`, `data-reconciler`, `qa-test-engineer` |
| **Sửa / Tối ưu Thuật toán Chấm điểm** | `scoring-architect`, `qa-test-engineer`, `frontend-specialist` |
| **Nâng cấp Giao diện & Tương tác** | `frontend-specialist`, `qa-test-engineer`, `devops-specialist` |
| **Debug Lỗi Sai Lệch / Trùng Lặp** | `debugger`, `data-reconciler`, `qa-test-engineer` |
| **Release & Deploy Production** | `devops-specialist`, `security-auditor`, `qa-test-engineer` |
| **Toàn bộ Tính năng Mới (End-to-End)** | `project-planner`, `scoring-architect`, `frontend-specialist`, `qa-test-engineer` |

---

## 🔴 QUY TRÌNH 2 GIAI ĐOẠN NGHIÊM NGẶT (STRICT 2-PHASE)

### GIAI ĐOẠN 1: LẬP KẾ HOẠCH (Sequential — Không chạy song song)
1. `project-planner`: Phân tích yêu cầu, xác định các trường dữ liệu và công thức liên quan.
2. Viết kế hoạch vào `implementation_plan.md`.
3. ⏸️ **DỪNG LẠI & XIN Ý KIẾN NGƯỜI DÙNG**. Chỉ chuyển sang Giai đoạn 2 khi người dùng duyệt!

### GIAI ĐOẠN 2: THỰC THI (Parallel Agents sau khi được duyệt)
- Triệu tập các Agent thực thi song song theo chuyên môn.
- Bước cuối cùng: `qa-test-engineer` và `security-auditor` chạy script kiểm tra xác thực.

---

## 🚦 EXIT GATE (Cổng Nghiệm thu)

Trước khi đóng phiên điều phối, kiểm tra:
1. ✅ **Số lượng Agent:** Đã kích hoạt $\ge 3$ Agent chuyên trách.
2. ✅ **Kiểm thử tự động:** `python .agent/scripts/checklist.py` trả về **5/5 PASSED**.
3. ✅ **Tài liệu cập nhật:** Đã cập nhật `PROGRESS.md` và `AUTONOMOUS_LOG.md`.
