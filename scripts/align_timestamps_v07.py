import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

audio_path = "temp/tongue_escape/voiceover_v07.wav"
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is the exact audio transcript:
"Wait... why is this tongue bridge climbing straight into the sky?! In +1 Tongue Escape, you train your tongue on crazy x99 Hacker treadmills to build bridges over impossible gaps! You can even unlock elemental trails like Fire, Lightning, and Galaxy! But can you actually beat Stage 8? Play +1 Tongue Escape on Roblox, link is in my bio!"

Analyze this fast-paced audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "WAIT...", "WHY IS THIS", "TONGUE BRIDGE", "INTO THE SKY?!", "+1 TONGUE ESCAPE", "x99 HACKER", "TREADMILLS", "IMPOSSIBLE GAPS!", "FIRE, LIGHTNING", "AND GALAXY!", "BEAT STAGE 8?")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight key terms in GOLD (e.g. "+1 TONGUE ESCAPE", "x99 HACKER", "STAGE 8", "LINK IN BIO")
- Highlight mechanics/features in GREEN (e.g. "TONGUE BRIDGE", "INTO THE SKY?!", "FIRE, LIGHTNING", "GALAXY")
- Highlight questions/challenges in RED (e.g. "WAIT...", "WHY IS THIS", "IMPOSSIBLE GAPS!", "BEAT STAGE 8?")
- Keep phrases short (1-3 words) for rapid kinetic popping.

Return ONLY a valid JSON list of objects matching schema:
[
  {"text": "WAIT...", "start": 0.0, "end": 0.45, "highlight": "RED"},
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
        print(f"Aligning Video 07 audio timestamps with {model} (attempt {attempt+1})...")
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

out_json = "temp/tongue_escape/subtitle_phrases_v07.json"
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
    "WHITE": "CenterWhite",
    "GOLD": "CenterGold",
    "RED": "CenterRed",
    "GREEN": "CenterGreen"
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
    "Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
    "Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
]

# Gameplay subtitles strictly stop before Endcard takes over (Endcard at 14.50s - 15.00s or whenever CTA begins)
# Endcard starts around 14.0s - 14.5s when CTA begins
for p in phrases:
    # Stop subtitles when CTA starts or before endcard
    if p["start"] >= 14.20:
        continue
    st = fmt_time(p["start"])
    et = fmt_time(min(p["end"], 14.20))
    sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
    txt = p["text"].strip().upper()
    ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

ass_path = "campaigns/tongue_escape/subtitles/captions_tongue_escape_v07.ass"
os.makedirs(os.path.dirname(ass_path), exist_ok=True)
with open(ass_path, "w", encoding="utf-8") as f:
    f.write("\n".join(ass_lines) + "\n")

print(f"Generated clean ASS subtitle at {ass_path} at Y=1180.")
