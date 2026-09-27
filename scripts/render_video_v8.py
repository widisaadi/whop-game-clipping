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
    os.makedirs("temp/v8_segments", exist_ok=True)
    os.makedirs("campaigns/how_to_fisch/output", exist_ok=True)

    # 1. Build SFX track if not already built
    sfx_track = "temp/sfx_track_v8.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_v8 import build_sfx_track
        build_sfx_track(duration=34.39)

    # 10 finely-timed segments totaling 34.39 seconds
    segments = [
        # 01: Hook - INTRO.mp4 avatar shock reaction with Metal Gear Alert at 0.00s (0.00s - 4.30s = 4.30s)
        ("shared/hooks/INTRO.mp4", 0.00, 4.30, "intro_clip"),
        # 02: Island 1 peaceful pier + Animated Spring Intro Badge on 'How to Fisch' (4.30s - 6.80s = 2.50s)
        ("campaigns/how_to_fisch/assets/clips/11_Clip 11.mp4", 0.10, 2.50, "intro_anim"),
        # 03: Reeling floppy shrimp on wooden dock (6.80s - 9.80s = 3.00s)
        ("campaigns/how_to_fisch/assets/clips/08_Clip 8.mp4", 0.50, 3.00, "none"),
        # 04: Water boiling violently & Spider Crab surfacing onto dock (9.80s - 13.00s = 3.20s)
        ("campaigns/how_to_fisch/assets/clips/19_Clip 19.mp4", 0.50, 3.20, "none"),
        # 05: Giant menacing Spider Crab stalking towards player (13.00s - 16.20s = 3.20s)
        ("campaigns/how_to_fisch/assets/clips/24_Clip 24.mp4", 0.50, 3.20, "none"),
        # 06: Bending heavy rod & upgrading gear (16.20s - 19.10s = 2.90s)
        ("campaigns/how_to_fisch/assets/clips/31_Clip 31.mp4", 0.50, 2.90, "none"),
        # 07: Weapon rack & heavy shotguns inventory (19.10s - 22.00s = 2.90s)
        ("campaigns/how_to_fisch/assets/clips/32_Clip 32.mp4", 0.20, 2.90, "none"),
        # 08: Fighting for life with crowbar & weapons vs monster (22.00s - 24.00s = 2.00s)
        ("campaigns/how_to_fisch/assets/clips/28_Clip 28.mp4", 0.50, 2.00, "none"),
        # 09: Team iron sights shootout vs colossal ocean boss (24.00s - 28.80s = 4.80s)
        ("campaigns/how_to_fisch/assets/clips/34_Clip 34.mp4", 0.50, 4.80, "none"),
        # 10: Living blurred endcard with Animated 3D Extruded Title + Floating Logo (28.80s - 34.39s = 5.59s)
        ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 5.59, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 34.39s)")

    concat_list_path = "temp/concat_list_v8.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v8_segments/seg_{idx:02d}.mp4"
            
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

    # 2. Concatenate all 10 segments
    raw_video = "temp/raw_concatenated_v8.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 10 segments into raw_concatenated_v8.mp4")

    # 3. Burn subtitles and mix 4 audio streams (Game SFX + Voiceover + BGM + SFX with Metal Gear Alert)
    temp_master = "temp/how_to_fisch_v8_raw.mp4"
    ass_path = os.path.abspath("campaigns/how_to_fisch/subtitles/captions_v8.ass").replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v8_tight.wav",
        "-i", "assets/bgm.mp3",
        "-i", "temp/sfx_track_v8.wav",
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.20[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.15,afade=t=out:st=32.39:d=2.0[a_bgm];"
        f"[3:a]volume=1.00[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "34.39",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master V8 with captions_v8.ass & 4-Track Audio Mix")

    # 4. Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "campaigns/how_to_fisch/output/04_how_to_fisch_giant_monsters.mp4"
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
    retagged_file = "campaigns/how_to_fisch/output/04_how_to_fisch_giant_monsters_retag.mp4"
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
    sheet_output = "campaigns/how_to_fisch/output/04_how_to_fisch_giant_monsters_sheet.png"
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
    print(f"VIDEO 04 (GIANT MONSTERS & BOSS BATTLES) COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Final Duration: 34.39s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
