# Project Overview: BOB AI Assistant

BOB is a custom-built, local AI executive assistant designed to run directly in the Linux terminal. It combines the reasoning power of **Ollama (llama3)** with practical system tools and voice capabilities.

### Technologies & Architecture
- **Core Logic:** Python-based agent (`bob_agent.py`) using a "Tool Controller" architecture. Now supports both subprocess CLI and HTTP API for Ollama connectivity.
- **Frontend:** 
  - **CLI:** Interactive Bash wrapper (`bob.sh`) and listener (`bob_listen.sh`).
  - **Web:** Open WebUI integrated via Docker.
- **AI Engine:** Ollama running `llama3` locally.
- **API Bridge:** FastAPI-based `bob_api.py` providing an OpenAI-compatible endpoint.
- **Voice Stack:** `SpeechRecognition` (Google API) for STT and `pyttsx3` for TTS.
- **Data Persistence:** A simple, AI-managed `memory.txt` file for long-term user context.

## Building and Running

### Prerequisites
- **Ollama:** Must be installed and running with the `llama3` model (`ollama run llama3`).
- **System Tools:** `arecord` (part of `alsa-utils`) and `portaudio-devel`.
- **Docker:** Required for Web UI deployment.
- **Environment:** A Python virtual environment located at `./bobenv/`.

### Commands
- **Start Interactive Session:** `./bob.sh`
- **Start Hands-Free Mode:** `./bob_listen.sh`
- **Start Docker Web UI:** `sudo docker compose up -d`
- **Dependencies:** `source bobenv/bin/activate && pip install -r requirements.txt`

## Development Conventions

### Memory Management
- BOB automatically extracts facts from conversations and saves them to `memory.txt`.
- Memory is injected into the AI as `[SYSTEM]` level "USER PROTOCOLS" to ensure strict compliance (e.g., using preferred titles like "Sir Maitrey").

### Tool Integration
- **Autonomous Reasoning:** The agent uses a two-step process:
  1. **Tool Selection:** AI evaluates the user input to decide if a tool (READ, WRITE, LIST, WEATHER, NEWS, SYSTEM) is needed.
  2. **Final Response:** AI generates a plain-text response based on the tool's output and user memory.
- **Formatting:** Responses are strictly plain text (no Markdown/Stars) for optimal terminal readability.

### Voice Protocol
- **Wake-Word:** BOB listens for "Hey Bob" or "Bob" in 2-second increments before activating a full 5-second command recording.
- **Safe Speech:** `bob_speak.py` uses a hard exit (`os._exit`) to bypass known GIL conflicts in Python voice libraries on Linux.
