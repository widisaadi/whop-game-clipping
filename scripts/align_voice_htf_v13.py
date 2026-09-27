import json
import whisper

def align():
    print("Loading whisper base model...")
    model = whisper.load_model("base")
    audio_path = "temp/how_to_fisch/voiceover_htf_v13_fast.wav"
    print(f"Transcribing {audio_path} with word-level timestamps...")
    result = model.transcribe(audio_path, word_timestamps=True)
    
    out_json = "temp/how_to_fisch/subtitles_htf_v13.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    
    print("\nWhisper Segments:")
    for s in result["segments"]:
        st = s["start"]
        en = s["end"]
        txt = s["text"].strip()
        print(f"[{st:5.2f}s - {en:5.2f}s] {txt}")

if __name__ == "__main__":
    align()
