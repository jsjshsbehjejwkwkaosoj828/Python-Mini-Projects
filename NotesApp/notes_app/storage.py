"""JSON-backed persistence for notes."""
import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "notes.json"


def load_notes():
    """Load notes safely; create an empty file on first launch."""
    if not DATA_FILE.exists():
        save_notes([])
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_notes(notes):
    """Write notes atomically to reduce the risk of JSON corruption."""
    temp_file = str(DATA_FILE) + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)
    os.replace(temp_file, DATA_FILE)
