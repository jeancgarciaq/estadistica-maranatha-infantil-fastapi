import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder

# Importar pantallas separadas
from screens import MenuScreen, AreasScreen, SalonesScreen, EstadisticaScreen, DonacionesScreen, DistribucionesScreen, LogisticaScreen, OtrasAreasScreen, EnsenanzaScreen, RecepcionScreen, ReporteScreen, AyudaScreen

# Cargar archivos KV
Builder.load_file('views/menu.kv')

# Definir el ScreenManager
class WindowManager(ScreenManager):
    pass

class EmiApp(App):    
    def build(self):
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        return WindowManager()

if __name__ == '__main__':
    EmiApp().run()
