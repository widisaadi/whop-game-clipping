import os
import subprocess

def main():
    os.makedirs("output/qa_cinematic_frames", exist_ok=True)
    video = "output/how_to_fisch_bang_motion.mp4"
    if not os.path.exists(video):
        print(f"Video {video} not found yet.")
        return

    timestamps = [
        ("00:00:02.000", "01_hook_question"),
        ("00:00:05.300", "02_intro_icon_badge"),
        ("00:00:12.500", "03_floppy_shrimp"),
        ("00:00:21.500", "04_spider_crab_boss"),
        ("00:00:28.500", "05_blurred_endcard_subtitles"),
        ("00:00:31.200", "06_blurred_endcard_clean")
    ]

    for ts, name in timestamps:
        out_img = f"output/qa_cinematic_frames/{name}.jpg"
        cmd = [
            "ffmpeg", "-y",
            "-ss", ts,
            "-i", video,
            "-vframes", "1",
            "-q:v", "2",
            out_img
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(out_img):
            print(f"Extracted QA frame: {out_img}")

if __name__ == "__main__":
    main()
