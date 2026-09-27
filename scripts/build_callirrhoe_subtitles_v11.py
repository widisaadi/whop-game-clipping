import os

ASS_CONTENT = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WordWhite,Impact,80,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1
Style: WordGold,Impact,88,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordRed,Impact,88,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordGreen,Impact,88,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.30,0:00:02.10,WordWhite,,0,0,0,,{\\pos(540,980)\\fscx115\\fscy115\\t(0,60,\\fscx100\\fscy100)}WHATEVER YOU DO...
Dialogue: 0,0:00:02.10,0:00:04.70,WordRed,,0,0,0,,{\\pos(540,980)\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}DO NOT PLAY THIS GAME ALONE!
Dialogue: 0,0:00:05.10,0:00:06.80,WordWhite,,0,0,0,,{\\pos(540,980)\\fscx115\\fscy115\\t(0,60,\\fscx100\\fscy100)}YOU THINK IT'S A PEACEFUL FISHING GAME...
Dialogue: 0,0:00:06.80,0:00:08.50,WordGold,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}THINK AGAIN!
Dialogue: 0,0:00:08.50,0:00:11.00,WordRed,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}UNTIL THE OCEAN TURNS BLOOD RED...
Dialogue: 0,0:00:11.00,0:00:13.20,WordRed,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}BOILING FURIOUSLY!
Dialogue: 0,0:00:13.20,0:00:16.10,WordRed,,0,0,0,,{\\pos(540,980)\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}AS GIANT MONSTERS SWARM THE PIER!
Dialogue: 0,0:00:16.50,0:00:18.50,WordGold,,0,0,0,,{\\pos(540,980)\\fscx115\\fscy115\\t(0,60,\\fscx100\\fscy100)}DROP YOUR FISHING ROD!
Dialogue: 0,0:00:18.50,0:00:20.80,WordGold,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}PULL OUT HEAVY SHOTGUNS!
Dialogue: 0,0:00:20.80,0:00:22.90,WordWhite,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}BLAST THROUGH WAVES OF SEA BEASTS!
Dialogue: 0,0:00:23.10,0:00:25.20,WordGreen,,0,0,0,,{\\pos(540,980)\\fscx115\\fscy115\\t(0,60,\\fscx100\\fscy100)}JUMP INTO HIGH SPEED MOTORBOATS...
Dialogue: 0,0:00:25.20,0:00:27.50,WordGold,,0,0,0,,{\\pos(540,980)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}VOYAGE INTO STORMY BOSS WATERS!
Dialogue: 0,0:00:27.50,0:00:30.00,WordGold,,0,0,0,,{\\pos(540,980)\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}RAID COLOSSAL OCEAN TITANS!
Dialogue: 0,0:00:30.40,0:00:32.80,WordGold,,0,0,0,,{\\pos(540,1460)\\fscx120\\fscy120\\t(0,60,\\fscx100\\fscy100)}THINK YOU CAN SURVIVE THE DEEP?
Dialogue: 0,0:00:32.80,0:00:35.30,WordGreen,,0,0,0,,{\\pos(540,1460)\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}SEARCH HOW TO FISCH ON ROBLOX!
"""

def generate_subtitles():
    out_path = "campaigns/how_to_fisch/subtitles/captions_v11_callirrhoe.ass"
    os.makedirs("campaigns/how_to_fisch/subtitles", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ASS_CONTENT.strip() + "\n")
    print(f"Generated {out_path} successfully!")

if __name__ == "__main__":
    generate_subtitles()
