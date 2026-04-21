import speech_recognition as sr
import sys

def record_audio(output_path, duration=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening for {duration} seconds...")
        audio = r.listen(source, phrase_time_limit=duration)
        with open(output_path, "wb") as f:
            f.write(audio.get_wav_data())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        record_audio(sys.argv[1])
    else:
        record_audio("input.wav")
