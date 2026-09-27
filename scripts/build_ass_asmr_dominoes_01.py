import json
import os

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

style_map = {
    "WHITE": "CenterWhite",
    "GOLD": "CenterGold",
    "RED": "CenterRed",
    "GREEN": "CenterGreen"
}

def generate_ass():
    json_path = "temp/asmr_dominoes/subtitle_phrases_ad_01.json"
    out_ass = "campaigns/asmr_dominoes/subtitles/01_asmr_dominoes_black_hole.ass"
    os.makedirs(os.path.dirname(out_ass), exist_ok=True)
    
    with open(json_path, "r", encoding="utf-8") as f:
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
    
    # Gameplay subtitles stop before Living Endcard starts at 20.00s
    endcard_cutoff = 20.00
    count = 0
    for p in phrases:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        txt = p["text"].strip().upper()
        # Kinetic pop effect with elastic bounce on entrance
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        count += 1
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
        
    print(f"Generated clean ASS subtitle with {count} dialogues: {out_ass} (stops at {endcard_cutoff:.2f}s before endcard).")

if __name__ == "__main__":
    generate_ass()
