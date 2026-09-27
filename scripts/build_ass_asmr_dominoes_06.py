import json
import os

phrases = [
    # Sentence 1: 0.19s - 3.98s
    {"text": "THIS IS WHAT", "start": 0.19, "end": 0.70, "highlight": "WHITE"},
    {"text": "HAPPENS WHEN", "start": 0.70, "end": 1.20, "highlight": "WHITE"},
    {"text": "YOU BUILD THE", "start": 1.20, "end": 1.70, "highlight": "WHITE"},
    {"text": "BIGGEST", "start": 1.70, "end": 2.20, "highlight": "GOLD"},
    {"text": "DOMINO SPIRAL", "start": 2.20, "end": 3.00, "highlight": "GOLD"},
    {"text": "IN ROBLOX!", "start": 3.00, "end": 3.98, "highlight": "GREEN"},

    # Sentence 2: 3.98s - 9.38s
    {"text": "MOST PLAYERS", "start": 3.98, "end": 4.55, "highlight": "WHITE"},
    {"text": "ONLY USE", "start": 4.55, "end": 4.95, "highlight": "WHITE"},
    {"text": "WOODEN BLOCKS,", "start": 4.95, "end": 5.65, "highlight": "RED"},
    {"text": "BUT YOU CAN", "start": 5.65, "end": 6.10, "highlight": "WHITE"},
    {"text": "EQUIP CUSTOM", "start": 6.10, "end": 6.75, "highlight": "GREEN"},
    {"text": "SOUND EFFECTS", "start": 6.75, "end": 7.35, "highlight": "GREEN"},
    {"text": "LIKE CELERY CRUNCH,", "start": 7.35, "end": 8.00, "highlight": "GOLD"},
    {"text": "BAMBOO CLACKS,", "start": 8.00, "end": 8.65, "highlight": "GOLD"},
    {"text": "AND BUBBLE POPS!", "start": 8.65, "end": 9.38, "highlight": "RED"},

    # Sentence 3: 9.38s - 15.52s
    {"text": "GRAB THE", "start": 9.38, "end": 9.85, "highlight": "WHITE"},
    {"text": "DRAG BRUSH", "start": 9.85, "end": 10.65, "highlight": "GREEN"},
    {"text": "TO PLACE", "start": 10.65, "end": 11.20, "highlight": "WHITE"},
    {"text": "1,000 DOMINOES", "start": 11.20, "end": 12.35, "highlight": "GOLD"},
    {"text": "IN THREE SECONDS,", "start": 12.35, "end": 13.50, "highlight": "GOLD"},
    {"text": "AND CRANK", "start": 13.50, "end": 14.15, "highlight": "WHITE"},
    {"text": "THE SCALE SLIDER!", "start": 14.15, "end": 15.52, "highlight": "GREEN"},

    # Sentence 4: 15.52s - 19.92s
    {"text": "HIT TOPPLE MODE,", "start": 15.52, "end": 16.35, "highlight": "GREEN"},
    {"text": "TRIGGER THE", "start": 16.35, "end": 16.85, "highlight": "WHITE"},
    {"text": "CHAIN REACTION,", "start": 16.85, "end": 17.65, "highlight": "GOLD"},
    {"text": "AND WATCH", "start": 17.65, "end": 18.05, "highlight": "WHITE"},
    {"text": "THE ENTIRE SPIRAL", "start": 18.05, "end": 18.75, "highlight": "GOLD"},
    {"text": "COLLAPSE INTO", "start": 18.75, "end": 19.25, "highlight": "RED"},
    {"text": "A MASSIVE BLACK HOLE!", "start": 19.25, "end": 19.92, "highlight": "RED"}
]

os.makedirs("temp/asmr_dominoes", exist_ok=True)
with open("temp/asmr_dominoes/subtitle_phrases_ad_06.json", "w", encoding="utf-8") as f:
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

out_ass = "campaigns/asmr_dominoes/subtitles/06_asmr_dominoes_hypnotic_spiral_sounds.ass"
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

ENDCARD_START = 19.92  # Living endcard starts at 19.92s

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
