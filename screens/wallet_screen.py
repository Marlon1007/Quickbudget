from kivymd.app import MDApp
from kivymd.uix.button import (
    MDRaisedButton,
    MDFlatButton,
)
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from datetime import datetime
from kivy.uix.scrollview import ScrollView

from widgets.background_screen import BackgroundScreen
from widgets.currency_label import CurrencyLabel
from widgets.premium_card import PremiumCard
from widgets.headers import build_back_header
from config.palette import Palette


class WalletScreen(BackgroundScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.recharge_dialog = None

        self.main_layout = BoxLayout(
            orientation="vertical", spacing=dp(15), padding=dp(20)
        )

        header, _ = build_back_header("Mi Billetera", self.go_back)
        self.main_layout.add_widget(header)

        self.balance_card = PremiumCard(
            size_hint=(1, None), height=dp(105), padding=dp(20)
        )
        balance_layout = BoxLayout(orientation="vertical", spacing=dp(2))
        balance_label = MDLabel(
            text="Saldo en cuenta",
            theme_text_color="Custom",
            text_color=Palette.TEXT_SECONDARY,
            font_style="Subtitle2",
        )
        self.balance_amount = CurrencyLabel(
            amount=0.0,
            theme_text_color="Custom",
            text_color=Palette.PRIMARY,
            font_style="H5",
            bold=True,
        )
        balance_layout.add_widget(balance_label)
        balance_layout.add_widget(self.balance_amount)
        self.balance_card.add_widget(balance_layout)
        self.main_layout.add_widget(self.balance_card)

        recharge_btn = MDRaisedButton(
            text="+ RECARGAR DINERO",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=Palette.PRIMARY,
            _radius=dp(14),
            on_press=self.show_recharge_dialog,
        )
        self.main_layout.add_widget(recharge_btn)

        search_section = BoxLayout(
            orientation="vertical", spacing=dp(6), size_hint_y=None, height=dp(90)
        )
        history_title = MDLabel(
            text="Historial de Transacciones",
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Custom",
            text_color=Palette.TEXT_PRIMARY,
        )

        self.search_input = MDTextField(
            hint_text="Buscar por monto o fecha...",
            size_hint_x=1,
            mode="rectangle",
            line_color_focus=Palette.PRIMARY,
            on_text_validate=self.filter_history,
        )
        search_section.add_widget(history_title)
        search_section.add_widget(self.search_input)
        self.main_layout.add_widget(search_section)

        self.scroll_view = ScrollView(do_scroll_x=False)
        self.history_list_layout = BoxLayout(
            orientation="vertical", spacing=dp(10), size_hint_y=None
        )
        self.history_list_layout.bind(
            minimum_height=self.history_list_layout.setter("height")
        )
        self.scroll_view.add_widget(self.history_list_layout)

        self.main_layout.add_widget(self.scroll_view)
        self.add_widget(self.main_layout)

    def update_wallet_ui(self):
        app = MDApp.get_running_app()
        self.balance_amount.amount = app.state.total_budget
        self.update_history_list()

    def show_recharge_dialog(self, instance):
        self.recharge_input = MDTextField(
            hint_text="Monto a depositar ($)", input_filter="float"
        )
        self.recharge_dialog = MDDialog(
            title="Centro de Recarga",
            type="custom",
            content_cls=self.recharge_input,
            buttons=[
                MDFlatButton(
                    text="CANCELAR", on_release=lambda x: self.recharge_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="EFECTUAR",
                    md_bg_color=Palette.ACCENT,
                    _radius=dp(8),
                    on_release=self.process_recharge,
                ),
            ],
        )
        self.recharge_dialog.open()

    def process_recharge(self, instance):
        if self.recharge_input.text.strip():
            amount = float(self.recharge_input.text)
            app = MDApp.get_running_app()
            app.state.total_budget += amount

            app.state.expense_history.append(
                {
                    "amount": amount,
                    "concept": "Recarga Exitosa",
                    "category": "Depósito",
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "is_expense": False,
                }
            )

            self.balance_amount.amount = app.state.total_budget
            self.update_history_list()
        self.recharge_dialog.dismiss()

    def update_history_list(self, filtered_history=None):
        self.history_list_layout.clear_widgets()
        app = MDApp.get_running_app()
        history = (
            filtered_history if filtered_history is not None else app.state.expense_history
        )

        if not history:
            lbl = MDLabel(
                text="No hay movimientos registrados.",
                halign="center",
                theme_text_color="Custom",
                text_color=Palette.TEXT_SECONDARY,
                size_hint_y=None,
                height=dp(40),
            )
            self.history_list_layout.add_widget(lbl)
            return

        home_screen = self.manager.get_screen("home")
        for item in reversed(history):
            self.history_list_layout.add_widget(home_screen.create_item_card(item))

    def filter_history(self, instance=None):
        app = MDApp.get_running_app()
        query = self.search_input.text.strip().lower()
        if not query:
            self.update_history_list()
            return
        filtered = [
            i
            for i in app.state.expense_history
            if query in i["date"]
            or query in f"{i['amount']:.2f}"
            or query in i["concept"].lower()
        ]
        self.update_history_list(filtered)

    def go_back(self, instance):
        self.search_input.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "home"
        self.manager.get_screen("home").refresh_ui()
