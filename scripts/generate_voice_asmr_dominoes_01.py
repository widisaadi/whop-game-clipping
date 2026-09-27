import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "This is what happens when you upgrade a basic domino into a literal black hole! "
    "At level one, you're placing five boring tiles for pocket change. "
    "Until you grab the drag brush, stretch out five hundred dominoes in three seconds, and crank the scale slider! "
    "Once we hit topple mode, the whole chain triggers cosmic multipliers. "
    "And at level nine ninety-nine, a massive singularity opens and swallows the entire map! "
    "Game is called ASMR Dominoes on Roblox, link in bio!"
)

def generate_voice():
    temp_dir = "temp/asmr_dominoes"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_ad_01_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_ad_01_fast.wav")
    fast_mp3 = os.path.join(temp_dir, "voiceover_ad_01_fast.mp3")
    
    models = ["gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
    
    print("Generating Puck voiceover for ASMR Dominoes Video 01 (Black Hole Singularity)...")
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
    
    success = False
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        print(f"Trying model {model_name} with Puck...")
        try:
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
            success = True
            break
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            time.sleep(2)
            
    if not success:
        print("Falling back to edge-tts with en-US-ChristopherNeural...")
        subprocess.run(["edge-tts", "--voice", "en-US-ChristopherNeural", "--text", VOICE_SCRIPT, "--write-media", raw_wav], check=True)
        raw_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_wav], text=True).strip())
        print(f"Saved fallback edge-tts voiceover: {raw_wav} ({raw_dur:.2f}s)")
    
    # Trim dead air >100ms and speed up to breathless cadence 1.28x
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    
    # Create mp3 version
    subprocess.run(["ffmpeg", "-y", "-i", fast_wav, "-q:a", "2", fast_mp3], check=True)
    
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
