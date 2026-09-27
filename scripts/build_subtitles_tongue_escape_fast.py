import json
import os

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    phrases_path = "temp/tongue_escape/subtitle_phrases_fast.json"
    with open(phrases_path, "r", encoding="utf-8") as f:
        phrases = json.load(f)

    out_dir = "campaigns/tongue_escape/subtitles"
    os.makedirs(out_dir, exist_ok=True)
    out_ass = os.path.join(out_dir, "captions_tongue_escape_fast.ass")

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HookHeader,Impact,54,&H0000FFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,3,0,1,7,4,8,60,60,220,1
Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1
Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = [
        r"Dialogue: 1,0:00:00.00,0:00:04.00,HookHeader,,0,0,0,,{\pos(540,240)\fscx105\fscy105}🔥 WEIRDEST ROBLOX GAME 🔥"
    ]

    style_map = {
        "WHITE": "CenterWhite",
        "GOLD": "CenterGold",
        "RED": "CenterRed",
        "GREEN": "CenterGreen"
    }

    # Position: exact center X=540, lowered by 15px below center Y=960+15=975
    pos_tag = r"{\pos(540,975)}"

    for p in phrases:
        start_str = format_ass_time(p["start"])
        end_str = format_ass_time(p["end"])
        style = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        text = p["text"].strip().upper()
        
        # Kinetic pop animation bounce (scale 115% -> 100%) combined with exact position (540, 975)
        anim_tag = r"{\pos(540,975)\t(0,60,\fscx115\fscy115)\t(60,120,\fscx100\fscy100)}"
        event_line = f"Dialogue: 2,{start_str},{end_str},{style},,0,0,0,,{anim_tag}{text}"
        events.append(event_line)

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated Fast ASS Subtitles with Center+15px (Y=975): {out_ass} ({len(events)} events)")

if __name__ == "__main__":
    main()
