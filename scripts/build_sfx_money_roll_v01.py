import subprocess
import os

def build_sfx(duration=19.50):
    os.makedirs("temp/money_roll", exist_ok=True)
    out_sfx = "temp/money_roll/sfx_track_v01.wav"
    
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
        ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
        ("shared/sfx/pop.mp3", 2800, 0.60),                 # t=2.80s: Cash roll pop
        ("shared/sfx/ding.mp3", 5200, 0.70),                # t=5.20s: Infinite cash ding
        ("shared/sfx/ding.mp3", 7600, 0.75),                # t=7.60s: Hatch legendary pets ding
        ("shared/sfx/whoosh.mp3", 10000, 0.50),             # t=10.00s: Gym speed whoosh
        ("shared/sfx/bass_drop.mp3", 12200, 0.70),          # t=12.20s: Secret stage bass drop
        ("shared/sfx/punch.mp3", 14000, 0.80),              # t=14.00s: Richest player punch
        ("shared/sfx/vine_boom.mp3", 15600, 0.85),          # t=15.60s: Endcard slam!
        ("shared/sfx/ding.mp3", 17500, 0.70),               # t=17.50s: Map code chime
    ]
    
    inputs = []
    filter_parts = []
    
    for idx, (path, delay_ms, vol) in enumerate(events):
        inputs.extend(["-i", path])
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f},aresample=48000[a{idx}];")
    
    mix_inputs = "".join(f"[a{idx}]" for idx in range(len(events)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(events)}:duration=longest:normalize=0[aout]")
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", "".join(filter_parts),
        "-map", "[aout]",
        "-t", f"{duration:.2f}",
        "-ar", "48000",
        "-ac", "2",
        out_sfx
    ]
    
    print(f"Generating {out_sfx} (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"--> Generated {out_sfx} ({os.path.getsize(out_sfx)} bytes)")
    return True

if __name__ == "__main__":
    build_sfx()
