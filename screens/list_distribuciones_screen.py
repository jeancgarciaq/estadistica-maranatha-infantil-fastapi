from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from components.styled_popup import StyledPopup
import logging
from kivy.lang import Builder

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para mayor detalle
logger = logging.getLogger(__name__)

class ListDistribucionesScreen(Screen):
    """Pantalla para desplegar la lista de distribuciones."""
    def __init__(self, controlador, **kwargs):
        """Inicializando ListDistribucionesScreen."""
        try:
            Builder.load_file("views/list_distribuciones.kv")
        except Exception as e:
            logger.error(f"Error cargando la vista de lista de distribuciones: {e}")
        super().__init__(**kwargs)
        logger.info("Inicializado ListAreasScreen")
        # Asignar el controlador correctamente
        self.controlador = controlador

    def actualizar_lista_distribuciones(self, distribuciones):
        """ Actualiza la vista de la lista de las distribuciones """
        logger.debug(f"Datos recibidos para actualizar lista de distribuciones: {distribuciones}")
        if not isinstance(distribuciones, list):
            logger.error("El parámetro 'distribuciones' no es una lista. Verifique el controlador.")
            distribuciones = []
        lista_distribuciones = self.ids.lista_distribuciones
        lista_distribuciones.clear_widgets()
        if not distribuciones or len(distribuciones) == 0:
            lista_distribuciones.add_widget(Label(text="No hay áreas registradas", font_size='18sp', size_hint_y=None, height=40))
        else:
            for distribucion in distribuciones:
                logger.debug(f"Agregando distribución: ID={distribucion.id}, ID Salón={distribucion.salon_id}, ID Donación={distribucion.donacion_id}, Cantidad={distribucion.cantidad}, Fecha={distribucion.fecha}")
                
                # ID
                lista_distribuciones.add_widget(Label(text=f"{distribucion.id}", size_hint_x=0.1, size_hint_y=None, height=40))
                
                # Donación (Podemos mostrar descripción si está cargada)
                donacion_text = f"{distribucion.donacion.descripcion}" if distribucion.donacion else str(distribucion.donacion_id)
                lista_distribuciones.add_widget(Label(text=donacion_text, size_hint_x=0.2, size_hint_y=None, height=40))
                
                # Salón
                salon_text = f"{distribucion.salon.salon}" if distribucion.salon else str(distribucion.salon_id)
                lista_distribuciones.add_widget(Label(text=salon_text, size_hint_x=0.1, size_hint_y=None, height=40))
                
                # Cantidad
                lista_distribuciones.add_widget(Label(text=str(distribucion.cantidad), size_hint_x=0.1, size_hint_y=None, height=40))
                
                # Unidad
                lista_distribuciones.add_widget(Label(text=str(distribucion.unidad), size_hint_x=0.1, size_hint_y=None, height=40))
                
                # Fecha
                lista_distribuciones.add_widget(Label(text=str(distribucion.fecha), size_hint_x=0.2, size_hint_y=None, height=40))
                
                # Acciones
                acciones_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_x=0.2, size_hint_y=None, height=40)
                
                btn_editar = Button(text="Editar", size_hint_y=None, height=30)
                btn_editar.bind(on_release=lambda btn, d_id=distribucion.id: self.editar_distribucion(d_id))
                
                btn_borrar = Button(text="Borrar", size_hint_y=None, height=30, background_color=(1, 0, 0, 1))
                btn_borrar.bind(on_release=lambda btn, d_id=distribucion.id: self.confirmar_eliminacion(d_id))
                
                acciones_layout.add_widget(btn_editar)
                acciones_layout.add_widget(btn_borrar)
                lista_distribuciones.add_widget(acciones_layout)

    def cargar_distribuciones(self):
        """Consultando y llenando la lista distribuciones."""
        try:
            distribuciones = self.controlador.listar_distribuciones()
            if distribuciones is None:
                logger.warning("El método listar_distribuciones devolvió None. Verifique el controlador.")
            else:
                logger.debug(f"Distribuciones consultadas: {distribuciones}")
            self.actualizar_lista_distribuciones(distribuciones or [])  # Asegurarse de pasar una lista vacía si es None
        except Exception as e:
            logger.error(f"Error consultando distribuciones: {e}")
            self.actualizar_lista_distribuciones([])

    def on_enter(self):
        """Llamando cuando la pantalla está completa."""
        self.cargar_distribuciones()

    def editar_distribucion(self, dist_id):
        """Navega al formulario para editar la distribución."""
        logger.info(f"Editando distribución ID: {dist_id}")
        dist_screen = self.manager.get_screen('distribuciones')
        dist_screen.preparar_edicion(dist_id)
        self.manager.current = 'distribuciones'

    def confirmar_eliminacion(self, dist_id):
        """Muestra confirmación antes de eliminar."""
        StyledPopup.mostrar_confirmacion(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar la distribución ID {dist_id}?",
            on_confirm=lambda: self.eliminar_distribucion(dist_id)
        )

    def eliminar_distribucion(self, dist_id):
        """Elimina la distribución y refresca la lista."""
        exito, mensaje = self.controlador.eliminar_distribucion(dist_id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_distribuciones()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def volver(self, instance):
        """Regresa a la pantalla de distribuciones"""
        self.manager.current = 'distribuciones'

