import json
import os
from datetime import datetime
from uuid import uuid4

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp


APP_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_FILE = os.path.join(APP_DIR, "notes.json")
KV_FILE = os.path.join(APP_DIR, "design.ky")


def load_notes():
    """Load notes safely; create an empty file on first launch."""
    if not os.path.exists(NOTES_FILE):
        save_notes([])
        return []

    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_notes(notes):
    """Write atomically to reduce the chance of corrupting the JSON file."""
    temp_file = NOTES_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)
    os.replace(temp_file, NOTES_FILE)


class NoteCard(BoxLayout):
    note_id = StringProperty("")
    note_title = StringProperty("")
    note_preview = StringProperty("")
    note_date = StringProperty("")


class NotesRoot(BoxLayout):
    search_text = StringProperty("")
    note_count = StringProperty("0 یادداشت")
    empty_message = StringProperty("هنوز یادداشتی نداری")
    notes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes = load_notes()
        self.refresh_notes()

    def refresh_notes(self):
        container = self.ids.notes_list
        container.clear_widgets()

        query = self.search_text.strip().casefold()
        visible_notes = [
            note for note in self.notes
            if query in note.get("title", "").casefold()
            or query in note.get("body", "").casefold()
        ]

        self.note_count = f"{len(self.notes)} یادداشت"
        self.empty_message = (
            "نتیجه‌ای پیدا نشد" if query else "هنوز یادداشتی نداری"
        )

        for note in sorted(
            visible_notes,
            key=lambda item: item.get("updated_at", ""),
            reverse=True
        ):
            body = note.get("body", "").strip().replace("\n", " ")
            preview = body[:105] + ("…" if len(body) > 105 else "")
            card = NoteCard(
                note_id=note.get("id", ""),
                note_title=note.get("title", "بدون عنوان"),
                note_preview=preview or "یادداشت خالی",
                note_date=self.format_date(note.get("updated_at", "")),
            )
            container.add_widget(card)

        self.ids.empty_state.opacity = 1 if not visible_notes else 0
        self.ids.empty_state.disabled = bool(visible_notes)

    @staticmethod
    def format_date(value):
        try:
            date = datetime.fromisoformat(value)
            return date.strftime("%Y/%m/%d  •  %H:%M")
        except (ValueError, TypeError):
            return "بدون تاریخ"

    def on_search(self, value):
        self.search_text = value
        self.refresh_notes()

    def open_new_note(self):
        self.open_editor()

    def open_editor(self, note_id=None):
        note = next((n for n in self.notes if n.get("id") == note_id), None)
        editor = NoteEditor(
            note_id=note_id or "",
            title_text=note.get("title", "") if note else "",
            body_text=note.get("body", "") if note else "",
            is_edit=bool(note),
        )
        popup = Popup(
            title="",
            content=editor,
            size_hint=(0.94, 0.86),
            auto_dismiss=False,
            separator_height=0,
            background="",
            background_color=(0.075, 0.09, 0.14, 1),
        )
        editor.popup = popup
        popup.open()

    def save_note(self, note_id, title, body, popup):
        title = title.strip()
        body = body.strip()

        if not title and not body:
            popup.dismiss()
            return

        if not title:
            title = "بدون عنوان"

        now = datetime.now().isoformat(timespec="minutes")
        existing = next((n for n in self.notes if n.get("id") == note_id), None)

        if existing:
            existing["title"] = title
            existing["body"] = body
            existing["updated_at"] = now
        else:
            self.notes.append({
                "id": str(uuid4()),
                "title": title,
                "body": body,
                "created_at": now,
                "updated_at": now,
            })

        save_notes(self.notes)
        popup.dismiss()
        self.refresh_notes()

    def confirm_delete(self, note_id):
        note = next((n for n in self.notes if n.get("id") == note_id), None)
        if not note:
            return

        content = BoxLayout(orientation="vertical", spacing=dp(14), padding=dp(18))
        content.add_widget(Label(
            text="این یادداشت برای همیشه حذف شود؟",
            color=(0.88, 0.91, 0.96, 1),
            font_size="15sp",
            halign="center",
            valign="middle",
        ))
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(10))
        popup = Popup(
            title="حذف یادداشت",
            content=content,
            size_hint=(0.82, None),
            height=dp(175),
            separator_color=(0.25, 0.31, 0.42, 1),
        )

        cancel = Button(text="انصراف", background_normal="", background_color=(0.18, 0.22, 0.30, 1))
        delete = Button(text="حذف", background_normal="", background_color=(0.78, 0.25, 0.31, 1))
        cancel.bind(on_release=popup.dismiss)

        def do_delete(*_):
            self.notes = [n for n in self.notes if n.get("id") != note_id]
            save_notes(self.notes)
            popup.dismiss()
            self.refresh_notes()

        delete.bind(on_release=do_delete)
        actions.add_widget(cancel)
        actions.add_widget(delete)
        content.add_widget(actions)
        popup.open()


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


class NotesApp(App):
    title = "Notes"

    def build(self):
        Builder.load_file(KV_FILE)
        return NotesRoot()


if __name__ == "__main__":
    NotesApp().run()
