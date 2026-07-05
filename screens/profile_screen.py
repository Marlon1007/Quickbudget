from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from widgets.background_screen import BackgroundScreen
from widgets.premium_card import PremiumCard
from widgets.headers import build_back_header
from config.palette import Palette


class ProfileScreen(BackgroundScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        main_layout = BoxLayout(orientation="vertical", spacing=dp(20), padding=dp(20))
        header, _ = build_back_header("Mi Perfil", self.go_back)
        main_layout.add_widget(header)

        profile_card = PremiumCard(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(20),
            size_hint_y=None,
            height=dp(300),
        )
        avatar = MDCard(
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            radius=[dp(35)],
            md_bg_color=Palette.PRIMARY,
            pos_hint={"center_x": 0.5},
        )
        avatar.add_widget(
            MDLabel(
                text="AD",
                halign="center",
                theme_text_color="Custom",
                text_color=Palette.TEXT_ON_PRIMARY,
                bold=True,
                font_style="H5",
            )
        )

        lbl_user = MDLabel(
            text="Administrador Pro", halign="center", font_style="H6", bold=True
        )
        lbl_mail = MDLabel(
            text="admin@quickbudget.com",
            halign="center",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
        )

        logout_btn = MDRaisedButton(
            text="CERRAR SESIÓN",
            md_bg_color=Palette.DANGER,
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
            _radius=dp(10),
            on_press=self.logout,
        )

        profile_card.add_widget(avatar)
        profile_card.add_widget(lbl_user)
        profile_card.add_widget(lbl_mail)
        profile_card.add_widget(logout_btn)
        main_layout.add_widget(profile_card)
        main_layout.add_widget(Widget())
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def logout(self, instance):
        self.manager.transition = FadeTransition(duration=0.3)
        self.manager.current = "login"
