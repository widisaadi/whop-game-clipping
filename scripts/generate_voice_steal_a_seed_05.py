import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "NEVER steal seeds in Steal a Seed's Snowlands with base speed! "
    "We grabbed the mythic gift seed with only one hundred speed, and the giant Snowman literally wiped us out! "
    "So we upgraded our gym treadmills, stacked over ten thousand speed, and invaded Snowlands for round two! "
    "We grabbed the frozen pillar, bought water buckets to boost growth, and our garden exploded to over 1.2 MILLION cash every single second! "
    "Now we're running around with the giant Wall Nut! "
    "Search Steal a Seed on Roblox and build your dream garden right now!"
)

def generate_voice():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_sas_05_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_sas_05_fast.wav")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    print(f"Generating Puck voiceover for Steal a Seed Video 05 (Snowlands Heist & $1.2M Garden)...")
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

if __name__ == "__main__":
    generate_voice()
