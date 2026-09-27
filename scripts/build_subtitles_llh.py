import os

SUB_PATH = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate\subtitles\captions_01.ass"

ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,92,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,4,5,40,40,40,1
Style: HighlightRose,Impact,96,&H00B020FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,4,5,40,40,40,1
Style: HighlightGold,Impact,96,&H0020E5FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,8,4,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.25,0:00:02.30,Default,,0,0,0,,{\\pos(540,1260)\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}HE SWORE HE {\\c&H0020E5FF}HATED HER...{\\c&H00FFFFFF}
Dialogue: 0,0:00:02.80,0:00:05.60,Default,,0,0,0,,{\\pos(540,1260)\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}BUT {\\c&H00B020FF}ENEMIES{\\c&H00FFFFFF} DON'T LOOK AT EACH OTHER LIKE THIS.
Dialogue: 0,0:00:06.20,0:00:09.80,Default,,0,0,0,,{\\pos(540,1260)\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}THE MOMENT HE {\\c&H0020E5FF}PINNED HER{\\c&H00FFFFFF} TO THE WALL...
Dialogue: 0,0:00:10.25,0:00:14.50,Default,,0,0,0,,{\\pos(540,1260)\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}SHE FELL FIRST... BUT {\\c&H0033FF66}HE FELL HARDER.{\\c&H00FFFFFF}
"""

with open(SUB_PATH, "w", encoding="utf-8") as f:
    f.write(ass_content.strip())

print("ASS Subtitles generated at:", SUB_PATH)
