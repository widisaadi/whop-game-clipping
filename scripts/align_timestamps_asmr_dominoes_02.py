import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/asmr_dominoes/voiceover_ad_02_fast.wav",
    "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_02.json",
    "transcript": (
        "Bro, if you had a stressful day, this Roblox game is literally pure therapy! "
        "Because toppling dominoes releases giant floating rainbow bubbles! "
        "Instead of boring clicks, you can choose custom ASMR sounds like celery cracks, bamboo clacks, and bubble pops! "
        "Grab the drag brush to stretch out five hundred tiles in three seconds flat! "
        "Hit topple mode and watch the entire spiral collapse into the center with zero lag! "
        "Every single tile drops satisfying multipliers for pure sensory satisfaction! "
        "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
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

Analyze this fast-paced breathless audio carefully (duration ~27.96 seconds).
Break down the ENTIRE transcript into short, punchy 1-3 word kinetic subtitle phrases.
CRITICAL: EVERY SINGLE WORD from the transcript MUST be included in the phrases in sequential order! DO NOT SKIP ANY WORDS. There should be continuous captions covering the entire speech from 0.00s to the end of speech.

For each phrase, output:
- "text": uppercase subtitle phrase (1 to 3 words, e.g. "BRO IF YOU", "HAD A", "STRESSFUL DAY", "THIS ROBLOX GAME", "IS LITERALLY", "PURE THERAPY!", "BECAUSE TOPPLING", "DOMINOES RELEASES", "GIANT FLOATING", "RAINBOW BUBBLES!", "INSTEAD OF", "BORING CLICKS", "YOU CAN CHOOSE", "CUSTOM ASMR", "SOUNDS LIKE", "CELERY CRACKS", "BAMBOO CLACKS", "AND BUBBLE POPS!", "GRAB THE", "DRAG BRUSH", "TO STRETCH OUT", "500 TILES", "IN THREE", "SECONDS FLAT!", "HIT TOPPLE MODE", "AND WATCH", "THE ENTIRE SPIRAL", "COLLAPSE", "INTO THE CENTER", "WITH ZERO LAG!", "EVERY SINGLE TILE", "DROPS SATISFYING", "MULTIPLIERS", "FOR PURE", "SENSORY SATISFACTION!", "GAME IS CALLED", "ASMR DOMINOES", "ON ROBLOX", "LINK IN", "PINNED COMMENT!")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "500 TILES", "THREE SECONDS", "ASMR DOMINOES")
- Highlight mechanics/actions/rewards in GREEN (e.g. "DRAG BRUSH", "TOPPLE MODE", "RAINBOW BUBBLES", "ZERO LAG", "MULTIPLIERS", "PINNED COMMENT")
- Highlight alerts/dangers/insane sensory features in RED (e.g. "PURE THERAPY", "CELERY CRACKS", "BAMBOO CLACKS", "BUBBLE POPS", "SENSORY SATISFACTION")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly monotonically increasing, matching the actual spoken audio.

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
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "audio/wav",
                            "data": audio_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    for attempt in range(1, 4):
        try:
            print(f"Aligning audio timestamps with gemini-2.5-flash (attempt {attempt})...")
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            phrases = json.loads(raw_text)
            
            os.makedirs(os.path.dirname(CONFIG["out_json"]), exist_ok=True)
            with open(CONFIG["out_json"], "w", encoding="utf-8") as out:
                json.dump(phrases, out, indent=2)
                
            print(f"Successfully generated {len(phrases)} subtitle phrases!")
            print(f"Saved timestamps to {CONFIG['out_json']}")
            for p in phrases[:8]:
                print(f"  [{p['start']:.2f}s - {p['end']:.2f}s] ({p['highlight']}) {p['text']}")
            return True
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")
            time.sleep(2)
            
    return False

if __name__ == "__main__":
    align_audio()
