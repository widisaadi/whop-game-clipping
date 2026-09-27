import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

audio_path = "temp/how_to_fisch/voiceover_htf_v10.wav"
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is the exact audio transcript:
"Whatever you do, do NOT hook this fish in Roblox! In How to Fisch, you start off like a normal fishing simulator, casting your rod into peaceful waters... until an enraged giant Sun Fish boss literally leaps out of the ocean and charges straight at you! You have to roll high-tier guns at the fish armory, blast through its health bar with your pistol, and harvest rare loot! Then hop in your motorboat to hunt down legendary sea titans across the open ocean! Search How to Fisch on Roblox and play right now!"

Analyze this fast-paced audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "DO NOT HOOK", "HOW TO FISCH", "SUN FISH BOSS", "PISTOL SHOOTOUT")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight key terms & titles in GOLD (e.g. "HOW TO FISCH", "SUN FISH BOSS", "LEGENDARY SEA TITANS", "SEARCH:")
- Highlight mechanics & loot in GREEN (e.g. "CASTING YOUR ROD", "FISH ARMORY", "RARE LOOT", "MOTORBOAT", "PLAY RIGHT NOW!")
- Highlight danger & warnings in RED (e.g. "DO NOT HOOK", "CHARGES AT YOU!", "BLAST THROUGH", "SURVIVE")
- Keep phrases short (1-3 words) for rapid kinetic popping.

Return ONLY a valid JSON list of objects matching schema:
[
  {"text": "WHATEVER YOU DO", "start": 0.0, "end": 0.40, "highlight": "WHITE"},
  ...
]
"""

payload = {
    "contents": [
        {
            "parts": [
                {"inline_data": {"mime_type": "audio/wav", "data": audio_b64}},
                {"text": prompt}
            ]
        }
    ],
    "generationConfig": {
        "responseMimeType": "application/json"
    }
}

models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
out_text = None

for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    for attempt in range(3):
        print(f"Aligning How to Fisch Video 10 timestamps with {model} (attempt {attempt+1})...")
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                out_text = res["candidates"][0]["content"]["parts"][0]["text"]
                break
        except Exception as e:
            print(f"Error with {model}: {e}")
            time.sleep(3)
    if out_text:
        break

if not out_text:
    raise RuntimeError("Failed to get response from all Gemini models")

phrases = json.loads(out_text)
print(f"Received {len(phrases)} timestamped phrases!")
for p in phrases:
    print(f"[{p['start']:05.2f}s - {p['end']:05.2f}s] ({p['highlight']}): {p['text']}")

out_json = "temp/how_to_fisch/subtitle_phrases_htf_v10.json"
with open(out_json, "w", encoding="utf-8") as f:
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
    "WHITE": "WordWhite",
    "GOLD": "WordGold",
    "RED": "WordRed",
    "GREEN": "WordGreen"
}

ass_lines = [
    "[Script Info]",
    "ScriptType: v4.00+",
    "PlayResX: 1080",
    "PlayResY: 1920",
    "ScaledBorderAndShadow: yes",
    "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: HookHeader,Impact,52,&H0000FFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,3,0,1,6,3,8,60,60,180,1",
    "Style: WordWhite,Impact,92,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
    "Style: WordGold,Impact,98,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1",
    "Style: WordRed,Impact,98,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1",
    "Style: WordGreen,Impact,98,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,60,1",
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    "Dialogue: 1,0:00:00.00,0:00:03.40,HookHeader,,0,0,0,,{\\pos(540,240)\\fscx105\\fscy105}⚠️ DO NOT HOOK THIS FISH ⚠️"
]

# When endcard starts (~20s / 21s), CTA subtitle moves to \pos(540,1460)
for p in phrases:
    st = fmt_time(p["start"])
    et = fmt_time(p["end"])
    sname = style_map.get(p.get("highlight", "WHITE"), "WordWhite")
    txt = p["text"].strip().upper()
    
    # Check if this phrase is in the endcard CTA (starts around "SEARCH HOW TO FISCH" / 21.0s)
    if p["start"] >= 21.0:
        y_pos = 1460
    else:
        y_pos = 980
        
    ass_lines.append(f"Dialogue: 0,{st},{et},{sname},,0,0,0,,{{\\pos(540,{y_pos})}}{{\\fscx115\\fscy115\\t(0,60,\\fscx100\\fscy100)}}{txt}")

ass_path = "campaigns/how_to_fisch/subtitles/captions_htf_v10.ass"
os.makedirs(os.path.dirname(ass_path), exist_ok=True)
with open(ass_path, "w", encoding="utf-8") as f:
    f.write("\n".join(ass_lines) + "\n")

print(f"Generated clean ASS subtitle at {ass_path} for How to Fisch Video 10.")
