from kivymd.app import MDApp
from kivymd.uix.button import (
    MDIconButton,
    MDFlatButton,
)
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty

from widgets.background_screen import BackgroundScreen
from widgets.premium_card import PremiumCard
from widgets.currency_label import CurrencyLabel
from config.constants import CATEGORY_ICONS
from config.palette import Palette


class HomeScreen(BackgroundScreen):
    total_budget = NumericProperty(0.0)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.float_layout = MDFloatLayout()
        self.scroll_view = ScrollView(
            size_hint=(1, 0.88), pos_hint={"top": 1}, do_scroll_x=False
        )
        self.main_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=(dp(20), dp(20), dp(20), dp(20)),
            size_hint_y=None,
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter("height"))

        header_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(55), spacing=dp(12)
        )
        profile_card = MDCard(
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            radius=[dp(22.5)],
            md_bg_color=Palette.PRIMARY,
        )
        profile_label = MDLabel(
            text="AD",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=Palette.TEXT_ON_PRIMARY,
            bold=True,
        )
        profile_card.add_widget(profile_label)

        welcome_layout = BoxLayout(orientation="vertical", spacing=0)
        welcome_label = MDLabel(
            text="Hola Admin",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=Palette.TEXT_PRIMARY,
        )
        subtitle_label = MDLabel(
            text="Bienvenido a Quick Budget",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
            font_style="Subtitle2",
        )
        welcome_layout.add_widget(welcome_label)
        welcome_layout.add_widget(subtitle_label)

        budget_icon_btn = MDIconButton(
            icon="cash-plus",
            icon_color=Palette.PRIMARY,
            icon_size=dp(28),
            pos_hint={"center_y": 0.5},
            on_press=self.go_to_wallet,
        )

        header_layout.add_widget(profile_card)
        header_layout.add_widget(welcome_layout)
        header_layout.add_widget(budget_icon_btn)
        self.main_layout.add_widget(header_layout)

        self.balance_card = PremiumCard(
            size_hint=(1, None), height=dp(110), padding=dp(20)
        )
        self.balance_card.bind(on_release=self.go_to_wallet)

        balance_texts = BoxLayout(orientation="vertical", spacing=dp(2))
        balance_label = MDLabel(
            text="Saldo Disponible",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
            font_style="Subtitle2",
        )
        self.label_remaining = CurrencyLabel(
            amount=self.total_budget,
            theme_text_color="Custom",
            text_color=Palette.ACCENT,
            font_style="H4",
        )
        self.bind(total_budget=self.label_remaining.setter("amount"))

        balance_texts.add_widget(balance_label)
        balance_texts.add_widget(self.label_remaining)
        self.balance_card.add_widget(balance_texts)
        self.main_layout.add_widget(self.balance_card)

        self.spending_card = PremiumCard(
            size_hint=(1, None), height=dp(55), padding=dp(15)
        )
        spending_layout = BoxLayout(orientation="horizontal", spacing=dp(10))
        self.spending_text = MDLabel(
            text="Gastado este mes:",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
            font_style="Subtitle2",
        )
        self.spending_amount = CurrencyLabel(
            amount=0.0,
            halign="right",
            theme_text_color="Custom",
            text_color=Palette.DANGER,
            font_style="Subtitle1",
            bold=True,
        )
        spending_layout.add_widget(self.spending_text)
        spending_layout.add_widget(self.spending_amount)
        self.spending_card.add_widget(spending_layout)
        self.main_layout.add_widget(self.spending_card)

        categories_label = MDLabel(
            text="Categorías",
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(25),
            theme_text_color="Custom",
            text_color=Palette.TEXT_PRIMARY,
        )
        self.main_layout.add_widget(categories_label)

        categories_container = AnchorLayout(
            anchor_x="center", size_hint_y=None, height=dp(90)
        )
        actions_layout = BoxLayout(
            orientation="horizontal", spacing=dp(14), size_hint_x=None
        )
        actions_layout.bind(minimum_width=actions_layout.setter("width"))

        categories = [
            ("Snack/Café", CATEGORY_ICONS["Snack/Café"], (254 / 255, 154 / 255, 0, 1)),
            (
                "Transporte",
                CATEGORY_ICONS["Transporte"],
                (43 / 255, 127 / 255, 255 / 255, 1),
            ),
            ("Ocio", CATEGORY_ICONS["Ocio"], (173 / 255, 70 / 255, 255 / 255, 1)),
            ("Otros", CATEGORY_ICONS["Otros"], (117 / 255, 117 / 255, 117 / 255, 1)),
        ]

        for category_name, icon, color in categories:
            item_box = BoxLayout(
                orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(68)
            )
            icon_card = MDCard(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                radius=[dp(25)],
                md_bg_color=(1, 1, 1, 1),
                elevation=1,
                pos_hint={"center_x": 0.5},
            )
            btn = MDIconButton(
                icon=icon,
                icon_color=color,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_press=lambda x, c=category_name: self.next_by_name(c),
            )
            icon_card.add_widget(btn)

            lbl = MDLabel(
                text=category_name.split("/")[0],
                halign="center",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=Palette.TEXT_PRIMARY,
            )
            item_box.add_widget(icon_card)
            item_box.add_widget(lbl)
            actions_layout.add_widget(item_box)

        categories_container.add_widget(actions_layout)
        self.main_layout.add_widget(categories_container)

        history_header = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(35)
        )
        history_label = MDLabel(
            text="Movimientos",
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Custom",
            text_color=Palette.TEXT_PRIMARY,
        )
        wallet_link = MDFlatButton(
            text="Ver Billetera", text_color=Palette.PRIMARY, on_press=self.go_to_wallet
        )
        history_header.add_widget(history_label)
        history_header.add_widget(wallet_link)
        self.main_layout.add_widget(history_header)

        self.expense_list_layout = BoxLayout(
            orientation="vertical", spacing=dp(10), size_hint_y=None
        )
        self.expense_list_layout.bind(
            minimum_height=self.expense_list_layout.setter("height")
        )
        self.main_layout.add_widget(self.expense_list_layout)

        self.scroll_view.add_widget(self.main_layout)
        self.float_layout.add_widget(self.scroll_view)

        bottom_nav = MDCard(
            size_hint=(1, None),
            height=dp(65),
            pos_hint={"y": 0},
            elevation=4,
            radius=[dp(20), dp(20), 0, 0],
            md_bg_color=(1, 1, 1, 1),
        )
        nav_anchor = AnchorLayout(
            anchor_x="center", anchor_y="center", padding=(0, dp(2))
        )
        nav_layout = BoxLayout(
            orientation="horizontal", spacing=dp(90), size_hint_x=None
        )
        nav_layout.bind(minimum_width=nav_layout.setter("width"))

        nav_items = [("home", "Inicio", "home"), ("account", "Tu Perfil", "profile")]
        for icon, label_text, screen_name in nav_items:
            is_active = label_text == "Inicio"
            item_box = BoxLayout(
                orientation="vertical", spacing=0, size_hint_x=None, width=dp(60)
            )
            btn = MDIconButton(
                icon=icon,
                icon_color=Palette.PRIMARY if is_active else Palette.TEXT_SECONDARY,
                pos_hint={"center_x": 0.5},
                on_press=lambda x, s=screen_name: (
                    self.navigate_to(s) if s != "home" else None
                ),
            )
            lbl = MDLabel(
                text=label_text,
                halign="center",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=Palette.PRIMARY if is_active else Palette.TEXT_SECONDARY,
            )
            item_box.add_widget(btn)
            item_box.add_widget(lbl)
            nav_layout.add_widget(item_box)

        nav_anchor.add_widget(nav_layout)
        bottom_nav.add_widget(nav_anchor)
        self.float_layout.add_widget(bottom_nav)
        self.add_widget(self.float_layout)

    def refresh_ui(self):
        app = MDApp.get_running_app()
        self.total_budget = app.state.total_budget
        self.spending_amount.amount = app.state.total_expenses

        self.expense_list_layout.clear_widgets()
        for exp in reversed(app.state.expense_history[-4:]):
            self.expense_list_layout.add_widget(self.create_item_card(exp))

    def navigate_to(self, screen_name):
        self.manager.transition.direction = "left"
        self.manager.current = screen_name

    def go_to_wallet(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "wallet"
        self.manager.get_screen("wallet").update_wallet_ui()

    def next_by_name(self, category_name):
        expense_screen = self.manager.get_screen("expense")
        expense_screen.set_category(category_name)
        self.manager.transition.direction = "left"
        self.manager.current = "expense"

    def create_item_card(self, item):
        card = PremiumCard(size_hint=(1, None), height=dp(68), padding=(dp(14), dp(6)))
        layout = BoxLayout(orientation="horizontal", spacing=dp(12))

        icon_container = MDCard(
            size_hint=(None, None),
            size=(dp(42), dp(42)),
            radius=[dp(21)],
            md_bg_color=Palette.PRIMARY_LIGHT,
            elevation=0,
            pos_hint={"center_y": 0.5},
        )

        icon_name = (
            "plus"
            if not item["is_expense"]
            else CATEGORY_ICONS.get(item["category"], "cash")
        )

        icon_widget = MDIconButton(
            icon=icon_name,
            icon_color=Palette.PRIMARY,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        icon_container.add_widget(icon_widget)

        text_box = BoxLayout(orientation="vertical", pos_hint={"center_y": 0.5})
        lbl_concept = MDLabel(text=item["concept"], font_style="Subtitle2", bold=True)
        lbl_date = MDLabel(
            text=item["date"],
            font_style="Caption",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
        )
        text_box.add_widget(lbl_concept)
        text_box.add_widget(lbl_date)

        prefix = "-" if item["is_expense"] else "+"
        color = Palette.DANGER if item["is_expense"] else Palette.ACCENT
        lbl_amount = CurrencyLabel(
            amount=item["amount"],
            halign="right",
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Custom",
            text_color=color,
            pos_hint={"center_y": 0.5},
        )
        lbl_amount.text = prefix + lbl_amount.text

        layout.add_widget(icon_container)
        layout.add_widget(text_box)
        layout.add_widget(lbl_amount)
        card.add_widget(layout)
        return card
