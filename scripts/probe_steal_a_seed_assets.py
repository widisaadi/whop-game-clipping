import os
import subprocess
import json
import glob
import shutil

BASE_DIR = "campaigns/steal_a_seed"
RAW_DIR = os.path.join(BASE_DIR, "assets", "drive_raw")
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
REVIEW_DIR = os.path.join(BASE_DIR, "guide", "review")
MANIFEST_PATH = os.path.join(BASE_DIR, "assets", "asset_manifest.json")
CATALOG_PATH = os.path.join(BASE_DIR, "guide", "footage_catalog.json")

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

def probe_file(filepath):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", filepath
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return None
    return json.loads(res.stdout)

def process():
    mp4_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.mp4")))
    print(f"Found {len(mp4_files)} downloaded mp4 files in drive_raw.")

    catalog = {}
    manifest = {
        "campaign": "Steal a Seed",
        "game_link": "https://www.roblox.com/games/122216176958450/Steal-A-Seed",
        "drive_folder": "https://drive.google.com/drive/folders/1LOLq4VNqOwca9HGmDe7w_PWhnPryRkeG",
        "total_clips_detected": 50,
        "branding_files": 1,
        "clips": []
    }

    for src_path in mp4_files:
        fname = os.path.basename(src_path)
        dest_path = os.path.join(CLIPS_DIR, fname)
        
        # Copy to clips if not exists
        if not os.path.exists(dest_path) or os.path.getsize(dest_path) != os.path.getsize(src_path):
            shutil.copy2(src_path, dest_path)

        # Generate contact sheet
        review_img = os.path.join(REVIEW_DIR, f"{os.path.splitext(fname)[0]}_review.jpg")
        if not os.path.exists(review_img):
            cmd = [
                "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
                dest_path, "--tiles", "3x2", "-o", review_img, "--overwrite"
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Generated review contact sheet: {review_img}")

        info = probe_file(dest_path)
        if not info:
            continue

        v_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
        a_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), {})
        fmt = info.get("format", {})

        dur = float(fmt.get("duration", 0.0))
        w = int(v_stream.get("width", 0))
        h = int(v_stream.get("height", 0))
        fps_eval = v_stream.get("r_frame_rate", "30/1")
        try:
            num, den = map(int, fps_eval.split("/"))
            fps = round(num / den, 2)
        except Exception:
            fps = 30.0

        catalog[fname] = {
            "path": dest_path.replace("\\", "/"),
            "duration": round(dur, 2),
            "resolution": f"{w}x{h}",
            "fps": fps,
            "has_audio": bool(a_stream),
            "review_image": review_img.replace("\\", "/")
        }

        manifest["clips"].append({
            "name": fname,
            "size_bytes": os.path.getsize(dest_path),
            "duration": round(dur, 2),
            "resolution": f"{w}x{h}"
        })

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Updated catalog ({len(catalog)} clips) and manifest.")

if __name__ == "__main__":
    process()
