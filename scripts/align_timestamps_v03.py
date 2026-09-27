import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

audio_path = "temp/tongue_escape/voiceover_v03.wav"
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is the exact audio transcript:
"Stop playing +1 Tongue Escape like a noob! Use these 3 secret working codes to get 15,000 free tongue studs and a 2x boost instantly! First, open the codes menu and type WELCOME1 for 5,000 free studs! Next, enter BONUS500 to claim 10,000 more! And finally, type FREEBOOST for an insane 30-minute double boost! Now you can skip the slow grind, launch across giant lava chasms, and crush Stage 7 for huge wins! Play +1 Tongue Escape on Roblox, link is in my bio!"

Analyze this fast-paced audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "CODE: WELCOME1")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Return ONLY a valid JSON list of objects matching schema:
[
  {"text": "STOP PLAYING", "start": 0.0, "end": 0.45, "highlight": "WHITE"},
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

print("Aligning Video 03 audio timestamps with Gemini 2.5 Flash...")
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    out_text = res["candidates"][0]["content"]["parts"][0]["text"]

phrases = json.loads(out_text)
print(f"Received {len(phrases)} timestamped phrases!")
for p in phrases:
    print(f"[{p['start']:05.2f}s - {p['end']:05.2f}s] ({p['highlight']}): {p['text']}")

out_json = "temp/tongue_escape/subtitle_phrases_v03.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(phrases, f, indent=2)

def fmt_time(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{m}:{s:02d}.{cs:02d}"

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
    "Style: HookHeader,Impact,54,&H0000FFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,3,0,1,7,4,8,60,60,220,1",
    "Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
    "Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    "Dialogue: 1,0:00:00.00,0:00:03.50,HookHeader,,0,0,0,,{\\pos(540,240)\\fscx105\\fscy105}🔥 SECRET WORKING CODES 🔥"
]

for p in phrases:
    st = fmt_time(p["start"])
    et = fmt_time(p["end"])
    sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
    txt = p["text"].strip().upper()
    ass_lines.append(f"Dialogue: 2,0:{st},0:{et},{sname},,0,0,0,,{{\\pos(540,975)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

ass_path = "campaigns/tongue_escape/subtitles/captions_tongue_escape_v03.ass"
with open(ass_path, "w", encoding="utf-8") as f:
    f.write("\n".join(ass_lines) + "\n")

print(f"Generated ASS subtitle at {ass_path} with {len(phrases)} phrases at Y=975.")
