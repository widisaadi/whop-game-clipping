import os
import re
from faster_whisper import WhisperModel

HIGHLIGHT_WORDS = {
    "HOW TO FISCH", "THINK AGAIN", "ROBLOX", "SPIDER CRAB", "SUNFISH", 
    "BOSSES", "MONSTERS", "WEAPONS", "PLAY RIGHT NOW", "FLOPPY", "SHRIMP", "CLAMS"
}

def clean_word(w):
    clean = re.sub(r"[^\w\s]", "", w).strip().upper()
    if clean == "SALE":
        clean = "SAIL"
    return clean

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def main():
    audio_path = "temp/gemini_voiceover_achird.wav"
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

    # Smart groupers for impact phrases
    grouped = []
    i = 0
    while i < len(raw_words):
        # Check for 3-word combo "HOW TO FISCH"
        if i + 2 < len(raw_words) and raw_words[i]["text"] == "HOW" and raw_words[i+1]["text"] == "TO" and raw_words[i+2]["text"] in ["FISCH", "FISH"]:
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+2]["end"],
                "text": "HOW TO FISCH",
                "special": "gold"
            })
            i += 3
        # Check for 2-word combo "THINK AGAIN"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "THINK" and raw_words[i+1]["text"] == "AGAIN":
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "THINK AGAIN!",
                "special": "red"
            })
            i += 2
        # Check for 2-word combo "SPIDER CRAB"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "SPIDER" and raw_words[i+1]["text"] == "CRAB":
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "SPIDER CRAB!",
                "special": "red"
            })
            i += 2
        # Check for 2-word combo "ON ROBLOX"
        elif i + 1 < len(raw_words) and raw_words[i]["text"] == "ON" and raw_words[i+1]["text"] == "ROBLOX":
            grouped.append({
                "start": raw_words[i]["start"],
                "end": raw_words[i+1]["end"],
                "text": "ON ROBLOX",
                "special": "gold"
            })
            i += 2
        # Check for 3-word combo "PLAY RIGHT NOW"
        elif i + 2 < len(raw_words) and raw_words[i]["text"] == "PLAY" and raw_words[i+1]["text"] in ["RIGHT", "FOR"] and raw_words[i+2]["text"] in ["NOW", "FREE"]:
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

    # Print out all words with timestamps for timing inspection
    for item in grouped:
        print(f"[{item['start']:.2f}s - {item['end']:.2f}s] {item['text']}")

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

    # Find the start of the final CTA section (last occurrence of ON ROBLOX or PLAY)
    # The endcard will transition in around 27.5s
    for item in grouped:
        start_t = format_time(item["start"])
        end_t = format_time(item["end"])
        word = item["text"]

        # Position: center of screen (540, 980) during gameplay, below CTA (540, 1460) during endcard (>27.0s)
        if item["start"] >= 27.0:
            pos = "\\pos(540,1460)"
        else:
            pos = "\\pos(540,980)"

        # Pop-up animation tag: starts 25% bigger, springs down to 100% in 70ms
        pop_effect = "{\\fscx125\\fscy125\\t(0,70,\\fscx100\\fscy100)}"

        # Style selection
        if item.get("special") == "gold":
            style = "WordGold"
        elif item.get("special") == "red":
            style = "WordRed"
        elif item.get("special") == "green":
            style = "WordGreen"
        elif word in ["SHRIMP", "CLAMS", "ISLANDS", "WEAPONS", "MONSTERS", "GEAR", "BAIT"]:
            style = "WordGreen"
        elif word in ["FISHING", "ROD", "SURVIVE", "CASTING"]:
            style = "WordGold"
        else:
            style = "WordWhite"

        dialogue = f"Dialogue: 0,{start_t},{end_t},{style},,0,0,0,,{{{pos}}}{pop_effect}{word}"
        ass_lines.append(dialogue)

    out_path = "subtitles/captions_gemini_achird.ass"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))

    print(f"Generated {len(grouped)} dynamic word-by-word pop-up subtitle events in {out_path}!")

if __name__ == "__main__":
    main()
