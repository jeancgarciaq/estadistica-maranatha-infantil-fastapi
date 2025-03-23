import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import LogisticaController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class LogisticaScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/logistica.kv')
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
        fecha = self.ids.logistica_fecha.text

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
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
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
            "secretaria": int(secretaria),
            "fecha": fecha
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
            self.ids.logistica_fecha.text = str(logistica.fecha)
            self.ids.logistica_id.text = str(logistica.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()