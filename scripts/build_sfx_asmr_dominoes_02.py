import subprocess
import os

def build_sfx():
    out_dir = "temp/asmr_dominoes"
    os.makedirs(out_dir, exist_ok=True)
    out_wav = os.path.join(out_dir, "sfx_track_ad_02.wav")
    
    # SFX events perfectly synchronized with updated semantic cuts & voiceover cues
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.00, 0.95),  # t=0.00s: Metal Gear Alert on INTRO.mp4 avatar shock
        ("assets/sfx/whoosh.mp3", 1.40, 0.85),            # t=1.40s: Cut from avatar shock to rainbow bubbles
        ("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 2.50, 0.85), # t=2.50s: Bubble pop stem
        ("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 4.50, 0.85), # t=4.50s: Giant bubble floating pop
        ("assets/sfx/whoosh.mp3", 6.70, 0.85),            # t=6.70s: Cut to Sound Selector Shop
        ("assets/sfx/ding.mp3", 8.00, 0.80),              # t=8.00s: Custom ASMR menu click
        ("assets/sfx/pop.mp3", 9.80, 0.85),               # t=9.80s: Celery crack snap
        ("assets/sfx/ding.mp3", 10.60, 0.85),             # t=10.60s: Bamboo clack chime
        ("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 11.40, 0.85), # t=11.40s: Bubble pop stem
        ("assets/sfx/whoosh.mp3", 12.40, 0.85),           # t=12.40s: Cut to drag brush build
        ("assets/sfx/pop.mp3", 13.50, 0.80),              # t=13.50s: 500-tile rapid brush placement
        ("assets/sfx/ding.mp3", 15.00, 0.85),             # t=15.00s: Three seconds flat ding
        ("assets/sfx/whoosh.mp3", 16.30, 0.85),           # t=16.30s: Cut to spiral collapse
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 17.00, 0.90), # t=17.00s: Spiral domino cascade
        ("assets/sfx/ding.mp3", 19.00, 0.80),             # t=19.00s: Center collapse zero lag
        ("assets/sfx/whoosh.mp3", 20.60, 0.85),           # t=20.60s: Cut to obsidian topple crunch
        ("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 21.20, 0.90), # t=21.20s: Pure satisfying crunch stem
        ("assets/sfx/ding.mp3", 22.50, 0.85),             # t=22.50s: Floating cheese star burst
        ("assets/sfx/whoosh.mp3", 24.20, 0.85),           # t=24.20s: Living Endcard entrance
        ("assets/sfx/ding.mp3", 24.50, 0.85)              # t=24.50s: Endcard card pop chime
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
        "-t", "27.96",
        out_wav
    ]
    
    print("Building full ASMR Dominoes Video 02 SFX track...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_wav, "-show_entries", "format=duration,size", "-v", "quiet", "-of", "csv=p=0"]
    pres = subprocess.run(pcmd, stdout=subprocess.PIPE, text=True)
    print(f"Generated SFX Track: {out_wav} -> {pres.stdout.strip()}")
    return out_wav

if __name__ == "__main__":
    build_sfx()
