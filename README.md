# BOB AI Assistant 🤖

BOB is a custom-built, local AI executive assistant designed to run directly in your terminal. It combines the reasoning power of **Ollama (llama3)** with practical system tools and voice capabilities.

## Features
- **Local AI:** Powered by Ollama (llama3), ensuring privacy and offline capability.
- **Tool Integration:** Can list files, read/write files, check weather, fetch news, and monitor system status.
- **Voice Support:** Speech-to-Text (STT) and Text-to-Speech (TTS) integration.
- **Memory:** Remembers user facts and preferences over time.
- **Cross-Platform:** Supports both Linux and Windows.

---

## Prerequisites

### 1. Ollama
Install Ollama and download the `llama3` model:
- **Download:** [ollama.com](https://ollama.com)
- **Run Model:** `ollama run llama3`

### 2. Python
Ensure you have Python 3.8+ installed.

---

## Installation

### Linux 🐧
1. **System Dependencies:**
   ```bash
   sudo apt update
   sudo apt install portaudio19-dev python3-pyaudio
   ```
2. **Setup Virtual Environment:**
   ```bash
   python3 -m venv bobenv
   source bobenv/bin/activate
   pip install -r requirements.txt
   ```
3. **Make Executable:**
   ```bash
   chmod +x bob.sh bob_listen.sh
   ```

### Windows 🪟
1. **Setup Environment:**
   ```powershell
   python -m venv bobenv
   .\bobenv\Scripts\activate
   pip install -r requirements.txt
   ```
   *Note: If `pyaudio` fails to install, you may need to download a pre-compiled wheel or install "Build Tools for Visual Studio".*

---

## Usage

### Interactive Mode
- **Linux:** `./bob.sh`
- **Windows:** `bob.bat`

Type your command or just say **"voice"** to trigger voice input.

### Hands-Free Mode (Linux Only)
To have BOB listen for a wake word ("Hey Bob"):
```bash
./bob_listen.sh
```

### Key Commands
- `exit`: Close the assistant.
- `clear`: Clear the terminal screen.
- `voice`: Activate 5-second voice recording.
- `What is the weather in London?`: Example of tool use.
- `Check my system status`: Example of system monitoring.

---

## Technical Details
- **Core Agent:** `bob_agent.py`
- **Voice Input:** `bob_record.py` & `bob_hear.py`
- **Voice Output:** `bob_speak.py`
- **Memory:** `memory.txt`
- **API (Optional):** `bob_api.py` (FastAPI wrapper)

## License
MIT
