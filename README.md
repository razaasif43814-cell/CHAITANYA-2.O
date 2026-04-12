# CHAITANYA-2.O
# 🤖 CHAITANYA 2.O – AI Desktop Assistant

A powerful voice-controlled AI assistant built using **Python**, combining AI intelligence, automation, and a modern GUI to perform real-world tasks through voice commands.

---

## 👨‍💻 Creators

* **Creator:** Nitish Yadav
* **Co-Creator:** Asif Raza

---

## 🚀 Overview

CHAITANYA 2.O is an advanced AI assistant capable of understanding voice commands, processing them intelligently, and performing actions like answering questions, automating tasks, generating images, and more.

---

## 🧠 Features

* 🎙️ Speech Recognition (Voice Input)
* 🔊 Text-to-Speech (Voice Output)
* 💬 AI Chatbot (LLM-powered)
* ⚡ Automation (open apps, search, play media)
* 🌐 Real-time search engine
* 🎨 AI Image Generation
* 🖥️ Modern GUI (PyQt5 interface)

---

## 🧩 Project Structure

```id="treefinal"
CHAITANYA-2.O/
│
├── Main.py                  # Main entry point (runs assistant)
│
├── Frontend/
│   ├── GUI.py              # GUI interface (PyQt5)
│   ├── Files/              # Temp data (status, mic, responses)
│   └── Graphics/           # Icons, GIFs, UI assets
│
├── Backend/
│   ├── Chatbot.py          # AI chatbot logic
│   ├── Model.py            # Decision-making model
│   ├── Automation.py       # Task automation
│   ├── RealtimeSearchEngine.py  # Live search
│   ├── SpeechToText.py     # Voice input system
│   ├── TextToSpeech.py     # Voice output system
│   └── ImageGeneration.py  # AI image generation
│
├── Data/
│   ├── ChatLog.json        # Chat history
│   ├── SearchLog.json      # Search history
│   ├── Voice.html          # Speech recognition page
│   └── Generated files     # Images & audio
│
├── .env                    # API keys & configuration
└── README.md               # Documentation
```

---

## ⚙️ How It Works

1. User speaks a command
2. Speech is converted to text
3. AI model classifies the query
4. System performs:

   * Chatbot 🤖
   * Automation ⚙️
   * Real-time search 🌐
   * Image generation 🎨
5. Output is displayed and spoken

---

## ▶️ Run the Project

```bash id="runupdated"
pip install pyqt5 cohere groq edge-tts pygame selenium webdriver-manager pillow requests python-dotenv pywhatkit AppOpener keyboard
python Main.py
```

---

## 🎯 Example Commands

* “Open Chrome”
* “Play songs on YouTube”
* “What is Artificial Intelligence?”
* “Generate image of a robot”
* “Search latest news”

---

## 🚀 Future Scope

* Wake word detection (“Hey Chaitanya”)
* Offline AI support
* Mobile/web version
* Advanced scheduling & reminders

---

## 📄 License

Open-source project for learning and development.

---

## 🙌 Credits

Inspired by modern AI assistants like Jarvis, Alexa, and Google Assistant.

---
