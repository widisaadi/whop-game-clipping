import os
import subprocess
import json
import glob
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = "campaigns/roll_anime_girls"
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
REVIEW_DIR = os.path.join(BASE_DIR, "guide", "review")
CATALOG_PATH = os.path.join(BASE_DIR, "guide", "footage_catalog.json")

os.makedirs(REVIEW_DIR, exist_ok=True)

def probe_file(filepath):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", filepath
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except Exception:
        return None

def make_contact_sheet(dest_path, review_img):
    if os.path.exists(review_img) and os.path.getsize(review_img) > 10000:
        return
    # Use look.py if available, or direct ffmpeg thumbnail grid
    cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        dest_path, "--tiles", "3x2", "-o", review_img, "--overwrite"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 or not os.path.exists(review_img):
        # Fallback to direct ffmpeg tile
        ff_cmd = [
            "ffmpeg", "-y", "-i", dest_path,
            "-vf", "select='not(mod(n\\,max(1\\,trunc(n_frames/6))))',scale=360:-1,tile=3x2",
            "-frames:v", "1", "-q:v", "3", review_img
        ]
        subprocess.run(ff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_single_clip(src_path):
    fname = os.path.basename(src_path)
    base_name = os.path.splitext(fname)[0]
    review_img = os.path.join(REVIEW_DIR, f"{base_name}_review.jpg")

    make_contact_sheet(src_path, review_img)
    info = probe_file(src_path)
    if not info:
        return fname, None

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

    return fname, {
        "file": fname,
        "path": src_path.replace("\\", "/"),
        "duration": round(dur, 2),
        "resolution": f"{w}x{h}",
        "width": w,
        "height": h,
        "fps": fps,
        "has_audio": bool(a_stream),
        "review_image": review_img.replace("\\", "/"),
        "size_mb": round(os.path.getsize(src_path) / (1024 * 1024), 2)
    }

def main():
    clips = sorted(glob.glob(os.path.join(CLIPS_DIR, "*.mp4")))
    print(f"Probing and creating contact sheets for {len(clips)} clips...")

    catalog = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(process_single_clip, clips)
        for fname, data in results:
            if data:
                catalog[fname] = data

    # Sort catalog numerically
    import re
    def num_key(k):
        m = re.match(r"^(\d+)", k)
        return int(m.group(1)) if m else 999
    
    sorted_catalog = {k: catalog[k] for k in sorted(catalog.keys(), key=num_key)}

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_catalog, f, indent=2)

    print(f"\nSuccessfully probed and cataloged {len(sorted_catalog)} clips -> {CATALOG_PATH}")

if __name__ == "__main__":
    main()
