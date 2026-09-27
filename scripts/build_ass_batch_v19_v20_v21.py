import json
import os
import subprocess

VIDEOS = {
    "v19": "temp/tongue_escape/voiceover_v19_fast.wav",
    "v20": "temp/tongue_escape/voiceover_v20_fast.wav",
    "v21": "temp/tongue_escape/voiceover_v21_fast.wav",
}

def get_audio_duration(path):
    cmd = ["ffprobe", "-i", path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

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

def build_ass_files():
    for key, audio_path in VIDEOS.items():
        json_path = f"temp/tongue_escape/subtitle_phrases_{key}.json"
        if not os.path.exists(json_path):
            print(f"Skipping {key}, {json_path} does not exist.")
            continue
            
        audio_dur = get_audio_duration(audio_path)
        with open(json_path, "r", encoding="utf-8") as f:
            phrases = json.load(f)
            
        max_end = max(p["end"] for p in phrases)
        scale = 1.0
        if max_end > audio_dur and max_end > 0:
            scale = audio_dur / max_end
            print(f"{key}: Scaling timestamps by {scale:.4f} (max_end={max_end:.2f}s -> audio_dur={audio_dur:.2f}s)")
            
        for p in phrases:
            p["start"] = round(p["start"] * scale, 2)
            p["end"] = round(p["end"] * scale, 2)
            
        # Detect endcard cutoff
        endcard_cutoff = audio_dur
        for p in phrases:
            text_u = p["text"].upper()
            if any(k in text_u for k in ["PLAY", "+1 TONGUE ESCAPE", "PLUS ONE", "LINK IS IN MY BIO", "LINK IN BIO"]):
                endcard_cutoff = p["start"]
                break
                
        print(f"{key}: Audio Dur = {audio_dur:.2f}s | Endcard cutoff at {endcard_cutoff:.2f}s | Endcard Duration = {audio_dur - endcard_cutoff:.2f}s")
        
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
        
        for p in phrases:
            if p["start"] >= endcard_cutoff:
                continue
            st = fmt_time(p["start"])
            et = fmt_time(min(p["end"], endcard_cutoff))
            sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
            txt = p["text"].strip().upper()
            ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
            
        out_ass = f"campaigns/tongue_escape/subtitles/captions_tongue_escape_{key}.ass"
        os.makedirs(os.path.dirname(out_ass), exist_ok=True)
        with open(out_ass, "w", encoding="utf-8") as f:
            f.write("\n".join(ass_lines) + "\n")
        print(f"Generated clean ASS: {out_ass}\n")

if __name__ == "__main__":
    build_ass_files()
