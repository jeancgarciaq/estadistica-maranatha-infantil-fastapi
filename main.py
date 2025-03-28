import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.areas_screen import AreasScreen
from screens.list_areas_screen import ListAreasScreen
from controllers.areas_controller import AreasController

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        areas_screen = AreasScreen(name='areas', controlador=AreasController(None))
        list_areas_screen = ListAreasScreen(name='areas_list', controlador=AreasController(None))
        sm.add_widget(areas_screen)
        sm.add_widget(list_areas_screen)
        areas_screen.controlador.vista = areas_screen  # Link controller to view
        return sm

if __name__ == '__main__':
    MyApp().run()