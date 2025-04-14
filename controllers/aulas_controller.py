import logging
from models.aulas import Aula
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulasController:
    def __init__(self, vista):
        self.vista = vista

    def crear_aula(self, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, fecha, id_salon):
        # ... (Validación de datos)
        if not auxiliar:
            self.vista.mostrar_error("El auxiliar del aula es obligatorio.")
            return
        if not capitan:
            self.vista.mostrar_error("El capitán del aula es obligatorio.")
            return
        if not colaborador:
            self.vista.mostrar_error("El colaborador del aula es obligatorio.")
            return
        if not condicion:
            self.vista.mostrar_error("La condición del aula es obligatoria.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del aula es obligatoria.")
            return
        if not maestra:
            self.vista.mostrar_error("La maestra del aula es obligatoria.")
            return
        if not ninos:
            self.vista.mostrar_error("El número de niños del aula es obligatorio.")
            return
        if not ninas:
            self.vista.mostrar_error("El número de niñas del aula es obligatorio.")
            return
        if not subcapitan:
            self.vista.mostrar_error("El subcapitán del aula es obligatorio.")
            return
        if not fecha:
            self.vista.mostrar_error("La fecha del aula es obligatoria.")
            return
        
        # Validar que el salón exista
        db = SessionLocal()
        salon = db.query(Salon).filter(Salon.id == id_salon).first()
        if not salon:
            self.vista.mostrar_error("El salón asociado no existe.")
            db.close()
            return

        db = SessionLocal()
        aula_creada = False
        try:
            with db.begin():
                # ... (Creación de aula)
                aula = Aula(
                    auxiliar = auxiliar,
                    capitan = capitan,
                    colaborador = colaborador,
                    condicion = condicion,
                    edad = edad,
                    maestra = maestra,
                    ninos = ninos,
                    ninas = ninas,
                    subcapitan = subcapitan,
                    fecha = datetime.strptime(fecha, '%Y-%m-%d').date(),
                )
                db.add(aula)
                logger.info(f"Aula creada: {aula.id}")
                aula_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear aula: {e}")
            self.vista.mostrar_error("Error al crear aula. Inténtalo de nuevo.")
        finally:
            db.close()
            if aula_creada:
                self.vista.mostrar_exito("Aula creada exitosamente.")

    def actualizar_aula(self, id, auxiliar, capitan, colaborador, condicion, edad, maestra, ninos, ninas, subcapitan, fecha, id_salon):
        # Validación de datos
        if not auxiliar:
            self.vista.mostrar_error("El auxiliar del aula es obligatorio.")
            return
        if not capitan:
            self.vista.mostrar_error("El capitán del aula es obligatorio.")
            return
        if not colaborador:
            self.vista.mostrar_error("El colaborador del aula es obligatorio.")
            return
        if not condicion:
            self.vista.mostrar_error("La condición del aula es obligatoria.")
            return
        if not edad:
            self.vista.mostrar_error("La edad del aula es obligatoria.")
            return
        if not maestra:
            self.vista.mostrar_error("La maestra del aula es obligatoria.")
            return
        if not ninos:
            self.vista.mostrar_error("El número de niños del aula es obligatorio.")
            return
        if not ninas:
            self.vista.mostrar_error("El número de niñas del aula es obligatorio.")
            return
        if not subcapitan:
            self.vista.mostrar_error("El subcapitán del aula es obligatorio.")
            return
        if not fecha:
            self.vista.mostrar_error("La fecha del aula es obligatoria.")
            return

        # Validar que el salón exista
        db = SessionLocal()
        try:
            salon = db.query(Salon).filter(Salon.id == id_salon).first()
            if not salon:
                self.vista.mostrar_error("El salón asociado no existe.")
                return

            aula_actualizada = False
            with db.begin():
                # Buscar el aula
                aula = db.query(Aula).filter(Aula.id == id).first()
                if aula:
                    # Actualizar los atributos del aula
                    aula.auxiliar = auxiliar
                    aula.capitan = capitan
                    aula.colaborador = colaborador
                    aula.condicion = condicion
                    aula.edad = edad
                    aula.maestra = maestra
                    aula.ninos = ninos
                    aula.ninas = ninas
                    aula.subcapitan = subcapitan
                    aula.fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                    aula.id_salon = id_salon
                    aula_actualizada = True
                    logger.info(f"Aula actualizada: {aula.id}")
                else:
                    self.vista.mostrar_error("Aula no encontrada.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar aula: {e}")
            self.vista.mostrar_error("Error al actualizar aula. Inténtalo de nuevo.")
        finally:
            db.close()

        if aula_actualizada:
            self.vista.mostrar_exito("Aula actualizada exitosamente.")

        def eliminar_aula(self, id):
            # Validación de ID
            if not id:
                self.vista.mostrar_error("El ID del aula es obligatorio.")
                return

            db = SessionLocal()
            aula_eliminada = False
            try:
                with db.begin():
                    # ... (Eliminación de aula)
                    aula = db.query(Aula).filter(Aula.id == id).first()
                    if aula:
                        db.delete(aula)
                        aula_eliminada = True
                        logger.info(f"Aula eliminada: {aula.id}")
                    else:
                        self.vista.mostrar_error("Aula no encontrada.")
            except SQLAlchemyError as e:
                logger.error(f"Error al eliminar aula: {e}")
                self.vista.mostrar_error("Error al eliminar aula. Inténtalo de nuevo.")
            finally:
                db.close()
                if aula_eliminada:
                    self.vista.mostrar_exito("Aula eliminada exitosamente.")

    def listar_aulas(self):
        db: SessionLocal()
        try:
            aulas = db.query(Aula).all()
            logger.info(f"{len(aulas)} aulas obtenidas de la base de datos.")
            if hasattr(self.vista, 'actualizar_lista'):
                self.vista.actualizar_lista(aulas)
            else:
                raise AttributeError("La vista no tiene el método 'actualizar_lista'.")
            return aulas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar aulas: {e}")
            self.vista.mostrar_error("Error al listar aulas. Inténtalo de nuevo.")
            return []
        finally:
            db.close()
    
    def listar_aulas_button_handler(self):
        """Método para manejar el evento de listar aulas."""
        self.listar_aulas(self.vista)

    def obtener_aula(self, id=None, fecha=None):
        if not id and not fecha:
            self.vista.mostrar_error("Debes proporcionar un ID o una fecha para obtener el aula.")
            return None
        db = SessionLocal()
        try:
            db.query(Aula)
            if id:
                aula = db.query(Aula).filter(Aula.id == id).first()
            else:
                aula = db.query(Aula).filter(Aula.fecha == fecha).first()

            if aula:
                logger.info(f"Aula encontrada: {aula.id}")
                self.mostrar_aula(f"Aula encontrada: {aula.id}, {aula.fecha}")
                return aula
            else:
                if id:
                    logger.warning(f"Aula con ID {id} no encontrada.")
                    self.vista.mostrar_error("Aula no encontrada.")
                elif fecha:
                    logger.warning(f"Aula con fecha {fecha} no encontrada.")
                    self.vista.mostrar_error("Aula no encontrada.")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener aula: {e}")
            self.vista.mostrar_error("Error al obtener aula. Inténtalo de nuevo.")
            return None
        finally:
            db.close()
    
    def mostrar_aula(self, mensaje):
        """Display a popup with the aula message."""
        class StyledPopup(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with self.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    self.bg_color = Color(0.102, 0.2, 0.396, 1)  # Updated background color
                    self.bg_rect = Rectangle(pos=self.pos, size=self.size)
                    self.bind(pos=self._update_rect, size=self._update_rect)

            def _update_rect(self, *args):
                self.bg_rect.pos = self.pos
                self.bg_rect.size = self.size

        popup_layout = StyledPopup(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(
            text=mensaje,
            size_hint=(1, 0.8),
            color=(1, 1, 1, 1)  # Updated text color to white
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
            title="Información del Aula",
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),  # Updated title text color to white
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()
    
    def get_db_session(self):
        """Obtener una nueva Sesión de Base de Datos."""
        return SessionLocal()