import subprocess
import os

SFX_CONFIGS = {
    "v12": {
        "duration": 19.50,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
            ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
            ("shared/sfx/pop.mp3", 2800, 0.60),                 # t=2.80s: Massive highway bridge pop
            ("shared/sfx/whoosh.mp3", 5400, 0.40),              # t=5.40s: Running over bridge
            ("shared/sfx/ding.mp3", 7800, 0.75),                # t=7.80s: x99 treadmill / crazy studs ding
            ("shared/sfx/bass_drop.mp3", 10300, 0.70),          # t=10.30s: Raging lava chasms bass drop
            ("shared/sfx/hitmarker.mp3", 12100, 0.65),          # t=12.10s: Stage 8 clear hitmarker
            ("shared/sfx/punch.mp3", 14100, 0.80),              # t=14.10s: Leaderboards flex punch
            ("shared/sfx/vine_boom.mp3", 15600, 0.85),          # t=15.60s: Endcard slam!
            ("shared/sfx/ding.mp3", 17500, 0.70),               # t=17.50s: Link in bio chime
        ]
    },
    "v13": {
        "duration": 19.70,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
            ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
            ("shared/sfx/pop.mp3", 2900, 0.60),                 # t=2.90s: Spit giant tongue pop
            ("shared/sfx/whoosh.mp3", 5600, 0.40),              # t=5.60s: Bridge gap whoosh
            ("shared/sfx/ding.mp3", 8000, 0.75),                # t=8.00s: High speed treadmills ding
            ("shared/sfx/bass_drop.mp3", 10500, 0.70),          # t=10.50s: Brutal moving lava bass drop
            ("shared/sfx/hitmarker.mp3", 12300, 0.65),          # t=12.30s: Flex Stage 8 hitmarker
            ("shared/sfx/punch.mp3", 14300, 0.80),              # t=14.30s: Global leaderboards punch
            ("shared/sfx/vine_boom.mp3", 15800, 0.85),          # t=15.80s: Endcard slam!
            ("shared/sfx/ding.mp3", 17700, 0.70),               # t=17.70s: Link in bio chime
        ]
    },
    "v14": {
        "duration": 19.50,
        "events": [
            ("shared/sfx/metal_gear_alert.mp3", 0, 0.85),       # t=0.00s: Hook alert
            ("shared/sfx/whoosh.mp3", 1300, 0.45),              # t=1.30s: Cut from avatar to gameplay
            ("shared/sfx/pop.mp3", 2800, 0.60),                 # t=2.80s: Stretch tongue pop
            ("shared/sfx/whoosh.mp3", 5500, 0.40),              # t=5.50s: Across map whoosh
            ("shared/sfx/ding.mp3", 7800, 0.75),                # t=7.80s: Gym training multipliers ding
            ("shared/sfx/bass_drop.mp3", 10300, 0.70),          # t=10.30s: Deadly lava chasms bass drop
            ("shared/sfx/hitmarker.mp3", 12100, 0.65),          # t=12.10s: Race to top hitmarker
            ("shared/sfx/punch.mp3", 14100, 0.80),              # t=14.10s: Leaderboards flex punch
            ("shared/sfx/vine_boom.mp3", 15600, 0.85),          # t=15.60s: Endcard slam!
            ("shared/sfx/ding.mp3", 17500, 0.70),               # t=17.50s: Link in bio chime
        ]
    }
}

def build_sfx(vid_key, config):
    os.makedirs("temp/tongue_escape", exist_ok=True)
    out_sfx = f"temp/tongue_escape/sfx_track_{vid_key}.wav"
    duration = config["duration"]
    events = config["events"]
    
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
        print(f"Error creating SFX track for {vid_key}:")
        print(res.stderr[-500:])
        return False
    print(f"--> Generated {out_sfx} ({os.path.getsize(out_sfx)} bytes)")
    return True

def main():
    for k, cfg in SFX_CONFIGS.items():
        build_sfx(k, cfg)

if __name__ == "__main__":
    main()
