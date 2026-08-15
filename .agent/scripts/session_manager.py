#!/usr/bin/env python3
"""Session Manager for Laptop Report VN — Manages progress tracking, modification logs, and session closes.
Inherited from Widget_Date architecture.
"""
import os, sys, datetime

def get_target_files(filename):
    candidates = [
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), "laptop-report-vn", filename),
    ]
    return [p for p in candidates if os.path.exists(os.path.dirname(p))]

def log_progress(role, description, status="Hoàn tất"):
    now_str = datetime.datetime.now().strftime("%d/%m/%Y")
    line = f"| {now_str} | `{role}` | {description} | {status} |\n"
    
    files = get_target_files("PROGRESS.md")
    for fpath in files:
        if os.path.exists(fpath):
            with open(fpath, "a", encoding="utf-8") as f:
                f.write(line)
            print(f"✅ Đã ghi nhận phiên làm việc vào {fpath}")

def log_autonomous(session_name, agents_list, goal, changes_summary, checklist_res="5/5 PASSED"):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"""
### [{now_str}] Session: {session_name}
- **Chế độ**: Orchestration / Autonomous
- **Agents tham gia**: {', '.join(f'`{a}`' for a in agents_list)}
- **Mục tiêu**: {goal}
- **Các thay đổi**:
{changes_summary}
- **Kết quả Checklist**: {checklist_res}
- **Trạng thái**: ✅ Hoàn tất xuất sắc.
"""
    files = get_target_files("AUTONOMOUS_LOG.md")
    for fpath in files:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if "## 📜 Lịch sử Phiên Chạy" in content:
                parts = content.split("## 📜 Lịch sử Phiên Chạy")
                new_content = parts[0] + "## 📜 Lịch sử Phiên Chạy\n" + entry + parts[1]
            else:
                new_content = content + "\n" + entry
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Đã ghi nhận autonomous log vào {fpath}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--progress":
        role = sys.argv[2] if len(sys.argv) > 2 else "orchestrator"
        desc = sys.argv[3] if len(sys.argv) > 3 else "Routine maintenance and checks"
        log_progress(role, desc)
    else:
        print("Sử dụng: python session_manager.py --progress <role> <description>")
