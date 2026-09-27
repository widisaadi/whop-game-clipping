import json
import re

with open("temp/tongue_escape/whisper_words_v18.json", "r", encoding="utf-8") as f:
    words = json.load(f)

print(f"Total words in v18: {len(words)}")

# Group words into 2-4 word punchy subtitle units
chunks = []
cur = []
for idx, w in enumerate(words):
    cur.append(w)
    has_punct = any(p in w["word"] for p in [".", ",", "!", "?"])
    is_last = (idx == len(words) - 1)
    has_gap = False
    if not is_last:
        gap = words[idx+1]["start"] - w["end"]
        if gap > 0.22:
            has_gap = True

    if len(cur) >= 3 or has_punct or has_gap or is_last:
        st = cur[0]["start"]
        et = cur[-1]["end"]
        et = max(et, st + 0.35)
        text = " ".join(x["word"] for x in cur).strip()
        clean_text = re.sub(r"[^\w\s\+,'\-\!]", "", text).upper()
        
        # Color highlight detection
        highlight = "WHITE"
        if any(k in clean_text for k in ["ROBLOX", "+1", "TONGUE ESCAPE", "PLUS ONE", "BIO", "LINK IN BIO"]):
            highlight = "GOLD"
        elif any(k in clean_text for k in ["TRAIN", "FLY", "GRIND", "MULTIPLIERS", "STRETCH", "UPGRADES", "THOUSANDS"]):
            highlight = "GREEN"
        elif any(k in clean_text for k in ["ILLEGAL", "TRAPPED", "BANNED", "CRAZIER", "LASER WALLS", "LAVA"]):
            highlight = "RED"

        chunks.append({
            "text": clean_text,
            "start": round(st, 2),
            "end": round(et, 2),
            "highlight": highlight
        })
        cur = []

print(f"Generated {len(chunks)} subtitle chunks:")
for c in chunks:
    print(f"[{c['start']:05.2f}s - {c['end']:05.2f}s] ({c['highlight']:5s}) {c['text']}")

with open("temp/tongue_escape/subtitle_phrases_v18.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Saved to temp/tongue_escape/subtitle_phrases_v18.json")
