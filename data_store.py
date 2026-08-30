import json
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

FILE_DEFAULTS = {
    "users.json": [],
    "feedback_usage.json": {},
    "writing_submissions.json": [],
    "sessions.json": {},
    "reading_content.json": [],
    "listening_content.json": [],
    "writing_prompts.json": [],
    "speaking_cuecards.json": [],
}


def ensure_data_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for file_name, default_value in FILE_DEFAULTS.items():
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            file_path.write_text(json.dumps(default_value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(file_name, default):
    path = DATA_DIR / file_name
    if not path.exists():
        ensure_data_files()
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return default


def write_json(file_name, payload):
    path = DATA_DIR / file_name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def get_all_users():
    return read_json("users.json", [])


def get_user_by_id(user_id):
    for user in get_all_users():
        if str(user.get("id")) == str(user_id):
            return user
    return None


def get_user_by_email(email):
    normalized_email = (email or "").strip().lower()
    for user in get_all_users():
        if str(user.get("email", "")).strip().lower() == normalized_email:
            return user
    return None


def get_user_by_username(username):
    normalized_username = (username or "").strip().lower()
    for user in get_all_users():
        if str(user.get("username", "")).strip().lower() == normalized_username:
            return user
    return None


def get_user_by_login(identifier, login_type="email"):
    value = (identifier or "").strip()
    if not value:
        return None

    if login_type == "username":
        return get_user_by_username(value)
    return get_user_by_email(value)


def create_user(email, username, password_hash):
    users = get_all_users()
    normalized_email = (email or "").strip().lower()
    normalized_username = (username or "").strip()

    if not normalized_username:
        raise ValueError("Username is required.")

    normalized_username = normalized_username.lower()

    if any(str(user.get("email", "")).strip().lower() == normalized_email for user in users):
        raise ValueError("An account with that email already exists.")

    if any(str(user.get("username", "")).strip().lower() == normalized_username for user in users):
        raise ValueError("That username is already taken.")

    user_id = max((user.get("id", 0) for user in users), default=0) + 1
    user = {
        "id": user_id,
        "email": normalized_email,
        "username": normalized_username,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    users.append(user)
    write_json("users.json", users)
    return user
