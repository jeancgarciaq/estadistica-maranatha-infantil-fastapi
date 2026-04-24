from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from components.styled_popup import StyledPopup

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
try:
    Builder.load_file('views/areas.kv')
except Exception as e:
    Logger.error(f"Error cargando views/areas.kv: {e}")

class AreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador

    def _limpiar_campos(self):
        self.ids.area_id.text = ''
        self.ids.area_nombre.text = ''

    def crear_area(self, nombre):
        exito, mensaje = self.controlador.crear_area(nombre)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_area(self, id_str, nombre):
        area_id = int(id_str) if id_str and id_str.isdigit() else None
        
        exito, mensaje = self.controlador.actualizar_area(area_id, nombre)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_area(self, id_str):
        area_id = int(id_str) if id_str and id_str.isdigit() else None
        
        exito, mensaje = self.controlador.eliminar_area(area_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def buscar_area(self):
        """Obtiene los datos del formulario y llama al método buscar_area del controlador."""
        area_id = self.ids.area_id.text.strip()  # ID del área
        area_nombre = self.ids.area_nombre.text.strip()  # Nombre del área

        area_id_int = int(area_id) if area_id.isdigit() else None

        # Llamar al método buscar_area del controlador
        exito, area, mensaje = self.controlador.buscar_area(id=area_id_int, nombre=area_nombre)
        
        if exito and area:
            StyledPopup.mostrar_popup("Información del Área", f"ID: {area.id}\nNombre: {area.area}", tipo="info")
            self._limpiar_campos()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")