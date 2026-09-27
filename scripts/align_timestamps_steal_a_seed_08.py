import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/steal_a_seed/voiceover_sas_08_fast.wav",
    "out_json": "temp/steal_a_seed/subtitle_phrases_sas_08.json",
    "transcript": (
        "DO NOT steal seeds in Steal a Seed's Desert without checking behind you! "
        "We grabbed the giant grey pillar with ten thousand speed, and the giant Brown Cactus chased us down! "
        "Then right before the border, a SECOND GIANT GREEN CACTUS jumped out to trap us! "
        "We juked both monsters, secured a clutch steal, and planted the Frost Mini Cactus in our farm! "
        "Now our garden prints over sixty thousand cash every second! "
        "Search Steal a Seed on Roblox and survive the desert ambush right now!"
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
- "text": uppercase subtitle text (e.g. "DO NOT STEAL", "STEAL A SEED", "DESERT", "10,000 SPEED", "BROWN CACTUS", "GREEN CACTUS", "CLUTCH STEAL", "FROST CACTUS", "+$60,000/SEC", "PLAY ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "STEAL A SEED", "10,000 SPEED", "+$60,000/SEC")
- Highlight mechanics/actions/rewards in GREEN (e.g. "CLUTCH STEAL", "FROST CACTUS", "IN OUR FARM", "GREY PILLAR")
- Highlight alerts/dangers/enemies in RED (e.g. "DO NOT STEAL", "BROWN CACTUS", "GREEN CACTUS", "TRAP US")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration (0.0 to ~22.28s) and strictly ordered.

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
