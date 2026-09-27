import asyncio
import edge_tts

TEXT = (
    "Think this is just another chill fishing game on Roblox? Think again! "
    "This is How to Fisch, where every catch has a mind of its own! "
    "Start by casting your rod, but instead of normal fish, you reel in floppy shrimp and goofy clams. "
    "Sell your loot to the lighthouse keeper to upgrade your gear and bait. "
    "Because out here, you have to survive against massive bosses like the Spider Crab! "
    "Sail to new islands, unlock weapons, and hunt down legendary sea monsters. "
    "Search How to Fisch on Roblox and play right now!"
)

VOICE = "en-US-ChristopherNeural"

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="+8%")
    submaker = edge_tts.SubMaker()
    
    with open("temp/voiceover.mp3", "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open("temp/voiceover.srt", "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())
        
    print("Voiceover and SRT generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
