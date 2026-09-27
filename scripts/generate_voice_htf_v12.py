import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT_TEXT = (
    "Bro, this is literally the most unhinged fishing game in Roblox! "
    "In How to Fisch, you cast your rod expecting a peaceful simulator, "
    "until an enraged giant Sun Fish boss charges straight out of the water! "
    "The only way to survive is rolling high-tier guns at the fish armory! "
    "Blast through its massive health bar with your pistol, "
    "then steer your motorboat into deep open waters to hunt down colossal mythical ocean titans! "
    "The game is called How to Fisch on Roblox. Search How to Fisch and play right now!"
)

def generate_voice():
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    raw_wav = "temp/how_to_fisch/voiceover_htf_v12_raw.wav"
    fast_wav = "temp/how_to_fisch/voiceover_htf_v12_fast.wav"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SCRIPT_TEXT}
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

    print("Requesting clean natural Puck voiceover from Gemini TTS for How to Fisch Video 12...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        res_data = json.loads(response.read().decode("utf-8"))

    part = res_data["candidates"][0]["content"]["parts"][0]
    audio_b64 = part["inlineData"]["data"]
    audio_bytes = base64.b64decode(audio_b64)

    # Gemini returns 24kHz mono PCM
    with wave.open(raw_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(audio_bytes)

    print(f"Saved raw voiceover to {raw_wav}")

    # Remove pauses >100ms and speed up slightly to reach ~4.0 wps breathless golden standard
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated breathless fast voiceover: {fast_wav}")

if __name__ == "__main__":
    generate_voice()
