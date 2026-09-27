"""
Download default background music for Whop Game Clipping pipeline.
Default track: "Sneaky Snitch" by Kevin MacLeod (Incompetech)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
"""

import sys
import urllib.request
from pathlib import Path

DEFAULT_BGM_URL = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Sneaky%20Snitch.mp3"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
TARGET_FILE = ASSETS_DIR / "bgm.mp3"


def download_bgm(force: bool = False) -> Path:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if TARGET_FILE.exists() and not force:
        print(f"[OK] Default BGM already exists: {TARGET_FILE}")
        return TARGET_FILE

    print(f"[*] Downloading default BGM (Kevin MacLeod - Sneaky Snitch)...")
    print(f"[*] Source: {DEFAULT_BGM_URL}")

    headers = {"User-Agent": "WhopGameClipping/1.0"}
    req = urllib.request.Request(DEFAULT_BGM_URL, headers=headers)

    with urllib.request.urlopen(req) as resp, open(TARGET_FILE, "wb") as f:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 64 * 1024

        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                percent = (downloaded / total) * 100
                sys.stdout.write(f"\r    Downloading: {percent:.1f}% ({downloaded // 1024} KB / {total // 1024} KB)")
                sys.stdout.flush()

    print(f"\n[SUCCESS] Default BGM saved to: {TARGET_FILE}")
    return TARGET_FILE


if __name__ == "__main__":
    force_download = "--force" in sys.argv
    download_bgm(force=force_download)
