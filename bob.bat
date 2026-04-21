@echo off
setlocal

echo ==============================
echo 🤖 BOB AI ASSISTANT READY
echo ==============================

:loop
set /p input="You: "

if "%input%"=="exit" (
    echo BOB: Goodbye 👋
    goto :eof
)

if "%input%"=="" goto loop

if "%input%"=="clear" (
    cls
    goto loop
)

:: Voice command
if "%input%"=="voice" (
    echo BOB: Listening... 🎤
    python bob_record.py input.wav
    echo BOB: Processing speech... 🧠
    for /f "delims=" %%i in ('python bob_hear.py input.wav') do set input=%%i
    echo You (Voice): %input%
)

echo BOB: Thinking... 🤔

:: Run the AI agent
for /f "delims=" %%i in ('python bob_agent.py %input%') do set response=%%i

echo ------------------------------
echo BOB: %response%
echo ------------------------------

:: Voice output (run in background-ish)
start /b python bob_speak.py "%response%"

goto loop
