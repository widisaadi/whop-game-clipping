import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Exactly matching the subtitle with zero filler words ("tanpa kata imbuhan, sesuai subtitle")
SCRIPT_TEXT = (
    "This is the most unhinged fishing game in Roblox! "
    "In How to Fisch, you cast your rod, "
    "until a giant Sun Fish boss charges at you! "
    "The only way to survive: roll high-tier guns at the armory! "
    "Blast its health bar with your pistol, "
    "then steer your motorboat into open waters "
    "to hunt down colossal ocean titans! "
    "Search How to Fisch on Roblox!"
)

def generate_voice():
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    raw_wav = "temp/how_to_fisch/voiceover_htf_v12_clean_raw.wav"
    fast_wav = "temp/how_to_fisch/voiceover_htf_v12_clean_fast.wav"

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

    print("Generating clean Puck voiceover matching exact subtitle text...")
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

    with wave.open(raw_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(audio_bytes)

    print(f"Saved raw voiceover to {raw_wav}")

    # Remove silence pauses >100ms and speed up slightly to ~1.25x for breathless delivery
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.25",
        fast_wav
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated breathless clean voiceover: {fast_wav}")

if __name__ == "__main__":
    generate_voice()
