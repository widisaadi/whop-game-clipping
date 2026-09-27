import os
import urllib.request
import json
import base64

API_KEY = os.environ.get("GEMINI_API_KEY", "")
audio_path = "temp/asmr_dominoes/vo_03_test_fast.wav"

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "Bro, whatever you do, DO NOT topple the level 500 lava dominoes! "
    "Basic wooden tiles only drop fifty coins. "
    "Grab the drag brush to place hundreds of dominoes in three seconds! "
    "Hit topple mode and watch the burning chain trigger massive multipliers, "
    "unleashing a blinding divine light pillar! "
    "Play ASMR Dominoes on Roblox, link in pin comment!"
)

prompt = f"""
Here is the exact audio transcript:
"{transcript}"

The audio is 16.87 seconds long.
Break down the transcript into short, punchy 1-3 word kinetic subtitle phrases matching when they are actually spoken in the audio.
Output a valid JSON list:
[
  {{"text": "PHRASE", "start": 0.0, "end": 0.40, "highlight": "WHITE"}},
  ...
]
Highlights:
- Game name / numbers in GOLD ("LEVEL 500", "FIFTY COINS", "HUNDREDS OF", "THREE SECONDS", "ASMR DOMINOES")
- Actions / tools / rewards in GREEN ("DRAG BRUSH", "TOPPLE MODE", "BURNING CHAIN", "MASSIVE MULTIPLIERS", "PIN COMMENT")
- Danger / alert words in RED ("DO NOT", "LAVA DOMINOES", "DIVINE LIGHT PILLAR")
- Normal words in WHITE
"""

payload = {
    "contents": [{
        "parts": [
            {"text": prompt},
            {"inlineData": {"mimeType": "audio/wav", "data": audio_b64}}
        ]
    }]
}

req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req, timeout=30) as resp:
    res = json.loads(resp.read().decode("utf-8"))

raw_text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
if raw_text.startswith("```"):
    raw_text = raw_text.split("\n", 1)[1]
    if raw_text.endswith("```"):
        raw_text = raw_text.rsplit("\n", 1)[0]

phrases = json.loads(raw_text)
out_json = "temp/asmr_dominoes/subtitle_phrases_ad_03_clean.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(phrases, f, indent=2)

print(f"Successfully aligned {len(phrases)} phrases to {out_json}!")
for p in phrases:
    print(f"{p['start']:.2f}s - {p['end']:.2f}s: {p['text']} [{p['highlight']}]")
