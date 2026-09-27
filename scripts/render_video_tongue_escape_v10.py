import os
import subprocess
import sys

def run_cmd(cmd, desc):
    print(f"\n--- {desc} ---")
    print(" ".join(cmd) if isinstance(cmd, list) else cmd)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        print("STDERR:\n" + res.stderr[-1000:])
        sys.exit(1)
    print(f"SUCCESS: {desc}")
    return res

def main():
    base_dir = os.path.abspath(".")
    temp_dir = os.path.join(base_dir, "temp", "tongue_escape_v10")
    seg_dir = os.path.join(temp_dir, "segments")
    out_dir = os.path.join(base_dir, "campaigns", "tongue_escape", "output")
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(base_dir, "temp", "tongue_escape", "voiceover_v10.wav")
    sfx_track = os.path.join(base_dir, "temp", "tongue_escape", "sfx_track_v10.wav")
    ass_path = os.path.join(base_dir, "campaigns", "tongue_escape", "subtitles", "captions_tongue_escape_v10.ass")
    endcard_frames_pattern = os.path.join(base_dir, "temp", "tongue_escape", "endcard_frames_v03", "endcard_%03d.png")

    # Segments Definition (Total 24.50 seconds / 735 frames @ 30fps)
    segments = [
        # (source, start_sec, duration_sec, type)
        ("shared/hooks/INTRO.mp4", 0.00, 1.20, "intro_clip"),
        ("campaigns/tongue_escape/assets/clips/04_Clip 4.mp4", 0.80, 3.00, "gameplay"),      # Crushing walls
        ("campaigns/tongue_escape/assets/clips/03_Clip 3 (2).mp4", 1.50, 3.80, "gameplay"),  # Gym Rainbow x30 trainer
        ("campaigns/tongue_escape/assets/clips/04_Clip 4.mp4", 2.50, 3.20, "gameplay"),      # Shooting tongue through closing trap
        ("campaigns/tongue_escape/assets/clips/10_Clip 10.mp4", 2.50, 3.80, "gameplay"),     # Supersonic canyon slide
        ("campaigns/tongue_escape/assets/clips/10_Clip 10.mp4", 8.00, 3.00, "gameplay"),     # Stage 7 +100 Wins landing
        ("campaigns/tongue_escape/assets/clips/07_Clip 7.mp4", 1.50, 2.30, "gameplay"),      # Golden halo avatar celebration
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 20.00, 4.20, "endcard_anim") # Living Endcard
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 24.50s)")

    concat_list_path = os.path.join(temp_dir, "concat_list_v10.txt")
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
                    "-i", endcard_frames_pattern.replace("\\", "/"),
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
            
            run_cmd(cmd, f"Rendering Segment {idx:02d} ({otype}, {dur:.2f}s)")
            seg_out_clean = seg_out.replace('\\', '/')
            clist.write(f"file '{seg_out_clean}'\n")

    # Concatenate Segments
    raw_video = os.path.join(temp_dir, "raw_concatenated_v10.mp4")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        raw_video
    ]
    run_cmd(concat_cmd, "Concatenating Segments")

    # Burn-in Subtitles & Mix Audio (VO + BGM2 + SFX + Gameplay)
    temp_master = os.path.join(temp_dir, "master_unnormalized_v10.mp4")
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
        f"[2:a]volume=0.24,afade=t=out:st=22.5:d=1.9[a_bgm];"
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
    run_cmd(mix_cmd, "Mixing Master with Fast VO Aoede, BGM2 & Center Subtitles (Y=1180)")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, "10_tongue_escape_crushing_walls.mp4")
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
    retagged_file = os.path.join(out_dir, "10_tongue_escape_crushing_walls_retag.mp4")
    if os.path.exists(retagged_file):
        os.replace(retagged_file, final_output)

    # Compliance Check
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--target", "tiktok"
    ]
    run_cmd(check_cmd, "Verifying TikTok / Shorts / Reels Compliance")

    # Generate 3x2 Contact Sheet
    sheet_output = os.path.join(out_dir, "10_tongue_escape_crushing_walls_sheet.png")
    sheet_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/contact_sheet.py",
        final_output,
        "-o", sheet_output,
        "--grid", "3x2",
        "--overwrite"
    ]
    run_cmd(sheet_cmd, "Generating 3x2 Visual Contact Sheet")

    print(f"\n==========================================")
    print(f"🎬 Video 10 Rendered Successfully!")
    print(f"File: {final_output}")
    print(f"Size: {os.path.getsize(final_output)} bytes")
    print(f"Sheet: {sheet_output}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
