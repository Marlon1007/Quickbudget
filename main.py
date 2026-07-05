from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.expense_screen import ExpenseScreen
from screens.wallet_screen import WalletScreen
from screens.profile_screen import ProfileScreen
from models.app_state import AppState
from kivy.core.window import Window
from kivy.utils import platform

if platform != "android":
    Window.size = (375, 667)


class QuickBudgetApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = AppState()

    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ExpenseScreen(name="expense"))
        sm.add_widget(WalletScreen(name="wallet"))
        sm.add_widget(ProfileScreen(name="profile"))

        return sm


QuickBudgetApp().run()
