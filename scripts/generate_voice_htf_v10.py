import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPT = (
    "Whatever you do, do NOT hook this fish in Roblox! "
    "In How to Fisch, you start off like a normal fishing simulator, casting your rod into peaceful waters... "
    "until an enraged giant Sun Fish boss literally leaps out of the ocean and charges straight at you! "
    "You have to roll high-tier guns at the fish armory, blast through its health bar with your pistol, and harvest rare loot! "
    "Then hop in your motorboat to hunt down legendary sea titans across the open ocean! "
    "Search How to Fisch on Roblox and play right now!"
)

def generate_voice():
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    # Try Callirrhoe first, fallback to Aoede
    voices = ["Callirrhoe", "Aoede"]
    audio_bytes = None
    
    for voice in voices:
        print(f"Requesting voiceover from gemini-3.1-flash-tts-preview (Voice: {voice})...")
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Read the following gaming voiceover with an energetic, punchy, high-momentum, and exciting fast-paced creator delivery. "
                                "Pronounce 'How to Fisch' clearly. No awkward long pauses:\n\n"
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
                            "voiceName": voice
                        }
                    }
                }
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode("utf-8"))
            for candidate in res_data.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    inline_data = part.get("inlineData") or part.get("inline_data")
                    if inline_data and "data" in inline_data:
                        audio_bytes = base64.b64decode(inline_data["data"])
                        break
            if audio_bytes:
                print(f"Successfully generated voiceover using voice: {voice}")
                break
        except Exception as e:
            print(f"Error requesting voice {voice}: {e}")
            
    if not audio_bytes:
        raise RuntimeError("Failed to generate voiceover with all voice candidates.")

    raw_wav = "temp/how_to_fisch/voiceover_htf_v10_raw.wav"
    with wave.open(raw_wav, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    # Re-speed to 1.15x for punchy, fast pacing like Video 08
    fast_wav = "temp/how_to_fisch/voiceover_htf_v10.wav"
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-filter:a", "atempo=1.15,aresample=48000",
        fast_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Get duration
    cmd_dur = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", fast_wav]
    dur_str = subprocess.check_output(cmd_dur, text=True).strip()
    duration = float(dur_str)
    print(f"Final voiceover generated: {fast_wav} (Duration: {duration:.2f}s)")
    return fast_wav, duration

if __name__ == "__main__":
    generate_voice()
