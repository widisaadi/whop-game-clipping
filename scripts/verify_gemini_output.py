import os
import subprocess

def main():
    os.makedirs("output/qa_achird_frames", exist_ok=True)
    video = "output/how_to_fisch_gemini_achird.mp4"
    if not os.path.exists(video):
        print(f"Video {video} not found yet.")
        return

    timestamps = [
        ("00:00:02.000", "hook_text"),
        ("00:00:05.300", "how_to_fisch_gold"),
        ("00:00:12.500", "gameplay_shrimp"),
        ("00:00:21.500", "spider_crab_red"),
        ("00:00:28.200", "endcard_cta_pos"),
        ("00:00:31.000", "endcard_clean_icon")
    ]

    for ts, name in timestamps:
        out_img = f"output/qa_achird_frames/{name}.jpg"
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
