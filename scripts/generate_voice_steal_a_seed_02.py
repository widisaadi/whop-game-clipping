import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "Stop playing Steal a Seed broke with zero cash! "
    "Everyone starts with zero dollars and locked garden plots, but the developers dropped an insane secret code! "
    "Open your menu and type in thirty five K likes right now to instantly claim two hundred and fifty thousand cash! "
    "You can immediately buy rare water buckets, unlock massive plots, and max out your garden treadmill speed! "
    "Redeem it before it expires! "
    "Play Steal a Seed on Roblox right now!"
)

# Note: We spell out "thirty five K likes" and "two hundred and fifty thousand cash" in the TTS prompt so Gemini pronounces "35K Likes" and "$250,000" naturally, while captions will display "35KLIKES" and "$250,000 CASH!"

def generate_voice():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_sas_02_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_sas_02_fast.wav")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    print(f"Generating Puck voiceover for Steal a Seed Video 02 (Secret Code)...")
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
