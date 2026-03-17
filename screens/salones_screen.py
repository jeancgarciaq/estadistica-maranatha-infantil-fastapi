from kivy.uix.screenmanager import Screen
from controllers import SalonesController
from kivy.lang import Builder
from components.styled_popup import StyledPopup


class SalonesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/salones.kv')
        except Exception as e:
            print(f"Error al cargar salones.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador
        self.controlador = controlador

    def obtener_datos_formulario(self):
        salon_nombre = self.ids.salon_nombre.text.strip()
        salon_edad = self.ids.salon_edad.text.strip()

        # Validación básica
        if not salon_nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del salón es obligatorio.", tipo="error")
            return None
        if not salon_edad:
            StyledPopup.mostrar_popup("Error", "La edad del salón es obligatoria.", tipo="error")
            return None

        return {"nombre": salon_nombre, "edad": salon_edad}

    def crear_salon(self):
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.crear_salon(datos["nombre"], datos["edad"])
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_salon(self):
        id_texto = self.ids.salon_id.text.strip()
        if not id_texto or not id_texto.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.actualizar_salon(int(id_texto), datos["nombre"], datos["edad"])
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_salon(self, id_val):
        if not id_val or not id_val.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para eliminar.", tipo="error")
            return
            
        exito, mensaje = self.controlador.eliminar_salon(int(id_val))
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def limpiar_formulario(self):
        self.ids.salon_id.text = ""
        self.ids.salon_nombre.text = ""
        self.ids.salon_edad.text = ""

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
        salon_id = self.ids.salon_id.text.strip()
        salon_nombre = self.ids.salon_nombre.text.strip()

        if not salon_id and not salon_nombre:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o un nombre para buscar el salón.", tipo="error")
            return

        s_id = int(salon_id) if salon_id.isdigit() else None
        exito, salon, mensaje = self.controlador.buscar_salon(id=s_id, nombre=salon_nombre)
        
        if exito:
            self.editar_salon(salon.id)
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")