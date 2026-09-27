import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/whoosh.mp3", 1400, 0.70),               # t=1.40s: Forest Zone entry
    ("assets/sfx/pop.mp3", 2500, 0.80),                  # t=2.50s: Suggested 900 speed
    ("assets/sfx/whoosh.mp3", 4400, 0.70),               # t=4.40s: Lifting Oak Seed
    ("assets/sfx/vine_boom.mp3", 5100, 0.85),            # t=5.10s: Red Monster charges!
    ("assets/sfx/whoosh.mp3", 7500, 0.70),               # t=7.50s: Sprint across red line
    ("assets/sfx/hitmarker.mp3", 8500, 0.75),           # t=8.50s: Steal successful!
    ("assets/sfx/whoosh.mp3", 10300, 0.70),              # t=10.30s: Planting in garden plot
    ("assets/sfx/ding.mp3", 11500, 0.80),                # t=11.50s: Countdown starts
    ("assets/sfx/pop.mp3", 13500, 0.85),                 # t=13.50s: Wall Nut harvested
    ("assets/sfx/ding.mp3", 14800, 0.80),                # t=14.80s: +$40k/s cash chime
    ("assets/sfx/whoosh.mp3", 16500, 0.70),              # t=16.50s: Garden explosion
    ("assets/sfx/bass_drop.mp3", 17200, 0.80),           # t=17.20s: +$1.1M/s rate flex
    ("assets/sfx/whoosh.mp3", 18500, 0.75),              # t=18.50s: Living Endcard entry
    ("assets/sfx/ding.mp3", 19500, 0.80),                # t=19.50s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_06.wav")
    dur = 22.38

    inputs = []
    filter_parts = []
    for idx, (path, delay_ms, vol) in enumerate(EVENTS):
        inputs.extend(["-i", path])
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f},aresample=48000[a{idx}];")

    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(EVENTS)))
    filter_complex = "".join(filter_parts) + f"{mix_inputs}amix=inputs={len(EVENTS)}:duration=longest:normalize=0:dropout_transition=0,aformat=sample_fmts=fltp:channel_layouts=stereo[a]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[a]",
        "-t", f"{dur:.2f}",
        out_sfx
    ]

    print("Building composite SFX track for Steal a Seed Video 06...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
