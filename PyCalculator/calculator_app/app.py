"""Kivy application bootstrap for PyCalculator."""
from kivy.app import App
from kivy.core.window import Window

from .ui.calculator import CalculatorUI


class PyCalculatorApp(App):
    title = "PyCalculator"

    def build(self):
        Window.clearcolor = (0.035, 0.055, 0.085, 1)
        return CalculatorUI()
