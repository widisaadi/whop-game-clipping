import os
import json
import subprocess

def build_sfx_for_video(v_conf):
    camp = v_conf["campaign"]
    vid_id = v_conf["vid_id"]
    
    out_dir = os.path.join("temp", camp)
    os.makedirs(out_dir, exist_ok=True)
    out_wav = os.path.join(out_dir, f"sfx_track_{vid_id}.wav")
    
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 100000:
        return out_wav
        
    events = [
        ("assets/sfx/metal_gear_alert.mp3", 0.00, 0.95),  # t=0.00s: Metal Gear Alert on INTRO.mp4 avatar shock
        ("assets/sfx/whoosh.mp3", 1.40, 0.85),            # t=1.40s: Cut to gameplay teaser
        ("assets/sfx/bass_drop.mp3", 1.60, 0.80),
        ("assets/sfx/whoosh.mp3", 3.80, 0.85),
        ("assets/sfx/pop.mp3", 4.50, 0.70),
        ("assets/sfx/whoosh.mp3", 7.50, 0.85),
        ("assets/sfx/ding.mp3", 10.50, 0.85),
        ("assets/sfx/ding.mp3", 14.50, 0.80),
        ("assets/sfx/vine_boom.mp3", 15.80, 0.90),        # t=15.80s: Peak Superpower Tease
        ("assets/sfx/whoosh.mp3", 17.50, 0.85),
        ("assets/sfx/bass_drop.mp3", 18.00, 0.90),
        ("assets/sfx/whoosh.mp3", 19.50, 0.85),           # t=19.50s: Living Endcard entrance
        ("assets/sfx/ding.mp3", 20.00, 0.85)              # t=20.00s: Endcard pop chime
    ]
    
    # Custom ASMR domino stems if in asmr_dominoes
    if camp == "asmr_dominoes":
        events.append(("temp/asmr_dominoes/sfx/bubble_pop_stem.wav", 8.20, 0.75))
        events.append(("temp/asmr_dominoes/sfx/domino_crunch_stem.wav", 12.50, 0.90))
        
    inputs = []
    filter_parts = []
    for i, (fpath, delay_sec, vol) in enumerate(events):
        delay_ms = int(delay_sec * 1000)
        inputs.extend(["-i", fpath])
        filter_parts.append(
            f"[{i}:a]volume={vol:.2f},adelay={delay_ms}|{delay_ms},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[s{i}];"
        )
        
    mix_ins = "".join([f"[s{i}]" for i in range(len(events))])
    mix_filter = f"{mix_ins}amix=inputs={len(events)}:duration=longest:normalize=0:dropout_transition=0,volume=1.0[outa]"
    full_filter = "".join(filter_parts) + mix_filter
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[outa]",
        "-t", "24.50",
        out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[{vid_id}] SFX Track built: {out_wav}")
    return out_wav

def main():
    with open("temp/batch_10_config.json", "r", encoding="utf-8") as f:
        configs = json.load(f)
    for conf in configs:
        build_sfx_for_video(conf)

if __name__ == "__main__":
    main()
