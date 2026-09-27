import json
import os

# Subtitle phrases aligned with exact speech timings
# Segment 0: 0.00s - 2.85s
# Segment 1: 2.85s - 5.45s
# Segment 2: 5.45s - 8.55s
# Segment 3: 8.55s - 11.35s
# Segment 4: 11.35s - 13.85s
# Segment 5: 13.85s - 15.70s
# Segment 6 (Endcard): 15.70s - 19.60s (subtitles STOP at 15.70s!)

phrases = [
    # Beat 1: Hook (0.00s - 2.85s)
    {"text": "IN ROBLOX,", "start": 0.00, "end": 0.65, "highlight": "WHITE"},
    {"text": "FISHING WILL", "start": 0.65, "end": 1.25, "highlight": "WHITE"},
    {"text": "LITERALLY", "start": 1.25, "end": 1.80, "highlight": "GOLD"},
    {"text": "GET YOU", "start": 1.80, "end": 2.20, "highlight": "WHITE"},
    {"text": "ATTACKED!", "start": 2.20, "end": 2.85, "highlight": "RED"},

    # Beat 2: Core Constraint / Premise (2.85s - 5.45s)
    {"text": "IN HOW TO FISCH", "start": 2.85, "end": 3.75, "highlight": "GOLD"},
    {"text": "YOU CAST", "start": 3.75, "end": 4.25, "highlight": "GREEN"},
    {"text": "YOUR ROD", "start": 4.25, "end": 4.80, "highlight": "GREEN"},
    {"text": "FOR A CALM CATCH", "start": 4.80, "end": 5.45, "highlight": "WHITE"},

    # Beat 3: Monster Attack (5.45s - 8.55s)
    {"text": "UNTIL A MUTANT", "start": 5.45, "end": 6.20, "highlight": "WHITE"},
    {"text": "PIRANHA BOSS", "start": 6.20, "end": 7.05, "highlight": "RED"},
    {"text": "LEAPS OUT", "start": 7.05, "end": 7.65, "highlight": "RED"},
    {"text": "TO EAT YOU", "start": 7.65, "end": 8.05, "highlight": "RED"},
    {"text": "ALIVE!", "start": 8.05, "end": 8.55, "highlight": "RED"},

    # Beat 4A: Upgrading Gear at Granny (8.55s - 11.35s)
    {"text": "SPRINT TO GRANNY", "start": 8.55, "end": 9.40, "highlight": "GREEN"},
    {"text": "TO BUY SHOTGUNS", "start": 9.40, "end": 10.35, "highlight": "GOLD"},
    {"text": "AND LETHAL BAIT", "start": 10.35, "end": 11.35, "highlight": "GREEN"},

    # Beat 4B: Iron Sights Boss Shootout (11.35s - 13.85s)
    {"text": "THEN LOCK", "start": 11.35, "end": 11.85, "highlight": "WHITE"},
    {"text": "YOUR IRON SIGHTS", "start": 11.85, "end": 12.65, "highlight": "GOLD"},
    {"text": "TO WIPE OUT", "start": 12.65, "end": 13.15, "highlight": "RED"},
    {"text": "ITS HEALTH BAR!", "start": 13.15, "end": 13.85, "highlight": "RED"},

    # Beat 5: Ocean Titan Motorboat (13.85s - 15.70s)
    {"text": "HOP INTO", "start": 13.85, "end": 14.30, "highlight": "WHITE"},
    {"text": "YOUR MOTORBOAT", "start": 14.30, "end": 14.95, "highlight": "GREEN"},
    {"text": "TO RAID", "start": 14.95, "end": 15.30, "highlight": "WHITE"},
    {"text": "OCEAN TITANS!", "start": 15.30, "end": 15.70, "highlight": "RED"}
]

os.makedirs("temp/how_to_fisch", exist_ok=True)
json_path = "temp/how_to_fisch/subtitles_htf_v13.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(phrases, f, indent=2)

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

endcard_cutoff = 15.70
for p in phrases:
    if p["start"] >= endcard_cutoff:
        continue
    st = fmt_time(p["start"])
    et = fmt_time(min(p["end"], endcard_cutoff))
    sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
    txt = p["text"].strip().upper()
    ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

out_ass = "campaigns/how_to_fisch/subtitles/captions_how_to_fisch_v13.ass"
os.makedirs(os.path.dirname(out_ass), exist_ok=True)
with open(out_ass, "w", encoding="utf-8") as f:
    f.write("\n".join(ass_lines) + "\n")

print(f"Generated clean ASS subtitle at {out_ass} stopping cleanly before endcard at {endcard_cutoff}s.")
