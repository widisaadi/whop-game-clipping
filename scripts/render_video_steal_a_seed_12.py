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
    # 01: Mega Garden $1.17M Overview & Item Shop Intro (1.40s - 6.45s | dur 5.05s)
    ("campaigns/steal_a_seed/assets/clips/19_Clip 19.mp4", 0.00, 5.05, "blurred_bg"),
    # 02: Desert Zone Infiltration & Spiky Cactus Monster Ambush (6.45s - 11.08s | dur 4.63s)
    ("campaigns/steal_a_seed/assets/clips/18_Clip 18.mp4", 0.00, 4.63, "blurred_bg"),
    # 03: Secret Item Shop: Frozen Grenades & Bear Traps (11.08s - 14.58s | dur 3.50s)
    ("campaigns/steal_a_seed/assets/clips/22_Clip 22.mp4", 0.00, 3.50, "blurred_bg"),
    # 04: Trail Shop & Cyan Laser Trail 13K Speed Sprint (14.58s - 17.26s | dur 2.68s)
    ("campaigns/steal_a_seed/assets/clips/28_Clip 28.mp4", 0.00, 2.68, "blurred_bg"),
    # 05a: Glowing Crystal Golems (17.26s - 20.36s | dur 3.10s)
    ("campaigns/steal_a_seed/assets/clips/19_Clip 19.mp4", 2.20, 3.10, "blurred_bg"),
    # 05b: Income Blasting to $1.17M/s - $1.26M/s (20.36s - 23.50s | dur 3.14s)
    ("campaigns/steal_a_seed/assets/clips/29_Clip 29.mp4", 0.00, 3.14, "blurred_bg"),
    # 06: Living Endcard CTA with Giant Wall Nut Head Flex (23.50s - 27.99s | dur 4.49s)
    ("campaigns/steal_a_seed/assets/clips/33_Clip 33.mp4", 0.50, 4.49, "endcard_anim"),
]

def render_steal_a_seed_12():
    vid_id = "12_steal_a_seed_secret_weapons_millionaire"
    base_dir = "campaigns/steal_a_seed"
    temp_dir = "temp/steal_a_seed"
    seg_dir = os.path.join(temp_dir, "segments_sas_12")
    out_dir = os.path.join(base_dir, "output")
    
    # Clean previous segments to guarantee 100% fresh render
    if os.path.exists(seg_dir):
        shutil.rmtree(seg_dir)
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_sas_12_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_sas_12.wav")
    ass_path = os.path.join(base_dir, "subtitles", "captions_steal_a_seed_12.ass")

    total_dur = sum(s[2] for s in SEGMENTS)
    print(f"\n=======================================================")
    print(f"RENDERING {vid_id} (Target: {total_dur:.2f}s)")
    print(f"Audio Mix: BloxClips Golden Mix (Puck +4dB, BGM3 -5dB, SFX 0.90, -14 LUFS)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_sas_12.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_sas_12.mp4")

    # Render segments
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
                    "-i", "temp/steal_a_seed/endcard_frames_12/endcard_%03d.png",
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
                    "[0:a]volume=0.25,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            run_cmd(cmd, f"Rendering Segment {idx:02d} ({dur:.2f}s)")
            clist.write(f"file '{os.path.abspath(seg_out)}'\n")

    # Concatenate segments
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        "-video_track_timescale", "15360",
        raw_video
    ]
    run_cmd(concat_cmd, "Concatenating Segments")

    # Mix Master Video with Subtitles, Voiceover, BGM, and SFX
    temp_master = os.path.join(temp_dir, "master_sas_12.mp4")
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
            os.remove(final_output)
            os.rename(retagged_file, final_output)
        except Exception:
            pass

    # Generate Visual Verification Contact Sheet
    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    sheet_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/look.py",
        final_output,
        "--tiles", "4x3",
        "-o", sheet_output,
        "--overwrite"
    ]
    run_cmd(sheet_cmd, f"Generating visual verification contact sheet for {vid_id}")

    print(f"\n=======================================================")
    print(f"SUCCESS! {vid_id}.mp4 RENDERED SUCCESSFULLY!")
    print(f"Master: {final_output}")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    render_steal_a_seed_12()
