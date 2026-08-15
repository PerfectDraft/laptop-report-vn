---
name: web-design-guidelines
description: Quy chuẩn thiết kế giao diện Dark Mode, typography, CSS tokens và trải nghiệm người dùng hiện đại.
---

# 🎨 Skill: Web Design Guidelines

## 1. CSS Design Tokens
```css
:root {
  --bg: #0f1420;
  --card: #1a2233;
  --card2: #202a3f;
  --border: #2c3a55;
  --text: #e8eef7;
  --muted: #93a3bc;
  --accent: #4f8cff;
  --accent2: #22d3ee;
  --gold: #fbbf24;
  --green: #34d399;
  --red: #f87171;
}
```

## 2. Micro-interactions
- Hiệu ứng hover cho thẻ laptop: `transform: translateY(-2px)`, đổ bóng phát sáng nhẹ `box-shadow: 0 4px 20px rgba(34, 211, 238, 0.1)`.
- Thanh trượt slider trọng số: Phản hồi gradient theo giá trị di chuyển.
- Badge tình trạng hàng rõ ràng, dễ nhìn.
