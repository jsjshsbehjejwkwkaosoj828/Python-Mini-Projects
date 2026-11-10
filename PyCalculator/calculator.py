from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
import ast
import operator
import re

# PyCalculator — a compact, modern calculator built with Kivy.
# Run: python main.py
# Dependency: kivy

Window.clearcolor = (0.035, 0.055, 0.085, 1)


class Panel(BoxLayout):
    """Rounded background panel."""
    def __init__(self, bg=(0.055, 0.085, 0.13, 1), radius=22, **kwargs):
        super().__init__(**kwargs)
        self._bg = bg
        self._radius = radius
        with self.canvas.before:
            self._color = Color(*self._bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[dp(self._radius)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size


class CalcButton(Button):
    def __init__(self, text, bg=(0.09, 0.14, 0.21, 1),
                 fg=(0.91, 0.96, 1, 1), **kwargs):
        super().__init__(text=text, **kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = fg
        self.font_size = sp(21)
        self.bold = True
        self.markup = False
        self._bg = bg
        self._radius = 17
        with self.canvas.before:
            self._shape_color = Color(*self._bg)
            self._shape = RoundedRectangle(pos=self.pos, size=self.size,
                                           radius=[dp(self._radius)])
        self.bind(pos=self._sync, size=self._sync, state=self._state_sync)

    def _sync(self, *_):
        self._shape.pos = self.pos
        self._shape.size = self.size

    def _state_sync(self, *_):
        self._shape_color.rgba = (
            tuple(min(1, c + 0.045) for c in self._bg[:3]) + (self._bg[3],)
            if self.state == "down" else self._bg
        )


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate only basic arithmetic; never uses eval()."""
    OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("Invalid number")

    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type not in self.OPS:
            raise ValueError("Unsupported operator")
        left, right = self.visit(node.left), self.visit(node.right)
        if op_type is ast.Pow and abs(right) > 8:
            raise ValueError("Exponent too large")
        result = self.OPS[op_type](left, right)
        if abs(result) > 10**15:
            raise ValueError("Result too large")
        return result

    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type not in self.OPS:
            raise ValueError("Unsupported operator")
        return self.OPS[op_type](self.visit(node.operand))

    def generic_visit(self, node):
        raise ValueError("Invalid expression")


class CalculatorUI(Panel):
    expression = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(20), dp(22)],
                         spacing=dp(16), bg=(0.035, 0.055, 0.085, 1), **kwargs)
        self.expression = ""
        self.just_calculated = False

        header = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        brand = Label(text="[b]PY[/b][color=35D6D0]CALCULATOR[/color]",
                      markup=True, halign="left", valign="middle",
                      font_size=sp(18), color=(0.9, 0.96, 1, 1))
        brand.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        version = Label(text="v1.0", size_hint_x=None, width=dp(48),
                        color=(0.42, 0.56, 0.68, 1), font_size=sp(11))
        header.add_widget(brand)
        header.add_widget(version)
        self.add_widget(header)

        display = Panel(orientation="vertical", padding=[dp(18), dp(16)],
                        spacing=dp(8), size_hint_y=None, height=dp(160),
                        bg=(0.055, 0.09, 0.14, 1), radius=22)
        self.status = Label(text="READY", size_hint_y=None, height=dp(18),
                            color=(0.25, 0.82, 0.79, 1),
                            font_size=sp(10), bold=True, halign="right")
        self.status.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.expr_label = Label(text="0", color=(0.92, 0.97, 1, 1),
                                font_size=sp(36), bold=True,
                                halign="right", valign="middle",
                                shorten=True, shorten_from="left")
        self.expr_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.preview = Label(text="PyCalculator • Kivy", color=(0.43, 0.58, 0.7, 1),
                             font_size=sp(12), halign="right")
        self.preview.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        display.add_widget(self.status)
        display.add_widget(self.expr_label)
        display.add_widget(self.preview)
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
                btn = CalcButton(label, bg=bg, fg=fg)
                btn.bind(on_release=lambda _btn, value=label: self.press(value))
                row_box.add_widget(btn)
            grid.add_widget(row_box)
        self.add_widget(grid)

        footer = Label(text="SIMPLE • FAST • OFFLINE",
                       size_hint_y=None, height=dp(18), color=(0.28, 0.42, 0.54, 1),
                       font_size=sp(9), bold=True)
        self.add_widget(footer)

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
            mapped = {"÷": "/", "×": "*", "−": "-", "%": "%"}
            char = mapped.get(key, key)
            if char == ".":
                # Avoid a second decimal point in the current number.
                current = re.split(r"[+\-*/%()]", self.expression)[-1]
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
            tree = ast.parse(safe_expr, mode="eval")
            result = SafeEvaluator().visit(tree)
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


class PyCalculatorApp(App):
    title = "PyCalculator"

    def build(self):
        root = CalculatorUI()
        return root


if __name__ == "__main__":
    PyCalculatorApp().run()
