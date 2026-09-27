import subprocess, os

clips = [
    '10_Clip 10.mp4', '11_Clip 11.mp4', '04_Clip 4.mp4', 
    '06_Clip 6.mp4', '07_Clip 7.mp4', '08_Clip 8.mp4', '09_Clip 9.mp4',
    '03_Clip 3 (1)_1eeXRC8.mp4', '05_Clip 5_1J29fm0.mp4'
]
os.makedirs('temp/inspect', exist_ok=True)
for c in clips:
    path = f'campaigns/tongue_escape/assets/clips/{c}'
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    dur = float(subprocess.check_output(cmd, shell=True).decode().strip())
    print(f'{c}: duration {dur:.2f}s')
    out1 = f'temp/inspect/{c[:2]}_f1.jpg'
    subprocess.run(f'ffmpeg -y -ss 2.0 -i "{path}" -vframes 1 -q:v 3 "{out1}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out2 = f'temp/inspect/{c[:2]}_f2.jpg'
    subprocess.run(f'ffmpeg -y -ss {dur/2:.1f} -i "{path}" -vframes 1 -q:v 3 "{out2}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Done extracting preview frames")
