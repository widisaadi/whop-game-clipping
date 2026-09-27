import subprocess
import os

EVENTS = [
    ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),        # t=0.00s: Hook opener
    ("assets/sfx/whoosh.mp3", 1400, 0.65),               # t=1.40s: Hard cut to $0 broke
    ("assets/sfx/bass_drop.mp3", 2400, 0.75),            # t=2.40s: Broke with $0 cash!
    ("assets/sfx/whoosh.mp3", 5750, 0.65),               # t=5.75s: Developers dropped code
    ("assets/sfx/vine_boom.mp3", 7950, 0.85),            # t=7.95s: 35KLIKES badge popup
    ("assets/sfx/pop.mp3", 8850, 0.70),                  # t=8.85s: Type in 35KLIKES
    ("assets/sfx/ding.mp3", 10900, 0.80),                # t=10.90s: Claim 250,000 cash!
    ("assets/sfx/hitmarker.mp3", 11600, 0.75),           # t=11.60s: Cash hit chime
    ("assets/sfx/whoosh.mp3", 13000, 0.65),              # t=13.00s: Item shop water buckets
    ("assets/sfx/pop.mp3", 15750, 0.70),                 # t=15.75s: Treadmill speed
    ("assets/sfx/bass_drop.mp3", 17500, 0.75),           # t=17.50s: Redeem before it expires
    ("assets/sfx/whoosh.mp3", 18700, 0.70),              # t=18.70s: Living Endcard entry
    ("assets/sfx/ding.mp3", 19700, 0.80),                # t=19.70s: Play on Roblox CTA
]

def build_sfx():
    temp_dir = "temp/steal_a_seed"
    os.makedirs(temp_dir, exist_ok=True)
    out_sfx = os.path.join(temp_dir, "sfx_track_sas_02.wav")
    dur = 22.20

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

    print("Building composite SFX track for Steal a Seed Video 02 (Fixed duration & normalize=0)...")
    subprocess.run(cmd, check=True)
    pcmd = ["ffprobe", "-i", out_sfx, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    actual_dur = float(subprocess.check_output(pcmd, text=True).strip())
    print(f"Generated verified SFX track: {out_sfx} (Duration: {actual_dur:.2f}s)")
    return actual_dur

if __name__ == "__main__":
    build_sfx()
