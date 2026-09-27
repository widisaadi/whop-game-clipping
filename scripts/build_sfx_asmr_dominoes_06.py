import subprocess
import os

def build_sfx():
    out_dir = "temp/asmr_dominoes"
    os.makedirs(out_dir, exist_ok=True)
    out_wav = os.path.join(out_dir, "sfx_track_ad_06.wav")
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.00, 0.95),  # t=0.00s: Metal Gear Alert on INTRO avatar hook
        ("assets/sfx/whoosh.mp3", 1.40, 0.85),            # t=1.40s: Cut to hypnotic spiral topple
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 2.50, 0.90), # t=2.50s: Domino crunch cascade
        ("assets/sfx/whoosh.mp3", 3.98, 0.85),            # t=3.98s: Cut to sound shop
        ("assets/sfx/pop.mp3", 6.10, 0.85),               # t=6.10s: Equip custom sounds
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 7.35, 0.95), # t=7.35s: Celery crunch
        ("assets/sfx/hitmarker.mp3", 8.00, 0.80),         # t=8.00s: Bamboo clacks
        ("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 8.65, 0.90),    # t=8.65s: Bubble pops
        ("assets/sfx/whoosh.mp3", 9.38, 0.85),            # t=9.38s: Cut to drag brush build
        ("assets/sfx/ding.mp3", 11.20, 0.85),             # t=11.20s: 1,000 dominoes ding
        ("assets/sfx/pop.mp3", 14.15, 0.85),              # t=14.15s: Scale slider crank pop
        ("assets/sfx/bass_drop.mp3", 15.52, 0.90),        # t=15.52s: Hit topple mode bass drop
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 16.85, 0.90),# t=16.85s: Spiral collapse crunch
        ("assets/sfx/whoosh.mp3", 19.25, 0.90),           # t=19.25s: Massive black hole
        ("assets/sfx/whoosh.mp3", 19.92, 0.85),           # t=19.92s: Living Endcard entrance
        ("assets/sfx/ding.mp3", 20.30, 0.90)              # t=20.30s: Endcard pop chime
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
    
    print("Building full ASMR Dominoes Video 06 SFX track...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_wav, "-show_entries", "format=duration,size", "-v", "quiet", "-of", "csv=p=0"]
    pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
    print(f"Generated SFX Track: {out_wav} -> {pres.stdout.strip()}")
    return out_wav

if __name__ == "__main__":
    build_sfx()
