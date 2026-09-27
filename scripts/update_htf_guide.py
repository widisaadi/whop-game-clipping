with open("campaigns/how_to_fisch/guide/campaign_guide.md", "r", encoding="utf-8") as f:
    content = f.read()

target = "### 08. Way More Fun Than It Looks (`08_how_to_fisch_way_more_fun.mp4` - TERBARU)"
replacement = """### 08. Way More Fun Than It Looks (`08_how_to_fisch_way_more_fun.mp4`)
- **Tema:** *"This new Roblox game is actually way more fun than it looks!"* (Official Campaign Guide Hook)
- **Voiceover:** Callirrhoe (Sped up 1.20x — Fast-Paced Pacing)
- **Hook Khusus:** Menggunakan avatar shock anime zoom dari `shared/hooks/INTRO.mp4` (3.40 detik) + sound effect *Metal Gear Solid Alert* di detik 0.00s.
- **Durasi:** 29.0 detik | **Loudness:** -14.1 LUFS
- **File Video:** [`08_how_to_fisch_way_more_fun.mp4`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/08_how_to_fisch_way_more_fun.mp4)
- **Metadata SEO:** [`08_how_to_fisch_way_more_fun_metadata.md`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/08_how_to_fisch_way_more_fun_metadata.md)

### 12. Sun Fish Hunt (`12_how_to_fisch_sunfish_hunt.mp4`)
- **Tema:** *"This is the most unhinged fishing game in Roblox!"*
- **Voiceover:** Gemini TTS Puck (+4 dB Boost)
- **Durasi:** 19.50 detik | **Loudness:** -14.0 LUFS
- **Living Endcard:** CTA `SEARCH ON ROBLOX` di Y=1180, official crowned boss icon
- **File Video:** [`12_how_to_fisch_sunfish_hunt.mp4`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/12_how_to_fisch_sunfish_hunt.mp4)
- **Metadata SEO:** [`12_how_to_fisch_sunfish_hunt_metadata.md`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/12_how_to_fisch_sunfish_hunt_metadata.md)

### 13. Piranha Boss Raid (`13_how_to_fisch_piranha_boss_raid.mp4` - TERBARU)
- **Tema:** *"In Roblox, fishing will literally get you attacked!"*
- **Voiceover:** Gemini TTS Puck (+4 dB Boost, breathless verbatim)
- **Visuals:** 1:1 sharp centered square on 9:16 blurred backdrop (Iron Rod cast -> dry land mutant Piranha Boss assault -> Granny shotgun upgrade -> Pistol iron sights shootout -> motorboat ocean raid)
- **Durasi:** 19.60 detik | **Loudness:** -14.2 LUFS (-1.5 dBTP, 48 kHz stereo)
- **Living Endcard:** CTA `SEARCH ON ROBLOX` di Y=1180, official crowned boss icon, `HOW TO FISCH` title
- **File Video:** [`13_how_to_fisch_piranha_boss_raid.mp4`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/13_how_to_fisch_piranha_boss_raid.mp4)
- **Metadata SEO:** [`13_how_to_fisch_piranha_boss_raid_metadata.md`](file:///d:/create%20something/Web%20App/bloxclip/campaigns/how_to_fisch/output/13_how_to_fisch_piranha_boss_raid_metadata.md)"""

idx = content.find(target)
if idx != -1:
    end_idx = content.find("---", idx)
    new_content = content[:idx] + replacement + "\n\n\n" + content[end_idx:]
    with open("campaigns/how_to_fisch/guide/campaign_guide.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Campaign guide updated successfully!")
else:
    print("Target not found")
