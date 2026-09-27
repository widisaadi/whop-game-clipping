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

SEGMENTS = [
    # 00: Avatar Shock Opening Hook (0.00s - 1.40s | dur 1.40s)
    ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
    # 01: Forest Zone Infiltration, Suggested 900 Speed, Grabbing Stone Oak Seed, Red Monster Ambush (1.40s - 4.60s | dur 3.20s)
    ("campaigns/steal_a_seed/assets/clips/16_Clip 16.mp4", 0.00, 3.20, "blurred_bg"),
    # 02: Sprinting across red boundary line & "Steal Successful!" (4.60s - 7.20s | dur 2.60s)
    ("campaigns/steal_a_seed/assets/clips/16_Clip 16.mp4", 3.20, 2.60, "blurred_bg"),
    # 03: Planting Oak Seed in garden, timer countdown Time: 02:30 starts (7.20s - 10.00s | dur 2.80s)
    ("campaigns/steal_a_seed/assets/clips/17_Clip 17.mp4", 0.00, 2.80, "blurred_bg"),
    # 04: Hitting "Claim!" on giant Wall Nut plant, placing it on stand, +$39,375/s (10.00s - 13.50s | dur 3.50s)
    ("campaigns/steal_a_seed/assets/clips/20_Clip 20.mp4", 0.00, 3.50, "blurred_bg"),
    # 05: Garden escalation overview with glowing crystal golems & (Total: $ 1.17M/s) (13.50s - 16.30s | dur 2.80s)
    ("campaigns/steal_a_seed/assets/clips/19_Clip 19.mp4", 2.20, 2.80, "blurred_bg"),
    # 06: Equipping the giant Frost Mini Cactus head helmet (16.30s - 18.50s | dur 2.20s)
    ("campaigns/steal_a_seed/assets/clips/32_Clip 32.mp4", 0.00, 2.20, "blurred_bg"),
    # 07: Living Endcard CTA (18.50s - 22.38s | dur 3.88s)
    ("campaigns/steal_a_seed/assets/clips/32_Clip 32.mp4", 2.20, 3.88, "endcard_anim"),
]

def render_steal_a_seed_06():
    vid_id = "06_steal_a_seed_forest_monster_oak_seed"
    base_dir = "campaigns/steal_a_seed"
    temp_dir = "temp/steal_a_seed"
    seg_dir = os.path.join(temp_dir, "segments_sas_06")
    out_dir = os.path.join(base_dir, "output")
    
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_sas_06_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_sas_06.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_steal_a_seed_06.ass")

    total_dur = sum(s[2] for s in SEGMENTS)
    print(f"\n=======================================================")
    print(f"RENDERING {vid_id} (Target: {total_dur:.2f}s)")
    print(f"Audio Mix: BloxClips Golden Mix (Puck +4dB, BGM3 -5dB, SFX 0.90, -14 LUFS)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_sas_06.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_sas_06.mp4")

    # Render segments
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(SEGMENTS):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            
            if not os.path.exists(seg_out) or os.path.getsize(seg_out) < 1000:
                if otype == "endcard_anim":
                    cmd = [
                        "ffmpeg", "-y",
                        "-ss", f"{start:.2f}",
                        "-t", f"{dur:.2f}",
                        "-i", source,
                        "-framerate", "30",
                        "-i", "temp/steal_a_seed/endcard_frames_04/endcard_%03d.png",
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
    temp_master = os.path.join(temp_dir, "master_sas_06.mp4")
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
    run_cmd(mix_cmd, "Mixing Master with Puck Voice (+4dB), BGM3 (-5dB), SFX Track (0.90) & Subtitles")

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
    timestamps = [0.6, 3.5, 6.0, 11.5, 15.0, 20.5]
    frame_files = []
    for f_idx, ts in enumerate(timestamps):
        ff = os.path.join(temp_dir, f"cs_06_frame_{f_idx}.jpg")
        fcmd = ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", final_output, "-vframes", "1", "-q:v", "2", ff]
        subprocess.run(fcmd, check=True)
        frame_files.append(ff)

    tile_cmd = [
        "ffmpeg", "-y",
        "-i", frame_files[0], "-i", frame_files[1], "-i", frame_files[2],
        "-i", frame_files[3], "-i", frame_files[4], "-i", frame_files[5],
        "-filter_complex",
        "[0:v]scale=540:960[v0];[1:v]scale=540:960[v1];[2:v]scale=540:960[v2];"
        "[3:v]scale=540:960[v3];[4:v]scale=540:960[v4];[5:v]scale=540:960[v5];"
        "[v0][v1][v2]hstack=inputs=3[row1];"
        "[v3][v4][v5]hstack=inputs=3[row2];"
        "[row1][row2]vstack=inputs=2[out]",
        "-map", "[out]",
        sheet_output
    ]
    run_cmd(tile_cmd, f"Building Custom Contact Sheet for {vid_id}")

    print(f"\n=======================================================")
    print(f"SUCCESS! {vid_id} rendered and verified:")
    print(f"Video: {final_output}")
    print(f"Sheet: {sheet_output}")
    print(f"=======================================================\n")

if __name__ == "__main__":
    render_steal_a_seed_06()
