import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# ------------ Logging ------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("app")

# ------------ Env ------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    raise SystemExit("Missing GEMINI_API_KEY. Put it in .env or set as env var.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# ------------ Flask ------------
app = Flask(__name__, static_folder="static", template_folder="templates")


def build_prompt(title: str) -> str:
    """Return a descriptive, semester-style course generation prompt."""
    return f"""
You are an expert educational designer. Create a **detailed, descriptive course outline** for the course titled "{title}".

The output must look like a semester syllabus with clear sections, formatted with Markdown-style headings.

Required sections:
1. **Objective of the Course:**
   - Write 1–2 descriptive paragraphs explaining the main goal of the course and what students will achieve.

2. **Sample Syllabus (Semester-wise):**
   - Provide 8–10 weekly modules or topics.
   - Each module should have a main theme and 2–3 sub-bullets describing subtopics or activities.

3. **Three Measurable Outcomes:**
   - Organize into categories: Knowledge, Comprehension, Application.
   - Use measurable verbs (e.g., explain, design, analyze, implement, evaluate).
   - Each outcome should have 2–3 specific points.

4. **Assessment Methods:**
   - List 3–4 types of assessments (assignments, quizzes, projects, presentations, final exam).
   - Briefly explain how each aligns with the learning outcomes.

5. **Recommended Readings:**
   - Provide 4–5 scholarly references (Author, Title, Year).

Formatting rules:
- Use Markdown-like formatting with **bold headings** and numbered/bulleted lists (like the sample in the screenshot).
- Ensure the text is **detailed and descriptive**, not just bullet points.
- Write naturally as if preparing an academic course syllabus.
""".strip()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    try:
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Course title is required."}), 400
        if len(title) > 120:
            return jsonify({"error": "Course title too long (max 120)."}), 400

        prompt = build_prompt(title)
        logger.info(f"Generating descriptive content for title='{title}' using {GEMINI_MODEL}")

        response = model.generate_content(
            prompt,
            safety_settings=None,
            generation_config={
                "temperature": 0.6,
                "max_output_tokens": 3000,
            },
        )

        raw = (response.text or "").strip()

        return jsonify({"title": title, "content": raw}), 200

    except Exception as e:
        logger.exception("Unhandled error in /api/generate")
        return jsonify({"error": str(e)}), 500


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", "8000"))
    logger.info(f"Starting app on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
