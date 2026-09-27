import subprocess
import os

def build_sfx_track(duration=19.40):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v09.wav"
    
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("assets/sfx/whoosh.mp3", 1250, 0.70),              # t=1.25s: Cliff drop / near-lava fall
        ("assets/sfx/whoosh.mp3", 3500, 0.60),              # t=3.50s: Giant tongue bridge shoot
        ("assets/sfx/pop.mp3", 6250, 0.65),                 # t=6.25s: Honeycomb obstacle dodge
        ("assets/sfx/ding.mp3", 8750, 0.70),                # t=8.75s: Gym treadmill studs chime
        ("assets/sfx/bass_drop.mp3", 11500, 0.75),          # t=11.50s: Max level tongue escalation
        ("assets/sfx/hitmarker.mp3", 13500, 0.80),          # t=13.50s: Stage 7 conquest
        ("assets/sfx/vine_boom.mp3", 15500, 0.85),          # t=15.50s: Living Endcard slam
        ("assets/sfx/ding.mp3", 17500, 0.75),               # t=17.50s: Link in bio CTA chime
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
    
    print(f"Generating sfx_track_v09.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track(duration=19.40)
