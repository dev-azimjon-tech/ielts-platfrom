from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from data_store import create_user, get_user_by_email
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("auth/signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("auth/signup.html")

        if get_user_by_email(email):
            flash("An account with that email already exists.", "error")
            return render_template("auth/signup.html")

        create_user(email=email, password_hash=generate_password_hash(password))
        flash("Your account was created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user_data = get_user_by_email(email)
        if user_data and check_password_hash(user_data["password_hash"], password):
            user = User(user_data)
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
