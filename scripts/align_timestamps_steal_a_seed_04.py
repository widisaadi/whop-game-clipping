import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/steal_a_seed/voiceover_sas_04_fast.wav",
    "out_json": "temp/steal_a_seed/subtitle_phrases_sas_04.json",
    "transcript": (
        "Bro, whatever you do in Steal a Seed, "
        "DO NOT enter the Desert Zone unless your speed is over ten thousand! "
        "Because the moment you grab the Thorn Seed, the giant cactus monster chases you down! "
        "With thirteen thousand speed, we cleared the red line and secured a successful steal! "
        "We planted it in our farm, generated sixty two thousand cash a second, "
        "and unlocked the legendary Coco Cannon printing half a million per second! "
        "Now we literally outrun everyone on the server! "
        "Search Steal a Seed on Roblox and build your dream farm right now!"
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
- "text": uppercase subtitle text (e.g. "WHATEVER YOU DO", "IN STEAL A SEED", "DO NOT ENTER", "DESERT ZONE", "10,000 SPEED", "THORN SEED", "CACTUS MONSTER", "13,000 SPEED", "SUCCESSFUL STEAL", "PLANTED IN FARM", "+$62,000/SEC", "COCO CANNON", "+$500,000/SEC", "OUTRUN EVERYONE", "STEAL A SEED", "PLAY ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "STEAL A SEED", "10,000 SPEED", "13,000 SPEED", "+$500,000/SEC")
- Highlight mechanics/actions/rewards in GREEN (e.g. "THORN SEED", "SUCCESSFUL STEAL", "+$62,000/SEC", "COCO CANNON", "DREAM FARM")
- Highlight alerts/dangers/enemies in RED (e.g. "DO NOT ENTER", "DESERT ZONE", "CACTUS MONSTER", "CHASES YOU DOWN")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration (0.0 to ~24.9s) and strictly ordered.

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
