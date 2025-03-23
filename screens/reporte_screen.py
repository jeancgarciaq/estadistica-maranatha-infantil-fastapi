import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class ReporteScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('views/reporte.kv')
        super().__init__(**kwargs)