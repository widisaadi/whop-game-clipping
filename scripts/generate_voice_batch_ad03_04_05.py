import urllib.request
import json
import base64
import wave
import os
import subprocess

API_KEY = os.environ.get("GEMINI_API_KEY", "")

SCRIPTS = {
    "03_asmr_dominoes_lava_magma_topple": (
        "Bro, whatever you do, DO NOT topple the level five hundred lava dominoes! "
        "Because the moment they fall, blazing molten magma literally melts the entire floor! "
        "Basic wooden tiles only drop fifty coins. "
        "Until you equip the volcano skin, grab the drag brush, and curve hundreds of fiery magma dominoes across the map! "
        "Hit topple mode, watch the burning chain trigger endless multiplier cheese stars, and unleash a blinding divine light pillar! "
        "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
    ),
    "04_asmr_dominoes_broken_chain_save": (
        "Bro, I almost ruined the biggest domino chain reaction on Roblox! "
        "Look at that massive missing gap, one single millimeter off and the whole run fails! "
        "Normal builders give up and lose all their streak multipliers. "
        "Not us! Grab the drag brush, sprint to the gap, and lay down fresh obsidian tiles before the wave hits! "
        "It connects! The chain sweeps through the giant spiral maze with zero lag, and crushes every multiplier record! "
        "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
    ),
    "05_asmr_dominoes_toilet_vs_singularity": (
        "Bro, who allowed the developers to add a literal TOILET domino to this game?! "
        "At level one, you're placing cute little tiles that float romantic red hearts. "
        "At level fifty, you unlock water ripple dominoes with crisp bamboo clacks. "
        "At level five hundred, it turns into an actual porcelain toilet that flushes the entire track! "
        "And at level nine ninety-nine, a cosmic singularity swallows the leaderboard and rips space-time apart! "
        "Game is called ASMR Dominoes on Roblox, link in pinned comment!"
    )
}

def generate_voice_batch():
    temp_dir = "temp/asmr_dominoes"
    os.makedirs(temp_dir, exist_ok=True)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-tts-preview:generateContent?key={API_KEY}"
    
    results = {}
    for vid_id, text in SCRIPTS.items():
        print(f"\n==========================================")
        print(f"Generating Puck voiceover for {vid_id}...")
        print(f"==========================================")
        
        raw_wav = os.path.join(temp_dir, f"voiceover_{vid_id}_raw.wav")
        fast_wav = os.path.join(temp_dir, f"voiceover_{vid_id}_fast.wav")
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": text}
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
        
        # Trim dead air >100ms and speed up to breathless cadence 1.28x
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_wav,
            "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
            fast_wav
        ]
        subprocess.run(cmd, check=True)
        
        pcmd = ["ffprobe", "-i", fast_wav, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
        pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
        fast_dur = float(pres.stdout.strip())
        print(f"Generated fast breathless voiceover: {fast_wav} ({fast_dur:.2f}s)")
        results[vid_id] = {
            "raw_wav": raw_wav,
            "fast_wav": fast_wav,
            "fast_dur": fast_dur,
            "text": text
        }
        
    print("\nAll voiceovers successfully generated!")
    for vid_id, data in results.items():
        print(f"- {vid_id}: {data['fast_dur']:.2f}s")
    return results

if __name__ == "__main__":
    generate_voice_batch()
