import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Hook opener
    ("assets/sfx/whoosh.mp3", 1400, 0.65),               # t=1.40s: Cut to slow run
    ("assets/sfx/bass_drop.mp3", 3150, 0.75),            # t=3.15s: Giant monster!
    ("assets/sfx/pop.mp3", 4600, 0.70),                  # t=4.60s: Monster catch us
    ("assets/sfx/whoosh.mp3", 6250, 0.65),               # t=6.25s: Treadmills in garden
    ("assets/sfx/ding.mp3", 8000, 0.80),                 # t=8.00s: +5 speed/s
    ("assets/sfx/pop.mp3", 9450, 0.70),                  # t=9.45s: Green track upgrade
    ("assets/sfx/hitmarker.mp3", 10600, 0.75),           # t=10.60s: 12 speed multipliers
    ("assets/sfx/vine_boom.mp3", 12500, 0.85),           # t=12.50s: Exploded over 21,000!
    ("assets/sfx/ding.mp3", 14100, 0.80),                # t=14.10s: Legendary Coco Cannons
    ("assets/sfx/whoosh.mp3", 17100, 0.70),              # t=17.10s: Literally fly across map
    ("assets/sfx/whoosh.mp3", 19800, 0.70),              # t=19.80s: Living Endcard entry
    ("assets/sfx/ding.mp3", 20800, 0.80),                # t=20.80s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_03.wav")
    dur = 23.30

    inputs = []
    filter_parts = []
    for idx, (path, delay_ms, vol) in enumerate(EVENTS):
        inputs.extend(["-i", path])
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f},aresample=48000[a{idx}];")

    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(EVENTS)))
    # CRITICAL: duration=longest and normalize=0 so delayed SFX across the entire 23.30s are preserved without volume attenuation
    filter_complex = "".join(filter_parts) + f"{mix_inputs}amix=inputs={len(EVENTS)}:duration=longest:normalize=0:dropout_transition=0,aformat=sample_fmts=fltp:channel_layouts=stereo[a]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[a]",
        "-t", f"{dur:.2f}",
        out_sfx
    ]

    print("Building composite SFX track for Steal a Seed Video 03 (Fixed full duration & normalize=0)...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
