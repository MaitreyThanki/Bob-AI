import os
import sys
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.prompt import Prompt
from bob_agent import agent, consolidate_memory, stream_agent

# ... existing imports ...

# Initialize Rich Console
console = Console()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def open_folder(path):
    expanded_path = os.path.expanduser(path)
    if os.path.exists(expanded_path):
        console.print(f"[bold green]BOB:[/bold green] Opening {path} 📂")
        if os.name == 'posix':
            subprocess.Popen(['xdg-open', expanded_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        else:
            os.startfile(expanded_path)
    else:
        console.print(f"[bold red]BOB:[/bold red] Folder {path} not found.")

def handle_voice():
    input_wav = os.path.join(SCRIPT_DIR, "input.wav")
    with console.status("[bold magenta]BOB is Listening... 🎤", spinner="pulse"):
        subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "bob_record.py"), input_wav], check=False)
    
    with console.status("[bold cyan]Processing speech... 🧠", spinner="dots"):
        result = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "bob_hear.py"), input_wav], capture_output=True, text=True)
        user_input = result.stdout.strip()
    
    if user_input.startswith("Error"):
        console.print(f"[bold red]BOB:[/bold red] {user_input}")
        return None
    
    console.print(f"[bold yellow]You (Voice):[/bold yellow] {user_input}")
    return user_input

def main():
    clear_screen()
    console.print(Panel(
        Text("BOB AI ASSISTANT (Gemma Edition)", justify="center", style="bold blue"),
        subtitle="Type 'exit' to quit | 'clean' to optimize memory",
        border_style="bright_blue"
    ))

    # Optional: Consolidate memory on startup to keep things fresh
    with console.status("[bold magenta]Optimizing memory... ✨", spinner="bouncingBar"):
        consolidate_memory()

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            if not user_input.strip():
                continue

            # Special Commands
            if user_input.lower() == "exit":
                console.print("[bold yellow]BOB: Goodbye 👋[/bold yellow]")
                break
            
            if user_input.lower() == "clear":
                clear_screen()
                console.print(Panel(Text("BOB AI ASSISTANT", justify="center", style="bold blue"), border_style="bright_blue"))
                continue

            if user_input.lower() == "clean":
                with console.status("[bold magenta]Cleaning and optimizing memory... ✨", spinner="bouncingBar"):
                    msg = consolidate_memory()
                console.print(f"[bold green]BOB:[/bold green] {msg}")
                continue

            # System Folders
            if "downloads" in user_input.lower():
                open_folder("~/Downloads")
                continue
            if "documents" in user_input.lower():
                open_folder("~/Documents")
                continue
            if "desktop" in user_input.lower():
                open_folder("~/Desktop")
                continue

            # AI Processing
            response_content = ""
            current_status = "BOB is thinking... 🤔"
            
            def make_panel(content, status):
                return Panel(
                    Markdown(content + ("\n\n---\n*" + status + "*" if status else "")),
                    title="[bold blue]BOB[/bold blue]",
                    border_style="blue"
                )

            with Live(make_panel("", current_status), console=console, refresh_per_second=10) as live:
                def update_status(msg):
                    nonlocal current_status
                    current_status = msg
                    live.update(make_panel(response_content, current_status))

                for chunk in stream_agent(user_input, status_callback=update_status):
                    response_content += chunk
                    # Clear status once we start getting the actual response
                    if current_status:
                        current_status = ""
                    live.update(make_panel(response_content, ""))

            # Voice Output disabled as requested
            # subprocess.Popen([sys.executable, os.path.join(SCRIPT_DIR, "bob_speak.py"), response], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        except KeyboardInterrupt:
            console.print("\n[bold yellow]BOB: Goodbye 👋[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]System Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
