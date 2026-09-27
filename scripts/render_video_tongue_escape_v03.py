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

def main():
    base_dir = "campaigns/tongue_escape"
    temp_dir = "temp/tongue_escape"
    seg_dir = os.path.join(temp_dir, "segments_v03")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_v03.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_v03.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_tongue_escape_v03.ass")

    # 10 ultra fast-paced segments totaling exactly 23.50 seconds
    segments = [
        # 01: Shocked avatar hook (0.00s - 1.30s = 1.30s)
        ("shared/hooks/INTRO.mp4", 0.00, 1.30, "intro_clip"),
        # 02: Spitting 4K tongue bridge (1.30s - 2.80s = 1.50s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 0.00, 1.50, "none"),
        # 03: Codes menu open (2.80s - 4.80s = 2.00s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1.mp4", 0.50, 2.00, "none"),
        # 04: Rainbow & Hacker x99 electric treadmills (4.80s - 6.80s = 2.00s)
        ("campaigns/tongue_escape/assets/clips/03_Clip 3 (2).mp4", 0.00, 2.00, "none"),
        # 05: Code WELCOME1 claim & +5,000 studs popup (6.80s - 10.10s = 3.30s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1.mp4", 6.50, 3.30, "none"),
        # 06: Code BONUS500 claim & +10,000 studs popup (10.10s - 12.50s = 2.40s)
        ("campaigns/tongue_escape/assets/clips/02_Clip 2.mp4", 4.00, 2.40, "none"),
        # 07: Code FREEBOOST claim & 2x Boost 30m popup (12.50s - 15.10s = 2.60s)
        ("campaigns/tongue_escape/assets/clips/03_Clip 3.mp4", 4.50, 2.60, "none"),
        # 08: Soaring across giant lava chasm 4K (15.10s - 17.70s = 2.60s)
        ("campaigns/tongue_escape/assets/clips/02_Clip 2 (2).mp4", 7.00, 2.60, "none"),
        # 09: Stage 7 +100 Wins pad touchdown (17.70s - 19.60s = 1.90s)
        ("campaigns/tongue_escape/assets/clips/10_Clip 10.mp4", 9.50, 1.90, "none"),
        # 10: Living Endcard with Title, Card, and No-Bg LINK IN BIO (19.60s - 23.50s = 3.90s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 10.00, 3.90, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 23.50s)")

    concat_list_path = os.path.join(temp_dir, "concat_list_v03.txt")
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            
            if otype == "endcard_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-framerate", "30",
                    "-i", "temp/tongue_escape/endcard_frames_v03/endcard_%03d.png",
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=26:6,eq=brightness=-0.26:contrast=1.12[bg];"
                    "[bg][1:v]overlay=0:0[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            elif otype == "intro_clip":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30",
                    "-af", "volume=0.10,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-vf", "crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30",
                    "-af", "volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            
            if not os.path.exists(seg_out) or os.path.getsize(seg_out) < 10000:
                run_cmd(cmd, f"Rendering Segment {idx+1}/{len(segments)} ({dur:.2f}s, type: {otype})")
            else:
                print(f"--> Segment {idx+1}/{len(segments)} already exists, skipping...")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate all 10 segments
    raw_video = os.path.join(temp_dir, "raw_concatenated_v03.mp4")
    if not os.path.exists(raw_video) or os.path.getsize(raw_video) < 10000:
        concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
        run_cmd(concat_cmd, "Concatenating segments into raw_concatenated_v03.mp4")
    else:
        print("--> Raw concatenated video already exists, skipping...")

    # Burn subtitles and mix audio: Game Audio + Fast VO Aoede + BGM2 + SFX Track
    temp_master = os.path.join(temp_dir, "tongue_escape_master_v03.mp4")
    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", vo_path,
        "-i", "assets/bgm2.mpeg",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.24,afade=t=out:st=21.5:d=2.0[a_bgm];"
        f"[3:a]volume=0.90[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{total_dur:.2f}",
        temp_master
    ]
    run_cmd(mix_cmd, "Mixing Master with Fast VO Aoede, BGM2 & Center+15px Subtitles")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, "03_tongue_escape_secret_codes.mp4")
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying 2-Pass Loudness Normalization (-14.0 LUFS)")

    # Retag Color Space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    retagged_file = os.path.join(out_dir, "03_tongue_escape_secret_codes_retag.mp4")
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # Platform compliance check
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    res_check = run_cmd(check_cmd, "Verifying TikTok/Reels platform compliance")
    print(res_check.stdout)

    # Visual Contact Sheet
    sheet_output = os.path.join(out_dir, "03_tongue_escape_secret_codes_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, "Generating Visual Contact Sheet")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"VIDEO 03 (SECRET CODES) COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
