from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from components.styled_popup import StyledPopup
import logging

logger = logging.getLogger(__name__)

class ListOtrasAreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/list_otras_areas.kv')
        except Exception as e:
            logger.error(f"Error cargando list_otras_areas.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def on_enter(self):
        """Se ejecuta al entrar a la pantalla."""
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los registros desde el controlador."""
        try:
            registros = self.controlador.listar_otrasareas()
            self.actualizar_lista(registros)
        except Exception as e:
            logger.error(f"Error al cargar datos de otras áreas: {e}")
            StyledPopup.mostrar_popup("Error", f"No se pudieron cargar los datos: {e}", tipo="error")

    def actualizar_lista(self, registros):
        """Puebla el contenedor con los registros."""
        container = self.ids.container
        container.clear_widgets()

        if not registros:
            container.add_widget(Label(text="No hay registros disponibles", size_hint_y=None, height=40))
            return

        for reg in registros:
            # Crear una fila para cada registro
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5, padding=[5, 0])
            
            # Formatear fecha si es objeto date
            fecha_str = reg.fecha.strftime('%Y-%m-%d') if hasattr(reg.fecha, 'strftime') else str(reg.fecha)
            
            row.add_widget(Label(text=fecha_str, size_hint_x=0.4))
            row.add_widget(Label(text=str(reg.id), size_hint_x=0.2))
            
            # Botones de Acción
            actions = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=5)
            
            btn_edit = Button(
                text="Editar",
                background_normal='',
                background_color=(0, 100/255, 180/255, 1),
                size_hint_y=0.8,
                pos_hint={'center_y': 0.5}
            )
            btn_edit.bind(on_release=lambda x, r=reg: self.editar_registro(r.id))
            
            btn_del = Button(
                text="Borrar",
                background_normal='',
                background_color=(180/255, 0, 0, 1),
                size_hint_y=0.8,
                pos_hint={'center_y': 0.5}
            )
            btn_del.bind(on_release=lambda x, r=reg: self.confirmar_eliminacion(r.id))
            
            actions.add_widget(btn_edit)
            actions.add_widget(btn_del)
            row.add_widget(actions)
            
            container.add_widget(row)

    def editar_registro(self, id):
        """Regresa a la pantalla principal y carga el registro para editar."""
        self.manager.current = 'otrasareas'
        main_screen = self.manager.get_screen('otrasareas')
        main_screen.editar_otrasareas(id)

    def confirmar_eliminacion(self, id):
        """Muestra el popup de confirmación antes de borrar."""
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            "Esta acción no se puede deshacer. ¿Está seguro de que desea eliminar este registro?",
            on_confirm=lambda: self.eliminar_registro(id)
        )

    def eliminar_registro(self, id):
        """Ejecuta la eliminación final del registro."""
        exito, mensaje = self.controlador.eliminar_otrasareas(id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_datos() # Refrescar lista
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")
