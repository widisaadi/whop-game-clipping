import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

audio_path = "temp/tongue_escape/voiceover_v11.wav"
with open(audio_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is the exact audio transcript:
"Look at what happens in +1 Tongue Escape! This giant lava pit in Stage 8 destroys anyone with a weak tongue! To make it across, you have to hit the gym treadmills to pump your tongue to forty thousand studs! Then you spit out a massive lightning bridge to rocket across the boiling lava, dodge the obstacles, and land safely on the finish platform! If you love crazy Roblox game breakdowns, smash that like button right now! And play +1 Tongue Escape on Roblox, link is in my bio!"

Analyze this fast-paced audio carefully.
Provide TWO parts in your JSON response:

PART 1: "sentences" - The exact start and end timestamps for each of the 6 narrative sections:
1. "avatar_intro": "Look at what happens in +1 Tongue Escape!"
2. "stage8_lava": "This giant lava pit in Stage 8 destroys anyone with a weak tongue!"
3. "gym_pump": "To make it across, you have to hit the gym treadmills to pump your tongue to forty thousand studs!"
4. "bridge_rocket": "Then you spit out a massive lightning bridge to rocket across the boiling lava, dodge the obstacles, and land safely on the finish platform!"
5. "like_breakdowns": "If you love crazy Roblox game breakdowns, smash that like button right now!"
6. "cta_endcard": "And play +1 Tongue Escape on Roblox, link is in my bio!"

PART 2: "cues" - Rapid 1-3 word kinetic pop subtitle cues up to the start of the endcard (cutoff before cta_endcard):
For each cue:
- "text": uppercase subtitle text (e.g. "LOOK AT WHAT", "HAPPENS IN", "+1 TONGUE ESCAPE!", "GIANT LAVA PIT", "STAGE 8", "DESTROYS", "WEAK TONGUE!", "HIT THE GYM", "TREADMILLS", "40,000 STUDS!", "LIGHTNING BRIDGE", "BOILING LAVA!", "FINISH PLATFORM!", "ROBLOX BREAKDOWNS", "SMASH THAT LIKE!")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules for highlights:
- GOLD: "+1 TONGUE ESCAPE!", "STAGE 8", "40,000 STUDS!", "ROBLOX BREAKDOWNS", "SMASH THAT LIKE!"
- GREEN: "HIT THE GYM", "TREADMILLS", "LIGHTNING BRIDGE", "FINISH PLATFORM!"
- RED: "GIANT LAVA PIT", "DESTROYS", "WEAK TONGUE!", "BOILING LAVA!"

Return ONLY a valid JSON object matching schema:
{
  "sentences": {
    "avatar_intro": {"start": 0.0, "end": 1.4},
    "stage8_lava": {"start": 1.4, "end": 5.2},
    "gym_pump": {"start": 5.2, "end": 9.8},
    "bridge_rocket": {"start": 9.8, "end": 15.3},
    "like_breakdowns": {"start": 15.3, "end": 19.0},
    "cta_endcard": {"start": 19.0, "end": 23.12}
  },
  "cues": [
    {"text": "+1 TONGUE ESCAPE!", "start": 0.5, "end": 1.4, "highlight": "GOLD"}
  ]
}
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

models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
out_text = None

for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    for attempt in range(3):
        print(f"Aligning Video 11 audio timestamps with {model} (attempt {attempt+1})...")
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                out_text = data["candidates"][0]["content"]["parts"][0]["text"]
                break
        except Exception as e:
            print(f"Error with {model}: {e}")
            time.sleep(2)
    if out_text:
        break

data = json.loads(out_text)
print("=== SENTENCE BOUNDARIES FOR VIDEO CUTS ===")
print(json.dumps(data["sentences"], indent=2))

cues = data["cues"]
print(f"Parsed {len(cues)} subtitle cues successfully.")

# Save alignment json
with open("temp/tongue_escape/alignment_v11.json", "w") as f:
    json.dump(data, f, indent=2)

# ASS Subtitle Generator adhering to BloxClips Patent
def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:01d}:{m:02d}:{s:05.2f}"

ass_content = """[Script Info]
Title: BloxClips Subtitles - Video 11
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CenterWhite,Impact,98,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,8,5,2,40,40,740,1
Style: CenterGold,Impact,102,&H0000D7FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1
Style: CenterRed,Impact,102,&H002020FF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1
Style: CenterGreen,Impact,102,&H0030E020,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,9,6,2,40,40,740,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

endcard_start = data["sentences"]["cta_endcard"]["start"]
print(f"Endcard start timestamp: {endcard_start:.2f}s")

for c in cues:
    # Subtitles MUST stop before endcard
    if c["start"] >= endcard_start:
        continue
    end_time = min(c["end"], endcard_start)
    hl = c.get("highlight", "WHITE")
    if hl == "GOLD":
        style = "CenterGold"
    elif hl == "RED":
        style = "CenterRed"
    elif hl == "GREEN":
        style = "CenterGreen"
    else:
        style = "CenterWhite"
        
    start_fmt = fmt_time(c["start"])
    end_fmt = fmt_time(end_time)
    text = c["text"]
    ass_content += f"Dialogue: 0,{start_fmt},{end_fmt},{style},,0,0,0,,{text}\n"

out_ass = "campaigns/tongue_escape/subtitles/captions_tongue_escape_v11.ass"
os.makedirs("campaigns/tongue_escape/subtitles", exist_ok=True)
with open(out_ass, "w", encoding="utf-8") as f:
    f.write(ass_content)

print(f"Wrote ASS subtitle file: {out_ass}")
