<div align="center">

# 🐍 Python Mini Projects

**A curated collection of practical Python applications and experiments.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/UI-Kivy-4B8BBE)](https://kivy.org/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-2ea44f)](#)

Small projects. Clear ideas. Practical code.

</div>

---

## Overview

Python Mini Projects is a growing workspace for independent Python applications, experiments, and useful tools. Each project is maintained in its own directory with a focused codebase, dedicated documentation, and its own setup instructions.

The repository currently contains two Kivy desktop applications:

| Project | Description | Main technologies |
|---|---|---|
| [**NotesApp**](NotesApp/) | A Persian-language notes manager with local storage, editing, deletion, and search. | Python, Kivy, JSON |
| [**PyCalculator**](PyCalculator/) | An offline calculator with a custom interface and restricted arithmetic evaluation. | Python, Kivy, AST |

## Repository structure

```text
Python-Mini-Projects/
├── NotesApp/
│   ├── notes_app/       # Application, screen logic, widgets, persistence
│   ├── ui/              # Kivy layout definitions
│   ├── notes.json       # Local notes data
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── PyCalculator/
│   ├── calculator_app/
│   │   ├── core/        # Arithmetic evaluation engine
│   │   └── ui/          # Calculator screen and reusable widgets
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
└── README.md
```

## Getting started

1. Clone the repository:

   ```bash
   git clone https://github.com/jsjshsbehjejwkwkaosoj828/Python-Mini-Projects.git
   cd Python-Mini-Projects
   ```

2. Choose a project and follow its own README. For example:

   ```bash
   cd PyCalculator
   python -m pip install -r requirements.txt
   python run.py
   ```

   Or launch NotesApp:

   ```bash
   cd NotesApp
   python -m pip install -r requirements.txt
   python run.py
   ```

## Design principles

- **Modular structure:** separate application startup, interface, business logic, and persistence.
- **Readable code:** keep responsibilities focused and make projects approachable.
- **Practical learning:** use each project to explore real application-development patterns.
- **Local-first where appropriate:** current applications work without requiring an online account or service.
- **Project-level documentation:** each application explains its features, dependencies, and launch process.

## Technology

- Python 3.9+
- Kivy 2.2+
- JSON for NotesApp local persistence
- Python AST for restricted calculator expression parsing

## Contributing

Ideas, bug reports, and improvements are welcome. When contributing, keep changes focused, preserve existing application behavior unless a change is intentional, and update the relevant project documentation when setup or features change.

## Project status

This repository is actively evolving. Features and project structure may change as the applications are improved. Check the README inside each project for its current architecture and instructions.

---

<div align="center">

**Built with Python 🐍**

</div>
