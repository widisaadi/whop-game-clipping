import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
mp3_path = "temp/steal_a_seed/voiceover_sas_12_fast.mp3"

with open(mp3_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "This is how we unlocked a one point seventeen million dollar garden in Steal a Seed, and equipped secret item shop weapons! "
    "When you enter the desert zone, the spiky cactus monster will wipe you out before you can even touch the seed! "
    "So you have to open the secret item shop, buy frozen grenades and bear traps, and equip the cyan laser trail to blaze at thirteen thousand speed! "
    "Once you plant your loot, glowing crystal golems take over, blasting your income past one point seventeen million dollars every single second! "
    "Can you survive the desert heist? Search Steal a Seed on Roblox and play right now!"
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
- Highlight game name, STEAL A SEED, 1.17 MILLION, 13,000 SPEED in GOLD
- Highlight UNLOCKED, SECRET WEAPONS, FROZEN GRENADES, BEAR TRAPS, CRYSTAL GOLEMS, PLAY RIGHT NOW in GREEN
- Highlight DESERT ZONE, SPIKY CACTUS MONSTER, WIPE YOU OUT, SURVIVE in RED
- Strictly keep all timestamps in range [0.0, 27.99]

Return JSON list:
[
  {{"text": "THIS IS HOW", "start": 0.0, "end": 0.55, "highlight": "WHITE"}},
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

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
print("Sending request to gemini-flash-latest for timestamp alignment...")
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=45) as resp:
    res = json.loads(resp.read().decode("utf-8"))
out = res["candidates"][0]["content"]["parts"][0]["text"]

with open("temp/steal_a_seed/subtitle_phrases_sas_12.json", "w", encoding="utf-8") as f:
    f.write(out)
print("Successfully aligned and saved subtitle_phrases_sas_12.json using gemini-flash-latest!")
