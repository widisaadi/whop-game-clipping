import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

SCRIPTS = {
    "07_asmr_dominoes_lvl1_vs_lvl999": (
        "Bro, this is what a level one domino looks like versus a level nine ninety-nine domino in Roblox! "
        "At level one, you can only drop five wooden tiles in a straight line that give you a pathetic fifty coins. "
        "Until you unlock the level nine ninety-nine drag brush, sprinting across the map and placing thousands of obsidian tiles in three seconds! "
        "Hit topple mode, watch the hypersonic chain topple with insane physics, and swallow the entire leaderboard into a dark matter singularity! "
        "Play ASMR Dominoes on Roblox, link in bio!"
    ),
    "08_asmr_dominoes_satisfying_bubble_pop": (
        "Whatever you do, DO NOT equip the bubble domino in Roblox! "
        "Because the moment they topple, they pop like real bubble wrap and you literally cannot look away! "
        "Normal blocks are boring, but dragging the slow-mo speed slider lets you hear every single micro crunch in crisp stereo! "
        "Curve a massive hundred-foot tidal wave across the grid, trigger the cinematic cam, and let the soothing popping wave crush every multiplier milestone and trigger a golden star jackpot! "
        "Play ASMR Dominoes on Roblox, link in bio!"
    ),
    "09_asmr_dominoes_shop_secret_skins": (
        "I spent a million coins to unlock the most illegal domino skins in Roblox! "
        "Most players are stuck with plain wooden blocks that sound like falling cardboard. "
        "Until you open the sound vault and equip crunchy celery cracks, bamboo clacks, and crystal dings! "
        "Pair it with the galaxy skin, build a hypnotic spiral maze across the entire arena, and watch thousands of tiles topple with zero lag before collapsing into an infinite cosmic black hole! "
        "Play ASMR Dominoes on Roblox, link in bio!"
    )
}

API_KEYS = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", "")).split(",") if k.strip()]

def request_tts_single(text, raw_wav, voice_name="Puck"):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": text}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name
                    }
                }
            }
        }
    }
    
    models = [
        "gemini-2.5-flash-preview-tts",
        "gemini-3.1-flash-tts-preview"
    ]
    
    for key_idx, key in enumerate(API_KEYS):
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            try:
                print(f"  Attempting model {model} with Key {key_idx + 1}...")
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    
                part = res_data["candidates"][0]["content"]["parts"][0]
                audio_b64 = part["inlineData"]["data"]
                audio_bytes = base64.b64decode(audio_b64)
                
                with wave.open(raw_wav, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(audio_bytes)
                    
                dur = (len(audio_bytes) / 2) / 24000
                print(f"  [SUCCESS] {model} -> {raw_wav} ({dur:.2f}s)")
                return raw_wav
            except Exception as e:
                print(f"  Failed: {e}")
                time.sleep(1)
                
    raise RuntimeError("All Gemini TTS models/keys failed!")

def main():
    temp_dir = "temp/asmr_dominoes/batch_07_08_09"
    os.makedirs(temp_dir, exist_ok=True)
    
    for vid_id, text in SCRIPTS.items():
        print(f"\n==========================================")
        print(f"Generating Puck VO for {vid_id}...")
        print(f"==========================================")
        raw_wav = os.path.join(temp_dir, f"{vid_id}_raw.wav")
        fast_wav = os.path.join(temp_dir, f"{vid_id}_fast.wav")
        
        request_tts_single(text, raw_wav, voice_name="Puck")
        
        # Trim dead air >100ms and speed up to breathless cadence 1.28x
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_wav,
            "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
            fast_wav
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr)
            raise RuntimeError("FFmpeg silenceremove/atempo failed")
            
        # Check duration
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", fast_wav],
            capture_output=True, text=True
        )
        fast_dur = float(json.loads(probe.stdout)["format"]["duration"])
        print(f"Fast VO duration: {fast_dur:.2f}s -> {fast_wav}")

if __name__ == "__main__":
    main()
