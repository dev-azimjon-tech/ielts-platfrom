import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import fcntl

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


def _lock_path_for(file_path: Path) -> Path:
    return file_path.parent / f".{file_path.name}.lock"


@contextmanager
def file_lock(file_path: Path):
    lock_path = _lock_path_for(file_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+b") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def atomic_write_json(file_path: Path, payload):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(file_path.parent),
        prefix=f".{file_path.name}.",
        suffix=".tmp",
        delete=False,
    ) as tmp_file:
        json.dump(payload, tmp_file, ensure_ascii=False, indent=2)
        tmp_file.write("\n")
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_path = tmp_file.name
    os.replace(tmp_path, file_path)


def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, default in FILE_DEFAULTS.items():
        path = DATA_DIR / filename
        if not path.exists():
            atomic_write_json(path, default)


def read_json(file_name: str, default):
    path = DATA_DIR / file_name
    if not path.exists():
        atomic_write_json(path, default)
    with file_lock(path):
        try:
            with open(path, "r", encoding="utf-8") as file_handle:
                return json.load(file_handle)
        except json.JSONDecodeError:
            return default


def write_json(file_name: str, payload):
    path = DATA_DIR / file_name
    with file_lock(path):
        atomic_write_json(path, payload)


def get_all_users():
    return read_json("users.json", [])


def get_user_by_id(user_id):
    for user in get_all_users():
        if str(user["id"]) == str(user_id):
            return user
    return None


def get_user_by_email(email: str):
    normalized_email = (email or "").strip().lower()
    for user in get_all_users():
        if str(user.get("email", "")).strip().lower() == normalized_email:
            return user
    return None


def create_user(email: str, password_hash: str):
    users = get_all_users()
    normalized_email = (email or "").strip().lower()

    if any(str(user.get("email", "")).strip().lower() == normalized_email for user in users):
        raise ValueError("An account with that email already exists.")

    user_id = max((user.get("id", 0) for user in users), default=0) + 1
    user = {
        "id": user_id,
        "email": normalized_email,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    users.append(user)
    write_json("users.json", users)
    return user
