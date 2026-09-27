from faster_whisper import WhisperModel
import json

audio_path = "temp/steal_a_seed/voiceover_sas_04_fast.wav"
print(f"Transcribing {audio_path}...")
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

print(f"Total words: {len(words_data)}")
for idx, w in enumerate(words_data):
    print(f"{idx+1:02d} | {w['start']:05.2f}s - {w['end']:05.2f}s : {w['word']}")

with open("temp/steal_a_seed/whisper_words_sas_04.json", "w", encoding="utf-8") as f:
    json.dump(words_data, f, indent=2)
print("Saved to temp/steal_a_seed/whisper_words_sas_04.json")
