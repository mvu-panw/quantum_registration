# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Standalone event registration page for a Palo Alto Networks quantum-safe networking lunch-and-learn. Visitors submit Name, Email, and Company; data is appended to `registrations.csv`; they land on a confirmation page.

## Running Locally

```bash
pip install flask
python3 server.py   # http://localhost:3535
```

No `requirements.txt` — `flask` is the only dependency.

## Architecture

Flask serves everything: `static_folder='.'` means all HTML, CSS, and images are served directly by Flask — no separate static server needed.

**Submission flow:**
1. `index.html` inline JS validates the form client-side, then POSTs JSON `{name, email, company}` to `POST /register`
2. `server.py` strips/lowercases fields, appends a UTC-timestamped row to `registrations.csv`, returns `{"status": "ok"}`
3. On success the JS does `window.location.href = 'thank-you.html'` — this is a client-side redirect, not a server redirect

`ensure_csv()` creates the CSV with a header row on first run; it's called at startup and lazily before each write. `thank-you.html` is directly accessible without going through the form.

## Key Files

- `index.html` — registration form; all submission logic is in an inline `<script>` at the bottom
- `thank-you.html` — static confirmation page; no server logic
- `css/styles.css` — all styles for both pages; PANW brand tokens defined as CSS custom properties in `:root` (`--orange`, `--navy`, etc.)
- `server.py` — Flask app (~30 lines): serves static files + handles `POST /register`
- `registrations.csv` — auto-created on first submission; not committed
