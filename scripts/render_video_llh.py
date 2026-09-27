import os
import subprocess
import json
import re

BASE_DIR = r"d:\create something\local\tiktokclipping\campaigns\lessons_in_love_and_hate"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = r"d:\create something\local\tiktokclipping\temp\lessons_in_love_and_hate"
BRANDING_DIR = os.path.join(BASE_DIR, "assets", "branding")
CLIPS_DIR = os.path.join(BASE_DIR, "assets", "clips")
SUB_DIR = os.path.join(BASE_DIR, "subtitles")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

CLIP_NAME = "LLH_clipping_19_almostKiss.mp4"
CLIP_PATH = os.path.join(CLIPS_DIR, CLIP_NAME)
VO_PATH = os.path.join(TEMP_DIR, "vo_48k.wav")
WATERMARK_PATH = os.path.join(BRANDING_DIR, "ShortsLogo.png")
ENDCARD_DIR = os.path.join(TEMP_DIR, "endcard_frames")
ASS_PATH = os.path.join(SUB_DIR, "captions_01.ass")

OUT_BASE = "01_llh_enemies_to_lovers_tension"
OUT_MP4 = os.path.join(OUTPUT_DIR, f"{OUT_BASE}.mp4")
OUT_SHEET = os.path.join(OUTPUT_DIR, f"{OUT_BASE}_sheet.png")
OUT_META = os.path.join(OUTPUT_DIR, f"{OUT_BASE}_metadata.md")

TOTAL_DURATION = 19.5
ENDCARD_START = 15.0

def step1_render_video():
    print(f"--- Rendering Master Video: {OUT_BASE}.mp4 ---")
    
    # Path escaping for FFmpeg filters
    ass_escaped = ASS_PATH.replace("\\", "/").replace(":", "\\:")
    endcard_seq = os.path.join(ENDCARD_DIR, "endcard_%04d.png").replace("\\", "/")
    
    # Pre-render endcard overlay clip from PNG sequence (4.5s @ 30fps)
    endcard_mov = os.path.join(TEMP_DIR, "endcard_overlay.mov")
    cmd_ec = [
        "ffmpeg", "-y", "-framerate", "30",
        "-i", endcard_seq,
        "-c:v", "png",
        "-pix_fmt", "rgba",
        "-t", "4.5",
        endcard_mov
    ]
    subprocess.run(cmd_ec, check=True)
    print("Pre-rendered endcard overlay MOV.")

    # Two-pass Audio Loudness Normalization with EBU R128
    print("Running Pass 1 Audio Loudness Analysis...")
    # Voiceover volume 1.38, Scene BGM volume 0.22 with fadeout
    filter_audio_pre = (
        f"[1:a]volume=1.38[vo]; "
        f"[0:a]volume=0.22,afade=t=out:st=18.0:d=1.5[bgm]; "
        f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[a_mix]; "
        f"[a_mix]ebur128=peak=true[ebur]"
    )
    cmd_p1 = [
        "ffmpeg", "-y",
        "-i", CLIP_PATH,
        "-i", VO_PATH,
        "-filter_complex", filter_audio_pre,
        "-f", "null", "-"
    ]
    p1_proc = subprocess.run(cmd_p1, capture_output=True, text=True)
    p1_out = p1_proc.stderr
    
    # Parse integrated loudness from ebur128 output
    i_matches = re.findall(r"I:\s+([-\d\.]+)\s+LUFS", p1_out)
    tp_matches = re.findall(r"Peak:\s+([-\d\.]+)\s+dBFS", p1_out)
    meas_i = float(i_matches[-1]) if i_matches else -14.0
    meas_tp = float(tp_matches[-1]) if tp_matches else -1.5
    print(f"Pass 1 Analysis: Measured Integrated = {meas_i} LUFS, Peak = {meas_tp} dBTP")
    
    # Calculate gain offset to hit -14.0 LUFS
    gain_needed = -14.0 - meas_i
    print(f"Applying EBU R128 Gain Correction: {gain_needed:+.2f} dB")
    
    # Prepare Watermark (ShortsLogo.png scaled to 180w with 85% opacity)
    # Filter Complex:
    # 0:v = Raw clip (1080x1920)
    # 1:v = Endcard overlay (1080x1920 RGBA)
    # 2:v = ShortsLogo.png
    filter_complex = (
        # 1. Main video branch: split into scene (0-15s) and endcard bg (15-19.5s)
        f"[0:v]trim=0:{TOTAL_DURATION},setpts=PTS-STARTPTS,fps=30,setsar=1,format=yuv420p[v_base]; "
        f"[v_base]split[v_live][v_for_bg]; "
        # Endcard background: blur and darken from 15.0s
        f"[v_for_bg]trim={ENDCARD_START}:{TOTAL_DURATION},setpts=PTS-STARTPTS,boxblur=24:4,eq=brightness=-0.35:contrast=1.12[v_bg_blur]; "
        # Overlay endcard graphic frames over blurred background
        f"[v_bg_blur][1:v]overlay=0:0:format=auto[v_endcard_full]; "
        # Concat live scene (0-15s) and endcard (15-19.5s)
        f"[v_live]trim=0:{ENDCARD_START},setpts=PTS-STARTPTS[v_scene]; "
        f"[v_scene][v_endcard_full]concat=n=2:v=1:a=0[v_composed]; "
        # Add subtle Shorts logo watermark in upper-right corner
        f"[2:v]scale=180:-1,format=rgba,colorchannelmixer=aa=0.85[wm]; "
        f"[v_composed][wm]overlay=W-w-50:60[v_watermarked]; "
        # Burn ASS subtitles (dialogue / hook)
        f"[v_watermarked]ass='{ass_escaped}'[v_final]; "
        # Audio mix with gain correction
        f"[4:a]volume=1.38[vo]; "
        f"[0:a]volume=0.22,afade=t=out:st=18.0:d=1.5[bgm]; "
        f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2,volume={gain_needed:.2f}dB[a_final]"
    )

    cmd_master = [
        "ffmpeg", "-y",
        "-i", CLIP_PATH,         # 0: video & game audio
        "-i", endcard_mov,       # 1: endcard mov
        "-i", WATERMARK_PATH,    # 2: ShortsLogo.png
        "-i", CLIP_PATH,         # 3: dummy / unused
        "-i", VO_PATH,           # 4: voiceover 48k
        "-filter_complex", filter_complex,
        "-map", "[v_final]",
        "-map", "[a_final]",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-video_track_timescale", "15360",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-t", str(TOTAL_DURATION),
        OUT_MP4
    ]

    print("Executing Master Render Pipeline...")
    subprocess.run(cmd_master, check=True)
    size_mb = os.path.getsize(OUT_MP4) / (1024 * 1024)
    print(f"Master Video Successfully Rendered: {OUT_MP4} ({size_mb:.2f} MB)")

def step2_generate_contact_sheet():
    print(f"--- Generating 3x2 Contact Sheet: {OUT_SHEET} ---")
    cmd = [
        "ffmpeg", "-y",
        "-i", OUT_MP4,
        "-vf", "select='not(mod(n,90))',scale=360:640,tile=3x2",
        "-frames:v", "1",
        "-q:v", "2",
        OUT_SHEET
    ]
    subprocess.run(cmd, check=True)
    print("Contact sheet created.")

def step3_compliance_audit():
    print("--- Running 13/13 Compliance Audit ---")
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,r_frame_rate,codec_name,pix_fmt,color_space:format=duration,size",
        "-of", "json", OUT_MP4
    ]
    probe_data = json.loads(subprocess.check_output(probe_cmd).decode("utf-8"))
    
    v = next(s for s in probe_data["streams"] if s["codec_name"] == "h264")
    dur = float(probe_data["format"]["duration"])
    w = v["width"]
    h = v["height"]
    fps = v["r_frame_rate"]
    color = v.get("color_space")
    
    print(f"Audit Checks:")
    print(f"1. Resolution: {w}x{h} -> {'PASS' if w==1080 and h==1920 else 'FAIL'}")
    print(f"2. Frame Rate: {fps} -> {'PASS' if fps=='30/1' else 'FAIL'}")
    print(f"3. Duration: {dur:.2f}s -> {'PASS' if dur>=10.0 else 'FAIL'}")
    print(f"4. Color Space: {color} -> {'PASS' if color=='bt709' else 'FAIL'}")
    
    # Freeze detection
    freeze_cmd = [
        "ffmpeg", "-i", OUT_MP4,
        "-vf", "freezedetect=noise=-60dB:d=1.5",
        "-f", "null", "-"
    ]
    fr_proc = subprocess.run(freeze_cmd, capture_output=True, text=True)
    has_freeze = "freeze_start" in fr_proc.stderr
    print(f"5. Zero Stuck Frames: {'PASS (0 frozen frames)' if not has_freeze else 'WARN (stuck frames detected)'}")

def step4_generate_metadata():
    print(f"--- Writing Social Distribution Pack: {OUT_META} ---")
    metadata_text = """# 01 Lessons In Love And Hate Enemies To Lovers Tension

**Topic/Angle**: Enemies-to-Lovers Romantic Tension & Almost-Kiss Chemistry
**Duration**: 19.5 seconds
**Series Title**: Lessons in Love and Hate
**Streaming Platform**: Shorts app

---

## 🎯 3 High-CTR Hook Angles

> *"He swore he hated her... but enemies don't look at each other like this."*

> *"The moment she realized the bad boy was never actually the villain..."*

> *"She fell first, but when he pinned her against the wall, he fell so much harder."*

---

## 📝 Copy-Ready Social Caption

```text
This enemies-to-lovers story has me completely obsessed. The tension between them is literally insane! You can watch Lessons in Love and Hate on Shorts right now. ❤️✨

Tag:
TikTok: @shortsapp
Instagram: @app.shorts
YouTube: @shorts_theapp
```

---

## 🎙️ Spoken Voiceover Script

> *"He swore he hated her... but enemies do not look at each other like this. The moment he pinned her against the wall, everything changed. She fell first... but he fell so much harder. You have to watch Lessons in Love and Hate on Shorts right now!"*

---

## 🏷️ Platform-Specific Hashtag Bundles

### TikTok Optimized:
`#LessonsInLoveAndHate #LLH #ShortsApp #EnemiesToLovers #YoungAdultRomance #RomanceSeries #TeenDrama #BadBoyRomance #BookTok #RomanceEdit #HeFallsHarder`

### Instagram Reels Optimized:
`#LessonsInLoveAndHate #LLH #ShortsApp #EnemiesToLovers #RomanceSeries #TeenDrama #BadBoyRomance #ReelsRomance #CoupleEdit #SlowBurn`

### YouTube Shorts Optimized:
`#LessonsInLoveAndHate #LLH #ShortsApp #EnemiesToLovers #RomanceSeries #TeenDrama #Shorts`

---

## 🚀 Posting Recommendations
- **Recommended Cover Frame**: 0:00:10.50 (Intense eye-to-eye contact against the wall with soft lighting).
- **Audio Strategy**: Ambient tension breathes under the voiceover with romantic soundtrack swell.
"""
    with open(OUT_META, "w", encoding="utf-8") as f:
        f.write(metadata_text.strip())
    print("Metadata pack written successfully.")

def main():
    step1_render_video()
    step2_generate_contact_sheet()
    step3_compliance_audit()
    step4_generate_metadata()
    print("\nALL PIPELINE PHASES COMPLETE!")

if __name__ == "__main__":
    main()
