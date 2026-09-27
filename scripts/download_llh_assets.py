import os
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate"
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
EPISODES_DIR = os.path.join(BASE_DIR, "assets", "episodes")
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(EPISODES_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)

# Catalog of assets to download
ASSETS = [
    # Short Moments (High intensity scenes)
    {"name": "LLH_clipping_4_Deception.mp4", "id": "1Qu6cEIp0cQsF4aBLEOJvoTNyREP3a8za", "target": CLIPS_DIR, "size_mb": 12.33},
    {"name": "LLH_clipping_9_Kiss.mp4", "id": "1cWKR9dzwI8HVKLAKd4r0NEPGrwlW-RTj", "target": CLIPS_DIR, "size_mb": 11.51},
    {"name": "LLH_clipping_10_Game.mp4", "id": "1hquSFsthiq_nIYgTPcmwTU-xxSq9PtM2", "target": CLIPS_DIR, "size_mb": 9.19},
    {"name": "LLH_clipping_17_Smile.mp4", "id": "1z7wjRfSCAwbLOd_1BSRNrwwKPaxahdmT", "target": CLIPS_DIR, "size_mb": 4.01},
    {"name": "LLH_clipping_18_Dance.mp4", "id": "1GiJesBxrkjWVtOwp3wYwGBaXni8rVKTl", "target": CLIPS_DIR, "size_mb": 22.04},
    {"name": "LLH_clipping_19_almostKiss.mp4", "id": "1N9b-FxsEWFJlhjAlVH5puERTskqDHVri", "target": CLIPS_DIR, "size_mb": 24.14},
    {"name": "LLH_clipping_20_KiSS.mp4", "id": "1AChf5GYqpq6jKe_-DY1ke_2rDSkdRjGC", "target": CLIPS_DIR, "size_mb": 13.91},
    {"name": "LLH_clipping_Hug.mp4", "id": "1mbUVvl-bdO_LZCB14FIhMZ62xHt3n145", "target": CLIPS_DIR, "size_mb": 9.05},

    # Love Edits (Montages)
    {"name": "LLH_clipping_montage1.mp4", "id": "1krP-gJqR2xE7YNO2N8Ma7cw4-fXx_6jA", "target": CLIPS_DIR, "size_mb": 24.23},
    {"name": "LLH_clipping_montage2.mp4", "id": "1rApculfQtesZVkonWCJ4Hu3MxEww_nc2", "target": CLIPS_DIR, "size_mb": 38.16},
    {"name": "LLH_clipping_montage3.mp4", "id": "1C5DK6bnM-nulLIOk6UwfNpFhyP8YjN3q", "target": CLIPS_DIR, "size_mb": 23.63},
    {"name": "LLH_clipping_montage4.mp4", "id": "1N1GBEdXEJtODFIzJOBqpim_ay0UPmVQU", "target": CLIPS_DIR, "size_mb": 33.37},
    {"name": "LLH_clipping_montage5.mp4", "id": "1SK0yImRKAwhwDOG2J_vIejWO_-3FvRh4", "target": CLIPS_DIR, "size_mb": 21.23},
    {"name": "LLH_clipping_montage6.mp4", "id": "1zxPbYY5D1auL7iA45Q5N9aO0tPVkWm-v", "target": CLIPS_DIR, "size_mb": 31.54},
    {"name": "LLH_clipping_montage7.mp4", "id": "1qkrvRfHaJjaY950yG0Rzey0-DHWL2Ls7", "target": CLIPS_DIR, "size_mb": 27.95},
    {"name": "LLH_clipping_montage8.mp4", "id": "1SkUIjrZg1Sp1MZwTDEec1Xz8UUHbrikK", "target": CLIPS_DIR, "size_mb": 19.81},
]

def download_one(asset):
    filepath = os.path.join(asset["target"], asset["name"])
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100000:
        actual_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"[EXISTS] {asset['name']} ({actual_mb:.2f} MB)")
        return True, asset["name"]

    url = f"https://drive.usercontent.google.com/download?id={asset['id']}&export=download&confirm=t"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(filepath, "wb") as f:
            f.write(data)
        elapsed = time.time() - t0
        mb = len(data) / (1024 * 1024)
        speed = mb / elapsed if elapsed > 0 else 0
        print(f"[DONE] {asset['name']} ({mb:.2f} MB in {elapsed:.1f}s @ {speed:.2f} MB/s)")
        return True, asset["name"]
    except Exception as e:
        print(f"[FAIL] {asset['name']}: {e}")
        return False, asset["name"]

def main():
    print(f"Starting download of {len(ASSETS)} core clips and montages...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(download_one, a): a for a in ASSETS}
        for future in as_completed(futures):
            res, name = future.result()

    print("\nDownload batch completed!")

if __name__ == "__main__":
    main()
