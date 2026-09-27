import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/steal_a_seed/voiceover_sas_07_fast.wav",
    "out_json": "temp/steal_a_seed/subtitle_phrases_sas_07.json",
    "transcript": (
        "You're playing Steal a Seed all wrong if you're not using the Secret Item Shop! "
        "When the giant prickly Cactus Monster ambushed us in the Desert Zone, we used the shop to buy Frozen Grenades, Bear Traps, and Mythic Buckets that cut growth time by 80%! "
        "Then we unlocked the neon Cyan Laser Trail and hit thirteen thousand speed! "
        "We claimed the legendary Pumpkin Baron, and our garden prints over 1.1 MILLION cash per second! "
        "Search Steal a Seed on Roblox and dominate the game right now!"
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
- "text": uppercase subtitle text (e.g. "ALL WRONG", "STEAL A SEED", "SECRET ITEM SHOP", "CACTUS MONSTER", "DESERT ZONE", "FROZEN GRENADES", "BEAR TRAPS", "-80% TIME", "CYAN LASER TRAIL", "13,000 SPEED", "PUMPKIN BARON", "+$1.1M/SEC", "DOMINATE THE GAME", "PLAY ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "STEAL A SEED", "-80% TIME", "13,000 SPEED", "+$1.1M/SEC")
- Highlight mechanics/actions/rewards in GREEN (e.g. "SECRET ITEM SHOP", "FROZEN GRENADES", "BEAR TRAPS", "CYAN LASER TRAIL", "PUMPKIN BARON")
- Highlight alerts/dangers/enemies in RED (e.g. "ALL WRONG", "CACTUS MONSTER", "DESERT ZONE", "AMBUSHED US")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration (0.0 to ~22.49s) and strictly ordered.

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
                with urllib.request.urlopen(req, timeout=40) as resp:
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
    print(f"Extracted {len(phrases)} subtitle phrases.")
    
    with open(CONFIG["out_json"], "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)
    print(f"Saved phrases to {CONFIG['out_json']}")

if __name__ == "__main__":
    align_audio()
