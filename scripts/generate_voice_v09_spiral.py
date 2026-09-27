import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

SCRIPT_TEXT = (
    "Bro, whatever you do, NEVER build a giant domino spiral in Roblox! "
    "Because the moment you hit topple mode, it triggers an endless hypnotic collapse winding straight toward the core! "
    "Open the sound vault, equip the deep sea thud and glass chime sound packs to hear every single click in crisp stereo! "
    "Grab the drag brush to place a thousand tiles, watch the inner rings accelerate with endless golden multiplier stars, "
    "and trigger a massive cosmic black hole that swallows the entire arena! "
    "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
)

API_KEYS = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", "")).split(",") if k.strip()]

def request_tts_single(text, raw_wav, voice_name="Puck"):
    payload = {
        "contents": [
            {"parts": [{"text": text}]}
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
                print(f"  Attempting model {model} with Key {key_idx + 1}...", flush=True)
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
                print(f"  [SUCCESS] {model} -> {raw_wav} ({dur:.2f}s)", flush=True)
                return raw_wav
            except Exception as e:
                print(f"  Failed: {e}", flush=True)
                time.sleep(1)
                
    raise RuntimeError("All Gemini TTS models/keys failed!")

def main():
    temp_dir = "temp/asmr_dominoes/v09_spiral"
    os.makedirs(temp_dir, exist_ok=True)
    raw_wav = os.path.join(temp_dir, "vo_raw.wav")
    fast_wav = os.path.join(temp_dir, "vo_fast.wav")
    
    print("\n==========================================")
    print("Generating Puck VO for Hypnotic Spiral Therapy...")
    print("==========================================", flush=True)
    
    request_tts_single(SCRIPT_TEXT, raw_wav, voice_name="Puck")
    
    # Trim dead air >100ms and speed up to breathless cadence 1.28x
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error speeding up VO:", res.stderr)
        return
        
    with wave.open(fast_wav, "r") as wf:
        fast_dur = wf.getnframes() / float(wf.getframerate())
    print(f"Fast VO duration: {fast_dur:.2f}s -> {fast_wav}", flush=True)

if __name__ == "__main__":
    main()
