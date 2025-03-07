import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

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

class EmiApp(App):
    def build(self):
        Builder.load_file('views/menu.kv')
        Builder.load_file('views/areas.kv')
        Builder.load_file('views/salones.kv')
        Builder.load_file('views/estadistica.kv')
        Builder.load_file('views/donaciones.kv')
        Builder.load_file('views/distribucion.kv')
        Builder.load_file('views/logistica.kv')
        Builder.load_file('views/otras_areas.kv')
        Builder.load_file('views/ensenanza.kv')
        Builder.load_file('views/recepcion.kv')
        Builder.load_file('views/reporte.kv')
        Builder.load_file('views/ayuda.kv')

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(AreasScreen(name='areas'))
        sm.add_widget(SalonesScreen(name='salones'))
        sm.add_widget(EstadisticaScreen(name='estadistica'))
        sm.add_widget(DonacionesScreen(name='donaciones'))
        sm.add_widget(DistribucionScreen(name='distribucion'))
        sm.add_widget(LogisticaScreen(name='logistica'))
        sm.add_widget(OtrasAreasScreen(name='otras_areas'))
        sm.add_widget(EnsenanzaScreen(name='ensenanza'))
        sm.add_widget(RecepcionScreen(name='recepcion'))
        sm.add_widget(ReporteScreen(name='reporte'))
        sm.add_widget(AyudaScreen(name='ayuda'))

        return sm

if __name__ == '__main__':
    EmiApp().run()