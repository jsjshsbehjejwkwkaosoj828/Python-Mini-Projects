"""Kivy application bootstrap for NotesApp."""
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder

from .screens import NotesRoot


class NotesApp(App):
    title = "Notes"

    def build(self):
        kv_file = Path(__file__).resolve().parent.parent / "ui" / "design.kv"
        Builder.load_file(str(kv_file))
        return NotesRoot()
