import json
import os

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    phrases_path = "temp/tongue_escape/subtitle_phrases_raw.json"
    with open(phrases_path, "r", encoding="utf-8") as f:
        phrases = json.load(f)

    out_dir = "campaigns/tongue_escape/subtitles"
    os.makedirs(out_dir, exist_ok=True)
    out_ass = os.path.join(out_dir, "captions_tongue_escape.ass")

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HookHeader,Impact,54,&H0000FFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,3,0,1,7,4,8,60,60,220,1
Style: WordWhite,Impact,92,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,2,60,60,420,1
Style: WordGold,Impact,98,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,2,60,60,420,1
Style: WordRed,Impact,98,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,2,60,60,420,1
Style: WordGreen,Impact,98,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,2,60,60,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = [
        r"Dialogue: 1,0:00:00.00,0:00:05.50,HookHeader,,0,0,0,,{\pos(540,240)\fscx105\fscy105}🔥 WEIRDEST ROBLOX GAME 🔥"
    ]

    style_map = {
        "WHITE": "WordWhite",
        "GOLD": "WordGold",
        "RED": "WordRed",
        "GREEN": "WordGreen"
    }

    for p in phrases:
        start_str = format_ass_time(p["start"])
        end_str = format_ass_time(p["end"])
        style = style_map.get(p.get("highlight", "WHITE"), "WordWhite")
        text = p["text"].strip().upper()
        
        # Pop animation tag: scale bounce 115% -> 100%
        pop_tag = r"{\t(0,70,\fscx115\fscy115)\t(70,140,\fscx100\fscy100)}"
        event_line = f"Dialogue: 2,{start_str},{end_str},{style},,0,0,0,,{pop_tag}{text}"
        events.append(event_line)

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated ASS Subtitles: {out_ass} with {len(events)} events.")

if __name__ == "__main__":
    main()
