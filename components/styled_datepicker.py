import calendar
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class StyledDatePicker(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.now = datetime.now()
        self.year = self.now.year
        self.month = self.now.month
        
        self.title = "Seleccionar Fecha"
        self.size_hint = (0.9, 0.7)
        
        # Meses en español
        self.meses = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.content = self.main_layout
        
        self.build_ui()

    def build_ui(self):
        self.main_layout.clear_widgets()
        
        # Header: Mes y Año
        header = BoxLayout(size_hint_y=None, height=50, spacing=5)
        prev_btn = Button(
            text="<", 
            size_hint_x=None, 
            width=50,
            background_normal='',
            background_color=(0, 119/255, 194/255, 1)
        )
        prev_btn.bind(on_release=self.prev_month)
        
        self.title_label = Label(text=f"{self.meses[self.month]} {self.year}", font_size=20, bold=True)
        
        next_btn = Button(
            text=">", 
            size_hint_x=None, 
            width=50,
            background_normal='',
            background_color=(0, 119/255, 194/255, 1)
        )
        next_btn.bind(on_release=self.next_month)
        
        header.add_widget(prev_btn)
        header.add_widget(self.title_label)
        header.add_widget(next_btn)
        self.main_layout.add_widget(header)
        
        # Cabecera de días de la semana
        weekdays = GridLayout(cols=7, size_hint_y=None, height=30)
        for day in ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]:
            weekdays.add_widget(Label(text=day, color=(0.7, 0.7, 0.7, 1), font_size=14))
        self.main_layout.add_widget(weekdays)
        
        # Cuadrícula de días
        self.days_grid = GridLayout(cols=7, spacing=5)
        self.populate_days()
        self.main_layout.add_widget(self.days_grid)
        
        # Botón cerrar
        cancel_btn = Button(
            text="Cancelar", 
            size_hint_y=None, 
            height=50, 
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_release=self.dismiss)
        self.main_layout.add_widget(cancel_btn)

    def populate_days(self):
        self.days_grid.clear_widgets()
        # Monday is 0, Sunday is 6
        month_days = calendar.monthcalendar(self.year, self.month)
        
        for week in month_days:
            for day in week:
                if day == 0:
                    self.days_grid.add_widget(Label(text=""))
                else:
                    is_today = (day == self.now.day and self.month == self.now.month and self.year == self.now.year)
                    btn = Button(
                        text=str(day),
                        background_normal='',
                        background_color=(0, 119/255, 194/255, 1) if not is_today else (0, 0.7, 0.3, 1)
                    )
                    btn.bind(on_release=lambda instance, d=day: self.select_date(d))
                    self.days_grid.add_widget(btn)

    def prev_month(self, *args):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_ui()

    def next_month(self, *args):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_ui()

    def update_ui(self):
        self.title_label.text = f"{self.meses[self.month]} {self.year}"
        self.populate_days()

    def select_date(self, day):
        # Formato YYYY-MM-DD
        date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        if self.callback:
            self.callback(date_str)
        self.dismiss()
