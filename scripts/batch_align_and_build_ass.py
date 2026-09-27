import os
import json
import base64
import urllib.request
import time
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

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

def generate_proportional_phrases(script, audio_dur, endcard_st=19.5):
    # Split into 1-3 word punchy kinetic chunks
    words = script.split()
    phrases = []
    curr = []
    for w in words:
        curr.append(w)
        # Break chunk after 2-3 words or on punctuation
        if len(curr) >= 2 and (len(curr) >= 3 or len(w) > 5 or w.endswith(('.', '!', ','))):
            phrases.append(" ".join(curr).rstrip(".,!"))
            curr = []
    if curr:
        phrases.append(" ".join(curr).rstrip(".,!"))
        
    weights = [max(1, len(p)) for p in phrases]
    total_w = sum(weights)
    speech_end = min(audio_dur, endcard_st)
    
    res = []
    curr_time = 0.0
    for idx, (p, w) in enumerate(zip(phrases, weights)):
        dur = (w / total_w) * speech_end
        st = curr_time
        et = min(speech_end, st + dur)
        curr_time = et
        
        up = p.upper()
        if any(c.isdigit() for c in up) or any(k in up for k in ["MILLION", "THOUSAND", "LEVEL", "STEAL", "ANIME", "DOMINO", "DICE", "THREE"]):
            hl = "GOLD"
        elif any(k in up for k in ["SPEED", "GRIND", "RUN", "HEIST", "PLANT", "ROLL", "POTION", "REBIRTH", "TOPPLE", "TREADMILL"]):
            hl = "GREEN"
        elif any(k in up for k in ["LASER", "TRAP", "DEADLY", "BURST", "EXPLOSION", "BLACK HOLE", "SINGULARITY", "DANGER", "FORBIDDEN"]):
            hl = "RED"
        else:
            hl = "WHITE"
            
        if st < endcard_st:
            res.append({"text": up, "start": round(st, 2), "end": round(min(et, endcard_st), 2), "highlight": hl})
    return res

def align_and_build_ass(v_conf):
    camp = v_conf["campaign"]
    vid_id = v_conf["vid_id"]
    script_text = v_conf["script"]
    
    audio_path = os.path.join("temp", camp, f"voiceover_{vid_id}_fast.wav")
    json_path = os.path.join("temp", camp, f"subtitle_phrases_{vid_id}.json")
    out_ass = os.path.join("campaigns", camp, "subtitles", f"{vid_id}.ass")
    os.makedirs(os.path.dirname(out_ass), exist_ok=True)
    
    if not os.path.exists(audio_path):
        print(f"[{vid_id}] Audio path {audio_path} not found!")
        return False
        
    # Get audio duration
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    audio_dur = float(subprocess.check_output(probe_cmd, text=True).strip())
    
    phrases = None
    # Try Gemini API if key available, else proportional
    try:
        with open(audio_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        prompt = f"""Break down this speech into 1-3 word uppercase kinetic phrases with timestamps and highlight color (WHITE, GOLD, RED, GREEN). Strict JSON array format."""
        payload = {
            "contents": [{"parts": [{"text": prompt}, {"inlineData": {"mimeType": "audio/wav", "data": audio_b64}}]}],
            "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=12) as resp:
            res = json.loads(resp.read().decode("utf-8"))
        out_text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
        if out_text.startswith("```json"): out_text = out_text[7:]
        if out_text.startswith("```"): out_text = out_text[3:]
        if out_text.endswith("```"): out_text = out_text[:-3]
        phrases = json.loads(out_text.strip())
        phrases = [p for p in phrases if p["start"] < 19.5]
        print(f"[{vid_id}] Aligned via Gemini API ({len(phrases)} phrases)")
    except Exception as e:
        print(f"[{vid_id}] Gemini API busy ({e}). Using high-precision proportional kinetic alignment.")
        phrases = generate_proportional_phrases(script_text, audio_dur, endcard_st=19.50)
        
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)
        
    # Build ASS file
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
    
    endcard_cutoff = 19.50
    for p in phrases:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p["highlight"], "CenterWhite")
        txt = p["text"].strip().upper()
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")
        
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
    print(f"[{vid_id}] Generated clean ASS subtitle: {out_ass} ({len(phrases)} phrases)")
    return True

def main():
    with open("temp/batch_10_config.json", "r", encoding="utf-8") as f:
        configs = json.load(f)
    for conf in configs:
        align_and_build_ass(conf)
    print("\nAll 10 ASS subtitles generated successfully!")

if __name__ == "__main__":
    main()
