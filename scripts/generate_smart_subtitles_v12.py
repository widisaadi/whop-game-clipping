import json
import os
import re

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    with open("temp/v12_whisper_words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    out_ass = "campaigns/how_to_fisch/subtitles/captions_v12_smart.ass"
    os.makedirs("campaigns/how_to_fisch/subtitles", exist_ok=True)

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HookHeader,Impact,52,&H0000FFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,3,0,1,6,3,8,60,60,180,1
Style: WordWhite,Impact,92,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1
Style: WordGold,Impact,98,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordRed,Impact,98,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: WordGreen,Impact,98,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1
Style: EndCardBig,Impact,80,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # 1. Top Hook Banner for first 7 seconds (Anti-Swipe Hook Header)
    events = [
        r"Dialogue: 1,0:00:00.00,0:00:07.50,HookHeader,,0,0,0,,{\pos(540,240)\fscx105\fscy105}🔥 SECRET ROBLOX DISCOVERY 🔥"
    ]

    # Smart 1-2 punchy word groupings crafted directly from whisper timestamps
    # Whisper words:
    # 01: This (0.00 - 0.44)
    # 02: new (0.44 - 0.74)
    # 03: Roblox (0.74 - 1.24)
    # 04: game (1.24 - 1.40)
    # 05: is (1.40 - 1.54)
    # 06: actually (1.54 - 1.78)
    # 07: way (1.78 - 2.08)
    # 08: more (2.08 - 2.30)
    # 09: fun (2.30 - 2.50)
    # 10: than (2.50 - 2.64)
    # 11: it (2.64 - 2.74)
    # 12: looks (2.74 - 3.00)
    
    # We create high-energy punchy groups:
    smart_groups = [
        # 0.0s - 3.15s: Hook
        (0.00, 0.74, "THIS NEW", "WordWhite", False),
        (0.74, 1.40, "ROBLOX GAME", "WordGold", False),
        (1.40, 2.08, "IS ACTUALLY", "WordWhite", False),
        (2.08, 2.50, "WAY MORE FUN", "WordRed", False),
        (2.50, 3.20, "THAN IT LOOKS!", "WordWhite", False),

        # 3.5s - 7.5s: Pier
        (3.50, 4.06, "WELCOME TO", "WordWhite", False),
        (4.06, 5.26, "HOW TO FISCH!", "WordGold", False),
        (5.26, 6.14, "START CATCHING", "WordWhite", False),
        (6.14, 6.92, "TINY FISCH", "WordGold", False),
        (6.92, 7.50, "FOR CASH...", "WordGreen", False),

        # 7.5s - 11.3s: Motorboat
        (7.58, 8.22, "UNTIL YOU BUY", "WordWhite", False),
        (8.22, 9.08, "THE MOTORBOAT!", "WordGreen", False),
        (9.08, 9.84, "AND CRUISE", "WordWhite", False),
        (9.84, 11.20, "UNCHARTED WATERS!", "WordGold", False),

        # 11.3s - 14.5s: Granny Shop
        (11.54, 12.60, "TRADE TO GRANNY", "WordGold", False),
        (12.60, 14.00, "BURRITO BAIT!", "WordGreen", False),
        (14.38, 15.50, "UNLOCK SHOTGUNS!", "WordGold", False),

        # 14.5s - 18.8s: Monster attack & Shootout
        (15.64, 16.46, "AND BLAST", "WordWhite", False),
        (16.46, 17.36, "MUTANT MONSTERS!", "WordRed", False),
        (17.36, 18.50, "CHARGING THE PIER!", "WordRed", False),

        # 18.8s - 24.6s: Stormy voyage & Colossal Titan Boss
        (18.88, 19.76, "SQUAD UP!", "WordGreen", False),
        (20.10, 21.44, "STORMY BOSS WATERS!", "WordWhite", False),
        (21.70, 22.82, "RAID COLOSSAL", "WordGold", False),
        (22.82, 23.36, "OCEAN TITANS!", "WordGold", False),
        (23.36, 24.30, "LEGENDARY BOUNTY!", "WordGreen", False),

        # 24.6s - 28.98s: Endcard CTA (Comfortable 2-part CTA)
        (24.66, 25.80, "CAN YOU SURVIVE?", "WordGold", True),
        (26.12, 27.50, "SEARCH: HOW TO FISCH", "WordGold", True),
        (27.50, 28.98, "PLAY ON ROBLOX NOW! 🎮", "WordGreen", True),
    ]

    for start_t, end_t, text, style, is_endcard in smart_groups:
        y_pos = 1460 if is_endcard else 980
        anim_tag = r"{\fscx115\fscy115\t(0,60,\fscx100\fscy100)}"
        pos_tag = f"{{\\pos(540,{y_pos})}}"
        start_str = format_time(start_t)
        end_str = format_time(end_t)
        line = f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{pos_tag}{anim_tag}{text}"
        events.append(line)

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated {len(events)} smart subtitle events in {out_ass}!")

if __name__ == "__main__":
    main()
