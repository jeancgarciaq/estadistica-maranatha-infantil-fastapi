from kivy.uix.screenmanager import Screen
from controllers import SalonesController
from kivy.lang import Builder
from components.styled_popup import StyledPopup


class SalonesScreen(Screen):
    def __init__(self, controlador, vista=None, **kwargs):
        try:
            Builder.load_file('views/salones.kv')
        except Exception as e:
            print(f"Error al cargar salones.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador
        self.vista = vista

    def obtener_datos_formulario(self):
        salon_nombre = self.ids.salon_nombre.text
        salon_edad = self.ids.salon_edad.text

        # Validación básica
        if not salon_nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del salón es obligatorio.", tipo="error")
            return None
        if not salon_edad:
            StyledPopup.mostrar_popup("Error", "La edad del salón es obligatoria.", tipo="error")
            return None

        return {"salón": salon_nombre}

    def actualizar_lista_salones(self, salones):
        lista_salones_grid = self.ids.lista_salones
        lista_salones_grid.clear_widgets()
        for salon in salones:
            lista_salones_grid.add_widget(Label(text=salon.nombre))
            lista_salones_grid.add_widget(Label(text=salon.edad))
            lista_salones_grid.add_widget(Button(text="Editar", on_press=lambda btn, id=salon.id: self.editar_salon(id)))
            lista_salones_grid.add_widget(Button(text="Eliminar", on_press=lambda btn, id=salon.id: self.controlador.eliminar_salon(id)))

    def editar_salon(self, id):
        salon = self.controlador.obtener_salon(id)
        if salon:
            self.ids.salon_nombre.text = salon.nombre
            self.ids.salon_id.text = str(salon.id)

    def buscar_salon(self):
        """Obtiene los datos del formulario y llama al método buscar_salon del controlador."""
        salon_id = self.ids.salon_id.text.strip()  # ID del salón
        salon_nombre = self.ids.salon_nombre.text.strip()  # Nombre del salón

        # Validar que al menos uno de los campos esté lleno
        if not salon_id and not salon_nombre:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o un nombre para buscar el salón.", tipo="error")
            return

        # Convertir el ID a entero si es posible
        salon_id = int(salon_id) if salon_id.isdigit() else None

        # Llamar al método buscar_salon del controlador
        self.controlador.buscar_salon(id=salon_id, nombre=salon_nombre)