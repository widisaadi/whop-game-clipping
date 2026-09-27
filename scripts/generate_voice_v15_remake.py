import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT_TEXT = (
    "I found the only Roblox obby where normal jumping is completely banned! "
    "If you try to jump like a normal obby, you instantly fall into the void. "
    "Instead, you have to spit out your tongue and turn it into a massive bridge! "
    "Train in the speed gym to unlock crazy multipliers, dodge brutal moving crushers, "
    "and see if you can actually survive the impossible Stage 8! "
    "The game is called +1 Tongue Escape on Roblox, link is in my bio!"
)

def generate_voice():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_wav = "temp/tongue_escape/voiceover_v15_remake.wav"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    prompt = (
        "Read the following Roblox gaming promotional voiceover with high energy, enthusiastic personality, and great comedic timing. "
        "Speak naturally with good cadence and clear breathing room so it sounds exciting but never overly rushed or forced. "
        "Pronounce '+1 Tongue Escape' clearly as 'Plus One Tongue Escape':\n\n"
        f"{SCRIPT_TEXT}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": "Aoede"
                    }
                }
            }
        }
    }

    print("Requesting natural, high-energy voiceover for v15 remake from Gemini Aoede...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        res_data = json.loads(response.read().decode("utf-8"))

    audio_bytes = None
    for candidate in res_data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline_data = part.get("inlineData") or part.get("inline_data")
            if inline_data and "data" in inline_data:
                audio_bytes = base64.b64decode(inline_data["data"])
                break

    if not audio_bytes:
        raise RuntimeError(f"No audio data found in response: {res_data}")

    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"--> Saved {out_wav} (Duration: {duration:.2f}s)")
    return out_wav, duration

if __name__ == "__main__":
    generate_voice()
