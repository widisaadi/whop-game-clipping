import subprocess
import os

def build_sfx():
    out_dir = "temp/asmr_dominoes"
    os.makedirs(out_dir, exist_ok=True)
    out_wav = os.path.join(out_dir, "sfx_track_ad_01.wav")
    
    # SFX events mapped to video timeline with INTRO.mp4 hook & Living Endcard
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.00, 0.95),  # t=0.00s: Metal Gear Alert on INTRO.mp4 avatar shock
        ("assets/sfx/whoosh.mp3", 1.40, 0.85),            # t=1.40s: Cut from avatar shock to black hole teaser
        ("assets/sfx/bass_drop.mp3", 1.60, 0.80),
        ("assets/sfx/whoosh.mp3", 3.96, 0.85),            # t=3.96s: Cut to Level 1 green dominoes
        ("assets/sfx/pop.mp3", 4.50, 0.70),
        ("assets/sfx/pop.mp3", 5.20, 0.70),
        ("assets/sfx/whoosh.mp3", 7.48, 0.85),            # t=7.48s: Cut to drag brush build
        ("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 8.20, 0.75),
        ("assets/sfx/ding.mp3", 10.48, 0.85),             # t=10.48s: Scale slider
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 12.68, 0.90), # t=12.68s: Spiral topple mode
        ("assets/sfx/ding.mp3", 14.50, 0.80),             # t=14.50s: Multipliers burst
        ("assets/sfx/vine_boom.mp3", 15.82, 0.90),        # t=15.82s: Level 999 singularity reveal
        ("assets/sfx/whoosh.mp3", 17.38, 0.85),
        ("assets/sfx/bass_drop.mp3", 17.80, 0.90),        # t=17.80s: Singularity swallows map
        ("assets/sfx/whoosh.mp3", 20.00, 0.85),           # t=20.00s: Living Endcard entrance
        ("assets/sfx/ding.mp3", 20.30, 0.85)              # t=20.30s: Endcard card pop chime
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
    # Golden rule: duration=longest:normalize=0 ensures all 16 SFX persist across full duration
    mix_filter = f"{mix_ins}amix=inputs={len(events)}:duration=longest:normalize=0:dropout_transition=0,volume=1.0[outa]"
    full_filter = "".join(filter_parts) + mix_filter
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[outa]",
        "-t", "23.75",
        out_wav
    ]
    
    print("Building full ASMR Dominoes SFX track...")
    subprocess.run(cmd, check=True)
    
    # Check duration and size
    pcmd = ["ffprobe", "-i", out_wav, "-show_entries", "format=duration,size", "-v", "quiet", "-of", "csv=p=0"]
    pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
    print(f"Generated SFX Track: {out_wav} -> {pres.stdout.strip()}")
    return out_wav

if __name__ == "__main__":
    build_sfx()
