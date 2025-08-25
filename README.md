# AI Course Generator (Gemini + Flask)
Simple web tool that turns a course title into structured educational content.

## Quick Start (Windows PowerShell)
```
cd ai-course-generator-gemini
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env   # paste your real GEMINI_API_KEY
python app.py
# open http://127.0.0.1:8000
```
