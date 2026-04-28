# BOB AI Assistant (TUI Edition)

BOB is a custom-built, local AI executive assistant designed to run directly in your terminal with a professional Textual User Interface (TUI). It combines the reasoning power of **Ollama (Gemma)** with practical system tools and voice capabilities.

## Features
- **Local AI:** Powered by Ollama (`gemma4:e4b` by default), ensuring privacy and offline capability.
- **TUI Interface:** Beautifully formatted terminal experience using the `rich` library.
- **Voice Support:** Speak to BOB and hear responses back.
- **Tool Integration:** BOB can read/write files, check weather, news, and system stats.
- **Memory:** Remembers user preferences and facts across sessions.

## Installation

### 1. Prerequisites
- **Ollama:** Install from [ollama.com](https://ollama.com).
- **Python 3.10+**
- **System Tools:** `arecord` (part of `alsa-utils`) for voice recording on Linux.

### 2. Setup
1. Clone the repository and navigate to the folder.
2. Download the AI model:
   ```bash
   ollama pull gemma4:e4b
   ```
3. Run the installer/launcher:
   ```bash
   chmod +x bob.sh
   ./bob.sh
   ```
   *Note: BOB will automatically create a `memory.txt` file to store personal facts. This file is ignored by Git to protect your privacy.*

## Usage
Run `./bob.sh` to start the assistant.

### Commands
- `voice`: Activate voice recognition to speak your command.
- `clear`: Clear the terminal screen.
- `exit`: Close the assistant.
- `downloads`, `documents`, `desktop`: Open respective system folders.

## Customization
BOB uses environment variables for configuration. You can create a `.env` file in the project root to set these:

```env
CURRENTS_API_KEY=your_key_here
BOB_MODEL="gemma4:e4b"
```

### News API
BOB uses the **Currents API** for latest news. You can get a free key at [currentsapi.services](https://currentsapi.services/).

### AI Model
You can change the AI model by setting the `BOB_MODEL` environment variable in your `.env` or exporting it:
```bash
export BOB_MODEL="gemma2:9b"
./bob.sh
```
