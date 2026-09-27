import os
import json
import base64
import wave
import subprocess
import time
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY", "")

def generate_one_voice(v_conf):
    camp = v_conf["campaign"]
    vid_id = v_conf["vid_id"]
    script_text = v_conf["script"]
    
    temp_dir = os.path.join("temp", camp)
    os.makedirs(temp_dir, exist_ok=True)
    
    raw_wav = os.path.join(temp_dir, f"voiceover_{vid_id}_raw.wav")
    fast_wav = os.path.join(temp_dir, f"voiceover_{vid_id}_fast.wav")
    
    if os.path.exists(fast_wav):
        probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fast_wav]
        dur = float(subprocess.check_output(probe_cmd, text=True).strip())
        print(f"[{vid_id}] Voiceover already exists ({dur:.2f}s). Skipping.")
        return dur
        
    print(f"\n[{vid_id}] Generating Puck Voiceover...")
    models = ["gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
    payload = {
        "contents": [{"parts": [{"text": script_text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": "Puck"}
                }
            }
        }
    }
    
    success = False
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
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
            print(f"[{vid_id}] Gemini {model_name} generated ({raw_dur:.2f}s)")
            success = True
            break
        except Exception as e:
            print(f"[{vid_id}] {model_name} error: {e}")
            time.sleep(2)
            
    if not success:
        print(f"[{vid_id}] Falling back to edge-tts with en-US-ChristopherNeural...")
        subprocess.run(["edge-tts", "--voice", "en-US-ChristopherNeural", "--text", script_text, "--write-media", raw_wav], check=True)
    
    # Trim dead air and breathless cadence
    cmd = [
        "ffmpeg", "-y",
        "-i", raw_wav,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.10:stop_threshold=-35dB,atempo=1.28",
        fast_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fast_wav]
    dur = float(subprocess.check_output(probe_cmd, text=True).strip())
    print(f"[{vid_id}] Fast breathless voiceover ready: {dur:.2f}s")
    return dur

def main():
    with open("temp/batch_10_config.json", "r", encoding="utf-8") as f:
        configs = json.load(f)
        
    durations = {}
    for conf in configs:
        dur = generate_one_voice(conf)
        durations[conf["vid_id"]] = dur
        
    with open("temp/batch_10_durations.json", "w", encoding="utf-8") as f:
        json.dump(durations, f, indent=2)
    print("\nAll 10 voiceovers generated successfully!")

if __name__ == "__main__":
    main()
