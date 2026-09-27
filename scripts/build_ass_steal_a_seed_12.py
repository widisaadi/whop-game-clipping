import json
import os

phrases = [
    # Sentence 1: 0.21s - 6.37s
    {"text": "THIS IS HOW WE", "start": 0.21, "end": 0.90, "highlight": "WHITE"},
    {"text": "UNLOCKED A", "start": 0.90, "end": 1.45, "highlight": "GREEN"},
    {"text": "$1.17 MILLION", "start": 1.45, "end": 2.50, "highlight": "GOLD"},
    {"text": "DOLLAR GARDEN", "start": 2.50, "end": 3.20, "highlight": "WHITE"},
    {"text": "IN STEAL A SEED", "start": 3.20, "end": 4.25, "highlight": "GOLD"},
    {"text": "AND EQUIPPED", "start": 4.25, "end": 4.80, "highlight": "WHITE"},
    {"text": "SECRET ITEM SHOP", "start": 4.80, "end": 5.60, "highlight": "GREEN"},
    {"text": "WEAPONS!", "start": 5.60, "end": 6.37, "highlight": "GREEN"},

    # Sentence 2: 6.45s - 11.08s
    {"text": "WHEN YOU ENTER", "start": 6.45, "end": 7.15, "highlight": "WHITE"},
    {"text": "THE DESERT ZONE", "start": 7.15, "end": 8.00, "highlight": "RED"},
    {"text": "THE SPIKY", "start": 8.00, "end": 8.45, "highlight": "WHITE"},
    {"text": "CACTUS MONSTER", "start": 8.45, "end": 9.35, "highlight": "RED"},
    {"text": "WILL WIPE YOU OUT", "start": 9.35, "end": 10.15, "highlight": "RED"},
    {"text": "BEFORE YOU CAN", "start": 10.15, "end": 10.60, "highlight": "WHITE"},
    {"text": "TOUCH THE SEED!", "start": 10.60, "end": 11.08, "highlight": "RED"},

    # Sentence 3: 11.16s - 17.26s
    {"text": "SO YOU HAVE TO", "start": 11.16, "end": 11.75, "highlight": "WHITE"},
    {"text": "OPEN THE SECRET", "start": 11.75, "end": 12.40, "highlight": "WHITE"},
    {"text": "ITEM SHOP", "start": 12.40, "end": 13.00, "highlight": "GREEN"},
    {"text": "BUY FROZEN GRENADES", "start": 13.00, "end": 13.90, "highlight": "GREEN"},
    {"text": "AND BEAR TRAPS", "start": 13.90, "end": 14.65, "highlight": "GREEN"},
    {"text": "AND EQUIP", "start": 14.65, "end": 15.15, "highlight": "WHITE"},
    {"text": "THE CYAN LASER TRAIL", "start": 15.15, "end": 16.15, "highlight": "GOLD"},
    {"text": "TO BLAZE AT", "start": 16.15, "end": 16.65, "highlight": "WHITE"},
    {"text": "13,000 SPEED!", "start": 16.65, "end": 17.26, "highlight": "GOLD"},

    # Sentence 4: 17.35s - 23.48s
    {"text": "ONCE YOU PLANT", "start": 17.35, "end": 18.05, "highlight": "GREEN"},
    {"text": "YOUR LOOT", "start": 18.05, "end": 18.55, "highlight": "WHITE"},
    {"text": "GLOWING CRYSTAL", "start": 18.55, "end": 19.35, "highlight": "GREEN"},
    {"text": "GOLEMS TAKE OVER", "start": 19.35, "end": 20.25, "highlight": "GREEN"},
    {"text": "BLASTING YOUR INCOME", "start": 20.25, "end": 21.15, "highlight": "WHITE"},
    {"text": "PAST ONE POINT", "start": 21.15, "end": 21.75, "highlight": "WHITE"},
    {"text": "SEVENTEEN MILLION", "start": 21.75, "end": 22.50, "highlight": "GOLD"},
    {"text": "EVERY SINGLE SECOND!", "start": 22.50, "end": 23.48, "highlight": "GOLD"}
]

os.makedirs("temp/steal_a_seed", exist_ok=True)
with open("temp/steal_a_seed/subtitle_phrases_sas_12.json", "w", encoding="utf-8") as f:
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

out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_12.ass"
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

ENDCARD_START = 23.50  # Living endcard starts at 23.50s

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
