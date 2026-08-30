# IELTS Practice Platform

A lightweight Flask-based prototype for practicing IELTS reading, listening, speaking, and writing tasks. Built for developers who want to quickly iterate on IELTS study features without complex infrastructure.

## Features

- **User Authentication**: Sign up, login, and logout with password hashing
- **Practice Modules**: Reading, listening, speaking (cue cards), and writing
- **Simple Data Storage**: JSON-based storage with file locking for concurrent safety
- **Clean Architecture**: Organized with Flask blueprints for maintainability

## Project Structure

```
ielts-platform/
├── app/                              # Main application package
│   ├── __init__.py                   # Flask app factory
│   ├── models.py                     # User model for Flask-Login
│   ├── data_store.py                 # JSON file operations with locking
│   ├── blueprints/
│   │   ├── auth/                     # Authentication (login, signup, logout)
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── dashboard/                # User dashboard
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── main/                     # Public pages (home, reading, listening)
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── static/                       # CSS, JavaScript, images
│   │   └── css/
│   │       └── style.css
│   └── templates/                    # Jinja2 HTML templates
│       ├── base.html                 # Base template
│       ├── index.html
│       ├── dashboard.html
│       ├── reading.html
│       ├── listening.html
│       └── auth/
│           ├── login.html
│           └── signup.html
├── data/                             # JSON data files
│   ├── users.json                    # User accounts
│   ├── sessions.json
│   ├── reading_content.json
│   ├── listening_content.json
│   ├── writing_prompts.json
│   ├── speaking_cuecards.json
│   ├── writing_submissions.json
│   └── feedback_usage.json
├── app.py                            # Application entry point
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Developer Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ielts-platform
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Development Server

```bash
export FLASK_ENV=development
python app.py
```

The application will be available at `http://localhost:5000`

### Environment Variables

Set these optional environment variables:

```bash
export FLASK_ENV=development        # Enable debug mode
export SECRET_KEY=your-secret-key   # Change default session key (use random string in production)
```

## Key Modules

### `app/__init__.py` - Application Factory
Creates and configures the Flask app with:
- Flask-Login for user authentication
- Blueprint registration
- Template and static folder configuration
- Data file initialization

### `app/models.py` - User Model
Implements `User` class with Flask-Login integration for session management

### `app/data_store.py` - Data Persistence
Provides thread-safe JSON file operations:
- File locking with `fcntl` to prevent concurrent write conflicts
- Atomic writes using temporary files
- User management functions (create, fetch by ID/email)
- Graceful error handling with JSON corruption recovery

### `app/blueprints/` - Route Organization
Modular route handlers:
- **auth**: Signup, login, logout
- **dashboard**: User authenticated pages
- **main**: Public pages

## Adding New Features

### 1. Add a New Route

Create in `app/blueprints/your_feature/routes.py`:

```python
from flask import Blueprint, render_template

feature_bp = Blueprint("feature", __name__)

@feature_bp.route("/your-route")
def your_route():
    return render_template("your_template.html")
```

### 2. Register the Blueprint

Update `app/__init__.py`:

```python
from app.blueprints.your_feature import feature_bp
# ...
app.register_blueprint(feature_bp)
```

### 3. Add Authentication (if needed)

```python
from flask_login import login_required

@feature_bp.route("/protected")
@login_required
def protected_route():
    return render_template("protected.html")
```

### 4. Access User Data

```python
from flask_login import current_user

@feature_bp.route("/user-data")
@login_required
def user_data():
    email = current_user.email
    return render_template("user_info.html", email=email)
```

## Data Storage

All user data is stored in JSON files in the `data/` directory:

- **users.json**: User accounts with hashed passwords
- **sessions.json**: User session data
- **reading_content.json**: Reading practice materials
- **listening_content.json**: Listening practice materials
- **writing_prompts.json**: Writing task prompts
- **speaking_cuecards.json**: Speaking cue cards
- **writing_submissions.json**: Submitted writing tasks
- **feedback_usage.json**: Feedback metrics

## Security Notes

⚠️ **For Development Only**

- Default `SECRET_KEY` is "dev-secret-change-me" - **change this in production**
- Passwords are hashed using `werkzeug.security.generate_password_hash`
- Email addresses are normalized (lowercase, whitespace trimmed)
- No rate limiting on login attempts - add this for production

## Tips for Development

- **Backup Data**: JSON files in `data/` contain user data. Back up before major changes
- **Reset Data**: Delete JSON files to start fresh (they'll be recreated)
- **Hot Reload**: Flask auto-reloads when you modify Python files (FLASK_ENV=development)
- **Debug Mode**: Enable with FLASK_ENV=development for better error messages
- **Testing Logins**: Create test accounts and check `data/users.json` for password hashes

## Dependencies

- **Flask**: Web framework
- **Flask-Login**: User session management
- **Werkzeug**: Security utilities (password hashing)

See `requirements.txt` for versions.

## Troubleshooting

### ImportError: Cannot import from app
- Ensure you're running from the project root
- Verify the .venv is activated
- Check that app/ directory exists

### 404 Not Found on routes
- Verify blueprint is registered in `app/__init__.py`
- Check that template files exist in `app/templates/`
- Use `flask routes` to list all registered routes

### Data not persisting
- Verify `data/` directory exists and is writable
- Check file permissions: `ls -la data/`
- JSON files must be valid: check with `python -m json.tool data/users.json`

### Login not working after signup
- Verify data was written: check `data/users.json` is not empty
- Confirm password is hashed correctly
- Check browser cookies are enabled

## Future Enhancements

- [ ] Database migration (SQLite/PostgreSQL)
- [ ] More comprehensive IELTS content
- [ ] User progress tracking and analytics
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Export results/reports

## License

This prototype is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check this README
2. Review error messages (enable debug mode)
3. Inspect JSON data files
4. Check Flask logs for traceback information
- Add new JSON files under `data/` for domain content (e.g., `reading_content.json`).
- Create routes and templates under the existing structure; keep logic in small modules (`auth.py`, `dashboard.py`).

Contributing
- Open a branch for your feature, keep commits focused, and add brief notes to the project owner about data file changes.

Contact / Next steps
- This README is a developer-focused starting point. If you'd like, I can add a quick CLI script to initialize or reset the `data/` JSON files, or add a `Makefile` with common tasks.
