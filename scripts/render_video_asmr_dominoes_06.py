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
    vid_id = "06_asmr_dominoes_hypnotic_spiral_sounds"
    total_dur = 24.20
    out_dir = "campaigns/asmr_dominoes/output"
    temp_dir = "temp/asmr_dominoes"
    seg_dir = os.path.join(temp_dir, "segments_ad_06")
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)

    vo_path = os.path.join(temp_dir, "voiceover_ad_06_fast.wav")
    sfx_track = os.path.join(temp_dir, "sfx_track_ad_06.wav")
    ass_path = "campaigns/asmr_dominoes/subtitles/06_asmr_dominoes_hypnotic_spiral_sounds.ass"

    # Semantic 1:1 Segments matching Puck Voiceover (Exact 24.20s):
    # Beat 1A (0.00s - 1.40s): Avatar hook opener (INTRO.mp4)
    # Beat 1B (1.40s - 3.98s): Hypnotic spiral domino topple wave (ASMR_Spiral.mp4)
    # Beat 2A (3.98s - 6.68s): Secret shop menu with skins & custom sounds (ASMR_Shop.mp4)
    # Beat 2B (6.68s - 9.38s): Sound selector (celery crunch, bamboo clacks, bubble pops) (ASMR_Shop.mp4 stretched)
    # Beat 3  (9.38s - 15.52s): 3-second drag brush build 1,000 dominoes + scale slider (ASMR_3s_build.mp4)
    # Beat 4  (15.52s - 19.92s): Hit topple mode, chain reaction & cosmic black hole (ASMR_BlackHole.mp4)
    # Beat 5  (19.92s - 24.20s): Living Endcard Focal Center over Black Hole (000.png + LINK IN BIO)
    SEGMENTS = [
        ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro_clip"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 4.50, 2.58, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Shop.mp4", 7.20, 2.70, "shop_framed"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Shop.mp4", 10.85, 1.00, "sound_selector_stretch"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 6.14, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 4.00, 4.40, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 13.00, 4.28, "endcard_anim"),
    ]

    print(f"=======================================================")
    print(f"RENDERING {vid_id} (Target: {total_dur:.2f}s)")
    print(f"=======================================================")

    concat_list_path = os.path.join(temp_dir, "concat_list_ad_06.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated_ad_06.mp4")

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
            elif otype == "native_vertical":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p",
                    "-af", "volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            elif otype == "shop_framed":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-filter_complex",
                    "[0:v]crop=1080:608:0:656[cropped];"
                    "[cropped]split[fg][bg_raw];"
                    "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[bg][fg]overlay=0:460,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    seg_out
                ]
            elif otype == "sound_selector_stretch":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-filter_complex",
                    "[0:v]crop=1080:608:0:656,setpts=2.70*PTS[cropped];"
                    "[cropped]split[fg][bg_raw];"
                    "[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=26:6,eq=brightness=-0.18:contrast=1.05[bg];"
                    "[bg][fg]overlay=0:460,fps=30,setsar=1,format=yuv420p[v];"
                    "[0:a]volume=0.30,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]",
                    "-map", "[v]",
                    "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-t", "2.70",
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
                    "-i", "temp/asmr_dominoes/endcard_frames_06/frame_%04d.png",
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
    temp_master = os.path.join(temp_dir, "master_ad_06.mp4")
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
    sample_times = [0.70, 2.80, 5.50, 8.00, 13.00, 21.50]
    labels = [
        '0:00.70 (INTRO Avatar Hook)',
        '0:02.80 (Biggest Domino Spiral)',
        '0:05.50 (Custom Sound Effects)',
        '0:08.00 (Celery & Bamboo ASMR)',
        '0:13.00 (1,000 Dominoes in 3s)',
        '0:21.50 (Living Endcard Bio Link)'
    ]

    for i, t in enumerate(sample_times):
        kp = os.path.join(temp_dir, f"keyframe_ad06_{i}.png")
        cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', final_output, '-vframes', '1', kp]
        subprocess.run(cmd, check=True)

    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 28)
    tile_w, tile_h = 360, 640
    grid = Image.new('RGB', (tile_w * 3, tile_h * 2), (32, 32, 32))

    for i, (t, lbl) in enumerate(zip(sample_times, labels)):
        col = i % 3
        row = i // 3
        kp = os.path.join(temp_dir, f"keyframe_ad06_{i}.png")
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
