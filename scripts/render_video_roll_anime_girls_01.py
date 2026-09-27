import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

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
    vid_id = "01_roll_anime_girls_rng_tycoon_secret_rolls"
    total_dur = 24.20
    out_dir = "campaigns/roll_anime_girls/output"
    temp_dir = "temp/roll_anime_girls"
    seg_dir = os.path.join(temp_dir, "segments_rag_01")
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_rag_01_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_rag_01.wav")
    ass_path = "campaigns/roll_anime_girls/subtitles/01_roll_anime_girls_rng_tycoon_secret_rolls.ass"

    # Semantic 1:1 Segments matching Puck Voiceover (Exact 24.20s):
    # Beat 1A (0.00s - 1.40s): Avatar hook opener (INTRO.mp4)
    # Beat 1B (1.40s - 4.32s): Rolling dice gacha animation in center (01_Clip 1.mp4)
    # Beat 2A (4.32s - 6.32s): Starter empty plot & pad (05_Clip 5.mp4)
    # Beat 2B (6.32s - 8.54s): Roll dice and drop anime girl (40_Clip 40.mp4)
    # Beat 3A (8.54s - 11.94s): Plot characters generating passive cash (20_Clip 20.mp4)
    # Beat 3B (11.94s - 14.14s): Placing anime girls on plot pads (50_Clip 50.mp4)
    # Beat 4A (14.14s - 17.18s): Potion Witch central stall luck potions (28_Clip 28.mp4)
    # Beat 4B (17.18s - 19.80s): Rebirth menu x1.5 permanent cash multiplier (25_Clip 25.mp4)
    # Beat 5  (19.80s - 24.20s): Living Endcard Focal Center over Divine Base (000.png + LINK IN BIO)
    SEGMENTS = [
        ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
        ("campaigns/roll_anime_girls/assets/clips/01_Clip 1.mp4", 0.00, 2.92, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/05_Clip 5.mp4", 0.00, 2.00, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/40_Clip 40.mp4", 0.00, 2.22, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/20_Clip 20.mp4", 0.00, 3.40, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/50_Clip 50.mp4", 0.00, 2.20, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/28_Clip 28.mp4", 0.00, 3.04, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/25_Clip 25.mp4", 0.00, 2.62, "ambient_square"),
        ("campaigns/roll_anime_girls/assets/clips/30_Clip 30.mp4", 0.00, 4.40, "endcard_anim"),
    ]

    print(f"=======================================================")
    print(f"RENDERING {vid_id} (Target: {total_dur:.2f}s)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_rag_01.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_rag_01.mp4")

    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(SEGMENTS):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            
            if otype == "intro_clip":
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
            elif otype == "ambient_square":
                # Standard BloxClips framing: 1:1 sharp square centered at Y=420 over ambient blurred background
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
            elif otype == "endcard_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", "temp/roll_anime_girls/endcard_frames_01/frame_%04d.png",
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
            
            run_cmd(cmd, f"Rendering Segment {idx+1}/{len(SEGMENTS)} (type: {otype})")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate segments
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "master_rag_01.mp4")
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
    sample_times = [0.70, 2.50, 5.50, 10.00, 15.50, 21.50]
    labels = [
        '0:00.70 (INTRO Avatar Hook)',
        '0:02.50 (Roll Dice for Anime Girls)',
        '0:05.50 (Empty Plot Base)',
        '0:10.00 (Passive Offline Cash)',
        '0:15.50 (Luck Potions & Rebirth)',
        '0:21.50 (Living Endcard Bio Link)'
    ]

    for i, t in enumerate(sample_times):
        kp = os.path.join(temp_dir, f"keyframe_rag01_{i}.png")
        cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', final_output, '-vframes', '1', kp]
        subprocess.run(cmd, check=True)

    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 28)
    tile_w, tile_h = 360, 640
    grid = Image.new('RGB', (tile_w * 3, tile_h * 2), (32, 32, 32))

    for i, (t, lbl) in enumerate(zip(sample_times, labels)):
        col = i % 3
        row = i // 3
        kp = os.path.join(temp_dir, f"keyframe_rag01_{i}.png")
        im = Image.open(kp).resize((tile_w, tile_h), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(6, 6), (tile_w - 6, 42)], fill=(0, 0, 0, 160))
        draw.text((12, 10), lbl, font=font, fill=(255, 255, 255))
        grid.paste(im, (col * tile_w, row * tile_h))

    grid.save(sheet_output)
    print(f"Generated comprehensive visual contact sheet: {sheet_output}")

    print("\n=======================================================")
    print(f"DONE! Final Video Master: {final_output}")
    print(f"Contact Sheet: {sheet_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
