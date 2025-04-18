from controllers.base_controller import BaseController
from models.areas import Area
from components.styled_popup import StyledPopup
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AreasController(BaseController):
    def __init__(self, vista):
        super().__init__(vista, Area)

    def crear_area(self, nombre):
        if not nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del área es obligatorio.", tipo="error")
            return

        db = SessionLocal()
        area_creada = False
        try:
            with db.begin():
                area = Area(area=nombre)
                db.add(area)
                logger.info(f"Área creada: {nombre}")
                area_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear área: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al crear área: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if area_creada:
                StyledPopup.mostrar_popup("Éxito", "Área creada exitosamente.", tipo="success")

    def actualizar_area(self, id, nombre):
        #Validar los datos
        if not id:
            StyledPopup.mostrar_popup("Error", "El id del área es obligatorio.", tipo="error")
            return
        if not nombre:
            StyledPopup.mostrar_popup("Error", "El nombre del área es obligatorio.", tipo="error")
            return

        db = SessionLocal()
        area_actualizada = False
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    area.area = nombre  
                    logger.info(f"Área actualizada: {nombre}")
                    area_actualizada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Área no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar área: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al actualizar área: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if area_actualizada:
                StyledPopup.mostrar_popup("Éxito", "Área actualizada exitosamente.", tipo="success")
                
    def eliminar_area(self, id):
        db = SessionLocal()
        area_eliminada = False
        try:
            with db.begin():
                area = db.query(Area).filter(Area.id == id).first()
                if area:
                    db.delete(area)
                    logger.info(f"Área eliminada: {area.area}")
                    area_eliminada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Área no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar área: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al eliminar área: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            logger.info("Conexión cerrada")
            if area_eliminada:
                self.mostrar_popup("Éxito", "Área eliminada exitosamente.", tipo="success")

    def listar_areas(self, vista):
        """Método para listar las áreas y manejar errores.."""
        db = SessionLocal()
        try:
            areas = db.query(Area).all()
            logger.info(f"{len(areas)} áreas obtenidas de la base de datos.")
            if hasattr(vista, 'actualizar_lista_areas'):
                vista.actualizar_lista_areas(areas)
            else:
                raise AttributeError("La vista no tiene un método 'actualizar_lista_areas'.")
            return areas
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener áreas: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al obtener área: {e}. Inténtalo de nuevo.", tipo="error")
            return []
        finally:
            db.close()
            logger.info("Conexión cerrada")

    def listar_areas_button_handler(self):
        """Handler for the 'List' button in the areas view."""
        self.listar_areas(self.vista)

    def buscar_area(self, id=None, nombre=None):
        """
        Busca un área por ID o nombre y muestra la información en un popup.
        :param id: ID del área a buscar.
        :param nombre: Nombre del área a buscar.
        """
        area = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="area")
        if area:
            # Mostrar la información del área en un popup
            StyledPopup.mostrar_popup(
                "Información del Área",
                f"ID: {area.id}\nNombre: {area.area}",
                tipo="info"
            )
        else:
            # Mostrar un mensaje de error si no se encuentra el área
            if id:
                StyledPopup.mostrar_popup("Error", f"No existe un área con ID {id}.", tipo="error")
            elif nombre:
                StyledPopup.mostrar_popup("Error", f"No existe un área con nombre '{nombre}'.", tipo="error")