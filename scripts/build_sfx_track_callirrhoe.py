import subprocess
import os

def build_sfx_track(duration=35.52):
    os.makedirs("temp", exist_ok=True)
    out_sfx = "temp/sfx_track_callirrhoe.wav"
    
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.90),     # t=0.00s: Metal Gear Alert on INTRO.mp4 hook
        ("shared/sfx/whoosh.mp3", 4800, 0.50),            # t=4.80s: Transition to peaceful pier
        ("shared/sfx/pop.mp3", 5100, 0.65),               # t=5.10s: Subtitle pop
        ("shared/sfx/whoosh.mp3", 8200, 0.45),            # t=8.20s: Water boils red
        ("shared/sfx/vine_boom.mp3", 12000, 0.85),        # t=12.00s: Monster charges dock
        ("shared/sfx/gunshot.mp3", 16400, 0.85),          # t=16.40s: Shotgun equip
        ("shared/sfx/hitmarker.mp3", 19800, 0.75),        # t=19.80s: Shootout impact
        ("shared/sfx/whoosh.mp3", 23100, 0.50),           # t=23.10s: Speedboat into ocean
        ("shared/sfx/gunshot.mp3", 26500, 0.85),          # t=26.50s: Colossal titan boss shootout
        ("shared/sfx/vine_boom.mp3", 30300, 0.90),        # t=30.30s: 3D Endcard slam
        ("shared/sfx/ding.mp3", 33500, 0.75),             # t=33.50s: CTA ding
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
    
    print(f"Generating sfx_track_callirrhoe.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("ERROR creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
