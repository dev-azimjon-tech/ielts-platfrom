# IELTS Practice Platform

A simple Flask project skeleton for an IELTS prep site with JSON-backed user storage and a clean feature-based file structure.

## Project structure

- `app.py` — main app entry point and app factory
- `auth.py` — signup, login, and logout logic
- `dashboard.py` — authenticated dashboard page
- `data_store.py` — safe JSON file reads/writes with file locking
- `models.py` — Flask-Login user model
- `data/` — JSON storage for users and future platform data
- `templates/` — Jinja2 UI templates
- `static/css/style.css` — site styling

## Local setup

1. Create a virtual environment
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies
   - `pip install -r requirements.txt`
3. Run the app
   - `python app.py`

## Current status

The project is currently set up for:

- user registration
- login/logout
- password hashing with `werkzeug.security`
- Flask-Login session support
- basic dashboard UI

This is a clean starting point before adding reading, listening, writing, and speaking modules.