from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from data_store import create_user, get_user_by_email, get_user_by_login, get_user_by_username
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_type = (request.form.get("login_type") or "email").strip().lower()
        login_value = (request.form.get("login_value") or "").strip()
        password = request.form.get("password") or ""

        if not login_value or not password:
            flash("Please enter your login details and password.", "error")
            return render_template("login.html", user=current_user)

        user_data = get_user_by_login(login_value, login_type)
        if user_data and check_password_hash(user_data["password_hash"], password):
            login_user(User(user_data))
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid login details or password.", "error")

    return render_template("login.html", user=current_user)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        if not email or not username or not password:
            flash("Email, username, and password are required.", "error")
            return render_template("register.html", user=current_user)

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html", user=current_user)

        if get_user_by_email(email):
            flash("An account with that email already exists.", "error")
            return render_template("register.html", user=current_user)

        if get_user_by_username(username):
            flash("That username is already taken.", "error")
            return render_template("register.html", user=current_user)

        try:
            create_user(email=email, username=username, password_hash=generate_password_hash(password))
            flash("Your account was created successfully. Please log in.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as exc:
            flash(str(exc), "error")
            return render_template("register.html", user=current_user)

    return render_template("register.html", user=current_user)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))
