import subprocess
import os

def build_sfx_track(duration=25.38):
    os.makedirs("temp/how_to_fisch", exist_ok=True)
    out_sfx = "temp/how_to_fisch/sfx_track_htf_v10.wav"
    
    # Total duration = 25.38s
    events = [
        ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
        ("shared/sfx/whoosh.mp3", 3400, 0.50),              # t=3.40s: Whoosh to gameplay / badge
        ("shared/sfx/vine_boom.mp3", 7200, 0.85),           # t=7.20s: Sun fish boss leaps out
        ("shared/sfx/bass_drop.mp3", 9300, 0.70),           # t=9.30s: Boss charge
        ("shared/sfx/ding.mp3", 12400, 0.75),               # t=12.40s: Armory weapon roll
        ("shared/sfx/gunshot.mp3", 14500, 0.80),            # t=14.50s: Pistol gunshot
        ("shared/sfx/hitmarker.mp3", 15600, 0.65),          # t=15.60s: Boss damage hitmarker
        ("shared/sfx/whoosh.mp3", 17500, 0.50),             # t=17.50s: Motorboat engine whoosh
        ("shared/sfx/punch.mp3", 21000, 0.80),              # t=21.00s: 3D Endcard impact
        ("shared/sfx/ding.mp3", 22800, 0.70),               # t=22.80s: Final CTA chime
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
    
    print(f"Generating sfx_track_htf_v10.wav (Duration: {duration:.2f}s)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Error creating SFX track:")
        print(res.stderr[-500:])
        return False
    print(f"Generated {out_sfx} successfully! Size: {os.path.getsize(out_sfx)} bytes")
    return True

if __name__ == "__main__":
    build_sfx_track()
