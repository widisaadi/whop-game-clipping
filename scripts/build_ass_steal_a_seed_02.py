import os

PHRASES = [
    {"text": "STOP PLAYING", "start": 0.35, "end": 0.90, "highlight": "WHITE"},
    {"text": "STEAL A SEED", "start": 0.90, "end": 1.60, "highlight": "GOLD"},
    
    {"text": "BROKE WITH", "start": 1.70, "end": 2.35, "highlight": "WHITE"},
    {"text": "$0 CASH!", "start": 2.35, "end": 3.15, "highlight": "RED"},
    
    {"text": "EVERYONE STARTS", "start": 3.30, "end": 4.10, "highlight": "WHITE"},
    {"text": "WITH $0 DOLLARS", "start": 4.10, "end": 4.80, "highlight": "RED"},
    {"text": "AND LOCKED PLOTS", "start": 4.80, "end": 5.65, "highlight": "RED"},
    
    {"text": "DEVELOPERS DROPPED", "start": 5.75, "end": 6.75, "highlight": "WHITE"},
    {"text": "AN INSANE", "start": 6.75, "end": 7.25, "highlight": "WHITE"},
    {"text": "SECRET CODE!", "start": 7.25, "end": 7.95, "highlight": "GOLD"},
    
    {"text": "OPEN YOUR MENU", "start": 8.05, "end": 8.85, "highlight": "WHITE"},
    {"text": "TYPE IN 35KLIKES", "start": 8.85, "end": 10.15, "highlight": "GREEN"},
    {"text": "RIGHT NOW!", "start": 10.15, "end": 10.85, "highlight": "GOLD"},
    
    {"text": "TO INSTANTLY CLAIM", "start": 10.90, "end": 11.60, "highlight": "WHITE"},
    {"text": "250,000 CASH!", "start": 11.60, "end": 12.85, "highlight": "GREEN"},
    
    {"text": "BUY RARE", "start": 13.00, "end": 13.75, "highlight": "WHITE"},
    {"text": "WATER BUCKETS!", "start": 13.75, "end": 14.85, "highlight": "GREEN"},
    
    {"text": "UNLOCK PLOTS", "start": 14.95, "end": 15.75, "highlight": "GREEN"},
    {"text": "MAX TREADMILL", "start": 15.75, "end": 16.65, "highlight": "GOLD"},
    {"text": "SPEED!", "start": 16.65, "end": 17.45, "highlight": "GOLD"},
    
    {"text": "REDEEM BEFORE", "start": 17.55, "end": 18.15, "highlight": "WHITE"},
    {"text": "IT EXPIRES!", "start": 18.15, "end": 18.70, "highlight": "RED"},
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
    out_ass = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_02.ass"
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
    
    endcard_cutoff = 18.70
    
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
