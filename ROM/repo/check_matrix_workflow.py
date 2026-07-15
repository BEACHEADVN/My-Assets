import sys
import json
import urllib.request

def get_run_inputs_and_sha(repo, run_id, token):
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("inputs", {}), data.get("head_sha", "")
    except Exception:
        return {}, ""

def main():
    if len(sys.argv) < 5:
        print("BUILD_ERROR|Thiếu tham số đầu vào (URL, REPO, TOKEN, CURRENT_SHA)")
        return
        
    target_url = sys.argv[1].strip()
    repo = sys.argv[2].strip()
    token = sys.argv[3].strip()
    current_sha = sys.argv[4].strip()
    
    try:
        data = json.load(sys.stdin)
        runs = data.get('workflow_runs', [])
        
        for r in runs[:2]:
            status = r.get('status', '')
            
            if status in ['in_progress', 'queued']:
                run_id = r.get('id')
                inputs, run_sha = get_run_inputs_and_sha(repo, run_id, token)
                rom_in_input = inputs.get('input_url', '').strip()
                
                # SỬA ĐỔI TẠI ĐÂY: Dùng startswith để mã SHA ngắn (7 số) khớp được với mã SHA dài (40 số)
                if target_url == rom_in_input and (run_sha.startswith(current_sha) or current_sha.startswith(run_sha)):
                    print("STOP_ACTIVE|ROM này với commit này hiện đang có luồng build khác đang chạy!")
                    return

        print("BUILD_NOT_RUNNING|Không có luồng trùng lặp nào đang chạy dở.")
            
    except Exception as e:
        print(f"BUILD_ERROR|Lỗi: {str(e)}")

if __name__ == '__main__':
    main()
