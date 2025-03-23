import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import EnsenanzaController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class EnsenanzaScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/ensenanza.kv')
        super().__init__(**kwargs)
        self.controlador = EnsenanzaController(self)

    def obtener_datos_formulario(self):
        capitan = self.ids.ensenanza_capitan.text
        subcapitan = self.ids.ensenanza_subcapitan.text
        fecha = self.ids.ensenanza_fecha.text

        # Validación básica
        if not capitan:
            self.mostrar_error("El nombre del capitán es obligatorio.")
            return None
        if not subcapitan:
            self.mostrar_error("El número de subcapitanes es obligatorio.")
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
            int(subcapitan)
        except ValueError:
            self.mostrar_error("El número de subcapitanes debe ser un número entero")
            return None

        return {
            "capitan": capitan,
            "subcapitan": int(subcapitan),
            "fecha": fecha
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