import os
import subprocess
import sys
import shutil

def run_cmd(cmd, desc):
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"ERROR in {desc}:")
        print(res.stderr[-800:])
        sys.exit(1)
    return res

def remux_video(v_num, title_tag, raw_video, vox_wav, sfx_wav, ass_file, duration, bgm_fade_start, final_output):
    print(f"\n==================================================================")
    print(f"RE-MIXING & MASTERING VIDEO {v_num} WITH BGM2 ({title_tag})")
    print(f"==================================================================")
    
    temp_master = f"temp/how_to_fisch_{v_num}_bgm2_raw.mp4"
    ass_path = os.path.abspath(ass_file).replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    # Mix 4 audio streams:
    # [0:a] Game audio: 0.18
    # [1:a] Voiceover: 1.40 (punchy, clear, pop up)
    # [2:a] BGM2: 0.24 (-4 dB gain reduction from 0.38, perfectly balanced)
    # [3:a] SFX: 0.95
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", vox_wav,
        "-i", "assets/bgm2.mpeg",
        "-i", sfx_wav,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.40[a_vox];"
        f"[2:a]volume=0.24,afade=t=out:st={bgm_fade_start:.2f}:d=2.0[a_bgm];"
        f"[3:a]volume=0.95[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{duration:.2f}",
        temp_master
    ]
    run_cmd(mix_cmd, f"Rendering Master {v_num} with BGM2 & Subtitles")

    # Loudness Normalization via ffmpeg-skill (-14 LUFS, TP <= -1.5 dBTP)
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, f"Loudness Normalization (-14.0 LUFS) for Video {v_num}")

    # Retag BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, f"Retagging BT.709 for Video {v_num}")
    retagged_file = final_output.replace(".mp4", "_retag.mp4")
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # Verify TikTok/Reels specs via check.py
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    res_check = run_cmd(check_cmd, f"Platform Compliance Check for Video {v_num}")
    print(res_check.stdout)

    # Generate Visual Contact Sheet
    sheet_output = final_output.replace(".mp4", "_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating Contact Sheet for Video {v_num}")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"SUCCESS: Video {v_num} rendered -> {final_output} ({file_size_mb:.2f} MB)")

def main():
    # Video 05
    remux_video(
        v_num="05",
        title_tag="FPS + Fishing Hybrid",
        raw_video="temp/raw_concatenated_v9.mp4",
        vox_wav="temp/voiceover_v9_fast.wav",
        sfx_wav="temp/sfx_track_v9.wav",
        ass_file="campaigns/how_to_fisch/subtitles/captions_v9.ass",
        duration=40.73,
        bgm_fade_start=38.73,
        final_output="campaigns/how_to_fisch/output/05_how_to_fisch_fps_fishing.mp4"
    )

    # Video 06
    remux_video(
        v_num="06",
        title_tag="Weirdest Game Discovery",
        raw_video="temp/raw_concatenated_v10.mp4",
        vox_wav="temp/voiceover_v10_fast.wav",
        sfx_wav="temp/sfx_track_v10.wav",
        ass_file="campaigns/how_to_fisch/subtitles/captions_v10.ass",
        duration=31.99,
        bgm_fade_start=29.99,
        final_output="campaigns/how_to_fisch/output/06_how_to_fisch_weirdest_game.mp4"
    )

    # Video 07
    remux_video(
        v_num="07",
        title_tag="Fight to Survive Mode",
        raw_video="temp/raw_concatenated_v11.mp4",
        vox_wav="temp/voiceover_v11_fast.wav",
        sfx_wav="temp/sfx_track_v11.wav",
        ass_file="campaigns/how_to_fisch/subtitles/captions_v11.ass",
        duration=35.37,
        bgm_fade_start=33.37,
        final_output="campaigns/how_to_fisch/output/07_how_to_fisch_fight_to_survive.mp4"
    )

    print("\n==================================================================")
    print("ALL 3 VIDEOS (05, 06, 07) RE-MASTERED WITH BGM2 SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    main()
