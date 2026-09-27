import os
import subprocess
import sys
import shutil

VID_ID = "12_how_to_fisch_sunfish_hunt"

SEGMENTS = [
    # 00: Hook Intro (0.00s - 2.60s) - "BRO THIS IS LITERALLY THE MOST UNHINGED FISHING GAME IN ROBLOX"
    ("shared/hooks/INTRO.mp4", 0.00, 2.60, "intro_clip"),
    # 01: Casting Gold Rod (2.60s - 5.50s) - "IN HOW TO FISCH YOU CAST YOUR ROD EXPECTING A PEACEFUL SIMULATOR"
    ("campaigns/how_to_fisch/assets/clips/30_Clip 30.mp4", 0.00, 2.90, "blurred_bg"),
    # 02: Sun Fish Boss Charges (5.50s - 8.60s) - "UNTIL AN ENRAGED GIANT SUN FISH BOSS CHARGES STRAIGHT OUT OF THE WATER"
    ("campaigns/how_to_fisch/assets/clips/31_Clip 31.mp4", 0.50, 3.10, "blurred_bg"),
    # 03: Fish Armory Guns Roll (8.60s - 11.70s) - "THE ONLY WAY TO SURVIVE IS ROLLING HIGH-TIER GUNS AT THE FISH ARMORY"
    ("campaigns/how_to_fisch/assets/clips/26_Clip 26.mp4", 0.50, 3.10, "blurred_bg"),
    # 04: Shooting Yellow Monster (11.70s - 14.00s) - "BLAST THROUGH ITS MASSIVE HEALTH BAR WITH YOUR PISTOL"
    ("campaigns/how_to_fisch/assets/clips/25_Clip 25.mp4", 0.50, 2.30, "blurred_bg"),
    # 05: Steering Motorboat (14.00s - 16.10s) - "THEN STEER YOUR MOTORBOAT INTO DEEP OPEN WATERS"
    ("campaigns/how_to_fisch/assets/clips/18_Clip 18.mp4", 0.50, 2.10, "blurred_bg"),
    # 06: Colossal Ocean Titans (16.10s - 18.30s) - "TO HUNT DOWN COLOSSAL MYTHICAL OCEAN TITANS"
    ("campaigns/how_to_fisch/assets/clips/33_Clip 33.mp4", 0.50, 2.20, "blurred_bg"),
    # 07: Living Endcard CTA (18.30s - 23.88s) - "THE GAME IS CALLED HOW TO FISCH ON ROBLOX SEARCH HOW TO FISCH AND PLAY RIGHT NOW"
    ("campaigns/how_to_fisch/assets/clips/36_Clip 36.mp4", 0.50, 5.58, "endcard_anim"),
]

def run_cmd(cmd, desc):
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
    if res.returncode != 0:
        print(f"ERROR in {desc}:")
        print(res.stderr[-1000:])
        sys.exit(1)
    return res

def render_video():
    base_dir = "campaigns/how_to_fisch"
    temp_dir = "temp/how_to_fisch"
    seg_dir = os.path.join(temp_dir, "segments_v12")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_htf_v12_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_htf_v12.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_how_to_fisch_v12.ass")

    total_dur = sum(s[2] for s in SEGMENTS)
    print(f"\n=======================================================")
    print(f"RENDERING {VID_ID} (Duration: {total_dur:.2f}s, Voice: Puck, BGM3, Search on Roblox)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_v12.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_v12.mp4")
    
    if not os.path.exists(raw_video) or "--force" in sys.argv:
        with open(concat_list_path, "w", encoding="utf-8") as clist:
            for idx, (source, start, dur, otype) in enumerate(SEGMENTS):
                seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
                
                if otype == "endcard_anim":
                    cmd = [
                        "ffmpeg", "-y",
                        "-ss", f"{start:.2f}",
                        "-t", f"{dur:.2f}",
                        "-i", source,
                        "-framerate", "30",
                        "-i", "temp/how_to_fisch/endcard_frames_v12/endcard_%03d.png",
                        "-filter_complex",
                        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.22:contrast=1.05[bg];"
                        "[bg][1:v]overlay=0:0,fps=30,setsar=1,format=yuv420p[v]",
                        "-map", "[v]",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-r", "30",
                        "-video_track_timescale", "15360",
                        "-an",
                        seg_out
                    ]
                elif otype == "intro_clip":
                    cmd = [
                        "ffmpeg", "-y",
                        "-ss", f"{start:.2f}",
                        "-t", f"{dur:.2f}",
                        "-i", source,
                        "-vf",
                        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-r", "30",
                        "-video_track_timescale", "15360",
                        "-an",
                        seg_out
                    ]
                else: # blurred_bg
                    cmd = [
                        "ffmpeg", "-y",
                        "-ss", f"{start:.2f}",
                        "-t", f"{dur:.2f}",
                        "-i", source,
                        "-filter_complex",
                        "[0:v]split[fg_raw][bg_raw];"
                        "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                        "[fg_raw]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080:(in_w-out_w)/2:(in_h-out_h)/2[fg];"
                        "[bg][fg]overlay=0:420,fps=30,setsar=1,format=yuv420p[v]",
                        "-map", "[v]",
                        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-r", "30",
                        "-video_track_timescale", "15360",
                        "-an",
                        seg_out
                    ]

                run_cmd(cmd, f"Encoding Segment {idx+1}/{len(SEGMENTS)} ({otype}, {dur:.2f}s)")
                clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

        # Concat segments
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_path,
            "-c", "copy",
            "-video_track_timescale", "15360",
            raw_video
        ]
        run_cmd(concat_cmd, "Concatenating Segments")
    else:
        print(f"\n--> Using existing {raw_video} (pass --force to re-render segments)")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "how_to_fisch_master_v12.mp4")
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
        f"[1:a]volume=1.35,volume=4dB[a_vox];"
        f"[2:a]volume=0.22,volume=-5dB,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
        f"[3:a]volume=0.90[a_sfx];"
        f"[a_vox][a_bgm][a_sfx]amix=inputs=3:duration=first:dropout_transition=2[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac", "-b:a", "256k",
        "-t", f"{total_dur:.2f}",
        temp_master
    ]
    run_cmd(mix_cmd, f"Mixing Master {VID_ID} with Voice Puck (+4dB boost), BGM3 (-5dB gain) & Kinetic Center Subtitles (Y=1180)")

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
        "--retag", "bt709"
    ]
    run_cmd(retag_cmd, "Retagging Video to BT.709 Color Space")

    # Generate Visual Contact Sheet (6 key moments)
    sheet_output = os.path.join(out_dir, f"{VID_ID}_sheet.png")
    sheet_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/sheet.py",
        final_output,
        "-o", sheet_output,
        "-c", "3", "-r", "2"
    ]
    run_cmd(sheet_cmd, "Generating 6-Frame Contact Sheet")

    # TikTok Compliance Verification
    check_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/check.py",
        final_output,
        "--platform", "tiktok"
    ]
    run_cmd(check_cmd, "Running Platform Compliance Verification")

    print(f"\nSUCCESS! Master Video 12 rendered at:\n{final_output}")
    print(f"Contact Sheet saved at:\n{sheet_output}")

if __name__ == "__main__":
    render_video()
