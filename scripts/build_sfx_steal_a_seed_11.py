import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/pop.mp3", 650, 0.80),                   # t=0.65s: STEAL A SEED pop
    ("assets/sfx/ding.mp3", 1400, 0.85),                 # t=1.40s: Free Reward pop-up appear
    ("assets/sfx/hitmarker.mp3", 2650, 0.85),            # t=2.65s: FREE OP ICEFLUFF SEED
    ("assets/sfx/pop.mp3", 4550, 0.80),                  # t=4.55s: WALL NUT text pop
    ("assets/sfx/vine_boom.mp3", 5050, 0.90),            # t=5.05s: Cut to boss monster chase
    ("assets/sfx/metal_pipe.mp3", 7350, 0.80),           # t=7.35s: WIPED OUT warning
    ("assets/sfx/whoosh.mp3", 8850, 0.75),               # t=8.85s: PATROL MONSTERS charge
    ("assets/sfx/whoosh.mp3", 9650, 0.70),               # t=9.65s: Cut to rare plots
    ("assets/sfx/punch.mp3", 11450, 0.85),               # t=11.45s: GRAB WALL NUT SEED
    ("assets/sfx/ding.mp3", 13250, 0.80),                # t=13.25s: THIRTY-NINE DOLLARS
    ("assets/sfx/whoosh.mp3", 15350, 0.70),              # t=15.35s: Cut to garden planting
    ("assets/sfx/ding.mp3", 17050, 0.85),                # t=17.05s: OVER 60,000 CASH
    ("assets/sfx/bass_drop.mp3", 18650, 0.80),           # t=18.65s: TOP POWER LEADERBOARD
    ("assets/sfx/whoosh.mp3", 20500, 0.75),              # t=20.50s: Living Endcard entry
    ("assets/sfx/ding.mp3", 22250, 0.85),                # t=22.25s: SEARCH STEAL A SEED
    ("assets/sfx/hitmarker.mp3", 23550, 0.80),           # t=23.55s: PLAY RIGHT NOW CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_11.wav")
    dur = 24.15

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

    print("Building composite SFX track for Steal a Seed Video 11 (Free OP Icefluff & Rare Wall Nut)...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
