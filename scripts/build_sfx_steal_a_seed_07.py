import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/whoosh.mp3", 1400, 0.70),               # t=1.40s: Desert Zone entry
    ("assets/sfx/pop.mp3", 2400, 0.80),                  # t=2.40s: Grabbing brown seed
    ("assets/sfx/vine_boom.mp3", 3600, 0.85),            # t=3.60s: Cactus Monster ambushes!
    ("assets/sfx/whoosh.mp3", 5900, 0.70),               # t=5.90s: Open Secret Item Shop
    ("assets/sfx/ding.mp3", 7000, 0.80),                 # t=7.00s: Frozen Grenades & Bear Traps
    ("assets/sfx/ding.mp3", 8400, 0.80),                 # t=8.40s: Mythic Water Bucket -80% time
    ("assets/sfx/whoosh.mp3", 9900, 0.70),               # t=9.90s: Trail Shop & laser speed trail
    ("assets/sfx/pop.mp3", 11000, 0.80),                 # t=11.00s: Equipping Cyan Trail
    ("assets/sfx/hitmarker.mp3", 12500, 0.75),           # t=12.50s: 13,000 speed hit
    ("assets/sfx/pop.mp3", 14700, 0.85),                 # t=14.70s: Legendary Pumpkin Baron
    ("assets/sfx/ding.mp3", 15500, 0.80),                # t=15.50s: Pumpkin Baron flex
    ("assets/sfx/whoosh.mp3", 16600, 0.70),              # t=16.60s: Mega garden overview
    ("assets/sfx/bass_drop.mp3", 17500, 0.80),           # t=17.50s: +$1.1M/s rate boom
    ("assets/sfx/whoosh.mp3", 18950, 0.75),              # t=18.95s: Living Endcard entry
    ("assets/sfx/ding.mp3", 19950, 0.80),                # t=19.95s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_07.wav")
    dur = 22.83

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

    print("Building composite SFX track for Steal a Seed Video 07...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
