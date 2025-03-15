import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from controllers import AreasController, SalonesController, AulasController, DonacionesController, EnsenanzaController, LogisticaController, OtrasAreasController, RecepcionController, DistribucionController
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime

class MenuScreen(Screen):
    pass

class AreasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = AreasController(self)
    
    def obtener_datos_formulario(self):
        area_nombre = self.ids.area_nombre.text

        # Validación básica
        if not area_nombre:
            self.mostrar_error("El nombre del área es obligatorio.")
            return None

        return {
            "area": area_nombre
        }

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
        self.controlador = SalonesController(self)

    def obtener_datos_formulario(self):
        salon_nombre = self.ids.salon_nombre.text
        salon_edad = self.ids.salon_edad.text

        # Validación básica
        if not salon_nombre:
            self.mostrar_error("El nombre del salón es obligatorio.")
            return None
        if not salon_edad:
            self.mostrar_error("La edad del salón es obligatoria.")
            return None

        return {
            "salon": salon_nombre,
            "edad": salon_edad
        }
    
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
        self.controlador = AulasController(self)
    
    def obtener_datos_formulario(self):
        auxiliar = self.ids.aula_auxiliar.text
        capitan = self.ids.aula_capitan.text
        colaborador = self.ids.aula_colaborador.text
        condicion = self.ids.aula_condicion.text
        edad = self.ids.aula_edad.text
        maestra = self.ids.aula_maestra.text
        ninos = self.ids.aula_ninos.text
        ninas = self.ids.aula_ninas.text
        subcapitan = self.ids.aula_subcapitan.text
        id_salon = self.ids.aula_id_salon.text

        # Validación básica
        if not auxiliar:
            self.mostrar_error("El número de auxiliares es obligatorio.")
            return None
        if not capitan:
            self.mostrar_error("El número de capitanes es obligatorio.")
            return None
        if not colaborador:
            self.mostrar_error("El número de colaboradores es obligatorio.")
            return None
        if not condicion:
            self.mostrar_error("La condición es obligatoria.")
            return None
        if not edad:
            self.mostrar_error("La edad es obligatoria.")
            return None
        if not maestra:
            self.mostrar_error("El número de maestras es obligatorio.")
            return None
        if not ninos:
            self.mostrar_error("El número de niños es obligatorio.")
            return None
        if not ninas:
            self.mostrar_error("El número de niñas es obligatorio.")
            return None
        if not subcapitan:
            self.mostrar_error("El número de subcapitanes es obligatorio.")
            return None
        if not id_salon:
            self.mostrar_error("El ID del salón es obligatorio.")
            return None

        try:
            int(auxiliar)
            int(capitan)
            int(colaborador)
            int(maestra)
            int(ninos)
            int(ninas)
            int(subcapitan)
            int(id_salon)
        except ValueError:
            self.mostrar_error("Los campos numéricos deben ser números enteros.")
            return None

        return {
            "auxiliar": int(auxiliar),
            "capitan": int(capitan),
            "colaborador": int(colaborador),
            "condicion": condicion,
            "edad": edad,
            "maestra": int(maestra),
            "ninos": int(ninos),
            "ninas": int(ninas),
            "subcapitan": int(subcapitan),
            "id_salon": int(id_salon)
        }

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
        self.controlador = DonacionesController(self)

    def obtener_datos_formulario(self):
        descripcion = self.ids.donacion_descripcion.text
        cantidad = self.ids.donacion_cantidad.text
        unidad = self.ids.donacion_unidad.textclear
        fecha = self.ids.donacion_fecha.text
        equipo = self.ids.donacion_equipo.text

        # Validación básica
        if not descripcion:
            self.mostrar_error("La descripción es obligatoria.")
            return None
        if not cantidad:
            self.mostrar_error("La cantidad es obligatoria.")
            return None
        try:
            float(cantidad)
        except ValueError:
            self.mostrar_error("La cantidad debe ser un número.")
            return None
        if not unidad:
            self.mostrar_error("La unidad es obligatoria.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            return None
        if not equipo:
            self.mostrar_error("El equipo es obligatorio.")
            return None

        return {
            "descripcion": descripcion,
            "cantidad": cantidad,
            "unidad": unidad,
            "fecha": fecha,
            "equipo": equipo
        }

    def crear_donacion(self):
        datos = self.obtener_datos_formulario()
        self.controlador.crear_donacion(datos["cantidad"], datos["descripcion"], datos["unidad"], datos["fecha"], datos["equipo"], self.obtener_salones_seleccionados())

    def actualizar_donacion(self):
        datos = self.obtener_datos_formulario()
        self.controlador.actualizar_donacion(self.ids.donacion_id.text, datos["cantidad"], datos["descripcion"], datos["unidad"], datos["fecha"], datos["equipo"], self.obtener_salones_seleccionados())

    def eliminar_donacion(self):
        self.controlador.eliminar_donacion(self.ids.donacion_id.text)

    def listar_donaciones(self):
        self.controlador.listar_donaciones()

    def actualizar_lista_donaciones(self, donaciones):
        self.ids.lista_donaciones.clear_widgets()
        for donacion in donaciones:
            self.ids.lista_donaciones.add_widget(Label(text=str(donacion.id)))
            self.ids.lista_donaciones.add_widget(Label(text=donacion.descripcion))
            editar_btn = Button(text='Editar')
            editar_btn.donacion = donacion
            editar_btn.bind(on_press=self.cargar_donacion_editar)
            self.ids.lista_donaciones.add_widget(editar_btn)

    def cargar_donacion_editar(self, instance):
        donacion = instance.donacion
        self.ids.donacion_id.text = str(donacion.id)
        self.ids.donacion_descripcion.text = donacion.descripcion
        self.ids.donacion_cantidad.text = str(donacion.cantidad)
        self.ids.donacion_unidad.text = donacion.unidad
        self.ids.donacion_fecha.text = donacion.fecha.strftime('%Y-%m-%d')
        self.ids.donacion_equipo.text = donacion.equipo
        self.cargar_salones_seleccionados(donacion.salones)

    def obtener_salones_seleccionados(self):
        salones_seleccionados = []
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox) and child.active:
                salones_seleccionados.append(int(child.text.split('-')[0]))
        return salones_seleccionados

    def cargar_salones(self):
        self.ids.salones_seleccionados.clear_widgets()
        salones = self.controlador.obtener_salones()
        for salon in salones:
            checkbox = CheckBox(text=f"{salon.id}-{salon.nombre}")
            self.ids.salones_seleccionados.add_widget(checkbox)

    def cargar_salones_seleccionados(self, salones):
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox):
                salon_id = int(child.text.split('-')[0])
                if any(s.id == salon_id for s in salones):
                    child.active = True

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class DistribucionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = DistribucionController(self)
        self.cargar_salones()
        self.cargar_donaciones()

    def cargar_donaciones(self):
      self.ids.donacion_spinner.values = self.controlador.obtener_donaciones()

    def obtener_donaciones(self):
        return self.controlador.obtener_donaciones()

    def obtener_donacion_seleccionada(self):
        donacion_text = self.ids.donacion_spinner.text
        if donacion_text:
            return int(donacion_text.split(':')[0])
        return None

    def obtener_salones_seleccionados(self):
        salones_seleccionados = []
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox) and child.active:
                salones_seleccionados.append(int(child.text.split(':')[0]))
        return salones_seleccionados

    def cargar_salones(self):
        salones = self.controlador.obtener_salones()
        self.ids.salones_seleccionados.clear_widgets()
        for salon in salones:
            checkbox = CheckBox(text=f'{salon.id}: {salon.salon}')
            self.ids.salones_seleccionados.add_widget(checkbox)

    def actualizar_lista_distribuciones(self, donaciones):
        lista_distribuciones_grid = self.ids.lista_distribuciones
        lista_distribuciones_grid.clear_widgets()
        for donacion in donaciones:
            salones_text = ', '.join([salon.salon for salon in donacion.salones])
            lista_distribuciones_grid.add_widget(Label(text=f'Donación {donacion.id}'))
            lista_distribuciones_grid.add_widget(Label(text=f'Salones: {salones_text}'))

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class LogisticaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = LogisticaController(self)

    def obtener_datos_formulario(self):
        almacen = self.ids.logistica_almacen.text
        capitan = self.ids.logistica_capitan.text
        distribucion = self.ids.logistica_distribucion.text
        fecha = self.ids.logistica_fecha.text
        hidratacion = self.ids.logistica_hidratacion.text
        pasillo = self.ids.logistica_pasillo.text
        secretaria = self.ids.logistica_secretaria.text

        # Validación básica
        if not almacen:
            self.mostrar_error("El número de almacenes es obligatorio.")
            return None
        if not capitan:
            self.mostrar_error("El número de capitanes es obligatorio.")
            return None
        if not distribucion:
            self.mostrar_error("El número de distribuciones es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        if not hidratacion:
            self.mostrar_error("El número de hidrataciones es obligatorio.")
            return None
        if not pasillo:
            self.mostrar_error("El número de pasillos es obligatorio.")
            return None
        if not secretaria:
            self.mostrar_error("El número de secretarias es obligatorio.")
            return None

        try:
            int(almacen)
            int(capitan)
            int(distribucion)
            int(hidratacion)
            int(pasillo)
            int(secretaria)
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Los campos numéricos deben ser números enteros y la fecha debe tener el formato AAAA-MM-DD.")
            return None

        return {
            "almacen": int(almacen),
            "capitan": int(capitan),
            "distribucion": int(distribucion),
            "fecha": fecha,
            "hidratacion": int(hidratacion),
            "pasillo": int(pasillo),
            "secretaria": int(secretaria)
        }
    
    def actualizar_lista_logisticas(self, logisticas):
        lista_logisticas_grid = self.ids.lista_logisticas
        lista_logisticas_grid.clear_widgets()
        for logistica in logisticas:
            lista_logisticas_grid.add_widget(Label(text=f'Logística {logistica.id}'))
            lista_logisticas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=logistica.id: self.editar_logistica(id)))
            lista_logisticas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=logistica.id: self.controlador.eliminar_logistica(id)))

    def editar_logistica(self, id):
        logistica = self.controlador.obtener_logistica(id)
        if logistica:
            self.ids.logistica_almacen.text = str(logistica.almacen)
            self.ids.logistica_capitan.text = str(logistica.capitan)
            self.ids.logistica_distribucion.text = str(logistica.distribucion)
            self.ids.logistica_fecha.text = str(logistica.fecha)
            self.ids.logistica_hidratacion.text = str(logistica.hidratacion)
            self.ids.logistica_pasillo.text = str(logistica.pasillo)
            self.ids.logistica_secretaria.text = str(logistica.secretaria)
            self.ids.logistica_id.text = str(logistica.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class OtrasAreasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = OtrasAreasController(self)

    def obtener_datos_formulario(self):
        alabanza = self.ids.otrasareas_alabanza.text
        fecha = self.ids.otrasareas_fecha.text
        protocolo = self.ids.otrasareas_protocolo.text
        semillitas = self.ids.otrasareas_semillitas.text
        sonido = self.ids.otrasareas_sonido.text
        teatro = self.ids.otrasareas_teatro.text
        tv = self.ids.otrasareas_tv.text
        ujier = self.ids.otrasareas_ujier.text

        # Validación básica
        if not alabanza:
            self.mostrar_error("El número de alabanzas es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        if not protocolo:
            self.mostrar_error("El número de protocolos es obligatorio.")
            return None
        if not semillitas:
            self.mostrar_error("El número de semillitas es obligatorio.")
            return None
        if not sonido:
            self.mostrar_error("El número de sonidos es obligatorio.")
            return None
        if not teatro:
            self.mostrar_error("El número de teatros es obligatorio.")
            return None
        if not tv:
            self.mostrar_error("El número de tvs es obligatorio.")
            return None
        if not ujier:
            self.mostrar_error("El número de ujieres es obligatorio.")
            return None

        try:
            int(alabanza)
            int(protocolo)
            int(semillitas)
            int(sonido)
            int(teatro)
            int(tv)
            int(ujier)
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Los campos numéricos deben ser números enteros y la fecha debe tener el formato AAAA-MM-DD.")
            return None

        return {
            "alabanza": int(alabanza),
            "fecha": fecha,
            "protocolo": int(protocolo),
            "semillitas": int(semillitas),
            "sonido": int(sonido),
            "teatro": int(teatro),
            "tv": int(tv),
            "ujier": int(ujier)
        }
    
    def actualizar_lista_otrasareas(self, otrasareas):
        lista_otrasareas_grid = self.ids.lista_otrasareas
        lista_otrasareas_grid.clear_widgets()
        for otrasarea in otrasareas:
            lista_otrasareas_grid.add_widget(Label(text=f'Otras áreas {otrasarea.id}'))
            lista_otrasareas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=otrasarea.id: self.editar_otrasareas(id)))
            lista_otrasareas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=otrasarea.id: self.controlador.eliminar_otrasareas(id)))

    def editar_otrasareas(self, id):
        otrasarea = self.controlador.obtener_otrasareas(id)
        if otrasarea:
            self.ids.otrasareas_alabanza.text = str(otrasarea.alabanza)
            self.ids.otrasareas_fecha.text = str(otrasarea.fecha)
            self.ids.otrasareas_protocolo.text = str(otrasarea.protocolo)
            self.ids.otrasareas_semillitas.text = str(otrasarea.semillitas)
            self.ids.otrasareas_sonido.text = str(otrasarea.sonido)
            self.ids.otrasareas_teatro.text = str(otrasarea.teatro)
            self.ids.otrasareas_tv.text = str(otrasarea.tv)
            self.ids.otrasareas_ujier.text = str(otrasarea.ujier)
            self.ids.otrasareas_id.text = str(otrasarea.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class EnsenanzaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = EnsenanzaController(self)

    def obtener_datos_formulario(self):
        capitan = self.ids.ensenanza_capitan.text
        fecha = self.ids.ensenanza_fecha.text
        subcapitan = self.ids.ensenanza_subcapitan.text

        # Validación básica
        if not capitan:
            self.mostrar_error("El nombre del capitán es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        if not subcapitan:
            self.mostrar_error("El número de subcapitanes es obligatorio.")
            return None

        try:
            int(subcapitan)
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("El número de subcapitanes debe ser un número entero y la fecha debe tener el formato AAAA-MM-DD.")
            return None

        return {
            "capitan": capitan,
            "fecha": fecha,
            "subcapitan": int(subcapitan)
        }
    
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = RecepcionController(self)

    def obtener_datos_formulario(self):
        nombre = self.ids.recepcion_nombre.text

        # Validación básica
        if not nombre:
            self.mostrar_error("El nombre es obligatorio.")
            return None

        return {
            "nombre": nombre
        }
    
    def actualizar_lista_recepciones(self, recepciones):
        lista_recepciones_grid = self.ids.lista_recepciones
        lista_recepciones_grid.clear_widgets()
        for recepcion in recepciones:
            lista_recepciones_grid.add_widget(Label(text=f'Recepción {recepcion.id}'))
            lista_recepciones_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=recepcion.id: self.editar_recepcion(id)))
            lista_recepciones_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=recepcion.id: self.controlador.eliminar_recepcion(id)))

    def editar_recepcion(self, id):
        recepcion = self.controlador.obtener_recepcion(id)
        if recepcion:
            self.ids.recepcion_nombre.text = recepcion.nombre
            self.ids.recepcion_id.text = str(recepcion.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

class ReporteScreen(Screen):
    pass

class AyudaScreen(Screen):
    pass

class EmiApp(App):
    def build(self):
        #Icono
        self.icon = 'kids.ico'
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