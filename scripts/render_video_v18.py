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

VID_ID = "18_tongue_escape_link_in_bio"

SEGMENTS = [
    # 00: Hook Intro (0.00s - 1.68s) - Speed skater kinetic trap
    ("shared/hooks/INTRO.mp4", 0.00, 1.68, "intro_clip"),
    # 01: Obby reveal pop-in (1.68s - 3.04s) - "...Roblox obby ever made"
    ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 0.00, 1.36, "blurred_bg"),
    # 02: Floating Island Stage 1 (3.04s - 6.44s) - "Your character is trapped on a floating island, and jumping is completely banned!"
    ("campaigns/tongue_escape/assets/clips/02_Clip 2 (2).mp4", 1.50, 3.40, "blurred_bg"),
    # 03: Spitting tongue bridge (6.44s - 8.74s) - "The only way to move... is by spitting out your own tongue!"
    ("campaigns/tongue_escape/assets/clips/02_Clip 2 (2).mp4", 4.90, 2.30, "blurred_bg"),
    # 04: Gym Treadmill Fast Train (8.74s - 11.44s) - "So you have to grind the speed gym, stacking massive multipliers..."
    ("campaigns/tongue_escape/assets/clips/04_Clip 4 (1).mp4", 0.00, 2.70, "blurred_bg"),
    # 05: Giant chasm canyon bridge (11.44s - 14.50s) - "...to stretch your tongue thousands of studs long, just to bridge giant gaps!"
    ("campaigns/tongue_escape/assets/clips/09_Clip 9.mp4", 2.00, 3.06, "blurred_bg"),
    # 06: Laser walls & moving lava (14.50s - 18.38s) - "Every stage gets crazy, laser walls, moving lava, and insane tongue upgrades!"
    ("campaigns/tongue_escape/assets/clips/15_Clip 15.mp4", 0.50, 3.88, "blurred_bg"),
    # 07: Flying tongue sky soaring (18.38s - 20.52s) - "Bro, you can literally fly across the entire map!"
    ("campaigns/tongue_escape/assets/clips/11_Clip 11.mp4", 2.00, 2.14, "blurred_bg"),
    # 08: Living Endcard CTA (20.52s - 23.73s) - "The game is called Plus One Tongue Escape on Roblox. If you wanna play, link is in my bio!"
    ("campaigns/tongue_escape/assets/clips/01_Clip 1 (2).mp4", 10.00, 3.21, "endcard_anim"),
]

def render_video():
    base_dir = "campaigns/tongue_escape"
    temp_dir = "temp/tongue_escape"
    seg_dir = os.path.join(temp_dir, "segments_v18")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_v18_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_v18.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_tongue_escape_v18.ass")

    total_dur = sum(s[2] for s in SEGMENTS)
    print(f"\n=======================================================")
    print(f"RENDERING {VID_ID} (Duration: {total_dur:.2f}s, Voice: Puck, BGM3, Link in Bio)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_v18.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_v18.mp4")
    
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
                        "-i", "temp/tongue_escape/endcard_frames_v03/endcard_%03d.png",
                        "-filter_complex",
                        "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
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
                    # Ambient blurred backdrop: 1:1 square sharp gameplay centered in 1080x1920 blurred canvas
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
                
                run_cmd(cmd, f"Rendering Segment {idx+1}/{len(SEGMENTS)} ({dur:.2f}s, type: {otype})")
                clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

        # Concatenate segments
        concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
        run_cmd(concat_cmd, "Concatenating segments into raw_concatenated_v18.mp4")
    else:
        print(f"\n--> Using existing {raw_video} (pass --force to re-render segments)")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "tongue_escape_master_v18.mp4")
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
        f"[0:a]volume=0.18[a_game];"
        f"[1:a]volume=1.35,volume=4dB[a_vox];"
        f"[2:a]volume=0.22,volume=-5dB,afade=t=out:st={fade_st:.1f}:d=1.9[a_bgm];"
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
    run_cmd(mix_cmd, f"Mixing Master {VID_ID} with Voice Puck (+4dB gain), BGM3 (-5dB gain) & Kinetic Center Subtitles (Y=1180)")

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
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging color space to BT.709")
    retagged_file = os.path.join(out_dir, f"{VID_ID}_retag.mp4")
    if os.path.exists(retagged_file):
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.replace(retagged_file, final_output)
        except Exception as e:
            print(f"Warning moving retagged file: {e}")
            if not os.path.exists(final_output):
                shutil.copy2(retagged_file, final_output)

    # Visual Contact Sheet
    sheet_output = os.path.join(out_dir, f"{VID_ID}_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating Visual Contact Sheet for {VID_ID}")

    file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"VIDEO 18 COMPLETE: {final_output}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Duration: {total_dur:.2f}s")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================\n")
    return final_output

if __name__ == "__main__":
    render_video()
