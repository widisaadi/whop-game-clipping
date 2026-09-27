import urllib.request
import re
import os
import sys
import time

content_files = [
    ("01_01_gameplay.mp4", "1GVJwheW9cPvbn1w66Q03a4foLQN_dcb-"),
    ("02_02_black_holes.mp4", "1NBlUeWIrHfT3Gwlgj_eLcF1TeH6A4VV1"),
    ("03_03_more_gameplay.mp4", "1c6vb3xeAOXCsCjZsa86f4o3C6qjmcDBr"),
    ("04_04_even_more_gameplay.mp4", "1T6QKt2-oJ6X1JB8eMfFVNtRKFR8sxSgj"),
    ("05_05_the_black_hole_effect.mp4", "1cALKgKaQtu3AGv_1qr3_nmjCDxj-jSV8"),
    ("06_2026-08-13_20-46-03.mp4", "1Bbq16ZlzXGZj40wzBptFNBi2toFVR_pa"),
    ("07_2026-08-14_10-16-18.mp4", "13YOoN_DQM7UyWKTsTNWy-AucGg8qNyQS"),
    ("08_2026-08-14_10-20-26.mp4", "1uW0NCg98BjkZa-msDNhiZXSSsDXhDLyD"),
    ("09_2026-08-14_10-20-54.mp4", "1S37fXz23E6pWPdBMyrchIFbrvhhZqGF1"),
    ("10_2026-08-14_10-21-20.mp4", "1oStbq-JE8M1uPALjf8E2BsWe8BWQ7dIF"),
    ("11_2026-08-14_12-55-34.mp4", "1Eh78xIZo2Vx029vkWturF8sXjbHia8DL"),
    ("12_2026-08-14_12-59-38.mp4", "1WP8FqWFpXaXz7nPgYvO7h2AAXFf6hO9C"),
    ("13_2026-08-14_13-05-27.mp4", "1j_LWKEQVEDtO0WMvZT8XV78cntpHgvHH"),
    ("14_2026-08-14_14-08-25.mp4", "1bFcvlsnELkjfQDOy1V3LNsnlrYHxlWE-"),
    ("15_2026-08-14_15-50-35.mp4", "1VjvwVxmsoMCS0w3DGVq__E-CfTXeUBQm")
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def download_one(name, fid, out_dir):
    out_path = os.path.join(out_dir, name)
    # Check if already fully downloaded (at least 1MB)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000000:
        # Check if file has incomplete size
        sz_mb = os.path.getsize(out_path) / (1024*1024)
        print(f"[EXISTS] {name} ({sz_mb:.2f} MB)", flush=True)
        return True

    url = f"https://drive.google.com/uc?export=download&id={fid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=90) as resp:
            ct = resp.headers.get("Content-Type", "")
            cl = resp.headers.get("Content-Length")
            sz_str = f"{int(cl)/(1024*1024):.2f} MB" if cl else "unknown size"
            print(f"Downloading {name} ({sz_str})...", flush=True)

            if "text/html" in ct:
                html = resp.read().decode("utf-8", errors="ignore")
                m = re.search(r'confirm=([a-zA-Z0-9_-]+)', html)
                if m:
                    token = m.group(1)
                    url2 = f"https://drive.google.com/uc?export=download&id={fid}&confirm={token}"
                    req2 = urllib.request.Request(url2, headers=headers)
                    with urllib.request.urlopen(req2, timeout=90) as resp2:
                        with open(out_path, "wb") as f:
                            while True:
                                b = resp2.read(1024*1024)
                                if not b:
                                    break
                                f.write(b)
                else:
                    print(f"Error: HTML returned but no confirm token for {name}", flush=True)
                    return False
            else:
                with open(out_path, "wb") as f:
                    while True:
                        b = resp.read(1024*1024)
                        if not b:
                            break
                        f.write(b)
            
            elapsed = time.time() - t0
            actual_sz = os.path.getsize(out_path) / (1024*1024)
            print(f"[DONE] {name}: {actual_sz:.2f} MB in {elapsed:.1f}s", flush=True)
            return True
    except Exception as e:
        print(f"[FAIL] {name}: {e}", flush=True)
        return False

out_dir = "campaigns/asmr_dominoes/assets/clips"
os.makedirs(out_dir, exist_ok=True)
for name, fid in content_files:
    download_one(name, fid, out_dir)
print("=== All Gameplay Clips Download Finished ===", flush=True)
