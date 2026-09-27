import subprocess, os

clips2 = [
    '01_Clip 1 (1)_1lBAJk7.mp4', '02_Clip 2 (2).mp4', '03_Clip 3 (2).mp4',
    '05_Clip 5 (1).mp4', '07_Clip 7.mp4', '08_Clip 8.mp4'
]
for c in clips2:
    path = f'campaigns/tongue_escape/assets/clips/{c}'
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    try:
        dur = float(subprocess.check_output(cmd, shell=True).decode().strip())
        print(f'{c}: {dur:.2f}s')
        out1 = f'temp/inspect/{c[:4]}_sub1.jpg'
        subprocess.run(f'ffmpeg -y -ss 3.0 -i "{path}" -vframes 1 -q:v 3 "{out1}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out2 = f'temp/inspect/{c[:4]}_sub2.jpg'
        subprocess.run(f'ffmpeg -y -ss {dur*0.6:.1f} -i "{path}" -vframes 1 -q:v 3 "{out2}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f'Error {c}: {e}')
print("Done extracting clips2")
