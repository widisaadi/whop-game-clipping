import urllib.request
import json
import base64
import wave
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "Look at what happens in +1 Tongue Escape! "
    "This giant lava pit in Stage 8 destroys anyone with a weak tongue! "
    "To make it across, you have to hit the gym treadmills to pump your tongue to forty thousand studs! "
    "Then you spit out a massive lightning bridge to rocket across the boiling lava, dodge the obstacles, and land safely on the finish platform! "
    "If you love crazy Roblox game breakdowns, smash that like button right now! "
    "And play +1 Tongue Escape on Roblox, link is in my bio!"
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
                            "Read the following Roblox gaming promotional voiceover with an ultra FAST-PACED, dramatic, punchy, high-energy, and exciting gaming delivery. "
                            "Pronounce '+1 Tongue Escape' clearly as 'Plus One Tongue Escape'. "
                            "No dead pauses, maximum energy and momentum from the first word to the very last word:\n\n"
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
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    print("Calling Gemini 3.1 Flash TTS Preview API (Aoede) for Video 11 (with Intro Hook)...")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        
    audio_data = res["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    raw_pcm = base64.b64decode(audio_data)
    
    out_wav = "temp/tongue_escape/voiceover_v11.wav"
    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(raw_pcm)
        
    print(f"Generated raw TTS audio: {out_wav}")
    
    import subprocess
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{out_wav}"'
    dur = float(subprocess.check_output(cmd, shell=True).decode().strip())
    print(f"Voiceover duration: {dur:.2f} seconds")
    return dur

if __name__ == "__main__":
    generate_voice()
