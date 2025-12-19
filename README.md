# Telugu Voice Agent (Government Schemes)

A voice-first AI agent that helps citizens verify eligibility for schemes like Rythu Bandhu.

## Tech Stack (Free Tier)
- **LLM:** Llama 3.1-70B (via Groq)
- **STT:** Whisper Large V3 (via Groq)
- **TTS:** Edge TTS (Microsoft Neural Voices)
- **Framework:** LangGraph# Telangana Bandhu: Voice-First Government Service Agent

**Telangana Bandhu** is an autonomous AI agent designed to help citizens of Telangana identify and apply for government welfare schemes (like *Rythu Bandhu* and *Aasara Pensions*) using natural **Telugu** voice interaction.

Unlike simple chatbots, this system uses an **Agentic Workflow** (LangGraph) to reason, plan, and execute tool calls to verify user eligibility dynamically.

---

## 🏗️ Architecture

The system follows a "Listen → Think → Act → Speak" pipeline:

1.  **Voice Input (The Ears):** Records audio and transcribes it using **Groq Whisper (Large-v3)**.
2.  **Agent Core (The Brain):** Uses **Llama 3.3 70B** (via Groq) to reason and decide next steps.
3.  **Tools (The Hands):** Custom Python functions (`check_eligibility`, `get_scheme_details`) to fetch data.
4.  **Voice Output (The Mouth):** Synthesizes natural Telugu speech using **Edge TTS** (`te-IN-MohanNeural`).

---

## 🛠️ Tech Stack (Free & Open Source)

* **Language:** Python 3.10+
* **Orchestration:** LangGraph (State Machine)
* **LLM:** Llama 3.3-70b-versatile (via Groq API - Free Tier)
* **Speech-to-Text:** Whisper-large-v3 (via Groq API)
* **Text-to-Speech:** Edge TTS (Microsoft Azure Neural Voices)
* **Audio Handling:** SoundDevice, Scipy, FFmpeg

---

## 🚀 Setup Instructions

### 1. Prerequisites
* Install **Python** (3.10 or higher).
* Install **FFmpeg** (Required for audio processing).
    * *Windows:* `winget install ffmpeg` (Run in PowerShell)
    * *Mac:* `brew install ffmpeg`
    * *Linux:* `sudo apt install ffmpeg`

### 2. Installation
Clone the repository and install dependencies:

```bash
# Install Python libraries
pip install langchain-groq groq edge-tts sounddevice scipy numpy langgraph python-dotenv langchain-communitystop


## Setup
1. Install dependencies: `pip install .`
2. Add API Key to `.env`: `GROQ_API_KEY=...`
3. Run: `python main.py`# Telugu-Bandhu
