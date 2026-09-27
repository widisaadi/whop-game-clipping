import os
import subprocess
import sys
import shutil

def run_cmd(cmd, desc):
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"ERROR in {desc}:")
        print(res.stderr[-1000:])
        sys.exit(1)
    return res

def mix_master():
    vid_id = "01_steal_a_seed_ultimate_heist"
    base_dir = "campaigns/steal_a_seed"
    temp_dir = "temp/steal_a_seed"
    out_dir = os.path.join(base_dir, "output")
    os.makedirs(out_dir, exist_ok=True)

    raw_video = os.path.join(temp_dir, "raw_concatenated_sas_01.mp4")
    vo_path = os.path.join(temp_dir, "voiceover_sas_01_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_sas_01.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_steal_a_seed_01.ass")
    temp_master = os.path.join(temp_dir, "master_sas_01.mp4")
    total_dur = 24.65

    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    fade_st = max(0.0, total_dur - 1.9)
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", vo_path,
        "-i", "assets/bgm3.mp3",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.35,volume=4dB[a_vox];"
        f"[2:a]volume=0.22,volume=-5dB,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
        f"[3:a]volume=0.90[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{total_dur:.2f}",
        temp_master
    ]
    run_cmd(mix_cmd, "Re-mixing Master with clean ASS subtitles and exact audio balance")

    final_output = os.path.join(out_dir, f"{vid_id}.mp4")
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, f"Applying 2-Pass Loudness Normalization (-14.0 LUFS) to {vid_id}")

    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, f"Retagging color space to BT.709 for {vid_id}")
    retagged_file = os.path.join(out_dir, f"{vid_id}_retag.mp4")
    if os.path.exists(retagged_file):
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.replace(retagged_file, final_output)
        except Exception as e:
            print(f"Warning moving retagged file: {e}")
            if not os.path.exists(final_output):
                shutil.copy2(retagged_file, final_output)

    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating Visual Contact Sheet for {vid_id}")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"RE-RENDER COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================\n")

if __name__ == "__main__":
    mix_master()
