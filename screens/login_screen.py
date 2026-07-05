from widgets.background_screen import BackgroundScreen
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from config.palette import Palette
from kivy.uix.image import Image
from kivy.metrics import dp


class LoginScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(orientation="vertical", padding=dp(35), spacing=dp(20))
        main_layout.add_widget(Widget(size_hint_y=0.2))

        logo = Image(
            source="assets/Logo.png",
            size_hint=(None, None),
            size=(dp(130), dp(130)),
            pos_hint={"center_x": 0.5},
        )
        main_layout.add_widget(logo)

        self.label = MDLabel(
            text="Quick Budget",
            halign="center",
            font_style="H4",
            bold=True,
            theme_text_color="Custom",
            text_color=Palette.PRIMARY,
            size_hint_y=None,
            height=dp(50),
        )
        main_layout.add_widget(self.label)
        main_layout.add_widget(Widget(size_hint_y=0.1))

        self.user = MDTextField(
            hint_text="Usuario",
            mode="rectangle",
            size_hint_x=1,
            pos_hint={"center_x": 0.5},
        )
        self.password = MDTextField(
            hint_text="Contraseña",
            password=True,
            mode="rectangle",
            size_hint_x=1,
            pos_hint={"center_x": 0.5},
        )

        main_layout.add_widget(self.user)
        main_layout.add_widget(self.password)
        main_layout.add_widget(Widget(size_hint_y=0.1))

        self.button = MDRaisedButton(
            text="Ingresar a Quick Budget",
            pos_hint={"center_x": 0.5},
            md_bg_color=Palette.PRIMARY,
            size_hint_x=1,
            height=dp(55),
            _radius=dp(12),
            on_press=lambda x: self.login(),
        )
        main_layout.add_widget(self.button)
        main_layout.add_widget(Widget(size_hint_y=0.3))
        self.add_widget(main_layout)

    def login(self):
        if self.user.text and self.password.text:
            self.manager.transition = FadeTransition(duration=0.3)
            self.manager.current = "home"
            self.manager.get_screen("home").refresh_ui()
