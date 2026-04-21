#!/bin/bash

echo "=============================="
echo "🤖 BOB AI ASSISTANT READY"
echo "=============================="

while true
do
    read -p "You: " input

    # Exit
    if [[ "$input" == "exit" ]]; then
        echo "BOB: Goodbye 👋"
        break
    fi

    # Empty input skip
    if [[ -z "$input" ]]; then
        continue
    fi

    # -------------------------
    # 📂 SYSTEM COMMANDS
    # -------------------------

    if [[ "$input" == *"downloads"* ]]; then
        xdg-open ~/Downloads &
        echo "BOB: Opening Downloads 📂"
        continue
    fi

    if [[ "$input" == *"documents"* ]]; then
        xdg-open ~/Documents &
        echo "BOB: Opening Documents 📂"
        continue
    fi

    if [[ "$input" == *"desktop"* ]]; then
        xdg-open ~/Desktop &
        echo "BOB: Opening Desktop 📂"
        continue
    fi

    if [[ "$input" == "clear" ]]; then
        clear
        continue
    fi

    # -------------------------
    # 🎤 VOICE INPUT COMMAND
    # -------------------------
    if [[ "$input" == "voice" ]]; then
        echo "BOB: Listening... 🎤"
        "$SCRIPT_DIR/bobenv/bin/python" "$SCRIPT_DIR/bob_record.py" "$SCRIPT_DIR/input.wav"
        echo "BOB: Processing speech... 🧠"
        input=$("$SCRIPT_DIR/bobenv/bin/python" "$SCRIPT_DIR/bob_hear.py" "$SCRIPT_DIR/input.wav")
        
        if [[ "$input" == Error* ]]; then
            echo "BOB: $input"
            continue
        fi
        echo "You (Voice): $input"
    fi

    # -------------------------
    # 🤖 AI RESPONSE (PYTHON AGENT)
    # -------------------------

    echo "BOB: Thinking... 🤔"

    # Use the virtual environment python and full path to the agent
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    response=$("$SCRIPT_DIR/bobenv/bin/python" "$SCRIPT_DIR/bob_agent.py" "$input")

    echo "------------------------------"
    echo "BOB: $response"
    echo "------------------------------"

    # 🔊 VOICE OUTPUT
    "$SCRIPT_DIR/bobenv/bin/python" "$SCRIPT_DIR/bob_speak.py" "$response" &

done
