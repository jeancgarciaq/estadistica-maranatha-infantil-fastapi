import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('views/menu.kv')
        super().__init__(**kwargs)
