import os
import subprocess
from gemini_tts import request_tts_with_rotation

SCRIPT_15 = (
    "Stop playing Steal a Seed broke when these three secret codes give you 250,000 cash and rare seeds instantly! "
    "Most beginners start with zero cash and get crushed by monsters before they can even buy a weapon! "
    "First code ADMINABUSE gives you 200 free gems, and code FREEZING unlocks the exclusive Vine Seed! "
    "Then redeem code 35KLIKES to instantly dump a quarter million dollars into your balance, upgrading your speed past twenty thousand! "
    "Now we unlocked the legendary Coco Cannon printing fifty thousand cash a second! "
    "Redeem them right now! Game is called Steal a Seed on Roblox, link in bio!"
)

def main():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    raw_wav = os.path.join(temp_dir, "voiceover_15_raw.wav")
    fast_wav = os.path.join(temp_dir, "voiceover_15_fast.wav")
    
    print("Generating Puck voiceover for Steal a Seed Video 15 (3 Secret Working Codes)...")
    request_tts_with_rotation(SCRIPT_15, voice_name="Puck", output_raw_wav=raw_wav)
    
    # Standar Emas BloxClips: Pangkas dead air >100ms dan pacing cepat ~3.9 wps
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
    print(f"\n[DONE] Generated breathless voiceover: {fast_wav} ({fast_dur:.2f}s)")
    return fast_dur

if __name__ == "__main__":
    main()
