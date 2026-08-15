# 🎯 GEMINI.md — Quy tắc Kỹ thuật Cốt lõi (Laptop Report VN)

Tài liệu này định nghĩa các nguyên tắc kỹ thuật bắt buộc cho toàn bộ Agent khi phát triển và bảo trì hệ thống Laptop Report VN.

---

## 1. 📐 Nguyên tắc Bất biến Toán học (Mathematical Invariants)

1. **Giới hạn Điểm số (Score Clamping)**:
   - Tất cả điểm thành phần $S_{component} \in [0, 100]$.
   - Tuyệt đối không cộng bonus sau khi clamp. Mọi bonus/penalty phải được gộp vào điểm thô trước khi thực hiện clamp duy nhất:
     ```python
     score_raw = base_calc + bonus_or_penalty
     score_clamped = min(100.0, max(0.0, score_raw))
     ```
2. **Tổng Trọng số (Sum of Weights)**:
   - Với tất cả 6 khối ngành (AI, CNTT, Đồ hoạ, Văn phòng, Game, CAD), tổng trọng số các tiêu chí bắt buộc:
     $$\sum_{i=1}^{6} w_i = 1.000$$
3. **Hệ số Giá trị (Value Factor)**:
   - $VF = 1.0 \pm dist \times 0.15$
   - $VF$ luôn bị chặn trong khoảng $[0.85, 1.15]$.
4. **Không Bonus dGPU gây Đảo Hạng**:
   - Điểm GPU sử dụng điểm PassMark G3D Mark log-scale. Do điểm G3D đã phản ánh chính xác khoảng cách giữa dGPU và iGPU, không được cộng thêm flat bonus $+10$ vào dGPU để tránh làm méo mó thứ hạng.

---

## 2. ⚡ Nguyên tắc Kiến trúc Web & Giao diện

1. **Zero-Runtime Dependency (Single File HTML)**:
   - File kết quả xuất xưởng (`bao-cao-laptop-phan-khuc.html` và `deploy/index.html`) là một tài liệu HTML độc lập, bao gồm toàn bộ inline CSS, JavaScript ES6 và nén Data JSON (~6x).
   - Không được require CDN nặng nề hoặc các framework bên ngoài khiến trang bị chậm hoặc hỏng khi offline.
2. **Đồng bộ Logic Python $\leftrightarrow$ JavaScript**:
   - Logic tính điểm phía Python (dùng để generate data ban đầu) và logic tính điểm phía JavaScript (dùng khi người dùng kéo slider tuỳ chỉnh trọng số) phải **hoàn toàn đồng nhất từng số thập phân**.
   - Mọi thay đổi công thức ở `build_compact.py` bắt buộc phải cập nhật tương ứng ở hàm JS `computeScore` và `valueFactorFor`.
3. **Trải nghiệm Trực quan Cao cấp**:
   - Giao diện hỗ trợ Dark Mode chuẩn mực với palette màu dịu mắt (`#0f1420`, `#1a2233`, `#22d3ee`, `#4f8cff`).
   - Mọi tương tác bộ lọc và thanh trượt slider phải phản hồi ngay lập tức dưới 16ms (60 FPS).

---

## 3. 🛡️ Nguyên tắc Cào dữ liệu & Bảo mật

1. **Tôn trọng Rate Limit**:
   - Khi chạy script cào dữ liệu từ 13 shop VN, luôn thêm delay ngẫu nhiên `0.5s – 2.0s` giữa các request để tránh gây tải cho server đích và tránh bị block IP.
2. **Xử lý Dữ liệu Khuyết thiếu (Defensive Parsing)**:
   - Luôn sử dụng `.get()` và cung cấp giá trị mặc định hợp lý (ví dụ: RAM 8GB, Pin 45Wh, màn hình 60Hz) khi shop không ghi rõ thông số, đồng thời gắn cờ `_fam = "unknown"` để theo dõi.
3. **Bảo vệ Bí mật (No Secret Leak)**:
   - Tuyệt đối không commit API keys, token, hoặc thông tin nhạy cảm vào repository.
