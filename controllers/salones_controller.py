import logging
from models.salones import Salon
from models.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonesController:
    def __init__(self, vista=None):
        self.vista = vista 

    def crear_salon(self, salon, edad):

        # Validación de datos
        if not salon:
            self.vista.mostrar_error("El nombre del salón es obligatorio.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del salón es obligatoria.")
            return
        db = SessionLocal()
        salon_creado = False
        try:
            with db.begin():
                nuevo_salon = Salon(nombre=salon, edad=edad)
                db.add(nuevo_salon)
                logger.info(f"Salón creado: {nuevo_salon.id}")
                salon_creado = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear salón: {e}")
            self.vista.mostrar_error(f"Error al crear salón: {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if salon_creado:
                self.vista.mostrar_exito("Salón creado exitosamente.")

    def actualizar_salon(self, id, salon, edad):
        # Validación de datos
        if not id:
            self.vista.mostrar_error("El ID del salón es obligatorio.")
            return
        if not salon:
            self.vista.mostrar_error("El nombre del salón es obligatorio.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del salón es obligatoria.")
            return

        db = SessionLocal()
        salon_actualizado = False
        try:
            with db.begin():
                salon_existente = db.query(Salon).filter(Salon.id == id).first()
                if not salon_existente:
                    self.vista.mostrar_error("El salón no existe.")
                    return
                salon_existente.nombre = salon
                salon_existente.edad = edad
                logger.info(f"Salón actualizado: {salon_existente.id}")
                salon_actualizado = True
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar salón: {e}")
            self.vista.mostrar_error(f"Error al actualizar salón: {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if salon_actualizado:
                self.vista.mostrar_exito("Salón actualizado exitosamente.")

    def eliminar_salon(self, id):
        # Validación de datos
        if not id:
            self.vista.mostrar_error("El ID del salón es obligatorio.")
            return

        db = SessionLocal()
        eliminar_salon = False
        try:
            with db.begin():
                salon_existente = db.query(Salon).filter(Salon.id == id).first()
                if not salon_existente:
                    self.vista.mostrar_error("El salón no existe.")
                    return
                db.delete(salon_existente)
                logger.info(f"Salón eliminado: {salon_existente.id}")
                self.mostrar_exito(f"Salón eliminado: {salon_existente.id}")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar salón: {e}")
            self.vista.mostrar_error(f"Error al eliminar salón {e}. Inténtalo de nuevo.")
        finally:
            db.close()
            if eliminar_salon:
                self.vista.mostrar_exito("Salón eliminado exitosamente.")

    def listar_salones(self, from_button=False):
        """
        Método para listar los salones y manejar errores.
        """
        db = SessionLocal()
        try:
            salones = db.query(Salon).all()  
            logger.info(f"{len(salones)} salones obtenidos de la base de datos.")
            if hasattr(vista, 'actualizar_lista_salones'):
                vista.actualizar_lista_salones(salones)
            else:
                raise AttributeError("The provided view does not have 'actualizar_lista_salones' method.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones: {e}")
            self.vista.mostrar_error(f"Error al listar salones {e}. Inténtalo de nuevo.")
            return []
        finally:
            db.close()
    
    def listar_salones_button_handler(self):
        """Handler for the 'List' button in the salones view."""
        self.listar_salones(self.vista)

    def obtener_salon(self, id):
        """Retrieve a single salon by its ID."""
        db = SessionLocal()
        try:
            salon = db.query(Salon).filter(Salon.id == id).first()
            if salon:
                logger.info(f"Salon encontrado: {salon.salon}")
                self.mostrar_salon(f"Salón encontrado: {salon.salon}")
                return salon
            else:
                logger.warning(f"Salon con ID {id} no encontrado.")
                self.vista.mostrar_ernor(f"Error al encontrar salón: {id}, no existe.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener el salón con ID {id}: {e}")
            self.vista.mostrar_ernor(f"Error al obtener el salón con ID {id}: {e}.")
            return None
        finally:
            db.close()
    
    def mostrar_area(self, mensaje):
        """Display a popup with the area message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)
        )
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0, 119/255, 194/255, 1),
            size_hint_y=None,
            height=50
        )
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Información del Área",
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def mostrar_ernor(self, mensaje):
        """Display a popup with the error message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)
        )
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            background_normal='',
            background_color=(0, 119/255, 194/255, 1),
            size_hint_y=None,
            height=50
        )
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Error",  
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()