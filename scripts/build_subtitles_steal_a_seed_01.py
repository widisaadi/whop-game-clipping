import os
import json
import re
from faster_whisper import WhisperModel

AUDIO_PATH = "temp/steal_a_seed/voiceover_sas_01_fast.wav"
OUT_ASS = "campaigns/steal_a_seed/subtitles/captions_steal_a_seed_01.ass"
WORDS_JSON = "temp/steal_a_seed/whisper_words_sas_01.json"
PHRASES_JSON = "temp/steal_a_seed/subtitle_phrases_sas_01.json"

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

style_map = {
    "WHITE": "CenterWhite",
    "GOLD": "CenterGold",
    "RED": "CenterRed",
    "GREEN": "CenterGreen"
}

def process_subtitles():
    if not os.path.exists(AUDIO_PATH):
        raise FileNotFoundError(f"Audio not found: {AUDIO_PATH}")

    print("Loading faster-whisper model (base, cpu, int8)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    print(f"Transcribing audio: {AUDIO_PATH}...")
    segments, info = model.transcribe(AUDIO_PATH, word_timestamps=True)
    words_data = []
    for s in segments:
        for w in s.words:
            words_data.append({
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3)
            })

    os.makedirs(os.path.dirname(WORDS_JSON), exist_ok=True)
    with open(WORDS_JSON, "w", encoding="utf-8") as f:
        json.dump(words_data, f, indent=2)
    print(f"Extracted {len(words_data)} words. Saved to {WORDS_JSON}")

    # Group words into 2-3 word punchy kinetic chunks
    chunks = []
    cur = []
    for idx, w in enumerate(words_data):
        cur.append(w)
        has_punct = any(p in w["word"] for p in [".", ",", "!", "?"])
        is_last = (idx == len(words_data) - 1)
        has_gap = False
        if not is_last:
            gap = words_data[idx+1]["start"] - w["end"]
            if gap > 0.18:
                has_gap = True

        if len(cur) >= 3 or has_punct or has_gap or is_last:
            st = cur[0]["start"]
            et = cur[-1]["end"]
            et = max(et, st + 0.30)
            text = " ".join(x["word"] for x in cur).strip()
            clean_text = re.sub(r"[^\w\s\+,'\-\!]", "", text).upper()

            # Highlight keywords
            highlight = "WHITE"
            if any(k in clean_text for k in ["ROBLOX", "STEAL A SEED", "20,000", "20000", "HEIST", "SPEED"]):
                highlight = "GOLD"
            elif any(k in clean_text for k in ["GIANT SEEDS", "SUCCESSFUL", "MASSIVE CASH", "PAYOUTS", "TREADMILLS", "LEGENDARY", "CANNONS", "DOMINATE"]):
                highlight = "GREEN"
            elif any(k in clean_text for k in ["ENRAGED", "MONSTER", "LOSE EVERYTHING", "RUN AWAY", "ALERT", "CATCHES"]):
                highlight = "RED"

            chunks.append({
                "text": clean_text,
                "start": round(st, 2),
                "end": round(et, 2),
                "highlight": highlight
            })
            cur = []

    with open(PHRASES_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    # Detect Endcard Cutoff: when "PLAY STEAL A SEED" or "ON ROBLOX" starts
    endcard_cutoff = 999.0
    for idx, c in enumerate(chunks):
        if any(k in c["text"] for k in ["PLAY STEAL A SEED", "STEAL A SEED ON ROBLOX"]):
            endcard_cutoff = c["start"]
            break

    # If not matched directly, find the last phrase mentioning "STEAL A SEED"
    if endcard_cutoff > 900.0:
        for idx in range(len(chunks)-1, -1, -1):
            if "STEAL A SEED" in chunks[idx]["text"]:
                endcard_cutoff = chunks[idx]["start"]
                break

    print(f"Detected Endcard Cutoff: {endcard_cutoff:.2f}s")

    # Build ASS file (Impact pop at Y=1180, Lower Gameplay Zone)
    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: CenterWhite,Impact,96,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1",
        "Style: CenterGold,Impact,102,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterRed,Impact,102,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "Style: CenterGreen,Impact,102,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for p in chunks:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        txt = p["text"].strip().upper()
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

    os.makedirs(os.path.dirname(OUT_ASS), exist_ok=True)
    with open(OUT_ASS, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")

    print(f"Generated clean ASS subtitle: {OUT_ASS}")
    return endcard_cutoff

if __name__ == "__main__":
    process_subtitles()
