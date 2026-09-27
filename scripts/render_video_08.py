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

def main():
    os.makedirs("temp/v12_segments", exist_ok=True)
    os.makedirs("campaigns/how_to_fisch/output", exist_ok=True)

    # 1. Build SFX track if needed
    sfx_track = "temp/sfx_track_v12.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_v12 import build_sfx_track
        build_sfx_track(duration=28.98)

    # 2. Build Subtitles if needed
    ass_path = "campaigns/how_to_fisch/subtitles/captions_v12_smart.ass"
    if not os.path.exists(ass_path):
        from scripts.generate_smart_subtitles_v12 import main as gen_subs
        gen_subs()

    # 8 precisely timed segments totaling 28.98 seconds
    segments = [
        # 01: Hook - INTRO.mp4 avatar shock reaction with Metal Gear Alert (0.00s - 3.40s = 3.40s)
        ("shared/hooks/INTRO.mp4", 0.00, 3.40, "intro_clip"),
        # 02: Island 1 pier + Spring Intro Badge on 'How to Fisch' (3.40s - 7.50s = 4.10s)
        ("campaigns/how_to_fisch/assets/clips/23_Clip 23.mp4", 0.50, 4.10, "intro_anim"),
        # 03: Fast motorboat cruising into uncharted open ocean (7.50s - 11.30s = 3.80s)
        ("campaigns/how_to_fisch/assets/clips/18_Clip 18.mp4", 0.50, 3.80, "none"),
        # 04: Granny shop & shotgun weapon rack (11.30s - 14.50s = 3.20s)
        ("campaigns/how_to_fisch/assets/clips/29_Clip 29.mp4", 0.20, 3.20, "none"),
        # 05: Blasting mutant beasts on pier (14.50s - 18.80s = 4.30s)
        ("campaigns/how_to_fisch/assets/clips/22_Clip 22.mp4", 0.50, 4.30, "none"),
        # 06: Steering boat into stormy waters with crew (18.80s - 21.80s = 3.00s)
        ("campaigns/how_to_fisch/assets/clips/17_Clip 17.mp4", 0.50, 3.00, "none"),
        # 07: Colossal titan boss shootout (21.80s - 24.60s = 2.80s)
        ("campaigns/how_to_fisch/assets/clips/35_Clip 35.mp4", 0.50, 2.80, "none"),
        # 08: Living blurred endcard with Animated 3D Title + Floating Logo + Roblox CTA (24.60s - 28.98s = 4.38s)
        ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 4.38, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 28.98s)")

    concat_list_path = "temp/concat_list_v12.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v12_segments/seg_{idx:02d}.mp4"
            
            if otype == "endcard_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-framerate", "30",
                    "-i", "temp/endcard_frames/endcard_%03d.png",
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=24:6,eq=brightness=-0.28:contrast=1.12[bg];"
                    "[bg][1:v]overlay=0:0[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_out
                ]
            elif otype == "intro_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-framerate", "30",
                    "-i", "temp/intro_frames/intro_%03d.png",
                    "-filter_complex",
                    "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30[bg];"
                    "[bg][1:v]overlay=0:0[v];"
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

    # Concatenate all 8 segments
    raw_video = "temp/raw_concatenated_v12.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 8 segments into raw_concatenated_v12.mp4")

    # Burn subtitles and mix 4 audio streams: Game Audio + VO Callirrhoe (1.20x) + BGM2 (-4dB) + SFX
    temp_master = "temp/how_to_fisch_v12_raw.mp4"
    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v12_fast.wav",
        "-i", "assets/bgm2.mpeg",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.40[a_vox];"
        f"[2:a]volume=0.24,afade=t=out:st=26.98:d=2.0[a_bgm];"
        f"[3:a]volume=0.95[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "28.98",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master V12 with Callirrhoe 1.20x VO, BGM2 (-4dB) & Subtitles")

    # Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "campaigns/how_to_fisch/output/08_how_to_fisch_way_more_fun.mp4"
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying 2-Pass Loudness Normalization (-14.0 LUFS) via ffmpeg-skill")

    # Retag color space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    retagged_file = "campaigns/how_to_fisch/output/08_how_to_fisch_way_more_fun_retag.mp4"
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # Verify platform compliance with check.py
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    res_check = run_cmd(check_cmd, "Verifying TikTok/Reels platform compliance via check.py")
    print(res_check.stdout)

    # Generate Contact Sheet via look.py
    sheet_output = "campaigns/how_to_fisch/output/08_how_to_fisch_way_more_fun_sheet.png"
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, "Generating Visual Contact Sheet via look.py")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"VIDEO 08 (WAY MORE FUN THAN IT LOOKS) COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Final Duration: 28.98s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
