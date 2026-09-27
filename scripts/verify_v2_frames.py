import os
import subprocess

def extract_frame(video_path, timestamp, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(timestamp),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Extracted QA frame: {output_path}")

def main():
    video = "output/how_to_fisch_combat_bosses.mp4"
    if not os.path.exists(video):
        print(f"Video not found: {video}")
        return

    frames = [
        (1.8, "output/qa_v2_frames/01_hook_guns.jpg"),
        (4.5, "output/qa_v2_frames/02_intro_badge.jpg"),
        (8.5, "output/qa_v2_frames/03_weapons_rod.jpg"),
        (13.2, "output/qa_v2_frames/04_mutant_beasts.jpg"),
        (18.5, "output/qa_v2_frames/05_sun_fish_boss.jpg"),
        (22.0, "output/qa_v2_frames/06_piranha_boss.jpg"),
        (25.5, "output/qa_v2_frames/07_blurred_endcard_cta.jpg")
    ]

    for ts, out in frames:
        extract_frame(video, ts, out)

if __name__ == "__main__":
    main()
