import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
mp3_path = "temp/steal_a_seed/voiceover_sas_11_fast.mp3"

with open(mp3_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "Stop playing Steal a Seed with zero cash when you can claim a free OP Icefluff Seed and unlock the rare Wall Nut! "
    "Most players get stuck running around with just a stick, getting wiped out by giant patrol monsters! "
    "So you have to sneak into the rare plots, grab the massive Wall Nut seed, and claim thirty-nine dollars every single second! "
    "Once you plant it, your garden prints over sixty thousand cash a second, shooting you straight to the Top Power leaderboard! "
    "Can you build the richest garden? Search Steal a Seed on Roblox and play right now!"
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
- Highlight game name, STEAL A SEED, ICEFLUFF SEED, WALL NUT, TOP POWER in GOLD
- Highlight FREE OP, CLAIM, PLANT IT, 60,000 CASH, PLAY RIGHT NOW in GREEN
- Highlight ZERO CASH, JUST A STICK, WIPED OUT, GIANT PATROL MONSTERS in RED
- Strictly keep all timestamps in range [0.0, 24.15]

Return JSON list:
[
  {{"text": "STOP PLAYING", "start": 0.0, "end": 0.65, "highlight": "WHITE"}},
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
print("Sending request to Gemini 2.5 Flash for timestamp alignment...")
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=45) as resp:
    res = json.loads(resp.read().decode("utf-8"))
out = res["candidates"][0]["content"]["parts"][0]["text"]

with open("temp/steal_a_seed/subtitle_phrases_sas_11.json", "w", encoding="utf-8") as f:
    f.write(out)
print("Successfully aligned and saved subtitle_phrases_sas_11.json!")
