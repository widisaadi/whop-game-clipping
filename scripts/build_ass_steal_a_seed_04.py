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
    json_path = "temp/steal_a_seed/subtitle_phrases_sas_04.json"
    out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_04.ass"
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
        "Style: CenterWhite,Impact,98,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterGold,Impact,98,&H0000E1FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterRed,Impact,98,&H002424FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterGreen,Impact,98,&H003CFF00,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]
    
    ENDCARD_START = 21.00 # Strict BloxClips standard: subtitle stops before endcard
    
    count = 0
    for p in phrases:
        start = p["start"]
        end = p["end"]
        
        if start >= ENDCARD_START:
            continue
        if end > ENDCARD_START:
            end = ENDCARD_START
            
        style = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        st_str = fmt_time(start)
        et_str = fmt_time(end)
        text = p["text"].strip().upper()
        
        # Kinetic pop effect at baseline Y=1180 (center X=540)
        line = f"Dialogue: 0,{st_str},{et_str},{style},,0,0,0,,{{\\pos(540,1180)\\fscx112\\fscy112\\t(0,70,\\fscx100\\fscy100)}}{text}"
        ass_lines.append(line)
        count += 1
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
        
    print(f"Generated {count} subtitle events in {out_ass} (cutoff strictly before endcard at {ENDCARD_START}s)")

if __name__ == "__main__":
    generate_ass()
