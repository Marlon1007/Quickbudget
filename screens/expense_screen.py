from kivymd.app import MDApp
from kivymd.uix.button import (
    MDRaisedButton,
    MDRectangleFlatIconButton,
    MDFlatButton,
)
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from datetime import datetime
from kivy.uix.scrollview import ScrollView

from widgets.background_screen import BackgroundScreen
from widgets.premium_card import PremiumCard
from widgets.concept_item import ConceptItem
from widgets.headers import build_back_header
from config.constants import CATEGORY_ICONS, PREDEFINED_CONCEPTS
from config.palette import Palette


class ExpenseScreen(BackgroundScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.category_name = ""
        self.selected_concept = ""
        self.concept_dialog = None

        main_layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))

        header, self.title_label = build_back_header("Nuevo Gasto", self.go_back)
        main_layout.add_widget(header)

        # Card height fits all dynamically swapped elements
        self.expense_card = PremiumCard(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(25),
            size_hint_y=None,
            height=dp(360),
        )

        self.amount_input = MDTextField(
            hint_text="Monto ($)", input_filter="float", mode="rectangle"
        )

        # Dropdown-style selector for predefined concepts
        self.concept_picker_btn = MDRectangleFlatIconButton(
            text="Seleccionar Concepto / Motivo",
            icon="format-list-bulleted",
            line_color=Palette.PRIMARY,
            text_color=Palette.TEXT_PRIMARY,
            icon_color=Palette.PRIMARY,
            size_hint_x=1,
            height=dp(52),
            on_press=self.open_concept_selector,
        )

        # Free-text input used for the "Otros" category
        self.custom_concept_input = MDTextField(
            hint_text="Concepto / Motivo personalizado",
            mode="rectangle",
            helper_text="Escribe la razón del gasto",
            helper_text_mode="on_focus",
        )

        self.save_btn = MDRaisedButton(
            text="GUARDAR GASTO",
            md_bg_color=Palette.PRIMARY,
            pos_hint={"center_x": 0.5},
            size_hint_x=1,
            height=dp(50),
            _radius=dp(12),
            on_press=self.save_expense,
        )

        self.expense_card.add_widget(self.amount_input)
        self.expense_card.add_widget(self.concept_picker_btn)
        self.expense_card.add_widget(Widget(size_hint_y=None, height=dp(10)))
        self.expense_card.add_widget(self.save_btn)

        main_layout.add_widget(self.expense_card)
        main_layout.add_widget(Widget())
        self.add_widget(main_layout)

    def set_category(self, category_name):
        self.category_name = category_name
        self.title_label.text = f"Gasto: {category_name}"
        self.selected_concept = ""
        self.amount_input.text = ""
        self.custom_concept_input.text = ""
        self.amount_input.error = False
        self.custom_concept_input.error = False

        # Remove both dynamic widgets first to avoid duplicates
        if self.concept_picker_btn in self.expense_card.children:
            self.expense_card.remove_widget(self.concept_picker_btn)
        if self.custom_concept_input in self.expense_card.children:
            self.expense_card.remove_widget(self.custom_concept_input)

        # Swap the concept input UI based on the selected category
        if self.category_name == "Otros":
            self.expense_card.add_widget(self.custom_concept_input, index=2)
        else:
            self.concept_picker_btn.text = "Seleccionar Concepto / Motivo"
            self.expense_card.add_widget(self.concept_picker_btn, index=2)

    def open_concept_selector(self, instance):
        if self.category_name == "Otros":
            return  # Safety check: this path should not be reachable

        current_icon = CATEGORY_ICONS.get(self.category_name, "cash")

        scroll = ScrollView(size_hint_y=None, height=dp(250))
        items_list = MDList()

        for concept in PREDEFINED_CONCEPTS.get(self.category_name, []):
            item = ConceptItem(text=concept, icon_name=current_icon)
            item.bind(on_press=self.select_concept_from_list)
            items_list.add_widget(item)

        scroll.add_widget(items_list)

        self.concept_dialog = MDDialog(
            title="Gastos frecuentes:",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=lambda x: self.concept_dialog.dismiss(),
                )
            ],
        )
        self.concept_dialog.open()

    def select_concept_from_list(self, instance):
        self.selected_concept = instance.text
        self.concept_picker_btn.text = f"Motivo: {self.selected_concept}"
        self.concept_dialog.dismiss()

    def go_back(self, instance):
        self.amount_input.text = ""
        self.selected_concept = ""
        self.custom_concept_input.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def save_expense(self, instance):
        app = MDApp.get_running_app()

        # Resolve the final concept depending on category type
        if self.category_name == "Otros":
            final_concept = self.custom_concept_input.text.strip()
        else:
            final_concept = self.selected_concept

        # Validate required fields
        if not self.amount_input.text.strip():
            self.amount_input.error = True
            return

        if not final_concept:
            if self.category_name == "Otros":
                self.custom_concept_input.error = True
            return

        try:
            amount = float(self.amount_input.text)
        except ValueError:
            self.amount_input.error = True
            self.amount_input.helper_text = "Ingresa un número válido"
            return

        if amount <= 0:
            self.amount_input.error = True
            self.amount_input.helper_text = "El monto debe ser mayor a 0"
            return

        if amount > app.state.total_budget:
            self.amount_input.error = True
            self.amount_input.helper_text = "Presupuesto insuficiente"
            self.show_budget_alert(app.state.total_budget)
            return

        app.state.total_budget -= amount
        app.state.total_expenses += amount

        new_expense = {
            "amount": amount,
            "concept": final_concept,
            "category": self.category_name,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "is_expense": True,
        }
        app.state.expense_history.append(new_expense)

        self.manager.get_screen("home").refresh_ui()
        self.go_back(instance)

    def show_budget_alert(self, current_budget):
        dialog = MDDialog(
            title="¡Presupuesto Insuficiente!",
            text=f"No tienes fondos suficientes para este gasto.\nTu saldo actual es: ${current_budget:.2f}",
            buttons=[
                MDFlatButton(
                    text="ENTENDIDO",
                    theme_text_color="Custom",
                    text_color=MDApp.get_running_app().theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss(),
                ),
            ],
        )
        dialog.open()
