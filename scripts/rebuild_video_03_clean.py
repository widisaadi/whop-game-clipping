import os
import subprocess
import shutil
import json
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

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def main():
    vid_id = "03_asmr_dominoes_lava_magma_topple"
    total_dur = 18.00
    temp_dir = f"temp/asmr_dominoes/{vid_id}_clean"
    seg_dir = os.path.join(temp_dir, "segments")
    out_dir = "campaigns/asmr_dominoes/output"
    
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    # 1. Prepare clean ASS Subtitles
    json_path = "temp/asmr_dominoes/subtitle_phrases_ad_03_clean.json"
    with open(json_path, "r", encoding="utf-8") as f:
        phrases = json.load(f)

    ass_path = "campaigns/asmr_dominoes/subtitles/03_asmr_dominoes_lava_magma_topple.ass"
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    style_map = {
        "WHITE": "CenterWhite",
        "GOLD": "CenterGold",
        "RED": "CenterRed",
        "GREEN": "CenterGreen"
    }

    # Cutoff subtitles right at 14.40s before Living Endcard
    cutoff = 14.40
    count = 0
    for p in phrases:
        if p["start"] >= cutoff or "PLAY ASMR" in p["text"].upper():
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        txt = p["text"].strip().upper()
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        count += 1

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    print(f"Generated clean ASS ({count} dialogues, stops at {cutoff}s): {ass_path}")

    # 2. Build SFX Track
    sfx_path = os.path.join(temp_dir, "sfx_track.wav")
    sfx_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", "assets/sfx/metal_gear_alert.mp3",
        "-i", "assets/sfx/whoosh.mp3",
        "-i", "assets/sfx/coin.mp3",
        "-i", "assets/sfx/vine_boom.mp3",
        "-filter_complex",
        "[1:a]volume=1.0[sfx0];"
        "[2:a]volume=0.85[sfx1];"
        "[3:a]volume=0.90[sfx2];"
        "[4:a]volume=1.10[sfx3];"
        "[0:a][sfx0]amix=inputs=2:duration=first:dropout_transition=0[m0];"
        "[m0][sfx1]adelay=1300|1300[d1];"
        "[d1][sfx2]adelay=4000|4000[d2];"
        "[d2][sfx3]adelay=12600|12600[a]",
        "-map", "[a]",
        "-t", f"{total_dur:.2f}",
        sfx_path
    ]
    # Use simpler amix filter with adelay
    sfx_filter = (
        "[1:a]volume=1.0,adelay=0|0[a0];"
        "[2:a]volume=0.85,adelay=1300|1300[a1];"
        "[3:a]volume=0.90,adelay=4000|4000[a2];"
        "[4:a]volume=1.10,adelay=12600|12600[a3];"
        "[0:a][a0][a1][a2][a3]amix=inputs=5:duration=first:dropout_transition=0[a]"
    )
    sfx_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", "assets/sfx/metal_gear_alert.mp3",
        "-i", "assets/sfx/whoosh.mp3",
        "-i", "assets/sfx/ding.mp3",
        "-i", "assets/sfx/vine_boom.mp3",
        "-filter_complex", sfx_filter,
        "-map", "[a]",
        "-t", f"{total_dur:.2f}",
        sfx_path
    ]
    run_cmd(sfx_cmd, "Building clean SFX track")

    # 3. Segments with Literal 1:1 Video-Audio Sync
    segments = [
        ("shared/hooks/INTRO.mp4", 0.00, 1.30, "intro_clip"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lava_topple.mp4", 1.50, 2.70, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Short_Chain.mp4", 0.50, 2.20, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 3.00, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lava_topple.mp4", 8.50, 3.40, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl3_3.mp4", 9.80, 1.80, "native_vertical"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 13.00, 3.60, "endcard_anim")
    ]

    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated.mp4")

    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
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
            elif otype == "endcard_anim":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", "temp/asmr_dominoes/endcard_frames/frame_%04d.png",
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
            run_cmd(cmd, f"Rendering Segment {idx+1}/{len(segments)}")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # Concatenate
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments")

    # Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "master.mp4")
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
        "-i", "temp/asmr_dominoes/vo_03_test_fast.wav",
        "-i", "assets/bgm3.mp3",
        "-i", sfx_path,
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
    run_cmd(mix_cmd, "Mixing Master with Burned Subtitles")

    # Loudness Normalization (-14.0 LUFS)
    final_output = os.path.join(out_dir, f"{vid_id}.mp4")
    loudness_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/loudness.py",
        temp_master,
        "-I", "-14",
        "--tp", "-1.5",
        "-o", final_output,
        "--overwrite"
    ]
    run_cmd(loudness_cmd, "Applying Loudness Normalization")

    # Retag BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, "Retagging BT.709")
    retagged_file = os.path.join(out_dir, f"{vid_id}_retag.mp4")
    if os.path.exists(retagged_file):
        try:
            if os.path.exists(final_output):
                os.remove(final_output)
            os.replace(retagged_file, final_output)
        except Exception:
            if not os.path.exists(final_output):
                shutil.copy2(retagged_file, final_output)

    # Contact Sheet
    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    samples = [
        (0.60, '0:00.60 (INTRO Shock)'),
        (2.50, '0:02.50 (Lava Dominoes)'),
        (5.00, '0:05.00 (50 Coins)'),
        (7.50, '0:07.50 (Drag Brush 3s)'),
        (13.50, '0:13.50 (Divine Pillar)'),
        (16.00, '0:16.00 (Living Endcard)')
    ]

    for i, (t, lbl) in enumerate(samples):
        kp = os.path.join(temp_dir, f"keyframe_{i}.png")
        cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', final_output, '-vframes', '1', kp]
        subprocess.run(cmd, check=True)

    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 28)
    tile_w, tile_h = 360, 640
    grid = Image.new('RGB', (tile_w * 3, tile_h * 2), (32, 32, 32))

    for i, (t, lbl) in enumerate(samples):
        col = i % 3
        row = i // 3
        kp = os.path.join(temp_dir, f"keyframe_{i}.png")
        im = Image.open(kp).resize((tile_w, tile_h), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(6, 6), (tile_w - 6, 42)], fill=(0, 0, 0, 160))
        draw.text((12, 10), lbl, font=font, fill=(255, 255, 255))
        grid.paste(im, (col * tile_w, row * tile_h))

    grid.save(sheet_output)
    print(f"Generated contact sheet: {sheet_output}")
    print(f"COMPLETED CLEAN VIDEO 03: {final_output}")

if __name__ == "__main__":
    main()
