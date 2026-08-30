"""
Application entry point for the IELTS Practice Platform.
This module creates and runs the Flask application using the app package.
"""

import os
from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from auth import auth_bp
from data_store import ensure_data_files, get_user_by_id
from listening import listening_bp
from models import User
from reading import reading_bp

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["JSON_SORT_KEYS"] = False

ensure_data_files()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data)
    return None


@app.route("/")
def home():
    return render_template("home.html", user=current_user)


@app.route("/index")
def index():
    return render_template("home.html", user=current_user)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


app.register_blueprint(auth_bp)
app.register_blueprint(reading_bp)
app.register_blueprint(listening_bp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
