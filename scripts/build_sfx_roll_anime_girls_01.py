import subprocess
import os

def build_sfx():
    out_dir = "temp/roll_anime_girls"
    os.makedirs(out_dir, exist_ok=True)
    out_wav = os.path.join(out_dir, "sfx_track_rag_01.wav")
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.00, 0.95),  # t=0.00s: Metal Gear Alert on INTRO avatar hook
        ("assets/sfx/whoosh.mp3", 1.40, 0.85),            # t=1.40s: Cut to roll dice
        ("assets/sfx/ding.mp3", 2.80, 0.85),              # t=2.80s: Dice roll anime girl summon
        ("assets/sfx/whoosh.mp3", 4.32, 0.85),            # t=4.32s: Cut to empty plot
        ("assets/sfx/pop.mp3", 6.85, 0.85),               # t=6.85s: Roll dice unlock character
        ("assets/sfx/pop.mp3", 8.54, 0.85),               # t=8.54s: Place character on plot pad
        ("assets/sfx/ding.mp3", 10.75, 0.85),             # t=10.75s: Passive money cash register
        ("assets/sfx/whoosh.mp3", 14.58, 0.85),           # t=14.58s: Cut to luck potions stall
        ("assets/sfx/ding.mp3", 16.05, 0.85),             # t=16.05s: Legendary drop chime
        ("assets/sfx/bass_drop.mp3", 16.95, 0.90),        # t=16.95s: Hit rebirth button
        ("assets/sfx/ding.mp3", 18.95, 0.85),             # t=18.95s: Permanent multiplier unlocked
        ("assets/sfx/whoosh.mp3", 19.80, 0.85),           # t=19.80s: Living Endcard entrance
        ("assets/sfx/ding.mp3", 20.20, 0.90)              # t=20.20s: Endcard pop chime
    ]
    
    inputs = []
    filter_parts = []
    
    for i, (fpath, delay_sec, vol) in enumerate(events):
        delay_ms = int(delay_sec * 1000)
        inputs.extend(["-i", fpath])
        filter_parts.append(
            f"[{i}:a]volume={vol:.2f},adelay={delay_ms}|{delay_ms},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[s{i}];"
        )
        
    mix_ins = "".join([f"[s{i}]" for i in range(len(events))])
    mix_filter = f"{mix_ins}amix=inputs={len(events)}:duration=longest:normalize=0:dropout_transition=0,volume=1.0[outa]"
    full_filter = "".join(filter_parts) + mix_filter
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[outa]",
        "-t", "24.20",
        out_wav
    ]
    
    print("Building full Roll Anime Girls Video 01 SFX track...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_wav, "-show_entries", "format=duration,size", "-v", "quiet", "-of", "csv=p=0"]
    pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
    print(f"Generated SFX Track: {out_wav} -> {pres.stdout.strip()}")
    return out_wav

if __name__ == "__main__":
    build_sfx()
