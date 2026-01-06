# API Keys and Providers

To enable real LLM-powered refactors, configure API keys for the provider you want to use.

Providers referenced by the project:

- **Gemini (Google)** — Sign up and obtain an API key from Google AI Studio.
- **Grok (xAI)** — Register at x.ai and obtain a key.
- **Claude (Anthropic)** — Obtain a key from Anthropic.
- **Ollama (Local)** — If using Ollama locally, ensure `ollama serve` is running and configure `OLLAMA_HOST` as needed.

Environment variables

Set keys in your shell or in a `.env` file (project reads `.env` if you integrate it):

```text
GEMINI_API_KEY=...
GROK_API_KEY=...
CLAUDE_API_KEY=...
OLLAMA_HOST=http://localhost:11434
```

Security tip: Never commit API keys to source control; rely on environment variables or secrets management in production.