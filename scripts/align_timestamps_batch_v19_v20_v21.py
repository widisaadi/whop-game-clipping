import urllib.request
import json
import base64
import os
import time
import re

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VIDEOS = {
    "v19": {
        "audio": "temp/tongue_escape/voiceover_v19_fast.wav",
        "transcript": (
            "Bro, this might be the most illegal Roblox obby ever! "
            "You are trapped on a floating island, and jumping is completely banned! "
            "The only way across... is spitting out your own giant tongue as a solid bridge! "
            "Grind the speed gym, stack massive multipliers, and slide across raging lava to escape! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v20": {
        "audio": "temp/tongue_escape/voiceover_v20_fast.wav",
        "transcript": (
            "Nobody told me this Roblox obby gets this completely insane! "
            "You start with zero reach and can't even clear the first jump! "
            "But once you hit the x99 Hacker gym, your tongue gains thousands of studs in seconds! "
            "Dodge moving obstacles, soar over deadly lava, and conquer Stage 8 for 100 wins! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v21": {
        "audio": "temp/tongue_escape/voiceover_v21_fast.wav",
        "transcript": (
            "Stop grinding with a tiny tongue in Roblox right now! "
            "Here are three secret working codes to instantly get 15,000 free tongue and a 2x boost! "
            "Type WELCOME1 for 5k, BONUS500 for another 10k, and FREEBOOST to double your growth speed! "
            "Now you can bridge entire maps with zero effort! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    }
}

models = ["gemini-2.5-flash", "gemini-3-flash-preview"]

def parse_json_safely(raw):
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s)
        s = re.sub(r"\s*```$", "", s)
    try:
        return json.loads(s)
    except Exception:
        # Regex fallback for json objects
        pattern = re.compile(r'\{\s*"text"\s*:\s*"([^"]+)"\s*,\s*"start"\s*:\s*([0-9\.]+)\s*,\s*"end"\s*:\s*([0-9\.]+)\s*,\s*"highlight"\s*:\s*"([^"]+)"\s*\}')
        matches = pattern.findall(s)
        if matches:
            res = []
            for m in matches:
                res.append({
                    "text": m[0],
                    "start": float(m[1]),
                    "end": float(m[2]),
                    "highlight": m[3]
                })
            return res
        raise

def align_all():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    
    for key, info in VIDEOS.items():
        out_file = f"temp/tongue_escape/subtitle_phrases_{key}.json"
        if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
            print(f"Skipping {key}, already aligned: {out_file}")
            continue
            
        audio_path = info["audio"]
        transcript = info["transcript"]
        
        print(f"\n=======================================================")
        print(f"Aligning timestamps for {key}: {audio_path}")
        print(f"=======================================================")
        
        with open(audio_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
            
        prompt = f"""
Here is the exact audio transcript:
"{transcript}"

Analyze this audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "NOBODY TOLD ME", "COMPLETELY INSANE", "ZERO REACH", "FIRST JUMP", "x99 HACKER", "THOUSANDS OF STUDS", "STAGE 8", "+100 WINS", "+1 TONGUE ESCAPE", "LINK IS IN MY BIO", "STOP GRINDING", "WELCOME1", "BONUS500", "FREEBOOST")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, codes, and stage numbers in GOLD (e.g. "+1 TONGUE ESCAPE", "STAGE 8", "WELCOME1", "BONUS500", "FREEBOOST", "x99 HACKER")
- Highlight super mechanics and rewards in GREEN (e.g. "SOLID BRIDGE", "GIANT TONGUE", "MULTIPLIERS", "+100 WINS", "FREE TONGUE", "2X BOOST", "ZERO EFFORT")
- Highlight constraints, death traps, and challenges in RED (e.g. "COMPLETELY INSANE", "ZERO REACH", "DEADLY LAVA", "STOP GRINDING", "TINY TONGUE")
- Keep phrases short (1-3 words) for rapid kinetic pop animation.

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
        
        out_text = None
        for attempt in range(5):
            for model in models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
                print(f"[Attempt {attempt+1}] Requesting alignment from {model} for {key}...")
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
                        print(f"SUCCESS with {model} for {key}!")
                        break
                except Exception as e:
                    print(f"Model {model} failed: {e}")
                    time.sleep(2)
            if out_text:
                break
            time.sleep(3)
                
        if not out_text:
            raise RuntimeError(f"All alignment models failed for {key}!")
            
        phrases = parse_json_safely(out_text)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(phrases, f, indent=2)
        print(f"Saved {len(phrases)} phrases to {out_file}")

if __name__ == "__main__":
    align_all()
