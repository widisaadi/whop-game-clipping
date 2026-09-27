import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "How fast can you become the richest player in this new Fortnite map?! "
    "In +1 Money Roll, you roll a giant money ball to generate infinite cash! "
    "Hatch pets for crazy multipliers, speed train in the gym, and roll across deadly lava to conquer secret stages! "
    "Play +1 Money Roll on Fortnite, map code is on screen!"
)

def generate_voice():
    os.makedirs("temp/money_roll", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Read the following Fortnite gaming promotional voiceover with an ultra FAST-PACED, high-energy, rapid-fire, punchy, and highly enthusiastic gaming delivery. "
                            "Pronounce '+1 Money Roll' clearly as 'Plus One Money Roll'. "
                            "No dead pauses, high momentum from the first word to the last:\n\n"
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

    print("Requesting tailored Fortnite voiceover for Money Roll from Gemini Aoede...")
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

    out_wav = "temp/money_roll/voiceover_v01_tailored.wav"
    with wave.open(out_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    duration = (len(audio_bytes) / 2) / 24000
    print(f"Saved tailored Aoede WAV voiceover to: {out_wav} (Duration: {duration:.2f}s)")
    return out_wav, duration

if __name__ == "__main__":
    generate_voice()
