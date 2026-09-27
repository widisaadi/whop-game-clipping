import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "This is the hardest stage in +1 Tongue Escape, and one slip means falling straight into the lava! "
    "Instead of jumping, you spit out a giant tongue bridge to slide across cracked cliffs and dodge deadly honeycomb walls! "
    "Train your tongue on gym treadmills to add thousands of studs, because only max-level tongues can conquer Stage 7! "
    "Can you beat it? "
    "Play +1 Tongue Escape on Roblox, link is in my bio, especially if you want to know why..."
)

def generate_voice():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Read the following Roblox gaming promotional voiceover with an ultra FAST-PACED, high-energy, rapid-fire, punchy, dramatic, and highly enthusiastic gaming delivery. "
                            "Pronounce '+1 Tongue Escape' clearly as 'Plus One Tongue Escape'. "
                            "No dead pauses, high momentum from the first word to the very last word:\n\n"
                            f"{SCRIPT}"
                        )
                    }
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

    print("Requesting fast-paced voiceover for Video 09 from gemini-3.1-flash-tts-preview (Aoede)...")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
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

    out_wav = "temp/tongue_escape/voiceover_v09.wav"
    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"Saved Gemini Aoede WAV voiceover to: {out_wav} (Duration: {duration:.2f}s)")
    return out_wav, duration

if __name__ == "__main__":
    generate_voice()
