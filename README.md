# IELTS Practice Platform

A compact Flask-based prototype for practicing IELTS tasks. The app uses JSON files for lightweight storage and focuses on a minimal, easy-to-run developer experience so you can iterate quickly on features.

**Goals**
- Provide a small, self-contained codebase to add reading, listening, speaking and writing practice features.
- Keep user management simple (JSON-backed) so you can focus on feature development.

**Who is this for**
- Developers building or prototyping IELTS study features.

**Repository layout**
- `app.py`: application entry point and Flask app setup.
- `auth.py`: signup, login, and logout routes and logic.
- `dashboard.py`: authenticated dashboard view and routes.
- `models.py`: `User` model used by Flask-Login.
- `data_store.py`: small helpers for safe JSON file read/write (file locking).
- `data/`: JSON files used as the data store (users, sessions, content, submissions).
- `templates/`: Jinja2 templates for the site UI.
- `static/css/style.css`: basic site styling.

Developer setup (macOS / Linux)

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the development server

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
```

Tips for development
- Data is stored in the `data/` folder as JSON files. Back up or reset these files if you need a fresh start.
- Passwords are hashed using `werkzeug.security` in `auth.py`.
- Use the dashboard routes in `dashboard.py` as a reference when adding authenticated features.

Recommended minimal changes for new features
- Add new JSON files under `data/` for domain content (e.g., `reading_content.json`).
- Create routes and templates under the existing structure; keep logic in small modules (`auth.py`, `dashboard.py`).

Contributing
- Open a branch for your feature, keep commits focused, and add brief notes to the project owner about data file changes.

Contact / Next steps
- This README is a developer-focused starting point. If you'd like, I can add a quick CLI script to initialize or reset the `data/` JSON files, or add a `Makefile` with common tasks.
