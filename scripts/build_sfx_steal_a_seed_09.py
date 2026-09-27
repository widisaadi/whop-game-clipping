import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/whoosh.mp3", 1400, 0.70),               # t=1.40s: Cut to base 100 speed
    ("assets/sfx/ding.mp3", 2200, 0.80),                 # t=2.20s: Leaderboard tease
    ("assets/sfx/whoosh.mp3", 5000, 0.70),               # t=5.00s: Wooden stick & 0 cash
    ("assets/sfx/vine_boom.mp3", 7200, 0.90),            # t=7.20s: Giant pumpkin boss ambush!
    ("assets/sfx/whoosh.mp3", 9420, 0.70),               # t=9.42s: Cut to gym treadmills
    ("assets/sfx/ding.mp3", 10500, 0.85),                # t=10.50s: Lightning multipliers +12/s
    ("assets/sfx/hitmarker.mp3", 12000, 0.85),           # t=12.00s: 20,000 speed hitmarker!
    ("assets/sfx/whoosh.mp3", 14150, 0.70),              # t=14.15s: Cut to glowing block heist
    ("assets/sfx/pop.mp3", 15000, 0.85),                 # t=15.00s: Steal successful pop!
    ("assets/sfx/ding.mp3", 16400, 0.85),                # t=16.40s: Electric cube & Top Power
    ("assets/sfx/bass_drop.mp3", 17500, 0.80),           # t=17.50s: Superpower flex
    ("assets/sfx/whoosh.mp3", 18650, 0.75),              # t=18.65s: Living Endcard entry
    ("assets/sfx/ding.mp3", 19800, 0.80),                # t=19.80s: Search on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_09.wav")
    dur = 22.57

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

    print("Building composite SFX track for Steal a Seed Video 09...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
