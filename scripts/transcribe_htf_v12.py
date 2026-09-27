from faster_whisper import WhisperModel
import json
import os

audio_path = "temp/how_to_fisch/voiceover_htf_v12_fast.wav"
print(f"Loading faster-whisper on CPU for {audio_path}...")
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_path, word_timestamps=True)

words_data = []
for s in segments:
    for w in s.words:
        words_data.append({
            "word": w.word.strip(),
            "start": round(w.start, 3),
            "end": round(w.end, 3)
        })

print(f"Extracted {len(words_data)} total words!")
for idx, w in enumerate(words_data[:15]):
    print(f"[{idx+1:02d}] {w['start']:05.2f}s - {w['end']:05.2f}s : {w['word']}")
print("...")
for idx, w in enumerate(words_data[-10:]):
    print(f"[{len(words_data)-10+idx+1:02d}] {w['start']:05.2f}s - {w['end']:05.2f}s : {w['word']}")

out_file = "temp/how_to_fisch/whisper_words_htf_v12.json"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(words_data, f, indent=2)

print(f"Saved to {out_file}")
