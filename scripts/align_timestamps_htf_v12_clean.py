import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
audio_path = "temp/how_to_fisch/voiceover_htf_v12_clean_fast.wav"

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "This is the most unhinged fishing game in Roblox! "
    "In How to Fisch, you cast your rod, "
    "until a giant Sun Fish boss charges at you! "
    "The only way to survive: roll high-tier guns at the armory! "
    "Blast its health bar with your pistol, "
    "then steer your motorboat into open waters "
    "to hunt down colossal ocean titans! "
    "Search How to Fisch on Roblox!"
)

prompt = f"""
Here is the exact audio transcript:
"{transcript}"

Analyze this audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
Every spoken word MUST be included in the output. There must be zero omitted words.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "THIS IS", "THE MOST", "UNHINGED", "FISHING GAME", "IN ROBLOX", "IN HOW TO FISCH", "YOU CAST", "YOUR ROD", "UNTIL A GIANT", "SUN FISH BOSS", "CHARGES AT YOU", "THE ONLY WAY", "TO SURVIVE", "ROLL HIGH-TIER GUNS", "AT THE ARMORY", "BLAST ITS", "HEALTH BAR", "WITH YOUR PISTOL", "THEN STEER", "YOUR MOTORBOAT", "INTO OPEN WATERS", "TO HUNT DOWN", "COLOSSAL", "OCEAN TITANS", "SEARCH", "HOW TO FISCH", "ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title ("HOW TO FISCH"), "ROBLOX", search in GOLD
- Highlight weapons/loot/actions ("CAST", "ROD", "ROLL HIGH-TIER GUNS", "ARMORY", "PISTOL", "MOTORBOAT") in GREEN
- Highlight monsters/shocks/bosses ("UNHINGED", "GIANT", "SUN FISH BOSS", "HEALTH BAR", "OCEAN TITANS") in RED
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Subtitles must be strictly aligned with the audio timestamps from 0.0s to the end of speech.

Return ONLY a valid JSON list of objects matching schema:
[
  {{"text": "PHRASE HERE", "start": 0.0, "end": 0.40, "highlight": "WHITE"}},
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

models = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-3.1-pro-preview"]
out_text = None

for m in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={API_KEY}"
    print(f"Aligning timestamps with {m}...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            out_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"Success with {m}!")
            break
    except Exception as e:
        print(f"Failed with {m}: {e}")

if not out_text:
    raise RuntimeError("All models failed to align audio timestamps!")

data = json.loads(out_text)
out_file = "temp/how_to_fisch/subtitles_htf_v12_clean.json"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data)} subtitle chunks to {out_file}!")
for idx, c in enumerate(data):
    print(f"[{idx+1:02d}] {c['start']:05.2f}s - {c['end']:05.2f}s | {c['highlight']:5s} | {c['text']}")
