from kivymd.uix.label import MDLabel, MDIcon
from kivy.properties import NumericProperty


class CurrencyLabel(MDLabel):
    amount = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bold = True
        self.update_text()
        self.bind(amount=self.update_text)

    def update_text(self, *args):
        self.text = f"${self.amount:,.2f}"