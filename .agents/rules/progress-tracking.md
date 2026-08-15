# 📈 progress-tracking.md — Quy Chuẩn Đảm Bảo Tiến Độ & Báo Cáo Chỉnh Sửa (Widget_Date Architecture)

Tài liệu này định nghĩa hệ thống quản lý tiến độ, ghi chép nhật ký và báo cáo kỹ thuật 3 lớp kế thừa từ kiến trúc chuẩn của **Widget_Date**.

---

## 🏛️ Hệ Thống Ghi Nhận 3 Lớp (Triple-Layer Progress Tracking)

| Lớp | File Lưu Trữ | Mục Đích | Thời Điểm Cập Nhật |
|---|---|---|---|
| **Lớp 1** | `BAO_CAO_SUA_DOI.md` | Báo cáo chi tiết kỹ thuật: nguyên nhân lỗi, cách fix, diff logic, kết quả test. | Mỗi khi có bất kỳ chỉnh sửa code / UI / data / thuật toán nào. |
| **Lớp 2** | `PROGRESS.md` | Lộ trình tính năng dự án (Roadmap) và tóm tắt phiên làm việc (Session Logs). | Cuối mỗi phiên làm việc hoặc khi hoàn thành task. |
| **Lớp 3** | `AUTONOMOUS_LOG.md` | Nhật ký điều phối Autonomous / Orchestration Squad. | Sau mỗi phiên chạy đa Agent hoặc chạy tự động. |

---

## 📝 1. Quy Chuẩn Lớp 1: Báo Cáo Sửa Đổi Kỹ Thuật (`BAO_CAO_SUA_DOI.md`)

Mỗi khi sửa đổi code, Agent **BẮT BUỘC** bổ sung một mục mới lên đầu file theo định dạng chuẩn:
```markdown
## 🚀 Phiên bản vX.Y — <Tên Đợt Sửa Đổi> (<DD/MM/YYYY>)

**Ngày:** DD/MM/YYYY • **Agents tham gia:** `agent-1`, `agent-2` • **Trạng thái:** ✅ Đã hoàn tất & build release

### 1. Vấn đề & Nguyên nhân (Problem & Root Cause)
- **Hiện tượng:** Mô tả chi tiết lỗi hoặc yêu cầu người dùng.
- **Nguyên nhân kỹ thuật:** Phân tích logic sai lệch, CSS conflict, dữ liệu khuyết thiếu...

### 2. Các thay đổi chi tiết (Detailed Modifications)
- **File A:** Sửa hàm X, đổi công thức Y...
- **File B:** Thêm CSS responsive, tách class...

### 3. Kết quả Kiểm thử & Nghiệm thu (Verification & Exit Gate)
- ✅ **Unit Tests:** `python test_scoring.py` $\rightarrow$ 35/35 passed.
- ✅ **Checklist:** `python .agent/scripts/checklist.py` $\rightarrow$ 5/5 PASSED.
- ✅ **Visual / Browser Test:** Kết quả kiểm tra trực quan.
```

---

## 📊 2. Quy Chuẩn Lớp 2: Lộ Trình & Tiến Độ Dự Án (`PROGRESS.md`)

- **Đầu phiên:** Kiểm tra `PROGRESS.md` để nắm bắt tính năng đang phát triển.
- **Trong phiên:** Đánh dấu `[x]` vào các checklist tính năng đã xong.
- **Cuối phiên:** Bổ sung dòng vào bảng **Session Logs**:
  `| DD/MM/YYYY | <Agents> | <Mô tả công việc> | Hoàn tất |`

---

## 🤖 3. Quy Chuẩn Lớp 3: Nhật Ký Điều Phối Squad (`AUTONOMOUS_LOG.md`)

- Ghi lại các phiên chạy Orchestration hoặc Autonomous.
- Ghi rõ danh sách tối thiểu 3 Agent tham gia, mục tiêu và kết quả kiểm tra `checklist.py`.

---

## 🚦 4. Giao Thức Đóng Phiên (Session Close Protocol)

Trước khi đóng phiên làm việc và báo cáo người dùng:
1. Chạy `python .agent/scripts/checklist.py` $\rightarrow$ Đạt **5/5 PASSED**.
2. Đồng bộ cập nhật đầy đủ cả 3 file: `BAO_CAO_SUA_DOI.md`, `PROGRESS.md`, `AUTONOMOUS_LOG.md`.
3. Kiểm tra tính toàn vẹn của build compact output (`deploy/index.html` và `bao-cao-laptop-phan-khuc.html`).
