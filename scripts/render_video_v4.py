import os
import subprocess
import sys

def run_cmd(cmd, desc):
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"ERROR in {desc}:")
        print(res.stderr[-800:])
        sys.exit(1)
    return res

def main():
    os.makedirs("temp/v4_segments", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # 1. Build SFX track if not already built
    sfx_track = "temp/sfx_track.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track import build_sfx_track
        build_sfx_track()

    # 2. Build animation frames if not already built
    if not os.path.exists("temp/intro_frames/intro_071.png") or not os.path.exists("temp/endcard_frames/endcard_157.png"):
        from scripts.create_animated_overlays import generate_intro_frames, generate_endcard_frames
        generate_intro_frames("temp/intro_frames", total_frames=72)
        generate_endcard_frames("temp/endcard_frames", total_frames=158)

    # 14 finely-timed segments totaling 33.76 seconds (matching voiceover_v3.wav exactly)
    # (source, start, dur, overlay_type)
    # overlay_type: 'none', 'intro_anim', 'endcard_anim'
    segments = [
        # 01: Hook - High speed motorboat cutting ocean (0.00s - 2.10s)
        ("assets/18_Clip 18.mp4", 0.50, 2.10, "none"),
        # 02: Hook 2 - 1st-person boat steering towards horizon (2.10s - 4.10s)
        ("assets/17_Clip 17.mp4", 0.80, 2.00, "none"),
        # 03: Island 1 peaceful pier + Animated Spring Intro Badge on 'How to Fisch' (4.10s - 6.50s)
        ("assets/11_Clip 11.mp4", 0.10, 2.40, "intro_anim"),
        # 04: Island 1 cast rod (6.50s - 8.50s)
        ("assets/23_Clip 23.mp4", 0.50, 2.00, "none"),
        # 05: Speeding boat towards Island 2 (8.50s - 11.00s)
        ("assets/18_Clip 18.mp4", 3.00, 2.50, "none"),
        # 06: Steering boat to uncharted island (11.00s - 13.00s)
        ("assets/17_Clip 17.mp4", 3.50, 2.00, "none"),
        # 07: Granny NPC talking with weapon wall & burritos (13.00s - 15.60s)
        ("assets/29_Clip 29.mp4", 0.20, 2.60, "none"),
        # 08: Weapon rack / pistol ready (15.60s - 18.20s)
        ("assets/32_Clip 32.mp4", 0.20, 2.60, "none"),
        # 09: Gold Rod + Burrito Bait in hand! (18.20s - 20.60s)
        ("assets/30_Clip 30.mp4", 0.50, 2.40, "none"),
        # 10: Punching mutant lobster with brass knuckles! (20.60s - 22.30s)
        ("assets/22_Clip 22.mp4", 0.50, 1.70, "none"),
        # 11: Stabbing mutant crab on land with crowbar! (22.30s - 23.60s)
        ("assets/28_Clip 28.mp4", 0.20, 1.30, "none"),
        # 12: Boss fight 1 - shooting Sun Fish Boss (23.60s - 26.00s)
        ("assets/32_Clip 32.mp4", 2.80, 2.40, "none"),
        # 13: Boss fight 2 - Iron sights shootout vs Pike Fish Boss (26.00s - 28.50s)
        ("assets/34_Clip 34.mp4", 0.50, 2.50, "none"),
        # 14: Living blurred endcard with Animated 3D Title + Floating Logo (28.50s - 33.76s = 5.26s)
        ("assets/36_Clip 36.mp4", 0.50, 5.26, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 33.76s)")

    concat_list_path = "temp/concat_list_v4.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v4_segments/seg_{idx:02d}.mp4"
            
            if otype == "endcard_anim":
                # Living blurred gameplay background + Animated 3D Title & Logo
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
                # Intro badge with spring pop-in & whoosh exit
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
            else:
                # Standard gameplay segment cropped to 9:16 vertical
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

    # Concatenate all 14 segments
    raw_video = "temp/raw_concatenated_v4.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 14 segments into raw_concatenated_v4.mp4")

    # Burn subtitles and mix 4 audio streams (Game SFX + Voiceover + BGM + Viral SFX)
    temp_master = "temp/how_to_fisch_island_expedition_raw.mp4"
    ass_path = os.path.abspath("subtitles/captions_v3.ass").replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v3.wav",
        "-i", "assets/bgm.mp3",
        "-i", "temp/sfx_track.wav",
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.25[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.15,afade=t=out:st=31.5:d=2.0[a_bgm];"
        f"[3:a]volume=1.00[a_viral];"
        f"[a_game][a_vox][a_bgm][a_viral]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "33.76",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master with ASS Subtitles & 4-Track Audio Mix")

    # Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "output/how_to_fisch_island_expedition.mp4"
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying 2-Pass Loudness Normalization (-14.0 LUFS) via ffmpeg-skill")

    # Verify platform compliance with check.py
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    res_check = run_cmd(check_cmd, "Verifying TikTok/Reels platform compliance via check.py")
    print(res_check.stdout)

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"MASTER RENDER V4 COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Target Duration: 33.76s")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
