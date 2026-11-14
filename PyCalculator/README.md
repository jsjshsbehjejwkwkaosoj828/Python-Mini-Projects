# PyCalculator

A compact, offline calculator with a custom dark interface, built using **Python** and **Kivy**.

## Features

- Addition, subtraction, multiplication, and division
- Modulo, decimal values, sign toggle, and backspace
- Expression preview and clear error states
- Restricted AST-based arithmetic evaluation; unrestricted Python `eval()` is not used
- Custom Kivy interface with a responsive keypad layout

## Requirements

- Python 3.9+
- Kivy 2.2+

## Run

```bash
python -m pip install -r requirements.txt
python run.py
```

## Project layout

```text
PyCalculator/
├── calculator_app/
│   ├── core/
│   │   └── evaluator.py   # Restricted arithmetic parser/evaluator
│   ├── ui/
│   │   ├── calculator.py # Calculator screen and interactions
│   │   └── widgets.py    # Reusable visual widgets
│   └── app.py            # Kivy application bootstrap
├── requirements.txt
└── run.py                # Application entry point
```

## Evaluation safety

Expressions are parsed with Python's AST and only explicitly supported numeric constants and arithmetic operators are evaluated. Other syntax is rejected. Exponents and result magnitude are bounded to reduce accidental resource-heavy calculations.

## Development

The calculation engine is independent from the Kivy interface, making it easier to maintain and test. UI components and application startup are kept in separate modules.
