import subprocess
import os

def build_sfx_track(duration=23.50):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = "temp/tongue_escape/sfx_track_v03.wav"
    
    # List of (file, delay_ms, volume)
    # Total duration = 23.50s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Metal Gear Alert hook
        ("shared/sfx/whoosh.mp3", 2000, 0.45),              # t=2.00s: Transition to codes menu
        ("shared/sfx/pop.mp3", 4100, 0.60),                 # t=4.10s: 15,000 studs teaser pop
        ("shared/sfx/ding.mp3", 7800, 0.80),                # t=7.80s: WELCOME1 redeemed ding!
        ("shared/sfx/ding.mp3", 10400, 0.80),               # t=10.40s: BONUS500 redeemed ding!
        ("shared/sfx/bass_drop.mp3", 12700, 0.75),          # t=12.70s: FREEBOOST 2x powerup bass!
        ("shared/sfx/whoosh.mp3", 15000, 0.50),             # t=15.00s: Whoosh across lava chasm
        ("shared/sfx/punch.mp3", 17600, 0.80),              # t=17.60s: Punch impact Stage 7
        ("shared/sfx/hitmarker.mp3", 17650, 0.65),          # t=17.65s: Hitmarker Stage 7 win
        ("shared/sfx/vine_boom.mp3", 19600, 0.85),          # t=19.60s: Endcard slam!
        ("shared/sfx/ding.mp3", 21300, 0.70),               # t=21.30s: Link in bio ding!
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
    
    print(f"Generating sfx_track_v03.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
