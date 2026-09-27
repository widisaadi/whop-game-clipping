import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

audio_path = "temp/tongue_escape/voiceover_v10.wav"
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is the exact audio transcript:
"Nobody warned me about the crushing walls in +1 Tongue Escape! If you hesitate for even one second, you get squished straight into the lava! To survive this nightmare, you have to sprint to the gym trainers and unlock the Rainbow times thirty tongue multiplier! Then you spit out a lightning bridge right through the closing walls, rocket past giant arrows, and crush Stage 7 for a hundred bonus wins! Can you dodge the traps and beat Stage 7? Play +1 Tongue Escape on Roblox, link is in my bio, unless you're afraid because..."

Analyze this fast-paced audio carefully. Break down the speech up to the start of the CTA into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
NOTE: STOP all subtitles before the living endcard (at around 19.5 - 20.0s). DO NOT generate subtitles for "Play +1 Tongue Escape on Roblox, link is in my bio, unless you're afraid because...". The endcard handles the CTA visually.

For each phrase up to the end of gameplay, output:
- "text": uppercase subtitle text (e.g. "NOBODY WARNED ME", "CRUSHING WALLS!", "+1 TONGUE ESCAPE", "EVEN ONE SECOND", "INTO THE LAVA!", "SURVIVE THIS!", "GYM TRAINERS", "RAINBOW X30", "TONGUE MULTIPLIER!", "LIGHTNING BRIDGE", "CLOSING WALLS", "GIANT ARROWS", "CRUSH STAGE 7!", "100 BONUS WINS!", "BEAT STAGE 7?")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight key terms in GOLD (e.g. "+1 TONGUE ESCAPE", "RAINBOW X30", "STAGE 7!", "100 BONUS WINS!")
- Highlight mechanics/features in GREEN (e.g. "GYM TRAINERS", "LIGHTNING BRIDGE", "ROCKET PAST", "DODGE THE TRAPS")
- Highlight danger/fail in RED (e.g. "CRUSHING WALLS!", "INTO THE LAVA!", "SQUISHED!", "CLOSING WALLS", "NIGHTMARE")
- Keep phrases short (1-3 words) for rapid kinetic popping.

Return ONLY a valid JSON list of objects matching schema:
[
  {"text": "NOBODY WARNED ME", "start": 0.0, "end": 0.55, "highlight": "WHITE"},
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
        print(f"Aligning Video 10 audio timestamps with {model} (attempt {attempt+1})...")
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                out_text = data["candidates"][0]["content"]["parts"][0]["text"]
                break
        except Exception as e:
            print(f"Error with {model}: {e}")
            time.sleep(2)
    if out_text:
        break

cues = json.loads(out_text)
print(f"Parsed {len(cues)} subtitle cues successfully.")

# ASS Subtitle Generator adhering to BloxClips Patent
def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:01d}:{m:02d}:{s:05.2f}"

ass_content = """[Script Info]
Title: BloxClips Subtitles - Video 10
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CenterWhite,Impact,98,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,8,5,2,40,40,740,1
Style: CenterGold,Impact,102,&H0000D7FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1
Style: CenterRed,Impact,102,&H002020FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1
Style: CenterGreen,Impact,102,&H0030E020,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for c in cues:
    # Strict cutoff: no subtitles past 19.8s
    if c["start"] >= 19.8:
        continue
    end_time = min(c["end"], 19.8)
    hl = c.get("highlight", "WHITE")
    if hl == "GOLD":
        style = "CenterGold"
    elif hl == "RED":
        style = "CenterRed"
    elif hl == "GREEN":
        style = "CenterGreen"
    else:
        style = "CenterWhite"
        
    start_fmt = fmt_time(c["start"])
    end_fmt = fmt_time(end_time)
    text = c["text"]
    ass_content += f"Dialogue: 0,{start_fmt},{end_fmt},{style},,0,0,0,,{text}\n"

out_ass = "campaigns/tongue_escape/subtitles/captions_tongue_escape_v10.ass"
os.makedirs("campaigns/tongue_escape/subtitles", exist_ok=True)
with open(out_ass, "w", encoding="utf-8") as f:
    f.write(ass_content)

print(f"Wrote ASS subtitle file: {out_ass}")
