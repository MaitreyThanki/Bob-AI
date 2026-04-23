import sys
import subprocess
import platform
import os

def record_audio(output_path, duration=5):
    # Try arecord on Linux first to avoid pyaudio dependency issues
    if platform.system() == "Linux":
        try:
            # -d: duration, -f: format, -r: rate, -c: channels, -t: type
            subprocess.run([
                "arecord",
                "-d", str(duration),
                "-f", "S16_LE",
                "-r", "16000",
                "-c", "1",
                "-t", "wav",
                output_path
            ], check=True, stderr=subprocess.DEVNULL)
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Fallback to SpeechRecognition (requires pyaudio)
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        # Microphone requires pyaudio
        with sr.Microphone() as source:
            print(f"Listening for {duration} seconds...")
            audio = r.listen(source, phrase_time_limit=duration)
            with open(output_path, "wb") as f:
                f.write(audio.get_wav_data())
    except Exception as e:
        print(f"Error: Could not record audio. {e}")
        if platform.system() == "Linux":
            print("Note: On Linux, ensure 'alsa-utils' is installed for arecord.")

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "input.wav"
    dur = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    record_audio(output, dur)
