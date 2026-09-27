import subprocess
import os

def main():
    os.makedirs("temp/test", exist_ok=True)
    out_seg = "temp/test/blurred_endcard_seg.mp4"
    out_frame = "temp/test/blurred_endcard_frame.jpg"
    
    # 1. Generate 5.3s video segment with blurred gameplay + endcard_overlay
    cmd = [
        "ffmpeg", "-y",
        "-ss", "3.5",
        "-t", "5.3",
        "-i", "assets/31_Clip 31.mp4",
        "-i", "assets/endcard_overlay.png",
        "-filter_complex",
        "[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,boxblur=24:6,eq=brightness=-0.3:contrast=1.1[bg];"
        "[bg][1:v]overlay=0:0[v]",
        "-map", "[v]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-an",
        out_seg
    ]
    subprocess.run(cmd, check=True)
    
    # 2. Extract a frame to check
    cmd_frame = [
        "ffmpeg", "-y",
        "-ss", "2.0",
        "-i", out_seg,
        "-vframes", "1",
        "-q:v", "2",
        out_frame
    ]
    subprocess.run(cmd_frame, check=True)
    print(f"Generated frame: {out_frame}")

if __name__ == "__main__":
    main()
