# 🧮 scoring-contract.md — Hợp đồng Quy chuẩn Chấm điểm Benchmark

Quy định chuẩn toán học và công thức tính điểm cho từng linh kiện phần cứng trong hệ thống Laptop Report VN.

---

## 1. Điểm CPU (`cpu_s`)
- **Nguồn dữ liệu**: PassMark CPU Mark (Single-thread & Multi-thread benchmark).
- **Thang đo**: Logarithmic scale chuẩn hoá theo dải hiệu năng thực tế.
- **Giá trị**: $0 \le S_{CPU} \le 100$.

---

## 2. Điểm RAM (`ram_s`)
- **Quy tắc**: Tăng trưởng theo hàm $\log_2$ (PassMark Standard).
- **Bảng quy đổi**:
  - $8\text{ GB} = 25.0$
  - $16\text{ GB} = 50.0$
  - $32\text{ GB} = 75.0$
  - $64\text{ GB} = 100.0$ (Cán trần $100$)
  - $\ge 128\text{ GB} = 100.0$ (Giữ mức trần $100$)

---

## 3. Điểm GPU (`gpu_s`)
- **Nguồn dữ liệu**: PassMark G3D Mark.
- **Thang đo**: Logarithmic scale.
- **Quy tắc**: KHÔNG cộng flat bonus $+10$ cho card rời (dGPU) vì G3D Mark đã phản ánh khoảng cách thực tế giữa iGPU và dGPU. Tránh gây hiện tượng đảo thứ hạng sai lệch.

---

## 4. Điểm Ổ cứng / Lưu trữ (`storage_s`)
- **Bảng điểm cơ sở theo chuẩn giao tiếp**:
  - **NVMe Gen 5**: $100$
  - **NVMe Gen 4**: $85$
  - **NVMe Gen 3**: $65$
  - **SATA SSD**: $45$ (Trung tính)
  - **HDD**: $15$
- **Hệ số dung lượng**:
  - $256\text{ GB} \rightarrow \times 0.9$
  - $512\text{ GB} \rightarrow \times 1.0$
  - $1\text{ TB} \rightarrow \times 1.08$
  - $2\text{ TB} \rightarrow \times 1.15$
- **Quy tắc Clamp**:
  $$\text{Storage Score} = \min(100.0, \max(0.0, \text{Base Tier} \times \text{Capacity Multiplier}))$$

---

## 5. Điểm Màn hình (`display_s`)
Điểm màn hình là tổng hợp có trọng số của 3 yếu tố:
$$\text{Display Score} = 0.45 \times S_{PPI} + 0.30 \times S_{Hz} + 0.25 \times S_{Panel}$$
- $S_{PPI}$: Mật độ điểm ảnh (PPI từ FHD trên 14" $\rightarrow$ 4K trên 16"/17").
- $S_{Hz}$: Tần số quét (60Hz $\rightarrow 0$, 120Hz $\rightarrow 50$, 144Hz $\rightarrow 70$, 240Hz+ $\rightarrow 100$).
- $S_{Panel}$: Công nghệ tấm nền (TN $= 40$, IPS $= 70$, OLED / Mini-LED $= 100$).
- **Giới hạn**: $\le 100.0$.

---

## 6. Điểm Pin (`batt_s`)
- **Chuẩn hoá**: Dựa trên giới hạn tối đa mang lên máy bay của IATA/FAA ($100\text{ Wh}$).
- **Công thức**:
  $$S_{Pin} = \min(100.0, \max(0.0, \text{Dung lượng Wh}))$$
- Ví dụ: Pin $50\text{ Wh} \rightarrow 50.0$ điểm, Pin $99.9\text{ Wh} \rightarrow 99.9$ điểm.

---

## 7. Hệ số Giá trị (Value Factor - $VF$)
- Nhằm phản ánh tương quan mức giá của sản phẩm trong phân khúc $[L, H]$:
  $$\text{dist} = \frac{|\text{Price} - \text{Center}|}{H - L}$$
  $$VF = \text{clamp}(1.0 \pm \text{dist} \times 0.15, [0.85, 1.15])$$
- **Điểm tổng kết cuối cùng**:
  $$\text{Final Score} = \left(\sum_{i} w_i \times S_i\right) \times VF$$
