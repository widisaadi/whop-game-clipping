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
    base_dir = "campaigns/money_roll"
    temp_dir = "temp/money_roll"
    seg_dir = os.path.join(temp_dir, "segments_tailored")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_v01_tailored.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_tailored.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_money_roll_tailored.ass")

    # 8 segments totaling exactly 19.50 seconds (100% Fortnite Native - Zero Roblox Artifacts!)
    segments = [
        # 01: High-impact opening: Giant golden money ball rolling with dollar signs flying (2.20s)
        ("campaigns/money_roll/assets/clips/02_Clip 2.mp4", 0.00, 2.20, "blurred_bg"),
        # 02: High-speed cash generation & rolling multiplier (2.30s)
        ("campaigns/money_roll/assets/clips/01_Clip 1_1DFmI2j.mp4", 2.00, 2.30, "blurred_bg"),
        # 03: Hatching pets & Golden Machine multipliers (2.30s)
        ("campaigns/money_roll/assets/clips/08_Clip 8.mp4", 0.00, 2.30, "blurred_bg"),
        # 04: Speed training on gym treadmills (2.20s)
        ("campaigns/money_roll/assets/clips/05_Clip 5 (1).mp4", 1.00, 2.20, "blurred_bg"),
        # 05: Level up! 68 -> 69 & unlocking cash stands with giant pink sphere (2.20s)
        ("campaigns/money_roll/assets/clips/11_Clip 11.mp4", 0.50, 2.20, "blurred_bg"),
        # 06: Stage 4: Rolling across narrow golden bridge over deadly boiling lava (2.30s)
        ("campaigns/money_roll/assets/clips/05_Clip 5.mp4", 0.00, 2.30, "blurred_bg"),
        # 07: Stage 6: 6.27M cash flex & richest player progression (2.10s)
        ("campaigns/money_roll/assets/clips/18_Clip 18.mp4", 1.00, 2.10, "blurred_bg"),
        # 08: Fortnite Living Endcard with Island Image, Title, Code & CTA (3.90s)
        ("campaigns/money_roll/assets/clips/02_Clip 2.mp4", 5.00, 3.90, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"\n=======================================================")
    print(f"RENDERING TAILORED FORTNITE VIDEO (+1 MONEY ROLL)")
    print(f"Total Duration: {total_dur:.2f}s (Target: 19.50s)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_tailored.txt")
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
                    "-i", "temp/money_roll/endcard_frames/endcard_%03d.png",
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=26:6,eq=brightness=-0.26:contrast=1.12[bg];"
                    "[bg][1:v]overlay=0:0,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            else:
                # Blurred backdrop framing: 1:1 sharp square gameplay centered in 1080x1920 blurred canvas
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
            
            run_cmd(cmd, f"Rendering Segment {idx+1}/{len(segments)} ({dur:.2f}s, type: {otype})")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate all 8 segments
    raw_video = os.path.join(temp_dir, "raw_concatenated_tailored.mp4")
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments into raw_concatenated_tailored.mp4")

    # Burn subtitles and mix audio: Game Audio + Fast VO Aoede + BGM2 + SFX Track
    temp_master = os.path.join(temp_dir, "money_roll_master_tailored.mp4")
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
        "-i", "assets/bgm2.mpeg",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.24,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
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
    run_cmd(mix_cmd, "Mixing Master with Tailored VO Aoede, BGM2 & Kinetic Subtitles (Y=1180)")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, "01_money_roll_craziest_fortnite_map.mp4")
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
    retagged_file = os.path.join(out_dir, "01_money_roll_craziest_fortnite_map_retag.mp4")
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # Visual Contact Sheet
    sheet_output = os.path.join(out_dir, "01_money_roll_craziest_fortnite_map_sheet.png")
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
    print(f"TAILORED VIDEO 01 COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
