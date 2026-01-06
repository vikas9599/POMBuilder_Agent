# Usage

This section explains how to use the POMify web UI to refactor Playwright scripts into a Page Object Model structure.

1. Start the application

```bash
python app.py
```

2. Open the UI

Navigate to `http://127.0.0.1:5000` in your browser.

3. Refactor a script

- **Upload**: Drag and drop a Playwright `.js` or `.ts` script in the provided upload box.
- **Configure**: Choose an LLM provider and (optionally) provide API key + model name.
- **Run**: Click **Refactor Script** and review the generated `TestPage`, `TestData`, and `TestScript` outputs.
- **Export**: Copy or click the download icon to save generated files.

Notes

- If no API key is provided, the app may fall back to a mock mode for local testing.
- Keep input scripts concise (single test file at a time) for best results.