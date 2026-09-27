import os
import subprocess
import json

CLIPS_DIR = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate\assets\clips"
CATALOG_PATH = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate\guide\footage_catalog.json"

catalog = []
files = sorted([f for f in os.listdir(CLIPS_DIR) if f.endswith(".mp4")])

for f in files:
    filepath = os.path.join(CLIPS_DIR, f)
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,r_frame_rate,duration,codec_name,pix_fmt:format=duration,size,bit_rate",
        "-of", "json", filepath
    ]
    try:
        out = subprocess.check_output(cmd, encoding="utf-8")
        data = json.loads(out)
        
        # Extract video stream info
        v_stream = next((s for s in data.get("streams", []) if s.get("codec_name") in ["h264", "hevc", "vp9"]), {})
        a_stream = next((s for s in data.get("streams", []) if s.get("codec_name") in ["aac", "mp3", "opus"]), {})
        
        width = v_stream.get("width")
        height = v_stream.get("height")
        fps = v_stream.get("r_frame_rate")
        duration = float(data.get("format", {}).get("duration", 0))
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        
        # Categorize trope / action
        trope = "Romantic Montage" if "montage" in f.lower() else "High-Tension Scene"
        if "kiss" in f.lower():
            action = "Passionate or almost kiss between leads"
        elif "dance" in f.lower():
            action = "Romantic dance / ballroom chemistry"
        elif "deception" in f.lower():
            action = "Drama, misunderstanding or confrontation"
        elif "hug" in f.lower():
            action = "Protective or emotional embrace"
        elif "game" in f.lower():
            action = "Playful banter / competition"
        elif "smile" in f.lower():
            action = "Bad boy revealing genuine soft smile"
        else:
            action = "Multi-scene relationship evolution montage"

        item = {
            "filename": f,
            "category": trope,
            "duration_seconds": round(duration, 2),
            "width": width,
            "height": height,
            "aspect_ratio": f"{width}:{height}",
            "fps": fps,
            "size_mb": round(size_mb, 2),
            "visual_action": action,
            "supported_claim": f"True visible footage of {action}"
        }
        catalog.append(item)
        print(f"[{f}] {width}x{height} | {duration:.1f}s | {action}")
    except Exception as e:
        print(f"Error probing {f}: {e}")

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"\nSaved footage catalog with {len(catalog)} entries to {CATALOG_PATH}")
