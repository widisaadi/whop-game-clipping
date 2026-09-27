import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

API_KEY = os.environ.get("GEMINI_API_KEY", "")

VOICE_SCRIPT = (
    "This legendary Coco Cannon plant prints fifty thousand dollars every single second in Steal a Seed, but to steal it, you need over twenty thousand speed! "
    "If you try sneaking into the deep desert zone with starter speed, you will get caught and lose everything! "
    "So you have to hit the garden treadmill gym, stacking plus twelve lightning multipliers until your speed breaks twenty-one thousand! "
    "Now you can blitz past every monster, cross the border for a guaranteed steal, and plant the Coco Cannon to print millions! "
    "Can you unlock the legendary plant? Search Steal a Seed on Roblox and play right now!"
)

def generate_voice():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, "voiceover_sas_13_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_sas_13_fast.wav")
    fast_mp3 = os.path.join(temp_dir, "voiceover_sas_13_fast.mp3")
    
    models = ["gemini-2.5-flash-preview-tts", "gemini-3.8-flash-tts"]
    
    print("Generating Puck voiceover for Steal a Seed Video 13 (Mythic Coco Cannon & 20K Speed)...")
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
        print(f"Trying model {model_name}...")
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
        # Fallback to edge-tts if API quota is reached
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
    
    # Also create mp3 version for alignment
    subprocess.run(["ffmpeg", "-y", "-i", fast_wav, "-q:a", "2", fast_mp3], check=True)
    
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
