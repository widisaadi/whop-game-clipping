import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "You're playing Steal a Seed all wrong if you're not using the Secret Item Shop! "
    "When the giant prickly Cactus Monster ambushed us in the Desert Zone, we used the shop to buy Frozen Grenades, Bear Traps, and Mythic Buckets that cut growth time by 80%! "
    "Then we unlocked the neon Cyan Laser Trail and hit thirteen thousand speed! "
    "We claimed the legendary Pumpkin Baron, and our garden prints over 1.1 MILLION cash per second! "
    "Search Steal a Seed on Roblox and dominate the game right now!"
)

def generate_voice():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_sas_07_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_sas_07_fast.wav")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    print(f"Generating Puck voiceover for Steal a Seed Video 07 (Desert Cactus & Secret Item Shop)...")
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": VOICE_SCRIPT}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": "Puck"
                    }
                }
            }
        }
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}...")
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                
            part = res_data["candidates"][0]["content"]["parts"][0]
            audio_b64 = part["inlineData"]["data"]
            audio_bytes = base64.b64decode(audio_b64)
            
            with wave.open(raw_wav, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_bytes)
                
            raw_dur = (len(audio_bytes) / 2) / 24000
            print(f"Saved raw voiceover: {raw_wav} ({raw_dur:.2f}s)")
            break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise
            time.sleep(3)
    
    # Trim dead air >100ms and speed up to breathless cadence 1.28x
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    
    # Get fast duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", fast_wav
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    fast_dur = float(res.stdout.strip())
    print(f"Processed fast voiceover: {fast_wav} ({fast_dur:.2f}s)")
    return fast_dur

if __name__ == "__main__":
    generate_voice()
