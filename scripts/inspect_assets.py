import os
import subprocess
import json

def get_clip_info(filepath):
    cmd = ['ffmpeg', '-i', filepath]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors='ignore')
    out = res.stderr
    
    dur = 'unknown'
    seconds = 0.0
    for line in out.split('\n'):
        if 'Duration:' in line:
            dur = line.split('Duration:')[1].split(',')[0].strip()
            try:
                h, m, s = dur.split(':')
                seconds = float(h)*3600 + float(m)*60 + float(s)
            except Exception:
                pass
            break
            
    res_str = 'unknown'
    has_audio = 'Audio:' in out
    fps = 'unknown'
    for line in out.split('\n'):
        if 'Stream #' in line and 'Video:' in line:
            parts = line.split(',')
            for pt in parts:
                pt_strip = pt.strip()
                if 'fps' in pt_strip:
                    fps = pt_strip.split(' ')[0]
                if 'x' in pt_strip:
                    chunk = pt_strip.split(' ')[0]
                    if any(c.isdigit() for c in chunk) and 'x' in chunk:
                        res_str = chunk
            break
            
    return {
        'name': os.path.basename(filepath),
        'duration': dur,
        'seconds': round(seconds, 2),
        'resolution': res_str,
        'has_audio': has_audio,
        'fps': fps,
        'size_mb': round(os.path.getsize(filepath) / (1024 * 1024), 2)
    }

def main():
    os.makedirs('scripts', exist_ok=True)
    assets = [os.path.join('assets', f) for f in os.listdir('assets') if f.endswith('.mp4')]
    assets.sort()
    
    inventory = [get_clip_info(f) for f in assets]
    
    with open('assets_inventory.json', 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)
        
    print(f"Total clips analyzed: {len(inventory)}")
    for item in inventory:
        print(f"{item['name']:<16} | Dur: {item['duration']} ({item['seconds']}s) | Res: {item['resolution']} | Audio: {item['has_audio']} | {item['size_mb']}MB")

if __name__ == '__main__':
    main()
