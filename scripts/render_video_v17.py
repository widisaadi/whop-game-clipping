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

VID_ID = "17_tongue_escape_puck_formula"

SEGMENTS = [
    # 00: Hook Intro (0.00s - 2.06s) - Speed skater kinetic trap
    ("shared/hooks/INTRO.mp4", 0.00, 2.06, "intro_clip"),
    # 01: Spitting glowing tongue (2.06s - 3.40s) - "absurd Roblox game"
    ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 0.00, 1.34, "blurred_bg"),
    # 02: Island stage overview (3.40s - 5.46s) - "escape the island"
    ("campaigns/tongue_escape/assets/clips/04_Clip 4 (1).mp4", 1.00, 2.06, "blurred_bg"),
    # 03: Tongue grappling pillars (5.46s - 7.68s) - "only thing you can use is your own tongue"
    ("campaigns/tongue_escape/assets/clips/09_Clip 9.mp4", 3.00, 2.22, "blurred_bg"),
    # 04: Gym treadmill training (7.68s - 10.00s) - "train your tongue to get super long"
    ("campaigns/tongue_escape/assets/clips/03_Clip 3 (2).mp4", 0.00, 2.32, "blurred_bg"),
    # 05: Lava gap jump swing (10.00s - 11.82s) - "swing across crazy obstacles"
    ("campaigns/tongue_escape/assets/clips/02_Clip 2 (2).mp4", 7.00, 1.82, "blurred_bg"),
    # 06: Leaderboard & chest unlocks (11.82s - 14.60s) - "unlock weirder tongues"
    ("campaigns/tongue_escape/assets/clips/10_Clip 10.mp4", 0.50, 2.78, "blurred_bg"),
    # 07: Flying tongue sky soaring (14.60s - 17.28s) - "tongue that lets you fly"
    ("campaigns/tongue_escape/assets/clips/11_Clip 11.mp4", 2.00, 2.68, "blurred_bg"),
    # 08: Official game card reveal (17.28s - 19.94s) - "The game is called Plus One Tongue Escape"
    ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 10.00, 2.66, "game_card_overlay"),
    # 09: Live code redemption (19.94s - 23.58s) - "use code BONUS500 to grab 10,000 free tongue power"
    ("campaigns/tongue_escape/assets/clips/02_Clip 2.mp4", 3.50, 3.64, "blurred_bg"),
]

def render_video():
    base_dir = "campaigns/tongue_escape"
    temp_dir = "temp/tongue_escape"
    seg_dir = os.path.join(temp_dir, "segments_v17")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_v17_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_v17.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_tongue_escape_v17.ass")
    card_overlay = os.path.join(temp_dir, "game_card_overlay_v17.png")

    total_dur = sum(s[2] for s in SEGMENTS)
    print(f"\n=======================================================")
    print(f"RENDERING {VID_ID} (Duration: {total_dur:.2f}s, Voice: Puck, Formula Benchmark)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_v17.txt")
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(SEGMENTS):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            
            if otype == "game_card_overlay":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-i", card_overlay,
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[bg][1:v]overlay=0:0,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            elif otype == "intro_clip":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
                    "-af", "volume=0.10,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            else:
                # Ambient blurred backdrop: 1:1 square sharp gameplay centered in 1080x1920 blurred canvas
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-filter_complex",
                    "[0:v]split[fg_raw][bg_raw];"
                    "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[fg_raw]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080:(in_w-out_w)/2:(in_h-out_h)/2[fg];"
                    "[bg][fg]overlay=0:420,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            
            if os.path.exists(seg_out) and os.path.getsize(seg_out) > 10000:
                print(f"Segment {idx+1}/{len(SEGMENTS)} already exists, skipping re-encode.")
            else:
                run_cmd(cmd, f"Rendering Segment {idx+1}/{len(SEGMENTS)} ({dur:.2f}s, type: {otype})")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate segments
    raw_video = os.path.join(temp_dir, "raw_concatenated_v17.mp4")
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments into raw_concatenated_v17.mp4")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "tongue_escape_master_v17.mp4")
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
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.22,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
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
    run_cmd(mix_cmd, f"Mixing Master {VID_ID} with Voice Puck, BGM3 & Kinetic Center Subtitles (Y=1180)")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, f"{VID_ID}.mp4")
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, f"Applying 2-Pass Loudness Normalization (-14.0 LUFS) to {VID_ID}")

    # Retag Color Space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    retagged_file = os.path.join(out_dir, f"{VID_ID}_retag.mp4")
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # Visual Contact Sheet
    sheet_output = os.path.join(out_dir, f"{VID_ID}_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating Visual Contact Sheet for {VID_ID}")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"VIDEO 17 COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================\n")
    return final_output

if __name__ == "__main__":
    render_video()
