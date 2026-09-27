import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/whoosh.mp3", 1400, 0.65),               # t=1.40s: Cut to Desert Zone
    ("assets/sfx/bass_drop.mp3", 2450, 0.75),            # t=2.45s: Desert Zone warning!
    ("assets/sfx/pop.mp3", 4900, 0.70),                  # t=4.90s: Grab Thorn Seed
    ("assets/sfx/bass_drop.mp3", 6600, 0.80),            # t=6.60s: Giant Cactus Monster!
    ("assets/sfx/whoosh.mp3", 8500, 0.70),               # t=8.50s: 13,000 speed sprint
    ("assets/sfx/ding.mp3", 10950, 0.85),                # t=10.95s: Steal Successful!
    ("assets/sfx/pop.mp3", 12000, 0.70),                 # t=12.00s: Planted in farm
    ("assets/sfx/hitmarker.mp3", 13400, 0.75),           # t=13.40s: +62,000 cash/sec
    ("assets/sfx/vine_boom.mp3", 15600, 0.85),           # t=15.60s: Legendary Coco Cannon!
    ("assets/sfx/ding.mp3", 17500, 0.80),                # t=17.50s: Half a million per second!
    ("assets/sfx/whoosh.mp3", 19100, 0.70),              # t=19.10s: Outrun everyone on the server!
    ("assets/sfx/whoosh.mp3", 21000, 0.75),              # t=21.00s: Living Endcard entry
    ("assets/sfx/ding.mp3", 22200, 0.80),                # t=22.20s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_04.wav")
    dur = 24.88

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

    print("Building composite SFX track for Steal a Seed Video 04...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
