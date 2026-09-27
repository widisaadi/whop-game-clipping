import os
import subprocess
import shutil

def run_cmd(cmd, desc):
    print(f"\n--- {desc} ---")
    print("Command:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {desc}:")
        print(res.stderr)
        raise RuntimeError(f"Command failed: {desc}")
    print(f"Successfully finished: {desc}")
    return res

def main():
    vid_id = "01_asmr_dominoes_black_hole_singularity"
    total_dur = 23.74
    out_dir = "campaigns/asmr_dominoes/output"
    temp_dir = "temp/asmr_dominoes"
    seg_dir = os.path.join(temp_dir, "segments_ad_01")
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_ad_01_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_ad_01.wav")
    ass_path = "campaigns/asmr_dominoes/subtitles/01_asmr_dominoes_black_hole.ass"

    # Precise 5-Beat Semantically Aligned Segments with INTRO.mp4 Avatar Shock Hook:
    # Beat 1A (0.00s - 1.40s): INTRO.mp4 avatar shock reaction with Metal Gear Alert
    # Beat 1B (1.40s - 3.96s): Velocity Hook Teaser - Dominoes toppling into purple black hole
    # Beat 2  (3.96s - 7.48s): Constraint / Underdog - Level 1 green dominoes toppling slowly for pocket change
    # Beat 3A (7.48s - 10.48s): Gameplay Loop - Drag brush 500 dominoes in 3s
    # Beat 3B (10.48s - 12.68s): Tools & Scaling - Scale slider cranked to mammoth studs
    # Beat 4  (12.68s - 15.82s): Progression Multipliers - Spiral chain topple triggering cosmic multipliers
    # Beat 5A (15.82s - 20.00s): Peak Singularity - Level 999 cosmic black hole vortex swallowing map
    # Beat 5B (20.00s - 23.74s): Living Endcard Focal Center with official 000.png card & LINK IN BIO
    SEGMENTS = [
        ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl999.mp4", 1.40, 2.56, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl3.mp4", 0.00, 3.52, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 3.00, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lava_topple.mp4", 5.50, 2.20, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 5.00, 3.14, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl999.mp4", 11.00, 4.18, "gameplay"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 13.00, 3.74, "endcard_anim"),
    ]

    print(f"=======================================================")
    print(f"RENDERING {vid_id} WITH INTRO.MP4 & LINK IN BIO (Target: {total_dur:.2f}s)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_ad_01.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_ad_01.mp4")

    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(SEGMENTS):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            
            if otype == "intro_clip":
                # INTRO.mp4 is 1080x1920 vertical avatar shock opener
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
            elif otype == "endcard_anim":
                # Endcard segment: living card animation overlay with LINK IN BIO
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", "temp/asmr_dominoes/endcard_frames_01/frame_%04d.png",
                    "-filter_complex",
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[bg][1:v]overlay=0:0,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            else:
                # Ambient blurred backdrop: 1:1 sharp square centered at Y=420 in 1080x1920 canvas
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
    run_cmd(concat_cmd, "Concatenating segments")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "master_ad_01.mp4")
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
    run_cmd(mix_cmd, "Mixing Master with Puck Voice (+4dB), BGM3 (-5dB), SFX & Subtitles")

    # EBU R128 2-Pass Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, f"{vid_id}.mp4")
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, f"Applying 2-Pass Loudness Normalization (-14.0 LUFS) to {vid_id}")

    # Retag Color Space to BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, f"Retagging color space to BT.709 for {vid_id}")
    retagged_file = os.path.join(out_dir, f"{vid_id}_retag.mp4")
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
    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    look_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "3x2",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(look_cmd, f"Generating visual contact sheet for {vid_id}")

    print("\n=======================================================")
    print(f"DONE! Final Video Master: {final_output}")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
