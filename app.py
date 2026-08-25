import os

from flask import Flask, render_template
from flask_login import LoginManager

from auth import auth_bp
from dashboard import dashboard_bp
from data_store import ensure_data_files, get_user_by_id
from models import User


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["JSON_SORT_KEYS"] = False
    ensure_data_files()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(user_data)
        return None

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route('/reading')
    def reading():
        return render_template('reading.html')

    @app.route('/listening')
    def listening():
        return render_template('listening.html')

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
