import urllib.request
import json
import base64
import os
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

CONFIGS = {
    "v12": {
        "audio": "temp/tongue_escape/voiceover_v12.wav",
        "endcard_start": 15.60,
        "out_ass": "campaigns/tongue_escape/subtitles/captions_tongue_escape_v12.ass",
        "out_json": "temp/tongue_escape/subtitle_phrases_v12.json",
        "transcript": (
            "I think I just found the most illegal obby on Roblox, and how is this even allowed?! "
            "In +1 Tongue Escape, you literally grow your tongue into a massive highway to bypass impossible death traps! "
            "Hop on the x99 treadmill to grind out crazy studs, jump across raging lava chasms, and conquer Stage 8 to flex on the leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v13": {
        "audio": "temp/tongue_escape/voiceover_v13.wav",
        "endcard_start": 15.80,
        "out_ass": "campaigns/tongue_escape/subtitles/captions_tongue_escape_v13.ass",
        "out_json": "temp/tongue_escape/subtitle_phrases_v13.json",
        "transcript": (
            "Nobody told me this Roblox obby gets this completely insane! "
            "In +1 Tongue Escape, normal jumping is impossible—you have to spit out a giant tongue to bridge crazy gaps! "
            "Train on high-speed treadmills to level up your reach, survive brutal moving lava obstacles, and flex Stage 8 on the global leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v14": {
        "audio": "temp/tongue_escape/voiceover_v14.wav",
        "endcard_start": 15.60,
        "out_ass": "campaigns/tongue_escape/subtitles/captions_tongue_escape_v14.ass",
        "out_json": "temp/tongue_escape/subtitle_phrases_v14.json",
        "transcript": (
            "This new Roblox game completely broke obby physics! "
            "Instead of regular parkour, +1 Tongue Escape lets you stretch your tongue thousands of studs across the map! "
            "Speed train in the gym for insane multipliers, cross deadly lava chasms without touching the floor, and race your friends to the top of the leaderboards! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    }
}

def fmt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def align_audio(vid_key, cfg):
    audio_path = cfg["audio"]
    if not os.path.exists(audio_path):
        print(f"Audio file {audio_path} not found for {vid_key}!")
        return False

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = f"""
Here is the exact audio transcript:
"{cfg['transcript']}"

Analyze this fast-paced audio carefully. Break down the entire speech into short 1-3 word punchy subtitle phrases for fast-paced TikTok/Reels captions.
For each phrase, output:
- "text": uppercase subtitle text (e.g. "MOST ILLEGAL", "+1 TONGUE ESCAPE", "MASSIVE HIGHWAY", "STAGE 8")
- "start": start time in seconds (float, 2 decimals)
- "end": end time in seconds (float, 2 decimals)
- "highlight": one of ["WHITE", "GOLD", "RED", "GREEN"]

Rules:
- Highlight game title, big numbers, stages, and leaderboards in GOLD (e.g. "+1 TONGUE ESCAPE", "x99 TREADMILL", "STAGE 8", "LEADERBOARDS")
- Highlight mechanics/features/actions in GREEN (e.g. "MASSIVE HIGHWAY", "SPIT OUT", "GIANT TONGUE", "SPEED TRAIN")
- Highlight challenges/warnings/shocks in RED (e.g. "MOST ILLEGAL", "EVEN ALLOWED?!", "DEATH TRAPS", "INSANE", "BROKE PHYSICS", "DEADLY LAVA")
- Keep phrases short (1-3 words) for rapid kinetic popping.

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
            print(f"Aligning {vid_key} audio timestamps with {model} (attempt {attempt+1})...")
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    out_text = res["candidates"][0]["content"]["parts"][0]["text"]
                    break
            except Exception as e:
                print(f"Error with {model} on {vid_key}: {e}")
                time.sleep(2)
        if out_text:
            break

    if not out_text:
        raise RuntimeError(f"Failed to get response for {vid_key} from all models")

    phrases = json.loads(out_text)
    print(f"Received {len(phrases)} timestamped phrases for {vid_key}!")
    
    os.makedirs(os.path.dirname(cfg["out_json"]), exist_ok=True)
    with open(cfg["out_json"], "w", encoding="utf-8") as f:
        json.dump(phrases, f, indent=2)

    style_map = {
        "WHITE": "CenterWhite",
        "GOLD": "CenterGold",
        "RED": "CenterRed",
        "GREEN": "CenterGreen"
    }

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

    endcard_cutoff = cfg["endcard_start"]
    for p in phrases:
        if p["start"] >= endcard_cutoff:
            continue
        st = fmt_time(p["start"])
        et = fmt_time(min(p["end"], endcard_cutoff))
        sname = style_map.get(p.get("highlight", "WHITE"), "CenterWhite")
        txt = p["text"].strip().upper()
        ass_lines.append(f"Dialogue: 2,{st},{et},{sname},,0,0,0,,{{\\pos(540,1180)\\t(0,60,\\fscx115\\fscy115)\\t(60,120,\\fscx100\\fscy100)}}{txt}")

    os.makedirs(os.path.dirname(cfg["out_ass"]), exist_ok=True)
    with open(cfg["out_ass"], "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")

    print(f"Generated clean ASS subtitle at {cfg['out_ass']} at Y=1180.")
    return True

def main():
    for k, cfg in CONFIGS.items():
        align_audio(k, cfg)

if __name__ == "__main__":
    main()
