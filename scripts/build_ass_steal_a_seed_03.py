import os

PHRASES = [
    {"text": "WE STARTED WITH", "start": 0.55, "end": 1.40, "highlight": "WHITE"},
    {"text": "ZERO SPEED!", "start": 1.40, "end": 2.45, "highlight": "RED"},
    {"text": "IN STEAL A SEED", "start": 2.45, "end": 3.15, "highlight": "GOLD"},
    
    {"text": "WALKING THIS SLOW", "start": 3.20, "end": 4.10, "highlight": "WHITE"},
    {"text": "MONSTER CATCHES US", "start": 4.10, "end": 5.40, "highlight": "RED"},
    {"text": "EVERY SINGLE TIME!", "start": 5.40, "end": 6.25, "highlight": "RED"},
    
    {"text": "PLACED TREADMILLS", "start": 6.25, "end": 7.35, "highlight": "WHITE"},
    {"text": "IN OUR GARDEN", "start": 7.35, "end": 8.00, "highlight": "WHITE"},
    {"text": "STACKED +5 SPEED", "start": 8.00, "end": 8.70, "highlight": "GOLD"},
    {"text": "PER SECOND!", "start": 8.70, "end": 9.45, "highlight": "GOLD"},
    
    {"text": "UPGRADED GREEN TRACK", "start": 9.45, "end": 10.60, "highlight": "GREEN"},
    {"text": "FOR +12 SPEED!", "start": 10.60, "end": 11.50, "highlight": "GOLD"},
    
    {"text": "SPEED EXPLODED", "start": 11.50, "end": 12.55, "highlight": "WHITE"},
    {"text": "OVER 21,000!", "start": 12.55, "end": 14.10, "highlight": "GOLD"},
    
    {"text": "LEGENDARY COCO CANNON", "start": 14.10, "end": 15.65, "highlight": "GREEN"},
    {"text": "+$50,000/SEC CASH!", "start": 15.65, "end": 17.05, "highlight": "GREEN"},
    
    {"text": "LITERALLY FLY", "start": 17.10, "end": 18.25, "highlight": "WHITE"},
    {"text": "ACROSS THE MAP!", "start": 18.25, "end": 19.10, "highlight": "GOLD"},
    {"text": "NOTHING TOUCHES US!", "start": 19.10, "end": 19.80, "highlight": "GREEN"},
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
    out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_03.ass"
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
    
    endcard_cutoff = 19.80
    
    for p in PHRASES:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        txt = p["text"].strip().upper()
        # Kinetic pop effect with scale bounce
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
        
    print(f"Generated clean ASS subtitle: {out_ass}")

if __name__ == "__main__":
    generate_ass()
