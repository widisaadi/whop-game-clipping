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
    os.makedirs("temp/v7_segments", exist_ok=True)
    os.makedirs("output/how_to_fisch", exist_ok=True)
    os.makedirs("campaigns/how_to_fisch/output/final_delivery", exist_ok=True)

    # 1. Build SFX track if not already built
    sfx_track = "temp/sfx_track_v7.wav"
    if not os.path.exists(sfx_track):
        from scripts.build_sfx_track_v7 import build_sfx_track
        build_sfx_track(duration=29.10)

    # 2. Build animation frames if not already built
    if not os.path.exists("temp/intro_frames/intro_074.png") or not os.path.exists("temp/endcard_frames/endcard_157.png"):
        from scripts.create_animated_overlays import generate_intro_frames, generate_endcard_frames
        generate_intro_frames("temp/intro_frames", total_frames=75)
        generate_endcard_frames("temp/endcard_frames", total_frames=158)

    # 10 finely-timed segments totaling 29.10 seconds
    segments = [
        # 01: Hook - INTRO.mp4 avatar shock reaction (0.00s - 3.00s)
        ("shared/hooks/INTRO.mp4", 0.00, 3.00, "intro_clip"),
        # 02: Island 1 peaceful pier + Animated Spring Intro Badge on 'How to Fisch' (3.00s - 5.40s)
        ("campaigns/how_to_fisch/assets/clips/11_Clip 11.mp4", 0.10, 2.40, "intro_anim"),
        # 03: Island 1 cast rod & reeling tiny shrimp catch (5.40s - 8.30s)
        ("campaigns/how_to_fisch/assets/clips/23_Clip 23.mp4", 0.50, 2.90, "none"),
        # 04: Fast motorboat cruising through waves (8.30s - 10.80s)
        ("campaigns/how_to_fisch/assets/clips/18_Clip 18.mp4", 0.50, 2.50, "none"),
        # 05: Steering boat into deep open water (10.80s - 13.30s)
        ("campaigns/how_to_fisch/assets/clips/17_Clip 17.mp4", 1.00, 2.50, "none"),
        # 06: Gold Rod & living burrito bait in hand (13.30s - 16.40s)
        ("campaigns/how_to_fisch/assets/clips/30_Clip 30.mp4", 0.50, 3.10, "none"),
        # 07: Punching mutant lobster with brass knuckles! (16.40s - 19.40s)
        ("campaigns/how_to_fisch/assets/clips/22_Clip 22.mp4", 0.50, 3.00, "none"),
        # 08: Weapon rack & shotgun inventory ready (19.40s - 22.00s)
        ("campaigns/how_to_fisch/assets/clips/32_Clip 32.mp4", 0.20, 2.60, "none"),
        # 09: Iron sights shootout vs giant Pike Fish Boss (22.00s - 24.80s)
        ("campaigns/how_to_fisch/assets/clips/34_Clip 34.mp4", 0.50, 2.80, "none"),
        # 10: Living blurred endcard with Animated 3D Title + Floating Logo (24.80s - 29.10s = 4.30s)
        ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 4.30, "endcard_anim"),
    ]

    total_dur = sum(s[2] for s in segments)
    print(f"Total calculated duration: {total_dur:.2f}s (Target: 29.10s)")

    concat_list_path = "temp/concat_list_v7.txt"
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = f"temp/v7_segments/seg_{idx:02d}.mp4"
            
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

    # Concatenate all 10 segments
    raw_video = "temp/raw_concatenated_v7.mp4"
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating 10 segments into raw_concatenated_v7.mp4")

    # Burn subtitles and mix 4 audio streams (Game SFX + Voiceover + BGM + SFX with Metal Gear Alert)
    temp_master = "temp/how_to_fisch_v7_raw.mp4"
    ass_path = os.path.abspath("campaigns/how_to_fisch/subtitles/captions_v7.ass").replace("\\", "/")
    if ":" in ass_path:
        drive, rest = ass_path.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = ass_path

    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", "temp/voiceover_v7_tight.wav",
        "-i", "assets/bgm.mp3",
        "-i", "temp/sfx_track_v7.wav",
        "-filter_complex",
        f"[0:v]subtitles='{ass_filter_path}'[v];"
        f"[0:a]volume=0.20[a_game];"
        f"[1:a]volume=1.35[a_vox];"
        f"[2:a]volume=0.15,afade=t=out:st=27.10:d=2.0[a_bgm];"
        f"[3:a]volume=1.00[a_sfx];"
        f"[a_game][a_vox][a_bgm][a_sfx]amix=inputs=4:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "29.10",
        temp_master
    ]
    run_cmd(mix_cmd, "Rendering Master V7 with captions_v7.ass & 4-Track Audio Mix")

    # Run loudness.py from ffmpeg-skill for EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
    final_output = "output/how_to_fisch/how_to_fisch_pro_guide.mp4"
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying 2-Pass Loudness Normalization (-14.0 LUFS) via ffmpeg-skill")

    # Tag color space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    if os.path.exists("output/how_to_fisch/how_to_fisch_pro_guide_retag.mp4"):
        shutil.move("output/how_to_fisch/how_to_fisch_pro_guide_retag.mp4", final_output)

    # Copy to campaigns/how_to_fisch/output/final_delivery/
    campaign_delivery = "campaigns/how_to_fisch/output/final_delivery/how_to_fisch_pro_guide.mp4"
    shutil.copy2(final_output, campaign_delivery)
    print(f"Copied final deliverable to {campaign_delivery}")

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
    print(f"MASTER RENDER V7 (BEGINNER TO PRO GUIDE) COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Final Duration: 29.10s")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
