import subprocess, os

os.makedirs("temp/inspect_v10", exist_ok=True)

# 04_Clip 4.mp4: dump frames every 1.5s
subprocess.run('ffmpeg -y -i "campaigns/tongue_escape/assets/clips/04_Clip 4.mp4" -vf "fps=1" "temp/inspect_v10/c4_%02d.jpg"', shell=True)

# 03_Clip 3 (2).mp4: dump frames every 1s
subprocess.run('ffmpeg -y -i "campaigns/tongue_escape/assets/clips/03_Clip 3 (2).mp4" -vf "fps=1" "temp/inspect_v10/c3_%02d.jpg"', shell=True)

# 10_Clip 10.mp4: dump frames every 2s
subprocess.run('ffmpeg -y -i "campaigns/tongue_escape/assets/clips/10_Clip 10.mp4" -vf "fps=0.5" "temp/inspect_v10/c10_%02d.jpg"', shell=True)

# 07_Clip 7.mp4: dump frames every 1.5s
subprocess.run('ffmpeg -y -i "campaigns/tongue_escape/assets/clips/07_Clip 7.mp4" -vf "fps=1" "temp/inspect_v10/c7_%02d.jpg"', shell=True)

print("Done extracting v10 frames")
