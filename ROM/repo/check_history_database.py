import sys
import json

def main():
    if len(sys.argv) < 3:
        print("ERROR|Thiếu tham số đầu vào (URL, CURRENT_SHA)")
        return
        
    target_url = sys.argv[1].strip()
    current_sha = sys.argv[2].strip()
    
    try:
        # Đọc dữ liệu JSON của file built_history.json từ stdin
        history = json.load(sys.stdin)
        roms = history.get('built_roms', [])
        
        # Kiểm tra xem có bản ghi nào trùng khít cả URL lẫn Commit SHA không
        match = any(r.get('url') == target_url and r.get('commit') == current_sha for r in roms)
        
        if match:
            print("DUPLICATED|Trùng lịch sử")
        else:
            print("NEW|Hợp lệ")
            
    except Exception as e:
        # Nếu file JSON trên My-Assets trống hoặc lỗi cấu trúc, coi như chưa build
        print(f"NEW|Lỗi đọc database hoặc file trống: {str(e)}")

if __name__ == '__main__':
    main()
