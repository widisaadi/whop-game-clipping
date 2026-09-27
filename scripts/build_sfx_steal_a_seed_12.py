import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/ding.mp3", 1450, 0.85),                 # t=1.45s: $1.17 MILLION highlight
    ("assets/sfx/pop.mp3", 3200, 0.80),                  # t=3.20s: STEAL A SEED brand pop
    ("assets/sfx/hitmarker.mp3", 4800, 0.85),            # t=4.80s: SECRET ITEM SHOP
    ("assets/sfx/whoosh.mp3", 6450, 0.70),               # t=6.45s: Cut to desert zone
    ("assets/sfx/vine_boom.mp3", 8450, 0.90),            # t=8.45s: SPIKY CACTUS MONSTER
    ("assets/sfx/metal_pipe.mp3", 9350, 0.80),           # t=9.35s: WIPE YOU OUT alarm
    ("assets/sfx/whoosh.mp3", 11160, 0.70),              # t=11.16s: Cut to Item Shop
    ("assets/sfx/ding.mp3", 13000, 0.80),                # t=13.00s: FROZEN GRENADES
    ("assets/sfx/punch.mp3", 13900, 0.85),               # t=13.90s: BEAR TRAPS
    ("assets/sfx/whoosh.mp3", 15150, 0.75),              # t=15.15s: CYAN LASER TRAIL
    ("assets/sfx/bass_drop.mp3", 16650, 0.80),           # t=16.65s: 13,000 SPEED sprint
    ("assets/sfx/ding.mp3", 17350, 0.85),                # t=17.35s: GLOWING CRYSTAL GOLEMS
    ("assets/sfx/ding.mp3", 21750, 0.85),                # t=21.75s: 1.17 MILLION CASH
    ("assets/sfx/whoosh.mp3", 23500, 0.75),              # t=23.50s: Living Endcard entry
    ("assets/sfx/ding.mp3", 25500, 0.85),                # t=25.50s: SEARCH STEAL A SEED
    ("assets/sfx/hitmarker.mp3", 27000, 0.80),           # t=27.00s: PLAY RIGHT NOW CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_12.wav")
    dur = 27.99

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

    print("Building composite SFX track for Steal a Seed Video 12...")
    subprocess.run(cmd, check=True)
    
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
