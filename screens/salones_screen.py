import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from controllers import SalonesController
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import logging

# Configuración de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class SalonesScreen(Screen):
    def __init__(self, controlador, vista, **kwargs):
        try:
            Builder.load_file('views/salones.kv')
        except Exception as e:
            print(f"Error al cargar salones.kv: {e}")
        super().__init__(**kwargs)
        # Crear el controlador como atributo
        self.controlador = SalonesController(self)
        self.vista = self

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
    
    def mostrar_exito(self, mensaje):
        popup = Popup(title='Éxito', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()