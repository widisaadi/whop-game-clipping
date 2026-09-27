import json
import os

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def main():
    phrases_path = "temp/how_to_fisch/subtitle_phrases_htf_v10.json"
    out_ass = "campaigns/how_to_fisch/subtitles/captions_htf_v10.ass"
    
    with open(phrases_path, "r", encoding="utf-8") as f:
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
    
    # Endcard starts at 21.00s. Subtitles strictly stop before endcard.
    for p in phrases:
        if p["start"] >= 21.00:
            continue
        
        start_t = p["start"]
        end_t = min(p["end"], 21.00)
        
        start_str = format_ass_time(start_t)
        end_str = format_ass_time(end_t)
        
        style = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        text = p["text"]
        
        # Kinetic pop animation + exact position at X=540, Y=1180
        anim = r"{\pos(540,1180)\t(0,60,\fscx115\fscy115)\t(60,120,\fscx100\fscy100)}"
        line = f"Dialogue: 2,{start_str},{end_str},{style},,0,0,0,,{anim}{text}"
        ass_lines.append(line)
        
    os.makedirs(os.path.dirname(out_ass), exist_ok=True)
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
        
    print(f"Generated standardized ASS captions at {out_ass}")

if __name__ == "__main__":
    main()
