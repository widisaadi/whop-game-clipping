import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPTS = {
    "v19": {
        "id": "19_tongue_escape_impossible_highway",
        "text": (
            "Bro, this might be the most illegal Roblox obby ever! "
            "You are trapped on a floating island, and jumping is completely banned! "
            "The only way across... is spitting out your own giant tongue as a solid bridge! "
            "Grind the speed gym, stack massive multipliers, and slide across raging lava to escape! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v20": {
        "id": "20_tongue_escape_multiplier_glitch",
        "text": (
            "Nobody told me this Roblox obby gets this completely insane! "
            "You start with zero reach and can't even clear the first jump! "
            "But once you hit the x99 Hacker gym, your tongue gains thousands of studs in seconds! "
            "Dodge moving obstacles, soar over deadly lava, and conquer Stage 8 for 100 wins! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    },
    "v21": {
        "id": "21_tongue_escape_secret_codes",
        "text": (
            "Stop grinding with a tiny tongue in Roblox right now! "
            "Here are three secret working codes to instantly get 15,000 free tongue and a 2x boost! "
            "Type WELCOME1 for 5k, BONUS500 for another 10k, and FREEBOOST to double your growth speed! "
            "Now you can bridge entire maps with zero effort! "
            "Play +1 Tongue Escape on Roblox, link is in my bio!"
        )
    }
}

def generate_voice_batch():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    for key, item in SCRIPTS.items():
        vid_id = item["id"]
        raw_text = item["text"]
        print(f"\n=======================================================")
        print(f"Generating Puck Natural Voice for {key} ({vid_id})...")
        print(f"Text: {raw_text}")
        print(f"=======================================================")
        
        raw_wav = f"temp/tongue_escape/voiceover_{key}_raw.wav"
        fast_wav = f"temp/tongue_escape/voiceover_{key}_fast.wav"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": raw_text}
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
            
        raw_dur = (len(audio_bytes) / 2) / 24000
        print(f"Saved raw voiceover: {raw_wav} ({raw_dur:.2f}s)")
        
        # Pangkas dead air >100ms dan pacing cadence rapat ~1.28x
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_wav,
            "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
            fast_wav
        ]
        subprocess.run(cmd, check=True)
        print(f"Generated fast breathless voiceover: {fast_wav}")

if __name__ == "__main__":
    generate_voice_batch()
