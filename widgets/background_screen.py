from config.palette import Palette
from kivy.uix.screenmanager import Screen
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle


class BackgroundScreen(Screen):
    """Base screen that draws a flat background color behind its content."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*Palette.BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
