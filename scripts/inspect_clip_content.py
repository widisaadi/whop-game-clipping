import os
import subprocess

clips = [
    "01_Clip 1 (2).mp4",
    "02_Clip 2 (2).mp4",
    "03_Clip 3 (2).mp4",
    "04_Clip 4 (1).mp4",
    "04_Clip 4 (2).mp4",
    "04_Clip 4.mp4",
    "09_Clip 9.mp4",
    "10_Clip 10.mp4",
    "11_Clip 11.mp4",
    "12_Clip 12.mp4",
    "13_Clip 13.mp4",
    "14_Clip 14.mp4",
    "15_Clip 15.mp4"
]

out_dir = "temp/tongue_escape/clip_sheets"
os.makedirs(out_dir, exist_ok=True)

for clip in clips:
    path = os.path.join("campaigns/tongue_escape/assets/clips", clip)
    if not os.path.exists(path):
        continue
    sheet_path = os.path.join(out_dir, f"{os.path.splitext(clip)[0]}_sheet.jpg")
    cmd = [
        "ffmpeg", "-y", "-i", path,
        "-vf", "select=not(mod(n\,60)),scale=480:-1,tile=3x3",
        "-frames:v", "1", "-q:v", "3",
        sheet_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Generated sheet for {clip} -> {sheet_path}")
