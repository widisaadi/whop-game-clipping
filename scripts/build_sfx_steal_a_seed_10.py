import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/pop.mp3", 950, 0.80),                   # t=0.95s: STEAL GIANT SEEDS
    ("assets/sfx/hitmarker.mp3", 1850, 0.85),            # t=1.85s: TERRIFYING MONSTERS
    ("assets/sfx/ding.mp3", 2950, 0.85),                 # t=2.95s: MILLIONAIRE TYCOON!
    ("assets/sfx/vine_boom.mp3", 4300, 0.90),            # t=4.30s: THE CATCH?
    ("assets/sfx/whoosh.mp3", 5100, 0.70),               # t=5.10s: BOSS MONSTERS charge
    ("assets/sfx/metal_pipe.mp3", 7500, 0.80),           # t=7.50s: LOSE EVERYTHING!
    ("assets/sfx/whoosh.mp3", 8900, 0.70),               # t=8.90s: Cut to desert SNEAK IN
    ("assets/sfx/punch.mp3", 10100, 0.80),               # t=10.10s: HEAVY SEED grab
    ("assets/sfx/whoosh.mp3", 11500, 0.70),              # t=11.50s: SPRINT FOR BORDER
    ("assets/sfx/hitmarker.mp3", 12800, 0.85),           # t=12.80s: MONSTER CHASING!
    ("assets/sfx/ding.mp3", 14200, 0.85),                # t=14.20s: ESCAPE! Steal Successful
    ("assets/sfx/pop.mp3", 15150, 0.80),                 # t=15.15s: PLANT THE SEED
    ("assets/sfx/ding.mp3", 16500, 0.85),                # t=16.50s: INSANE CASH
    ("assets/sfx/whoosh.mp3", 17800, 0.70),              # t=17.80s: GYM TREADMILLS
    ("assets/sfx/bass_drop.mp3", 18600, 0.80),           # t=18.60s: 20,000 SPEED!
    ("assets/sfx/whoosh.mp3", 19500, 0.75),              # t=19.50s: Living Endcard entry
    ("assets/sfx/ding.mp3", 21000, 0.80),                # t=21.00s: PLAY ON ROBLOX CTA punch
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_10.wav")
    dur = 23.83

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

    print("Building composite SFX track for Steal a Seed Video 10 (Heist)...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
