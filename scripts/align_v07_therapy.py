import json
from faster_whisper import WhisperModel

GOLD_WORDS = ["ASMR DOMINOES", "ROBLOX", "1,000 TILES", "THOUSAND TILES", "PURE SENSORY BLISS", "GOLDEN MULTIPLIER", "PURE THERAPY"]
GREEN_WORDS = ["DRAG BRUSH", "CRUNCHY CELERY", "BAMBOO CLACKS", "BUBBLE POPS", "LINK IN PINNED COMMENT", "ZERO LAG"]
RED_WORDS = ["TOTAL RESET", "BORING CLICKS", "GIANT SPIRAL", "COLLAPSE"]

def determine_highlight(text):
    t = text.upper()
    for gw in GOLD_WORDS:
        if gw in t:
            return "GOLD"
    for rw in RED_WORDS:
        if rw in t:
            return "RED"
    for grw in GREEN_WORDS:
        if grw in t:
            return "GREEN"
    return "WHITE"

def group_words(words):
    phrases = []
    i = 0
    n = len(words)
    while i < n:
        w1 = words[i]
        t1 = w1['word'].strip()
        
        if i + 1 < n:
            w2 = words[i + 1]
            t2 = w2['word'].strip()
            
            if i + 2 < n:
                w3 = words[i + 2]
                t3 = w3['word'].strip()
                dur_3 = float(w3['end']) - float(w1['start'])
                combo_3 = f"{t1} {t2} {t3}".strip()
                if len(combo_3.split()) <= 3 and dur_3 <= 0.85:
                    phrases.append({
                        "text": combo_3.upper(),
                        "start": round(float(w1['start']), 2),
                        "end": round(float(w3['end']), 2),
                        "highlight": determine_highlight(combo_3)
                    })
                    i += 3
                    continue
            
            combo_2 = f"{t1} {t2}".strip()
            phrases.append({
                "text": combo_2.upper(),
                "start": round(float(w1['start']), 2),
                "end": round(float(w2['end']), 2),
                "highlight": determine_highlight(combo_2)
            })
            i += 2
        else:
            phrases.append({
                "text": t1.upper(),
                "start": round(float(w1['start']), 2),
                "end": round(float(w1['end']), 2),
                "highlight": determine_highlight(t1)
            })
            i += 1
            
    return phrases

def main():
    print("Loading Whisper model...", flush=True)
    model = WhisperModel("base", device="cpu", compute_type="int8")
    audio = "temp/asmr_dominoes/v07_therapy/vo_fast.wav"
    segments, _ = model.transcribe(audio, word_timestamps=True)
    
    words = []
    for s in segments:
        for w in s.words:
            words.append({"word": w.word.strip(), "start": float(w.start), "end": float(w.end)})
            print(f"{w.word}: {w.start:.2f} -> {w.end:.2f}", flush=True)
            
    phrases = group_words(words)
    out_json = "temp/asmr_dominoes/v07_therapy/subtitle_phrases.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)
    print(f"\nGrouped into {len(phrases)} phrases -> {out_json}", flush=True)

if __name__ == "__main__":
    main()
