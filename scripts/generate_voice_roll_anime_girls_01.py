import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "In this Roblox game, you roll dice for anime girls and use them to make millions! "
    "You start with zero cash on an empty plot, so you have to roll the dice to unlock your first character! "
    "Place them down and they print passive money every second, even while you are completely offline! "
    "Stack luck potions to pull legendary drops, and hit rebirth to unlock massive permanent cash multipliers! "
    "Can you roll the rarest anime girl? Game is called Roll Anime Girls on Roblox, link in bio!"
)

def generate_voice():
    temp_dir = "temp/roll_anime_girls"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_rag_01_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_rag_01_fast.wav")
    fast_mp3 = os.path.join(temp_dir, "voiceover_rag_01_fast.mp3")
    
    print("Generating energetic Puck voiceover for Roll Anime Girls Video 01...")
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
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
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
    
    # Check volume of raw voiceover
    vres = subprocess.run(["ffmpeg", "-i", raw_wav, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    for line in vres.stderr.split("\n"):
        if "mean_volume" in line or "max_volume" in line:
            print("  [Volume Check]:", line.strip())
            
    # Trim dead air >100ms and speed up to breathless cadence 1.28x
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    
    # Save mp3
    subprocess.run(["ffmpeg", "-y", "-i", fast_wav, "-q:a", "2", fast_mp3], check=True)
    
    fast_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fast_wav], text=True).strip())
    print(f"Generated fast breathless voiceover: {fast_wav} ({fast_dur:.2f}s)")
    return fast_dur

if __name__ == "__main__":
    generate_voice()
