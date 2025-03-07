import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window

# Cargar los archivos KV
Builder.load_file('app.kv')  # Contiene el menú principal
Builder.load_file('main.kv') # Contiene la navegación entre pantallas

# Definir las pantallas
class MenuScreen(Screen):
    pass

class AreasScreen(Screen):
    pass

class SalonesScreen(Screen):
    pass

class EstadisticaScreen(Screen):
    pass

class DonacionesScreen(Screen):
    pass

class DistribucionScreen(Screen):
    pass

class LogisticaScreen(Screen):
    pass

class OtrasAreasScreen(Screen):
    pass

class EnsenanzaScreen(Screen):
    pass

class RecepcionScreen(Screen):
    pass

class ReporteScreen(Screen):
    pass

class AyudaScreen(Screen):
    pass

# Administrador de pantallas
class WindowManager(ScreenManager):
    pass

class EmiApp(App):    
    def build(self):
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        return WindowManager()

if __name__ == '__main__':
    EmiApp().run()