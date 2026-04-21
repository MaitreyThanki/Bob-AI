import speech_recognition as sr
import sys
import os

def transcribe_audio(file_path):
    r = sr.Recognizer()
    if not os.path.exists(file_path):
        return "Error: Audio file not found."
    
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    
    try:
        # Using Google Speech Recognition (free, no API key required for small use)
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio."
    except sr.RequestError as e:
        return f"Error: Could not request results; {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(transcribe_audio(sys.argv[1]))
    else:
        print("Usage: python bob_hear.py <path_to_wav>")
