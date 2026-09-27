import urllib.request
import json
import base64
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")
audio_path = "temp/tongue_escape/voiceover_v17_test.wav"

with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

transcript = (
    "Bro, I literally just found the most absurd Roblox game. "
    "In this game, your goal is to escape the island. But the only thing you can use is your own tongue. "
    "So you have to train your tongue to get super long, just to swing across crazy obstacles. "
    "And every time you beat a stage, you unlock weirder tongues. Bro, there is literally a tongue that lets you fly. "
    "The game is called Plus One Tongue Escape. "
    "And if you want to start on easy mode, use code BONUS500 to grab ten thousand free tongue power."
)

prompt = f"""
Here is the exact audio transcript:
"{transcript}"

Analyze this audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "BRO I LITERALLY", "JUST FOUND", "THE MOST ABSURD", "ROBLOX GAME", "ESCAPE THE ISLAND", "ONLY THING", "YOUR OWN TONGUE", "TRAIN YOUR TONGUE", "SUPER LONG", "CRAZY OBSTACLES", "BEAT A STAGE", "WEIRDER TONGUES", "LETS YOU FLY", "+1 TONGUE ESCAPE", "BONUS500", "10,000 FREE TONGUE")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big numbers, stages, and codes in GOLD (e.g. "+1 TONGUE ESCAPE", "BONUS500", "10,000 FREE TONGUE")
- Highlight mechanics/actions in GREEN (e.g. "TRAIN YOUR TONGUE", "SUPER LONG", "LETS YOU FLY", "SWING ACROSS")
- Highlight obstacles/shocks in RED (e.g. "MOST ABSURD", "CRAZY OBSTACLES", "ESCAPE THE ISLAND")
- Keep phrases short (1-3 words) for rapid kinetic popping.

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

models = ["gemini-2.5-pro", "gemini-3-flash-preview", "gemini-3.1-pro-preview", "gemini-3.5-flash"]
out_text = None

for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    print(f"Trying alignment with {model}...")
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
            print(f"SUCCESS with {model}!")
            break
    except Exception as e:
        print(f"Model {model} failed: {e}")

if not out_text:
    raise RuntimeError("All models failed!")

phrases = json.loads(out_text)
print(f"Received {len(phrases)} phrases!")
for p in phrases[:10]:
    print(f"[{p['start']:.2f}s - {p['end']:.2f}s] {p['text']} ({p.get('highlight', 'WHITE')})")
print("...")
for p in phrases[-5:]:
    print(f"[{p['start']:.2f}s - {p['end']:.2f}s] {p['text']} ({p.get('highlight', 'WHITE')})")

out_file = "temp/tongue_escape/subtitle_phrases_v17.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(phrases, f, indent=2)
print(f"Saved timestamps to {out_file}")
