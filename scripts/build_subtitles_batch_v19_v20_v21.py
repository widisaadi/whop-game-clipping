import os
import json
import re
from faster_whisper import WhisperModel

VIDEOS = ["v19", "v20", "v21"]

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
    print("Loading faster-whisper model (base, cpu, int8)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    for key in VIDEOS:
        audio_path = f"temp/tongue_escape/voiceover_{key}_fast.wav"
        if not os.path.exists(audio_path):
            print(f"Skipping {key}, audio not found: {audio_path}")
            continue

        print(f"\n=======================================================")
        print(f"Transcribing {key}: {audio_path}")
        print(f"=======================================================")

        segments, info = model.transcribe(audio_path, word_timestamps=True)
        words_data = []
        for s in segments:
            for w in s.words:
                words_data.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3)
                })

        whisper_json = f"temp/tongue_escape/whisper_words_{key}.json"
        with open(whisper_json, "w", encoding="utf-8") as f:
            json.dump(words_data, f, indent=2)
        print(f"Extracted {len(words_data)} words. Saved to {whisper_json}")

        # Group words into 2-4 word punchy kinetic chunks
        chunks = []
        cur = []
        for idx, w in enumerate(words_data):
            cur.append(w)
            has_punct = any(p in w["word"] for p in [".", ",", "!", "?"])
            is_last = (idx == len(words_data) - 1)
            has_gap = False
            if not is_last:
                gap = words_data[idx+1]["start"] - w["end"]
                if gap > 0.20:
                    has_gap = True

            if len(cur) >= 3 or has_punct or has_gap or is_last:
                st = cur[0]["start"]
                et = cur[-1]["end"]
                et = max(et, st + 0.32)
                text = " ".join(x["word"] for x in cur).strip()
                clean_text = re.sub(r"[^\w\s\+,'\-\!]", "", text).upper()

                # Highlight keywords
                highlight = "WHITE"
                if any(k in clean_text for k in ["ROBLOX", "+1", "TONGUE ESCAPE", "PLUS ONE", "BIO", "LINK IN BIO", "STAGE 8", "WELCOME1", "BONUS500", "FREEBOOST"]):
                    highlight = "GOLD"
                elif any(k in clean_text for k in ["TRAIN", "FLY", "GRIND", "MULTIPLIERS", "STRETCH", "UPGRADES", "THOUSANDS", "5K", "10K", "2X", "BOOST", "FREE TONGUE", "SOLID BRIDGE"]):
                    highlight = "GREEN"
                elif any(k in clean_text for k in ["ILLEGAL", "TRAPPED", "BANNED", "CRAZIER", "LASER WALLS", "LAVA", "STOP GRINDING", "TINY TONGUE", "ZERO REACH", "FAIL"]):
                    highlight = "RED"

                chunks.append({
                    "text": clean_text,
                    "start": round(st, 2),
                    "end": round(et, 2),
                    "highlight": highlight
                })
                cur = []

        phrases_json = f"temp/tongue_escape/subtitle_phrases_{key}.json"
        with open(phrases_json, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)

        # Detect Endcard Cutoff: when "PLAY +1 TONGUE ESCAPE" or "LINK IS IN MY BIO" starts
        endcard_cutoff = 999.0
        for idx, c in enumerate(chunks):
            if any(k in c["text"] for k in ["PLAY", "+1 TONGUE ESCAPE", "LINK IS IN MY BIO", "LINK IN BIO"]):
                endcard_cutoff = c["start"]
                break

        print(f"Endcard cutoff for {key}: {endcard_cutoff:.2f}s")

        # Build ASS file
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

        out_ass = f"campaigns/tongue_escape/subtitles/captions_tongue_escape_{key}.ass"
        os.makedirs(os.path.dirname(out_ass), exist_ok=True)
        with open(out_ass, "w", encoding="utf-8") as f:
            f.write("\n".join(ass_lines) + "\n")

        print(f"Generated clean ASS subtitle: {out_ass}")

if __name__ == "__main__":
    process_subtitles()
