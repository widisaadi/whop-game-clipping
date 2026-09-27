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
    seg_dir = os.path.join(temp_dir, "segments")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_raw.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_tongue_escape.ass")
    intro_badge = os.path.join(temp_dir, "intro_badge.png")

    if not os.path.exists(vo_path):
        from scripts.generate_gemini_voice_tongue_escape import generate_voice
        generate_voice()

    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_tongue_escape import build_sfx_track
        build_sfx_track()

    if not os.path.exists(ass_path):
        from scripts.build_subtitles_tongue_escape import main as gen_subs
        gen_subs()

    if not os.path.exists(intro_badge) or not os.path.exists(os.path.join(temp_dir, "endcard_frames")):
        from scripts.create_tongue_escape_overlays import create_intro_badge, create_endcard_frames
        create_intro_badge()
        create_endcard_frames()

    # 10 segments matching 44.24 seconds
    segments = [
        # 01: Avatar Shock Hook (0.00s - 2.50s = 2.50s)
        ("shared/hooks/INTRO.mp4", 0.00, 2.50, "intro_clip"),
        # 02: Tongue Bridge Shoot (2.50s - 5.50s = 3.00s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 0.00, 3.00, "none"),
        # 03: Name "+1 Tongue Escape" spoken + Slide with Intro Badge overlay (5.50s - 12.80s = 7.30s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 3.00, 7.30, "intro_badge"),
        # 04: Gym Treadmill Training & Studs Growth (12.80s - 19.50s = 6.70s)
        ("campaigns/tongue_escape/assets/clips/13_Clip 13.mp4", 0.00, 5.60, "none"),
        ("campaigns/tongue_escape/assets/clips/04_Clip 4 (2).mp4", 0.00, 1.10, "none"),
        # 05: High-Tier Hacker Treadmill x99 (19.50s - 23.20s = 3.70s)
        ("campaigns/tongue_escape/assets/clips/03_Clip 3 (2).mp4", 0.00, 3.70, "none"),
        # 06: Vertical Sky Tongue Climb (23.20s - 27.50s = 4.30s)
        ("campaigns/tongue_escape/assets/clips/05_Clip 5_1J29fm0.mp4", 0.00, 4.30, "none"),
        # 07: Stage 7 Moving Platforms & +100 Wins Pad (27.50s - 31.50s = 4.00s)
        ("campaigns/tongue_escape/assets/clips/10_Clip 10.mp4", 6.00, 4.00, "none"),
        # 08: Elemental Trail Shop - Fire, Lightning, Galaxy (31.50s - 36.80s = 5.30s)
        ("campaigns/tongue_escape/assets/clips/06_Clip 6 (1).mp4", 0.00, 3.50, "none"),
        ("campaigns/tongue_escape/assets/clips/07_Clip 7 (1).mp4", 0.00, 1.80, "none"),
        # 09: Stage 8 Climax (36.80s - 39.50s = 2.70s)
        ("campaigns/tongue_escape/assets/clips/15_Clip 15.mp4", 2.00, 2.70, "none"),
        # 10: 3D Living Endcard Overlay (39.50s - 44.24s = 4.74s)
        ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 10.00, 4.74, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 44.24s)")

    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
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
                    "-i", "temp/tongue_escape/endcard_frames/endcard_%03d.png",
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
            elif otype == "intro_badge":
                # Show badge for first 3.5 seconds of this segment with fade
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-i", intro_badge,
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30[bg];"
                    "[1:v]fade=t=in:st=0.0:d=0.3:alpha=1,fade=t=out:st=3.2:d=0.3:alpha=1[badge];"
                    "[bg][badge]overlay=0:0:enable='between(t,0,3.5)'[v];"
                    "[0:a]volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
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
            
            run_cmd(cmd, f"Rendering Segment {idx+1}/{len(segments)} ({dur:.2f}s, type: {otype})")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate all segments
    raw_video = os.path.join(temp_dir, "raw_concatenated.mp4")
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments into raw_concatenated.mp4")

    # Burn subtitles and mix audio: Game Audio + VO Aoede + BGM2 (-5dB) + SFX Track
    temp_master = os.path.join(temp_dir, "tongue_escape_master_raw.mp4")
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
        f"[2:a]volume=0.22,afade=t=out:st=41.5:d=2.5[a_bgm];"
        f"[3:a]volume=0.90[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "44.24",
        temp_master
    ]
    run_cmd(mix_cmd, "Mixing Master with VO Aoede, BGM2 & Animated Subtitles")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, "01_tongue_escape_way_more_fun.mp4")
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
    retagged_file = os.path.join(out_dir, "01_tongue_escape_way_more_fun_retag.mp4")
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
    sheet_output = os.path.join(out_dir, "01_tongue_escape_way_more_fun_sheet.png")
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
    print(f"+1 TONGUE ESCAPE VIDEO GENERATION COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
