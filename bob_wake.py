import speech_recognition as sr
import sys
import os

def check_for_wake_word(file_path):
    r = sr.Recognizer()
    if not os.path.exists(file_path):
        return False
    
    try:
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio).lower()
        print(f"Heard: {text}") # Debug info
        if "bob" in text or "hey" in text:
            return True
    except:
        pass
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if check_for_wake_word(sys.argv[1]):
            sys.exit(0) # Found
        else:
            sys.exit(1) # Not found
