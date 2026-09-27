import urllib.request
import os
import sys
import time

content_files = [
    ("01_01_gameplay.mp4", "1GVJwheW9cPvbn1w66Q03a4foLQN_dcb-"),
    ("02_02_black_holes.mp4", "1NBlUeWIrHfT3Gwlgj_eLcF1TeH6A4VV1"),
    ("03_03_more_gameplay.mp4", "1c6vb3xeAOXCsCjZsa86f4o3C6qjmcDBr"),
    ("04_04_even_more_gameplay.mp4", "1T6QKt2-oJ6X1JB8eMfFVNtRKFR8sxSgj"),
    ("05_05_the_black_hole_effect.mp4", "1cALKgKaQtu3AGv_1qr3_nmjCDxj-jSV8"),
    ("06_2026-08-13_20-46-03.mp4", "1Bbq16ZlzXGZj40wzBptFNBi2toFVR_pa"),
    ("07_2026-08-14_10-16-18.mp4", "13YOoN_DQM7UyWKTsTNWy-AucGg8qNyQS"),
    ("08_2026-08-14_10-20-26.mp4", "1uW0NCg98BjkZa-msDNhiZXSSsDXhDLyD"),
    ("09_2026-08-14_10-20-54.mp4", "1S37fXz23E6pWPdBMyrchIFbrvhhZqGF1"),
    ("10_2026-08-14_10-21-20.mp4", "1oStbq-JE8M1uPALjf8E2BsWe8BWQ7dIF"),
    ("11_2026-08-14_12-55-34.mp4", "1Eh78xIZo2Vx029vkWturF8sXjbHia8DL"),
    ("12_2026-08-14_12-59-38.mp4", "1WP8FqWFpXaXz7nPgYvO7h2AAXFf6hO9C"),
    ("13_2026-08-14_13-05-27.mp4", "1j_LWKEQVEDtO0WMvZT8XV78cntpHgvHH"),
    ("14_2026-08-14_14-08-25.mp4", "1bFcvlsnELkjfQDOy1V3LNsnlrYHxlWE-"),
    ("15_2026-08-14_15-50-35.mp4", "1VjvwVxmsoMCS0w3DGVq__E-CfTXeUBQm")
]

ref_files = [
    ("ASMR_3s_build.mp4", "19wx094vNfBFwc2juhmuPZNPh_TkB9-Ii"),
    ("ASMR_BlackHole.mp4", "1117qNr5Miapgv8AQPvhTNpEpPZh8fzbi"),
    ("ASMR_BrokenChain.mp4", "13x0V6KS2-g9NJd8USGKiCpucUzr0_Bfu"),
    ("ASMR_Bubbles.mp4", "1fWrD62oTQ6huax-LgSHIkLUKBgefeyK8"),
    ("ASMR_Lava_topple.mp4", "132EhAydfQMSnQPejq2B4bDbGFeWFdJGD"),
    ("ASMR_Lvl1_vs_Lvl3_2.mp4", "1yW0P4yZbQiRiMgiMaDMrJr9PzuJptMdm"),
    ("ASMR_Lvl1_vs_Lvl3_3.mp4", "1Aqom4SHpBFQ6QRpy9C17Xwqu5S-jzczN"),
    ("ASMR_Lvl1_vs_Lvl3.mp4", "16tas-xl61TGnBB5RbvF9KPVlikMKVRW_"),
    ("ASMR_Lvl1_vs_Lvl999.mp4", "1efWHFZSGNCXEz0L3Nnbvplq7BCrM4vBf"),
    ("ASMR_Shop.mp4", "1uyvDLNFh8651HdAKj-rXijol7III-w0l"),
    ("ASMR_Short_Chain.mp4", "12G1JNyT1qEoEmu_-t2VfWjNZvOTf73Vx"),
    ("ASMR_Sounds_Showcase.mp4", "1qQk7FItkLZhrwoDJl0LOeC2yY1sy4oTO"),
    ("ASMR_Spiral.mp4", "1tGsBaeY11SQTDPt8Gx5Y6BuV41A_7IdD"),
    ("ASMR_Toilet.mp4", "1DjhoKGjs1xXXs-ZlMr2-B9ySlotWBL8N"),
    ("ASMR_Topple_Crunch.mp4", "1JuG1_nkNUrS98ccP-8MrRB68oykq8G9c")
]

def download_file(name, fid, target_dir):
    target_path = os.path.join(target_dir, name)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
        print(f"[SKIP] {name} already exists ({os.path.getsize(target_path) / (1024*1024):.2f} MB)", flush=True)
        return True

    urls_to_try = [
        f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
        f"https://drive.google.com/uc?export=download&id={fid}&confirm=t"
    ]

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                # check if response is HTML (virus scan or error)
                ct = resp.headers.get("Content-Type", "")
                if "text/html" in ct:
                    content = resp.read()
                    import re
                    match = re.search(r'confirm=([a-zA-Z0-9_-]+)', content.decode("utf-8", errors="ignore"))
                    if match:
                        confirm_token = match.group(1)
                        url_confirm = f"https://drive.google.com/uc?export=download&id={fid}&confirm={confirm_token}"
                        req2 = urllib.request.Request(url_confirm, headers=headers)
                        with urllib.request.urlopen(req2, timeout=60) as resp2:
                            with open(target_path, "wb") as f:
                                while True:
                                    chunk = resp2.read(1024*1024)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            print(f"[DONE] {name} downloaded via confirm token ({os.path.getsize(target_path) / (1024*1024):.2f} MB)", flush=True)
                            return True
                    continue
                
                with open(target_path, "wb") as f:
                    while True:
                        chunk = resp.read(1024*1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"[DONE] {name} downloaded ({os.path.getsize(target_path) / (1024*1024):.2f} MB)", flush=True)
                return True
        except Exception as e:
            print(f"[RETRY] {name} failed with {url}: {e}", flush=True)
            time.sleep(1)

    print(f"[FAILED] {name} could not be downloaded", flush=True)
    return False

def main():
    clips_dir = "campaigns/asmr_dominoes/assets/clips"
    refs_dir = "campaigns/asmr_dominoes/assets/references"
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(refs_dir, exist_ok=True)

    print("=== Downloading Raw Gameplay Clips (01 - Content) ===", flush=True)
    for name, fid in content_files:
        download_file(name, fid, clips_dir)

    print("\n=== Downloading Reference Videos (02 - References) ===", flush=True)
    for name, fid in ref_files:
        download_file(name, fid, refs_dir)

    print("\nAll downloads completed!", flush=True)

if __name__ == "__main__":
    main()
