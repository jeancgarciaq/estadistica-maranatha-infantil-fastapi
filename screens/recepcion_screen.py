import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import RecepcionController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class RecepcionScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/recepcion.kv')
        super().__init__(**kwargs)
        self.controlador = RecepcionController(self)

    def obtener_datos_formulario(self):
        nombre = self.ids.recepcion_nombre.text
        fecha = self.ids.recepcion_fecha.text

        # Validación básica
        if not nombre:
            self.mostrar_error("El nombre es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            return None

        return {
            "nombre": nombre,
            "fecha": fecha
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
            self.ids.recepcion_fecha.text = recepcion.fecha.strftime('%Y-%m-%d')
            self.ids.recepcion_id.text = str(recepcion.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()