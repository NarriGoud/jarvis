# JARVIS: Tactical Command Interface 🤖

Jarvis is a high-performance, semi-offline AI assistant designed for system automation, developer productivity, and proactive monitoring. It utilizes a FastAPI-based "Brain" for complex logic via Groq and executes system-level tasks locally.

---

## 🚀 Core Features

- **Semi-Offline Architecture:** Offline Speech-to-Text (Vosk) and Text-to-Speech (pyttsx3) for privacy and speed.
- **Barge-in Support:** Instantly interrupt Jarvis mid-sentence; the mic is always listening for commands.
- **Contextual Awareness (Ghost Log):** Monitors active windows to track productivity and offer proactive project assistance.
- **System Mastery:** Controls media playback, system volume, takes screenshots, and monitors hardware (CPU/RAM).
- **Developer Tools:** Automated FastAPI project scaffolding and file organization.
- **Remote Alerts:** Integrated with Telegram for urgent notifications and system status reports.

---

## 🏗️ Project Structure

```text
D:\Kelly-1.0.0\jarvis\
├── app/
│   ├── main.py          # FastAPI Brain (Heart of the system)
│   ├── api.py           # Tool mapping and Groq integration
├── core/
│   ├── voice.py         # Vosk-powered offline listening
│   ├── speaker.py       # Speech management and Barge-in logic
│   ├── vosk-model/      # Offline STT Model (User provided)
├── tools/
│   ├── observer.py      # Background "Ghost Log" window monitor
│   ├── system.py        # Hardware stats (psutil)
│   ├── actions.py       # File and Media controls
│   ├── vision.py        # Screenshot capabilities
├── images/              # Screen captures and backups
├── speak.py             # Offline TTS execution script
└── start_jarvis.bat     # Smart-wait launcher
```

---

## 🛠️ Setup Instructions

### 1. Requirements

Ensure you have **Python 3.10+** installed. Install all dependencies:

```bash
pip install fastapi uvicorn requests psutil pyautogui pycaw comtypes pywin32 pygetwindow vosk pyttsx3
```

---

### 2. Offline Model Setup

For offline voice recognition:

1. Download the **Vosk Small English Model**.
2. Extract the contents into:

```
core/vosk-model/
```

3. Verify that `core/vosk-model/am/` and other model files are present.

---

### 3. Environment Variables

Create a `.env` file in the root directory:

```plaintext
GROQ_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_id_here
```

---

## 🚦 Usage

- **Launch the System:**  
  Double-click `start_jarvis.bat`.  
  This starts the FastAPI Brain and Voice Interface.

- **Wake Word:**  
  Say **"Hey Jarvis"** or **"Jarvis"**.

- **Interruption:**  
  Speak while Jarvis is talking. Playback stops instantly.

---

## 🛡️ Future Roadmap

- [ ] Integration with MarketMind AI LSTM models.
- [ ] Automated daily backup of business logs to Oracle Cloud.
- [ ] Network Sentinel: Telegram alerts for new Wi-Fi devices.
