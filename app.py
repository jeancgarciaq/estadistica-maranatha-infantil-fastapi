import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder

# Importar pantallas separadas
from screens.menu_screen import MenuScreen
from screens.areas_screen import AreasScreen
from screens.salones_screen import SalonesScreen
from screens.estadistica_screen import EstadisticaScreen
from screens.donaciones_screen import DonacionesScreen
from screens.distribuciones_screen import DistribucionesScreen
from screens.logistica_screen import LogisticaScreen
from screens.otras_areas_screen import OtrasAreasScreen
from screens.ensenanza_screen import EnsenanzaScreen
from screens.recepcion_screen import RecepcionScreen
from screens.reporte_screen import ReporteScreen
from screens.ayuda_screen import AyudaScreen

# Cargar archivos KV
Builder.load_file('styles/app.kv')
Builder.load_file('main.kv')

# Definir el ScreenManager
class WindowManager(ScreenManager):
    pass

class EmiApp(App):    
    def build(self):
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        return WindowManager()

if __name__ == '__main__':
    EmiApp().run()
