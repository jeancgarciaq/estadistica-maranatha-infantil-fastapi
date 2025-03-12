import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from controllers.areas_controller import ControladorArea
from controllers.salones_controller import ControladorSalon
from controllers.aulas_controller import ControladorAula
from controllers.donaciones_controller import ControladorDonacion
from controllers.ensenanza_controller import ControladorEnsenanza
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session

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

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

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

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class AulasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = ControladorAula(self)

    def actualizar_lista_aulas(self, aulas):
        lista_aulas_grid = self.ids.lista_aulas
        lista_aulas_grid.clear_widgets()
        for aula in aulas:
            lista_aulas_grid.add_widget(Label(text=f'Aula {aula.id}'))
            lista_aulas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=aula.id: self.editar_aula(id)))
            lista_aulas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=aula.id: self.controlador.eliminar_aula(id)))

    def editar_aula(self, id):
        aula = self.controlador.obtener_aula(id)
        if aula:
            self.ids.aula_auxiliar.text = str(aula.auxiliar)
            self.ids.aula_capitan.text = str(aula.capitan)
            self.ids.aula_colaborador.text = str(aula.colaborador)
            self.ids.aula_condicion.text = aula.condicion
            self.ids.aula_edad.text = aula.edad
            self.ids.aula_maestra.text = str(aula.maestra)
            self.ids.aula_ninos.text = str(aula.ninos)
            self.ids.aula_ninas.text = str(aula.ninas)
            self.ids.aula_subcapitan.text = str(aula.subcapitan)
            self.ids.aula_id_salon.text = str(aula.id_salon)
            self.ids.aula_id.text = str(aula.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class EstadisticaScreen(Screen):
    pass

class DonacionesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = ControladorDonacion(self)
        self.cargar_salones()

    def obtener_salones_seleccionados(self):
        salones_seleccionados = []
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox) and child.active:
                salones_seleccionados.append(int(child.text.split(':')[0]))
        return salones_seleccionados

    def actualizar_lista_donaciones(self, donaciones):
        lista_donaciones_grid = self.ids.lista_donaciones
        lista_donaciones_grid.clear_widgets()
        for donacion in donaciones:
            salones_text = ', '.join([salon.salon for salon in donacion.salones])
            lista_donaciones_grid.add_widget(Label(text=f'Donación {donacion.id} ({salones_text})'))
            lista_donaciones_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=donacion.id: self.editar_donacion(id)))
            lista_donaciones_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=donacion.id: self.controlador.eliminar_donacion(id)))

    def editar_donacion(self, id):
        donacion = self.controlador.obtener_donacion(id)
        if donacion:
            self.ids.donacion_cantidad.text = str(donacion.cantidad)
            self.ids.donacion_descripcion.text = donacion.descripcion
            self.ids.donacion_equipo.text = donacion.equipo
            self.ids.donacion_fecha.text = str(donacion.fecha)
            self.ids.donacion_sembrador.text = donacion.sembrador
            self.ids.donacion_id.text = str(donacion.id)
            self.cargar_salones(donacion.salones)

    def cargar_salones(self, salones_seleccionados=None):
        db: Session = next(get_db())
        salones = db.query(Salon).all()
        self.ids.salones_seleccionados.clear_widgets()
        for salon in salones:
            checkbox = CheckBox(text=f'{salon.id}: {salon.salon}', active=False)
            if salones_seleccionados and salon in salones_seleccionados:
                checkbox.active = True
            self.ids.salones_seleccionados.add_widget(checkbox)
    
    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class DistribucionScreen(Screen):
    pass

class LogisticaScreen(Screen):
    pass

class OtrasAreasScreen(Screen):
    pass

class EnsenanzaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = ControladorEnsenanza(self)

    def actualizar_lista_ensenanzas(self, ensenanzas):
        lista_ensenanzas_grid = self.ids.lista_ensenanzas
        lista_ensenanzas_grid.clear_widgets()
        for ensenanza in ensenanzas:
            lista_ensenanzas_grid.add_widget(Label(text=f'Enseñanza {ensenanza.id}'))
            lista_ensenanzas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=ensenanza.id: self.editar_ensenanza(id)))
            lista_ensenanzas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=ensenanza.id: self.controlador.eliminar_ensenanza(id)))

    def editar_ensenanza(self, id):
        ensenanza = self.controlador.obtener_ensenanza(id)
        if ensenanza:
            self.ids.ensenanza_capitan.text = ensenanza.capitan
            self.ids.ensenanza_fecha.text = str(ensenanza.fecha)
            self.ids.ensenanza_subcapitan.text = str(ensenanza.subcapitan)
            self.ids.ensenanza_id.text = str(ensenanza.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

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
        Builder.load_file('views/aulas.kv')
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
        sm.add_widget(AulasScreen(name='aulas'))
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