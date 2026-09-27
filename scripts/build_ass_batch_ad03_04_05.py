import json
import os

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

CONFIGS = [
    {
        "id": "03_asmr_dominoes_lava_magma_topple",
        "json": "temp/asmr_dominoes/subtitle_phrases_ad_03.json",
        "out_ass": "campaigns/asmr_dominoes/subtitles/03_asmr_dominoes_lava_magma_topple.ass",
        "endcard_phrase": "GAME IS CALLED"
    },
    {
        "id": "04_asmr_dominoes_broken_chain_save",
        "json": "temp/asmr_dominoes/subtitle_phrases_ad_04.json",
        "out_ass": "campaigns/asmr_dominoes/subtitles/04_asmr_dominoes_broken_chain_save.ass",
        "endcard_phrase": "GAME IS CALLED"
    },
    {
        "id": "05_asmr_dominoes_toilet_vs_singularity",
        "json": "temp/asmr_dominoes/subtitle_phrases_ad_05.json",
        "out_ass": "campaigns/asmr_dominoes/subtitles/05_asmr_dominoes_toilet_vs_singularity.ass",
        "endcard_phrase": "GAME IS CALLED"
    }
]

def generate_ass_one(cfg):
    json_path = cfg["json"]
    out_ass = cfg["out_ass"]
    os.makedirs(os.path.dirname(out_ass), exist_ok=True)
    
    with open(json_path, "r", encoding="utf-8") as f:
        phrases = json.load(f)
        
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
    
    # Determine endcard cutoff timestamp from the phrase "GAME IS"
    cutoff = 999.0
    for p in phrases:
        if ("GAME IS" in p["text"].upper() or "ASMR DOMINOES" in p["text"].upper()) and p["start"] > 15.0:
            cutoff = p["start"]
            break
            
    count = 0
    for p in phrases:
        if p["start"] >= cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        txt = p["text"].strip().upper()
        # Kinetic pop effect with elastic bounce on entrance
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        count += 1
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
        
    print(f"Generated clean ASS subtitle for {cfg['id']}: {out_ass} ({count} dialogues, stops at {cutoff:.2f}s before living endcard).")
    return cutoff

def main():
    cutoffs = {}
    for cfg in CONFIGS:
        cutoffs[cfg["id"]] = generate_ass_one(cfg)
    return cutoffs

if __name__ == "__main__":
    main()
