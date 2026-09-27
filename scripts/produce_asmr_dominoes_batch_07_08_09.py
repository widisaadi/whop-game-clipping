import os
import subprocess
import shutil
import json
import math
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

VIDEOS_CONFIG = [
    {
        "id": "07_asmr_dominoes_lvl1_vs_lvl999",
        "title": "ASMR Dominoes Video 07 (Level 1 Noob vs Level 999 God Domino)",
        "concept": "Angle 1 — Avatar Shock Hook + Level 1 Wood Tiles (50 Coins) vs Level 999 God Drag Brush / Obsidian Cascade / Dark Matter Singularity Vortex",
        "total_dur": 26.50,
        "endcard_start": 22.22,
        "subtitle_cutoff": 22.22,
        "fast_vo": "temp/asmr_dominoes/batch_07_08_09/07_asmr_dominoes_lvl1_vs_lvl999_fast.wav",
        "phrases_json": "temp/asmr_dominoes/subtitle_phrases_07.json",
        "ass_file": "campaigns/asmr_dominoes/subtitles/07_asmr_dominoes_lvl1_vs_lvl999.ass",
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.30, "intro"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl999.mp4", 0.00, 4.50, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_3s_build.mp4", 0.00, 3.80, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl999.mp4", 5.20, 6.00, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl999.mp4", 11.20, 6.62, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 12.00, 4.28, "endcard")
        ],
        "sfx": [
            ("assets/sfx/metal_gear_alert.mp3", 0, 1.00),
            ("assets/sfx/whoosh.mp3", 1300, 0.85),
            ("assets/sfx/ding.mp3", 5800, 0.90),
            ("assets/sfx/whoosh.mp3", 9600, 0.85),
            ("assets/sfx/bass_drop.mp3", 15600, 1.00),
            ("assets/sfx/vine_boom.mp3", 22220, 1.10)
        ],
        "contact_samples": [
            (0.60, '0:00.60 (INTRO Shock)'),
            (3.00, '0:03.00 (Lvl 1 Chain 50 Coins)'),
            (7.50, '0:07.50 (Lvl 999 Drag Brush 3s)'),
            (12.50, '0:12.50 (Obsidian Hypersonic Cascade)'),
            (18.50, '0:18.50 (Singularity Approach)'),
            (24.00, '0:24.00 (Living Endcard CTA)')
        ]
    },
    {
        "id": "08_asmr_dominoes_satisfying_bubble_pop",
        "title": "ASMR Dominoes Video 08 (The Most Addicting Bubble Dominoes)",
        "concept": "Angle 2 — Avatar Shock Hook + Iridescent Bubble Dominoes / 0.30x Slow-Mo Speed Slider / Bubbly Tidal Wave / Golden Star Jackpot",
        "total_dur": 24.50,
        "endcard_start": 20.96,
        "subtitle_cutoff": 20.96,
        "fast_vo": "temp/asmr_dominoes/batch_07_08_09/08_asmr_dominoes_satisfying_bubble_pop_fast.wav",
        "phrases_json": "temp/asmr_dominoes/subtitle_phrases_08.json",
        "ass_file": "campaigns/asmr_dominoes/subtitles/08_asmr_dominoes_satisfying_bubble_pop.ass",
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.30, "intro"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Bubbles.mp4", 0.00, 3.80, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Topple_Crunch.mp4", 0.00, 4.20, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Bubbles.mp4", 4.50, 6.20, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl3_2.mp4", 9.50, 5.46, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Lvl1_vs_Lvl3_2.mp4", 15.00, 3.54, "endcard")
        ],
        "sfx": [
            ("assets/sfx/metal_gear_alert.mp3", 0, 1.00),
            ("assets/sfx/whoosh.mp3", 1300, 0.85),
            ("assets/sfx/pop.mp3", 5100, 0.95),
            ("assets/sfx/whoosh.mp3", 9300, 0.85),
            ("assets/sfx/ding.mp3", 15500, 0.90),
            ("assets/sfx/vine_boom.mp3", 20960, 1.10)
        ],
        "contact_samples": [
            (0.60, '0:00.60 (INTRO Shock)'),
            (3.00, '0:03.00 (Bubble Wrap Dominoes)'),
            (7.00, '0:07.00 (Slow-Mo Crunch Slider)'),
            (12.00, '0:12.00 (Tidal Wave Cinematic Cam)'),
            (18.00, '0:18.00 (Multiplier Milestone Cascade)'),
            (22.50, '0:22.50 (Living Endcard CTA)')
        ]
    },
    {
        "id": "09_asmr_dominoes_shop_secret_skins",
        "title": "ASMR Dominoes Video 09 (Unlocking Secret Domino Skins & Celery ASMR)",
        "concept": "Angle 3 — Avatar Shock Hook + 100 Million Coins Secret Skin Vault / Custom Sound Menu (Celery, Bamboo, Crystal) / Hypnotic Galaxy Spiral / Cosmic Black Hole",
        "total_dur": 24.50,
        "endcard_start": 21.00,
        "subtitle_cutoff": 21.00,
        "fast_vo": "temp/asmr_dominoes/batch_07_08_09/09_asmr_dominoes_shop_secret_skins_fast.wav",
        "phrases_json": "temp/asmr_dominoes/subtitle_phrases_09.json",
        "ass_file": "campaigns/asmr_dominoes/subtitles/09_asmr_dominoes_shop_secret_skins.ass",
        "segments": [
            ("shared/hooks/INTRO.mp4", 0.00, 1.30, "intro"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Short_Chain.mp4", 0.00, 3.40, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Shop.mp4", 7.00, 4.10, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 0.50, 6.50, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_Spiral.mp4", 7.00, 5.70, "native"),
            ("campaigns/asmr_dominoes/assets/references/ASMR_BlackHole.mp4", 14.00, 3.50, "endcard")
        ],
        "sfx": [
            ("assets/sfx/metal_gear_alert.mp3", 0, 1.00),
            ("assets/sfx/whoosh.mp3", 1300, 0.85),
            ("assets/sfx/ding.mp3", 4700, 0.90),
            ("assets/sfx/whoosh.mp3", 8800, 0.85),
            ("assets/sfx/bass_drop.mp3", 15300, 1.00),
            ("assets/sfx/vine_boom.mp3", 21000, 1.10)
        ],
        "contact_samples": [
            (0.60, '0:00.60 (INTRO Shock)'),
            (3.00, '0:03.00 (Wooden Blocks Cardboard)'),
            (6.50, '0:06.50 (Custom Sound Vault Menu)'),
            (11.50, '0:11.50 (Galaxy Spiral Labyrinth)'),
            (18.00, '0:18.00 (Zero-Lag Inner Cascade)'),
            (22.50, '0:22.50 (Living Endcard CTA)')
        ]
    }
]

def build_ass_subtitles(cfg):
    with open(cfg["phrases_json"], "r", encoding="utf-8") as f:
        phrases = json.load(f)

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

    cutoff = cfg["subtitle_cutoff"]
    count = 0
    for p in phrases:
        txt = p["text"].strip().upper()
        if p["start"] >= cutoff or "PLAY ASMR" in txt or "LINK IN BIO" in txt:
            continue
        
        # Clean any trailing endcard words if combined
        if "PLAY ASMR" in txt:
            txt = txt.split("PLAY ASMR")[0].strip()
            if not txt:
                continue

        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        count += 1

    os.makedirs(os.path.dirname(cfg["ass_file"]), exist_ok=True)
    with open(cfg["ass_file"], "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    print(f"Generated clean ASS ({count} dialogues, stops at {cutoff}s): {cfg['ass_file']}", flush=True)

def build_sfx_track(cfg, temp_dir):
    sfx_path = os.path.join(temp_dir, "sfx_track.wav")
    total_dur = cfg["total_dur"]
    
    inputs = ["-f", "lavfi", "-t", f"{total_dur:.2f}", "-i", "anullsrc=r=48000:cl=stereo"]
    filter_parts = []
    mix_inputs = ["[0:a]"]
    
    for idx, (path, delay_ms, vol) in enumerate(cfg["sfx"]):
        inputs.extend(["-i", path])
        in_idx = idx + 1
        out_lbl = f"sfx{idx}"
        filter_parts.append(f"[{in_idx}:a]volume={vol:.2f},adelay={delay_ms}|{delay_ms}[{out_lbl}]")
        mix_inputs.append(f"[{out_lbl}]")
        
    mix_filter = "".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=0[a]"
    full_filter = ";".join(filter_parts) + ";" + mix_filter
    
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", full_filter, "-map", "[a]", "-t", f"{total_dur:.2f}", sfx_path]
    run_cmd(cmd, f"Building SFX track for {cfg['id']}")
    return sfx_path

def render_single_video(cfg):
    vid_id = cfg["id"]
    total_dur = cfg["total_dur"]
    temp_dir = f"temp/asmr_dominoes/{vid_id}_prod"
    seg_dir = os.path.join(temp_dir, "segments")
    out_dir = "campaigns/asmr_dominoes/output"
    
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f"PRODUCING VIDEO: {vid_id} (Target: {total_dur:.2f}s)")
    print(f"=======================================================", flush=True)
    
    # 1. Build Subtitles
    build_ass_subtitles(cfg)
    
    # 2. Build SFX Track
    sfx_path = build_sfx_track(cfg, temp_dir)
    
    # 3. Render Segments
    concat_list_path = os.path.join(temp_dir, "concat_list.txt")
    raw_video = os.path.join(temp_dir, "raw_concatenated.mp4")
    
    with open(concat_list_path, "w", encoding="utf-8") as clist:
        for idx, (source, start, dur, otype) in enumerate(cfg["segments"]):
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
            elif otype == "endcard":
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.2f}",
                    "-t", f"{dur:.2f}",
                    "-i", source,
                    "-start_number", "0",
                    "-framerate", "30",
                    "-i", "temp/asmr_dominoes/batch_endcard_frames/frame_%04d.png",
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
            run_cmd(cmd, f"Rendering Segment {idx+1}/{len(cfg['segments'])} for {vid_id}")
            clist.write(f"file '{os.path.abspath(seg_out).replace(chr(92), '/')}'\n")

    # 4. Concatenate
    concat_cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path, "-c", "copy", raw_video]
    run_cmd(concat_cmd, f"Concatenating segments for {vid_id}")

    # 5. Burn subtitles and mix audio
    temp_master = os.path.join(temp_dir, "master.mp4")
    abs_ass = os.path.abspath(cfg["ass_file"]).replace("\\", "/")
    if ":" in abs_ass:
        drive, rest = abs_ass.split(":", 1)
        ass_filter_path = f"{drive}\\:{rest}"
    else:
        ass_filter_path = abs_ass

    fade_st = max(0.0, total_dur - 1.9)
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", cfg["fast_vo"],
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
    run_cmd(mix_cmd, f"Mixing Master with Burned Subtitles for {vid_id}")

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
    run_cmd(loudness_cmd, f"Applying Loudness Normalization to {vid_id}")

    # 7. Retag BT.709
    retag_cmd = [
        "python", ".agents/skills/ffmpeg-skill/scripts/color.py",
        final_output,
        "--retag", "bt709",
        "--overwrite"
    ]
    run_cmd(retag_cmd, f"Retagging BT.709 for {vid_id}")
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
    samples = cfg["contact_samples"]

    for i, (t, lbl) in enumerate(samples):
        kp = os.path.join(temp_dir, f"keyframe_{i}.png")
        cmd = ['ffmpeg', '-y', '-ss', str(t), '-i', final_output, '-vframes', '1', kp]
        subprocess.run(cmd, check=True)

    font_path = 'C:/Windows/Fonts/arialbd.ttf'
    font = ImageFont.truetype(font_path, 28) if os.path.exists(font_path) else ImageFont.load_default()
    tile_w, tile_h = 360, 640
    grid = Image.new('RGB', (tile_w * 3, tile_h * 2), (32, 32, 32))

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
    return final_output

def main():
    for cfg in VIDEOS_CONFIG:
        render_single_video(cfg)
    print("\nALL 3 VIDEOS SUCCESSFULLY PRODUCED!", flush=True)

if __name__ == "__main__":
    main()
