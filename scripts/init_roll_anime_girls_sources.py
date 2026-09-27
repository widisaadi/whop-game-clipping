import urllib.request
import os
import shutil

DOC_URL = "https://docs.google.com/document/d/1RRD6Jmnc9YQBqprv3ipjZpt3c5hDmVAzh_-K8fZnKoM"
DOC_HTML_EXPORT = f"{DOC_URL}/export?format=html"
DOC_TXT_EXPORT = f"{DOC_URL}/export?format=txt"

source_dir = "campaigns/roll_anime_girls/guide/source"
os.makedirs(source_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Save HTML export
req = urllib.request.Request(DOC_HTML_EXPORT, headers=headers)
html_data = urllib.request.urlopen(req).read()
with open(os.path.join(source_dir, "roll_anime_girls_guide.html"), "wb") as f:
    f.write(html_data)

# Save TXT export
req = urllib.request.Request(DOC_TXT_EXPORT, headers=headers)
txt_data = urllib.request.urlopen(req).read()
with open(os.path.join(source_dir, "roll_anime_girls_guide.txt"), "wb") as f:
    f.write(txt_data)

print("Saved raw source files to guide/source/")

# Download game icon
branding_dir = "campaigns/roll_anime_girls/assets/branding"
os.makedirs(branding_dir, exist_ok=True)
icon_url = "https://tr.rbxcdn.com/180DAY-20310640a29818b5bdf390393c371a37/512/512/Image/Png/noFilter"
req = urllib.request.Request(icon_url, headers=headers)
icon_data = urllib.request.urlopen(req).read()

icon_path = os.path.join(branding_dir, "roll_anime_girls_icon_512.png")
icon_000_path = os.path.join(branding_dir, "000.png")
with open(icon_path, "wb") as f:
    f.write(icon_data)
with open(icon_000_path, "wb") as f:
    f.write(icon_data)

print(f"Downloaded game icon to {icon_path} and {icon_000_path} ({len(icon_data)} bytes)")
