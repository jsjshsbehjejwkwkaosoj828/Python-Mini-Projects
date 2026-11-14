# NotesApp

A lightweight Persian-language desktop notes application built with **Python** and **Kivy**. Notes are stored locally in JSON, so the app works offline and does not require an account or a remote service.

## Features

- Create, edit, and delete notes
- Search note titles and content
- Sort notes by most recently updated
- Local JSON persistence with atomic file replacement
- Dark, responsive Kivy interface
- Persian interface text

## Requirements

- Python 3.9+
- Kivy 2.2+

## Run

From this directory, install the dependency and launch the app:

```bash
python -m pip install -r requirements.txt
python run.py
```

## Project layout

```text
NotesApp/
├── notes_app/
│   ├── __init__.py
│   ├── app.py          # Kivy application bootstrap
│   ├── screens.py      # Note list, search, editing and deletion flows
│   ├── storage.py      # JSON persistence
│   └── widgets.py      # Reusable note widgets
├── ui/
│   └── design.kv       # Kivy interface declarations
├── notes.json          # Local note data (created when needed)
├── requirements.txt
└── run.py              # Application entry point
```

## Data and privacy

All notes remain in the local `notes.json` file. The application does not implement cloud sync, user accounts, or network transmission. Back up this file to preserve your notes.

## Development

The code is separated by responsibility: persistence lives in `storage.py`, reusable components in `widgets.py`, screen behavior in `screens.py`, and startup configuration in `app.py`. The Kivy layout is maintained separately in `ui/design.kv`.
