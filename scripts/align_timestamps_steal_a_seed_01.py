import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/steal_a_seed/voiceover_sas_01_fast.wav",
    "out_json": "temp/steal_a_seed/subtitle_phrases_sas_01.json",
    "transcript": (
        "Bro, this might be the most intense Roblox heist ever! "
        "You have to sneak into enemy territory and steal giant seeds, but if the massive enraged monster catches you, you lose everything! "
        "The second you grab the seed, a huge alert screams RUN AWAY, and you gotta sprint across the map to cross the border line for a successful steal! "
        "Then you plant your stolen seeds at your base plot, harvest massive cash payouts, and hit the garden treadmills to stack over 20,000 speed! "
        "Unlock legendary cannons and dominate the entire server! "
        "Play Steal a Seed on Roblox right now!"
    )
}

def align_audio():
    audio_path = CONFIG["audio"]
    if not os.path.exists(audio_path):
        print(f"Audio file {audio_path} not found!")
        return False

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = f"""
Here is the exact audio transcript:
"{CONFIG['transcript']}"

Analyze this fast-paced breathless audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced kinetic captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "MOST INTENSE", "ROBLOX HEIST", "STEAL GIANT SEEDS", "ENRAGED MONSTER", "RUN AWAY", "STEAL SUCCESSFUL", "20,000 SPEED", "STEAL A SEED", "PLAY ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "ROBLOX HEIST", "20,000 SPEED", "STEAL A SEED")
- Highlight mechanics/actions/rewards in GREEN (e.g. "STEAL GIANT SEEDS", "SUCCESSFUL STEAL", "MASSIVE CASH", "LEGENDARY CANNONS")
- Highlight alerts/dangers/enemies in RED (e.g. "ENRAGED MONSTER", "LOSE EVERYTHING", "RUN AWAY")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration (0.0 to ~24.6s) and strictly ordered.

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

    models = ["gemini-2.5-flash", "gemini-2.5-pro"]
    out_text = None

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        for attempt in range(3):
            print(f"Aligning audio timestamps with {model} (attempt {attempt+1})...")
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    out_text = res["candidates"][0]["content"]["parts"][0]["text"]
                    break
            except Exception as e:
                print(f"Error with {model}: {e}")
                time.sleep(3)
        if out_text:
            print(f"Successfully aligned using {model}!")
            break

    if not out_text:
        raise RuntimeError("Failed to get response from all models")

    phrases = json.loads(out_text)
    print(f"Received {len(phrases)} timestamped phrases!")
    for p in phrases:
        print(f"[{p['start']:.2f}s - {p['end']:.2f}s] {p['text']} ({p.get('highlight', 'WHITE')})")
    
    os.makedirs(os.path.dirname(CONFIG["out_json"]), exist_ok=True)
    with open(CONFIG["out_json"], "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)

    return phrases

if __name__ == "__main__":
    align_audio()
