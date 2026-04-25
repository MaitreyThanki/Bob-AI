import sys
import subprocess
import requests
import os
import re
import platform
try:
    import psutil
except ImportError:
    psutil = None

# -------- MEMORY --------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.txt")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return ""
    with open(MEMORY_FILE, "r") as f:
        return f.read()

def save_memory(new_info):
    current_memory = load_memory()
    clean_info = new_info.strip().rstrip('.')
    if clean_info.lower() in current_memory.lower():
        return False
    with open(MEMORY_FILE, "a") as f:
        f.write(clean_info + ".\n")
    return True

def automate_memory(user_input, ai_response):
    # ... (code for automate_memory)
    # I will keep the previous implementation of automate_memory here for context
    current_memory = load_memory()
    prompt = f"""
[SYSTEM] You are BOB's Memory Processor.
Your task is to extract NEW, UNIQUE, and HIGH-SIGNAL facts about the user from the conversation.

CRITICAL RULES:
- ONLY extract personal facts (preferences, names, locations, tools used, OS, habits).
- DO NOT extract meta-information (e.g., "User is talking to AI", "User sent a message").
- DO NOT extract facts that are ALREADY in the Current Memory below.
- DO NOT extract empty or generic statements.
- Format: "User [fact]."
- If no NEW and UNIQUE facts are found, reply ONLY with 'NONE'.

Current Memory:
{current_memory}

User: {user_input}
AI: {ai_response}

New Unique Fact:"""
    extracted = ask_ai(prompt).strip()
    if extracted and extracted.upper() != "NONE" and len(extracted) < 150:
        # Final sanity check to avoid junk
        if "User " in extracted and not any(x in extracted.lower() for x in ["interact", "talk", "none", "nothing"]):
            save_memory(extracted)

def consolidate_memory():
    """Reads memory.txt and asks the AI to deduplicate and clean it."""
    current_memory = load_memory()
    if not current_memory.strip():
        return "Memory is already empty."

    prompt = f"""
[SYSTEM] You are BOB's Memory Optimizer.
Below is a messy list of facts about a user. 
Your goal is to:
1. Deduplicate similar facts.
2. Remove meta-noise (e.g., "User is talking", "NONE", "Extracted fact").
3. Correct formatting to "User [fact]."
4. Keep only high-signal personal information.

Messy Memory:
{current_memory}

Cleaned, Unique Facts (Bulleted List):"""

    cleaned = ask_ai(prompt).strip()
    if cleaned and len(cleaned) > 10:
        # Reformat bulleted list to plain lines
        lines = [line.strip("- ").strip() for line in cleaned.split("\n") if line.strip()]
        final_memory = "\n".join([f"{line.rstrip('.')}." for line in lines if "User " in line])
        
        with open(MEMORY_FILE, "w") as f:
            f.write(final_memory + "\n")
        return "Memory successfully consolidated and cleaned."
    return "Consolidation failed or returned empty."

# -------- TOOLS: FILE SYSTEM --------

def list_dir(path="."):
    try:
        full_path = os.path.abspath(os.path.join(SCRIPT_DIR, path))
        files = os.listdir(full_path)
        return "\n".join([f"📄 {f}" if os.path.isfile(os.path.join(full_path, f)) else f"📁 {f}" for f in files])
    except Exception as e:
        return f"Error listing directory: {e}"

def read_file(path):
    try:
        full_path = os.path.abspath(os.path.join(SCRIPT_DIR, path))
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path, content):
    try:
        full_path = os.path.abspath(os.path.join(SCRIPT_DIR, path))
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully written to {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def ask_ai_stream(prompt):
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = os.getenv("BOB_MODEL", "gemma4:e4b")
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                import json
                chunk = json.loads(line)
                yield chunk.get("response", "")
    except Exception as e:
        yield f"Error: {e}"

# -------- AI (OLLAMA) --------
def ask_ai(prompt):
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name = os.getenv("BOB_MODEL", "gemma4:e4b")
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        # Fallback to subprocess if API fails and we are not in Docker (optional, but let's keep it simple)
        try:
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                env={**os.environ, "TERM": "dumb"}
            )
            return result.stdout.strip()
        except:
            return f"Error connecting to AI: {e}"

# -------- TOOLS: EXTERNAL --------

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=801ef43486bc40309fdbba06460a9e05"
        data = requests.get(url).json()
        headlines = ["- " + a["title"] for a in data.get("articles", [])[:5]]
        return "\n".join(headlines)
    except:
        return "Unable to fetch news right now."

def get_weather(city=""):
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)
        return response.text.strip() if response.status_code == 200 else "Weather unavailable."
    except:
        return "Weather service error."

def get_system_info():
    try:
        info = f"OS: {platform.system()} {platform.release()}\n"
        if psutil:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info += f"CPU Usage: {cpu_usage}%\n"
            info += f"RAM: {memory.percent}% used ({memory.available // (1024**2)}MB free)\n"
            info += f"Disk: {disk.percent}% used ({disk.free // (1024**3)}GB free)"
        else:
            # Fallback for Linux if psutil is not installed (though it should be)
            if platform.system() == "Linux":
                uptime = subprocess.run(["uptime", "-p"], capture_output=True, text=True).stdout.strip()
                info += f"Uptime: {uptime}"
            else:
                info += "Install 'psutil' for detailed system info."
        return info
    except Exception as e:
        return f"Error gathering system info: {e}"

# -------- AGENT --------

def stream_agent(user_input, status_callback=None):
    memory = load_memory()
    
    # --- 1. TOOL SELECTION (Still non-streaming) ---
    if status_callback:
        status_callback("Analyzing request... 🔍")
    
    tool_prompt = f"""
[SYSTEM] You are BOB's Tool Controller.
Available Tools:
- LIST: (lists files)
- READ: <filename> (reads file)
- WRITE: <filename>|<content> (writes to file)
- WEATHER: <city> (checks weather)
- NEWS: (gets latest news)
- SYSTEM: (checks system status like CPU, RAM, Uptime)
- NONE: (no tool needed)

User: "{user_input}"
Decision (Output ONLY the command):"""

    decision = ask_ai(tool_prompt).strip()
    
    tool_result = ""
    if decision.startswith("LIST"):
        if status_callback: status_callback("Listing files... 📁")
        tool_result = list_dir()
    elif decision.startswith("READ:"):
        filename = decision.replace("READ:", "").strip()
        if status_callback: status_callback(f"Reading {filename}... 📄")
        tool_result = read_file(filename)
    elif decision.startswith("WRITE:"):
        try:
            _, params = decision.split(":", 1)
            filename, content = params.split("|", 1)
            if status_callback: status_callback(f"Writing to {filename}... ✏️")
            tool_result = write_file(filename.strip(), content.strip())
        except: tool_result = "Error in write format."
    elif decision.startswith("WEATHER"):
        if status_callback: status_callback("Checking weather... 🌦️")
        city = decision.replace("WEATHER:", "").strip()
        tool_result = get_weather(city)
    elif decision.startswith("NEWS"):
        if status_callback: status_callback("Fetching news... 📰")
        tool_result = get_news()
    elif decision.startswith("SYSTEM"):
        if status_callback: status_callback("Gathering system info... 💻")
        tool_result = get_system_info()

    if status_callback:
        status_callback("Generating response... 🤔")

    # --- 2. FINAL RESPONSE (Streaming) ---
    context = f"User Memory:\n{memory}"
    if tool_result:
        context += f"\n\nResult from {decision}:\n{tool_result}"

    final_prompt = f"""
[SYSTEM] You are BOB, a smart assistant. 
USER PROTOCOLS:
{memory}

Rules for Response:
- Use PLAIN TEXT only.
- DO NOT use Markdown (no stars *, no hashtags #).
- Use simple dashes (-) for lists.
- Stay concise and professional.

Context:
{context}

[USER] {user_input}

[RESPONSE]"""
    
    full_response = ""
    for chunk in ask_ai_stream(final_prompt):
        full_response += chunk
        yield chunk
    
    automate_memory(user_input, full_response)

def agent(user_input):
    memory = load_memory()
    user_input_lower = user_input.lower()

    # --- 1. TOOL SELECTION ---
    tool_prompt = f"""
[SYSTEM] You are BOB's Tool Controller.
Available Tools:
- LIST: (lists files)
- READ: <filename> (reads file)
- WRITE: <filename>|<content> (writes to file)
- WEATHER: <city> (checks weather)
- NEWS: (gets latest news)
- SYSTEM: (checks system status like CPU, RAM, Uptime)
- NONE: (no tool needed)

User: "{user_input}"
Decision (Output ONLY the command):"""

    decision = ask_ai(tool_prompt).strip()
    
    tool_result = ""
    if decision.startswith("LIST"):
        tool_result = list_dir()
    elif decision.startswith("READ:"):
        filename = decision.replace("READ:", "").strip()
        tool_result = read_file(filename)
    elif decision.startswith("WRITE:"):
        try:
            _, params = decision.split(":", 1)
            filename, content = params.split("|", 1)
            tool_result = write_file(filename.strip(), content.strip())
        except: tool_result = "Error in write format."
    elif decision.startswith("WEATHER"):
        city = decision.replace("WEATHER:", "").strip()
        tool_result = get_weather(city)
    elif decision.startswith("NEWS"):
        tool_result = get_news()
    elif decision.startswith("SYSTEM"):
        tool_result = get_system_info()

    # --- 2. FINAL RESPONSE ---
    context = f"User Memory:\n{memory}"
    if tool_result:
        context += f"\n\nResult from {decision}:\n{tool_result}"

    final_prompt = f"""
[SYSTEM] You are BOB, a smart assistant. 
USER PROTOCOLS:
{memory}

Rules for Response:
- Use PLAIN TEXT only.
- DO NOT use Markdown (no stars *, no hashtags #).
- Use simple dashes (-) for lists.
- Stay concise and professional.

Context:
{context}

[USER] {user_input}

[RESPONSE]"""
    
    response = ask_ai(final_prompt)
    automate_memory(user_input, response)
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(agent(" ".join(sys.argv[1:])))
