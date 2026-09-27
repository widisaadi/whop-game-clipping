import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
mp3_path = "temp/steal_a_seed/voiceover_sas_10_fast.mp3"

with open(mp3_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "In this Roblox game, you have to steal giant seeds, outrun terrifying monsters, and build a millionaire garden tycoon! "
    "The catch? Giant boss monsters patrol every single zone, and if they catch you holding a seed, you lose everything! "
    "So you have to sneak in, grab the heavy seed block, and sprint for the border with the monster chasing you! "
    "Once you escape, you plant the seed in your plot to print insane cash, and hit the gym treadmills to blast past twenty thousand speed! "
    "Can you survive the heist? Search Steal a Seed on Roblox and play right now!"
)

prompt = f"""
Audio Transcript:
"{transcript}"

Analyze this audio carefully. Break down the spoken words into short 1-3 word punchy subtitle phrases for kinetic text pop.
For each phrase, output:
- text: uppercase string
- start: float seconds (2 decimals)
- end: float seconds (2 decimals)
- highlight: one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game name, 20,000 SPEED, MILLIONAIRE in GOLD
- Highlight STEAL SEEDS, PLANT SEED, INSANE CASH, GYM TREADMILLS in GREEN
- Highlight TERRIFYING MONSTERS, BOSS MONSTERS, LOSE EVERYTHING!, RUN! in RED
- Strictly keep all timestamps in range [0.0, 23.83]

Return JSON list:
[
  {{"text": "IN THIS ROBLOX GAME", "start": 0.0, "end": 0.95, "highlight": "WHITE"}},
  ...
]
"""

payload = {
    "contents": [{
        "parts": [
            {"inline_data": {"mime_type": "audio/mp3", "data": b64}},
            {"text": prompt}
        ]
    }],
    "generationConfig": {"responseMimeType": "application/json"}
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
print("Sending request to Gemini 2.5 Flash...")
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as resp:
    res = json.loads(resp.read().decode("utf-8"))
out = res["candidates"][0]["content"]["parts"][0]["text"]

with open("temp/steal_a_seed/subtitle_phrases_sas_10.json", "w", encoding="utf-8") as f:
    f.write(out)
print("Successfully aligned and saved subtitle_phrases_sas_10.json!")
