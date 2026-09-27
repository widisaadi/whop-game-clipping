import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "We started with zero speed in Steal a Seed, "
    "and walking this slow made the giant monster catch us every single time! "
    "So we placed treadmills in our garden, stacked five speed per second, "
    "and upgraded to the green track for twelve speed multipliers! "
    "Our speed exploded over twenty one thousand, "
    "while our legendary Coco Cannons printed fifty thousand cash a second! "
    "Now we literally fly across the map and nothing can touch us! "
    "Play Steal a Seed on Roblox right now!"
)

def generate_voice():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_sas_03_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_sas_03_fast.wav")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    print(f"Generating Puck voiceover for Steal a Seed Video 03 (Speed Multiplier Glitch)...")
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
        
    raw_dur = (len(audio_bytes) / 2) / 24000
    print(f"Saved raw voiceover: {raw_wav} ({raw_dur:.2f}s)")
    
    # Trim dead air >100ms and speed up to breathless cadence 1.28x
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    
    # Probe duration
    pcmd = ["ffprobe", "-i", fast_wav, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
    fast_dur = float(pres.stdout.strip())
    print(f"Generated fast breathless voiceover: {fast_wav} ({fast_dur:.2f}s)")
    return fast_dur

if __name__ == "__main__":
    generate_voice()
