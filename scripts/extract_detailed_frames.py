import os
import subprocess

def extract_keyframes(clip_rel, start_sec, count, interval, prefix):
    out_dir = f"temp/tongue_escape/verify_frames/{prefix}"
    os.makedirs(out_dir, exist_ok=True)
    clip_path = os.path.join("campaigns/tongue_escape/assets/clips", clip_rel)
    for i in range(count):
        t = start_sec + i * interval
        out_jpg = os.path.join(out_dir, f"frame_{i:02d}_{t:.2f}s.jpg")
        cmd = [
            "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", clip_path,
            "-vframes", "1", "-q:v", "3", out_jpg
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Extracted {count} frames for {clip_rel} -> {out_dir}")

# 1. Floating island & stage 1 in 02_Clip 2 (2).mp4
extract_keyframes("02_Clip 2 (2).mp4", 0.0, 8, 1.0, "clip02_island")

# 2. Spitting tongue in 02_Clip 2 (2).mp4
extract_keyframes("02_Clip 2 (2).mp4", 3.0, 6, 0.5, "clip02_spit")

# 3. Treadmill in 04_Clip 4 (1).mp4
extract_keyframes("04_Clip 4 (1).mp4", 0.0, 6, 0.5, "clip04_treadmill")

# 4. Giant chasm in 09_Clip 9.mp4
extract_keyframes("09_Clip 9.mp4", 2.0, 6, 0.5, "clip09_chasm")

# 5. Laser walls in 15_Clip 15.mp4
extract_keyframes("15_Clip 15.mp4", 0.0, 8, 0.5, "clip15_laser")
