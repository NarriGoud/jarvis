@echo off
title Jarvis System Launcher

:: Step 1: Activate the virtual environment
call jarvis_env\Scripts\activate

:: Step 2: Start the FastAPI Brain in a new window
echo 🧠 Starting Jarvis Brain (API)...
start "Jarvis API" cmd /c "uvicorn app.main:app --reload"

:: Step 3: Smart Wait for the Brain to load weights
echo ⏳ Initializing neural weights... please wait.
:wait_loop
curl -s http://127.0.0.1:8000/health >nul
if %errorlevel% neq 0 (
    timeout /t 2 >nul
    goto wait_loop
)

echo ✅ Brain is Online! Neural link established.

:: Step 4: Start the Voice Interface
echo 🎤 Starting Voice Interface...
python voice_jarvis.py

pause