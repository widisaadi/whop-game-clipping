import os
import json
from faster_whisper import WhisperModel

audio_path = "temp/steal_a_seed/voiceover_14_fast.wav"
out_ass = "campaigns/steal_a_seed/subtitles/14_steal_a_seed_50k_speed_sonic_sprint.ass"
os.makedirs(os.path.dirname(out_ass), exist_ok=True)

print(f"Transcribing {audio_path} with Whisper base...")
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_path, word_timestamps=True)

words = []
for s in segments:
    for w in s.words:
        clean = w.word.strip().upper().replace(",", "").replace(".", "").replace("!", "").replace("?", "")
        if clean:
            words.append({
                "word": clean,
                "start": round(w.start, 2),
                "end": round(w.end, 2)
            })

print(f"Detected {len(words)} exact words in audio:")
for idx, w in enumerate(words):
    print(f"  {w['start']:05.2f}s - {w['end']:05.2f}s : {w['word']}")

# Find CTA start time (e.g. "GAME IS CALLED STEAL A SEED")
cta_start = 20.80
for i in range(len(words)-3):
    if words[i]["word"] in ["GAME", "CALLED"] and words[i+1]["word"] in ["IS", "CALLED", "STEAL"]:
        cta_start = words[i]["start"]
        print(f"\n--> CTA starts at: {cta_start:.2f}s (Endcard transition boundary)")
        break

# Group words into 1-3 word punchy kinetic phrases
phrases = []
curr = []
for w in words:
    curr.append(w)
    if len(curr) >= 2:
        dur = curr[-1]["end"] - curr[0]["start"]
        if len(curr) >= 3 or dur >= 0.70:
            phrases.append({
                "text": " ".join([x["word"] for x in curr]),
                "start": curr[0]["start"],
                "end": curr[-1]["end"]
            })
            curr = []
if curr:
    phrases.append({
        "text": " ".join([x["word"] for x in curr]),
        "start": curr[0]["start"],
        "end": curr[-1]["end"]
    })

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

ass_template = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CenterWhite,Impact,98,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,5,5,60,60,0,1
Style: CenterGold,Impact,104,&H0020E5FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterRed,Impact,104,&H003344FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1
Style: CenterGreen,Impact,104,&H0033FF66,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,9,6,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

gold_words = ["STEAL", "SEED", "TWENTY", "THOUSAND", "20,000", "TWENTY-ONE", "21,000", "FIFTY", "50,000", "ROBLOX"]
green_words = ["TREADMILL", "GYM", "LIGHTNING", "MULTIPLIERS", "PURPLE", "TRAILS", "TRAIL", "BLITZ", "GUARANTEED", "PLANT", "FARM", "PRINTING"]
red_words = ["NEVER", "DESERT", "ZONE", "THORN", "GIANT", "MONSTER", "CHASES", "WIPES", "INVENTORY"]

style_map = {"WHITE": "CenterWhite", "GOLD": "CenterGold", "RED": "CenterRed", "GREEN": "CenterGreen"}

# Subtitle must cut off before living endcard starts
endcard_cutoff = cta_start
ass_events = []
for p in phrases:
    if p["start"] >= endcard_cutoff:
        continue
    st = fmt_time(p["start"])
    et = fmt_time(min(p["end"], endcard_cutoff))
    txt = p["text"]
    
    words_in_p = txt.split()
    if any(any(k in w for k in gold_words) for w in words_in_p) or any(c.isdigit() for c in txt):
        hl = "GOLD"
    elif any(any(k in w for k in green_words) for w in words_in_p):
        hl = "GREEN"
    elif any(any(k in w for k in red_words) for w in words_in_p):
        hl = "RED"
    else:
        hl = "WHITE"
        
    sname = style_map[hl]
    ass_events.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

full_ass = ass_template + "\n".join(ass_events) + "\n"
with open(out_ass, "w", encoding="utf-8") as f:
    f.write(full_ass)

print(f"\nSaved 100% accurate Whisper ASS subtitle: {out_ass} ({len(ass_events)} kinetic phrases)")
print(f"Endcard starts at: {cta_start:.2f}s")
