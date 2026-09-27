import json
import os

phrases = [
    # Sentence 1: 0.15s - 5.18s
    {"text": "THIS LEGENDARY", "start": 0.15, "end": 0.70, "highlight": "WHITE"},
    {"text": "COCO CANNON PLANT", "start": 0.70, "end": 1.55, "highlight": "GOLD"},
    {"text": "PRINTS $50,000", "start": 1.55, "end": 2.09, "highlight": "GREEN"},
    {"text": "EVERY SINGLE SECOND", "start": 2.17, "end": 2.85, "highlight": "GREEN"},
    {"text": "IN STEAL A SEED!", "start": 2.85, "end": 3.55, "highlight": "GOLD"},
    {"text": "BUT TO STEAL IT", "start": 3.55, "end": 4.10, "highlight": "WHITE"},
    {"text": "YOU NEED OVER", "start": 4.10, "end": 4.55, "highlight": "WHITE"},
    {"text": "20,000 SPEED!", "start": 4.55, "end": 5.18, "highlight": "GOLD"},

    # Sentence 2: 5.28s - 8.87s
    {"text": "IF YOU SNEAK INTO", "start": 5.28, "end": 5.95, "highlight": "WHITE"},
    {"text": "THE DEEP DESERT ZONE", "start": 5.95, "end": 6.85, "highlight": "RED"},
    {"text": "WITH STARTER SPEED", "start": 6.85, "end": 7.55, "highlight": "RED"},
    {"text": "YOU WILL GET CAUGHT", "start": 7.55, "end": 8.15, "highlight": "RED"},
    {"text": "AND LOSE EVERYTHING!", "start": 8.15, "end": 8.87, "highlight": "RED"},

    # Sentence 3: 8.96s - 15.93s
    {"text": "SO YOU HAVE TO", "start": 8.96, "end": 9.43, "highlight": "WHITE"},
    {"text": "HIT THE GARDEN", "start": 9.53, "end": 10.15, "highlight": "WHITE"},
    {"text": "TREADMILL GYM", "start": 10.15, "end": 11.00, "highlight": "GREEN"},
    {"text": "STACKING PLUS TWELVE", "start": 11.00, "end": 11.79, "highlight": "GREEN"},
    {"text": "LIGHTNING MULTIPLIERS", "start": 11.87, "end": 12.85, "highlight": "GREEN"},
    {"text": "UNTIL YOUR SPEED", "start": 12.85, "end": 13.85, "highlight": "WHITE"},
    {"text": "BREAKS TWENTY-ONE", "start": 13.85, "end": 14.85, "highlight": "GOLD"},
    {"text": "THOUSAND SPEED!", "start": 14.85, "end": 15.93, "highlight": "GOLD"},

    # Sentence 4: 16.01s - 20.80s
    {"text": "NOW YOU CAN BLITZ", "start": 16.01, "end": 16.56, "highlight": "GREEN"},
    {"text": "PAST EVERY MONSTER", "start": 16.65, "end": 17.40, "highlight": "GREEN"},
    {"text": "CROSS THE BORDER", "start": 17.40, "end": 17.99, "highlight": "GOLD"},
    {"text": "FOR A GUARANTEED STEAL", "start": 18.09, "end": 19.10, "highlight": "GREEN"},
    {"text": "AND PLANT THE", "start": 19.10, "end": 19.65, "highlight": "WHITE"},
    {"text": "COCO CANNON", "start": 19.65, "end": 20.20, "highlight": "GOLD"},
    {"text": "TO PRINT MILLIONS!", "start": 20.20, "end": 20.80, "highlight": "GREEN"}
]

os.makedirs("temp/steal_a_seed", exist_ok=True)
with open("temp/steal_a_seed/subtitle_phrases_sas_13.json", "w", encoding="utf-8") as f:
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

out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_13.ass"
os.makedirs(os.path.dirname(out_ass), exist_ok=True)

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

ENDCARD_START = 20.80  # Living endcard starts at 20.80s

count = 0
for p in phrases:
    start = float(p["start"])
    end = float(p["end"])
    if start >= ENDCARD_START:
        continue
    if end > ENDCARD_START:
        end = ENDCARD_START
    style = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
    st_str = fmt_time(start)
    et_str = fmt_time(end)
    text = p["text"].strip().upper()
    line = f"Dialogue: 0,{st_str},{et_str},{style},,0,0,0,,{{\\pos(540,1180)\\fscx112\\fscy112\\t(0,70,\\fscx100\\fscy100)}}{text}"
    ass_lines.append(line)
    count += 1

with open(out_ass, "w", encoding="utf-8") as f:
    f.write("\n".join(ass_lines) + "\n")

print(f"Generated {count} subtitle events in {out_ass} (cutoff strictly at {ENDCARD_START}s)")
