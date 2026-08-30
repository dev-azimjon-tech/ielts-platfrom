import importlib.util
import sys
import types
from pathlib import Path

from flask import Blueprint, render_template

from data_store import read_json

reading_bp = Blueprint("reading", __name__)


@reading_bp.route("/reading")
def reading_page():
    tasks = read_json("reading_content.json", [])
    return render_template("reading.html", tasks=tasks)
