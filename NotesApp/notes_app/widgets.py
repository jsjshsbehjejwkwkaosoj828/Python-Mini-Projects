"""Reusable Kivy widgets used by the notes interface."""
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout


class NoteCard(BoxLayout):
    note_id = StringProperty("")
    note_title = StringProperty("")
    note_preview = StringProperty("")
    note_date = StringProperty("")


class NoteEditor(BoxLayout):
    note_id = StringProperty("")
    title_text = StringProperty("")
    body_text = StringProperty("")
    is_edit = BooleanProperty(False)
    popup = None

    def save(self):
        root = App.get_running_app().root
        root.save_note(
            self.note_id,
            self.ids.title_input.text,
            self.ids.body_input.text,
            self.popup,
        )
