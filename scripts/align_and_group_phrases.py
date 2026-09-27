import os
import json
import re
from faster_whisper import WhisperModel

CONFIGS = [
    {
        "id": "07_asmr_dominoes_lvl1_vs_lvl999",
        "audio": "temp/asmr_dominoes/batch_07_08_09/07_asmr_dominoes_lvl1_vs_lvl999_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_07.json",
        "gold_words": ["LEVEL 999", "LEVEL 1", "LEVEL ONE", "FIFTY COINS", "ASMR DOMINOES", "ROBLOX", "LEADERBOARD"],
        "green_words": ["DRAG BRUSH", "TOPPLE MODE", "LINK IN BIO", "THREE SECONDS", "SPRINTING", "OBSIDIAN TILES"],
        "red_words": ["PATHETIC", "DO NOT", "INSANE PHYSICS", "DARK MATTER", "SINGULARITY", "HYPERSONIC"]
    },
    {
        "id": "08_asmr_dominoes_satisfying_bubble_pop",
        "audio": "temp/asmr_dominoes/batch_07_08_09/08_asmr_dominoes_satisfying_bubble_pop_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_08.json",
        "gold_words": ["BUBBLE DOMINO", "ROBLOX", "ASMR DOMINOES", "JACKPOT", "GOLDEN STAR"],
        "green_words": ["DRAG BRUSH", "TOPPLE MODE", "CINEMATIC CAM", "LINK IN BIO", "SLOW-MO", "CRISP STEREO"],
        "red_words": ["DO NOT", "BUBBLE WRAP", "TIDAL WAVE", "CANNOT LOOK AWAY", "MICRO CRUNCH"]
    },
    {
        "id": "09_asmr_dominoes_shop_secret_skins",
        "audio": "temp/asmr_dominoes/batch_07_08_09/09_asmr_dominoes_shop_secret_skins_fast.wav",
        "out_json": "temp/asmr_dominoes/subtitle_phrases_09.json",
        "gold_words": ["MILLION COINS", "GALAXY SKIN", "ROBLOX", "ASMR DOMINOES", "ZERO LAG"],
        "green_words": ["SOUND VAULT", "SPIRAL MAZE", "LINK IN BIO", "CRYSTAL DINGS", "CELERY CRACKS", "BAMBOO CLACKS"],
        "red_words": ["ILLEGAL DOMINO", "CARDBOARD", "COSMIC BLACK HOLE", "COLLAPSING", "BLACK HOLE"]
    }
]

def clean_word(w):
    return re.sub(r'[^a-zA-Z0-9\-\+\$]', '', w).upper()

def determine_highlight(text, gold_list, green_list, red_list):
    t = text.upper()
    for gw in gold_list:
        if gw in t:
            return "GOLD"
    for rw in red_list:
        if rw in t:
            return "RED"
    for grw in green_list:
        if grw in t:
            return "GREEN"
    return "WHITE"

def group_words_into_phrases(words, gold_list, green_list, red_list):
    phrases = []
    i = 0
    n = len(words)
    
    while i < n:
        w1 = words[i]
        text1 = w1['word'].strip()
        
        # Look ahead 1 or 2 words
        if i + 1 < n:
            w2 = words[i + 1]
            text2 = w2['word'].strip()
            
            # Check if 3 words fit comfortably (duration < 0.9s or word count <= 3)
            if i + 2 < n:
                w3 = words[i + 2]
                text3 = w3['word'].strip()
                dur_3 = float(w3['end']) - float(w1['start'])
                combo_3 = f"{text1} {text2} {text3}".strip()
                
                # Check if combo_3 contains a key phrase or is short
                if len(combo_3.split()) <= 3 and dur_3 <= 0.85:
                    hl = determine_highlight(combo_3, gold_list, green_list, red_list)
                    phrases.append({
                        "text": combo_3.upper(),
                        "start": round(float(w1['start']), 2),
                        "end": round(float(w3['end']), 2),
                        "highlight": hl
                    })
                    i += 3
                    continue
            
            # Pair 2 words
            dur_2 = float(w2['end']) - float(w1['start'])
            combo_2 = f"{text1} {text2}".strip()
            hl = determine_highlight(combo_2, gold_list, green_list, red_list)
            phrases.append({
                "text": combo_2.upper(),
                "start": round(float(w1['start']), 2),
                "end": round(float(w2['end']), 2),
                "highlight": hl
            })
            i += 2
        else:
            hl = determine_highlight(text1, gold_list, green_list, red_list)
            phrases.append({
                "text": text1.upper(),
                "start": round(float(w1['start']), 2),
                "end": round(float(w1['end']), 2),
                "highlight": hl
            })
            i += 1
            
    return phrases

def main():
    print("Loading faster-whisper base model on CPU...", flush=True)
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    for cfg in CONFIGS:
        print(f"\nAligning {cfg['id']}...", flush=True)
        segments, _ = model.transcribe(cfg['audio'], word_timestamps=True)
        words = []
        for segment in segments:
            for w in segment.words:
                words.append({
                    "word": w.word.strip(),
                    "start": float(w.start),
                    "end": float(w.end)
                })
        print(f"Transcribed {len(words)} words.", flush=True)
        
        phrases = group_words_into_phrases(words, cfg['gold_words'], cfg['green_words'], cfg['red_words'])
        print(f"Grouped into {len(phrases)} kinetic phrases.", flush=True)
        
        with open(cfg['out_json'], 'w', encoding='utf-8') as f:
            json.dump(phrases, f, indent=2)
        print(f"Saved: {cfg['out_json']}", flush=True)

if __name__ == "__main__":
    main()
