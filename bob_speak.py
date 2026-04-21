import pyttsx3
import sys
import os

def speak(text):
    try:
        # Initialize the engine
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 150)
        
        # Speak
        engine.say(text)
        engine.runAndWait()
        
        # Cleanly stop the engine to prevent GIL errors
        engine.stop()
        
    except Exception as e:
        # If voice fails, don't crash the whole agent
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        # If text is extremely long, trim it for speech to avoid hangs
        speak(text[:500])
    
    # Force exit to prevent the finalize/TSS error
    os._exit(0)
