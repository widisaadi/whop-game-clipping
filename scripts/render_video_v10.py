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
    os.makedirs("temp/v10_segments", exist_ok=True)
    os.makedirs("campaigns/how_to_fisch/output", exist_ok=True)

    sfx_track = "temp/sfx_track_v10.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_v10 import build_sfx_track
        build_sfx_track(duration=31.99)

    # 8 verified segments totaling 31.99 seconds
    segments = [
        # 01: Hook - INTRO.mp4 avatar shock reaction with Metal Gear Alert (0.00s - 3.50s = 3.50s)
        ("shared/hooks/INTRO.mp4", 0.00, 3.50, "intro_clip"),
        # 02: Island 1 peaceful pier + Animated Spring Intro Badge (3.50s - 6.70s = 3.20s)
        ("campaigns/how_to_fisch/assets/clips/01_Clip 1.mp4", 0.50, 3.20, "intro_anim"),
        # 03: Gold Rod & living Burrito Bait in hand (6.70s - 11.00s = 4.30s)
        ("campaigns/how_to_fisch/assets/clips/30_Clip 30.mp4", 0.50, 4.30, "none"),
        # 04: Granny lighthouse NPC & shotgun purchases (11.00s - 15.80s = 4.80s)
        ("campaigns/how_to_fisch/assets/clips/14_Clip 14.mp4", 0.50, 4.80, "none"),
        # 05: Punching mutant lobster with brass knuckles (15.80s - 20.70s = 4.90s)
        ("campaigns/how_to_fisch/assets/clips/22_Clip 22.mp4", 0.20, 4.90, "none"),
        # 06: Weapon rack upgrade shop (20.70s - 24.30s = 3.60s)
        ("campaigns/how_to_fisch/assets/clips/32_Clip 32.mp4", 0.50, 3.60, "none"),
        # 07: Iron sights boss shootout vs giant Pike Fish Boss (24.30s - 27.20s = 2.90s)
        ("campaigns/how_to_fisch/assets/clips/34_Clip 34.mp4", 0.50, 2.90, "none"),
        # 08: Living blurred endcard with Animated 3D Extruded Title + Floating Logo (27.20s - 31.99s = 4.79s)
        ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 4.79, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 31.99s)")

    concat_list_path = "temp/concat_list_v10.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v10_segments/seg_{idx:02d}.mp4"
            
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

    # 2. Concatenate all 8 segments
    raw_video = "temp/raw_concatenated_v10.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 8 segments into raw_concatenated_v10.mp4")

    # 3. Burn subtitles and mix 4 audio streams
    temp_master = "temp/how_to_fisch_v10_raw.mp4"
    ass_path = os.path.abspath("campaigns/how_to_fisch/subtitles/captions_v10.ass").replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v10_fast.wav",
        "-i", "assets/bgm.mp3",
        "-i", "temp/sfx_track_v10.wav",
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.20[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.15,afade=t=out:st=29.99:d=2.0[a_bgm];"
        f"[3:a]volume=1.00[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "31.99",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master V10 with captions_v10.ass & 4-Track Audio Mix")

    # 4. Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "campaigns/how_to_fisch/output/06_how_to_fisch_weirdest_game.mp4"
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying 2-Pass Loudness Normalization (-14.0 LUFS) via ffmpeg-skill")

    # 5. Tag color space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    retagged_file = "campaigns/how_to_fisch/output/06_how_to_fisch_weirdest_game_retag.mp4"
    if os.path.exists(retagged_file):
        shutil.move(retagged_file, final_output)

    # 6. Verify platform compliance with check.py
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    res_check = run_cmd(check_cmd, "Verifying TikTok/Reels platform compliance via check.py")
    print(res_check.stdout)

    # 7. Generate Contact Sheet via look.py
    sheet_output = "campaigns/how_to_fisch/output/06_how_to_fisch_weirdest_game_sheet.png"
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
    print(f"VIDEO 06 (WEIRDEST GAME DISCOVERY) COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Final Duration: 31.99s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
