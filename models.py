from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["id"])
        self.email = user_data["email"]
        self.username = user_data.get("username") or self.email
        self.password_hash = user_data["password_hash"]
        self.created_at = user_data.get("created_at")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
