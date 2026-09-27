import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT_TEXT = (
    "This is the fastest way to get millions of cash in +1 Money Roll! "
    "Most players waste hours slowly rolling their starting ball, but here's the secret trick. "
    "First, rush straight to the pet stands and hatch rare eggs for insane cash multipliers! "
    "Next, hit the speed gym treadmills to max out your roll velocity, "
    "then hit the rebirth machine to instantly double your entire income! "
    "Roll that massive money boulder across the finish line and flex on the leaderboards! "
    "Play +1 Money Roll on Fortnite, map code is on screen!"
)

def generate_voice():
    os.makedirs("temp/money_roll", exist_ok=True)
    out_wav = "temp/money_roll/voiceover_v02.wav"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    prompt = (
        "Read the following Fortnite gaming promotional voiceover with an ultra FAST, rapid-fire, breathless, punchy gaming delivery. "
        "Keep intense momentum with virtually no dead pauses between sentences, delivering every word with high enthusiasm. "
        "Pronounce '+1 Money Roll' clearly as 'Plus One Money Roll':\n\n"
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

    print("Requesting rapid-fire breathless voiceover for Money Roll v02 from Gemini Aoede...")
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
