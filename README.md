# Lavendar AI Assistant

Lavendar is a Windows-optimized, voice-enabled AI assistant with a webcam interface and chat UI, built using Python, Gradio, OpenAI/Groq, and ElevenLabs APIs. It supports continuous speech-to-text, AI-powered conversation, and text-to-speech responses, all in a modern web interface.

## Features
- 🎤 Continuous speech-to-text (STT) using Groq API
- 🤖 AI-powered chat responses (OpenAI/Groq)
- 🔊 Text-to-speech (TTS) with ElevenLabs
- 📹 Live webcam feed with Windows-optimized camera handling
- 💬 Modern Gradio chat UI with avatars
- 🪟 Designed for Windows compatibility

## Requirements
- Python 3.10+
- ffmpeg (must be installed and in your PATH)
- A Groq API key (for STT and chat)
- An ElevenLabs API key (for TTS)

## Installation
1. **Clone the repository:**
	```powershell
	git clone https://github.com/Sanawer-Batool/Lavendar-AI-Assistant.git
	cd Lavendar-AI-Assistant
	```
2. **Create and activate a virtual environment:**
	```powershell
	python -m venv .venv
	.venv\Scripts\activate
	```
3. **Install dependencies:**
	```powershell
	uv pip install -r requirements.txt
	```
	Or, if using `pyproject.toml`:
	```powershell
	uv pip install -r pyproject.toml
	```
4. **Install ffmpeg:**
	- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
	- Extract and add the `bin` folder to your system PATH
	- Verify with: `ffmpeg -version`

5. **Set up environment variables:**
	- Create a `.env` file in the project root:
	  ```env
	  GROQ_API_KEY=your_groq_api_key_here
	  ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
	  ```

## Usage
1. **Run the assistant:**
	```powershell
	uv run main.py
	```
2. **Open your browser:**
	- Go to `http://127.0.0.1:7860` (or the port shown in the terminal)

3. **Interact:**
	- Click "Start Camera" to enable webcam
	- Speak to the assistant; it will transcribe, respond, and speak back
	- Say "goodbye", "exit", or "quit" to end the conversation

## File Structure
- `main.py` – Main app and Gradio UI
- `speech_to_text.py` – Audio recording and transcription
- `text_to_speech.py` – TTS with ElevenLabs
- `ai_agent.py` – AI chat logic
- `tools.py` – Utility functions
- `sample.jpg` – Sample image (for avatars or UI)
- `responses/`, `audio/`, `temp/` – Runtime directories

## Troubleshooting
- **ffmpeg not found:**
  - Ensure ffmpeg is installed and its `bin` folder is in your PATH
- **API key errors:**
  - Double-check your `.env` file and keys
- **Microphone/camera issues:**
  - Make sure your devices are connected and not used by other apps

## License
MIT License

---

*Lavendar AI Assistant – Your personal, voice-enabled AI for Windows!*
