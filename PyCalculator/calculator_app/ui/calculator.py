"""Calculator screen and keypad interaction logic."""
import re

from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from ..core.evaluator import evaluate
from .widgets import Panel, CalcButton


class CalculatorUI(Panel):
    expression = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(20), dp(22)],
                         spacing=dp(16), bg=(0.035, 0.055, 0.085, 1), **kwargs)
        self.expression = ""
        self.just_calculated = False
        header = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        brand = Label(text="[b]PY[/b][color=35D6D0]CALCULATOR[/color]", markup=True,
                      halign="left", valign="middle", font_size=sp(18), color=(0.9, 0.96, 1, 1))
        brand.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        version = Label(text="v1.0", size_hint_x=None, width=dp(48),
                        color=(0.42, 0.56, 0.68, 1), font_size=sp(11))
        header.add_widget(brand)
        header.add_widget(version)
        self.add_widget(header)

        display = Panel(orientation="vertical", padding=[dp(18), dp(16)], spacing=dp(8),
                        size_hint_y=None, height=dp(160), bg=(0.055, 0.09, 0.14, 1), radius=22)
        self.status = Label(text="READY", size_hint_y=None, height=dp(18),
                            color=(0.25, 0.82, 0.79, 1), font_size=sp(10), bold=True, halign="right")
        self.status.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.expr_label = Label(text="0", color=(0.92, 0.97, 1, 1), font_size=sp(36), bold=True,
                                halign="right", valign="middle", shorten=True, shorten_from="left")
        self.expr_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.preview = Label(text="PyCalculator • Kivy", color=(0.43, 0.58, 0.7, 1),
                             font_size=sp(12), halign="right")
        self.preview.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        for widget in (self.status, self.expr_label, self.preview):
            display.add_widget(widget)
        self.add_widget(display)

        keys = [
            [("AC", "action"), ("⌫", "action"), ("%", "operator"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("±", "action"), ("0", "number"), (".", "number"), ("=", "equals")],
        ]
        grid = BoxLayout(orientation="vertical", spacing=dp(10))
        for row in keys:
            row_box = BoxLayout(spacing=dp(10))
            for label, kind in row:
                if kind == "operator":
                    bg, fg = (0.08, 0.22, 0.28, 1), (0.34, 0.91, 0.87, 1)
                elif kind == "equals":
                    bg, fg = (0.12, 0.78, 0.72, 1), (0.025, 0.09, 0.12, 1)
                elif kind == "action":
                    bg, fg = (0.14, 0.19, 0.27, 1), (0.72, 0.84, 0.92, 1)
                else:
                    bg, fg = (0.075, 0.115, 0.17, 1), (0.91, 0.96, 1, 1)
                button = CalcButton(label, bg=bg, fg=fg)
                button.bind(on_release=lambda _button, value=label: self.press(value))
                row_box.add_widget(button)
            grid.add_widget(row_box)
        self.add_widget(grid)
        self.add_widget(Label(text="SIMPLE • FAST • OFFLINE", size_hint_y=None, height=dp(18),
                              color=(0.28, 0.42, 0.54, 1), font_size=sp(9), bold=True))

    def refresh(self):
        self.expr_label.text = self.expression or "0"

    def press(self, key):
        if key == "AC":
            self.expression = ""
            self.status.text = "CLEARED"
            self.preview.text = "PyCalculator • Kivy"
            self.just_calculated = False
        elif key == "⌫":
            self.expression = self.expression[:-1]
            self.status.text = "EDITING"
            self.just_calculated = False
        elif key == "=":
            self.calculate()
            return
        elif key == "±":
            if self.expression:
                self.expression = f"-({self.expression})"
            self.status.text = "SIGN CHANGED"
            self.just_calculated = False
        else:
            if self.just_calculated and (key.isdigit() or key == "."):
                self.expression = ""
            self.just_calculated = False
            char = {"÷": "/", "×": "*", "−": "-", "%": "%"}.get(key, key)
            if char == ".":
                current = re.split(r"[+\\-*/%()]", self.expression)[-1]
                if "." in current:
                    return
                if not current:
                    char = "0."
            if char in "+-*/%":
                if not self.expression and char != "-":
                    return
                if self.expression and self.expression[-1] in "+-*/%":
                    self.expression = self.expression[:-1]
            self.expression += char
            self.status.text = "EDITING"
        self.refresh()

    def calculate(self):
        if not self.expression:
            return
        safe_expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        try:
            result = evaluate(safe_expr)
            if isinstance(result, float):
                result_text = f"{result:.10f}".rstrip("0").rstrip(".")
            else:
                result_text = str(result)
            self.preview.text = f"= {result_text}"
            self.expression = result_text
            self.status.text = "COMPLETE"
            self.just_calculated = True
        except ZeroDivisionError:
            self.status.text = "MATH ERROR"
            self.preview.text = "Cannot divide by zero"
        except (SyntaxError, ValueError, OverflowError):
            self.status.text = "INVALID INPUT"
            self.preview.text = "Check your expression"
        self.refresh()
