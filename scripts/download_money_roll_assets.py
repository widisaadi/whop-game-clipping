import os
import re
import urllib.request
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = "campaigns/money_roll"
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)

# Parse Google Drive HTML page
with open("temp/campaign_intake/gdrive_page.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r'aria-label="([^"]+?)\s+(?:Video|Image|Audio|Binary|Document|File)[^"]*".*?ssk=[\'"][^:\'"]*:[^:\'"]*:([a-zA-Z0-9_-]{25,})-[^\'"]*[\'"]'
matches = re.findall(pattern, html, re.DOTALL)

assets = []
seen_ids = set()
used_filenames = set()

for name, raw_id in matches:
    clean_id = raw_id.rsplit("-", 1)[0] if "-" in raw_id else raw_id
    if clean_id in seen_ids:
        continue
    seen_ids.add(clean_id)

    # Determine target dir & extension
    if "IMAGE" in name or name.endswith((".png", ".jpg", ".jpeg")):
        target_dir = BRANDING_DIR
        ext = ".png" if not name.endswith((".png", ".jpg", ".jpeg")) else ""
        local_name = f"{name}{ext}"
    else:
        target_dir = CLIPS_DIR
        ext = ".mp4" if not name.endswith(".mp4") else ""
        local_name = f"{name}{ext}"

    # Disambiguate duplicate names
    if local_name in used_filenames:
        base, ext_part = os.path.splitext(local_name)
        local_name = f"{base}_{clean_id[:7]}{ext_part}"
    used_filenames.add(local_name)

    assets.append({
        "id": clean_id,
        "original_name": name,
        "local_filename": local_name,
        "target_dir": target_dir,
        "local_path": os.path.join(target_dir, local_name)
    })

print(f"Total unique assets to download: {len(assets)}")

def download_file(item):
    path = item["local_path"]
    name = item["local_filename"]
    fid = item["id"]

    if os.path.exists(path) and os.path.getsize(path) > 10000:
        actual_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"[EXISTS] {name} ({actual_mb:.2f} MB)")
        return {**item, "status": "exists", "size": os.path.getsize(path), "error": None}

    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(path, "wb") as f:
            f.write(data)
        elapsed = time.time() - t0
        mb = len(data) / (1024 * 1024)
        speed = mb / elapsed if elapsed > 0 else 0
        print(f"[DONE] {name} ({mb:.2f} MB in {elapsed:.1f}s @ {speed:.2f} MB/s)")
        return {**item, "status": "downloaded", "size": len(data), "error": None}
    except Exception as e:
        print(f"[FAIL] {name} (ID: {fid}): {e}")
        return {**item, "status": "failed", "size": 0, "error": str(e)}

def main():
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(download_file, item): item for item in assets}
        for future in as_completed(futures):
            results.append(future.result())

    total_mb = sum(r["size"] for r in results) / (1024 * 1024)
    success = sum(1 for r in results if r["status"] in ["downloaded", "exists"])
    failed = sum(1 for r in results if r["status"] == "failed")
    elapsed = time.time() - start_time

    print(f"\n=======================================================")
    print(f"DOWNLOAD SUMMARY FOR +1 MONEY ROLL TO GET RICH")
    print(f"Total Files: {len(results)}")
    print(f"Success: {success} | Failed: {failed}")
    print(f"Total Size: {total_mb:.2f} MB in {elapsed:.1f}s")
    print(f"=======================================================\n")

    manifest = {
        "campaign": "+1 Money Roll To Get Rich",
        "campaign_slug": "money_roll",
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_drive_folder": "https://drive.google.com/drive/folders/1we4TNL1DxdsBgZyFw1moTZJilLaJ7kGz",
        "backup_drive_folder": "https://drive.google.com/drive/folders/1V6XGa1MXGU6CY0Y8_xSCOT4b4i229q0L",
        "total_items_found": len(results),
        "successful_downloads": success,
        "failed_downloads": failed,
        "files": results
    }

    manifest_path = os.path.join(BASE_DIR, "assets", "asset_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved asset manifest to: {manifest_path}")

if __name__ == "__main__":
    main()
