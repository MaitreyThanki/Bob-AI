#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$SCRIPT_DIR/bobenv/bin/python"

echo "======================================"
echo "🛡️  BOB WAKE-WORD ACTIVE ('Hey Bob')"
echo "======================================"

while true
do
    # Listen for 2 seconds
    arecord -d 2 -f cd "$SCRIPT_DIR/wake.wav" 2>/dev/null
    
    # Check if 'Bob' or 'Hey' was said
    if "$PYTHON" "$SCRIPT_DIR/bob_wake.py" "$SCRIPT_DIR/wake.wav" > /dev/null; then
        echo "🔔 Wake word detected!"
        
        # Give a small beep or visual cue
        echo -e "\a" 
        
        # Now listen for the actual command for 5 seconds
        echo "BOB: Listening for your command... 🎤"
        arecord -d 5 -f cd "$SCRIPT_DIR/input.wav" 2>/dev/null
        
        # Transcribe
        echo "BOB: Processing... 🧠"
        input=$("$PYTHON" "$SCRIPT_DIR/bob_hear.py" "$SCRIPT_DIR/input.wav")
        
        if [[ "$input" == Error* ]]; then
            echo "BOB: Sorry, I didn't catch that."
        else
            echo "You: $input"
            echo "BOB: Thinking... 🤔"
            
            # Get response from agent
            response=$("$PYTHON" "$SCRIPT_DIR/bob_agent.py" "$input")
            
            echo "------------------------------"
            echo "BOB: $response"
            echo "------------------------------"
            
            # Speak the response
            "$PYTHON" "$SCRIPT_DIR/bob_speak.py" "$response"
        fi
        
        echo "🛡️  BOB: Returning to wake-word mode..."
    fi
done
