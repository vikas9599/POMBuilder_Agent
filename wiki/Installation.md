# Installation

Follow these steps to get the project running locally.

1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a Python virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Optional: configure environment variables

- `GEMINI_API_KEY` — your Google/Gemini key (if used)
- `GROK_API_KEY` — xAI Grok key
- `CLAUDE_API_KEY` — Anthropic key
- `OLLAMA_HOST` — if using Ollama locally

5. Run the app

```bash
python app.py
```

Open your browser to `http://127.0.0.1:5000`.