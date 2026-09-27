import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIG = {
    "audio": "temp/asmr_dominoes/voiceover_ad_06_fast.wav",
    "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_06.json",
    "transcript": (
        "This is the most hypnotic ASMR game on Roblox, where you can change the sound of every single domino you topple! "
        "Most players get bored of normal wooden clicks, but the secret shop lets you equip whisper pops, celery crunches, and wet mop sounds! "
        "Grab the drag brush to spawn a thousand galaxy dominoes in three seconds, and crank the scale slider to mammoth pillars! "
        "Trigger the chain reaction, and watch the whole spiral collapse into soap bubble explosions and a massive cosmic black hole! "
        "Are your ears ready? Game is called ASMR Dominoes on Roblox, link in bio!"
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

Analyze this fast-paced breathless audio carefully (duration ~16.83 seconds).
Break down the ENTIRE transcript into short, punchy 1-3 word kinetic subtitle phrases.
CRITICAL: EVERY SINGLE WORD from the transcript MUST be included in the phrases in sequential order! DO NOT SKIP ANY WORDS. There should be continuous captions covering the entire speech from 0.00s to the end of speech (~16.83s).

For each phrase, output:
- "text": uppercase subtitle phrase (1 to 3 words, e.g. "THIS IS", "THE MOST", "HYPNOTIC ASMR", "GAME ON ROBLOX,", "WHERE YOU CAN", "CHANGE THE SOUND", "OF EVERY", "SINGLE DOMINO", "YOU TOPPLE!", "MOST PLAYERS", "GET BORED OF", "WOODEN CLICKS,", "BUT THE", "SECRET SHOP", "LETS YOU EQUIP", "WHISPER POPS,", "CELERY CRUNCHES,", "AND WET MOP SOUNDS!", "GRAB THE", "DRAG BRUSH", "TO SPAWN", "1,000 GALAXY DOMINOES", "IN THREE SECONDS,", "AND CRANK", "THE SCALE SLIDER", "TO MAMMOTH PILLARS!", "TRIGGER THE", "CHAIN REACTION,", "AND WATCH", "THE WHOLE SPIRAL", "COLLAPSE INTO", "SOAP BUBBLE EXPLOSIONS", "AND A MASSIVE", "COSMIC BLACK HOLE!", "ARE YOUR EARS", "READY?", "GAME IS CALLED", "ASMR DOMINOES", "ON ROBLOX,", "LINK IN BIO!")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD (e.g. "1,000 GALAXY DOMINOES", "THREE SECONDS", "ASMR DOMINOES")
- Highlight mechanics/tools/actions in GREEN (e.g. "DRAG BRUSH", "SECRET SHOP", "CHAIN REACTION", "SCALE SLIDER", "LINK IN BIO!")
- Highlight crazy sensory features/alerts in RED (e.g. "HYPNOTIC ASMR", "WHISPER POPS,", "CELERY CRUNCHES,", "WET MOP SOUNDS!", "COSMIC BLACK HOLE!")
- Keep phrases short (1-3 words) for rapid kinetic popping.
- Ensure timestamps are strictly monotonically increasing, matching the actual spoken audio.
- The end timestamp of the final subtitle must not exceed 16.83s.

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
            for p in phrases[:10]:
                print(f"  [{p['start']:.2f}s - {p['end']:.2f}s] ({p['highlight']}) {p['text']}")
            return True
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")
            time.sleep(2)
            
    return False

if __name__ == "__main__":
    align_audio()
