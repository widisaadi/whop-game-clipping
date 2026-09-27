import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/tongue_escape/voiceover_v16.wav",
    "out_ass": "campaigns/tongue_escape/subtitles/captions_tongue_escape_v16.ass",
    "out_json": "temp/tongue_escape/subtitle_phrases_v16.json",
    "transcript": (
        "Why does literally everyone fail this jump in +1 Tongue Escape?! "
        "Most players think you can just hop your way across, but without enough tongue length, you drop straight into the lava! "
        "The secret is grinding the speed gym treadmills to stack massive multipliers, "
        "then spitting out your tongue to bridge the entire chasm in one shot! "
        "Dodge the crushing laser walls, conquer Stage 8, and flex on the global leaderboards! "
        "The game is called +1 Tongue Escape on Roblox, link is in my bio!"
    )
}

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

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

Analyze this fast-paced breathless audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "WHY DOES", "EVERYONE FAIL", "THIS JUMP", "+1 TONGUE ESCAPE", "SPEED GYM", "MASSIVE MULTIPLIERS", "STAGE 8")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big numbers, stages, and leaderboards in GOLD (e.g. "+1 TONGUE ESCAPE", "STAGE 8", "LEADERBOARDS")
- Highlight mechanics/features/actions in GREEN (e.g. "SPEED GYM", "MASSIVE MULTIPLIERS", "SPITTING OUT", "ONE SHOT")
- Highlight challenges/warnings/shocks in RED (e.g. "EVERYONE FAIL", "STRAIGHT INTO LAVA", "CRUSHING WALLS", "LASER WALLS")
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

    models = ["gemini-2.5-flash", "gemini-2.5-pro"]
    out_text = None

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        for attempt in range(3):
            print(f"Aligning v16 audio timestamps with {model} (attempt {attempt+1})...")
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
