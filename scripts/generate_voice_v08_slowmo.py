import urllib.request
import json
import base64
import wave
import os
import subprocess
import time

SCRIPT_TEXT = (
    "Bro, whatever you do, NEVER topple dominoes at normal speed in Roblox! "
    "Because the moment you drag the speed slider down to point thirty x, "
    "it slows down time so you can hear every single micro crunch in crisp stereo! "
    "Open the sound vault, equip the snow crunch and crystal ding sound packs, "
    "and grab the drag brush to place a thousand tiles in three seconds flat! "
    "Hit topple mode, watch the chain trigger endless golden star multipliers, "
    "and unleash a blinding celestial light pillar! "
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
    temp_dir = "temp/asmr_dominoes/v08_slowmo"
    os.makedirs(temp_dir, exist_ok=True)
    raw_wav = os.path.join(temp_dir, "vo_raw.wav")
    fast_wav = os.path.join(temp_dir, "vo_fast.wav")
    
    print("\n==========================================")
    print("Generating Puck VO for Slow-Mo Crunch Therapy...")
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
        print("FFmpeg error:", res.stderr)
        raise RuntimeError("FFmpeg silenceremove/atempo failed")
        
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", fast_wav],
        capture_output=True, text=True
    )
    fast_dur = float(json.loads(probe.stdout)["format"]["duration"])
    print(f"Fast VO duration: {fast_dur:.2f}s -> {fast_wav}", flush=True)

if __name__ == "__main__":
    main()
