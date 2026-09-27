import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/ding.mp3", 700, 0.85),                  # t=0.70s: COCO CANNON PLANT
    ("assets/sfx/ding.mp3", 1550, 0.85),                 # t=1.55s: $50,000 CASH
    ("assets/sfx/pop.mp3", 2850, 0.80),                  # t=2.85s: IN STEAL A SEED
    ("assets/sfx/bass_drop.mp3", 4550, 0.80),            # t=4.55s: 20,000 SPEED
    ("assets/sfx/whoosh.mp3", 5280, 0.70),               # t=5.28s: Cut to desert zone
    ("assets/sfx/vine_boom.mp3", 7550, 0.90),            # t=7.55s: GET CAUGHT
    ("assets/sfx/metal_pipe.mp3", 8150, 0.80),           # t=8.15s: LOSE EVERYTHING
    ("assets/sfx/whoosh.mp3", 8960, 0.70),               # t=8.96s: Cut to treadmill gym
    ("assets/sfx/ding.mp3", 11000, 0.85),                # t=11.00s: +12 LIGHTNING MULTIPLIERS
    ("assets/sfx/whoosh.mp3", 13850, 0.75),              # t=13.85s: Cut to 21K speed sprint
    ("assets/sfx/bass_drop.mp3", 14850, 0.80),           # t=14.85s: 21,000 SPEED
    ("assets/sfx/whoosh.mp3", 16010, 0.70),              # t=16.01s: BLITZ PAST MONSTERS
    ("assets/sfx/hitmarker.mp3", 17400, 0.85),           # t=17.40s: STEAL SUCCESSFUL
    ("assets/sfx/ding.mp3", 19650, 0.85),                # t=19.65s: PRINT MILLIONS
    ("assets/sfx/whoosh.mp3", 20800, 0.75),              # t=20.80s: Living Endcard entry
    ("assets/sfx/ding.mp3", 22200, 0.85),                # t=22.20s: SEARCH STEAL A SEED
    ("assets/sfx/hitmarker.mp3", 23500, 0.80),           # t=23.50s: PLAY RIGHT NOW CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_13.wav")
    dur = 24.50

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

    print("Building composite SFX track for Steal a Seed Video 13 (Mythic Coco Cannon)...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
