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
    os.makedirs("temp/v7_callirrhoe_segments", exist_ok=True)
    os.makedirs("campaigns/how_to_fisch/output", exist_ok=True)

    # 1. Build SFX track if not present
    sfx_track = "temp/sfx_track_callirrhoe.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_callirrhoe import build_sfx_track
        build_sfx_track(duration=35.52)

    # 2. Build Subtitles
    ass_path = "campaigns/how_to_fisch/subtitles/captions_v11_callirrhoe.ass"
    if not os.path.exists(ass_path):
        from scripts.build_callirrhoe_subtitles_v11 import generate_subtitles
        generate_subtitles()

    # 9 precisely timed segments totaling 35.52 seconds
    segments = [
        # 01: Hook - INTRO.mp4 avatar shock reaction with Metal Gear Alert (0.00s - 4.80s = 4.80s)
        ("shared/hooks/INTRO.mp4", 0.00, 4.80, "intro_clip"),
        # 02: Island 1 peaceful pier (4.80s - 8.20s = 3.40s)
        ("campaigns/how_to_fisch/assets/clips/01_Clip 1.mp4", 0.50, 3.40, "none"),
        # 03: Ocean water turns red & boils furiously (8.20s - 12.00s = 3.80s)
        ("campaigns/how_to_fisch/assets/clips/19_Clip 19.mp4", 0.50, 3.80, "none"),
        # 04: Giant mutant monsters swarm the pier (12.00s - 16.40s = 4.40s)
        ("campaigns/how_to_fisch/assets/clips/25_Clip 25.mp4", 0.50, 4.40, "none"),
        # 05: Drop rod, pull out iron sights shotguns (16.40s - 19.80s = 3.40s)
        ("campaigns/how_to_fisch/assets/clips/32_Clip 32.mp4", 0.20, 3.40, "none"),
        # 06: Blast through waves of sea beasts shootout (19.80s - 23.10s = 3.30s)
        ("campaigns/how_to_fisch/assets/clips/34_Clip 34.mp4", 0.50, 3.30, "none"),
        # 07: High speed motorboat into stormy boss waters (23.10s - 26.50s = 3.40s)
        ("campaigns/how_to_fisch/assets/clips/18_Clip 18.mp4", 0.50, 3.40, "none"),
        # 08: Raid colossal ocean titans with squad (26.50s - 30.30s = 3.80s)
        ("campaigns/how_to_fisch/assets/clips/35_Clip 35.mp4", 0.50, 3.80, "none"),
        # 09: Living blurred endcard with Animated 3D Title + Floating Logo + Roblox CTA (30.30s - 35.52s = 5.22s)
        ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 5.22, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 35.52s)")

    concat_list_path = "temp/concat_list_v7_callirrhoe.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v7_callirrhoe_segments/seg_{idx:02d}.mp4"
            
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

    # Concatenate all 9 segments
    raw_video = "temp/raw_concatenated_v7_callirrhoe.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 9 segments into raw_concatenated_v7_callirrhoe.mp4")

    # Burn subtitles and mix 4 audio streams: Game Audio + VO Callirrhoe + BGM2 (-4dB) + SFX
    temp_master = "temp/how_to_fisch_v7_callirrhoe_raw.mp4"
    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v11_callirrhoe.wav",
        "-i", "assets/bgm2.mpeg",
        "-i", sfx_track,
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.40[a_vox];"
        f"[2:a]volume=0.24,afade=t=out:st=33.52:d=2.0[a_bgm];"
        f"[3:a]volume=0.95[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "35.52",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master with Callirrhoe VO, BGM2 (-4dB) & Subtitles")

    # Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "campaigns/how_to_fisch/output/07_how_to_fisch_fight_to_survive.mp4"
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
    retagged_file = "campaigns/how_to_fisch/output/07_how_to_fisch_fight_to_survive_retag.mp4"
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
    sheet_output = "campaigns/how_to_fisch/output/07_how_to_fisch_fight_to_survive_sheet.png"
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
    print(f"VIDEO 07 REMASTER WITH CALLIRRHOE VO COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Final Duration: 35.52s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
