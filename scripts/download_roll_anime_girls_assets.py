import os
import re
import urllib.request
import time
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = "campaigns/roll_anime_girls"
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")
os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)

# Parse main folder
with open("temp/campaign_intake/rag_main.html", "r", encoding="utf-8") as f:
    main_html = f.read()

pattern = r'aria-label="([^"]+?)\s+(?:Video|Image|Audio|Binary|Document|File)[^"]*".*?ssk=[\'"][^:\'"]*:[^:\'"]*:([a-zA-Z0-9_-]{25,})-[^\'"]*[\'"]'
main_matches = re.findall(pattern, main_html, re.DOTALL)

# Parse backup folder
with open("temp/campaign_intake/rag_backup.html", "r", encoding="utf-8") as f:
    backup_html = f.read()
backup_matches = re.findall(pattern, backup_html, re.DOTALL)

backup_map = {}
for name, raw_id in backup_matches:
    clean_id = raw_id.rsplit("-", 1)[0] if "-" in raw_id else raw_id
    # e.g. "Copy of 01_Clip 1.mp4" -> "01_Clip 1.mp4"
    normalized = name.replace("Copy of ", "").strip()
    backup_map[normalized] = clean_id

assets = []
seen = set()
for name, raw_id in main_matches:
    clean_id = raw_id.rsplit("-", 1)[0] if "-" in raw_id else raw_id
    if clean_id in seen:
        continue
    seen.add(clean_id)
    
    local_name = name if name.endswith(".mp4") else f"{name}.mp4"
    local_path = os.path.join(CLIPS_DIR, local_name)
    backup_id = backup_map.get(name) or backup_map.get(local_name)

    assets.append({
        "original_name": name,
        "local_name": local_name,
        "main_id": clean_id,
        "backup_id": backup_id,
        "local_path": local_path
    })

# Sort numerically by prefix
def sort_key(item):
    m = re.match(r"^(\d+)", item["local_name"])
    return int(m.group(1)) if m else 999

assets.sort(key=sort_key)
print(f"Total clips to download: {len(assets)}")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def is_valid_mp4(filepath):
    if not os.path.exists(filepath):
        return False
    if os.path.getsize(filepath) < 50000:
        return False
    try:
        with open(filepath, "rb") as f:
            header = f.read(64)
            # Check for ftyp box or general mp4 signature
            if b"ftyp" in header or b"moov" in header or b"\x00\x00\x00" in header[:4]:
                return True
            # Also check if it's an HTML error page
            if b"<!DOCTYPE" in header or b"<html" in header:
                return False
        return True
    except Exception:
        return False

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def try_download_stream(fid, target_path):
    urls = [
        f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
        f"https://drive.google.com/uc?export=download&id={fid}&confirm=t"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                ct = resp.headers.get("Content-Type", "")
                if "text/html" in ct:
                    data = resp.read()
                    m = re.search(rb'confirm=([a-zA-Z0-9_-]+)', data)
                    if m:
                        confirm_token = m.group(1).decode("utf-8")
                        url_confirm = f"https://drive.google.com/uc?export=download&id={fid}&confirm={confirm_token}"
                        req2 = urllib.request.Request(url_confirm, headers=headers)
                        with urllib.request.urlopen(req2, timeout=120) as resp2:
                            with open(target_path, "wb") as f:
                                while chunk := resp2.read(1024 * 1024):
                                    f.write(chunk)
                            if is_valid_mp4(target_path):
                                return True
                    continue
                with open(target_path, "wb") as f:
                    while chunk := resp.read(1024 * 1024):
                        f.write(chunk)
                if is_valid_mp4(target_path):
                    return True
        except Exception:
            pass
    return False

def download_asset(item):
    name = item["local_name"]
    target_path = item["local_path"]
    main_fid = item["main_id"]
    backup_fid = item["backup_id"]

    if is_valid_mp4(target_path):
        size = os.path.getsize(target_path)
        return {
            **item,
            "status": "exists",
            "size_bytes": size,
            "sha256": compute_sha256(target_path),
            "error": None
        }

    t0 = time.time()
    # Try main ID first
    ok = try_download_stream(main_fid, target_path)
    used_id = main_fid
    used_source = "main"

    if not ok and backup_fid:
        ok = try_download_stream(backup_fid, target_path)
        used_id = backup_fid
        used_source = "backup"

    elapsed = time.time() - t0
    if ok and is_valid_mp4(target_path):
        size = os.path.getsize(target_path)
        mb = size / (1024 * 1024)
        speed = mb / elapsed if elapsed > 0 else 0
        print(f"[DONE] {name} ({mb:.2f} MB in {elapsed:.1f}s from {used_source})", flush=True)
        return {
            **item,
            "status": "downloaded",
            "source_used": used_source,
            "used_id": used_id,
            "size_bytes": size,
            "sha256": compute_sha256(target_path),
            "download_time_sec": round(elapsed, 2),
            "error": None
        }
    else:
        if os.path.exists(target_path):
            try:
                os.remove(target_path)
            except Exception:
                pass
        print(f"[FAILED] {name} (Main ID: {main_fid}, Backup ID: {backup_fid})", flush=True)
        return {
            **item,
            "status": "failed",
            "size_bytes": 0,
            "sha256": None,
            "error": "Download failed or invalid MP4 format"
        }

def main():
    print(f"Starting parallel download of {len(assets)} clips with 8 workers...")
    t_start = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_asset, item): item for item in assets}
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=sort_key)
    elapsed_total = time.time() - t_start

    success_count = sum(1 for r in results if r["status"] in ["downloaded", "exists"])
    fail_count = sum(1 for r in results if r["status"] == "failed")
    total_bytes = sum(r["size_bytes"] for r in results)
    total_mb = total_bytes / (1024 * 1024)

    print("\n" + "="*60)
    print("DOWNLOAD REPORT: Roll Anime Girls")
    print(f"Total Items: {len(results)}")
    print(f"Success: {success_count} | Failed: {fail_count}")
    print(f"Total Size: {total_mb:.2f} MB")
    print(f"Total Time: {elapsed_total:.1f}s")
    print("="*60 + "\n")

    # Add game icon info
    icon_path = os.path.join(BRANDING_DIR, "roll_anime_girls_icon_512.png")
    branding_files = []
    if os.path.exists(icon_path):
        branding_files.append({
            "original_name": "Roll Anime Girls Official Icon (512x512)",
            "local_name": "roll_anime_girls_icon_512.png",
            "source": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=92289737492030",
            "local_path": icon_path,
            "size_bytes": os.path.getsize(icon_path),
            "sha256": compute_sha256(icon_path),
            "status": "downloaded"
        })

    manifest = {
        "campaign": "Roll Anime Girls",
        "campaign_slug": "roll_anime_girls",
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_doc_url": "https://docs.google.com/document/d/1RRD6Jmnc9YQBqprv3ipjZpt3c5hDmVAzh_-K8fZnKoM/edit?tab=t.0",
        "source_drive_folder": "https://drive.google.com/drive/folders/1Xi98KNF6BVtez7uGbfqUR_31iq9YPUYh",
        "backup_drive_folder": "https://drive.google.com/drive/folders/10SxlUCsJxiIV0A6U4n7egdvnBiANYj7T",
        "total_files_discovered": len(results) + len(branding_files),
        "total_successful": success_count + len(branding_files),
        "total_failed": fail_count,
        "total_size_mb": round(total_mb, 2),
        "clips": results,
        "branding": branding_files
    }

    manifest_path = os.path.join(BASE_DIR, "assets", "asset_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to {manifest_path}")

if __name__ == "__main__":
    main()
