import json
import re
from faster_whisper import WhisperModel

def main():
    audio_path = "temp/voiceover_v12_fast.wav"
    print(f"Loading faster-whisper on CPU for {audio_path}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, word_timestamps=True)

    words_data = []
    for s in segments:
        for w in s.words:
            raw_w = w.word.strip()
            clean_w = re.sub(r"[^\w\s\?!,'-]", "", raw_w).strip()
            if clean_w:
                words_data.append({
                    "word": clean_w,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3)
                })

    print(f"Extracted {len(words_data)} total words!")
    for idx, w in enumerate(words_data):
        print(f"[{idx+1:02d}] {w['start']:05.2f}s - {w['end']:05.2f}s : {w['word']}")

    with open("temp/v12_whisper_words.json", "w", encoding="utf-8") as f:
        json.dump(words_data, f, indent=2)
    print("Saved to temp/v12_whisper_words.json")

if __name__ == "__main__":
    main()
