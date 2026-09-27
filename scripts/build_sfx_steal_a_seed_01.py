import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook opener
    ("assets/sfx/whoosh.mp3", 2500, 0.65),              # t=2.50s: Enemy territory
    ("assets/sfx/bass_drop.mp3", 5350, 0.75),           # t=5.35s: Enraged monster!
    ("assets/sfx/pop.mp3", 8200, 0.70),                 # t=8.20s: Grab seed & alert
    ("assets/sfx/ding.mp3", 11100, 0.80),               # t=11.10s: Steal successful!
    ("assets/sfx/ding.mp3", 14250, 0.75),               # t=14.25s: Harvest cash
    ("assets/sfx/whoosh.mp3", 18050, 0.70),             # t=18.05s: 20k speed trail
    ("assets/sfx/hitmarker.mp3", 20250, 0.80),          # t=20.25s: Legendary cannons
    ("assets/sfx/vine_boom.mp3", 22450, 0.85),          # t=22.45s: Endcard slam
    ("assets/sfx/ding.mp3", 23400, 0.80),               # t=23.40s: Play on Roblox
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_01.wav")
    dur = 24.65

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

    print("Building composite SFX track for Steal a Seed Video 01 (Fixed duration & normalize=0)...")
    subprocess.run(cmd, check=True)
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
