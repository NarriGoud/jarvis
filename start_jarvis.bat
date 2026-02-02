@echo off
title Jarvis System Launcher

:: Step 1: Activate the virtual environment
call jarvis_env\Scripts\activate

:: Step 2: Start the FastAPI Brain in a new window
echo 🧠 Starting Jarvis Brain (API)...
start "Jarvis API" cmd /k "uvicorn app.main:app --reload"

:: Step 3: Wait a moment for the server to spin up
timeout /t 3

:: Step 4: Start the Voice Interface
echo 🎤 Starting Voice Interface...
python voice_jarvis.py

pause