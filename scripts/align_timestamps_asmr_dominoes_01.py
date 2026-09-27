import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/asmr_dominoes/voiceover_ad_01_fast.wav",
    "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_01.json",
    "transcript": (
        "This is what happens when you upgrade a basic domino into a literal black hole! "
        "At level one, you're placing five boring tiles for pocket change. "
        "Until you grab the drag brush, stretch out five hundred dominoes in three seconds, and crank the scale slider! "
        "Once we hit topple mode, the whole chain triggers cosmic multipliers. "
        "And at level nine ninety-nine, a massive singularity opens and swallows the entire map! "
        "Game is called ASMR Dominoes on Roblox, link in bio!"
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

Analyze this fast-paced breathless audio carefully (total duration is ~23.49 seconds).
Break down the speech into short 1-3 word punchy subtitle phrases for fast-paced kinetic captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "WHAT HAPPENS", "UPGRADE DOMINO", "LITERAL BLACK HOLE", "LEVEL ONE", "BORING TILES", "POCKET CHANGE", "DRAG BRUSH", "500 DOMINOES", "THREE SECONDS", "SCALE SLIDER", "TOPPLE MODE", "COSMIC MULTIPLIERS", "LEVEL 999", "MASSIVE SINGULARITY", "SWALLOWS ENTIRE MAP")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "500 DOMINOES", "LEVEL 999", "THREE SECONDS")
- Highlight mechanics/actions/rewards in GREEN (e.g. "DRAG BRUSH", "TOPPLE MODE", "SCALE SLIDER", "COSMIC MULTIPLIERS")
- Highlight alerts/dangers/insane features in RED (e.g. "LITERAL BLACK HOLE", "MASSIVE SINGULARITY", "SWALLOWS ENTIRE MAP")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly within the audio duration (0.0 to 23.49s) and strictly ordered.
- CRITICAL: Stop subtitle phrases before 19.5s (do not generate subtitle phrases for "Game is called ASMR Dominoes on Roblox, link in bio", because the visual endcard already clearly displays the title and LINK IN BIO).

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

    models = ["gemini-2.5-flash", "gemini-2.0-flash"]
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
                with urllib.request.urlopen(req, timeout=45) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                out_text = res["candidates"][0]["content"]["parts"][0]["text"]
                break
            except Exception as e:
                print(f"  Attempt {attempt+1} failed: {e}")
                time.sleep(2)
        if out_text:
            break

    if not out_text:
        print("Failed to align with Gemini API.")
        return False

    out_text = out_text.strip()
    if out_text.startswith("```json"):
        out_text = out_text[7:]
    if out_text.startswith("```"):
        out_text = out_text[3:]
    if out_text.endswith("```"):
        out_text = out_text[:-3]
    out_text = out_text.strip()

    phrases = json.loads(out_text)
    print(f"Successfully generated {len(phrases)} subtitle phrases!")

    # Filter out anything starting after 19.5s
    phrases = [p for p in phrases if p["start"] < 19.5]

    with open(CONFIG["out_json"], "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)

    print(f"Saved timestamps to {CONFIG['out_json']}")
    for p in phrases[:8]:
        print(f"  [{p['start']:.2f}s - {p['end']:.2f}s] ({p['highlight']}) {p['text']}")
    print("  ...")
    return True

if __name__ == "__main__":
    align_audio()
