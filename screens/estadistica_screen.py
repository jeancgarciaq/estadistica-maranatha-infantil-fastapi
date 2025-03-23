import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class EstadisticaScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('views/estadistica.kv')
        super().__init__(**kwargs)
