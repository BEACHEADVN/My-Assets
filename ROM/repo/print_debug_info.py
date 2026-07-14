import os
import sys
import json

def main():
    # Đọc dữ liệu JSON trực tiếp từ các biến môi trường
    commits_raw = os.environ.get("COMMITS_RAW", "[]")
    runs_raw = os.environ.get("RUNS_RAW", "{}")

    try:
        commits = json.loads(commits_raw)
    except Exception as e:
        print(f"❌ Lỗi giải mã dữ liệu Commit JSON: {e}")
        commits = []

    try:
        runs_data = json.loads(runs_raw)
        runs = runs_data.get("workflow_runs", [])
    except Exception as e:
        print(f"❌ Lỗi giải mã dữ liệu Workflow JSON: {e}")
        runs = []

    print("=" * 80)
    print("📝 [1 COMMIT MỚI NHẤT TRÊN REPO BUILD]")
    print("=" * 80)
    
    if commits and isinstance(commits[0], dict):
        c = commits[0]
        sha = c.get("sha", "")[:7]
        msg = c.get("commit", {}).get("message", "").strip()
        print(f"💻 SHA: {sha}")
        print(f"💬 Message: {msg}")
    else:
        print("ℹ️ Không tìm thấy dữ liệu commit nào.")

    print("\n" + "=" * 80)
    print("📊 [1 WORKFLOW RUN MỚI NHẤT CỦA BUILD.YML]")
    print("=" * 80)
    
    if runs and isinstance(runs[0], dict):
        r = runs[0]
        run_number = r.get("run_number", 0)
        title = r.get("display_title", "No Title")
        status = r.get("status", "unknown")
        conclusion = r.get("conclusion", "None")
        
        status_icon = "⏳"
        if status == "completed":
            if conclusion == "success":
                status_icon = "✅ [THÀNH CÔNG]"
            elif conclusion == "failure":
                status_icon = "❌ [THẤT BẠI]"
            elif conclusion == "cancelled":
                status_icon = "🛑 [ĐÃ HỦY]"
            else:
                status_icon = f"💤 [{conclusion.upper()}]"
        elif status in ["in_progress", "queued"]:
            status_icon = "🔄 [ĐANG CHẠY/ĐANG CHỜ]"

        print(f"🚀 Run #{run_number} | Trạng thái: {status_icon}")
        print(f"📌 Tiêu đề (Link ROM): {title}")
    else:
        print("ℹ️ Không tìm thấy lượt chạy nào của build.yml.")

    print("=" * 80)

if __name__ == "__main__":
    main()
