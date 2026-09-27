import os
import subprocess
import shutil
import json
from PIL import Image, ImageDraw, ImageFont

def run_cmd(cmd, desc):
    print(f"\n--- {desc} ---", flush=True)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {desc}:", flush=True)
        print(res.stderr, flush=True)
        raise RuntimeError(f"Command failed: {desc}")
    print(f"Successfully finished: {desc}", flush=True)
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
    vid_id = "07_asmr_dominoes_pure_sensory_therapy"
    total_dur = 24.50
    subtitle_cutoff = 20.46
    
    temp_dir = f"temp/asmr_dominoes/{vid_id}_prod"
    seg_dir = os.path.join(temp_dir, "segments")
    out_dir = "campaigns/asmr_dominoes/output"
    
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Prepare ASS Subtitles
    phrases_json = "temp/asmr_dominoes/v07_therapy/subtitle_phrases.json"
    with open(phrases_json, "r", encoding="utf-8") as f:
        phrases = json.load(f)

    ass_path = f"campaigns/asmr_dominoes/subtitles/{vid_id}.ass"
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

    count = 0
    for p in phrases:
        txt = p["text"].strip().upper()
        if p["start"] >= subtitle_cutoff or "PLAY ASMR" in txt or "LINK IN" in txt or "GAME IS CALLED" in txt:
            continue
        
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], subtitle_cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        count += 1

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    print(f"Generated clean ASS ({count} dialogues, stops at {subtitle_cutoff}s): {ass_path}", flush=True)

    # 2. Build SFX Track
    sfx_path = os.path.join(temp_dir, "sfx_track.wav")
    sfx_events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 1.00),
        ("assets/sfx/whoosh.mp3", 1400, 0.85),
        ("assets/sfx/pop.mp3", 1800, 0.90),
        ("assets/sfx/ding.mp3", 4560, 0.85),
        ("assets/sfx/whoosh.mp3", 11020, 0.85),
        ("assets/sfx/bass_drop.mp3", 14400, 1.00),
        ("assets/sfx/ding.mp3", 17040, 0.90),
        ("assets/sfx/vine_boom.mp3", 20460, 1.10)
    ]
    
    inputs = ["-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=48000:cl=stereo"]
    filter_parts = []
    mix_inputs = ["[0:a]"]
    
    for idx, (path, delay_ms, vol) in enumerate(sfx_events):
        inputs.extend(["-i", path])
        in_idx = idx + 1
        out_lbl = f"sfx{idx}"
        filter_parts.append(f"[{in_idx}:a]volume={vol:.2f},adelay={delay_ms}|{delay_ms}[{out_lbl}]")
        mix_inputs.append(f"[{out_lbl}]")
        
    mix_filter = "".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=0[a]"
    full_filter = ";".join(filter_parts) + ";" + mix_filter
    
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", full_filter, "-map", "[a]", "-t", f"{total_dur:.2f}", sfx_path]
    run_cmd(cmd, "Building SFX track")

    # 3. Segments with Literal 1:1 Semantic Sync
    # 0.00 -> 1.40 (1.40s): INTRO avatar shock
    # 1.40 -> 4.56 (3.16s): ASMR_Bubbles (2.0 -> 5.16) "total reset, this Roblox game is literally pure therapy"
    # 4.56 -> 11.02 (6.46s): ASMR_Shop (6.5 -> 12.96) "custom ASMR sounds like crunchy celery, resonant bamboo clacks, and airy bubble pops"
    # 11.02 -> 14.40 (3.38s): ASMR_3s_build (0.0 -> 3.38) "stretch out a thousand tiles in three seconds flat"
    # 14.40 -> 17.04 (2.64s): ASMR_Spiral (4.5 -> 7.14) "watch the giant spiral maze collapse with zero lag"
    # 17.04 -> 20.46 (3.42s): ASMR_Lvl1_vs_Lvl3_2 (10.0 -> 13.42) "every single domino drops golden multiplier stars for pure sensory bliss"
    # 20.46 -> 24.50 (4.04s): ASMR_BlackHole (13.0 -> 17.04) "Living Endcard CTA"
    segments = [
        ("shared/hooks/INTRO.mp4", 0.00, 1.40, "intro"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Bubbles.mp4", 2.00, 3.16, "native"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Shop.mp4", 6.50, 6.46, "shop_framed"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 3.38, "native"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 4.50, 2.64, "native"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl3_2.mp4", 10.00, 3.42, "native"),
        ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 13.00, 4.04, "endcard")
    ]

    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated.mp4")

    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(segments):
            seg_out = os.path.join(seg_dir, f"seg_{idx:02d}.mp4")
            if otype == "intro":
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
            elif otype == "native":
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
                # Clean shop frame with blurred ambient backdrop
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
            elif otype == "endcard":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", "temp/asmr_dominoes/v07_therapy/endcard_frames/frame_%04d.png",
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

    # 4. Concatenate
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, "Concatenating segments")

    # 5. Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "master.mp4")
    abs_ass = os.path.abspath(ass_path).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    fade_st = max(0.0, total_dur - 1.9)
    fast_vo = "temp/asmr_dominoes/v07_therapy/vo_fast.wav"
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", fast_vo,
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

    # 6. Loudness Normalization (-14.0 LUFS)
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

    # 7. Retag BT.709
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

    # 8. Visual Contact Sheet
    sheet_output = os.path.join(out_dir, f"{vid_id}_sheet.png")
    samples = [
        (0.60, '0:00.60 (INTRO Shock)'),
        (3.00, '0:03.00 (Bubble Domino Therapy)'),
        (8.50, '0:08.50 (Custom Sound Vault)'),
        (13.00, '0:13.00 (Drag Brush 1000 Tiles)'),
        (16.00, '0:16.00 (Zero-Lag Spiral Collapse)'),
        (19.00, '0:19.00 (Golden Star Multipliers)'),
        (22.50, '0:22.50 (Living Endcard CTA)')
    ]

    for i, (t, lbl) in enumerate(samples):
        kp = os.path.join(temp_dir, f"keyframe_{i}.png")
        cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', final_output, '-vframes', '1', kp]
        subprocess.run(cmd, check=True)

    font_path = 'C:/Windows/Fonts/arialbd.ttf'
    font = ImageFont.truetype(font_path, 28) if os.path.exists(font_path) else ImageFont.load_default()
    tile_w, tile_h = 360, 640
    # 7 samples: 4 cols x 2 rows (last slot dark) or 3 cols x 3 rows (9 slots)
    grid = Image.new('RGB', (tile_w * 3, tile_h * 3), (32, 32, 32))

    for i, (t, lbl) in enumerate(samples):
        col = i % 3
        row = i // 3
        kp = os.path.join(temp_dir, f"keyframe_{i}.png")
        im = Image.open(kp).resize((tile_w, tile_h), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (tile_w, 48)], fill=(0, 0, 0, 200))
        draw.text((10, 8), lbl, fill=(255, 220, 0), font=font)
        grid.paste(im, (col * tile_w, row * tile_h))

    grid.save(sheet_output, "PNG")
    print(f"Generated Visual Contact Sheet: {sheet_output}", flush=True)

if __name__ == "__main__":
    main()
