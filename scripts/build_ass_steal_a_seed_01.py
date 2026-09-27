import os

PHRASES = [
    {"text": "BRO THIS MIGHT BE", "start": 0.00, "end": 0.70, "highlight": "WHITE"},
    {"text": "THE MOST INTENSE", "start": 0.70, "end": 1.60, "highlight": "WHITE"},
    {"text": "ROBLOX HEIST EVER!", "start": 1.60, "end": 2.45, "highlight": "GOLD"},
    
    {"text": "SNEAK INTO", "start": 2.50, "end": 3.40, "highlight": "WHITE"},
    {"text": "ENEMY TERRITORY", "start": 3.40, "end": 4.30, "highlight": "RED"},
    {"text": "STEAL GIANT SEEDS!", "start": 4.30, "end": 5.25, "highlight": "GREEN"},
    
    {"text": "IF THE MASSIVE", "start": 5.35, "end": 6.25, "highlight": "WHITE"},
    {"text": "ENRAGED MONSTER", "start": 6.25, "end": 7.15, "highlight": "RED"},
    {"text": "YOU LOSE EVERYTHING!", "start": 7.15, "end": 8.10, "highlight": "RED"},
    
    {"text": "THE SECOND YOU", "start": 8.20, "end": 9.05, "highlight": "WHITE"},
    {"text": "GRAB THE SEED", "start": 9.05, "end": 9.85, "highlight": "GREEN"},
    {"text": "HUGE ALERT SCREAMS", "start": 9.85, "end": 10.45, "highlight": "GOLD"},
    {"text": "RUN AWAY!!", "start": 10.45, "end": 11.05, "highlight": "RED"},
    
    {"text": "SPRINT ACROSS", "start": 11.10, "end": 11.90, "highlight": "WHITE"},
    {"text": "THE ENTIRE MAP", "start": 11.90, "end": 12.70, "highlight": "WHITE"},
    {"text": "CROSS THE BORDER", "start": 12.70, "end": 13.40, "highlight": "GREEN"},
    {"text": "SUCCESSFUL STEAL!", "start": 13.40, "end": 14.15, "highlight": "GREEN"},
    
    {"text": "PLANT STOLEN SEEDS", "start": 14.25, "end": 15.15, "highlight": "GREEN"},
    {"text": "AT YOUR BASE", "start": 15.15, "end": 16.05, "highlight": "WHITE"},
    {"text": "HARVEST MASSIVE CASH", "start": 16.05, "end": 17.05, "highlight": "GREEN"},
    {"text": "GARDEN TREADMILLS", "start": 17.05, "end": 18.05, "highlight": "GREEN"},
    {"text": "STACK OVER", "start": 18.05, "end": 19.10, "highlight": "WHITE"},
    {"text": "20,000 SPEED!", "start": 19.10, "end": 20.15, "highlight": "GOLD"},
    
    {"text": "UNLOCK LEGENDARY", "start": 20.25, "end": 21.25, "highlight": "GREEN"},
    {"text": "COCO CANNONS!", "start": 21.25, "end": 22.12, "highlight": "GREEN"},
]

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

def generate_ass():
    out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_01.ass"
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
        "Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]
    
    endcard_cutoff = 22.14
    for p in PHRASES:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        txt = p["text"].strip().upper()
        # Kinetic pop effect with elastic bounce on entrance
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
        
    print(f"Generated clean ASS subtitle: {out_ass} (stops at {endcard_cutoff:.2f}s before endcard).")

if __name__ == "__main__":
    generate_ass()
