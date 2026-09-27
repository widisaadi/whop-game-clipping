import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/steal_a_seed/voiceover_sas_09_fast.wav",
    "out_json": "temp/steal_a_seed/subtitle_phrases_sas_09.json",
    "transcript": (
        "We started with base 100 speed in Steal a Seed, but unlocked the secret to climbing the global leaderboard! "
        "At first you only have a wooden stick and zero cash, getting wiped out by giant pumpkin bosses! "
        "So we hit the gym treadmills, stacked lightning multipliers, and blasted past twenty thousand speed! "
        "We stole the rare glowing block, grew the massive electric cube, and skyrocketed up the Top Power Leaderboard! "
        "Search Steal a Seed on Roblox and claim your spot on the leaderboard right now!"
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
- "text": uppercase subtitle text (e.g. "BASE 100 SPEED", "STEAL A SEED", "SECRET UNLOCKED", "GLOBAL LEADERBOARD", "WOODEN STICK", "ZERO CASH", "PUMPKIN BOSS", "GYM TREADMILLS", "+LIGHTNING MULTIPLIER", "20,000 SPEED", "GLOWING BLOCK", "ELECTRIC CUBE", "TOP POWER", "PLAY ON ROBLOX")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "STEAL A SEED", "BASE 100 SPEED", "20,000 SPEED", "LEADERBOARD")
- Highlight mechanics/actions/rewards in GREEN (e.g. "GYM TREADMILLS", "LIGHTNING MULTIPLIER", "GLOWING BLOCK", "ELECTRIC CUBE")
- Highlight alerts/dangers/enemies in RED (e.g. "ZERO CASH", "WIPED OUT", "PUMPKIN BOSS")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration and strictly ordered.

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

    models = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"]
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
                with urllib.request.urlopen(req, timeout=60) as resp:
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
