import logging
from controllers.base_controller import BaseController
from models.salones import Salon
from sqlalchemy.exc import SQLAlchemyError
from components.styled_popup import StyledPopup

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonesController(BaseController):
    def __init__(self, vista=None, session=None):
        super().__init__(vista, Salon, session)
        self.session = session
        logger.info("Inicializando AulasController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        self.vista = vista
        logger.info("SalonesController inicializado con éxito.")

    def crear_salon(self, nombre, edad):
        if not nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del salón es obligatorio.", tipo="error")
            return
        if not edad:
            StyledPopup.mostrar_popup("Error", "La edad del salón es obligatoria.", tipo="error")
            return

        db = self.get_db_session()  # Usar el método de la clase madre
        salon_creado = False
        try:
            with db.begin():
                salon = Salon(salon=nombre, edad=edad)
                db.add(salon)
                logger.info(f"Salón creado: {nombre}")
                salon_creado = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear salón: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al crear salón: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if salon_creado:
                StyledPopup.mostrar_popup("Éxito", "Salón creado exitosamente.", tipo="success")

    def actualizar_salon(self, id, nombre, edad):
        #Validar los datos
        if not id:
            StyledPopup.mostrar_popup("Error", "El id del salón es obligatorio.", tipo="error")
            return
        if not nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del salón es obligatorio.", tipo="error")
            return
        if not edad:
            StyledPopup.mostrar_popup("Error", "La edad del saón es obligatoria.", tipo="error")
            return

        db = self.get_db_session()  # Usar el método de la clase madre
        salon_actualizado = False
        try:
            with db.begin():
                salon = db.query(Salon).filter(Salon.id == id).first()
                if salon:
                    salon.salon = nombre  
                    salon.edad = edad
                    logger.info(f"Salón actualizado: {nombre}")
                    salon_actualizado = True
                else:
                    StyledPopup.mostrar_popup("Error", "Salón no encontrado.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar salón: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al actualizar salón: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if salon_actualizado:
                StyledPopup.mostrar_popup("Éxito", "Salón actualizado exitosamente.", tipo="success")
                
    def eliminar_salon(self, id):
        db = self.get_db_session()  # Usar el método de la clase madre
        salon_eliminado = False
        try:
            with db.begin():
                salon = db.query(Salon).filter(Salon.id == id).first()
                if salon:
                    db.delete(salon)
                    logger.info(f"Salón eliminada: {area.area}")
                    salon_eliminado = True
                else:
                    StyledPopup.mostrar_popup("Error", "Salón no encontrado.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar salón: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al eliminar salón: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            logger.info("Conexión cerrada")
            if salon_eliminado:
                StyledPopup.mostrar_popup("Éxito", "Salón eliminada exitosamente.", tipo="success")

    def listar_salones(self, vista):
        """Método para listar las saloness y manejar errores."""
        db = self.get_db_session()  # Usar el método de la clase madre
        try:
            salones = db.query(Salon).all()
            logger.info(f"{len(salones)} salones obtenidos de la base de datos.")
            if hasattr(vista, 'actualizar_lista_salones'):
                vista.actualizar_lista_salones(salones)
            else:
                raise AttributeError("La vista no tiene un método 'actualizar_lista_salones'.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener salones: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al obtener salón: {e}. Inténtalo de nuevo.", tipo="error")
            return []
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def listar_salones_button_handler(self):
        """Manejador para el botón que despliega la vista 'Lista' en salones."""
        self.listar_salones(self.vista)

    def buscar_salon(self, id=None, nombre=None):
        """
        Busca un salón por ID o nombre y muestra la información en un popup.
        :param id: ID del salón a buscar.
        :param nombre: Nombre del salón a buscar.
        """
        #Validar datos
        if not id and not nombre:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o un nombre para buscar el salón.", tipo="error")
            return
        if id and not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID debe ser un número entero.", tipo="error")
            return
        if nombre and not isinstance(nombre, str):
            StyledPopup.mostrar_popup("Error", "El nombre debe ser una cadena de texto.", tipo="error")
            return
        # Buscar salon 
        salon = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="salon")
        if salon:
            # Mostrar la información del salón en un popup
            StyledPopup.mostrar_popup(
                "Información del Salón",
                f"ID: {salon.id}\nNombre: {salon.salon}",
                tipo="info"
            )
        else:
            # Mostrar un mensaje de error si no se encuentra el salón
            if id:
                StyledPopup.mostrar_popup("Error", f"No existe un salón con ID {id}.", tipo="error")
            elif nombre:
                StyledPopup.mostrar_popup("Error", f"No existe un salón con nombre '{nombre}'.", tipo="error")