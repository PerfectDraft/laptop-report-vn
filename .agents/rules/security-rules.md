# 🛡️ security-rules.md — Quy tắc An toàn & Bảo mật

---

## 1. Bảo mật Crawler & Chống Chặn (Anti-Bot Safety)
- **User-Agent Rotation**: Luôn sử dụng User-Agent hợp lệ của các trình duyệt phổ biến (Chrome/Edge/Firefox).
- **Throttling & Backoff**: Đặt khoảng nghỉ giữa các request `[0.5s - 2.0s]`. Nếu gặp mã `429 Too Many Requests` hoặc `403 Forbidden`, kích hoạt hàm exponential backoff.
- **Không bypass Trái phép**: Không can thiệp hoặc cố tình phá vỡ các hệ thống bảo mật phức tạp; ưu tiên đọc API công khai hoặc sitemap chính thức của shop.

---

## 2. Bảo vệ Thông tin Bí mật (Secrets Protection)
- Không commit các thông tin định danh nhạy cảm, API keys (như AIza, OpenAI token, PassMark API key thương mại) vào Git.
- Mọi cấu hình môi trường phải nằm trong file `.env` và được khai báo vào `.gitignore`.

---

## 3. An toàn File & Bộ nhớ (Resource Safety)
- Quản lý kích thước bộ nhớ khi load các file JSON lớn (như `details.json` 700KB+, `_ALL_scored.json` 3300+ items).
- Đóng file đúng cách (`with open(...) as f:`).
