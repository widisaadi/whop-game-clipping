import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/whoosh.mp3", 1400, 0.70),               # t=1.40s: Desert Zone entry
    ("assets/sfx/pop.mp3", 2400, 0.80),                  # t=2.40s: Grabbing grey pillar seed
    ("assets/sfx/vine_boom.mp3", 3400, 0.85),            # t=3.40s: Brown Cactus chases!
    ("assets/sfx/whoosh.mp3", 5200, 0.70),               # t=5.20s: Cut to Green Cactus trap
    ("assets/sfx/vine_boom.mp3", 6000, 0.90),            # t=6.00s: Second Green Cactus leaps out!
    ("assets/sfx/whoosh.mp3", 8400, 0.70),               # t=8.40s: Juking across border
    ("assets/sfx/hitmarker.mp3", 9500, 0.75),           # t=9.50s: Steal successful!
    ("assets/sfx/whoosh.mp3", 11200, 0.70),              # t=11.20s: Garden planting
    ("assets/sfx/pop.mp3", 12500, 0.85),                 # t=12.50s: Frost Mini Cactus claimed
    ("assets/sfx/ding.mp3", 13800, 0.80),                # t=13.80s: Steady cash chime
    ("assets/sfx/whoosh.mp3", 14800, 0.70),              # t=14.80s: Mega garden jumping
    ("assets/sfx/ding.mp3", 16000, 0.80),                # t=16.00s: +$62,974/s cash chime
    ("assets/sfx/bass_drop.mp3", 17500, 0.80),           # t=17.50s: Cash explosion flex
    ("assets/sfx/whoosh.mp3", 18800, 0.75),              # t=18.80s: Living Endcard entry
    ("assets/sfx/ding.mp3", 19800, 0.80),                # t=19.80s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_08.wav")
    dur = 22.80

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

    print("Building composite SFX track for Steal a Seed Video 08...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
