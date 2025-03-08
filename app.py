import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

class MenuScreen(Screen):
    pass

class AreasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = ControladorArea(self)

    def actualizar_lista_areas(self, areas):
        lista_areas_grid = self.ids.lista_areas
        lista_areas_grid.clear_widgets()
        for area in areas:
            lista_areas_grid.add_widget(Label(text=area.nombre))
            lista_areas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=area.id: self.editar_area(id)))
            lista_areas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=area.id: self.controlador.eliminar_area(id)))

    def editar_area(self, id):
        area = self.controlador.obtener_area(id)
        if area:
            self.ids.area_nombre.text = area.nombre
            self.ids.area_id.text = str(area.id)

class SalonesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = ControladorSalon(self)

    def actualizar_lista_salones(self, salones):
        lista_salones_grid = self.ids.lista_salones
        lista_salones_grid.clear_widgets()
        for salon in salones:
            lista_salones_grid.add_widget(Label(text=salon.salon + " (" + salon.edad + ")"))
            lista_salones_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=salon.id: self.editar_salon(id)))
            lista_salones_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=salon.id: self.controlador.eliminar_salon(id)))

    def editar_salon(self, id):
        salon = self.controlador.obtener_salon(id)
        if salon:
            self.ids.salon_salon.text = salon.salon
            self.ids.salon_edad.text = salon.edad
            self.ids.salon_id.text = str(salon.id)

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
        # Vistas de la aplicación
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

        #Manejador de las ventanas
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