"""Reusable visual widgets for PyCalculator."""
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class Panel(BoxLayout):
    """Rounded background panel."""
    def __init__(self, bg=(0.055, 0.085, 0.13, 1), radius=22, **kwargs):
        super().__init__(**kwargs)
        self._bg, self._radius = bg, radius
        with self.canvas.before:
            Color(*self._bg)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._rect.pos, self._rect.size = self.pos, self.size


class CalcButton(Button):
    def __init__(self, text, bg=(0.09, 0.14, 0.21, 1), fg=(0.91, 0.96, 1, 1), **kwargs):
        super().__init__(text=text, **kwargs)
        self.background_normal = self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color, self.font_size, self.bold = fg, sp(21), True
        self.markup = False
        self._bg, self._radius = bg, 17
        with self.canvas.before:
            self._shape_color = Color(*self._bg)
            self._shape = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(self._radius)])
        self.bind(pos=self._sync, size=self._sync, state=self._state_sync)

    def _sync(self, *_):
        self._shape.pos, self._shape.size = self.pos, self.size

    def _state_sync(self, *_):
        self._shape_color.rgba = (
            tuple(min(1, channel + 0.045) for channel in self._bg[:3]) + (self._bg[3],)
            if self.state == "down" else self._bg
        )
