import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Opening avatar shock
    ("assets/sfx/bass_drop.mp3", 100, 0.75),             # t=0.10s: Sub-bass impact
    ("assets/sfx/whoosh.mp3", 1400, 0.70),               # t=1.40s: Cut to Snowlands heist
    ("assets/sfx/vine_boom.mp3", 3800, 0.85),            # t=3.80s: Ragdoll flip across line
    ("assets/sfx/punch.mp3", 4000, 0.75),                # t=4.00s: Impact on ground
    ("assets/sfx/whoosh.mp3", 5200, 0.65),               # t=5.20s: Snowman wipeout
    ("assets/sfx/whoosh.mp3", 8300, 0.70),               # t=8.30s: Treadmill gym upgrade
    ("assets/sfx/ding.mp3", 9200, 0.85),                 # t=9.20s: Upgrade Level 1 -> Level 2
    ("assets/sfx/hitmarker.mp3", 10200, 0.75),           # t=10.20s: 10,000 speed hit
    ("assets/sfx/whoosh.mp3", 11000, 0.70),              # t=11.00s: Infiltrating Snowlands round 2
    ("assets/sfx/pop.mp3", 12200, 0.80),                 # t=12.20s: Grabbing frozen pillar seed
    ("assets/sfx/whoosh.mp3", 13700, 0.70),              # t=13.70s: Water bucket & neon purple trail
    ("assets/sfx/ding.mp3", 15000, 0.80),                # t=15.00s: Water bucket boost
    ("assets/sfx/whoosh.mp3", 16700, 0.70),              # t=16.70s: Garden explosion
    ("assets/sfx/pop.mp3", 17800, 0.85),                 # t=17.80s: Over $1.2M/s cash rate
    ("assets/sfx/ding.mp3", 19200, 0.80),                # t=19.20s: Multipliers soaring
    ("assets/sfx/pop.mp3", 20000, 0.85),                 # t=20.00s: Giant Wall Nut equipped
    ("assets/sfx/whoosh.mp3", 21800, 0.75),              # t=21.80s: Living Endcard entry
    ("assets/sfx/ding.mp3", 22800, 0.80),                # t=22.80s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_05.wav")
    dur = 25.68

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

    print("Building composite SFX track for Steal a Seed Video 05...")
    subprocess.run(cmd, check=True)
    
    # Verify duration
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
