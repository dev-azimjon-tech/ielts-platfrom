import importlib.util
import sys
import types
from pathlib import Path

from flask import Blueprint, render_template

from data_store import read_json

listening_bp = Blueprint("listening", __name__)


@listening_bp.route("/listening")
def listening_page():
    tasks = read_json("listening_content.json", [])
    return render_template("listening.html", tasks=tasks)
