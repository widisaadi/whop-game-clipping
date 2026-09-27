import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIGS = [
    {
        "id": "03_asmr_dominoes_lava_magma_topple",
        "audio": "temp/asmr_dominoes/voiceover_03_asmr_dominoes_lava_magma_topple_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_03.json",
        "transcript": (
            "Bro, whatever you do, DO NOT topple the level five hundred lava dominoes! "
            "Because the moment they fall, blazing molten magma literally melts the entire floor! "
            "Basic wooden tiles only drop fifty coins. "
            "Until you equip the volcano skin, grab the drag brush, and curve hundreds of fiery magma dominoes across the map! "
            "Hit topple mode, watch the burning chain trigger endless multiplier cheese stars, and unleash a blinding divine light pillar! "
            "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
        ),
        "gold_words": ["FIVE HUNDRED", "FIFTY COINS", "HUNDREDS OF", "ASMR DOMINOES"],
        "green_words": ["VOLCANO SKIN", "DRAG BRUSH", "TOPPLE MODE", "BURNING CHAIN", "MULTIPLIER CHEESE", "PINNED COMMENT"],
        "red_words": ["DO NOT", "LAVA DOMINOES", "MOLTEN MAGMA", "DIVINE LIGHT PILLAR"]
    },
    {
        "id": "04_asmr_dominoes_broken_chain_save",
        "audio": "temp/asmr_dominoes/voiceover_04_asmr_dominoes_broken_chain_save_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_04.json",
        "transcript": (
            "Bro, I almost ruined the biggest domino chain reaction on Roblox! "
            "Look at that massive missing gap, one single millimeter off and the whole run fails! "
            "Normal builders give up and lose all their streak multipliers. "
            "Not us! Grab the drag brush, sprint to the gap, and lay down fresh obsidian tiles before the wave hits! "
            "It connects! The chain sweeps through the giant spiral maze with zero lag, and crushes every multiplier record! "
            "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
        ),
        "gold_words": ["BIGGEST DOMINO", "ONE SINGLE", "ASMR DOMINOES"],
        "green_words": ["DRAG BRUSH", "OBSIDIAN TILES", "IT CONNECTS", "GIANT SPIRAL", "ZERO LAG", "PINNED COMMENT"],
        "red_words": ["ALMOST RUINED", "MISSING GAP", "WHOLE RUN FAILS", "MULTIPLIER RECORD"]
    },
    {
        "id": "05_asmr_dominoes_toilet_vs_singularity",
        "audio": "temp/asmr_dominoes/voiceover_05_asmr_dominoes_toilet_vs_singularity_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_ad_05.json",
        "transcript": (
            "Bro, who allowed the developers to add a literal TOILET domino to this game?! "
            "At level one, you're placing cute little tiles that float romantic red hearts. "
            "At level fifty, you unlock water ripple dominoes with crisp bamboo clacks. "
            "At level five hundred, it turns into an actual porcelain toilet that flushes the entire track! "
            "And at level nine ninety-nine, a cosmic singularity swallows the leaderboard and rips space-time apart! "
            "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
        ),
        "gold_words": ["LEVEL ONE", "LEVEL FIFTY", "LEVEL FIVE HUNDRED", "LEVEL NINE NINETY-NINE", "ASMR DOMINOES"],
        "green_words": ["RED HEARTS", "WATER RIPPLE", "BAMBOO CLACKS", "FLUSHES", "PINNED COMMENT"],
        "red_words": ["TOILET DOMINO", "PORCELAIN TOILET", "COSMIC SINGULARITY", "RIPS SPACE-TIME"]
    }
]

def align_one(cfg):
    audio_path = cfg["audio"]
    if not os.path.exists(audio_path):
        print(f"Audio file {audio_path} not found!")
        return False

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = f"""
Here is the exact audio transcript:
"{cfg['transcript']}"

Analyze this fast-paced breathless audio carefully.
Break down the ENTIRE transcript into short, punchy 1-3 word kinetic subtitle phrases.
CRITICAL: EVERY SINGLE WORD from the transcript MUST be included in the phrases in sequential order! DO NOT SKIP ANY WORDS. There should be continuous captions covering the entire speech from 0.00s to the end of speech.

For each phrase, output:
- "text": uppercase subtitle phrase (1 to 3 words)
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big stats, numbers in GOLD ({cfg['gold_words']})
- Highlight mechanics/actions/rewards in GREEN ({cfg['green_words']})
- Highlight alerts/dangers/insane sensory features in RED ({cfg['red_words']})
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
            print(f"Aligning {cfg['id']} with gemini-2.5-flash (attempt {attempt})...")
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            phrases = json.loads(raw_text)
            
            os.makedirs(os.path.dirname(cfg["out_json"]), exist_ok=True)
            with open(cfg["out_json"], "w", encoding="utf-8") as out:
                json.dump(phrases, out, indent=2)
                
            print(f"Successfully generated {len(phrases)} subtitle phrases for {cfg['id']}!")
            return True
        except Exception as e:
            print(f"Error on attempt {attempt}: {e}")
            time.sleep(2)
            
    return False

def main():
    for cfg in CONFIGS:
        align_one(cfg)

if __name__ == "__main__":
    main()
