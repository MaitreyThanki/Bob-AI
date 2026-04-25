# Project Overview: BOB AI Assistant (TUI)

BOB is a custom-built, local AI executive assistant designed to run directly in the Linux terminal. It uses a TUI (Textual User Interface) built with Python and `rich`.

### Technologies & Architecture
- **Core Logic:** Python-based agent (`bob_agent.py`) using a "Tool Controller" architecture.
- **Frontend:** 
  - **TUI:** Interactive Python script (`bob_tui.py`) using the `rich` library for stylized output.
  - **Shell:** Bash wrapper (`bob.sh`) for environment setup and execution.
- **AI Engine:** Ollama running `gemma4:e4b` locally (configurable via `BOB_MODEL`).
- **Voice Stack:** `SpeechRecognition` (Google API) for STT and `pyttsx3` for TTS.
- **Data Persistence:** AI-managed `memory.txt` file for long-term user context.

## Building and Running

### Prerequisites
- **Ollama:** Must be installed and running with the preferred model (`ollama pull gemma4:e4b`).
- **System Tools:** `arecord` (part of `alsa-utils`) and `portaudio-devel`.
- **Environment:** A Python virtual environment located at `./bobenv/`.

### Commands
- **Start Interactive Session:** `./bob.sh`
- **Dependencies:** `source bobenv/bin/activate && pip install -r requirements.txt`

## Development Conventions

### Memory Management
- BOB automatically extracts facts from conversations and saves them to `memory.txt`.
- Memory is injected as `[SYSTEM]` level "USER PROTOCOLS".

### Tool Integration
- **Autonomous Reasoning:** 
  1. **Tool Selection:** AI evaluates input to decide if a tool (LIST, READ, WRITE, WEATHER, NEWS, SYSTEM) is needed.
  2. **Final Response:** AI generates plain-text response based on tool output and memory.
- **Formatting:** Responses are rendered using Markdown via the `rich` library.

### Voice Protocol
- **Record:** `bob_record.py` handles 5-second audio captures.
- **Speak:** `bob_speak.py` uses a hard exit (`os._exit`) to bypass known GIL conflicts in Python voice libraries on Linux.
