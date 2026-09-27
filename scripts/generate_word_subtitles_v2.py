import os
import re
from faster_whisper import WhisperModel

def clean_word(w):
    clean = re.sub(r"[^\w\s\?!]", "", w).strip().upper()
    return clean

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    audio_path = "temp/voiceover_v2.wav"
    print(f"Loading faster-whisper model for {audio_path}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    
    raw_words = []
    for segment in segments:
        for w in segment.words:
            raw_text = w.word.strip()
            clean_text = clean_word(raw_text)
            if clean_text:
                raw_words.append({
                    "start": w.start,
                    "end": max(w.end, w.start + 0.16),
                    "text": clean_text
                })

    print(f"Total raw words: {len(raw_words)}")

    grouped = []
    i = 0
    while i < len(raw_words):
        # Combo "HAVE GUNS"
        if i + 1 < len(raw_words) and "GUN" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": f"{raw_words[i]['text']} {raw_words[i+1]['text']}?!",
                "special": "red"
            })
            i += 2
        # Combo "HOW TO FISCH"
        elif i + 2 < len(raw_words) and raw_words[i]["text"] == "HOW" and raw_words[i+1]["text"] == "TO" and any(k in raw_words[i+2]["text"] for k in ["FISCH", "FISH"]):
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+2]["end"],
                "text": "HOW TO FISCH",
                "special": "gold"
            })
            i += 3
        # Combo "FIGHT BACK"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "FIGHT" and "BACK" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "FIGHT BACK!",
                "special": "red"
            })
            i += 2
        # Combo "REAL WEAPONS"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "REAL" and "WEAPON" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "REAL WEAPONS",
                "special": "green"
            })
            i += 2
        # Combo "BURRITO BAIT"
        elif i + 1 < len(raw_words) and "BURRITO" in raw_words[i]["text"] and "BAIT" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "BURRITO BAIT",
                "special": "green"
            })
            i += 2
        # Combo "SUN FISH BOSS"
        elif i + 2 < len(raw_words) and "SUN" in raw_words[i]["text"] and "FISH" in raw_words[i+1]["text"] and "BOSS" in raw_words[i+2]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+2]["end"],
                "text": "SUN FISH BOSS",
                "special": "gold"
            })
            i += 3
        # Combo "PIRANHA BOSS"
        elif i + 1 < len(raw_words) and "PIRANHA" in raw_words[i]["text"] and "BOSS" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "PIRANHA BOSS!",
                "special": "red"
            })
            i += 2
        # Combo "ON ROBLOX"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "ON" and "ROBLOX" in raw_words[i+1]["text"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "ON ROBLOX",
                "special": "gold"
            })
            i += 2
        # Combo "PLAY RIGHT NOW"
        elif i + 2 < len(raw_words) and raw_words[i]["text"] == "PLAY" and raw_words[i+1]["text"] in ["RIGHT", "FOR"] and any(k in raw_words[i+2]["text"] for k in ["NOW", "FREE"]):
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+2]["end"],
                "text": f"{raw_words[i]['text']} {raw_words[i+1]['text']} {raw_words[i+2]['text']}!",
                "special": "green"
            })
            i += 3
        else:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i]["end"],
                "text": raw_words[i]["text"],
                "special": None
            })
            i += 1

    # Smooth timing gaps
    for k in range(len(grouped) - 1):
        gap = grouped[k+1]["start"] - grouped[k]["end"]
        if 0 < gap < 0.12:
            grouped[k]["end"] = grouped[k+1]["start"]

    for item in grouped:
        print(f"[{item['start']:.2f}s - {item['end']:.2f}s] {item['text']}")

    os.makedirs("subtitles", exist_ok=True)
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: WordWhite,Impact,78,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,7,4,5,60,60,60,1",
        "Style: WordGold,Impact,86,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "Style: WordRed,Impact,86,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "Style: WordGreen,Impact,86,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,60,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    # Endcard transition happens at 22.5s to end (27.4s)
    for item in grouped:
        start_t = format_time(item["start"])
        end_t = format_time(item["end"])
        word = item["text"]

        # Positioning: in gameplay center (540, 980), in endcard below CTA (540, 1460)
        if item["start"] >= 23.0:
            pos = "\\pos(540,1460)"
        else:
            pos = "\\pos(540,980)"

        pop_effect = "{\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}"

        if item.get("special") == "gold":
            style = "WordGold"
        elif item.get("special") == "red":
            style = "WordRed"
        elif item.get("special") == "green":
            style = "WordGreen"
        elif any(k in word for k in ["GUNS", "BLAST", "DEADLY", "BOSS", "MUTANT"]):
            style = "WordRed"
        elif any(k in word for k in ["WEAPONS", "BURRITO", "GEAR", "BAIT", "UPGRADE"]):
            style = "WordGreen"
        elif any(k in word for k in ["ROBLOX", "SURVIVE", "LEGENDARY", "FISCH"]):
            style = "WordGold"
        else:
            style = "WordWhite"

        dialogue = f"Dialogue: 0,{start_t},{end_t},{style},,0,0,0,,{{{pos}}}{pop_effect}{word}"
        ass_lines.append(dialogue)

    out_path = "subtitles/captions_v2.ass"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))

    print(f"Generated {len(grouped)} dynamic word-by-word subtitle events in {out_path}!")

if __name__ == "__main__":
    main()
