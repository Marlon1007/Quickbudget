from kivymd.uix.list import OneLineIconListItem
from config.palette import Palette
from kivymd.uix.button import (
    MDIconButton,
)


class ConceptItem(OneLineIconListItem):
    def __init__(self, icon_name, **kwargs):
        super().__init__(**kwargs)
        self.ids._left_container.add_widget(
            MDIconButton(icon=icon_name, icon_color=Palette.PRIMARY)
        )
