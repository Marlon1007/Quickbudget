from kivymd.uix.card import MDCard
from kivy.metrics import dp


class PremiumCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 1.5
        self.radius = [dp(24)]
        self.md_bg_color = (1, 1, 1, 1)
        self.ripple_behavior = True
