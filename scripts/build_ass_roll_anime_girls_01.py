import json
import os

phrases = [
    # Sentence 1: 0.18s - 4.32s
    {"text": "IN THIS", "start": 0.18, "end": 0.65, "highlight": "WHITE"},
    {"text": "ROBLOX GAME,", "start": 0.65, "end": 1.25, "highlight": "GOLD"},
    {"text": "YOU ROLL DICE", "start": 1.25, "end": 1.95, "highlight": "GREEN"},
    {"text": "FOR ANIME GIRLS", "start": 1.95, "end": 2.85, "highlight": "GOLD"},
    {"text": "AND USE THEM", "start": 2.85, "end": 3.45, "highlight": "WHITE"},
    {"text": "TO MAKE MILLIONS!", "start": 3.45, "end": 4.32, "highlight": "GREEN"},

    # Sentence 2: 4.32s - 8.54s
    {"text": "YOU START WITH", "start": 4.32, "end": 4.90, "highlight": "WHITE"},
    {"text": "ZERO CASH", "start": 4.90, "end": 5.50, "highlight": "RED"},
    {"text": "ON AN EMPTY PLOT,", "start": 5.50, "end": 6.32, "highlight": "RED"},
    {"text": "SO YOU HAVE TO", "start": 6.32, "end": 6.85, "highlight": "WHITE"},
    {"text": "ROLL THE DICE", "start": 6.85, "end": 7.55, "highlight": "GREEN"},
    {"text": "TO UNLOCK", "start": 7.55, "end": 7.95, "highlight": "WHITE"},
    {"text": "YOUR FIRST CHARACTER!", "start": 7.95, "end": 8.54, "highlight": "GOLD"},

    # Sentence 3: 8.54s - 14.58s
    {"text": "PLACE THEM DOWN", "start": 8.54, "end": 9.35, "highlight": "GREEN"},
    {"text": "AND THEY PRINT", "start": 9.35, "end": 9.95, "highlight": "WHITE"},
    {"text": "PASSIVE MONEY", "start": 9.95, "end": 10.75, "highlight": "GREEN"},
    {"text": "EVERY SECOND,", "start": 10.75, "end": 11.55, "highlight": "GOLD"},
    {"text": "EVEN WHILE", "start": 11.55, "end": 12.15, "highlight": "WHITE"},
    {"text": "YOU ARE", "start": 12.15, "end": 12.55, "highlight": "WHITE"},
    {"text": "COMPLETELY OFFLINE!", "start": 12.55, "end": 14.58, "highlight": "RED"},

    # Sentence 4: 14.58s - 19.80s
    {"text": "STACK LUCK POTIONS", "start": 14.58, "end": 15.65, "highlight": "GREEN"},
    {"text": "TO PULL", "start": 15.65, "end": 16.05, "highlight": "WHITE"},
    {"text": "LEGENDARY DROPS,", "start": 16.05, "end": 16.95, "highlight": "GOLD"},
    {"text": "AND HIT REBIRTH", "start": 16.95, "end": 17.85, "highlight": "RED"},
    {"text": "TO UNLOCK", "start": 17.85, "end": 18.25, "highlight": "WHITE"},
    {"text": "MASSIVE PERMANENT", "start": 18.25, "end": 18.95, "highlight": "GOLD"},
    {"text": "CASH MULTIPLIERS!", "start": 18.95, "end": 19.80, "highlight": "GREEN"}
]

os.makedirs("temp/roll_anime_girls", exist_ok=True)
with open("temp/roll_anime_girls/subtitle_phrases_rag_01.json", "w", encoding="utf-8") as f:
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

out_ass = "campaigns/roll_anime_girls/subtitles/01_roll_anime_girls_rng_tycoon_secret_rolls.ass"
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

ENDCARD_START = 19.80  # Living endcard starts at 19.80s

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
