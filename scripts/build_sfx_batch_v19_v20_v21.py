import subprocess
import os

SFX_CONFIG = {
    "v19": {
        "duration": 18.23,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook opener
            ("shared/sfx/whoosh.mp3", 1800, 0.50),              # t=1.80s: Trapped on island
            ("shared/sfx/bass_drop.mp3", 3500, 0.65),           # t=3.50s: Jumping banned!
            ("shared/sfx/pop.mp3", 5800, 0.60),                 # t=5.80s: Spitting giant tongue
            ("shared/sfx/ding.mp3", 9100, 0.75),                # t=9.10s: Speed gym treadmills
            ("shared/sfx/whoosh.mp3", 12300, 0.60),             # t=12.30s: Slide across lava
            ("shared/sfx/vine_boom.mp3", 15340, 0.85),          # t=15.34s: Endcard slam
            ("shared/sfx/ding.mp3", 16800, 0.75),               # t=16.80s: Link in bio
        ]
    },
    "v20": {
        "duration": 16.70,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook opener
            ("shared/sfx/whoosh.mp3", 2100, 0.50),              # t=2.10s: Zero reach
            ("shared/sfx/punch.mp3", 3800, 0.65),               # t=3.80s: Can't clear jump
            ("shared/sfx/ding.mp3", 5500, 0.75),                # t=5.50s: x99 Hacker gym
            ("shared/sfx/pop.mp3", 7200, 0.60),                 # t=7.20s: Thousands of studs
            ("shared/sfx/whoosh.mp3", 9200, 0.60),              # t=9.20s: Soar over lava
            ("shared/sfx/hitmarker.mp3", 11200, 0.70),          # t=11.20s: Stage 8 100 wins
            ("shared/sfx/vine_boom.mp3", 14160, 0.85),          # t=14.16s: Endcard slam
            ("shared/sfx/ding.mp3", 15500, 0.75),               # t=15.50s: Link in bio
        ]
    },
    "v21": {
        "duration": 18.61,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Stop grinding!
            ("shared/sfx/whoosh.mp3", 2000, 0.50),              # t=2.00s: 3 secret codes
            ("shared/sfx/ding.mp3", 5200, 0.75),                # t=5.20s: WELCOME1 5k
            ("shared/sfx/pop.mp3", 8300, 0.65),                 # t=8.30s: BONUS500 10k
            ("shared/sfx/ding.mp3", 11500, 0.75),               # t=11.50s: FREEBOOST 2x
            ("shared/sfx/whoosh.mp3", 13800, 0.60),             # t=13.80s: Bridge entire maps
            ("shared/sfx/vine_boom.mp3", 15760, 0.85),          # t=15.76s: Endcard slam
            ("shared/sfx/ding.mp3", 17200, 0.75),               # t=17.20s: Link in bio
        ]
    }
}

def build_all_sfx():
    os.makedirs("temp/tongue_escape", exist_ok=True)
    for key, cfg in SFX_CONFIG.items():
        out_sfx = f"temp/tongue_escape/sfx_track_{key}.wav"
        events = cfg["events"]
        dur = cfg["duration"]
        
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
            "-t", f"{dur:.2f}",
            "-ar", "48000",
            "-ac", "2",
            out_sfx
        ]
        
        print(f"Generating SFX track for {key}: {out_sfx} ({dur:.2f}s)...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error creating SFX for {key}:")
            print(res.stderr[-500:])
        else:
            print(f"--> Generated {out_sfx} ({os.path.getsize(out_sfx)} bytes)")

if __name__ == "__main__":
    build_all_sfx()
