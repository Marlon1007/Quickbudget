from kivy.uix.boxlayout import BoxLayout
from config.palette import Palette
from kivymd.uix.button import (
    MDIconButton,
)
from kivymd.uix.label import MDLabel
from kivy.metrics import dp


def build_back_header(title_text, on_back, height=dp(55)):
    """Build a reusable horizontal header with a back button and a title label."""
    header = BoxLayout(
        orientation="horizontal", size_hint_y=None, height=height, spacing=dp(10)
    )
    back_btn = MDIconButton(
        icon="arrow-left", icon_color=Palette.PRIMARY, on_press=on_back
    )
    title_label = MDLabel(
        text=title_text,
        font_style="H5",
        bold=True,
        theme_text_color="Custom",
        text_color=Palette.TEXT_PRIMARY,
    )
    header.add_widget(back_btn)
    header.add_widget(title_label)
    return header, title_label
